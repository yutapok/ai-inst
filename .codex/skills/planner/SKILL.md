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
2. Treat a contract as fixed only if provocation has been run and no contract-review concern remains unresolved.
3. Prefer tracer-bullet work over broad test-first expansion when uncertainty is still high.
4. Prefer review when the implementation has accumulated surface area or quality risk.
5. Prefer drift-check when architectural boundaries or contracts may have changed.
6. Prefer human decision when the likely result is a structural adjustment or an unresolved contract meaning question.

## Output Contract

Keep the output short and user-facing.

- Use a numbered `次のステップ:` section as the canonical output.
- Include `Current Read:` only when the current situation is not already obvious from the surrounding response.
- When a task introduces or changes a public contract and reaches a major checkpoint, include a short `Contract Review:` block before `次のステップ:`.
- Use this structure:

```markdown
Contract Review:
- Success-condition error: [No concern / Needs review: ...]
- Boundary error: [No concern / Needs review: ...]
- Omission error: [No concern / Needs review: ...]
```

- Keep each review line to a single short sentence.
- If any review line says `Needs review`, do not recommend `EXPAND`.
- Provide up to 3 options.
- Mark only option `1.` as recommended using `（推奨）`.
- Keep option `1.` as the synchronous mainline recommendation; do not mark the recommended option as `（Async）`.
- When the recommendation assumes repo code changes, add a short `Verify:` line under option `1.` with a local build, test, or command the user can run.
- Keep `Verify:` to one command and one observation point so the user can run it without choosing among alternatives.
- Use `Verify:` to help the user validate and better understand AI-generated changes locally.
- When a sidecar option can be delegated independently in parallel, prefix the action with `（Async）`.
- Try to decompose the alternatives into independently parallelizable sidecars when feasible, without moving the critical path out of option `1.`.
- For each `（Async）` option, attach a minimal `Async Task Envelope` using these four fields:
  - `Goal:` what the delegated session should determine or produce
  - `Scope:` the files, modules, or responsibility boundary it may touch
  - `Done:` the completion condition or expected output format
  - `Non-goals:` the work it must not expand into
- Keep the envelope short. Prefer one short line per field.
- Every option must contain exactly one workflow state token from: `INVESTIGATE`, `CONTRACT_LOCK`, `TRACER`, `EXPAND`, `REVIEW`, `DRIFT_CHECK`, `HUMAN_DECISION`.
- Keep surrounding prose in the user's language, but keep workflow state tokens in uppercase English.

## Output Template

```markdown
Current Read: [short status if needed]

次のステップ:
1. （推奨）[WORKFLOW_STATE]: [short action]
   Verify: [one command + one observation point]
2. [WORKFLOW_STATE]: （Async）[short action]
   Goal: [short goal]
   Scope: [short scope]
   Done: [short completion condition]
   Non-goals: [short exclusions]
3. [WORKFLOW_STATE]: [short action]
```
