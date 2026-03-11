# /drift-check command

This command triggers an evaluation of recent code changes to ensure they comply with the Antigravity architecture boundaries.

> **Task**: $ARGUMENTS

When executing this command, Claude must adhere to the following sequence:

1. **Activate Architecture Skill**: Read the `architecture.md` skill to understand the boundary rules and drift classification criteria.
2. **Analyze Changes**: Review the recent modifications or the specified code area.
3. **Evaluate Vectors**: Check the changes across the 5 vectors (Dependency, Cyclic, Responsibility, Contract, Tech Choice).
4. **Determine Drift**: Classify the change (e.g., NO_CHANGE, MINOR_UPDATE, STRUCTURAL_ADJUST).
5. **Enforce Guardrails**:
   - If boundaries are violated, **HALT** any further implementation.
   - Propose an Architecture Decision Record (ADR) detailing the Context, Decision, and Consequences for the user's approval.
