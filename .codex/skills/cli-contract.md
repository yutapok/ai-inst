---
name: CLI Contract Definition & Enforcement
description: Skill for writing and automating CLI contracts as integration tests prior to implementation.
---

# CLI Contract Definition for Autonomous Agents

Before finalizing internal implementation (class structures, methods), you must define the standard CLI Contract. This serves as an automated regression guardrail.

## 1. Define the Contract as an Integration Test
- **Test-First**: Do not merely document the contract; write it as an automated integration test (e.g., in `tests/integration/`).
- **Assert External Behavior**: When generating the test, ensure it executes the CLI command natively and explicitly asserts:
  - **Inputs**: Accepted commands, flags, and `stdin`.
  - **Outputs**: The exact `stdout` format for success.
  - **Exit Codes**: `0` for success, non-zero for specific errors.
  - **Error Messages**: The expected `stderr` format.

## 2. Autonomous Verification Loop
- Continuously run these integration tests during your development loop using your terminal execution abilities.
- If the integration test fails after the initial Tracer Bullet phase, you have broken the contract.
- Revert or fix your internal changes until the test passes again before declaring the task complete.
