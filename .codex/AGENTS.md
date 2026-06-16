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

## Role-Specific Guidance: Codex

Codex excels in **detailed implementation, rigorous logic verification, test-first expansion, and post-implementation cleanups**. However, to prevent local optimization and context loss, Codex must adhere to the following role-specific constraints:

- **Maximize Strengths (Precision & Implementation)**:
  - Lead execution during the `TRACER` (Tracer Bullet) and `EXPAND` (Test-First Expansion) states.
  - Drive code optimization, test coverage hardening, and dead-code removal (`dead-code-cleanup`).
- **Mitigate Weaknesses (Context Loss & Boundary Drift)**:
  - Before writing code, always perform an `INVESTIGATE` step to verify project-wide boundaries and dependency directions.
  - Never breach established CLI/API contracts. If a local change risks causing architectural drift (`STRUCTURAL_ADJUST`), immediately halt and escalate to `HUMAN_DECISION`.

## Codex Workflow Sources

For Codex, the canonical workflow source is:

1. **`AGENTS.md`**
   Persistent project policy, boundaries, and task-routing guidance.
2. **`skills/`**
   Reusable execution playbooks for investigation, tracer bullets, test-first expansion, CLI contracts, review, planning, and architecture governance.
3. **`report-contract/`**
   The tracked contract and samples for workflow records, defining what may be written locally without committing runtime logs.
4. **`agents/`**
   Optional role presets that bind a focused responsibility to one or more skills.
5. **`prompts/`**
   Compatibility shortcuts only. Prompts may remain available for legacy workflows, but they are not the source of truth.

When Codex has both a prompt and a skill available for the same workflow, it must follow the skill and this `AGENTS.md` first, and treat the prompt as a convenience entrypoint.

## Codex Distribution Tiers

The minimal portable `.codex` core is:

1. **`AGENTS.md`**
2. **`skills/`**
3. **`report-contract/`**

This core intentionally avoids model pins, multi-agent runtime settings, and prompt-surfacing assumptions so it remains resilient to Codex CLI and model changes.

Additional optional layers are:

- **`agents/`** for role presets and tool-specific execution hints
- **`prompts/`** for legacy compatibility only

## Skill Routing

Use the following skills by default for Codex tasks:

- **Investigation / debugging / impact analysis / research** → `skills/investigation/SKILL.md`
- **Locking observable CLI behavior** → `skills/cli-contract/SKILL.md`
- **Minimal viable end-to-end implementation** → `skills/tracer-bullet/SKILL.md`
- **Expanding coverage and hardening behavior** → `skills/test-first/SKILL.md`
- **Suggesting the next best action at workflow checkpoints** → `skills/planner/SKILL.md`
- **Architecture drift checks and ADR decisions** → `skills/architecture/SKILL.md`
- **Heuristic review for architecture, security, and maintainability** → `skills/review/SKILL.md`
- **Post-implementation code reduction and dead-code removal** → `skills/dead-code-cleanup/SKILL.md`
- **Pre-commit leak / privacy / secret exposure review** → `skills/pre-commit-leak-review/SKILL.md`
- **Runtime record hygiene / observability contract enforcement** → `skills/report-observability/SKILL.md`

If multiple skills apply, prefer the smallest set that matches the current task and preserve this order of operations:

1. Investigate
2. Lock the observable contract when relevant
3. Prove the minimal path
4. Expand coverage and invariants
5. Review for drift or broader quality risks
6. Remove dead, duplicate, or pointless code once behavior is already protected

## Adaptive Workflow Policy

Codex must infer the current workflow state from the user's prompt and the current code maturity. The user does not need to name a phase.

The internal workflow states are:

- `INVESTIGATE`
- `CONTRACT_LOCK`
- `TRACER`
- `EXPAND`
- `REVIEW`
- `DRIFT_CHECK`
- `HUMAN_DECISION`

These states are an internal routing tool, not a user-facing requirement. They are not strictly linear. Codex may move forward, backward, or temporarily insert `REVIEW` / `DRIFT_CHECK` when the situation warrants it.

`CONTRACT_LOCK` is the point where Codex must decide whether the public contract is safe enough to build behind. It is not enough that a contract exists; Codex must also check whether the contract could pass while still missing the user's real goal.

When the task introduces or changes a public CLI or API contract, Codex must run a provocation check by asking for the smallest case that would pass the contract but still be wrong. The candidate counterexample must be classified as a success-condition error, boundary error, or omission error. If the contract change reaches a major checkpoint, Codex must surface a short `Contract Review:` block for the human that covers all three categories.

### Tracer-before-Test-First Rule

Codex must prefer `TRACER` before `EXPAND` when any of the following are true:

- A new execution path is being introduced
- A new adapter or external integration is being added
- The observable contract is not yet fixed
- The implementation approach is still uncertain
- The blast radius is unclear

Codex may start with `EXPAND` or direct implementation when all of the following are true:

- The existing execution path already works
- The change is local and well understood
- The contract is unchanged or already protected
- The work is primarily a bug fix, narrow refactor, or pure test addition

When the `Tracer-before-Test-First Rule` says `TRACER`, Codex must not jump directly into broad test-first expansion.

### Flexible Insertion Rules

Codex may insert `INVESTIGATE`, `REVIEW`, or `DRIFT_CHECK` between implementation steps when needed.

- Re-enter `INVESTIGATE` when new uncertainty appears
- Return to `CONTRACT_LOCK` when provocation reveals an unresolved contract concern
- Insert `REVIEW` when implementation has accumulated enough risk or surface area
- Insert `DRIFT_CHECK` when architectural boundaries, public contracts, or technology choices may have changed
- Move to `HUMAN_DECISION` when the unresolved concern is about product meaning, public boundary semantics, or responsibility boundaries rather than code mechanics

### Review and Drift Triggers

Queue a `REVIEW` recommendation when any of the following are true:

- The implementation has grown across multiple files or modules
- A tracer bullet has been expanded beyond the happy path
- Performance, security, or maintainability concerns are visible
- The implementation works but now contains dead code, duplicate logic, or cleanup opportunities
- Temporary implied ADR notes exist
- The user asks for hardening, cleanup, or broader confidence

Queue a `DRIFT_CHECK` recommendation when any of the following are true:

- Dependency direction has changed
- Responsibilities moved across boundaries
- Public CLI or API contracts changed
- New technology or infrastructure choices were introduced
- New wiring crosses architectural boundaries

If the likely result is `STRUCTURAL_ADJUST`, stop autonomous evolution and move to `HUMAN_DECISION`.

### Next Action Contract

At major checkpoints, Codex must provide a short next-step recommendation using the planner skill. This is an `AGENTS.md` / planner output contract, not a Codex CLI Plan mode feature. Major checkpoints include:

- End of the current turn
- After a tracer bullet is proven
- After a meaningful expansion milestone
- When review or drift triggers are observed
- Before waiting for a human decision
- In the final response after implementation or investigation work completes for the current turn

The planner output must use a numbered `次のステップ:` section and keep it concise.

- Each step must include exactly one workflow state token.
- Execution markers are optional and limited to `(Recommended)` and `<ASYNC>`.
- Step `1.` is required and is the only recommended option; it must be labeled `(Recommended)`.
- When the recommendation assumes repo code changes, add a short `Verify:` line under step `1.` with a local build, test, or command for the user.
- Keep `Verify:` to one command and one observation point so the user can run it without choosing among alternatives.
- Use `<ASYNC>` only for independently parallelizable sidecar options that do not block the recommended path.
- Omit any execution marker for synchronous follow-up options.
- Attempt to split recommendations into independently parallelizable instructions when feasible, but keep the critical path in the recommended option.
- Offer at most 3 options.
- Workflow state tokens must remain exactly: `INVESTIGATE`, `CONTRACT_LOCK`, `TRACER`, `EXPAND`, `REVIEW`, `DRIFT_CHECK`, `HUMAN_DECISION`.
- Add a short `Current Read:` line before `次のステップ:` only when the surrounding context is not already obvious.
- When a task changes a public contract and reaches a major checkpoint, include a short `Contract Review:` block covering success-condition error, boundary error, and omission error before recommending `EXPAND`.
- If any line in that review is unresolved, do not recommend `EXPAND`; recommend `CONTRACT_LOCK` or `HUMAN_DECISION` instead.

The canonical format is:

```markdown
Current Read: [short status if needed]

次のステップ:
1. (Recommended) [WORKFLOW_STATE]: [short action]
   Verify: [one command + one observation point]
2. <ASYNC> [WORKFLOW_STATE]: [short action]
3. [WORKFLOW_STATE]: [short action]
```

## Record-Only Observability

Use `.codex/report-contract/` as the tracked contract and `.codex/reports/` as the local runtime output directory.

- `run-log.jsonl`: Task-level facts and overall outcomes
- `planner-checkpoints.jsonl`: Major checkpoint recommendations
- `verification-ledger.jsonl`: `Verify:` command results
- `human-decisions.jsonl`: Human approvals, stops, and rationale

These artifacts must remain **record-only**:

- Allowed: tracked samples and schemas under `.codex/report-contract/`, plus append-only local records under `.codex/reports/`
- Not allowed: log-driven routing, automatic retries, approval enforcement, or any other runtime control loop
- Do not commit real runtime logs under `.codex/reports/`

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
