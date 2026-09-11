#!/usr/bin/env python3
"""
Deterministic Evaluation Harness for Agentic Architecture State Transitions.

Simulates and verifies:
1. Scenario 1 (Happy Path): Standard single-agent canonical forward traversal.
2. Scenario 2 (Back Edge): Review defect injection correctly routes back to TRACER_BULLET.
3. Scenario 3 (Drift Halt): Structural adjustment immediately halts at HUMAN_DECISION gate.
4. Scenario 4 (Illegal Transition): Prohibited shortcuts/jumps are rejected with TransitionRejectedError.
5. Scenario 5 (Economy Profile Fallback): Human lever forces single-agent mode, saving tokens.
6. Scenario 6 (Parallel Investigation Fan-out/Fan-in): Deduplicates facts and merges unknowns.
7. Scenario 7 (Competitive Tracer Arbitration): Automated contract test selects minimal-drift branch.
8. Scenario 8 (Specialist Review Merging): Merges multi-angle reviews and routes back-edge on defect.
9. Scenario 9 (Anti-Pattern Rejection): Blocks parallel mutations on shared workspaces.
"""

import json
import sys
import unittest
from pathlib import Path
from typing import Any, Dict, List, Optional

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
MANIFEST_PATH = REPO_ROOT / "graph" / "canonical_graph.json"


class TransitionRejectedError(Exception):
    """Raised when an illegal state transition is attempted."""
    pass


class TerminalHaltReached(Exception):
    """Raised when a terminal gate (e.g., HUMAN_DECISION) is reached and automated transitions are blocked."""
    pass


class SharedWorkspaceMutationError(Exception):
    """Raised when parallel agents attempt to mutate a shared workspace without branch isolation."""
    pass


class StateGraphSimulator:
    """Deterministic state machine simulator for ai-inst workflow graph."""

    def __init__(self, manifest_path: Path = MANIFEST_PATH, profile: str = "balanced"):
        if not manifest_path.is_file():
            raise FileNotFoundError(f"Manifest not found: {manifest_path}")
        with open(manifest_path, "r", encoding="utf-8") as fp:
            self.manifest = json.load(fp)

        self.nodes = self.manifest.get("nodes", {})
        self.edges = self.manifest.get("edges", [])
        self.profiles = self.manifest.get("execution_profiles", {})
        if profile not in self.profiles:
            raise ValueError(f"Unknown execution profile '{profile}'. Allowed: {list(self.profiles.keys())}")
        self.profile = profile

        self.current_state = self.manifest.get("entry_node", "INVESTIGATION")
        self.history: List[str] = [self.current_state]
        self.is_halted: bool = False
        self.subagents_spawned_count: int = 0

    def transition(self, next_state: str, condition: Optional[str] = None) -> str:
        """Attempt to transition to next_state under an optional condition."""
        if self.is_halted:
            raise TerminalHaltReached(
                f"State machine is halted at {self.current_state} (Human Gate). "
                f"Cannot transition to {next_state} without human decision."
            )

        # Validate that edge exists from self.current_state to next_state
        candidate_edges = [
            e for e in self.edges
            if e["from"] == self.current_state and e["to"] == next_state
        ]

        if not candidate_edges:
            raise TransitionRejectedError(
                f"Illegal transition rejected: {self.current_state} -> {next_state}. "
                f"No matching edge defined in canonical graph manifest."
            )

        if condition is not None:
            matching_conditions = [e for e in candidate_edges if e.get("condition") == condition]
            if not matching_conditions:
                allowed_conditions = [e.get("condition") for e in candidate_edges]
                raise TransitionRejectedError(
                    f"Invalid condition '{condition}' for transition {self.current_state} -> {next_state}. "
                    f"Allowed conditions: {allowed_conditions}"
                )

        self.current_state = next_state
        self.history.append(next_state)

        # Check if entered a human gate / terminal halt state
        node_info = self.nodes.get(next_state, {})
        if node_info.get("human_gate") or node_info.get("permission_level") == "TERMINAL_HALT":
            self.is_halted = True

        return self.current_state

    def dispatch_subagents(self, roles: List[str], workspace_mode: str = "branch") -> Dict[str, Any]:
        """Dispatch subagents according to node topology and active execution profile."""
        profile_config = self.profiles[self.profile]
        node_info = self.nodes.get(self.current_state, {})
        node_topology = node_info.get("execution_topology", "SINGLE_AGENT")

        # Economy mode: always collapse to sequential single-agent (token saving lever)
        if not profile_config.get("allow_subagents", True) or self.profile == "economy":
            return {
                "status": "COLLAPSED_TO_SINGLE_AGENT",
                "spawned": 0,
                "profile": self.profile,
                "reason": "Economy profile strictly suppresses subagents to preserve tokens and latency."
            }

        # Anti-pattern check: Mutating shared workspace concurrently
        if node_topology == "SINGLE_AGENT" and workspace_mode == "inherit":
            raise SharedWorkspaceMutationError(
                f"Cannot concurrently mutate shared workspace in state '{self.current_state}' "
                f"without isolated branch workspaces."
            )

        max_workers = profile_config.get("max_parallel_workers", 3)
        actual_workers = roles[:max_workers]
        self.subagents_spawned_count += len(actual_workers)

        return {
            "status": "DISPATCHED",
            "spawned": len(actual_workers),
            "workers": actual_workers,
            "workspace_mode": workspace_mode,
            "topology": node_topology
        }

    @staticmethod
    def reduce_investigation_facts(worker_fact_sheets: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Fan-in Reducer for INVESTIGATION: Deduplicates facts and merges unknowns."""
        unified_facts = set()
        unified_unknowns = set()

        for sheet in worker_fact_sheets:
            for fact in sheet.get("facts", []):
                unified_facts.add(fact)
            for unknown in sheet.get("unknowns", []):
                unified_unknowns.add(unknown)

        return {
            "facts": sorted(list(unified_facts)),
            "unknowns": sorted(list(unified_unknowns)),
            "count_facts": len(unified_facts),
            "status": "FACTS_ESTABLISHED"
        }

    @staticmethod
    def arbitrate_tracer_spikes(candidates: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Automated Arbiter for competitive TRACER_BULLET spikes."""
        valid_candidates = [c for c in candidates if c.get("contract_test_passed")]
        if not valid_candidates:
            return {"winner": None, "status": "ALL_FAILED", "reason": "No branch passed contract tests"}

        # Sort key: 1. NO_CHANGE drift first, 2. lowest diff lines
        def candidate_score(c):
            drift_score = 0 if c.get("drift") == "NO_CHANGE" else 1
            return (drift_score, c.get("diff_lines", 999999))

        winner = min(valid_candidates, key=candidate_score)
        return {
            "winner": winner["branch"],
            "status": "ARBITRATION_SUCCESS",
            "diff_lines": winner["diff_lines"],
            "drift": winner["drift"]
        }

    @staticmethod
    def merge_review_findings(reviewer_reports: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Fan-in Merger for specialist REVIEW reports."""
        all_findings = []
        has_defect = False

        for report in reviewer_reports:
            for finding in report.get("findings", []):
                all_findings.append(finding)
                if finding.get("severity") in ("CRITICAL", "BLOCKER"):
                    has_defect = True

        severity_order = {"BLOCKER": 0, "CRITICAL": 1, "WARNING": 2, "INFO": 3}
        all_findings.sort(key=lambda f: severity_order.get(f.get("severity", "INFO"), 99))

        return {
            "findings": all_findings,
            "has_defect": has_defect,
            "next_condition": "DEFECT_FOUND" if has_defect else "QUALITY_CLEARED"
        }


class EvaluationHarnessScenarios(unittest.TestCase):
    """Evaluation scenarios verifying state machine and multi-agent invariants."""

    def test_scenario_1_happy_path(self):
        """Scenario 1 (Happy Path): Standard end-to-end development cycle."""
        sim = StateGraphSimulator()
        self.assertEqual(sim.current_state, "INVESTIGATION")

        sim.transition("TRACER_BULLET", condition="FACTS_ESTABLISHED")
        sim.transition("TEST_FIRST", condition="CONTRACT_LOCKED")
        sim.transition("REVIEW", condition="TESTS_EXPANDED")
        sim.transition("ARCHITECTURE", condition="QUALITY_CLEARED")
        sim.transition("DEAD_CODE_CLEANUP", condition="NO_CHANGE_OR_MINOR")
        sim.transition("PRE_COMMIT_LEAK_REVIEW", condition="CLEANUP_DONE")

        self.assertFalse(sim.is_halted)
        self.assertEqual(sim.current_state, "PRE_COMMIT_LEAK_REVIEW")

    def test_scenario_2_back_edge_on_defect(self):
        """Scenario 2 (Back Edge): Defect found in review properly loops back to TRACER_BULLET."""
        sim = StateGraphSimulator()
        sim.transition("TRACER_BULLET", condition="FACTS_ESTABLISHED")
        sim.transition("TEST_FIRST", condition="CONTRACT_LOCKED")
        sim.transition("REVIEW", condition="TESTS_EXPANDED")

        # Review discovers defect -> Must not patch ad-hoc, must return to TRACER_BULLET
        sim.transition("TRACER_BULLET", condition="DEFECT_FOUND")
        self.assertEqual(sim.current_state, "TRACER_BULLET")

        # Resume from tracer repair
        sim.transition("TEST_FIRST", condition="CONTRACT_LOCKED")
        sim.transition("REVIEW", condition="TESTS_EXPANDED")
        sim.transition("ARCHITECTURE", condition="QUALITY_CLEARED")
        sim.transition("DEAD_CODE_CLEANUP", condition="NO_CHANGE_OR_MINOR")
        sim.transition("PRE_COMMIT_LEAK_REVIEW", condition="CLEANUP_DONE")

        self.assertFalse(sim.is_halted)

    def test_scenario_3_structural_adjust_halt(self):
        """Scenario 3 (Drift Halt): STRUCTURAL_ADJUST strictly triggers HUMAN_DECISION halt."""
        sim = StateGraphSimulator()
        sim.transition("TRACER_BULLET", condition="FACTS_ESTABLISHED")
        sim.transition("TEST_FIRST", condition="CONTRACT_LOCKED")
        sim.transition("REVIEW", condition="TESTS_EXPANDED")
        sim.transition("ARCHITECTURE", condition="QUALITY_CLEARED")

        # Architectural drift detected: STRUCTURAL_ADJUST
        sim.transition("HUMAN_DECISION", condition="STRUCTURAL_ADJUST")
        self.assertTrue(sim.is_halted)
        self.assertEqual(sim.current_state, "HUMAN_DECISION")

        # Automated attempts to bypass human decision must raise TerminalHaltReached
        with self.assertRaises(TerminalHaltReached):
            sim.transition("DEAD_CODE_CLEANUP")

        with self.assertRaises(TerminalHaltReached):
            sim.transition("PRE_COMMIT_LEAK_REVIEW")

    def test_scenario_4_illegal_transitions_rejected(self):
        """Scenario 4 (Illegal Transition): Premature shortcuts and contract bypasses are rejected."""
        sim = StateGraphSimulator()

        # Cannot skip directly from INVESTIGATION to PRE_COMMIT_LEAK_REVIEW
        with self.assertRaises(TransitionRejectedError):
            sim.transition("PRE_COMMIT_LEAK_REVIEW")

        # Cannot skip directly from INVESTIGATION to DEAD_CODE_CLEANUP
        with self.assertRaises(TransitionRejectedError):
            sim.transition("DEAD_CODE_CLEANUP")

        sim.transition("TRACER_BULLET", condition="FACTS_ESTABLISHED")
        with self.assertRaises(TransitionRejectedError):
            sim.transition("ARCHITECTURE")

    def test_scenario_5_economy_profile_fallback(self):
        """Scenario 5 (Economy Profile Fallback): Human lever forces single-agent mode without subagents."""
        sim = StateGraphSimulator(profile="economy")
        self.assertEqual(sim.current_state, "INVESTIGATION")

        # Request to dispatch subagents under economy mode must collapse to single-agent
        result = sim.dispatch_subagents(["code_ast_inspector", "log_history_analyst"])
        self.assertEqual(result["status"], "COLLAPSED_TO_SINGLE_AGENT")
        self.assertEqual(result["spawned"], 0)
        self.assertEqual(sim.subagents_spawned_count, 0)

        # Runs full cycle sequentially on primary agent
        sim.transition("TRACER_BULLET", condition="FACTS_ESTABLISHED")
        sim.transition("TEST_FIRST", condition="CONTRACT_LOCKED")
        sim.transition("REVIEW", condition="TESTS_EXPANDED")
        sim.transition("ARCHITECTURE", condition="QUALITY_CLEARED")
        sim.transition("DEAD_CODE_CLEANUP", condition="NO_CHANGE_OR_MINOR")
        sim.transition("PRE_COMMIT_LEAK_REVIEW", condition="CLEANUP_DONE")
        self.assertEqual(sim.subagents_spawned_count, 0)

    def test_scenario_6_parallel_investigation_fan_out_fan_in(self):
        """Scenario 6 (Parallel Investigation Fan-out/Fan-in): Reducer deduplicates facts."""
        sim = StateGraphSimulator(profile="balanced")
        roles = ["code_ast_inspector", "log_history_analyst", "external_doc_researcher"]
        dispatch = sim.dispatch_subagents(roles, workspace_mode="branch")
        self.assertEqual(dispatch["status"], "DISPATCHED")
        self.assertEqual(dispatch["spawned"], 3)

        # Simulated reports from 3 subagents
        reports = [
            {"facts": ["CLI argument 'convert' exists", "AST confirms no format flag"], "unknowns": ["Memory constraint"]},
            {"facts": ["AST confirms no format flag", "log/slog format is JSON"], "unknowns": ["Throughput target"]},
            {"facts": ["RFC 8259 compliance needed"], "unknowns": ["Memory constraint"]}
        ]

        reduced = StateGraphSimulator.reduce_investigation_facts(reports)
        self.assertEqual(reduced["count_facts"], 4)
        self.assertEqual(len(reduced["unknowns"]), 2)
        self.assertEqual(reduced["status"], "FACTS_ESTABLISHED")

        sim.transition("TRACER_BULLET", condition=reduced["status"])
        self.assertEqual(sim.current_state, "TRACER_BULLET")

    def test_scenario_7_competitive_tracer_arbitration(self):
        """Scenario 7 (Competitive Tracer Arbitration): Contract test selects minimal-drift branch."""
        candidates = [
            {"branch": "spike/in_memory_channel", "contract_test_passed": True, "diff_lines": 35, "drift": "NO_CHANGE"},
            {"branch": "spike/redis_queue", "contract_test_passed": True, "diff_lines": 140, "drift": "MINOR_UPDATE"},
            {"branch": "spike/broken_syntax", "contract_test_passed": False, "diff_lines": 20, "drift": "NO_CHANGE"}
        ]

        arbiter_decision = StateGraphSimulator.arbitrate_tracer_spikes(candidates)
        self.assertEqual(arbiter_decision["status"], "ARBITRATION_SUCCESS")
        self.assertEqual(arbiter_decision["winner"], "spike/in_memory_channel")
        self.assertEqual(arbiter_decision["drift"], "NO_CHANGE")

    def test_scenario_8_specialist_review_merging(self):
        """Scenario 8 (Specialist Review Merging): Aggregates defects and routes back-edge."""
        sim = StateGraphSimulator(profile="deep_parallel")
        sim.transition("TRACER_BULLET", condition="FACTS_ESTABLISHED")
        sim.transition("TEST_FIRST", condition="CONTRACT_LOCKED")
        sim.transition("REVIEW", condition="TESTS_EXPANDED")

        # 2 Specialist reviews
        concurrency_review = {
            "findings": [{"id": "RACE-001", "severity": "CRITICAL", "message": "Data race detected in pool.go"}]
        }
        security_review = {
            "findings": [{"id": "SEC-001", "severity": "INFO", "message": "No secret leaks in diff"}]
        }

        merged = StateGraphSimulator.merge_review_findings([concurrency_review, security_review])
        self.assertTrue(merged["has_defect"])
        self.assertEqual(merged["next_condition"], "DEFECT_FOUND")
        self.assertEqual(merged["findings"][0]["severity"], "CRITICAL")

        # Back edge triggered deterministically
        sim.transition("TRACER_BULLET", condition=merged["next_condition"])
        self.assertEqual(sim.current_state, "TRACER_BULLET")

    def test_scenario_9_anti_pattern_shared_workspace_mutation_blocked(self):
        """Scenario 9 (Anti-Pattern Rejection): Prevents parallel mutations on shared workspace."""
        sim = StateGraphSimulator(profile="deep_parallel")
        sim.transition("TRACER_BULLET", condition="FACTS_ESTABLISHED")
        sim.transition("TEST_FIRST", condition="CONTRACT_LOCKED")

        # Attempting to fan-out with shared workspace mutation in TEST_FIRST must be blocked
        with self.assertRaises(SharedWorkspaceMutationError):
            sim.dispatch_subagents(["worker_1", "worker_2"], workspace_mode="inherit")


def run_evaluation():
    suite = unittest.TestLoader().loadTestsFromTestCase(EvaluationHarnessScenarios)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    if not result.wasSuccessful():
        sys.exit(1)
    print("\n[SUCCESS] Deterministic Simulation Evaluation (9 Scenarios) completed with 0 violations.")


if __name__ == "__main__":
    run_evaluation()
