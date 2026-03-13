---
name: Test-First Expansion
description: Procedure for test-first expansion (Examples → Contracts → Invariants)
---

# Test-First Expansion Procedure

This is the process of nurturing the "Tracer Bullet" created during the `/mission` phase into robust, production-ready code. You must strictly detail the specifications in the following order:

## 1. Add Examples
- First, add test cases demonstrating representative concrete examples of the happy path.
- This ensures the code continuously meets the basic functional requirements.

## 2. Enforce Contracts
- Next, add test cases for abnormal flows (e.g., validation errors, accessing non-existent resources).
- Verify that the "error exit codes" and "error output formats" defined in the CLI Contract are strictly adhered to.

## 3. Protect Invariants
- Finally, write tests that protect invariants—conditions that must always remain true across the entire system (e.g., money balances cannot be negative, state transition sequences must be followed).
- This is the stage where you fully introduce encapsulation (private/readonly) and module splitting as defensive programming measures.

## 4. Organize in Given/When/Then (GWT) Format
- All test code must be structured so that the specifications are immediately obvious upon reading the code:
  - **Given**: Setting up the initial state for the test.
  - **When**: Executing the target functionality.
  - **Then**: Verifying the expected outcome (state, output, side effects).

## Caution
Avoid "haphazard refactoring" aimed solely at passing the tests. Always be conscious of enhancing "maintainability," and perform structured refactoring loops (review-fix) as needed.
