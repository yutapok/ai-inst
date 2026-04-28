# Principles & Workflows for Autonomous Coding Agents

This repository provides the core **principles, architectural guardrails, workflows, and skills** necessary to safely and effectively introduce autonomous coding agents into a software project.

Rather than letting AI agents guess implementation details or make speculative architectural decisions, these configurations enforce a strict, test-driven development loop. They ensure that agents investigate before modifying, establish automated CLI test contracts, and seek human approval before enacting structural changes.

## Supported Agents

We provide tailored instructions and skill definitions for various AI agent platforms:

- **`.agent`**: The generic / platform-independent rules and skills. Compatible with **Antigravity** and other CLI-based agent frameworks.
- **`.claude`**: Optimized for **Claude Code**. Leverages Claude's custom slash commands (e.g., `/mission`, `/expand`, `/btw-async`) and Markdown-based skill framework.
- **`.codex`**: Optimized for **OpenAI Codex** (and similar IDE-based agents like Cursor/Copilot). Uses `AGENTS.md` as the canonical policy layer, `skills/` as reusable workflows, `report-contract/` as the tracked runtime-record contract, and optional `agents/` presets for focused roles including next-step planning. `prompts/` is retained only as a compatibility layer.

## Core Concepts

By installing this configuration, your coding agents will be bound by the following concepts:

1. **Investigation Methodology**: Agents must gather facts, form hypotheses, and declare unknown variables before mutating files.
2. **Tracer Bullet Methodology**: Agents must prove the minimal end-to-end viable path locally before attempting complex abstractions.
3. **CLI Contract Enforcement**: The external boundary must be locked down via an automated integration test *before* internal implementation begins.
4. **Test-First Expansion**: Agents must expand the Tracer Bullet using a Given/When/Then (GWT) approach (Examples → Contracts → Invariants).
5. **Architecture Governance**: Agents must evaluate file drift. Any structural boundary violation must trigger a hard **STOP** and result in an Architecture Decision Record (ADR) proposal for human review.

## Installation

You can use the included `Makefile` to install the appropriate configuration into your target project.

1. Open a terminal in this repository.
2. Run the `make` command corresponding to your target agent, specifying your target project's path using the `DEST` variable.

```bash
# Install generic .agent configs
make install DEST=/path/to/your/project

# Install Claude Code (.claude) configs
make install-claude DEST=/path/to/your/project

# Install Codex (.codex) configs
make install-codex DEST=/path/to/your/project

# Install Codex core config to ~/.codex with AGENTS.md + skills + report-contract
make install-home-codex-core

# Install Codex config to ~/.codex with compatibility prompts
make install-home-codex

# Install Codex config to ~/.codex without prompts
make install-home-codex-minimal
```

## Structure

- **`rules.md` / `CLAUDE.md` / `AGENTS.md`**: The primary entrypoints and guardrail definitions.
- **`skills/`**: Specific playbooks detailing how the agent should handle architecture governance, investigation, tracer bullets, CLI contracts, test-first expansion, review timing, and next-step planning.
- **`dead-code-cleanup`**: A post-implementation cleanup skill for removing unused, duplicate, or unnecessarily verbose code once behavior is already protected.
- **`report-contract/`**: Tracked schemas, samples, and guardrails for runtime records.
- **`agents/`**: Optional Codex role presets that bind a responsibility to one or more skills.
- **`commands/` / `workflows/`**: (Platform-specific) The predefined workflows for the agents to follow during the development cycle (e.g., `/mission` and `/expand`).
- **Claude `/btw-async`**: A short next-step suggester for deciding when to insert asynchronous inspection such as `/ql-review` or `/drift-check`.
  Recommended option `1.` stays on the main path; independently parallelizable side tasks should be prefixed with `（Async）`.
- **`prompts/`**: Codex compatibility shortcuts retained for legacy workflows, but not the canonical source of behavior.

## Codex Usage Model

For Codex, prefer the following order of authority:

1. **`AGENTS.md`** for persistent repo policy and task-routing guidance
2. **`skills/`** for reusable execution playbooks
3. **`report-contract/`** for tracked schemas, samples, and guardrails for runtime records
4. **`agents/`** for focused presets such as investigator, tracer, tester, planner, and architect
5. **`prompts/`** only as optional shortcuts for legacy workflows

This matters because recent Codex versions may not reliably surface custom prompts from `~/.codex/prompts`, while `AGENTS.md`, installed skills, and the tracked report contract remain the stable path. Agent presets are still useful, but they are intentionally optional because model pins and multi-agent runtime assumptions are more likely to drift across Codex CLI releases.

Recommended Codex distribution tiers:

- `core`: `AGENTS.md + skills + report-contract`
- `minimal`: `AGENTS.md + skills + report-contract + agents`
- `full`: `AGENTS.md + skills + report-contract + agents + prompts`

Recommended skill routing for Codex:

- Investigation, debugging, impact analysis, and research -> `investigation`
- Observable CLI definition and regression guardrails -> `cli-contract`
- Minimal viable end-to-end path -> `tracer-bullet`
- Coverage expansion and invariant protection -> `test-first`
- Next-step recommendation at major checkpoints -> `planner`
- Architecture drift checks and ADR decisions -> `architecture`
- Broad review and triage -> `review`
- Post-implementation code reduction and dead-code removal -> `dead-code-cleanup`
- Runtime record hygiene and report-scope control -> `report-observability`
- Pre-commit leak / privacy / secret exposure review -> `pre-commit-leak-review`

`dead-code-cleanup` is intentionally narrower than `review`: use `review` to surface broad quality risks, and use `dead-code-cleanup` when the main question is what can now be deleted, merged, inlined, or simplified without changing intended behavior.

`make install-home-codex-core` installs the long-lived portable core: `AGENTS.md + skills + report-contract`.

`make install-home-codex-minimal` installs `AGENTS.md + skills + report-contract + agents`.

`make install-home-codex` installs `AGENTS.md + skills + report-contract + agents` and also keeps `prompts/` for backward compatibility.

Use `.codex/report-contract/` for tracked samples and `.codex/reports/` for untracked runtime output. The files in `.codex/reports/` are **record-only**. They may store facts, verifications, recommendations, and human decisions, but they must not become inputs for automatic routing, retries, or approval enforcement.

## Post-Install Operator Notes

After distribution, the user-facing next-step guidance should stay aligned across Claude and Codex:

- Use a numbered `次のステップ:` section for checkpoint recommendations.
- Mark only `1.` as recommended with `（推奨）`.
- When `1.` assumes code changes, add a short `Verify:` line with a local build, test, or command for the user.
- Keep `Verify:` to one command and one observation point so the user can run it without choosing among alternatives.
- When a follow-up can run independently in parallel, prefix that action with `（Async）`.
- Keep workflow state tokens explicit: `INVESTIGATE`, `CONTRACT_LOCK`, `TRACER`, `EXPAND`, `REVIEW`, `DRIFT_CHECK`, `HUMAN_DECISION`.
- Add `Current Read:` only when the current status is not already obvious.

Canonical format:

```markdown
Current Read: [short status if needed]

次のステップ:
1. （推奨）[WORKFLOW_STATE]: [short action]
   Verify: [one command + one observation point]
2. [WORKFLOW_STATE]: （Async）[short action]
3. [WORKFLOW_STATE]: [short action]
```

For Claude users, `/btw-async` is the lightweight entrypoint for these inspection-oriented recommendations and can point to follow-up checks such as `/ql-review` or `/drift-check`.

## Verification

Run the repository integration checks with:

```bash
make test
```

These checks verify the distributed Codex configuration still:

- installs the required `AGENTS.md`, skills, report-contract, prompts, and agent presets
- preserves the CLI-contract requirement for automated integration tests
- preserves the planner output contract built around `次のステップ:`, `Verify:`, `（Async）`, and explicit workflow states
