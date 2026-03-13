# /investigate command

This command is for maintenance, incident response, research, and QA.

> **Task**: $ARGUMENTS

## Agent Execution Steps

1. **Select Mode**
   - BUG_FIX | IMPACT | SECURITY | RESEARCH.
2. **Activate Investigation Skill**
   - Read `.claude/skills/investigation/SKILL.md`.
   - Apply specific heuristics based on mode.
3. **Generate Report & Stop**
   - Output report to `.claude/reports/investigate-latest.md`.
   - **STOP** and wait for human direction.
