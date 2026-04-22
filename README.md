# Principles & Workflows for Autonomous Coding Agents

This repository provides the core **principles, architectural guardrails, workflows, and skills** necessary to safely and effectively introduce autonomous coding agents into a software project.

Rather than letting AI agents guess implementation details or make speculative architectural decisions, these configurations enforce a strict, test-driven development loop. They ensure that agents investigate before modifying, establish automated CLI test contracts, and seek human approval before enacting structural changes.

## Supported Agents

We provide tailored instructions and skill definitions for various AI agent platforms:

- **`.agent`**: The generic / platform-independent rules and skills. Compatible with **Antigravity** and other CLI-based agent frameworks.
- **`.claude`**: Optimized for **Claude Code**. Leverages Claude's custom slash commands (e.g., `/mission`, `/expand`) and Markdown-based skill framework.
- **`.codex`**: Optimized for **OpenAI Codex** (and similar IDE-based agents like Cursor/Copilot). Uses `AGENTS.md` as the canonical policy layer, `skills/` as reusable workflows, and optional `agents/` presets for focused roles including next-step planning. `prompts/` is retained only as a compatibility layer.

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

# Install Codex config to ~/.codex with compatibility prompts
make install-home-codex

# Install Codex config to ~/.codex without prompts
make install-home-codex-minimal
```

## Structure

- **`rules.md` / `CLAUDE.md` / `AGENTS.md`**: The primary entrypoints and guardrail definitions.
- **`skills/`**: Specific playbooks detailing how the agent should handle architecture governance, investigation, tracer bullets, CLI contracts, test-first expansion, review timing, and next-step planning.
- **`agents/`**: Optional Codex role presets that bind a responsibility to one or more skills.
- **`commands/` / `workflows/`**: (Platform-specific) The predefined workflows for the agents to follow during the development cycle (e.g., `/mission` and `/expand`).
- **`prompts/`**: Codex compatibility shortcuts retained for legacy workflows, but not the canonical source of behavior.

## Codex Usage Model

For Codex, prefer the following order of authority:

1. **`AGENTS.md`** for persistent repo policy and task-routing guidance
2. **`skills/`** for reusable execution playbooks
3. **`agents/`** for focused presets such as investigator, tracer, tester, planner, and architect
4. **`prompts/`** only as optional shortcuts for legacy workflows

This matters because recent Codex versions may not reliably surface custom prompts from `~/.codex/prompts`, while `AGENTS.md` and installed skills remain the stable path.

Recommended skill routing for Codex:

- Investigation, debugging, impact analysis, and research -> `investigation`
- Observable CLI definition and regression guardrails -> `cli-contract`
- Minimal viable end-to-end path -> `tracer-bullet`
- Coverage expansion and invariant protection -> `test-first`
- Next-step recommendation at major checkpoints -> `planner`
- Architecture drift checks and ADR decisions -> `architecture`
- Broad review and triage -> `review`

`make install-home-codex` installs `AGENTS.md + skills + agents` and also keeps `prompts/` for backward compatibility.

`make install-home-codex-minimal` installs only the supported long-term path: `AGENTS.md + skills + agents`.

## Verification

Run the repository integration checks with:

```bash
make test
```

These checks verify the distributed Codex configuration still:

- installs the required `AGENTS.md`, skills, prompts, and agent presets
- preserves the CLI-contract requirement for automated integration tests
- preserves the planner output contract built around `次のステップ:` and explicit workflow states
