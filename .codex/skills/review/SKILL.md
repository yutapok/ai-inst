---
name: Code and Architecture Review
description: Comprehensive review for architecture, security, performance, and tech-debt.
---

# Review Procedures

This skill stands on its own. Use it for broad code review, architecture review, security review, or tech-debt triage, regardless of whether a prompt triggered the work.

This skill is used to perform a deep, heuristic review of the codebase. Unlike a rigid architecture drift check, this review surfaces potential improvements, architectural trade-offs, and security concerns.

## Timing Triggers

Prefer this skill when one or more of the following are true:

- The implementation now spans multiple files or modules
- A tracer bullet has already been expanded beyond the happy path
- Security, performance, or maintainability concerns are visible
- Temporary implied ADR notes exist and need triage
- The user asks for hardening, confidence, cleanup, or broad quality review

This skill may be inserted between implementation steps. It does not require a fixed phase order.

## Review Dimensions

When instructed to review the code, evaluate it against the following dimensions:

### 1. Architecture
- **Trade-off Analysis**: Are there better patterns (caching, async, event-driven) for the current requirements?
- **Coupling**: Are modules loosely coupled?
- **Distributed Processing**: Are there eventual consistency issues in distributed operations?
- **Implied ADR Formalization**: Review any temporary files in `.codex/reports/tmp/implied-adr/implied-adr-*.md`. Determine if these decisions should be promoted to a formal ADR, modified, or discarded.

### 2. Security
- **Vulnerabilities**: Are there known patterns of vulnerability (SQLi, XSS, etc.)?
- **Information Leakage**: Are sensitive data or tokens being logged or exposed?
- **Defender's Advantage**: Is the system robust enough to limit blast radius upon compromise?

### 3. Code (Maintainability & Optimization)
- **Performance**: Are there memory allocation hotspots or inefficient algorithms?
- **Readability**: Can the code be refactored for better clarity and maintainability?

## Output Format

The output must be an actionable Markdown checklist formatted as `.codex/reports/ql-report-latest.md`. Use `[ ]` for each finding so the human can easily triage and check `[x]` the ones they want to fix.

```markdown
# QL Report [Date]

## Architecture
- [ ] [Issue Title]: [Description of issue and proposed fix]

## Security
- [ ] [Issue Title]: [Description of issue and proposed fix]

## Code (Optimization & Maintainability)
- [ ] [Issue Title]: [Description of issue and proposed fix]
```
