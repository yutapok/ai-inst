# /mission command

This command triggers "Tracer Bullet" planning and implementation to prove viability.

> **Task**: $ARGUMENTS

## Agent Execution Steps

1. **Activate Investigation Skill**
   - Read `.claude/skills/investigation/SKILL.md`.
   - Investigate state and organize unknowns.
2. **Fix CLI Contract**
   - Read `.claude/skills/cli-contract/SKILL.md`.
   - Define inputs/outputs and implement as an integration test.
3. **Implement Tracer Bullet**
   - Read `.claude/skills/tracer-bullet/SKILL.md`.
   - Write minimal working code.
4. **Verify & Stop**
   - Run integration tests locally.
   - Output `mission.md` report and **STOP**.
