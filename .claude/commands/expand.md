# /expand command

This command triggers the "Test-First Expansion" phase on a working Tracer Bullet (the minimal viable path).

When executing this command, Claude must adhere to the following sequence:

1. **Activate relevant Skills**: Ensure you have reviewed `cli-contract.md` and `test-first.md`.
2. **Identify the Tracer Bullet**: Analyze the recently created logic (which should currently be minimal and lacking robust edge-case handling).
3. **Define CLI Contract Integration Test**: First, write an integration test that asserts the external inputs, `stdout`, `stderr`, and exit codes.
4. **Expand Tests in Order**:
   - Write tests for Representative Examples (Happy Path)
   - Write tests enforcing Contracts (Abnormal flow, errors)
   - Write tests protecting Invariants (State rules)
5. **Implement Refactoring**: Refactor the initial Tracer Bullet code, introducing encapsulation and modules if needed, to pass the tests. Keep tests structured in Given/When/Then (GWT) format.
