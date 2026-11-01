# Engineering practices

## Design and scope

Keep responsibilities clear and interfaces small. Prefer composition and explicit dependencies to hidden globals or new inheritance layers. Extract an abstraction when it removes real duplication or isolates a real boundary, not merely to satisfy a pattern name.

Trace a change from entry point to storage or external effects and back to the response. Preserve documented contracts: paths, response shapes, status codes, identifiers, ordering, pagination, configuration keys, and authorization behavior. Identify intentional compatibility changes and update consumers together where needed.

## Failure behavior

Validate untrusted input at the boundary and enforce business invariants in the owning service. Return errors in the service's established format without stack traces or secret values. Keep enough sanitized context in logs to diagnose a failure.

Set deliberate timeouts for outbound work. Retry only transient failures, with bounded attempts and backoff. Consider whether repeating a request duplicates a payment, message, or write. Preserve cancellation and avoid unbounded queues, loops, goroutines, or thread pools.

Keep transactions scoped to required consistency. Review concurrent updates, uniqueness constraints, and idempotency for state-changing operations. Do not claim a transaction covers remote services when it only covers local database writes.

## Dependencies and configuration

Use the manifest and lockfile in the affected project as the version source. Do not upgrade an entire stack as a side effect of a feature. Explain any new runtime dependency and update the appropriate lockfile using the project's package manager.

Separate configuration from secrets. Document new keys, expected units, defaults, required values, and failure behavior. Validate required configuration at startup. Match the existing deployment mechanism rather than introducing a second one.

## Observability

Reuse existing logging, request IDs, metrics, and health mechanisms. Record useful outcomes and latency without logging credentials, tokens, sensitive payloads, or unbounded user-controlled labels. Keep health checks appropriate to their purpose. A liveness check should not restart a healthy process because a dependency is temporarily down.

Log levels, unless the project defines its own:

- `ERROR` is a failed operation that requires attention.
- `WARN` is a recovered condition worth noticing.
- `INFO` is a routine business event.
- `DEBUG` is development detail.

Do not log at `ERROR` for an expected validation failure. Prefer structured logs in deployed environments. Local runs can use plain text. Do not add a second log format just to satisfy a tool. The project map names the correlation header and any extra redaction rules.

Metrics names and labels follow the existing service's conventions. Do not introduce a new metrics library in a service that already has one.

## Documentation

Explain non-obvious decisions and invariants near the relevant code. Update interface and setup documentation when behavior changes. Prefer links to maintained source over copied code samples or hardcoded version lists that drift.

Comment style:

- Default to no comments. Well-named identifiers already describe what the code does.
- Add a comment only when it names a hidden constraint, workaround, or invariant a reader would otherwise miss.
- Never comment what the code already says.
- Do not write `// added for X task`, `// used by Y flow`, or `// removed because Z`. Task context belongs in the commit message. "Removed" context belongs in the deletion itself.
- No multi-line comment blocks or multi-paragraph docstrings. One short line is the ceiling.

Do not generate a large completion report for a small change unless requested. Use the [work-record templates](../templates/WORK_RECORDS.md) when a decision or handoff warrants a durable record.
