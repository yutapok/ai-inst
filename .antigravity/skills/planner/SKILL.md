---
name: Workflow Planner
description: Suggest the next best action from the current state using workflow states and a short numbered 次のステップ section.
---

# Workflow Planner

Use this skill when the task is not to do the work itself, but to recommend the next inspection or implementation move from the current situation.

This skill stands on its own. It is the required skill for next-step recommendations, and it may also be reused at meaningful checkpoints.

## When To Use It

Use this skill:

- When the user asks what should happen next
- When enough changes have accumulated that an inspection might be useful
- When the current path may need broad review or architectural drift verification
- When you want a short, decision-oriented answer instead of more implementation

## Decision Rules

When building the recommendation:

1. Treat a contract as fixed only if provocation has been run and no contract-review concern remains unresolved.
2. Prefer `REVIEW` when implementation surface area, risk, or uncertainty has grown and a broad inspection would reduce risk.
3. Prefer `DRIFT_CHECK` when responsibilities, contracts, dependency direction, or technology choices may have shifted.
4. Prefer `INVESTIGATE` when the real blocker is still missing facts rather than inspection.
5. Prefer `HUMAN_DECISION` when the likely result is a structural adjustment, approval gate, or unresolved contract meaning question.
6. Keep the result short and action-oriented.

## Output Contract

- Include `Current Read:` only when needed.
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
- Then output `次のステップ:`.
- Provide up to 3 options.
- Mark only option `1.` as `（推奨）`.
- When the recommendation assumes repo code changes, add a short `Verify:` line under option `1.` with a local build, test, or command the user can run.
- Keep `Verify:` to one command and one observation point so the user can run it without choosing among alternatives.
- Use `Verify:` to help the user validate and better understand AI-generated changes locally.
- When an option can be delegated independently in parallel, prefix the action with `（Async）`.
- Try to decompose the recommendation into independently parallelizable instructions when feasible.
- For each `（Async）` option, attach a minimal `Async Task Envelope` using these four fields:
  - `Goal:` what the delegated session should determine or produce
  - `Scope:` the files, modules, or responsibility boundary it may touch
  - `Done:` the completion condition or expected output format
  - `Non-goals:` the work it must not expand into
- Keep the envelope short. Prefer one short line per field.
- Every option must contain exactly one workflow state token from:
  - `INVESTIGATE`
  - `CONTRACT_LOCK`
  - `TRACER`
  - `EXPAND`
  - `REVIEW`
  - `DRIFT_CHECK`
  - `HUMAN_DECISION`

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
