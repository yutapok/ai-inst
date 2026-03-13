---
description: [Phase 2] Expand the tracer bullet using Test-First principles, review, and fix.
---

# /expand (Phase 2: Flesh Out Implementation)

This workflow expands the "minimal working code (tracer bullet)" created in `/mission` into production-ready code by handling coverage, edge cases, and refactoring.
**This command must STOP and wait for Human Inspection as soon as the test-first expansion and self-review fixes are complete.**

## Agent Execution Steps

1. **Test-First Expansion Loop**
   - Extend the code by adding unit/component test cases to the existing tracer bullet.
   - Detail the specifications in the following order: `Examples` → `Contracts` → `Invariants`.
   - **Autonomously run the integration tests (e.g., `go test tests/integration/...`) after every significant change to ensure the CLI Contract guardrail remains intact.**
   - *(Required skill: `.agent/skills/test-first/SKILL.md`)*

2. **Self-Review and Fix Iteration (Defect Prevention)**
   - Conduct a Defect Prevention Self-Review during implementation, focusing on:
     - **Observability**: Ensure `log/slog` logs have proper context (no swallowed errors) and OpenTelemetry spans are correctly placed.
     - **Data**: Verify input validation (fail-fast) and data integrity (transaction boundaries, locks).
     - **Concurrency**: Check for Goroutine data races, deadlocks, and ensure channels are appropriately closed.
   - If issues are found, fix them immediately in small increments.
   - (Note: If the user provided review comments when triggering the prompt, prioritize fixing those first.)

3. **Output Expansion Results and Stop**
   - Output the artifact using the `expand_result.md` format below and **STOP** working.

---

## Output Format (`expand_result.md`)

```markdown
# Expand Result
[Overview of the expanded features]

# Test Coverage Added
[List of newly covered test cases and edge cases]

# Modified Components
[List of changed or added files/modules]

# Review & Fix (If any)
[Points fixed based on self-review or user feedback]

# Next Steps for /drift-check
[Readiness state for architectural evaluation]
```
