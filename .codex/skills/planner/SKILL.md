---
name: Workflow Planner
description: Decide the next best user-facing action at workflow checkpoints and present concise options.
---

# Workflow Planner

Use this skill at major checkpoints to make the next action explicit without requiring the user to think in phases.

This skill does not perform implementation, review, or drift classification itself. Its job is to read the current situation and propose the next best move.

## When to Use It

Use this skill:

- At the end of the current turn
- After a tracer bullet is proven
- After a meaningful test-first expansion milestone
- When review or drift triggers are observed
- Before pausing for human input or approval

Do not use it after every tiny step. Reserve it for meaningful checkpoints.

## Inputs to Consider

Before proposing the next action, inspect:

- What the user actually asked for
- What was completed in the current turn
- What remains uncertain
- Whether the contract is already fixed
- Whether a tracer bullet already exists
- Whether review triggers are present
- Whether drift triggers are present

## Decision Rules

When choosing the recommendation:

1. Prefer the smallest action that unlocks the next useful learning.
2. Prefer tracer-bullet work over broad test-first expansion when uncertainty is still high.
3. Prefer review when the implementation has accumulated surface area or quality risk.
4. Prefer drift-check when architectural boundaries or contracts may have changed.
5. Prefer human decision when the likely result is a structural adjustment.

## Output Contract

Keep the output short and user-facing.

- Use a numbered `次のステップ:` section as the canonical output.
- Include `Current Read:` only when the current situation is not already obvious from the surrounding response.
- Provide up to 3 options.
- Mark only option `1.` as recommended using `（推奨）`.
- Every option must contain exactly one workflow state token from: `INVESTIGATE`, `CONTRACT_LOCK`, `TRACER`, `EXPAND`, `REVIEW`, `DRIFT_CHECK`, `HUMAN_DECISION`.
- Keep surrounding prose in the user's language, but keep workflow state tokens in uppercase English.

## Output Template

```markdown
Current Read: [short status if needed]

次のステップ:
1. （推奨）: [WORKFLOW_STATE] [short action]
2. [WORKFLOW_STATE] [short action]
3. [WORKFLOW_STATE] [short action]
```
