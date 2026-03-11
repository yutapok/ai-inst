# Antigravity Architecture Rules for Claude Code

This repository follows the **Antigravity Agentic Architecture Pattern**. As Claude Code, you must strictly adhere to the following principles, guardrails, and procedures during all interactions.

## 1. Core Principles & Workflow
- **Investigate Before Modifying**: Do not write code based on assumptions. Gather observable facts (logs, code), separate hypotheses, identify unknowns, and decide the next action (Tracer Bullet scope) first.
- **Tracer Bullet First**: Build the minimal, contiguous end-to-end execution path locally to prove viability. Do not prematurely abstract, split classes/modules, or handle exhaustive edge cases upfront.
- **Test is Specification**: Define the CLI Contract (inputs, stdout, stderr, exit codes) as an automated integration test *before* finalizing implementation.
- **Test-First Expansion**: Nurture the tracer bullet into production code by writing tests in this order: Representative Examples (Happy Path) → Contract Enforcement (Abnormal Flows) → Invariant Protection. Use Given/When/Then format.

## 2. Architectural Guardrails
- **Dependency Rules**: Strictly maintain unidirectional dependencies (`CLI/UI → Domain → Adapters`). No cyclic dependencies.
- **Minimal Boundaries**: Keep structure simple. Do not split prematurely.

## 3. Drift Classification & Stopping Condition
Evaluate every change. If it is `NO_CHANGE` or `MINOR_UPDATE`, proceed.
🚨 **[STOP] CONDITION (`STRUCTURAL_ADJUST`)**: If a change breaks a boundary, dependency rule, or public contract, you must **IMMEDIATELY HALT** implementation. Propose an Architecture Decision Record (ADR) detailing Context, Decision, and Consequences to the user for approval before continuing.

## 4. Safety Restrictions (Requires Human Confirmation)
- Mass file deletion
- Widespread filesystem rewrites
- Structural changes to live infrastructure

## 5. Multi-Agent Workflows
This repository supports custom Claude Code **Sub-agents**, mapping to the Antigravity architecture roles:

- `investigator`: Optimized for read-only fact gathering.
- `architect`: Evaluates structural boundaries and initiates ADRs if violations occur.
- `tracer`: Constructs the smallest viable end-to-end path (Tracer Bullet).
- `tester`: Implements exhaustive GWT tests and CLI Contracts.

### Sub-agents vs. Commands
- **Commands**: E.g., `/mission` expands a prompt macro into your *current* conversation context. Used to structure your own workflow.
- **Sub-agents**: These are *isolated, separate Claude sessions* with specialized system prompts, tools, and cost profiles. Used to delegate complete chunks of work to another "persona" (often in the background). 

**Usage Example:**
> "Please spawn the `investigator` to read through the `src/domain` codebase in the background, and report back the facts without making any code modifications."
