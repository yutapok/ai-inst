---
description: [Phase 3] Perform an architecture drift check against formal ADRs or discovered baselines.
---

# /drift-check (Phase 3: Architectural Governance)

Compatibility note: this prompt is a legacy shortcut. The canonical workflow lives in `.codex/AGENTS.md` and `.codex/skills/architecture/SKILL.md`.

This workflow verifies whether the current changes adhere to the existing architectural guardrails, and triggers necessary documentation updates or structural evolution.
**This command must STOP and wait for Human Inspection as soon as the drift classification (and an ADR draft if applicable) is output.**

Use this when drift triggers appear, even if the work did not proceed through a perfectly linear sequence.

## Agent Execution Steps

1. **Check Architectural Violation Vectors**
   - Review all altered code to ensure no deviations occurred across these 5 vectors:
     - Dependency Direction Violation (CLI → Domain → Adapters)
     - Cyclic Dependencies
     - Boundary Responsibility Leak
     - Public Contract Break
     - Technology Choice Deviation
   - **If no formal ADRs exist, use the baseline rules set by `/init-arch` or identified via discovery.**
   - *(Required skill: `.codex/skills/architecture/SKILL.md`)*

2. **Drift Classification**
   - Classify the changes into one of the following based on the review results:
     - `NO_CHANGE` (Within acceptable limits)
     - `MINOR_UPDATE` (Requires minor fixes or documentation)
     - `STRUCTURAL_ADJUST` (Major structural deviation)

3. **ADR Creation for STRUCTURAL_ADJUST**
   - If classified as `STRUCTURAL_ADJUST`, automatically draft an Architecture Decision Record (ADR) and propose an architectural evolution (arch-evolve).

4. **Output Report and Stop**
   - Output the artifact to `.codex/reports/drift-report-latest.md` using the format below and **STOP** working.
   - Include a short planner-style next action recommendation for the user unless the result is `STRUCTURAL_ADJUST`, in which case request human decision directly.

---

## Output Format (`.codex/reports/drift-report-latest.md`)

```markdown
# Drift Classification
[Result: NO_CHANGE | MINOR_UPDATE | STRUCTURAL_ADJUST]

# Architecture Review
[Evaluation of the changes across the 5 architectural vectors]
- Dependency Direction: [OK/NG]
- Cyclic Dependencies: [OK/NG]
- Boundary Responsibilities: [OK/NG]
- Public Contracts: [OK/NG]
- Technology Choices: [OK/NG]

# Required Actions
[Actions needed based on classification: fixes for MINOR_UPDATE, or a link to the drafted ADR for STRUCTURAL_ADJUST]

# Conclusion
[A statement requesting approval from the human reviewer]
```
