# /ql-review command

This command initiates a Quality Loop (QL) review (Asynchronous).

> **Task**: $ARGUMENTS

## Agent Execution Steps

1. **Activate Review Skill**
   - Read `.claude/skills/review/SKILL.md`.
2. **Perform Review**
   - Evaluate Architecture, Security, and Code Quality.
   - Search for "Implied ADR" notes in `.claude/reports/tmp/implied-adr/implied-adr-*.md`.
3. **Generate Report & Stop**
   - Output triagable checklist to `.claude/reports/ql-report-latest.md`.
   - **STOP** and wait for human triage.

