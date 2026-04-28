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

When `/btw-async` is used, Claude Code must return a short next-step recommendation using the following format:

- Add `Current Read:` only when the status is not already obvious.
- Then emit a numbered `次のステップ:` section.
- Step `1.` is the only recommended option and must be labeled `（推奨）`.
- When the recommendation assumes repo code changes, add a short `Verify:` line under step `1.` with a local build, test, or command for the user.
- Keep `Verify:` to one command and one observation point so the user can run it without choosing among alternatives.
- If a step can be issued independently in parallel, prefix that action with `（Async）`.
- Attempt to split recommendations into independently parallelizable instructions when feasible.
- Offer at most 3 options.
- Each option must contain exactly one workflow state token.
- When the task changes a public contract and reaches a major checkpoint, include a short `Contract Review:` block covering success-condition error, boundary error, and omission error before recommending `EXPAND`.
- If any review line is unresolved, do not recommend `EXPAND`; recommend `CONTRACT_LOCK` or `HUMAN_DECISION` instead.

The canonical format is:

```markdown
Current Read: [short status if needed]

次のステップ:
1. （推奨）[WORKFLOW_STATE]: [short action]
   Verify: [one command + one observation point]
2. [WORKFLOW_STATE]: （Async）[short action]
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
