---
name: Dead Code Cleanup
description: Find code that can be removed after implementation has settled, including unused code, duplicate logic, pointless indirection, and other safe-to-delete leftovers.
---

# Dead Code Cleanup

Use this skill after implementation has grown and you need to reduce the codebase without changing the intended behavior.

This skill is narrower than broad `review`. Its job is to identify code that can be deleted, merged, inlined, or simplified after the fact.

## When to Use It

Prefer this skill when one or more of the following are true:

- A feature or refactor left behind compatibility code, temporary helpers, or tracer-era scaffolding
- The same logic appears in multiple places
- A module, function, flag, or wrapper no longer appears to be used
- The code works, but some abstraction now adds noise instead of value
- The user explicitly asks what can be safely removed

## What to Look For

- Unused code: unreachable functions, dead branches, stale helpers, obsolete configs, unused exports
- Duplicate code: repeated transformations, mirrored validation, copy-pasted branching, overlapping helpers
- Pointless indirection: wrappers that no longer hide meaningful complexity, pass-through adapters, one-use abstractions
- Temporary leftovers: compatibility shims, migration glue, debug-only code, tracer hardcoding that has already been replaced
- Redundant structure: nested conditionals, duplicated conversions, needless state plumbing, extra files whose only job is forwarding

## Decision Rules

For each candidate, classify it as one of:

- `DELETE`: remove it completely
- `MERGE`: collapse duplicated logic into one place
- `INLINE`: remove the extra layer and keep the behavior inline
- `SIMPLIFY`: keep the behavior but rewrite it in a smaller form
- `KEEP`: do not change it yet

Also assign one safety level:

- `Safe`: removal is strongly supported by local evidence
- `Needs Verification`: likely removable, but requires contract, test, or build confirmation
- `Needs Human Decision`: intent or compatibility risk is still unclear

## Required Evidence

Before recommending removal, gather concrete evidence:

- Search for references and call sites
- Check whether the code participates in public CLI or API contracts
- Check whether tests rely on the code directly or indirectly
- Distinguish actual dead code from extension points, instrumentation hooks, or compatibility layers

Do not label something unused just because it is referenced infrequently.

## Hard Stops

Do not recommend autonomous deletion when:

- The code is part of a public contract and removal would change observable behavior
- The code may be a dormant feature flag or deliberate extension point with unclear ownership
- The code looks redundant but is required for security, observability, or operations
- The code crosses an architectural boundary in a way that may require `ARCHITECTURE`

In those cases, classify it as `KEEP` or `Needs Human Decision`.

## Output Format

Report findings first. If nothing is worth removing, say so explicitly.

For each finding, include:

- `Classification`: `DELETE`, `MERGE`, `INLINE`, `SIMPLIFY`, or `KEEP`
- `Safety`: `Safe`, `Needs Verification`, or `Needs Human Decision`
- `Why removable`: the concrete evidence
- `Suggested action`: the cleanup move
- `Verify`: the smallest check that confirms behavior still holds

Use this skill to reduce code volume, not to redesign the whole system.
