---
name: Tracer Bullet Methodology
description: Skill for building and verifying the minimal end-to-end path before abstraction.
---

# Tracer Bullet Methodology for Claude Code

When approaching a new feature or refactor, you must build the "smallest technically viable path" before attempting to draft a "perfect architecture." 

## Do:
- **Pass the Minimal End-to-End**: Write a contiguous execution flow that pierces through the system (from CLI input to the lowest layer).
- **Run Locally**: Formulate a terminal command to execute the code and confirm it produces the intended result (Proof of Viability). Read the output.
- **Allow Hardcoding of Data Logic**: Defer complex conditionals and generalizations. Prioritize the Happy Path. ⚠️ **Never hardcode credentials, API keys, tokens, or environment-specific values** — always use environment variables or config files for those.

## Don't:
- **Do Not Prematurely Abstract**: Avoid over-designing class hierarchies, extracting interfaces, or complex directory structures until *after* the tracer bullet succeeds.
- **Do Not Exhaustively Handle Edge Cases**: Full coverage of validation and abnormal behavior handling should be deferred to the Test-First Expansion phase.
