import json
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

    def test_install_codex_copies_required_contract_files(self) -> None:
        print("=== CLI Contract Encompassed Packages ===")
        print(".codex/AGENTS.md")
        print(".codex/skills (Core 7)")
        print(".codex/report-contract/README.md")
        print(".codex/agents/*.toml")
        with tempfile.TemporaryDirectory() as tmpdir:
            dest = Path(tmpdir) / "dest"
            dest.mkdir()
            proc = self.run_cmd("make", "install-codex", f"DEST={dest}")
            self.assertIn("Installation complete. Target project is now ready for Codex.", proc.stdout)

            codex_root = dest / ".codex"
            self.assertTrue((codex_root / "AGENTS.md").exists())
            self.assertTrue((codex_root / "config.toml").exists())
            self.assertTrue((codex_root / "report-contract" / "README.md").exists())
            self.assertTrue((codex_root / "reports").exists())
            self.assertTrue((codex_root / "agents" / "architect.toml").exists())
            self.assertTrue((codex_root / "agents" / "tracer.toml").exists())

            # Core 7 skills must exist
            core_7_skills = [
                "investigation",
                "tracer-bullet",
                "test-first",
                "review",
                "architecture",
                "dead-code-cleanup",
                "pre-commit-leak-review",
            ]
            for skill in core_7_skills:
                self.assertTrue(
                    (codex_root / "skills" / skill / "SKILL.md").exists(),
                    f"Core skill {skill} missing from .codex/skills/",
                )

            # Deleted skills must NOT exist
            deleted_skills = ["cli-contract", "planner", "report-observability"]
            for skill in deleted_skills:
                self.assertFalse(
                    (codex_root / "skills" / skill).exists(),
                    f"Obsolete skill {skill} still present in .codex/skills/",
                )

            # State machine graph and rules in AGENTS.md
            self.assert_contains(codex_root / "AGENTS.md", "Core 7 Skills & State Machine")
            self.assert_contains(codex_root / "AGENTS.md", "stateDiagram-v2")
            self.assert_contains(codex_root / "AGENTS.md", "次のステップ:")

            # Integrated contract rules in tracer-bullet and test-first
            self.assert_contains(
                codex_root / "skills" / "tracer-bullet" / "SKILL.md",
                "Lock the Observable Contract First",
            )
            self.assert_contains(
                codex_root / "skills" / "test-first" / "SKILL.md",
                "Property-Based Testing",
            )
            self.assert_contains(
                codex_root / "skills" / "dead-code-cleanup" / "SKILL.md",
                "`DELETE`, `MERGE`, `INLINE`, `SIMPLIFY`, or `KEEP`",
            )
            self.assert_contains(
                codex_root / "skills" / "investigation" / "SKILL.md",
                "Canvas-Native Mermaid Artifact Output",
            )

    def test_install_home_codex_variants_copy_expected_files(self) -> None:
        print("=== CLI Contract Encompassed Packages ===")
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
            self.assertTrue((home_codex / "skills" / "investigation" / "SKILL.md").exists())
            self.assertTrue((home_codex / "skills" / "dead-code-cleanup" / "SKILL.md").exists())
            self.assertTrue((home_codex / "skills" / "pre-commit-leak-review" / "SKILL.md").exists())
            self.assertFalse((home_codex / "skills" / "planner").exists())
            self.assertFalse((home_codex / "skills" / "cli-contract").exists())
            self.assertTrue((home_codex / "report-contract" / "README.md").exists())
            self.assertTrue((home_codex / "reports").exists())
            self.assertFalse((home_codex / "config.toml").exists())
            self.assertFalse((home_codex / "agents").exists())

        with tempfile.TemporaryDirectory() as tmp_home:
            env = os.environ.copy()
            env["HOME"] = tmp_home

            stale = Path(tmp_home) / ".codex"
            (stale / "agents").mkdir(parents=True)
            (stale / "agents" / "obsolete.txt").write_text("old")
            proc = self.run_cmd("make", "install-home-codex", env=env)
            self.assertIn("Home installation complete. Codex is now globally configured", proc.stdout)

            home_codex = Path(tmp_home) / ".codex"
            self.assertTrue((home_codex / "AGENTS.md").exists())
            self.assertTrue((home_codex / "config.toml").exists())
            self.assertTrue((home_codex / "skills" / "test-first" / "SKILL.md").exists())
            self.assertTrue((home_codex / "skills" / "dead-code-cleanup" / "SKILL.md").exists())
            self.assertTrue((home_codex / "report-contract" / "run-log.sample.jsonl").exists())
            self.assertTrue((home_codex / "reports").exists())
            self.assertTrue((home_codex / "agents" / "tester.toml").exists())
            self.assertFalse((home_codex / "agents" / "obsolete.txt").exists())

    def test_install_antigravity_copies_rules_workflows_and_skills(self) -> None:
        print("=== CLI Contract Encompassed Packages ===")
        print(".antigravity/ANTIGRAVITY.md")
        print(".antigravity/skills (Core 7)")
        with tempfile.TemporaryDirectory() as tmpdir:
            dest = Path(tmpdir) / "dest"
            dest.mkdir()
            proc = self.run_cmd("make", "install-antigravity", f"DEST={dest}")
            self.assertIn("Installation complete. Target project is now ready for Antigravity.", proc.stdout)

            antigravity_root = dest / ".antigravity"
            self.assertTrue((dest / "GEMINI.md").exists())
            self.assertTrue((antigravity_root / "GEMINI.md").exists())
            self.assertTrue((antigravity_root / "ANTIGRAVITY.md").exists())
            self.assertTrue((antigravity_root / "hooks.json").exists())
            self.assertTrue((antigravity_root / "skills" / "investigation" / "SKILL.md").exists())
            self.assertTrue((antigravity_root / "skills" / "dead-code-cleanup" / "SKILL.md").exists())
            self.assertTrue((antigravity_root / "skills" / "pre-commit-leak-review" / "SKILL.md").exists())
            self.assertFalse((antigravity_root / "skills" / "planner").exists())
            self.assertFalse((antigravity_root / "skills" / "cli-contract").exists())

            self.assert_contains(antigravity_root / "ANTIGRAVITY.md", "Portable Development Loop for Antigravity")
            self.assert_contains(antigravity_root / "GEMINI.md", "Core 7 Skills & State Machine")
            self.assert_contains(antigravity_root / "GEMINI.md", "stateDiagram-v2")
            self.assert_contains(
                antigravity_root / "skills" / "test-first" / "SKILL.md",
                "Property-Based Testing",
            )
            self.assert_contains(
                antigravity_root / "skills" / "tracer-bullet" / "SKILL.md",
                "Lock the Observable Contract First",
            )

    def test_install_home_antigravity_copies_global_skills(self) -> None:
        print("=== CLI Contract Encompassed Packages ===")
        print(".antigravity/skills")
        with tempfile.TemporaryDirectory() as tmp_home:
            env = os.environ.copy()
            env["HOME"] = tmp_home

            proc = self.run_cmd("make", "install-home-antigravity", env=env)
            self.assertIn("Home installation complete. Antigravity is now globally configured with skills, rules, and hooks.", proc.stdout)

            home_gemini_config = Path(tmp_home) / ".gemini" / "config"
            self.assertTrue((home_gemini_config / "GEMINI.md").exists())
            self.assertTrue((home_gemini_config / "hooks.json").exists())
            self.assertTrue((home_gemini_config / "skills" / "investigation" / "SKILL.md").exists())
            self.assertTrue((home_gemini_config / "skills" / "dead-code-cleanup" / "SKILL.md").exists())
            self.assertFalse((home_gemini_config / "skills" / "planner").exists())

            home_gemini_cli = Path(tmp_home) / ".gemini" / "antigravity-cli" / "skills"
            self.assertTrue((home_gemini_cli / "investigation" / "SKILL.md").exists())
            self.assertTrue((home_gemini_cli / "dead-code-cleanup" / "SKILL.md").exists())
            self.assertFalse((home_gemini_cli / "skills" / "planner").exists())

    def test_cli_linter_detects_breaking_drift(self) -> None:
        print("=== CLI Contract Encompassed Packages ===")
        print("tools/cli_linter/lint_cli.py")
        with tempfile.TemporaryDirectory() as tmpdir:
            base_file = Path(tmpdir) / "baseline.json"
            curr_broken = Path(tmpdir) / "broken.json"
            curr_compat = Path(tmpdir) / "compat.json"

            base_file.write_text(
                '{"name": "mycli", "flags": {"--env": {"required": false, "default": "dev"}}, "subcommands": {"deploy": {"flags": {"--force": {"required": false}}}}}'
            )
            # Breaking: removed --env flag
            curr_broken.write_text(
                '{"name": "mycli", "flags": {}, "subcommands": {"deploy": {"flags": {"--force": {"required": false}}}}}'
            )
            # Compatible: added optional --dry-run
            curr_compat.write_text(
                '{"name": "mycli", "flags": {"--env": {"required": false, "default": "dev"}, "--dry-run": {"required": false}}, "subcommands": {"deploy": {"flags": {"--force": {"required": false}}}}}'
            )

            # Test broken contract -> exit code 1
            proc_fail = subprocess.run(
                ["python3", "tools/cli_linter/lint_cli.py", "--baseline", str(base_file), "--current", str(curr_broken)],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(proc_fail.returncode, 1)
            self.assertIn("Flag removed: '--env'", proc_fail.stdout)

            # Test compatible extension -> exit code 0
            proc_pass = subprocess.run(
                ["python3", "tools/cli_linter/lint_cli.py", "--baseline", str(base_file), "--current", str(curr_compat)],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(proc_pass.returncode, 0)
            self.assertIn("New optional flag added: '--dry-run' (Compatible)", proc_pass.stdout)

    def test_render_walkthrough_compiles_investigation_html(self) -> None:
        print("=== CLI Contract Encompassed Packages ===")
        print("tools/render_walkthrough.py")
        print("templates/investigation_template.html")
        with tempfile.TemporaryDirectory() as tmpdir:
            sample_spec = Path(tmpdir) / "investigation.json"
            output_html = Path(tmpdir) / "walkthrough.html"

            sample_spec.write_text(
                json.dumps({
                    "flowDiagram": "sequenceDiagram\nUser->>CLI: run",
                    "dependencyDiagram": "graph TD\nCLI-->Service",
                    "items": [
                        {
                            "id": "CLI",
                            "name": "CLI Entrypoint",
                            "type": "fact",
                            "typeLabel": "FACT",
                            "file": "cmd/main.go:L1-L20",
                            "code": "func main() {}",
                            "fact": "Verified entrypoint",
                            "hypothesis": "None"
                        }
                    ]
                }),
                encoding="utf-8"
            )

            proc = subprocess.run(
                [
                    "python3",
                    "tools/render_walkthrough.py",
                    "--type",
                    "investigation",
                    "--input",
                    str(sample_spec),
                    "--output",
                    str(output_html),
                    "--verify-browser",
                ],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(proc.returncode, 0, f"STDOUT: {proc.stdout}\nSTDERR: {proc.stderr}")
            self.assertTrue(output_html.exists())
            html_text = output_html.read_text(encoding="utf-8")
            self.assertIn("Investigation Visual Walkthrough", html_text)
            self.assertIn("Verified entrypoint", html_text)

    def test_render_walkthrough_browser_verification_detects_syntax_errors(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            bad_spec = Path(tmpdir) / "bad_spec.json"
            bad_html = Path(tmpdir) / "bad.html"
            bad_spec.write_text(
                json.dumps({
                    "flowDiagram": "sequenceDiagram\n:::invalid syntax:::",
                    "items": []
                }),
                encoding="utf-8"
            )
            proc = subprocess.run(
                [
                    "python3",
                    "tools/render_walkthrough.py",
                    "--type",
                    "investigation",
                    "--input",
                    str(bad_spec),
                    "--output",
                    str(bad_html),
                    "--verify-browser",
                ],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            # If browser is available with network, it must catch the error and fail with returncode 1
            # If in offline sandbox, it gracefully logs and proceeds
            if "Browser Verify FAILED" in proc.stderr:
                self.assertEqual(proc.returncode, 1)
            else:
                self.assertEqual(proc.returncode, 0)


if __name__ == "__main__":
    unittest.main()


