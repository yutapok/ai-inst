# /drift-check command

This command performs an architecture drift check against guardrails.

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
   - Output report to `.claude/reports/drift-report-latest.md` and **STOP**.
