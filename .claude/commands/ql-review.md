# /ql-review command

This command initiates a Quality Loop (QL) review (Asynchronous).

> **Task**: $ARGUMENTS

## Agent Execution Steps

1. **Activate Review Skill**
   - Read `.claude/skills/review/SKILL.md`.
2. **Perform Review**
   - Evaluate Architecture, Security, and Code Quality.
   - Search for "Implied ADR" notes in `/tmp/implied-adr-*.md`.
3. **Generate Report & Stop**
   - Output triagable checklist to `.claude/reports/ql-report-latest.md`.
   - **STOP** and wait for human triage.

---

# /apply-fix

Used after human triages the QL report.

1. **Read Triage**: Identify checked items in `.claude/reports/ql-report-latest.md`.
2. **Execute Fixes**: Apply fixes or formalize ADRs.
3. **Output Result**: Summarize work and **STOP**.
