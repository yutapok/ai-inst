# /mission command

This command triggers the initial "Tracer Bullet" planning and implementation phase for a new feature or scope of work.

> **Task**: $ARGUMENTS

When executing this command, Claude must adhere to the following sequence:

1. **Activate Investigation Skill**: Read the `investigation.md` skill to understand the methodology.
2. **Read Current State**: Gather facts about the codebase related to the user's request. Identify the unknowns.
3. **Activate Tracer Bullet Skill**: Read the `tracer-bullet.md` skill.
4. **Determine Scope**: Define the minimal technically viable path ("Tracer Bullet") needed to prove the concept.
5. **Implement**: Write the code. Do not prematurely abstract or over-engineer. Hardcoding of *data logic* is permitted in this phase; **hardcoding secrets, API keys, credentials, or environment-specific values is never permitted**.
6. **Verify & Next Action**: Run the code locally to prove viability, report the facts, and explain the next steps for the `/expand` phase.
