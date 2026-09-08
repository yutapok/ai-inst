---
name: Test-First Expansion
description: Procedure for test-first expansion across the test pyramid (Examples → Contracts → Invariants)
---

# Test-First Expansion Procedure

This skill stands on its own. Use it after a minimal path already works and the next step is to harden behavior with additional tests and structured refactoring.

This is the process of nurturing an already-working tracer bullet into robust, production-ready code.

To maintain high reasoning speed, conserve agent tokens, and enable human mental debugging, you must strictly detail specifications and assign them to the proper test pyramid layer in the following order:

---

## Start Gate

Before using this skill, verify that one of the following is true:

- A tracer bullet already proves the happy path end-to-end
- The change is a local, well-understood bug fix on an already-working path
- The work is primarily test expansion without changing the main execution shape
- If the task changes a public contract, the `Contract Review:` block has already been shown and every line is resolved or explicitly approved by the human

If none of these are true, do not proceed with broad test-first expansion yet. Return to investigation or tracer-bullet work first.

---

## 1. Test Pyramid & Responsibility Allocation

| Test Layer | Primary Target | Mechanism | Why / Characteristics |
|---|---|---|---|
| **Domain Unit Tests** | Core business logic, pure calculations, invariants, complex branching | In-memory function/method calls | **Blazing fast (< 0.1s)**, high density, exact localized stack traces, zero subprocess overhead. |
| **In-Process Contract Tests** | CLI/API adapters, flags, input validation, exit codes, output schemas | Callable CLI entrypoint (`app.Run(...)`) | Fast (< 0.5s), verifies public boundaries, self-documenting typed contracts. |
| **Tracer E2E Tests** | End-to-end viability, OS wiring, process startup | External process execution (`subprocess.run`) | **Minimal count (1–2 cases)**, run only at milestones. |

---

## 2. Expansion Sequence: Examples → Contracts → Invariants

### Step 1: Add Examples (Happy Path)
- Add concrete, representative test cases demonstrating intended usage.
- Start with in-process CLI contract tests and domain unit tests for the standard happy path.

### Step 2: Enforce Contracts (Abnormal Flows & Boundary Validation)
- Add contract test cases for edge cases, missing arguments, invalid flags, and external failure modes.
- Verify that typed validation errors, error exit codes, and structured error responses adhere strictly to the observable boundary specification.

### Step 3: Protect Invariants (Property-Based Testing & Domain Encapsulation)
- Write domain unit tests and Property-Based Tests (PBT) that protect invariants—conditions that must always remain true across the entire system regardless of external input (e.g., state machines cannot perform invalid transitions, balances cannot be negative, CLI never panics on arbitrary fuzz inputs).
- **Core CLI/Domain Invariants to Test with PBT**:
  1. **Crash-Freedom Invariant**: Arbitrary string slices or flags passed to the CLI never cause an unhandled panic (Go) or unhandled exception (Python); they must safely yield a controlled exit code (0, 1, or 2).
  2. **Schema Validity Invariant**: When `--json` is requested, the stdout/stderr payload is guaranteed to strictly conform to the declared JSON schema under all generated inputs.
  3. **Idempotence Invariant**: Running a mutation or synchronization command twice with identical parameters yields a consistent state and does not create duplicate side effects.
- **PBT Tooling**:
  - **Go**: `testing/quick` (standard library) or `pgregory.net/rapid`
  - **Python**: `hypothesis`
- Introduce defensive programming, encapsulation (private fields, read-only structures), and domain value objects to enforce invariants by construction.


---

## 3. Structure in Given / When / Then (GWT) Format for Mental Debugging

All test code must be structured so that a human reviewer or an AI agent can execute it mentally (desk debugging) without inspecting implementation details:

- **Given**: Setting up the typed inputs, domain entities, or state.
- **When**: Invoking the exact function or in-process CLI command.
- **Then**: Asserting against specific structured fields, exit codes, or state changes.

---

## 4. Autonomous Inner Loop Rules

- **Run Fast Tests Autonomously**: In your `TEST_FIRST` loop, run Domain Unit Tests and In-Process Contract Tests after every logical edit.
- **Diff-Friendly Assertions**: Use structured comparisons (e.g., dict equality, model equality) that yield concise diffs on failure, rather than substring checks on unstructured logs.
- **Avoid Spec Gaming**: If a test fails, fix the internal implementation. Never weaken or delete assertions simply to make tests pass.

At a meaningful checkpoint, hand off to the planner skill so the next action is explicit.
