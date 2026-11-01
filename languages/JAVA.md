# Java and Spring

Apply this only to active Java code. A project may also have a Go implementation and Java rollback trees. The project map says which tree to edit.

## Defaults

Resolve dependency and plugin versions through the affected POM hierarchy. Do not infer them from an old report or from this document. The project overlay names the JDK version and the skeleton to copy for a new service.

For new and changed Java code, unless the project overlay says otherwise:

- Explicit imports. Avoid wildcard imports and inline fully qualified names when an import suffices.
- Prefer one top-level class or enum per file, with a cohesive responsibility.
- Prefer constructor injection.
- Do not expose a persistence entity or a secret field just to avoid writing a mapping.
- Avoid adding Lombok, a builder, or another library where the module does not already use it.
- Unrelated types do not need to be rewritten to match a new preference.

Follow neighboring DTO serialization and validation conventions.

## Spring boundaries

Keep controllers focused on request and response handling, services on business rules, and repositories on persistence. Choose transaction boundaries deliberately and account for lazy loading and query counts. Prefer explicit database migrations and schema validation to automatic production DDL.

Reuse the project's shared security, error, auditing, and HTTP-client components. Verify the actual package and dependency coordinates before importing them. Authorization-server configuration and resource-server configuration serve different purposes.

Use the project's error envelope. Do not introduce a custom error DTO when the existing handler already produces the shape.

## Checks

Use the affected module's Maven setup and test frameworks. JUnit 5, Mockito, and Spring slices or MockMvc are the usual tools. Follow the POM's actual test discovery rules: `IT*`, `*IT`, and `*Test` are not interchangeable unless configured that way.

Run narrow tests during iteration and the relevant module or consumer checks at completion. Inspect Maven lifecycle plugins before `package` or `install`. A build target can create a Docker image and install artifacts into the local repository.
