# Maintaining these references

## Change rules where they live

Keep one maintained statement of each rule. Shared practice belongs in `~/.ai/core/`. Language defaults belong in `~/.ai/languages/`. Project facts and exceptions belong in that project's overlay. Entry files and adapters route readers. They should not grow a second copy of the policy.

When changing a standard, describe the problem it solves and its scope. Link to current source or an accepted decision where useful. Prefer a rule a reviewer can assess over a slogan such as "production ready" or a requirement to use a named pattern everywhere.

Do not describe a proposed convention as existing implementation. Date an observation that can drift, and update it when the source changes. Avoid copying full dependency versions or service configurations into prose.

Nothing project-specific belongs in `~/.ai`. If a sentence names one project's service, host, schema, or path, it belongs in that project's overlay.

## Resolve human questions

Use an exact `## todo human` heading for each unresolved decision. Include the question, evidence, impact, and interim behavior. Repeated headings are intentional and searchable.

Resolution:

- A `## todo human` with no answer underneath is a pending question. Do not act on a proposed default. Keep working around it, and leave the heading alone.
- A `## todo human` with an answer underneath is a resolution. Rewrite the block in place: replace the question with the accepted rule and its scope, remove the `## todo human` heading, and fold the decision into the surrounding section. Update affected references in the same change, then run the documentation check.

Do not leave a resolved question behind as "resolved — see below." The next reader should see the rule, not the history.

## Dates in records

Use an ISO 8601 date (`2026-10-25`) in every dated observation, work record, and archived file name. Never write "yesterday", "last week", "earlier this month", or "soon". When a date is unknown, write "date unknown" rather than guessing.

## Keeping docs current

When you change behavior, a convention, or a path that any shared or project reference names, update the affected doc in the same change. Do not leave the docs stale and plan to catch up later.

`~/.ai/scripts/check_docs.py` is a manual validator for a review pass, not an every-edit hook. Do not run it after every doc change. Run it when you change the reference set, and when a `## todo human` is resolved.

## Project exceptions

Document an exception in the project overlay, with the shared rule, the reason, the scope, and any compensating check. Do not duplicate an entire shared guide to express one difference. Do not use an exception to silently override an explicit user instruction.

## Moving a guide later

1. Move reusable practices and language defaults together, preserving relative links inside `~/.ai`.
2. Leave each project's overlay in that project, and update its links into `~/.ai`.
3. Pin or vendor a revision if a project cannot read `~/.ai` directly, so a checkout is reproducible.
4. Update entry files and assistant setup in the same change.
5. Validate links, and verify that a session opened inside one service can still reach the guide.
