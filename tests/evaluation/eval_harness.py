#!/usr/bin/env python3
"""
Deterministic Evaluation Harness for Agentic Architecture State Transitions.

Simulates and verifies 4 key representative scenarios:
1. Scenario 1 (Happy Path): Complete canonical forward traversal protecting contracts and invariants.
2. Scenario 2 (Back Edge): Review defect injection correctly routes back to TRACER_BULLET.
3. Scenario 3 (Drift Halt): Structural adjustment immediately halts at HUMAN_DECISION gate.
4. Scenario 4 (Illegal Transition): Prohibited shortcuts/jumps are rejected with TransitionRejectedError.
"""

import json
import sys
import unittest
from pathlib import Path
from typing import List, Optional

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
MANIFEST_PATH = REPO_ROOT / "graph" / "canonical_graph.json"


class TransitionRejectedError(Exception):
    """Raised when an illegal state transition is attempted."""
    pass


class TerminalHaltReached(Exception):
    """Raised when a terminal gate (e.g., HUMAN_DECISION) is reached and automated transitions are blocked."""
    pass


class StateGraphSimulator:
    """Deterministic state machine simulator for ai-inst workflow graph."""

    def __init__(self, manifest_path: Path = MANIFEST_PATH):
        if not manifest_path.is_file():
            raise FileNotFoundError(f"Manifest not found: {manifest_path}")
        with open(manifest_path, "r", encoding="utf-8") as fp:
            self.manifest = json.load(fp)

        self.nodes = self.manifest.get("nodes", {})
        self.edges = self.manifest.get("edges", [])
        self.current_state = self.manifest.get("entry_node", "INVESTIGATION")
        self.history: List[str] = [self.current_state]
        self.is_halted: bool = False

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


class EvaluationHarnessScenarios(unittest.TestCase):
    """Evaluation scenarios verifying state machine invariants."""

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

        expected_history = [
            "INVESTIGATION",
            "TRACER_BULLET",
            "TEST_FIRST",
            "REVIEW",
            "ARCHITECTURE",
            "DEAD_CODE_CLEANUP",
            "PRE_COMMIT_LEAK_REVIEW",
        ]
        self.assertEqual(sim.history, expected_history)
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

        expected_history = [
            "INVESTIGATION",
            "TRACER_BULLET",
            "TEST_FIRST",
            "REVIEW",
            "TRACER_BULLET",
            "TEST_FIRST",
            "REVIEW",
            "ARCHITECTURE",
            "DEAD_CODE_CLEANUP",
            "PRE_COMMIT_LEAK_REVIEW",
        ]
        self.assertEqual(sim.history, expected_history)
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

        # Move to TRACER_BULLET
        sim.transition("TRACER_BULLET", condition="FACTS_ESTABLISHED")

        # Cannot skip from TRACER_BULLET directly to ARCHITECTURE or COMMIT
        with self.assertRaises(TransitionRejectedError):
            sim.transition("ARCHITECTURE")
        with self.assertRaises(TransitionRejectedError):
            sim.transition("PRE_COMMIT_LEAK_REVIEW")

        # Invalid condition string must also be rejected
        with self.assertRaises(TransitionRejectedError):
            sim.transition("TEST_FIRST", condition="UNREGISTERED_CONDITION")


def run_evaluation():
    suite = unittest.TestLoader().loadTestsFromTestCase(EvaluationHarnessScenarios)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    if not result.wasSuccessful():
        sys.exit(1)
    print("\n[SUCCESS] Deterministic Simulation Evaluation completed with 0 violations.")


if __name__ == "__main__":
    run_evaluation()
