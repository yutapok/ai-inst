---
name: Tracer Bullet Methodology
description: Design, implementation, and verification techniques for a tracer bullet (minimal e2e path)
---

# What is a Tracer Bullet?

This skill stands on its own. Use it when the task is still uncertain and you need the smallest viable end-to-end path before investing in abstractions.

A tracer bullet is a technique to build the "smallest technically viable path" before attempting to draft a "perfect architecture." It rapidly uncovers unknown design complexities, integration gaps, and UX inadequacies early in the process.

## When to Use It First

Prefer this skill before test-first expansion when the task introduces a new path, a new integration, a new contract, or meaningful uncertainty about the implementation shape.

## Rules: Do
- **Pass the Minimal End-to-End**: Write a contiguous execution flow that pierces through the system—from the CLI input down to the bottom layer (e.g., database access or external API calls) if necessary.
- **Run Locally**: Actually execute the code and confirm that it produces the intended results (Proof of Viability).
- **Allow Hardcoding of Data Logic**: Defer complex branching and generalizations. Prioritize getting the "Happy Path" to work first. ⚠️ **Never hardcode credentials, API keys, tokens, or environment-specific values** — always use environment variables or config files for those.

## Rules: Don't
- **Do Not Prematurely Abstract or Split**: Avoid over-designing class hierarchies, extracting interfaces, or rigidly organizing directories until *after* the tracer bullet proves successful.
- **Do Not Exhaustively Handle Edge Cases**: Full coverage of validation and abnormal behavior handling should be deferred to the later test-first expansion phase.

## Done Criteria

Treat the tracer bullet as complete when all of the following are true:

- A single happy path works end-to-end
- The key observable behavior is verified locally
- The implementation proves viability without requiring full generalization
- If the task changes a public contract, the required `Contract Review:` block has been shown and no review line remains unresolved

The tracer bullet is not responsible for:

- Full validation coverage
- Invariant protection across the whole system
- Broad refactoring for maintainability
- Exhaustive error handling

If the tracer bullet works but the public contract still has unresolved provocation concerns, return to `CONTRACT_LOCK` instead of proceeding to `EXPAND`.

After the tracer bullet is proven, use the planner skill to suggest the next best action.

## Why are Tracer Bullets Necessary?
They prevent "Speculative Architecture" driven by guesswork, and they provide momentum by quickly delivering a working piece of software locally.
