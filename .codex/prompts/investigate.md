---
description: [Ad-hoc] Investigate code state and fact-gathering without making modifications.
---

# /investigate

This workflow is used for maintenance, incident response, research, and general QA. Its purpose is to gather facts, map execution paths, and identify root causes without making code changes.

## 1. Select Investigation Mode
Depending on the user's request, identify the primary mode:
- **`BUG_FIX`**: Investigate a bug report or error.
- **`IMPACT`**: Analyze the effect of a change or refactor.
- **`SECURITY`**: Search for vulnerabilities or sensitive data leaks.
- **`RESEARCH`**: Answer technical questions or architectural "how-to"s.

## 2. Agent Execution Steps

1. **Fact Gathering & Analysis**
   - Read relevant code, logs, and config files.
   - Apply specific heuristics from the investigation skill (Impact scoping, 5 Whys, Trace data flow).
   - *(Required skill: `.codex/skills/investigation/SKILL.md`)*

2. **Generate Structured Report**
   - Output an `.codex/reports/investigate-latest.md` using the format below.
   - **STOP** and wait for human direction.

---

## Output Format (`.codex/reports/investigate-latest.md`)

```markdown
# Investigation Report: [Title]
**Mode**: [BUG_FIX | IMPACT | SECURITY | RESEARCH]

## 1. Facts & Observations
- [List of observable evidence gathered]

## 2. Hypothesis & Analysis
- [Interpretation of facts, root cause for bugs, or blast radius for impact]

## 3. Unknowns & Risks
- [Remaining uncertainties or potential trade-offs]

## 4. Proposed Next Steps
- [Concrete actions or Tracer Bullet scope for resolution]
```
