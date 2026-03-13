---
description: [Phase 1] Investigate state, fix contracts, and create a tracer bullet (minimum e2e) to prove viability.
---

# /mission (Phase 1: Prove Viability)

This workflow is used to determine the direction of a new task and create the smallest technically viable code (tracer bullet).
**This command must STOP and wait for Human Inspection as soon as the tracer bullet behavior is verified.**

## Non-Functional Requirements (NFRs) Baseline

All implementations in this phase must adhere to the following standards:
- **Logging**: Use the standard `log/slog` package for structured logging. Avoid `fmt.Println` for application logs.
- **Tracing**: Define observation points and traces using OpenTelemetry (e.g., proper span creation).

## Agent Execution Steps

1. **Investigation**
   - Investigate the current state of the relevant code and repository.
   - Organize known facts and identify uncertainties.
   - *(Required skill: `.codex/skills/investigation/SKILL.md`)*

2. **Fix the CLI Contract (Observable Specs)**
   - Define the target CLI inputs, expected outputs, exit codes, and error classifications.
   - **Crucially, implement this contract as an automated integration test (e.g., in `tests/integration/...`).**
   - *(Required skill: `.codex/skills/cli-contract/SKILL.md`)*

3. **Implement and Verify the Tracer Bullet**
   - Write the "minimal working code" that connects from the CLI down to the bottom layer without premature abstraction or splitting.
   - Run the integration tests (e.g., `go test tests/integration/...`) locally to ensure the code behaves exactly according to the CLI contract.
   - *(Required skill: `.codex/skills/tracer-bullet/SKILL.md`)*

4. **Output Plan and Stop**
   - Output the artifact using the `mission.md` format below and **STOP** working.

---

## Output Format (`mission.md`)

```markdown
# Mission
[Brief objective of the task]

# Context / Current State
[Current specifications and facts discovered during investigation]

# CLI Contract
[The fixed CLI inputs, outputs, exit codes, and error classifications]

# Tracer Bullet Result
[Location of the minimal implementation and the proof of success when executed (e.g., terminal output)]

# Next Steps for /expand
[Guidelines for extending coverage, edge cases, and refactoring using TDD in the next phase]
```
