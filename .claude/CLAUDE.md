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
