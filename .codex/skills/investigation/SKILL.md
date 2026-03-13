---
name: Investigation Methodology
description: Methodology for grasping the situation and organizing facts before modifications
---

# Investigation Methodology

Before modifying any code, you must strictly follow these steps to organize facts and prevent assumption-based changes. You must not hallucinate or guess the state of the codebase.

## 1. Gather Facts
- Extract only observable "facts" such as logs, error messages, and the current implementation code.
- Review related peripheral code and dependencies.

## 2. Separate Hypotheses
- Formulate hypotheses ("it might be working this way") based on the gathered facts.
- **Clearly distinguish between facts and hypotheses** when recording your findings.

## 3. Identify Unknowns
- List what is still unknown (uncertainties) that must be clarified before proceeding with implementation.
- Do not proceed with implementation blindly without doing this.

## 4. Maintenance Heuristics

Depending on the investigation mode, apply these specific techniques:

### Impact Analysis (Impact Scoping)
- **Dependency Crawl**: Identify all modules that depend on the component being changed.
- **Blast Radius Mapping**: List indirect side effects (e.g., shared DB state, secondary events).
- **Contract Impact**: Check if the change alters CLI inputs/outputs or public API signatures.

### Root Cause Analysis (Bug Investigation)
- **5 Whys**: Drill down into the technical cause until the systemic failure point is found.
- **Fact Correlation**: Correlate logs, error messages, and state transitions to build a timeline of the failure.
- **Reproduction Case**: Define the minimal steps or test cases required to reliably reproduce the issue.

### Security & Vulnerability Assessment
- **Untrusted Input Flow**: Trace data from external entry points (CLI, UI, API) to sensitive sinks (DB, shell, filesystem).
- **Sensitive Data Handling**: Search for hardcoded secrets, unencrypted logs, or insecure storage.

## 5. Decide Next Action (Scoping the Tracer)
- Decide the "next place to look" or "what to try next" in order to clarify the unknowns or prove a hypothesis.
- For bugs, this usually means creating a failing test.
- For impact analysis, it means drafting a minimal verification plan.
