#!/usr/bin/env python3
"""CLI Contract Linter & Drift Detector.

Verifies CLI interface definitions (flags, subcommands, exit codes, output schema)
against a locked baseline contract to detect breaking changes (CLI Drift).
Zero external dependencies (uses standard library only).
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple


def compare_specs(
    baseline: Dict[str, Any], current: Dict[str, Any]
) -> Tuple[List[str], List[str]]:
    """Compares baseline and current CLI specifications.

    Returns:
        (breaking_errors, non_breaking_warnings)
    """
    errors: List[str] = []
    warnings: List[str] = []

    # Check top-level command name
    base_name = baseline.get("name", "")
    curr_name = current.get("name", "")
    if base_name and curr_name and base_name != curr_name:
        errors.append(f"Root command renamed from '{base_name}' to '{curr_name}'")

    # Check subcommands
    base_subs = baseline.get("subcommands", {})
    curr_subs = current.get("subcommands", {})

    for sub_name, base_sub in base_subs.items():
        if sub_name not in curr_subs:
            errors.append(f"Subcommand removed: '{sub_name}'")
        else:
            curr_sub = curr_subs[sub_name]
            sub_errs, sub_warns = compare_command_spec(
                f"{sub_name}", base_sub, curr_sub
            )
            errors.extend(sub_errs)
            warnings.extend(sub_warns)

    for sub_name in curr_subs:
        if sub_name not in base_subs:
            warnings.append(f"New subcommand added: '{sub_name}' (Non-breaking)")

    # Check root flags/options
    root_errs, root_warns = compare_flags(
        "root", baseline.get("flags", {}), current.get("flags", {})
    )
    errors.extend(root_errs)
    warnings.extend(root_warns)

    # Check root output_schema
    base_schema = baseline.get("output_schema")
    curr_schema = current.get("output_schema")
    if base_schema is not None:
        if curr_schema is None:
            errors.append("[root] output_schema removed")
        else:
            s_errs, s_warns = compare_output_schema("root", base_schema, curr_schema)
            errors.extend(s_errs)
            warnings.extend(s_warns)
    elif curr_schema is not None:
        warnings.append("[root] New output_schema defined (Non-breaking)")

    return errors, warnings


def compare_command_spec(
    prefix: str, base: Dict[str, Any], curr: Dict[str, Any]
) -> Tuple[List[str], List[str]]:
    errors: List[str] = []
    warnings: List[str] = []

    # Compare exit codes
    base_codes = set(base.get("exit_codes", []))
    curr_codes = set(curr.get("exit_codes", []))
    missing_codes = base_codes - curr_codes
    if missing_codes:
        errors.append(
            f"[{prefix}] Missing documented exit codes: {sorted(list(missing_codes))}"
        )

    # Compare flags
    flag_errs, flag_warns = compare_flags(
        prefix, base.get("flags", {}), curr.get("flags", {})
    )
    errors.extend(flag_errs)
    warnings.extend(flag_warns)

    # Recursively compare nested subcommands
    base_subs = base.get("subcommands", {})
    curr_subs = curr.get("subcommands", {})
    for sub_name, base_sub in base_subs.items():
        if sub_name not in curr_subs:
            errors.append(f"[{prefix}] Subcommand removed: '{sub_name}'")
        else:
            curr_sub = curr_subs[sub_name]
            sub_errs, sub_warns = compare_command_spec(
                f"{prefix} {sub_name}", base_sub, curr_sub
            )
            errors.extend(sub_errs)
            warnings.extend(sub_warns)

    for sub_name in curr_subs:
        if sub_name not in base_subs:
            warnings.append(f"[{prefix}] New subcommand added: '{sub_name}' (Non-breaking)")

    # Compare output schema
    base_schema = base.get("output_schema")
    curr_schema = curr.get("output_schema")
    if base_schema is not None:
        if curr_schema is None:
            errors.append(f"[{prefix}] output_schema removed")
        else:
            s_errs, s_warns = compare_output_schema(prefix, base_schema, curr_schema)
            errors.extend(s_errs)
            warnings.extend(s_warns)
    elif curr_schema is not None:
        warnings.append(f"[{prefix}] New output_schema defined (Non-breaking)")

    return errors, warnings


def compare_output_schema(
    prefix: str, base_schema: Dict[str, Any], curr_schema: Dict[str, Any]
) -> Tuple[List[str], List[str]]:
    """Compares JSON schemas to detect breaking changes (field removals, type changes)."""
    errors: List[str] = []
    warnings: List[str] = []

    # Check type
    base_type = base_schema.get("type")
    curr_type = curr_schema.get("type")
    if base_type and curr_type and base_type != curr_type:
        errors.append(
            f"[{prefix}] output_schema type changed from '{base_type}' to '{curr_type}'"
        )
        return errors, warnings

    base_props = base_schema.get("properties", {})
    curr_props = curr_schema.get("properties", {})

    for prop_name, base_prop in base_props.items():
        if prop_name not in curr_props:
            errors.append(f"[{prefix}] output_schema property removed: '{prop_name}'")
        else:
            curr_prop = curr_props[prop_name]
            # Check property type
            bp_type = base_prop.get("type")
            cp_type = curr_prop.get("type")
            if bp_type and cp_type and bp_type != cp_type:
                errors.append(
                    f"[{prefix}] output_schema property '{prop_name}' type changed from '{bp_type}' to '{cp_type}'"
                )
            # Recursive check if nested object
            if bp_type == "object" and cp_type == "object":
                nested_errs, nested_warns = compare_output_schema(
                    f"{prefix}.{prop_name}", base_prop, curr_prop
                )
                errors.extend(nested_errs)
                warnings.extend(nested_warns)

    for prop_name in curr_props:
        if prop_name not in base_props:
            warnings.append(
                f"[{prefix}] output_schema new property added: '{prop_name}' (Compatible)"
            )

    return errors, warnings


def compare_flags(
    prefix: str, base_flags: Dict[str, Any], curr_flags: Dict[str, Any]
) -> Tuple[List[str], List[str]]:
    errors: List[str] = []
    warnings: List[str] = []

    for flag_name, base_flag in base_flags.items():
        if flag_name not in curr_flags:
            errors.append(f"[{prefix}] Flag removed: '{flag_name}'")
        else:
            curr_flag = curr_flags[flag_name]
            # Check if an optional flag became required
            if not base_flag.get("required", False) and curr_flag.get(
                "required", False
            ):
                errors.append(
                    f"[{prefix}] Optional flag '{flag_name}' became required"
                )
            # Check default value change
            if base_flag.get("default") != curr_flag.get("default"):
                warnings.append(
                    f"[{prefix}] Flag '{flag_name}' default changed: "
                    f"'{base_flag.get('default')}' -> '{curr_flag.get('default')}'"
                )

    for flag_name in curr_flags:
        if flag_name not in base_flags:
            if curr_flags[flag_name].get("required", False):
                errors.append(
                    f"[{prefix}] New required flag added without default: '{flag_name}'"
                )
            else:
                warnings.append(
                    f"[{prefix}] New optional flag added: '{flag_name}' (Compatible)"
                )

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(
        description="CLI Contract Linter & Drift Detector"
    )
    parser.add_argument(
        "--baseline",
        required=True,
        help="Path to locked CLI contract specification JSON",
    )
    parser.add_argument(
        "--current",
        required=True,
        help="Path to current/candidate CLI specification JSON",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat warnings as errors (fail on any drift)",
    )

    args = parser.parse_args()

    baseline_path = Path(args.baseline)
    current_path = Path(args.current)

    if not baseline_path.exists():
        print(f"[Error]: Baseline contract file not found: {baseline_path}", file=sys.stderr)
        return 2

    if not current_path.exists():
        print(f"[Error]: Current specification file not found: {current_path}", file=sys.stderr)
        return 2

    try:
        baseline_spec = json.loads(baseline_path.read_text())
        current_spec = json.loads(current_path.read_text())
    except Exception as e:
        print(f"[Error]: Failed to parse JSON specification: {e}", file=sys.stderr)
        return 2

    errors, warnings = compare_specs(baseline_spec, current_spec)

    print("=== CLI Contract Drift Analysis ===")
    if not errors and not warnings:
        print("[Status]: Clean - No CLI drift detected.")
        return 0

    if warnings:
        print(f"\n[Warnings / Compatible Extensions ({len(warnings)})]:")
        for w in warnings:
            print(f"  - {w}")

    if errors:
        print(f"\n[Errors / Breaking Changes ({len(errors)})]:")
        for err in errors:
            print(f"  - [BREAKING]: {err}")
        print("\nResult: CLI Contract Broken! Halt and propose an ADR (STRUCTURAL_ADJUST).")
        return 1

    if args.strict and warnings:
        print("\nResult: Strict mode enabled, failing on warnings.")
        return 1

    print("\nResult: Non-breaking changes detected (MINOR_UPDATE).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
