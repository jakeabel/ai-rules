# Python

Follow the project's role for Python. Where Python is tooling and glue (documentation checks, generators, migration utilities) rather than the application language, treat a script as a small tool, not as a service.

## Implementation

- Target Python 3 and the interpreter the project actually runs. A script that runs in CI must say so and must not assume a developer's local virtualenv.
- Prefer the standard library. Add a third-party dependency only when it solves a problem the standard library does not.
- Use the package manager the tool already uses. Record a new dependency in that tool's `requirements.txt` or equivalent. Do not introduce a second manager (poetry, uv) as a side effect.
- Type hints are optional. Add them when they clarify intent or when the function is reused. Do not force them onto every helper.
- Keep one responsibility per script. A script that both inspects and mutates must say so in its usage.
- Scripts live under the project's `scripts/` directory or the owning tool's directory. One-off assistant notes stay in the project's local notes directory.

## Style

- 4-space indentation and UTF-8 source.
- No formatter is required. If a script already uses `black` or `ruff format`, keep that style. Do not reformat an unrelated edit.
- Prefer explicit imports (`from pathlib import Path`), not star imports.
- Avoid `eval`, `exec`, and `shell=True` subprocess calls on untrusted input.

## Checks

- Run the script with its expected arguments before declaring that it works.
- If the script is a validator, its exit code and output are the contract. Preserve both when editing it.
- Do not `pip install` unpinned packages as a side effect of another task.
