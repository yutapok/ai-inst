---
description: [Quality Loop] Asynchronous review for tech-debt, architecture formalization, and security.
---

# /ql-review

This workflow initiates a Quality Loop (QL) review. It performs a comprehensive heuristic review and formalizes "Implied ADRs" recorded during development. **It must NOT alter any code during this phase.**

## Agent Execution Steps

1. **Perform Review**
   - Read the codebase or the specified section.
   - **Search for "Implied ADR" notes** in `/tmp/implied-adr-*.md`.
   - Use the `review` skill to evaluate Architecture, Security, and Code Quality.
   - *(Required skill: `.codex/skills/review/SKILL.md`)*

2. **Generate Report**
   - Output the findings as a triagable checklist in `.codex/reports/ql-report-latest.md`.
   - Use `[ ]` syntax so the user can select items to fix or ADRs to formalize.
   - **STOP** and wait for human triage.

---

# /apply-fix

This command is used AFTER the human has triaged the `.codex/reports/ql-report-latest.md` file (by checking `[x]` on selected items).

## Agent Execution Steps

1. **Read Triage Selection**
   - Open `.codex/reports/ql-report-latest.md` and identify all items checked as `[x]`.

2. **Execute Fixes / Formalize ADRs**
   - For each checked item, plan the fix or create the formal ADR.
   - Run tests iteratively (if applicable) to ensure you broke nothing.
   - Update the report item from `[x]` to `[x] (Fixed/Formalized)` to indicate completion.

3. **Output Result**
   - Summarize the fixes and ADRs applied and **STOP**.
