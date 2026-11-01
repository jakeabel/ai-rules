# Security and data changes

## Authentication and authorization

Use the project's existing identity and permission mechanisms. Authentication establishes identity. Authorization must separately check the action and the resource. Preserve tenant or customer boundaries on reads, lists, writes, background jobs, exports, and administrative paths.

Do not assume that an absent tenant means unrestricted access, that a service token is an administrator, or that a valid token permits every operation. Existing bypasses must be understood and tested before changes near them. Do not broaden them as a workaround.

For a protected operation, check unauthenticated requests, insufficient permissions, the wrong tenant, and authorized success. Preserve issuer, audience, signature, expiry, and CSRF checks where they apply. Do not copy a stateless API security configuration into a browser login flow without examining session and cookie behavior.

Follow the project's documented authorization policy while checking the actual enforcement code. Do not assume the intended policy is already implemented everywhere. The project overlay records the mismatches.

## Secrets and sensitive data

Never commit real credentials, private keys, tokens, secret properties, or database dumps. Use example files with obvious placeholders and the existing secret delivery mechanism. Inspect only the secret configuration necessary for the task. Do not print values to discover whether they are set.

Redact logs and shared command output. Do not put secrets in URLs, source examples, screenshots, exception messages, or completion reports. Treat user data as sensitive even when it is present in a development database.

If a secret is accidentally exposed, stop spreading it and report the location without repeating the value. Do not rotate or delete a shared credential without authorization and a concrete recovery plan.

Use the project's gitignored local-only directory for files that must not be committed. Do not invent a second "will not be committed" directory.

### Scanning before commit

`gitleaks` is the scanner for these projects. Install it once (`brew install gitleaks` on macOS) and wire it as a pre-commit hook where the repository uses one. On every commit, the hook must run `gitleaks protect --staged` and refuse the commit on a finding.

If a finding is reported:

1. Do not use `--no-verify` to bypass the hook.
2. Remove the value from the staged diff. If it was already committed, treat the credential as compromised: tell Jake and begin rotation under his guidance.
3. If the finding is a false positive on a value that is not a real secret (an example in docs, a well-known public identifier), add a narrow `.gitleaksignore` entry or an inline comment per the gitleaks docs, not a global ignore.

## Schema ownership and evolution

Locate the active migration runner and its configured file locations before adding SQL. Use the owning service's migration directory. Historical SQL and schema snapshots are references, not migration inputs.

For an already applied versioned migration, add a new migration rather than editing history. Check the next available version on the branch you intend to push. Do not enable Flyway repair, clean, automatic baselining, or schema recreation to hide drift.

### Picking the next version number

Before adding `V<N>__…`:

1. Pull latest on the branch you intend to push.
2. Look at the service's migration directory for the current highest version.
3. Pick `N+1`, commit, and push together. Do not sit on an unpushed migration while other work lands above you.

If a collision is noticed before push, rename the file to the next unused number. If two unmerged branches both picked the same version, the branch that merges later renames its migration and records the move in the commit message. Do not edit the migration that already landed.

Prefer additive, compatible steps. For a rename, type conversion, or removal, consider old and new application versions running at the same time, plus backfill, validation, and recovery. A `DROP` or a rollback file is not a recovery plan for lost data. Never apply a migration to a shared database merely to validate its syntax.

Use database constraints for integrity, explicit transaction boundaries, and parameterized queries. Preserve the project's identifier and timestamp conventions. Do not globally convert existing data types as incidental cleanup.

## Domain-sensitive work

Payment and billing changes need explicit money units, currency and rounding rules, idempotency, provider sandbox isolation, and duplicate-event handling. Notification and webhook tests must avoid real recipients. File and URL handlers need appropriate size limits, path and ownership validation, and outbound destination controls.

These are review concerns for the affected work, not a requirement to retrofit every service during an unrelated task.

## Dependency vulnerabilities

A critical or high CVE in a direct dependency warrants its own change, separate from unrelated feature work. Open the fix as its own commit (or pull request, when branches are in use) so the audit trail is clean.

A transitive CVE is raised to Jake rather than silently resolved. Upgrading a transitive dependency can bump many unrelated versions and should be a deliberate call.

Lockfile churn to pick up patch versions is acceptable inside a dependency fix. A major-version bump needs its own change and its own verification.

Dependabot pull requests are handled by Jake. Do not review, merge, or close them without being asked. If one is blocking other work, flag it rather than acting on it.
