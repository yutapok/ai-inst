# /ql-review command

This command initiates a Quality Loop (QL) review (Asynchronous).

It is a common follow-up command after `/btw-async` recommends `REVIEW`.

> **Task**: $ARGUMENTS

## Agent Execution Steps

1. **Activate Review Skill**
   - Read `.claude/skills/review/SKILL.md`.
2. **Perform Review**
   - Evaluate Architecture, Security, and Code Quality.
   - Search for "Implied ADR" notes in `.claude/reports/tmp/implied-adr/implied-adr-*.md`.
3. **Generate Report & Stop**
   - Output triagable checklist to `.claude/reports/ql-report-latest.md`.
   - The generated report may be consumed later in the same session or a different session.
   - **STOP** and wait for human triage.
