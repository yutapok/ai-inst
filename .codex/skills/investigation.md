---
name: Investigation Methodology
description: Skill for gathering facts and formulating hypotheses before making changes.
---

# Investigation Methodology for Autonomous Agents

As an autonomous agent, you must not hallucinate or guess the state of the codebase. Strictly follow these steps before modifying code:

## 1. Gather Facts
- Use your file system tools (e.g., grep, view file) or run local commands to extract observable facts (error messages, logs, current implementation).
- Read related peripheral code and dependencies.

## 2. Separate Hypotheses
- Formulate hypotheses based solely on the gathered facts ("it might be working this way because...").
- Keep facts and your hypotheses clearly separated in your reasoning.

## 3. Identify Unknowns
- List what is still uncertain and must be clarified before proceeding.

## 4. Decide Next Action (Tracer Bullet Scope)
- Decide the "next place to look" or "what to try next" to clarify the unknowns.
- Define the concrete scope of a Tracer Bullet (minimal viable path) before proceeding with file mutations.
