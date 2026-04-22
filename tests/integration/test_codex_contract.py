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
        self.assertIn("make install-home-codex", proc.stdout)
        self.assertIn("make install-home-codex-minimal", proc.stdout)

    def test_install_codex_copies_required_contract_files(self) -> None:
        print("=== CLI Contract Encompassed Packages ===")
        print(".codex/AGENTS.md")
        print(".codex/skills/cli-contract/SKILL.md")
        print(".codex/skills/planner/SKILL.md")
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
                codex_root / "skills" / "planner" / "SKILL.md",
                "1. （推奨）: [WORKFLOW_STATE] [short action]",
            )

    def test_install_home_codex_variants_copy_expected_files(self) -> None:
        print("=== CLI Contract Encompassed Packages ===")
        print(".codex/prompts")
        print(".codex/skills")
        print(".codex/agents")
        with tempfile.TemporaryDirectory() as tmp_home:
            env = os.environ.copy()
            env["HOME"] = tmp_home

            proc = self.run_cmd("make", "install-home-codex", env=env)
            self.assertIn("Home installation complete. Codex is now globally configured", proc.stdout)

            home_codex = Path(tmp_home) / ".codex"
            self.assertTrue((home_codex / "AGENTS.md").exists())
            self.assertTrue((home_codex / "prompts" / "mission.md").exists())
            self.assertTrue((home_codex / "skills" / "cli-contract" / "SKILL.md").exists())
            self.assertTrue((home_codex / "agents" / "tester.toml").exists())

        with tempfile.TemporaryDirectory() as tmp_home:
            env = os.environ.copy()
            env["HOME"] = tmp_home

            proc = self.run_cmd("make", "install-home-codex-minimal", env=env)
            self.assertIn("Minimal home installation complete. Codex is now globally configured", proc.stdout)

            home_codex = Path(tmp_home) / ".codex"
            self.assertTrue((home_codex / "AGENTS.md").exists())
            self.assertFalse((home_codex / "prompts").exists())
            self.assertTrue((home_codex / "skills" / "planner" / "SKILL.md").exists())
            self.assertTrue((home_codex / "agents" / "tracer.toml").exists())


if __name__ == "__main__":
    unittest.main()
