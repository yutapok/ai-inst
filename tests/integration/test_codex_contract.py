import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from typing import Dict, Optional


REPO_ROOT = Path(__file__).resolve().parents[2]


class CodexContractIntegrationTests(unittest.TestCase):
    maxDiff = None

    def run_cmd(self, *args: str, env: Optional[Dict[str, str]] = None):
        proc = subprocess.run(
            args,
            cwd=REPO_ROOT,
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )
        if proc.returncode != 0:
            self.fail(
                f"command failed: {' '.join(args)}\n"
                f"exit={proc.returncode}\nstdout:\n{proc.stdout}\nstderr:\n{proc.stderr}"
            )
        return proc

    def assert_contains(self, path: Path, expected: str) -> None:
        content = path.read_text()
        self.assertIn(expected, content, f"{path} did not contain expected text: {expected}")

    def test_make_help_advertises_codex_targets(self) -> None:
        print("=== CLI Contract Encompassed Packages ===")
        print("Makefile")
        proc = self.run_cmd("make", "help")
        self.assertIn("make install-codex", proc.stdout)
        self.assertIn("make install-home-codex-core", proc.stdout)
        self.assertIn("make install-home-codex", proc.stdout)
        self.assertIn("make install-home-codex-minimal", proc.stdout)
        self.assertIn("make install-antigravity", proc.stdout)
        self.assertIn("make install-home-antigravity", proc.stdout)

    def test_install_claude_copies_btw_async_and_planner_skill(self) -> None:
        print("=== CLI Contract Encompassed Packages ===")
        print(".claude/CLAUDE.md")
        print(".claude/commands/btw-async.md")
        print(".claude/commands/ql-review.md")
        print(".claude/commands/drift-check.md")
        print(".claude/skills/planner/SKILL.md")
        print(".claude/skills/dead-code-cleanup/SKILL.md")
        print(".claude/agents/*.md")
        with tempfile.TemporaryDirectory() as tmpdir:
            dest = Path(tmpdir) / "dest"
            dest.mkdir()
            proc = self.run_cmd("make", "install-claude", f"DEST={dest}")
            self.assertIn("Installation complete. Target project is now ready for Claude Code.", proc.stdout)

            claude_root = dest / ".claude"
            self.assertTrue((claude_root / "CLAUDE.md").exists())
            self.assertTrue((claude_root / "commands" / "btw-async.md").exists())
            self.assertTrue((claude_root / "skills" / "planner" / "SKILL.md").exists())
            self.assertTrue((claude_root / "skills" / "dead-code-cleanup" / "SKILL.md").exists())
            self.assertTrue((claude_root / "agents" / "tracer.md").exists())

            self.assert_contains(claude_root / "CLAUDE.md", "次のステップ:")
            self.assert_contains(claude_root / "CLAUDE.md", "DRIFT_CHECK")
            self.assert_contains(
                claude_root / "commands" / "btw-async.md",
                "/ql-review",
            )
            self.assert_contains(
                claude_root / "commands" / "btw-async.md",
                "/drift-check",
            )
            self.assert_contains(
                claude_root / "skills" / "planner" / "SKILL.md",
                "1. （推奨）[WORKFLOW_STATE]: [short action]",
            )
            self.assert_contains(
                claude_root / "skills" / "planner" / "SKILL.md",
                "Verify: [one command + one observation point]",
            )
            self.assert_contains(
                claude_root / "skills" / "planner" / "SKILL.md",
                "2. [WORKFLOW_STATE]: （Async）[short action]",
            )
            self.assert_contains(
                claude_root / "skills" / "planner" / "SKILL.md",
                "Goal: [short goal]",
            )
            self.assert_contains(
                claude_root / "skills" / "planner" / "SKILL.md",
                "Non-goals: [short exclusions]",
            )

    def test_install_codex_copies_required_contract_files(self) -> None:
        print("=== CLI Contract Encompassed Packages ===")
        print(".codex/AGENTS.md")
        print(".codex/skills/cli-contract/SKILL.md")
        print(".codex/skills/planner/SKILL.md")
        print(".codex/skills/dead-code-cleanup/SKILL.md")
        print(".codex/report-contract/README.md")
        print(".codex/prompts/mission.md")
        print(".codex/prompts/expand.md")
        print(".codex/agents/*.toml")
        with tempfile.TemporaryDirectory() as tmpdir:
            dest = Path(tmpdir) / "dest"
            dest.mkdir()
            proc = self.run_cmd("make", "install-codex", f"DEST={dest}")
            self.assertIn("Installation complete. Target project is now ready for Codex.", proc.stdout)

            codex_root = dest / ".codex"
            self.assertTrue((codex_root / "AGENTS.md").exists())
            self.assertTrue((codex_root / "skills" / "cli-contract" / "SKILL.md").exists())
            self.assertTrue((codex_root / "skills" / "test-first" / "SKILL.md").exists())
            self.assertTrue((codex_root / "skills" / "planner" / "SKILL.md").exists())
            self.assertTrue((codex_root / "skills" / "dead-code-cleanup" / "SKILL.md").exists())
            self.assertTrue((codex_root / "skills" / "report-observability" / "SKILL.md").exists())
            self.assertTrue((codex_root / "config.toml").exists())
            self.assertTrue((codex_root / "report-contract" / "README.md").exists())
            self.assertTrue((codex_root / "reports").exists())
            self.assertTrue((codex_root / "agents" / "architect.toml").exists())
            self.assertTrue((codex_root / "agents" / "planner.toml").exists())

            self.assert_contains(codex_root / "AGENTS.md", "次のステップ:")
            self.assert_contains(codex_root / "AGENTS.md", "CONTRACT_LOCK")
            self.assert_contains(
                codex_root / "skills" / "cli-contract" / "SKILL.md",
                "implement it as an automated integration test",
            )
            self.assert_contains(
                codex_root / "skills" / "cli-contract" / "SKILL.md",
                "The exact `stdout` format for a successful execution",
            )
            self.assert_contains(
                codex_root / "skills" / "cli-contract" / "SKILL.md",
                "`stderr` format representing the expected errors",
            )
            self.assert_contains(
                codex_root / "skills" / "cli-contract" / "SKILL.md",
                "help the user validate and understand AI-generated code",
            )
            self.assert_contains(
                codex_root / "skills" / "dead-code-cleanup" / "SKILL.md",
                "`DELETE`, `MERGE`, `INLINE`, `SIMPLIFY`, or `KEEP`",
            )
            self.assert_contains(
                codex_root / "skills" / "dead-code-cleanup" / "SKILL.md",
                "`Safe`, `Needs Verification`, or `Needs Human Decision`",
            )
            self.assert_contains(
                codex_root / "skills" / "planner" / "SKILL.md",
                "1. （推奨）[WORKFLOW_STATE]: [short action]",
            )
            self.assert_contains(
                codex_root / "skills" / "planner" / "SKILL.md",
                "Verify: [one command + one observation point]",
            )
            self.assert_contains(
                codex_root / "skills" / "planner" / "SKILL.md",
                "2. [WORKFLOW_STATE]: （Async）[short action]",
            )
            self.assert_contains(
                codex_root / "skills" / "planner" / "SKILL.md",
                "Goal: [short goal]",
            )
            self.assert_contains(
                codex_root / "skills" / "planner" / "SKILL.md",
                "Non-goals: [short exclusions]",
            )
            self.assert_contains(
                codex_root / "report-contract" / "README.md",
                "Do not commit real runtime logs",
            )
            self.assert_contains(
                codex_root / "report-contract" / "verification-ledger.sample.jsonl",
                "\"facts\"",
            )

    def test_install_home_codex_variants_copy_expected_files(self) -> None:
        print("=== CLI Contract Encompassed Packages ===")
        print(".codex/prompts")
        print(".codex/skills")
        print(".codex/agents")
        print(".codex/report-contract")
        with tempfile.TemporaryDirectory() as tmp_home:
            env = os.environ.copy()
            env["HOME"] = tmp_home

            proc = self.run_cmd("make", "install-home-codex-core", env=env)
            self.assertIn("Core home installation complete. Codex is now globally configured", proc.stdout)

            home_codex = Path(tmp_home) / ".codex"
            self.assertTrue((home_codex / "AGENTS.md").exists())
            self.assertTrue((home_codex / "skills" / "planner" / "SKILL.md").exists())
            self.assertTrue((home_codex / "skills" / "dead-code-cleanup" / "SKILL.md").exists())
            self.assertTrue((home_codex / "skills" / "report-observability" / "SKILL.md").exists())
            self.assertTrue((home_codex / "report-contract" / "README.md").exists())
            self.assertTrue((home_codex / "reports").exists())
            self.assertFalse((home_codex / "config.toml").exists())
            self.assertFalse((home_codex / "agents").exists())
            self.assertFalse((home_codex / "prompts").exists())

        with tempfile.TemporaryDirectory() as tmp_home:
            env = os.environ.copy()
            env["HOME"] = tmp_home

            stale = Path(tmp_home) / ".codex"
            (stale / "agents").mkdir(parents=True)
            (stale / "prompts").mkdir(parents=True)
            (stale / "agents" / "obsolete.txt").write_text("old")
            (stale / "prompts" / "obsolete.txt").write_text("old")
            proc = self.run_cmd("make", "install-home-codex", env=env)
            self.assertIn("Home installation complete. Codex is now globally configured", proc.stdout)

            home_codex = Path(tmp_home) / ".codex"
            self.assertTrue((home_codex / "AGENTS.md").exists())
            self.assertTrue((home_codex / "config.toml").exists())
            self.assertTrue((home_codex / "prompts" / "mission.md").exists())
            self.assertTrue((home_codex / "skills" / "cli-contract" / "SKILL.md").exists())
            self.assertTrue((home_codex / "skills" / "dead-code-cleanup" / "SKILL.md").exists())
            self.assertTrue((home_codex / "report-contract" / "run-log.sample.jsonl").exists())
            self.assertTrue((home_codex / "reports").exists())
            self.assertTrue((home_codex / "agents" / "tester.toml").exists())
            self.assertFalse((home_codex / "agents" / "obsolete.txt").exists())
            self.assertFalse((home_codex / "prompts" / "obsolete.txt").exists())

        with tempfile.TemporaryDirectory() as tmp_home:
            env = os.environ.copy()
            env["HOME"] = tmp_home

            stale = Path(tmp_home) / ".codex"
            (stale / "agents").mkdir(parents=True)
            (stale / "prompts").mkdir(parents=True)
            (stale / "agents" / "obsolete.txt").write_text("old")
            (stale / "prompts" / "obsolete.txt").write_text("old")
            proc = self.run_cmd("make", "install-home-codex-minimal", env=env)
            self.assertIn("Minimal home installation complete. Codex is now globally configured", proc.stdout)

            home_codex = Path(tmp_home) / ".codex"
            self.assertTrue((home_codex / "AGENTS.md").exists())
            self.assertTrue((home_codex / "config.toml").exists())
            self.assertFalse((home_codex / "prompts").exists())
            self.assertTrue((home_codex / "skills" / "planner" / "SKILL.md").exists())
            self.assertTrue((home_codex / "skills" / "dead-code-cleanup" / "SKILL.md").exists())
            self.assertTrue((home_codex / "report-contract" / "human-decisions.sample.jsonl").exists())
            self.assertTrue((home_codex / "reports").exists())
            self.assertTrue((home_codex / "agents" / "tracer.toml").exists())
            self.assertFalse((home_codex / "agents" / "obsolete.txt").exists())
            self.assertFalse((home_codex / "prompts").exists())

    def test_install_home_claude_copies_btw_async_and_planner_skill(self) -> None:
        print("=== CLI Contract Encompassed Packages ===")
        print(".claude/commands")
        print(".claude/skills")
        with tempfile.TemporaryDirectory() as tmp_home:
            env = os.environ.copy()
            env["HOME"] = tmp_home

            stale = Path(tmp_home) / ".claude"
            (stale / "commands").mkdir(parents=True)
            (stale / "skills").mkdir(parents=True)
            (stale / "agents").mkdir(parents=True)
            (stale / "commands" / "obsolete.txt").write_text("old")
            (stale / "skills" / "obsolete.txt").write_text("old")
            (stale / "agents" / "obsolete.txt").write_text("old")
            proc = self.run_cmd("make", "install-home-claude", env=env)
            self.assertIn("Home installation complete. Claude Code is now globally configured", proc.stdout)
            home_claude = Path(tmp_home) / ".claude"
            self.assertTrue((home_claude / "CLAUDE.md").exists())
            self.assertTrue((home_claude / "commands" / "btw-async.md").exists())
            self.assertTrue((home_claude / "skills" / "planner" / "SKILL.md").exists())
            self.assertTrue((home_claude / "skills" / "dead-code-cleanup" / "SKILL.md").exists())
            self.assertTrue((home_claude / "agents" / "tracer.md").exists())
            self.assertFalse((home_claude / "commands" / "obsolete.txt").exists())
            self.assertFalse((home_claude / "skills" / "obsolete.txt").exists())
            self.assertFalse((home_claude / "agents" / "obsolete.txt").exists())

    def test_install_antigravity_copies_rules_workflows_and_skills(self) -> None:
        print("=== CLI Contract Encompassed Packages ===")
        print(".antigravity/ANTIGRAVITY.md")
        print(".antigravity/workflows/*.md")
        print(".antigravity/skills/*/SKILL.md")
        with tempfile.TemporaryDirectory() as tmpdir:
            dest = Path(tmpdir) / "dest"
            dest.mkdir()
            proc = self.run_cmd("make", "install-antigravity", f"DEST={dest}")
            self.assertIn("Installation complete. Target project is now ready for Antigravity.", proc.stdout)

            antigravity_root = dest / ".antigravity"
            self.assertTrue((antigravity_root / "ANTIGRAVITY.md").exists())
            self.assertTrue((antigravity_root / "workflows" / "mission.md").exists())
            self.assertTrue((antigravity_root / "skills" / "planner" / "SKILL.md").exists())
            self.assertTrue((antigravity_root / "skills" / "dead-code-cleanup" / "SKILL.md").exists())

            self.assert_contains(antigravity_root / "ANTIGRAVITY.md", "Portable Development Loop for Antigravity")
            self.assert_contains(
                antigravity_root / "workflows" / "mission.md",
                "*(Required skill: `.antigravity/skills/investigation/SKILL.md`)*",
            )
            self.assert_contains(
                antigravity_root / "skills" / "planner" / "SKILL.md",
                "Workflow Planner",
            )

    def test_install_home_antigravity_copies_global_skills(self) -> None:
        print("=== CLI Contract Encompassed Packages ===")
        print(".antigravity/skills")
        with tempfile.TemporaryDirectory() as tmp_home:
            env = os.environ.copy()
            env["HOME"] = tmp_home

            proc = self.run_cmd("make", "install-home-antigravity", env=env)
            self.assertIn("Home installation complete. Antigravity is now globally configured with skills.", proc.stdout)

            home_gemini_config = Path(tmp_home) / ".gemini" / "config" / "skills"
            self.assertTrue((home_gemini_config / "planner" / "SKILL.md").exists())
            self.assertTrue((home_gemini_config / "dead-code-cleanup" / "SKILL.md").exists())

            home_gemini_cli = Path(tmp_home) / ".gemini" / "antigravity-cli" / "skills"
            self.assertTrue((home_gemini_cli / "planner" / "SKILL.md").exists())
            self.assertTrue((home_gemini_cli / "dead-code-cleanup" / "SKILL.md").exists())


if __name__ == "__main__":
    unittest.main()
