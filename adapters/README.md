# Give every assistant the same context

Engineering policy lives in `~/.ai`. Project facts live in the project's overlay. Root `AGENTS.md`, `CLAUDE.md`, and `GROK.md` in a project are short entry points. They point here and then at that project's map. Automatic loading depends on the tool and how a session is opened. A file on disk does not prove the assistant read it.

## Where each tool looks

| Tool | Global pointer | Skill discovery |
| --- | --- | --- |
| Grok | `~/.grok/AGENTS.md`, and `~/.claude/CLAUDE.md` when Claude compatibility is on | `~/.grok/skills/fine-tune` symlinks to `~/.ai/skills/fine-tune`. `~/.grok/config.toml` also lists `~/.ai/skills`. |
| Claude Code | `~/.claude/CLAUDE.md` | `~/.claude/skills/fine-tune` symlinks to the same skill |
| Codex | `~/.codex/AGENTS.md` | `~/.codex/skills/fine-tune` symlinks to the same skill |
| ChatGPT in a browser | No home-directory autoload | Attach this file and the linked documents. A link to a local path is not enough. |

The global pointer files are short. They tell the assistant to read `~/.ai/README.md` and then the project entry file. Do not paste these standards into the pointer files.

IntelliJ is the IDE. An assistant integrated into it receives the same entry point. Do not assume an unspecified integration loads it. Open the entry file when discovery is unavailable.

## Setup for a project session

1. Start in the intended project checkout.
2. Provide that project's `AGENTS.md`, through project instructions or by opening it.
3. Read `~/.ai/README.md`, the working agreement, the project map, and the task references before editing.
4. When the session starts inside a nested service repository, open the parent guide if it was not loaded. An independently cloned service does not contain the parent overlay.
5. If this session cannot read `~/.ai`, stop and say so. Do not invent the shared rules.
6. Confirm the affected implementation, repository, and planned checks in the normal work update.

A reusable session instruction:

> Before working, read ~/.ai/README.md and the project AGENTS.md. Apply the task-relevant standards, inspect current code and commands, preserve existing changes, and mark an unresolved documentation decision with the exact heading "## todo human". Report checks actually run and material limitations.

## Portability

Keep relative links inside `~/.ai`. Put project paths and decisions in that project's overlay. Do not add credentials or a project's hostnames to these shared files.

If a project later vendors a copy, pin a reviewed revision. Do not make an assistant fetch and execute an unreviewed latest policy on every task.

## Capability expectations

The guide assumes an assistant can read files, run shell commands, and inspect command output. Tools differ:

- Some sessions have no filesystem access.
- Some sessions are read-only.
- Some have no web access, and some cannot render an image.

When a required step cannot be performed, say so. For example: "I cannot run `make test` in this session. Run it and paste the output." Do not substitute a static-source review for a required check without saying so.

Do not simulate output. A test result that was not produced by running the test is a fabrication.

## Handoff between sessions

A session often ends mid-task, and the next session may be a different tool. The previous transcript is not available. Leave a handoff where the project says handoffs go.

- Include what is done, what is next, decisions taken, open questions, and the exact commands that already passed.
- The project's task list is the authoritative "what's next." The handoff note is "where I left off inside this one item."
- Do not rely on another tool reading your previous session or its private memory. If it is not in the handoff note or the standards, it does not transfer.
- When picking up a task, read the handoff note first and the current source second. Verify the note before continuing. It may be stale.
