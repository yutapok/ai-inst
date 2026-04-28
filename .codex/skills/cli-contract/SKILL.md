---
name: CLI Contract Definition & Enforcement
description: Procedure for defining and automating CLI inputs/outputs, exit codes, and error classifications via integration tests
---

# Defining and Enforcing the CLI Contract

This skill stands on its own. Use it whenever the task changes observable CLI behavior, even if no prompt or named workflow is involved.

Before finalizing the internal implementation (e.g., class structures or methods), you must strictly define the CLI Contract. This contract serves as the "observable boundary" from the outside and acts as your **automated regression guardrail**.

`CONTRACT_LOCK` is not a proof that the contract is correct. Its job is to prevent the agent from expanding an implementation behind a contract that may still misrepresent the user's real goal.

## 1. Define the Contract as an Integration Test
- Instead of merely documenting the contract, you must **implement it as an automated integration test**.
- Typically, these tests reside in an integration test directory (e.g., `tests/integration/...`).
- The test must execute the CLI command (e.g., passing input via `cat XXX | ...` or using execution libraries like `os/exec` in Go) and explicitly assert the following:
  - **Inputs**: What commands, flags, and stdin it accepts.
  - **Outputs**: The exact `stdout` format for a successful execution.
  - **Exit Codes**: `0` for success, non-zero for specific errors.
  - **Error Messages**: `stderr` format representing the expected errors.

## 1.5. Run Provocation Before Treating the Contract as Fixed
- For every contract lock, you must explicitly ask: **"What is the smallest case that would pass this contract but still miss the user's real goal?"**
- This provocation is mandatory whenever the task introduces or changes a public CLI or API contract.
- Classify the candidate counterexample into exactly one of these error classes:
  - **Success-condition error**: The contract marks a case as success even though it should fail or require re-evaluation.
  - **Boundary error**: The contract locks an internal implementation detail rather than a user-visible outcome.
  - **Omission error**: The contract leaves out a meaningful branch, failure mode, or constraint.
- If you cannot produce or classify a candidate counterexample, treat the contract as under-specified rather than proven.

## 1.6. Human-in-the-Loop Contract Review
- When the task creates or changes a public contract, present a short human-facing review block at major checkpoints.
- Use this exact structure:

```markdown
Contract Review:
- Success-condition error: [No concern / Needs review: ...]
- Boundary error: [No concern / Needs review: ...]
- Omission error: [No concern / Needs review: ...]
```

- Keep each line to a single short sentence.
- If any line is marked `Needs review`, do not autonomously treat the contract as fixed.
- If all three lines are `No concern`, you may continue to tracer or expansion work.

## 2. Integration Test Visibility (Scope of Quality Assurance)
- To make the scope of quality assurance transparent to both human reviewers and AI agents, the integration test **MUST output a list of packages or modules it encompasses and verifies** during execution.
- Extract the analyzed packages from the test target or output, and explicitly dump them as logs to `stdout` (e.g., `=== CLI Contract Encompassed Packages ===`).
- To consistently evaluate the entire target path instead of relying on local diffs, set your execution baseline properly (e.g., comparing against an empty tree hash) whenever your tool operates on source differences.

## 3. Autonomous Verification Loop (The Guardrail)
- This integration test is the ultimate source of truth for the system's external behavior.
- **You must autonomously and continuously run the integration tests** (e.g., `go test -v tests/integration/...` or the framework equivalent) during your development loop.
- If the integration test fails at any point after the initial Tracer Bullet phase, you have broken the contract. You must immediately revert or fix the internal changes until the test passes again.

## 3.5. Stop Conditions and Human Decision Conditions
- Do **not** proceed to `EXPAND` while any of the following remain unresolved:
  - A counterexample candidate still stands
  - The success criteria can be interpreted in more than one valid way
  - The contract mainly locks internal implementation details instead of a public outcome
  - Moving forward would spread a likely contract mistake across multiple files or modules
- Escalate to `HUMAN_DECISION` when any of the following are true:
  - There are multiple plausible contract interpretations and picking one is a product decision
  - The contract changes the meaning of a public CLI or API boundary
  - Resolving the contract requires changing responsibility boundaries or dependency direction
  - The remaining ambiguity is about what failure the product should tolerate, not about code mechanics

## 4. User Validation Loop (Understanding the Generated Change)
- CLI contract tests are not only regression guardrails for the agent. They also help the user validate and understand AI-generated code by running observable behavior locally.
- When you change CLI-facing behavior or generate code that the user should verify locally, include at least one short user-facing verification suggestion (for example: compile, targeted test, or command execution) in the final handoff or next-step recommendation.
- Prefer suggestions that let the user directly observe the locked contract, such as `make test`, a focused integration test command, or a concrete CLI invocation.
- Example: `Verify: Run \`make test\` to re-run the locked integration contract and confirm the CLI-facing behavior still passes end-to-end.`

## Why is this necessary?
By anchoring regression testing on automated, observable behavior (Test is specification), you create a safety net that allows you (the agent) to autonomously and aggressively refactor the internal architecture without human intervention. Explicitly logging encompassed packages builds further trust into the regression guardrails. The same observable checks also give the user a concrete way to verify and understand the generated behavior locally.
