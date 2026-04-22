---
description: [Quality Loop] Apply fixes and formalize ADRs after QL review triage.
---

# /apply-fix

Compatibility note: this prompt is a legacy shortcut. The canonical workflow lives in `.codex/AGENTS.md` and the relevant files under `.codex/skills/`.

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
