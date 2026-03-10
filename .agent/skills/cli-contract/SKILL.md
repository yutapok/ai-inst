---
name: CLI Contract Definition & Enforcement
description: Procedure for defining and automating CLI inputs/outputs, exit codes, and error classifications via integration tests
---

# Defining and Enforcing the CLI Contract

Before finalizing the internal implementation (e.g., class structures or methods), you must strictly define the CLI Contract. This contract serves as the "observable boundary" from the outside and acts as your **automated regression guardrail**.

## 1. Define the Contract as an Integration Test
- Instead of merely documenting the contract, you must **implement it as an automated integration test**.
- Typically, these tests reside in an integration test directory (e.g., `tests/integration/...`).
- The test must execute the CLI command (e.g., passing input via `cat XXX | ...` or using execution libraries like `os/exec` in Go) and explicitly assert the following:
  - **Inputs**: What commands, flags, and stdin it accepts.
  - **Outputs**: The exact `stdout` format for a successful execution.
  - **Exit Codes**: `0` for success, non-zero for specific errors.
  - **Error Messages**: The expected `stderr` format.

## 2. Autonomous Verification Loop (The Guardrail)
- This integration test is the ultimate source of truth for the system's external behavior.
- **You must autonomously and continuously run the integration tests** (e.g., `go test tests/integration/...` or the framework equivalent) during your development loop.
- If the integration test fails at any point after the initial Tracer Bullet phase, you have broken the contract. You must immediately revert or fix the internal changes until the test passes again.

## Why is this necessary?
By anchoring regression testing on automated, observable behavior (Test is specification), you create a safety net that allows you (the agent) to autonomously and aggressively refactor the internal architecture without human intervention.
