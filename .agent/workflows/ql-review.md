---
description: [Quality Loop] Asynchronous review for tech-debt, architecture formalization, and security.
---

# /ql-review

This workflow initiates a Quality Loop (QL) review. It performs a comprehensive heuristic review and formalizes "Implied ADRs" recorded during development. **It must NOT alter any code during this phase.**

## Agent Execution Steps

1. **Perform Review**
   - Read the codebase or the specified section.
   - Search for "Implied ADR" notes in `.agent/reports/tmp/implied-adr/implied-adr-*.md`.
   - Use the `review` skill to evaluate Architecture, Security, and Code Quality.
   - *(Required skill: `.agent/skills/review/SKILL.md`)*

2. **Generate Report**
   - Output the findings as a triagable checklist in `.agent/reports/ql-report-latest.md`.
   - Use `[ ]` syntax so the user can select items to fix or ADRs to formalize.
   - **STOP** and wait for human triage.

