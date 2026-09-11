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

2. **Adversarial Self-Review and YAGNI Cleanup Iteration**
   - Conduct an **Adversarial Self-Review (Devil's Advocate Protocol)** after completing test expansion:
     - **Inviolable Rules**: No self-congratulations ("LGTM" prohibited), enforce **Negative Quota** (identify >= 2 YAGNI / over-engineering / fragility points).
     - **Hard Boundary, Lean Core**: Confirm public CLI contracts (Tier A: `app.Run`) are locked, and prune single-use interfaces, premature DI, or fragile internal mock tests.
     - **Concurrency & Async**:
       - **Go**: Check for Goroutine data races (`go test -race`), deadlocks, and ensure channels terminate cleanly.
       - **Python**: Check for event loop blocking, unhandled task exceptions, thread safety, and async cleanup.
     - **CLI Drift & Linter**: Run the CLI contract linter to guarantee backwards compatibility.
   - Output minimal **Kill / Keep / Fix Checklist** (under 10 lines) and immediately invoke `.antigravity/skills/dead-code-cleanup/SKILL.md` to prune dead code.
   - *(Required skills: `.antigravity/skills/review/SKILL.md`, `.antigravity/skills/dead-code-cleanup/SKILL.md`)*

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
