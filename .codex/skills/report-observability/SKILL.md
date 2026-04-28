---
name: Report Observability Hygiene
description: Define and operate lightweight runtime records without bloating the repo or leaking sensitive data
---

# Report Observability Hygiene

Use this skill when Codex needs to add, review, or operate workflow records under `.codex/reports/`.

## Purpose

Keep runtime observability useful without turning it into:

- repo bloat
- a source of secret leakage
- an orchestration engine

## Rules

- Treat `.codex/report-contract/` as the tracked contract.
- Treat `.codex/reports/` as local runtime output only.
- Store only the minimum facts needed to explain what happened.
- Prefer summaries over raw command output dumps.
- Redact or omit secrets, tokens, local-machine identifiers, and unnecessary paths.
- Keep runtime records append-only.
- Do not use runtime records to trigger automatic routing, retries, or approval decisions.

## Record Design

Each JSONL record should use:

- `facts`: timestamps, commands, exit codes, explicit human choices, stable file identifiers
- `inferences`: optional model summaries such as `recommended_state`, `risk_summary`, `why_now`

If a field is not needed to understand the decision or verification result, leave it out.

## Review Checklist

Before recommending a runtime record format, confirm:

- the same repo goal cannot be met with a tracked sample instead of a real log
- the record is small enough to append repeatedly
- the record avoids secrets and unnecessary workstation details
- the contract lives under `.codex/report-contract/`, not `.codex/reports/`
