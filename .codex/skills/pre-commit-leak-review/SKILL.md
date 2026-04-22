---
name: Pre-Commit Leak Review
description: Review staged git changes for local-machine details, secrets, internal-only values, and other disclosure risks before commit or publish.
---

# Pre-Commit Leak Review

Use this skill when the user wants a commit-time safety review focused on information disclosure rather than functional correctness.

This skill stands on its own. Use it before commit, before push, before publishing a patch, or whenever the user asks whether a diff contains local-PC information or non-public data.

## Review Target Order

Inspect targets in this order:

1. `git diff --cached`
2. `git diff` only if the user explicitly asks for unstaged review too, or if nothing is staged and the user clearly means the whole working tree
3. Newly added files included by the diff, especially tests, fixtures, snapshots, generated files, and copied config files

If `git diff --cached` is empty, say that explicitly before widening scope.

## What To Look For

Prioritize disclosure risks that commonly slip into commits:

- Absolute local paths such as `/Users/...`, `C:\\Users\\...`, home-directory expansions, temp paths, editor state files, and machine-specific cache locations
- Personal identifiers such as usernames, personal email addresses, hostnames, Wi-Fi names, device names, or internal employee handles
- Credentials and secret material such as API keys, tokens, passwords, private keys, cookies, bearer headers, DSNs, or `.env` contents
- Internal-only infrastructure details such as private URLs, VPN-only hosts, localhost assumptions that reveal developer setup, bucket names, account IDs, database names, or undocumented service endpoints
- Proprietary or non-public business information such as customer data, incident details, screenshots, logs, internal ticket links, roadmap notes, or copied production values
- Test artifacts that accidentally embed real values in snapshots, fixtures, command output, or failure logs

## Investigation Method

Use both structured review and pattern search:

1. Read the staged diff directly.
2. Search the staged diff for high-signal leak patterns such as:
   - absolute paths
   - usernames and email addresses
   - `secret`, `token`, `password`, `passwd`, `apikey`, `api_key`, `Authorization`, `Bearer`
   - `BEGIN ... PRIVATE KEY`
   - private hostnames, `localhost`, `127.0.0.1`, internal domains, cloud account identifiers
3. Inspect any matching files in context to determine whether the value is a real disclosure, a placeholder, or an acceptable example.
4. For generated or copied files, check whether the sensitive value appears only once or is repeated across the artifact.

Do not rely on pattern matches alone. Confirm whether a hit is actually sensitive before reporting it.

## Reporting Rules

Default to a code-review style response with findings first.

- If you find issues, list them ordered by severity with file references and a short explanation of the leak risk.
- If no issues are found, state that explicitly and mention what scope was reviewed, for example staged diff only.
- Distinguish confirmed leaks from lower-confidence risks.
- Call out any residual blind spots, such as binary files, large generated artifacts, or unstaged changes not reviewed.

## Output Template

```markdown
[Findings or "No leak-risk findings in reviewed scope."]

Reviewed scope: [staged diff only | staged + unstaged]

Residual risks:
- [short note]
```
