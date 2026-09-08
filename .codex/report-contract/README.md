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

- `run-log.jsonl`: Task-level facts, capability tiers, evidence items, and overall outcomes
- `planner-checkpoints.jsonl`: Major checkpoint recommendations
- `verification-ledger.jsonl`: `Verify:` command results with explicit verification levels
- `human-decisions.jsonl`: Human approvals, stops, rationale, and contract-review decisions for public contract changes

## Schema 2.0.0 & Evidence Graph

Starting with schema version `2.0.0`, records support capability tier annotation and structured evidence claims.

### 1. Capability Tiers

Recorded under `facts.capability_tier`:
- `routine`: Low-latency, lightweight tasks (file search, formatting, simple linter runs)
- `standard`: Core implementation, test-first expansion, and refactoring
- `frontier`: High-complexity root-cause analysis, cross-module architecture, and ADR decisions

### 2. Verification Levels

Every verified assertion or evidence entry declares an explicit `level`:
- `LOCAL_STATIC`: Static analysis, AST validation, regex scans, code inspection
- `LOCAL_RUNTIME`: In-process contract tests, local unit/integration test executions
- `REMOTE_RUNTIME`: Remote CI runs, staging environment, containerized integration
- `PRODUCTION`: Production monitoring, canary observation, live telemetry

### 3. Evidence Schema

In `run-log.jsonl`, `facts.evidence` contains structured claims:
```json
{
  "claim": "Install preserves reports and creates backup",
  "command": "make test",
  "level": "LOCAL_RUNTIME",
  "status": "PASS"
}
```

## Shareability Guidelines (準公開サマリ規約)

When preparing handoff packets or cross-review documentation for peer AI models or external stakeholders:

1. **Strip Private Information**:
   - Do NOT include raw session JSONL logs or full prompt histories.
   - Do NOT expose absolute filesystem paths (e.g., `/Users/username/...`). Use relative paths rooted at workspace.
   - Do NOT expose environment secrets, tokens, or personal identifiers.
2. **Aggregated Facts & Evidence**:
   - Reference verification levels (`LOCAL_STATIC`, `LOCAL_RUNTIME`, etc.) and test commands instead of raw console dumps.
   - Use relative paths and concise diff summaries.

## Guardrails

- Treat runtime artifacts as **record-only**.
- Keep runtime records **append-only** during normal operation.
- Separate `facts` from `inferences`.
- Avoid storing secrets, raw tokens, or unnecessary local-machine details.
- Do not use runtime artifacts for automatic routing, retries, or approval enforcement.
