---
description: [Quality Loop] Asynchronous review for tech-debt, architecture formalization, and security.
---

# /ql-review

Compatibility note: this prompt is a legacy shortcut. The canonical workflow lives in `.codex/AGENTS.md` and `.codex/skills/review/SKILL.md`.

This workflow initiates a Quality Loop (QL) review. It performs a comprehensive heuristic review and formalizes "Implied ADRs" recorded during development. **It must NOT alter any code during this phase.**

Use this when review triggers have accumulated enough risk or surface area that a review should be inserted before more implementation continues.

## Agent Execution Steps

1. **Perform Review**
   - Read the codebase or the specified section.
   - Search for "Implied ADR" notes in `.codex/reports/tmp/implied-adr/implied-adr-*.md`.
   - Use the `review` skill to evaluate Architecture, Security, and Code Quality.
   - *(Required skill: `.codex/skills/review/SKILL.md`)*

2. **Generate Report**
   - Output the findings as a triagable checklist in `.codex/reports/ql-report-latest.md`.
   - Use `[ ]` syntax so the user can select items to fix or ADRs to formalize.
   - **STOP** and wait for human triage.
   - Include a short planner-style next action recommendation for the user.
