---
name: Tracer Bullet Methodology
description: Design, implementation, and verification techniques for a tracer bullet (minimal e2e path)
---

# What is a Tracer Bullet?

A tracer bullet is a technique to build the "smallest technically viable path" before attempting to draft a "perfect architecture." It rapidly uncovers unknown design complexities, integration gaps, and UX inadequacies early in the process.

## Rules: Do
- **Pass the Minimal End-to-End**: Write a contiguous execution flow that pierces through the system—from the CLI input down to the bottom layer (e.g., database access or external API calls) if necessary.
- **Run Locally**: Actually execute the code and confirm that it produces the intended results (Proof of Viability).
- **Allow Hardcoding**: Defer complex branching and generalizations. Prioritize getting the "Happy Path" to work first.

## Rules: Don't
- **Do Not Prematurely Abstract or Split**: Avoid over-designing class hierarchies, extracting interfaces, or rigidly organizing directories until *after* the tracer bullet proves successful.
- **Do Not Exhaustively Handle Edge Cases**: Full coverage of validation and abnormal behavior handling should be deferred to the subsequent `/expand` (Test-First Expansion) phase.

## Why are Tracer Bullets Necessary?
They prevent "Speculative Architecture" driven by guesswork, and they provide momentum by quickly delivering a working piece of software locally.
