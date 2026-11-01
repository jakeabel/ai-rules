# Go

Use the `go.mod` in the active module as the toolchain and module boundary. A repository may contain several modules. A root-level `go test ./...` is not a workspace-wide test strategy unless a `go.work` file says so.

## Implementation

- Follow the module's existing package and router structure. Keep transport handling separate from business rules and persistence where that separation already exists.
- Use `gofmt`. Keep dependencies explicit and reuse existing packages before adding another framework.
- Wrap returned errors with useful context, preserve error identity when callers need it, and avoid logging the same error at every layer.
- Propagate request contexts and cancellation to database and network calls. Set relevant client and server timeouts.
- Bound concurrent work and make goroutine ownership and shutdown explicit. Close response bodies, rows, and other resources on all paths.
- Use parameterized SQL, explicit transactions when needed, and the existing migration owner. Do not infer a new schema from Go structs.
- Preserve JSON names, null behavior, status codes, and authorization checks when replacing an endpoint that another language already serves.

## Checks

Run focused package tests, then `go test ./...` in the affected module where appropriate. Use `go vet ./...` and race testing when relevant and supported. Inspect build tags and environment dependencies before enabling an integration test. Do not run `go mod tidy` by habit. Use it when a dependency change warrants it, and review the resulting diff.

When two languages implement the same service, compare the externally visible contract. Do not translate framework internals line by line. The project map says which tree is deployed and which trees are rollback copies.

## New services

Follow the project's Go service template when it has one. Adopt it gradually in an existing module when relevant work reaches that area. Preserve the existing contract and document an exception. Do not impose a whole-service rewrite during an unrelated fix. The existence of a template does not mean current modules already conform.
