# Autonomous Agent Instructions (Antigravity Architecture)

Welcome to the Antigravity codebase. As an autonomous AI coding agent, your actions are governed by strict architectural guardrails and a test-driven development loop.

## 1. Safety & Investigation (READ FIRST)
- **Do Not Guess**: Always "Investigate Before Modifying". Extract facts, separate hypotheses, and clarify unknowns before making modifications.
- **Destructive Actions**: Mass deletions, big rewrites, and external infra changes are strictly prohibited without explicit human authorization.

## 2. Portable Development Loop
- **Tracer Bullet Methodology**: Always implement the smallest viable end-to-end path first. Run it locally. Hardcoding is permitted initially. Avoid premature abstraction.
- **CLI Contract Definition**: The external boundary must be defined as an automated integration test. Assert inputs, expected `stdout`, expected `stderr`, and exit codes. This is your regression guardrail.
- **Test-First Expansion**: After the tracer bullet works, expand via GWT (Given/When/Then) tests:
  1. Examples (Happy path)
  2. Contracts (Error handling/exit codes)
  3. Invariants (Encapsulation/state defense)

## 3. Architecture Governance
- **Strict Dependencies**: `CLI/UI → Domain → Adapters`. Never violate this direction and never create cycles.
- **Drift Classification**: Evaluate changes across 5 vectors (Dependency, Cyclic, Responsibility, Contract, Tech Choice).
- 🛑 **EVOLUTION HALT (`STRUCTURAL_ADJUST`)**: If your proposed code violates existing boundaries or contracts, you must **STOP**. Do not proceed with the change autonomously. Instead, draft an Architecture Decision Record (ADR) containing Context, Decision, and Consequences, and present it to the human for approval.

## 4. Agent Skills & Commands
This repository contains specific skills to enforce the Antigravity architecture. You must use these skills located in `.codex/skills/`:
- **When analyzing tasks or starting work (`/mission`)**: ALWAYS use the `investigation` and `tracer-bullet` skills to define the scope and prove viability locally first.
- **When a Tracer Bullet is complete (`/expand`)**: ALWAYS use the `cli-contract` and `test-first` skills to write automated integration tests and expand the GWT (Given/When/Then) test suites.
- **Before making any file modifications**: ALWAYS use the `architecture` skill to evaluate drift and determine if an ADR is required.

## 5. Multi-Agent Roles 
Codex's `multi_agent` feature is enabled for this project. When dealing with complex tasks, you can orchestrate or spawn dedicated sub-agents optimized for specific Antigravity architectural phases:

- `investigator`: Uses the investigation skill to strictly perform read-only fact-finding and evidence gathering.
- `architect`: Evaluates structural changes (drift) in read-only mode and formulates necessary ADRs.
- `tracer`: Optimized to execute Tracer Bullet implementations with minimal abstractions.
- `tester`: Focuses specifically on Test-First Expansion and CLI Contract implementation.

**Usage Example:**
> "I need to add a new CLI command to clear the cache. Spawn an `investigator` to map the current architecture, then use `architect` to verify no boundaries are broken, and finally have `tracer` and `tester` implement it."
