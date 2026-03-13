---
name: Code and Architecture Review
description: Comprehensive review for architecture, security, performance, and tech-debt.
---

# Review Procedures

This skill is used to perform a deep, heuristic review of the codebase. Unlike `drift-check` which is rigid and deterministic, this review surfaces potential improvements, architectural trade-offs, and security concerns.

## Review Dimensions

When instructed to review the code, evaluate it against the following dimensions:

### 1. Architecture
- **Trade-off Analysis**: Are there better patterns (caching, async, event-driven) for the current requirements?
- **Coupling**: Are modules loosely coupled?
- **Distributed Processing**: Are there eventual consistency issues in distributed operations?
- **Implied ADR Formalization**: Review any temporary files in `/tmp/implied-adr-*.md`. Determine if these decisions should be promoted to a formal ADR, modified, or discarded.

### 2. Security
- **Vulnerabilities**: Are there known patterns of vulnerability (SQLi, XSS, etc.)?
- **Information Leakage**: Are sensitive data or tokens being logged or exposed?
- **Defender's Advantage**: Is the system robust enough to limit blast radius upon compromise?

### 3. Code (Maintainability & Optimization)
- **Performance**: Are there memory allocation hotspots or inefficient algorithms?
- **Readability**: Can the code be refactored for better clarity and maintainability?

## Output Format

The output must be an actionable Markdown checklist formatted as `.agent/reports/ql-report-latest.md`. Use `[ ]` for each finding so the human can easily triage and check `[x]` the ones they want to fix.

```markdown
# QL Report [Date]

## Architecture
- [ ] [Issue Title]: [Description of issue and proposed fix]

## Security
- [ ] [Issue Title]: [Description of issue and proposed fix]

## Code (Optimization & Maintainability)
- [ ] [Issue Title]: [Description of issue and proposed fix]
```
