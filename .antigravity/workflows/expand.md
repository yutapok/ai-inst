---
description: [Phase 2] Expand the tracer bullet using Test-First principles, review, and fix.
---

# /expand (Phase 2: Flesh Out Implementation)

This workflow expands the "minimal working code (tracer bullet)" created in `/mission` into production-ready code by handling coverage, edge cases, and refactoring.
**This command must STOP and wait for Human Inspection as soon as the test-first expansion and self-review fixes are complete.**

## Agent Execution Steps

1. **Test-First Expansion Loop**
   - Extend the code by adding unit/component test cases across the test pyramid.
   - Detail the specifications in the following order: `Examples` → `Contracts` → `Invariants` (including Property-Based Tests).
   - **Autonomously run fast domain unit tests and in-process contract tests (Tier A) after every logical edit to maintain instant feedback and conserve tokens.**
   - *(Required skill: `.antigravity/skills/test-first/SKILL.md`)*

2. **Self-Review and Fix Iteration (Defect Prevention)**
   - Conduct a Defect Prevention Self-Review during implementation, focusing on:
     - **Observability**: Ensure structured logs have proper context (no swallowed errors) and OpenTelemetry spans are correctly placed:
       - **Go**: `log/slog` with contextual attributes.
       - **Python**: `structlog` or standard `logging` with structured dictionary context.
     - **Data**: Verify input validation (fail-fast) and data integrity (transaction boundaries, locks).
     - **Concurrency & Async**:
       - **Go**: Check for Goroutine data races (`go test -race`), deadlocks, and ensure channels/goroutines terminate cleanly.
       - **Python**: Check for event loop blocking, unhandled task exceptions, thread safety, and async context manager cleanup.
     - **CLI Drift & Linter**: Run the CLI contract linter to ensure no accidental breaking changes to flags, arguments, or schemas occurred.
   - If issues are found, fix them immediately in small increments.
   - (Note: If the user provided review comments when triggering the prompt, prioritize fixing those first.)

3. **Output Expansion Results and Stop**
   - Output the artifact using the `expand_result.md` format below (or compile the Interactive Walkthrough HTML `walkthrough.html`) and **STOP** working.

---

## Output Format (`expand_result.md`)

```markdown
# Expand Result
[Overview of the expanded features]

# Test Coverage & PBT Invariants Added
[List of newly covered test cases, edge cases, and PBT properties tested]

# Modified Components
[List of changed or added files/modules]

# Review & Fix (If any)
[Points fixed based on self-review, concurrency checks, or user feedback]

# Visual Cross-Check Artifact
[Path to generated interactive walkthrough HTML or Mermaid diagram mapping test scenarios]

# Next Steps for /drift-check
[Readiness state for architectural evaluation]
```
