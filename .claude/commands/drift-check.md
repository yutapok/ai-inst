# /drift-check command

This command performs an architecture drift check against guardrails.

It is a common follow-up command after `/btw-async` recommends `DRIFT_CHECK`.

> **Task**: $ARGUMENTS

## Agent Execution Steps

1. **Activate Architecture Skill**
   - Read `.claude/skills/architecture/SKILL.md`.
2. **Verify Guardrails**
   - Check Dependency Direction, Cycles, Boundaries, Contracts, and Tech Choices.
3. **Classify Drift**
   - NO_CHANGE | MINOR_UPDATE | STRUCTURAL_ADJUST.
4. **Output Report & Stop**
   - If STRUCTURAL_ADJUST, draft an ADR.
   - Output report to `.claude/reports/drift-report-latest.md`. The generated report may be consumed later in the same session or a different session.
   - **STOP**.
