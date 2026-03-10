---
name: Test-First Expansion
description: Skill for nurturing a Tracer Bullet into robust code using GWT tests.
---

# Test-First Expansion Procedure for Autonomous Agents

Once you have verified that a "Tracer Bullet" (minimal end-to-end path) works, you must nurture it into production-ready code. Do this by strictly detailing specifications as tests in the following order:

## 1. Add Examples (Happy Path)
- Add test cases demonstrating representative concrete examples of the successful end-to-end execution.

## 2. Enforce Contracts (Abnormal Flow)
- Add test cases for abnormal flows (validation errors, missing resources).
- Critically: Verify that the exact "error exit codes" and "error output formatting" defined in the CLI integration test are adhered to.

## 3. Protect Invariants
- Write tests that protect system-wide invariants (e.g., state transitions, negative balances).
- Introduce encapsulation (private/readonly variables) and split modules as a defensive measure during this phase.

## 4. Use Given/When/Then (GWT)
Structure all test code clearly:
- **Given**: Setting up the initial state.
- **When**: Executing the functionality.
- **Then**: Verifying the expected outcome (state, output, side effects).
