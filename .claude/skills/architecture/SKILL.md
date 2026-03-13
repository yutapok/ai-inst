---
name: Architecture Governance
description: Criteria for drift classification, ADR creation, and architecture evolution
---

# Architecture Governance Procedures

As an AI agent, you must evaluate whether your code changes fit within the existing architectural guardrails of the project, and safely evolve the architecture only when necessary.

## 1. Drift Verification
Evaluate the implementation across these 5 vectors to ensure no deviation has occurred.

1. **Dependency Direction Violation**: Did the Domain layer directly reference the Adapters layer, breaking the `CLI → Domain → Adapters` unidirectional rule?
2. **Cyclic Dependencies**: Have mutual dependencies or interwoven responsibilities been created between modules?
3. **Boundary Responsibility Leak**: Has a module absorbed responsibilities that properly belong to a different boundary?
4. **Public Contract Break**: Have breaking changes been introduced to the CLI Contract or public interfaces?
5. **Technology Choice Deviation**: Has there been an unauthorized deviation from the technical policies decided in existing ADRs?

## 2. Drift Classification
All changes must be classified into one of the following:

- **`NO_CHANGE`**
  The implementation is completely contained within existing guardrails. No architectural documentation or structural changes are required.
- **`MINOR_UPDATE`**
  The direction is valid, but documentation or minor code cleanup is lacking. This includes clarifying responsibility comments, light dependency fixes, or addressing non-structural discrepancies.
- **`STRUCTURAL_ADJUST`**
  A change has occurred that cannot be explained by the current guardrails. It requires a boundary, responsibility, technology choice, or contract update to remain consistent.

## 3. Architecture Evolution
If the classification is `STRUCTURAL_ADJUST`, the agent must **STOP** autonomous modification and propose an architecture evolution to the human. When doing so, you must always create or update an **ADR (Architecture Decision Record)** to leave a formal record of the reasoning behind the change.

Triggers that permit evolution include:
- Performance pressure
- Repeated boundary violations
- Unexplainable complexity / New requirements that break existing boundaries
- Unavoidable technology decision changes

## 4. Implied ADRs (Temporary Records)
During phases of high uncertainty (e.g., Tracer Bullet development), architectural decisions may be made rapidly. To ensure these decisions are not lost:
- **Record**: Create a temporary note in `.claude/reports/tmp/implied-adr/implied-adr-[Topic]-[Date].md` (keep volatile).
- **Content**: Briefly record the context, the chosen path, and any immediate trade-offs observed.
- **Transition**: These notes are *not* formal architecture. They must be reviewed and either formalized into an ADR or discarded during the `/ql-review` phase once the implementation is validated.

## 5. ADR Creation Rules (Formal Records)
An ADR must be structured as follows:
- **Context**: The current challenge and the reasoning behind why the architecture needs to change.
- **Decision**: The specific new boundaries, dependency rules, or technology choices.
- **Consequences**: The resulting benefits, as well as the trade-offs (limitations) introduced.
