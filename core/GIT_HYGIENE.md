# Git hygiene

## Commit messages

- The subject says what was done, in prose. Conventional-commit prefixes (`feat:`, `fix:`, `chore:`) are not required.
- Keep the subject short. About 50 characters is the target. Do not truncate a clear subject just to hit that number.
- Wrap the body at 72 characters when a body is useful. Omit the body for a self-explanatory change.
- Imperative mood ("add", "fix", "update"), not past tense.
- Do not add AI-tool attribution trailers: no `Co-Authored-By: Claude`, no `Generated with [Claude Code]`, no `Co-Authored-By: Codex`, and no equivalents from other tools. Attribution for AI assistance belongs in the pull request description if anywhere, not in commit history.

## Pushing

- After a commit that was requested, push `origin HEAD` without asking again.
- Push only when the GitHub org is `jakeabel` or `abelurx`. Never push a remote that belongs to any other org. A project does not get an exception because the remote is convenient.
- Direct push to `main` is currently acceptable. Branches and human review will come later. This guide will be updated when that changes.
- Never force-push to `main` or any shared branch.
- `git push --force-with-lease` is preferable to `--force` on a branch you own. Confirm the target before using either.

## Branch naming

When a branch is appropriate, use one of:

- `feature/<short-description>` for new functionality.
- `bugfix/<short-description>` for a defect.
- `hotfix/<short-description>` for an urgent production fix.

Keep the description short and kebab-cased: `feature/service-auth-rollout`, not `feature/Add_the_new_service_authentication_rollout`.

## Pull request descriptions

When a pull request is opened:

- Title: same style as a commit subject.
- Body: a short summary of what the pull request does. Screenshots or a test plan only if the change warrants them. Do not pad with boilerplate sections ("Why", "What", "How") when a sentence suffices.

## Revert vs reset

- `git revert <sha>` is the default when a commit is already on `main` or shared history. It preserves the audit trail.
- `git reset --hard` plus `git clean -fd` is only acceptable when the commit has not been pushed and there are no other uncommitted changes that could be lost.

Before any destructive git operation, run `git status --short` and `git stash list` and read the output. If there is uncommitted work you did not create, stop and ask.

## Inspecting old revisions

- Use `git show <sha>:<path>` to read a historical version of a file.
- Use `git worktree add` for a separate working copy on another revision when you need to run it.
- Do not `git checkout <old-sha>` in the main working tree if there are uncommitted changes.

## Never do

- Never rewrite shared history (`rebase -i`, `commit --amend`) on commits that have been pushed.
- Never use `--no-verify` to skip pre-commit hooks unless Jake has explicitly authorized it for that commit.
- Never update git config as a side effect of an unrelated task.
- Never run `git submodule update --init --recursive` as a routine setup step. The project map says which nested checkouts are real repositories.
