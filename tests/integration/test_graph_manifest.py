#!/usr/bin/env python3
"""
Integration tests for Canonical Graph Manifest (graph/canonical_graph.json).

Validates:
1. Schema conformity (schema_version, nodes, edges, conditions).
2. Reachability invariants (from entry node, all active nodes are reachable).
3. Terminal & safety invariants (HUMAN_DECISION halts, no dead ends).
4. Mermaid consistency with .codex/AGENTS.md and .antigravity/GEMINI.md.
"""

import json
import os
import re
import unittest
from collections import deque
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
MANIFEST_PATH = REPO_ROOT / "graph" / "canonical_graph.json"
CODEX_AGENTS_PATH = REPO_ROOT / ".codex" / "AGENTS.md"
GEMINI_PATH = REPO_ROOT / ".antigravity" / "GEMINI.md"

EXPECTED_NODES = {
    "INVESTIGATION",
    "TRACER_BULLET",
    "TEST_FIRST",
    "REVIEW",
    "ARCHITECTURE",
    "DEAD_CODE_CLEANUP",
    "PRE_COMMIT_LEAK_REVIEW",
    "HUMAN_DECISION",
}


class CanonicalGraphManifestTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.assertTrue(cls, MANIFEST_PATH.is_file(), f"Missing {MANIFEST_PATH}")
        with open(MANIFEST_PATH, "r", encoding="utf-8") as fp:
            cls.manifest = json.load(fp)

    def test_schema_structure_and_nodes(self):
        """Verify top-level structure, version, entry node, and node presence."""
        self.assertEqual(self.manifest.get("schema_version"), "2.0.0")
        self.assertEqual(self.manifest.get("graph_id"), "ai_inst_portable_loop")
        self.assertEqual(self.manifest.get("entry_node"), "INVESTIGATION")

        # Execution profiles check
        profiles = self.manifest.get("execution_profiles", {})
        self.assertEqual(set(profiles.keys()), {"economy", "balanced", "deep_parallel"})
        self.assertFalse(profiles["economy"]["allow_subagents"])
        self.assertEqual(profiles["economy"]["max_parallel_workers"], 1)
        self.assertTrue(profiles["balanced"]["allow_subagents"])
        self.assertTrue(profiles["deep_parallel"]["allow_subagents"])

        nodes = self.manifest.get("nodes", {})
        self.assertEqual(set(nodes.keys()), EXPECTED_NODES)

        valid_topologies = {"SINGLE_AGENT", "MULTI_AGENT_FAN_OUT", "HYBRID_COMPETITIVE", "HUMAN_GATE"}
        valid_fan_ins = {"FACT_UNION", "ARBITRATION_BY_CONTRACT", "RISK_LEDGER_MERGE", "NOT_APPLICABLE", "HUMAN_INSPECTION"}

        for node_id, node_data in nodes.items():
            self.assertIn("permission_level", node_data, f"Node {node_id} missing permission_level")
            self.assertIn("human_gate", node_data, f"Node {node_id} missing human_gate")
            self.assertIn(node_data.get("execution_topology"), valid_topologies, f"Node {node_id} invalid topology")
            self.assertIn(node_data.get("fan_in_policy"), valid_fan_ins, f"Node {node_id} invalid fan_in_policy")
            self.assertIsInstance(node_data.get("subagent_roles"), list)

            if node_id == "HUMAN_DECISION":
                self.assertTrue(node_data["human_gate"])
                self.assertEqual(node_data["permission_level"], "TERMINAL_HALT")
                self.assertEqual(node_data["execution_topology"], "HUMAN_GATE")
                self.assertIsNone(node_data["skill"])
            else:
                self.assertFalse(node_data["human_gate"])
                self.assertIsNotNone(node_data["skill"])
                skill_path = REPO_ROOT / ".agent" / node_data["skill"]
                self.assertTrue(
                    skill_path.is_file(),
                    f"Referenced skill file does not exist: {skill_path}",
                )

    def test_edge_definitions_and_conditions(self):
        """Verify edge schema, valid node endpoints, and recognized types."""
        edges = self.manifest.get("edges", [])
        self.assertGreaterEqual(len(edges), 14, "Expected at least 14 transitions in canonical graph")

        valid_types = {"FORWARD", "SHORTCUT", "BACK_EDGE", "HALT"}
        for edge in edges:
            u, v = edge.get("from"), edge.get("to")
            self.assertIn(u, EXPECTED_NODES, f"Invalid source node: {u}")
            self.assertIn(v, EXPECTED_NODES, f"Invalid destination node: {v}")
            self.assertIn(edge.get("type"), valid_types, f"Invalid edge type in {edge}")
            self.assertTrue(edge.get("condition"), f"Missing condition in {edge}")

        # Check halt edge
        halt_edges = [e for e in edges if e["type"] == "HALT"]
        self.assertEqual(len(halt_edges), 1)
        self.assertEqual(halt_edges[0]["from"], "ARCHITECTURE")
        self.assertEqual(halt_edges[0]["to"], "HUMAN_DECISION")
        self.assertEqual(halt_edges[0]["condition"], "STRUCTURAL_ADJUST")

    def test_graph_reachability_and_safety_invariants(self):
        """Verify reachability from entry node and path to exits."""
        nodes = self.manifest["nodes"]
        edges = self.manifest["edges"]

        adj = {n: [] for n in nodes}
        rev_adj = {n: [] for n in nodes}
        for edge in edges:
            adj[edge["from"]].append(edge["to"])
            rev_adj[edge["to"]].append(edge["from"])

        # 1. Reachability from entry node (INVESTIGATION)
        visited = set()
        queue = deque(["INVESTIGATION"])
        while queue:
            curr = queue.popleft()
            if curr not in visited:
                visited.add(curr)
                for neighbor in adj[curr]:
                    if neighbor not in visited:
                        queue.append(neighbor)

        self.assertEqual(
            visited,
            EXPECTED_NODES,
            f"Unreachable nodes from INVESTIGATION: {EXPECTED_NODES - visited}",
        )

        # 2. Safety: Every non-terminal node must have an outgoing path to HUMAN_DECISION or PRE_COMMIT_LEAK_REVIEW
        exit_nodes = {"HUMAN_DECISION", "PRE_COMMIT_LEAK_REVIEW"}
        can_reach_exit = set(exit_nodes)
        queue = deque(exit_nodes)
        while queue:
            curr = queue.popleft()
            for pred in rev_adj[curr]:
                if pred not in can_reach_exit:
                    can_reach_exit.add(pred)
                    queue.append(pred)

        self.assertEqual(
            can_reach_exit,
            EXPECTED_NODES,
            f"Nodes unable to reach any exit gate: {EXPECTED_NODES - can_reach_exit}",
        )

    def _extract_mermaid_edges(self, markdown_path: Path):
        """Helper to extract (source, dest) transitions from Mermaid blocks in markdown."""
        with open(markdown_path, "r", encoding="utf-8") as fp:
            content = fp.read()

        mermaid_match = re.search(r"```mermaid\s*\nstateDiagram-v2\n(.*?)\n```", content, re.DOTALL)
        self.assertIsNotNone(mermaid_match, f"Could not find Mermaid state diagram in {markdown_path}")
        diagram_text = mermaid_match.group(1)

        extracted_edges = set()
        # Matches lines like: SOURCE --> DEST: optional comment
        edge_pattern = re.compile(r"^\s*([A-Za-z0-9_]+)\s*-->\s*([A-Za-z0-9_]+)", re.MULTILINE)
        for src, dst in edge_pattern.findall(diagram_text):
            if src not in ("[*]", "Drift判定") and dst not in ("[*]", "Drift判定"):
                extracted_edges.add((src.upper(), dst.upper()))

        return extracted_edges

    def test_mermaid_consistency_with_documentation(self):
        """Verify AGENTS.md and GEMINI.md state diagrams reflect manifest transitions."""
        manifest_edges = {(e["from"], e["to"]) for e in self.manifest["edges"]}

        for doc_path in (CODEX_AGENTS_PATH, GEMINI_PATH):
            mermaid_edges = self._extract_mermaid_edges(doc_path)
            # Ensure all Mermaid edges correspond to valid manifest transitions
            for src, dst in mermaid_edges:
                self.assertIn(
                    (src, dst),
                    manifest_edges,
                    f"{doc_path.name} has transition {src} --> {dst} not in canonical_graph.json",
                )
            # Ensure Core 7 forward chain is fully covered in Mermaid
            core_chain = [
                ("INVESTIGATION", "TRACER_BULLET"),
                ("TRACER_BULLET", "TEST_FIRST"),
                ("TEST_FIRST", "REVIEW"),
                ("REVIEW", "ARCHITECTURE"),
                ("ARCHITECTURE", "HUMAN_DECISION"),
                ("ARCHITECTURE", "DEAD_CODE_CLEANUP"),
                ("DEAD_CODE_CLEANUP", "PRE_COMMIT_LEAK_REVIEW"),
            ]
            for src, dst in core_chain:
                self.assertIn(
                    (src, dst),
                    mermaid_edges,
                    f"{doc_path.name} missing essential Core transition {src} --> {dst}",
                )


if __name__ == "__main__":
    unittest.main()
