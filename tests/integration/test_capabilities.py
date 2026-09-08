#!/usr/bin/env python3
"""
Integration tests for Capability Tiers (capabilities/tiers.json).

Validates:
1. Tier definitions (routine, standard, frontier).
2. Fallback degradation chain (frontier -> standard -> routine).
3. Complete coverage of nodes from graph/canonical_graph.json.
4. Absence of vendor-specific model strings (vendor-neutral tier contract).
"""

import json
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
TIERS_PATH = REPO_ROOT / "capabilities" / "tiers.json"
GRAPH_PATH = REPO_ROOT / "graph" / "canonical_graph.json"

EXPECTED_TIERS = {"routine", "standard", "frontier"}


class CapabilityTiersTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.assertTrue(cls, TIERS_PATH.is_file(), f"Missing {TIERS_PATH}")
        with open(TIERS_PATH, "r", encoding="utf-8") as fp:
            cls.data = json.load(fp)

        with open(GRAPH_PATH, "r", encoding="utf-8") as fp:
            cls.graph = json.load(fp)

    def test_tier_definitions(self):
        """Verify presence of 3 standard tiers and schema version."""
        self.assertEqual(self.data.get("schema_version"), "1.0.0")
        tiers = self.data.get("tiers", {})
        self.assertEqual(set(tiers.keys()), EXPECTED_TIERS)

        for tier_name, tier_info in tiers.items():
            self.assertIn("level", tier_info)
            self.assertIn("description", tier_info)
            self.assertIn("target_tasks", tier_info)
            self.assertIn("model_traits", tier_info)

    def test_fallback_degradation_chain(self):
        """Verify safe fallback degradation policy."""
        tiers = self.data.get("tiers", {})

        # Frontier must degrade to standard
        frontier = tiers["frontier"]
        self.assertEqual(frontier.get("fallback_tier"), "standard")
        degradation = frontier.get("degradation_policy", {})
        self.assertEqual(degradation.get("target"), "standard")
        self.assertEqual(degradation.get("strategy"), "PROMPT_DEEPENING")

        # Standard falls back to routine
        standard = tiers["standard"]
        self.assertEqual(standard.get("fallback_tier"), "routine")

        # Routine has no lower tier
        routine = tiers["routine"]
        self.assertIsNone(routine.get("fallback_tier"))

    def test_node_coverage(self):
        """Verify that every node in canonical graph has a mapped capability tier."""
        graph_nodes = set(self.graph.get("nodes", {}).keys())
        mapping = self.data.get("node_tier_mapping", {})

        self.assertEqual(
            set(mapping.keys()),
            graph_nodes,
            f"Node tier mapping does not match canonical graph nodes: {set(mapping.keys()) ^ graph_nodes}",
        )

        for node_name, tier in mapping.items():
            if node_name == "HUMAN_DECISION":
                self.assertIsNone(tier)
            else:
                self.assertIn(tier, EXPECTED_TIERS, f"Node {node_name} mapped to unknown tier: {tier}")

    def test_vendor_neutrality(self):
        """Ensure no vendor-specific model strings leak into tiers.json."""
        raw_text = json.dumps(self.data).lower()
        forbidden_substrings = ["gpt-", "claude-", "gemini-", "openai", "anthropic", "deepseek"]
        for forbidden in forbidden_substrings:
            self.assertNotIn(
                forbidden,
                raw_text,
                f"Tiers definition should remain vendor-neutral, found '{forbidden}'",
            )


if __name__ == "__main__":
    unittest.main()
