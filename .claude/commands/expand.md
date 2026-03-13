# /expand command

This command expands the tracer bullet using Test-First principles.

> **Task**: $ARGUMENTS

## Agent Execution Steps

1. **Activate Test-First Skill**
   - Read `.claude/skills/test-first/SKILL.md`.
   - Loop through: Examples → Contracts → Invariants.
   - Run integration tests after every significant change.
2. **Self-Review & Fix**
   - Conduct a Defect Prevention review (Observability, Data, Concurrency).
3. **Output Result & Stop**
   - Output `expand_result.md` and **STOP**.
