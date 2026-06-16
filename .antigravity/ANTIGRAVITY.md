# Agentic Architecture Pattern: Portable Development Loop for Antigravity

## Core Principles

1. **Test is Specification**
   The source of truth lies in observable behavior, not in lengthy documentation.
2. **Start Small, Expand Later**
   Do not aim for a complete architecture from the start. Pass the minimal end-to-end path first, and only abstract or split when necessary.
3. **Tracer Bullet First**
   When facing uncertainty, build a "tracer bullet"—the minimal technical path that works—first, and run it locally.
4. **Investigate Before Modifying**
   Do not write code based on assumptions. Gather facts, separate hypotheses, and decide the next action first.

## Role-Specific Guidance: Gemini / Antigravity

Gemini (Antigravity) possesses a **vast context window capable of ingestion and semantic lookup across the entire codebase and log history**. However, to maintain high compliance with long instructions and prevent task deviation, Gemini must adhere to the following role-specific constraints:

- **Maximize Strengths (Vast Context & Investigation)**:
  - Lead deep code exploration, impact analysis, logs troubleshooting, and broad context retrieval during the `INVESTIGATE` state.
  - Analyze multi-modal cues (such as UI/UX layout states) when relevant.
- **Mitigate Weaknesses (Focus Deviation & Instruction Compliance)**:
  - Deconstruct complex tasks into atomic, single-step operations. Execute commands and verify changes sequentially rather than attempting parallel massive edits.
  - When summarizing broad codebases or logs, use precise file references and short summaries. Avoid dumping massive code blocks back into the conversation context.

## Architectural Guardrails

Architecture is not a "perfect blueprint" but a "minimal set of constraints to prevent excessive drift."

- **Preserve Observable Boundaries**: Define and lock the contract (CLI inputs/outputs, exit codes, error classifications) before implementation, and do not break it.
- **Dependency Direction**: Strictly adhere to unidirectional dependencies: `CLI/UI → Domain → Adapters`.
- **No Cyclic Dependencies**: Do not create circular references between modules.
- **Minimal Boundaries**: Keep the structure simple; do not prematurely split into components until the scope demands it.

## Drift Classification

Every change must be evaluated and classified into one of three categories:

| Classification | State | Action |
|---|---|---|
| **NO_CHANGE** | Fits completely within existing ADRs, boundaries, contracts, and dependency rules. | Proceed as is. |
| **MINOR_UPDATE** | Direction is valid, but requires minor documentation updates or code cleanup (e.g., clarifying responsibility comments). | Clean up and proceed. |
| **STRUCTURAL_ADJUST** | Cannot be explained by existing guardrails. Breaks a boundary, responsibility, or contract. | **[STOP]** Immediately halt the implementation and propose an Architecture Decision Record (ADR) and evolution plan to the human. |

## Safety Restrictions

The following destructive actions are strictly prohibited without explicit human confirmation:
- Mass file deletion
- Widespread filesystem rewrites
- External side effects (e.g., executing structural changes on live infrastructure)

## Loop Governance & Self-Correction

To practice robust Loop Engineering and ensure reliable autonomous execution, the agent must adhere to the following execution loop rules:

### 1. Autonomous Retry Loop
When a command, test, or build fails, the agent must not immediately halt or prompt the user for help. Instead, it must autonomously initiate a self-correction loop:
1. **Analyze**: Inspect the error logs, trace output, and recent code changes.
2. **Hypothesize**: Formulate a clear hypothesis about the root cause of the failure.
3. **Execute & Verify**: Implement the corrected logic and re-run the verification command.

### 2. Infinite Loop & Stalling Prevention
To prevent resource waste and infinite looping:
- If the self-correction loop fails to resolve the issue after **3 attempts** (or if the implementation results in the same recurring error), the agent must halt autonomous execution.
- Route the task to `HUMAN_DECISION` and present a structured summary using the following **Escalation Summary Format**:
  ```markdown
  ### Loop Halt: [Short reason for stall]
  - **Goal**: [What the loop was trying to achieve]
  - **Failed Attempts**: [Brief list of what was tried and failed (e.g., Command X failed with Error Y)]
  - **Tested Hypotheses**: [What hypotheses were disproven]
  - **Proposed Options**:
    1. [Option A - recommended adjustment]
    2. [Option B - alternative]
  ```
