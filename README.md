# Shared AI engineering guide

This is the common reference set for Claude, Grok, ChatGPT, Codex, and other assistants working on Jake's projects. It is also readable by humans. The goal is useful work with consistent decisions, small changes, and verifiable results.

These rules are not project facts. A project's entry file (`AGENTS.md`, `CLAUDE.md`, or `GROK.md`) names the overlay that holds that project's paths, services, and exceptions. Do not copy a project fact into this directory, and do not copy these rules into a project.

Explicit current user instructions and the assistant's actual permissions take priority. Remaining questions are marked `## todo human`. An unconfirmed proposal is not settled policy.

## Read only what the task needs

Always read the [working agreement](core/WORKING_AGREEMENT.md), then the project entry file and its map. Choose the other references from the task:

| Task | Read next |
| --- | --- |
| Any behavior change | [Engineering practices](core/ENGINEERING.md), [verification](core/VERIFICATION.md) |
| Java or Spring | [Java](languages/JAVA.md), then the project's Java notes |
| Go | [Go](languages/GO.md), then the project's Go template if it has one |
| React, Next.js, or browser behavior | [Web UI](languages/WEB.md) |
| Python tooling and scripts | [Python](languages/PYTHON.md) |
| Shell scripts and recipes | [Shell](languages/SHELL.md) |
| Authentication, authorization, tenant data, schema, secrets | [Security and data](core/SECURITY_AND_DATA.md), then the project's authorization notes |
| Commits, branches, pushes, pull requests | [Git hygiene](core/GIT_HYGIENE.md) |
| Planning a substantial change or recording a decision | [Work records](templates/WORK_RECORDS.md) |
| Coordinating a cross-service migration | [Migration template](templates/MIGRATION.md) |
| Connecting an assistant to these files | [Tool setup](adapters/README.md) |
| Interactively improving project guidance | [Fine-tune skill](skills/fine-tune/SKILL.md) |
| Changing or moving these standards | [Maintenance](core/MAINTENANCE.md) |

Read the affected project's README, manifests, implementation, tests, and command definitions as well. Do not load every archived note to begin a small task.

## Layout

- `core/`: practices that travel between projects.
- `languages/`: language defaults. A project's actual setup wins.
- `adapters/`: how to give different assistants this same context.
- `templates/`: optional short records for work that needs them.
- `skills/fine-tune/`: the interview that folds accepted decisions back into these files or the project overlay.
- `scripts/check_docs.py`: local link check. No third-party dependencies.

Application code and deployment configuration remain the evidence for how a system currently works.

## Human review

Search from any project, or from this directory:

```sh
rg -n '^## todo human' ~/.ai
```

Each question includes the evidence and the interim behavior. Resolve it by replacing the question with the decision and its scope. Do not silently turn a guess into a requirement.

## Check links

```sh
python3 ~/.ai/scripts/check_docs.py
python3 ~/.ai/scripts/check_docs.py ~/Projects/<project>
```

The first command checks this tree. Pass a project root to also check that project's entry files and `ai-engineering-standards/` tree. The script checks local file links, including `~/.ai/...` links. It does not validate application behavior or prove that an assistant loaded the files.

## Ownership

Jake owns these standards and makes the final decision when conventions conflict. Record a material conflict with the evidence. Do not resolve it through an unrelated rewrite.
