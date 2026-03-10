---
name: Architecture Governance
description: Skill for evaluating drift classification and proposing Architecture Decision Records (ADRs).
---

# Architecture Governance for Claude Code

As an AI agent, you must evaluate whether your code changes fit within the existing architectural guardrails of the project, and safely evolve the architecture only when necessary.

## 1. Drift Verification
Before proposing a final code change, evaluate your implementation across these 5 vectors:
1. **Dependency Direction**: Did you break the `CLI → Domain → Adapters` unidirectional rule? (e.g., Domain layer directly referencing Adapters).
2. **Cyclic Dependencies**: Did you introduce mutual dependencies between modules?
3. **Boundary Responsibility**: Did a module absorb responsibilities that belong elsewhere?
4. **Public Contract**: Did you introduce breaking changes to the CLI Contract or public interfaces without a test failure?
5. **Technology Choice**: Did you deviate from the tech policies in existing ADRs?

## 2. Drift Classification
Classify your proposed change:
- **`NO_CHANGE`**: Implementation is completely within guardrails. Proceed.
- **`MINOR_UPDATE`**: Valid direction, but minor cleanup or inline documentation is needed. Proceed and clean up.
- **`STRUCTURAL_ADJUST`**: The change breaks a boundary, responsibility, or contract. You must **STOP** and propose an evolution.

## 3. Architecture Evolution (STOP CONDITION)
If the classification is `STRUCTURAL_ADJUST`:
1. **HALT** any file modifications for this feature.
2. Formulate an **Architecture Decision Record (ADR)** to propose to the user.
3. Use the following format for the proposed ADR in your response:
   - **Context**: The challenge and reasoning for the architecture change.
   - **Decision**: The specific new boundaries, dependency rules, or technology choices.
   - **Consequences**: The resulting benefits and trade-offs.
4. Wait for the user to explicitly approve before continuing.
