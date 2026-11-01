# Shell scripting

Treat a shell script as production code. These scripts touch databases, publish artifacts, and modify shared systems. A Makefile recipe that shells out is in the same category.

## Script preamble

Every shell script starts with:

```sh
#!/usr/bin/env bash
set -euo pipefail
```

- `-e` exits on error.
- `-u` fails on an unset variable.
- `-o pipefail` makes a failing command in a pipeline fail the whole pipeline.

If one line must tolerate failure, scope it narrowly: `foo || true` on that line, not a global disable.

## Variables and expansion

- Quote expansions: `"$var"`, `"${var}"`, `"$@"`. An unquoted expansion is the usual shell bug.
- Prefer `"${var}"` when the variable is followed by other characters.
- Avoid `eval`. Use an array for an argument list that needs word splitting.
- Use `$(cmd)`, not backticks.

## Dry-run and read-only flags

A script that touches a shared system (a database, a remote host, a container registry, a Helm release) must support a read-only mode.

- `--info` or `--dry-run` must be truly read-only. If the flag only sets an environment variable that a downstream script ignores, that is a bug.
- When a script invokes another script that does not honor the dry-run signal, the outer script must refuse to run with `--info`, or it must document the limitation at the top of the file.
- Print the target (host, database, cluster) before a destructive action. A person reading stdout should see what is about to change.

The project command reference records known cases where this contract is currently broken. Fix the script when working on it. Do not add a parallel workaround.

## Portability

- Target bash. Do not assume dash or `sh`. The shebang is explicit for that reason.
- Do not rely on a GNU-only option (`grep -P`, `sed -i` differences) without noting the macOS and Linux difference.
- Prefer `rg` where it is available. Fall back to `grep` only when the script must run in a minimal image.

## Dangerous operations

A script that runs `rm -rf`, `DROP`, `TRUNCATE`, `kubectl delete`, or `git push --force` must:

1. Require an explicit confirmation flag (`--yes` or `--force`), not a bare invocation.
2. Print the target first.
3. Fail safe when a required variable is unset.

Do not write a script that deletes without a flag.

## Checks

- Lint with `shellcheck` when it is available. Address a warning, or document why it is intentional.
- Run the script against a disposable fixture before declaring that it works. Reading the script is not the same as running it.
