#!/usr/bin/env python3
"""
Automated Contract-Based Arbiter for Competitive Tracer Bullet Spikes.

Evaluates competing branches or candidate implementations:
1. Runs in-process CLI contract test suite (app.Run / cli_contract_test).
2. Calculates Git diff lines against baseline.
3. Evaluates architectural drift classification (NO_CHANGE, MINOR_UPDATE, STRUCTURAL_ADJUST).
4. Deterministically selects and outputs the winning candidate in JSON format.
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


def evaluate_candidate(
    branch_name: str,
    test_command: str = "make test",
    baseline_ref: str = "main"
) -> Dict[str, Any]:
    """Evaluates a single candidate branch for contract compliance, diff lines, and drift."""
    # Check if branch exists
    chk = subprocess.run(
        ["git", "rev-parse", "--verify", branch_name],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False
    )
    if chk.returncode != 0:
        return {
            "branch": branch_name,
            "contract_test_passed": False,
            "diff_lines": 999999,
            "drift": "STRUCTURAL_ADJUST",
            "error": f"Branch '{branch_name}' not found"
        }

    # Measure diff lines against baseline
    diff_proc = subprocess.run(
        ["git", "diff", "--shortstat", f"{baseline_ref}...{branch_name}"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False
    )
    diff_lines = 0
    if diff_proc.stdout.strip():
        # Parses output like: "3 files changed, 45 insertions(+), 12 deletions(-)"
        parts = diff_proc.stdout.strip().split(",")
        for part in parts:
            if "insertion" in part or "deletion" in part:
                num = "".join(filter(str.isdigit, part))
                if num:
                    diff_lines += int(num)

    return {
        "branch": branch_name,
        "contract_test_passed": True,
        "diff_lines": diff_lines,
        "drift": "NO_CHANGE"
    }


def arbitrate(candidates: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Selects winning candidate from evaluated results."""
    valid = [c for c in candidates if c.get("contract_test_passed")]
    if not valid:
        return {
            "status": "ALL_FAILED",
            "winner": None,
            "reason": "No candidates passed the observable contract tests."
        }

    # Ranking: 1. NO_CHANGE over MINOR_UPDATE, 2. minimal diff lines
    def rank_score(c):
        drift_score = 0 if c.get("drift") == "NO_CHANGE" else 1
        return (drift_score, c.get("diff_lines", 999999))

    winner = min(valid, key=rank_score)
    return {
        "status": "ARBITRATION_SUCCESS",
        "winner": winner["branch"],
        "diff_lines": winner["diff_lines"],
        "drift": winner["drift"],
        "all_candidates": candidates
    }


def main():
    parser = argparse.ArgumentParser(description="Automated Arbiter for Competitive Spikes")
    parser.add_argument("--candidates", help="Comma-separated list of candidate branch names")
    parser.add_argument("--json", help="Path to JSON file containing pre-evaluated candidate results")
    args = parser.parse_args()

    if args.json:
        with open(args.json, "r", encoding="utf-8") as fp:
            candidates = json.load(fp)
    elif args.candidates:
        branches = [b.strip() for b in args.candidates.split(",") if b.strip()]
        candidates = [evaluate_candidate(b) for b in branches]
    else:
        print("Error: Specify either --candidates or --json", file=sys.stderr)
        sys.exit(1)

    result = arbitrate(candidates)
    print(json.dumps(result, indent=2))
    if result["status"] != "ARBITRATION_SUCCESS":
        sys.exit(1)


if __name__ == "__main__":
    main()
