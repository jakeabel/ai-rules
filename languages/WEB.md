# Web UI

Find the source that owns the visible behavior before editing. Some services only host or proxy assets built in another project. Editing the host is not necessarily a UI change.

Use the local `package.json`, lockfile, framework configuration, and existing component patterns as the source for commands and versions. Do not assume every UI folder has the same scripts or tests.

## Implementation

Keep component and state responsibilities clear. Reuse the established design system. Preserve keyboard access, labels, focus behavior, contrast, and responsive layout. Handle loading, empty, error, and success states appropriate to the task.

Keep secrets and privileged operations on the server. Browser code is public. Enforce permissions on the API even when a control is hidden in the UI. Preserve existing session and cookie protections. Do not store a sensitive token through a new mechanism without a deliberate design.

Respect the project's deployment model. A static export cannot rely on a new runtime server feature without a coordinated hosting change. Check routing, asset paths, API URL configuration, and host fallback behavior.

Edit source assets rather than generated export or embedded output, unless that output is intentionally maintained. Check copy scripts carefully. Some replace an entire static directory.

## Checks

Use the package's declared build, lint, typecheck, and test scripts when they exist. Do not invent a `test` script or claim browser verification from a successful build. For a visible change, inspect the affected flow and the relevant viewport sizes if a browser is available. Otherwise say that visible behavior was not checked.

For a UI bug report, ask for a screenshot when the symptom is not reproducible from code alone. A screenshot is evidence of the symptom. It is not evidence of a fix. The fix still needs a browser check, or an explicit statement that no browser check ran. Never claim "verified in a browser" when no browser was opened.

Avoid whole-tree formatting or an incidental lockfile change.

## File organization

Prefer one primary exported component or responsibility per file. This is a default, not a strict requirement. A small helper can stay with the component it supports. Do not split every function into its own file.
