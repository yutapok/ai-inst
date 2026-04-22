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

## Codex Workflow Sources

For Codex, the canonical workflow source is:

1. **`AGENTS.md`**
   Persistent project policy, boundaries, and task-routing guidance.
2. **`skills/`**
   Reusable execution playbooks for investigation, tracer bullets, test-first expansion, CLI contracts, review, planning, and architecture governance.
3. **`agents/`**
   Optional role presets that bind a focused responsibility to one or more skills.
4. **`prompts/`**
   Compatibility shortcuts only. Prompts may remain available for legacy workflows, but they are not the source of truth.

When Codex has both a prompt and a skill available for the same workflow, it must follow the skill and this `AGENTS.md` first, and treat the prompt as a convenience entrypoint.

## Skill Routing

Use the following skills by default for Codex tasks:

- **Investigation / debugging / impact analysis / research** → `skills/investigation/SKILL.md`
- **Locking observable CLI behavior** → `skills/cli-contract/SKILL.md`
- **Minimal viable end-to-end implementation** → `skills/tracer-bullet/SKILL.md`
- **Expanding coverage and hardening behavior** → `skills/test-first/SKILL.md`
- **Suggesting the next best action at workflow checkpoints** → `skills/planner/SKILL.md`
- **Architecture drift checks and ADR decisions** → `skills/architecture/SKILL.md`
- **Heuristic review for architecture, security, and maintainability** → `skills/review/SKILL.md`
- **Pre-commit leak / privacy / secret exposure review** → `skills/pre-commit-leak-review/SKILL.md`

If multiple skills apply, prefer the smallest set that matches the current task and preserve this order of operations:

1. Investigate
2. Lock the observable contract when relevant
3. Prove the minimal path
4. Expand coverage and invariants
5. Review for drift or broader quality risks

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
- Insert `REVIEW` when implementation has accumulated enough risk or surface area
- Insert `DRIFT_CHECK` when architectural boundaries, public contracts, or technology choices may have changed

### Review and Drift Triggers

Queue a `REVIEW` recommendation when any of the following are true:

- The implementation has grown across multiple files or modules
- A tracer bullet has been expanded beyond the happy path
- Performance, security, or maintainability concerns are visible
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

At major checkpoints, Codex must provide a short next-step recommendation using the planner skill. Major checkpoints include:

- End of the current turn
- After a tracer bullet is proven
- After a meaningful expansion milestone
- When review or drift triggers are observed
- Before waiting for a human decision

The planner output must use a numbered `次のステップ:` section and keep it concise.

- Each step must include exactly one workflow state token.
- Step `1.` is the only recommended option and must be labeled `（推奨）`.
- Offer at most 3 options.
- Workflow state tokens must remain exactly: `INVESTIGATE`, `CONTRACT_LOCK`, `TRACER`, `EXPAND`, `REVIEW`, `DRIFT_CHECK`, `HUMAN_DECISION`.
- Add a short `Current Read:` line before `次のステップ:` only when the surrounding context is not already obvious.

The canonical format is:

```markdown
Current Read: [short status if needed]

次のステップ:
1. （推奨）[WORKFLOW_STATE]: [short action]
2. [WORKFLOW_STATE]: [short action]
3. [WORKFLOW_STATE]: [short action]
```

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
