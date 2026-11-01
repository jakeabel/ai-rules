---
name: fine-tune
description: "Interview the project owner in chat to make a codebase easier for AI assistants to work on, then incorporate accepted decisions into shared project documentation. Use for /fine-tune or $fine-tune with an optional directory, or requests for an interactive project-guidance interview. This is documentation refinement, not model training."
---

# Fine-tune project guidance

Turn the owner's tacit knowledge into useful shared project references through an adaptive conversation. The user answers in chat, not in a questionnaire document. Keep the interview tied to real tasks an assistant needs to perform correctly.

## Select the directory

Accept `/fine-tune`, `/fine-tune <directory>`, `$fine-tune`, and equivalent natural-language invocations. Without a directory, use the current working directory. An argument matching the current directory's name means the current directory: from `/Projects/billing`, `/fine-tune billing` targets `/Projects/billing`, not `/Projects/billing/billing`.

Otherwise resolve an existing explicit or relative path within the available access. If the directory is missing or genuinely ambiguous, ask which directory the user intends. Do not create or clone a project to satisfy the argument. State the resolved target briefly and keep project-specific edits scoped to it and its established documentation locations.

## Establish what is already known

Read `~/.ai/README.md`, the project entry file, the project map if present, and repository status. Follow instructions in any separate service repository before touching it. Inspect only enough current source or configuration to ground the questions. Do not turn the interview into an exhaustive source audit.

Separate accepted decisions, observed implementation, and unresolved knowledge. Use previous answers in this conversation and existing accepted policy. Do not ask the user to repeat them. A policy not yet implemented belongs in follow-up work, not back on the list of unanswered policy questions.

Identify the most consequential missing context for the owner's actual workflow. If that workflow is unclear, start by asking for a recent task that required too much explanation or correction. Use the example to discover what the assistant could not infer from the project.

## Interview in chat

- Ask one focused question per turn, then wait for the answer. Keep progress comments free of additional questions. Do not produce a large initial questionnaire or write questions into a document as the interview interface.
- Offer two or three concrete options when they reduce effort, and always allow a free-form or combined answer. Do not force a false choice or recommend an answer without explaining a material tradeoff.
- Prefer concrete situations, examples, boundaries, and acceptance criteria over generic questions such as whether the user wants readable code. Distinguish how the system works now from how the owner wants it to work.
- Adapt the next question to the answer. Briefly restate a consequential interpretation. Ask a follow-up only when ambiguity would materially change the guidance. Do not silently convert a tentative answer into a hard rule.
- Cover only relevant gaps: domain vocabulary and ownership, tracing a feature across services, business invariants, trusted examples, local setup and verification, compatibility, common mistakes, or the desired completion evidence. Do not run through every category mechanically.
- Keep the pending question and accepted answers in conversational context. If the user pauses, preserve confirmed decisions as requested and resume without restarting the interview. Skipping a question is not an answer.
- If source and the owner's answer differ, explain the precise mismatch and distinguish a corrected fact from a desired change. Ask for a decision only if the intention remains ambiguous. Do not implement application changes during the interview.

The interview is ready to wrap up when the agreed target workflow has an actionable route from request to verification, important remaining unknowns are identified, and further questions would add little practical value. State remaining themes briefly when needed and give the user an opportunity to continue or finish. Do not declare all projects understood after a small number of generic answers.

## Incorporate the decisions

When the user finishes the interview or the agreed scope is covered, update the actual references. The invocation authorizes this documentation work. No extra approval is needed for ordinary in-scope edits. If the user wants incremental incorporation, save settled answers as the conversation proceeds instead.

- Put each decision in its owning reference and link to it. Do not make a parallel interview-answer file or a per-assistant policy copy.
- A practice that applies to every project goes in `~/.ai`. A fact about one project (its services, hosts, schemas, paths, or standing exceptions) stays in that project's overlay. Do not move a project fact into `~/.ai`.
- Prefer concrete navigation, source references, worked examples, prerequisites, and observable checks over more policy prose. Verify referenced paths and avoid inventing commands.
- Reconcile related references so an old rule does not remain active elsewhere. Preserve unrelated edits, historical evidence, and explicit exceptions.
- Keep desired behavior distinct from current implementation. Put implementation work in the project's task list with acceptance criteria. Do not mark it complete or execute it merely because the policy was accepted. Follow local priority and tracking conventions. Do not retag the whole task list as a side effect.
- Leave a truly unresolved decision under the exact heading `## todo human`, with the question, the evidence, and the interim behavior. Do not leave that heading attached to an answered decision. Use it for a residual unknown, not as a replacement for asking during the chat.

Check links, entry-point discoverability, contradictions, and the focused diff. Run `python3 ~/.ai/scripts/check_docs.py` and, when a project overlay changed, pass that project root. Do not run an application build, contact a shared environment, deploy, rotate a secret, or publish an artifact to validate prose.

Finish with a concise account of where the guidance changed, material follow-up, and the checks actually run. Do not claim application behavior changed or that all uncertainty is resolved.
