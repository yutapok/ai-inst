---
description: [Phase 0] Scan project structure and initialize architectural context.
---

# /init-arch (Phase 0: Architectural Discovery)

This workflow scans the current project structure to discover implicit architectural patterns and initialize the governance framework (`rules.md` and a baseline ADR).

## Agent Execution Steps

1. **Scan Project Structure**
   - Perform a depth-limited search of the filesystem to understand the directory layout.
   - Identify key entry points (e.g., `main.go`, `index.js`, `cmd/`).
   - Identify dependency management files (e.g., `go.mod`, `package.json`, `Makefile`).

2. **Discover Implicit Patterns**
   - Look for standard layering (e.g., `internal/`, `pkg/`, `api/`, `domain/`).
   - Analyze import/dependency directions in a few sample files to confirm the pattern.

3. **Initialize Governance Files**
   - **`rules.md`**: Draft base architectural guardrails (Dependency Direction, No Cyclic Dependencies, etc.) tailored to the discovered structure.
   - **`ADR-001 (Baseline)`**: Formally record the current state as the starting architectural baseline.

4. **Output Discovery Report**
   - Present the identified structure and the drafted governance files to the human.
   - Output the discovery report to `.agent/reports/arch-discovery-latest.md`.
   - **STOP** and wait for human confirmation.

---

## Output Format (`.agent/reports/arch-discovery-latest.md`)

```markdown
# Architectural Discovery Report

## Discovered Structure
[Description of the identified directory layout and key components]

## Implicit Patterns
- Layering: [e.g., Clean Architecture, Flat, Modular Monolith]
- Entry Points: [List of main entry points]

## Drafted Governance
- [Link to drafted rules.md]
- [Link to drafted ADR-001]

# Conclusion
[A request for the human to review and approve the initial baseline]
```
