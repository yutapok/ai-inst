---
name: Investigation Methodology
description: Methodology for grasping the situation and organizing facts before modifications
---

# Investigation Methodology

Before modifying any code, you must strictly follow these steps to organize facts and prevent assumption-based changes.

## 1. Gather Facts
- Extract only observable "facts" such as logs, error messages, and the current implementation code.
- Review related peripheral code and dependencies.

## 2. Separate Hypotheses
- Formulate hypotheses ("it might be working this way") based on the gathered facts.
- **Clearly distinguish between facts and hypotheses** when recording your findings.

## 3. Identify Unknowns
- List what is still unknown (uncertainties) that must be clarified before proceeding with implementation.
- Do not proceed with implementation blindly without doing this.

## 4. Decide Next Action
- Decide the "next place to look" or "what to try next" in order to clarify the unknowns or prove a hypothesis.
- This will form the concrete scope of the Tracer Bullet you create next.
