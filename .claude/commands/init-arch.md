# /init-arch command

This command scans the project structure and initializes the architectural context.

> **Task**: $ARGUMENTS

## Agent Execution Steps

1. **Scan Project Structure**
   - Perform a depth-limited search of the filesystem.
   - Identify entry points and dependency management files.
2. **Discover Implicit Patterns**
   - Analyze layering and import directions.
3. **Initialize Governance Files**
   - Draft `rules.md` (guardrails) and `ADR-001 (Baseline)`.
4. **Output Discovery Report**
   - Store the report at `.claude/reports/arch-discovery-latest.md`.
   - **STOP** and wait for human confirmation.
