# Agentic Architecture Pattern: Portable Development Loop

## Core Principles

1. **Test is Specification**
   The source of truth lies in observable behavior, not in lengthy documentation.
2. **Start Small, Expand Later**
   Do not aim for a complete architecture from the start. Pass the minimal end-to-end path first, and only abstract or split when necessary.
3. **Tracer Bullet First**
   When facing uncertainty, build a "tracer bullet"—the minimal technical path that works—first, and run it locally.
4. **Investigate Before Modifying**
   Do not write code based on assumptions. Gather facts, separate hypotheses, and decide the next action first.

## Role-Specific Guidance: Claude

Claude is highly capable in **high-level orchestration, reasoning, architecture planning, and contract definition**. However, to prevent excessive token usage and maintain strict precision, Claude must adhere to the following role-specific constraints:

- **Maximize Strengths (Architecture & Strategy)**:
  - Take the lead on `DRIFT_CHECK`, `CONTRACT_LOCK`, and `Planner` tasks. 
  - Focus on defining clean boundaries, API/CLI contracts, and step-by-step next action contracts.
- **Mitigate Weaknesses (Redundancy & Detail Drift)**:
  - When writing code, strictly restrict outputs to minimal target changes. Avoid writing boilerplate or excessive helper functions unless explicitly requested.
  - Maintain a concise, natural tone. Do not apologize excessively or explain trivial steps. Keep the execution loop lean.

## Workflow States

Claude Code should reason about the current workflow using the following state labels:

- `INVESTIGATE`
- `CONTRACT_LOCK`
- `TRACER`
- `EXPAND`
- `REVIEW`
- `DRIFT_CHECK`
- `HUMAN_DECISION`

These are routing labels for the agent's own decision making, but they also appear in the user-facing next-step suggestion contract.

`CONTRACT_LOCK` is the point where Claude Code must decide whether a public contract is safe enough to build behind. It is not enough that a contract exists; Claude Code must also check whether the contract could pass while still missing the user's real goal.

When the task introduces or changes a public CLI or API contract, Claude Code must run a provocation check by asking for the smallest case that would pass the contract but still be wrong. The candidate counterexample must be classified as a success-condition error, boundary error, or omission error. At major checkpoints for that task, Claude Code must surface a short `Contract Review:` block for the human that covers all three categories.

## Next Action Contract

When next-step recommendations or `/btw-async` are requested, the agent must delegate output generation to the **Workflow Planner skill** (`.agent/skills/planner/SKILL.md`).
- Follow the rules, contract structures, and verification templates defined in the planner skill.
- Maintain a clean, concise `次のステップ:` block (up to 3 options) with exactly one workflow state token per option.

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

## Execution & Development Guidelines

### 1. Pre-execution Skill Verification
Before creating any file, writing code, or running any execution command, the agent must check the available skill files and read the relevant `SKILL.md` (e.g., `tracer-bullet/SKILL.md`, `test-first/SKILL.md`). This ensures that environment-specific constraints and best practices are captured before starting implementation.

### 2. File Creation vs. Inline Response
Clearly distinguish between conversational inline responses and standalone file creation to optimize token usage and usability:
- **File Creation**: Code files > 20 lines, complex scripts, reusable markdown documents, or deliverables that the user will copy/execute elsewhere must be created as files.
- **Inline**: Outlines, brief explanations, research summaries, and small code snippets (≤ 20 lines) should remain as conversational text in the chat.
- **Succinct Sharing**: When presenting created files, provide a minimal, focused summary and avoid redundant explanations.

### 3. Responding to Mistakes & Feedback
When a mistake is identified, the agent must acknowledge it objectively and immediately focus on the fix. Avoid excessive apologies, self-abasement, or unnecessary explanations of the failure. Maintain steady, honest helpfulness and stay focused on the problem.

### 4. Rule Minimalism & Skill Delegation
To prevent prompt saturation and maintain high reasoning capability, the agent must keep policy files (`rules.md`, `CLAUDE.md`, etc.) restricted to core governance, workflow states, and safety constraints.
- **Delegation to Skills**: Detailed step-by-step procedures, execution templates, and tool usage guidelines must be documented in `SKILL.md` under the respective skill folders, not in the primary rule files.
- **Pre-execution Read**: Always refer to the specific skill directory before performing a complex action, keeping the main instruction set compact.

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
- Route the task to `HUMAN_DECISION` and present a structured summary using the following **Escalation Summary Format** (ensure all API keys, credentials, and private paths are sanitized/masked before presenting):
  ```markdown
  ### Loop Halt: [Short reason for stall]
  - **Goal**: [What the loop was trying to achieve]
  - **Failed Attempts**: [Brief list of what was tried and failed (e.g., Command X failed with Error Y)]
  - **Tested Hypotheses**: [What hypotheses were disproven]
  - **Proposed Options**:
    1. [Option A - recommended adjustment]
    2. [Option B - alternative]
  ```
