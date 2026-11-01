# Verification and completion

## Choose checks by risk

Read the affected project's scripts, test setup, and CI configuration. Start with focused checks, then broaden where a shared interface or dependency change warrants it. A documentation-only change generally needs link and diff review, not a full application build.

| Change | Useful evidence |
| --- | --- |
| Bug fix | A regression test that fails for the original behavior and passes with the fix |
| Business logic | Normal case, boundaries, invalid inputs, meaningful failure cases |
| API or authorization | Contract assertions, unauthenticated and forbidden cases, tenant isolation |
| Database | Clean initialization and upgrade from a representative prior schema; constraints and mappings |
| External write, payment, job, webhook | Duplicate delivery, timeout, partial failure, bounded retry behavior |
| Shared library | Focused library tests and representative affected consumers |
| UI | Build, type, and lint checks available in the project, and visible behavior at relevant sizes |
| Documentation | Existing paths, valid links, consistent entry files, no invented claims |

Apply the project's merge and coverage policy as well. The project map names forbidden test targets. Do not point a test at a shared host, lab cluster, or production-like database because a local fixture failed to start.

Test externally observable behavior, not private method structure. Use the repository's frameworks. Add meaningful tests for new behavior and regressions. Avoid tests that merely repeat constants or implementation details. Do not create a low-value test for a wording change.

## Test taxonomy

"Run the tests" is ambiguous. These are the categories used here:

- **Unit tests** exercise one class or function with no network, no database, and no container. Java files named `Test*`, `*Test`, or `*Tests`. Go `_test.go` files without an integration build tag. Web `*.test.ts(x)` or `*.spec.ts(x)`.
- **Integration tests** exercise a module against local disposable fixtures (Testcontainers for PostgreSQL or Redis, local mocks for external providers). Java files named `IT*`, `*IT`, `*IntegrationTest`, or `*IntegrationTests`. Go files behind `//go:build integration` or an equivalent tag. Web integration suites live beside the host they exercise.
- **End-to-end tests** exercise the full stack against local containers that approximate production topology. They are rare. Mark one explicitly when adding it.

Unit tests must not require Testcontainers, Docker, or a network. Integration tests must not require a shared cluster or any shared host. The project map names the local-test rule for that checkout.

When invoking tests, run the narrower category first and widen only if the change warrants it. Report which category ran, not just "tests passed."

## Test environment

Automated tests use disposable local instances through Testcontainers or an equivalent isolated fixture. Inspect effective database and endpoint configuration, allocate local fixture ports dynamically, and mock external providers. If local dependencies cannot start, report the check as blocked. Never fall back to a shared host or a lab database.

Do not replace authentication or tenant enforcement with an unconditional bypass to make a test pass. Keep test-only substitutions confined to test configuration.

## Interpret results honestly

Record the directory, the command, the result, and any prerequisites. Distinguish passed, failed, and not run. A compile is not an integration test. A mock is not proof that the real service is reachable. A zero exit code with zero selected tests is not evidence that behavior was tested.

If an environment issue prevents verification, report the specific issue and what remains unverified. Do not repeatedly rerun an unchanged failure without a reason. A pre-existing failure needs a baseline or other evidence before being called pre-existing.

## Completion review

- The requested outcome is implemented, including affected interfaces and necessary documentation.
- Relevant checks passed, or their limitations are explicit.
- No unintended generated outputs, secret files, dependency churn, or unrelated edits entered the diff.
- Compatibility, security, and data implications were considered where applicable.
- Unresolved human decisions are recorded with `## todo human`. Resolved decisions are incorporated into the guidance. Do not represent an unimplemented policy as completed application work.
