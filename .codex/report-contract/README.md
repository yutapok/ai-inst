# Codex Report Contract

This directory contains the tracked contract for Codex workflow records.

Use it to define:

- which artifacts may be written at runtime
- which fields belong in those artifacts
- which data must remain local and uncommitted

## Separation of Concerns

- `.codex/report-contract/` is versioned documentation and sample data.
- `.codex/reports/` is the untracked runtime output directory.

Do not commit real runtime logs under `.codex/reports/`.

## Runtime Artifacts

- `run-log.jsonl`: Task-level facts and overall outcomes
- `planner-checkpoints.jsonl`: Major checkpoint recommendations
- `verification-ledger.jsonl`: `Verify:` command results
- `human-decisions.jsonl`: Human approvals, stops, rationale, and contract-review decisions for public contract changes

## Guardrails

- Treat runtime artifacts as **record-only**.
- Keep runtime records **append-only** during normal operation.
- Separate `facts` from `inferences`.
- Avoid storing secrets, raw tokens, or unnecessary local-machine details.
- Do not use runtime artifacts for automatic routing, retries, or approval enforcement.
