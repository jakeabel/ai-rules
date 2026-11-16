---
name: bump-core
description: "Bump the Catalyst core patch version, push it, wait for Jenkins to publish it, then point every consuming service at the published version and push those too. Use for /bump-core, 'bump core', or 'release core and update the services'."
user-invocable: true
argument-hint: "[new-version]"
---

# Bump core

Release `~/Projects/catalyst/foundation/core` and move its consumers onto the new version. Only for Jake's lab and repos under the `abelurx` GitHub org. Do not add AI attribution to commits. Work from `~/Projects/catalyst`.

## Rules learned the hard way

- **Core's `Jenkinsfile` runs `scripts/release-check.sh pre` first.** HEAD must be a commit whose subject starts with `Increment version` (or `Release `) and that changes only `pom.xml` files and `.ai/versioning.md`. A code change committed together with the bump fails the build, and so does any commit pushed on top of the bump. Commit and push code first, then the bump as its own last commit.
- A version that failed to build is never in Nexus. Do not repoint services at it. Bump again.
- Never point a service at a version before Jenkins has published it: its own build fails.
- Other sessions work in these repos at the same time and may commit or push between your steps. Re-read `git log` and `git status` before each commit, stage only your own files by name, and never use `git add -A` on a repo with unrelated changes.

## Steps

1. **Check core.** In `foundation/core/`: `git fetch`, `git status -sb`. Anything uncommitted that is not yours stays out of the bump. If code changes need to ship, they are committed and pushed first as normal commits (tests run for them).
2. **Bump.** In `foundation/core/`: `./bump-version.sh` (next patch) or `./bump-version.sh <new-version>`. It edits every POM and `.ai/versioning.md`.
3. **Commit only the version files**, subject `Increment version to <version>`:
   ```bash
   git add -- $(git status --short | awk '{print $2}' | grep -E 'pom\.xml$|^\.ai/versioning\.md$')
   git commit -m "Increment version to <version>"
   scripts/release-check.sh versions
   git show --name-only --format= HEAD | grep -v -E '(^|/)pom\.xml$|^\.ai/versioning\.md$'   # must print nothing
   ```
4. **Push** (`origin` must be `abelurx/core`): `git push origin HEAD`.
5. **Wait for the build.** `~/bin/jenkins wait core main <short-sha>` blocks and prints `core/main #N RESULT sha`. Run it in the background and wait for the notification. It can take several minutes: build, consumer builds, Nexus deploy.
   - `SUCCESS`: go on.
   - `FAILURE`: find which stage failed before deciding (see step 6 for the one known harmless case). Read the cause with `~/bin/jenkins log core main --build N --errors --tail 60` (and `--full | grep release-check`). Report it. Do not touch the services.
6. **Confirm it is published**, whatever the build colour. Nexus needs the `nexus` credentials from `~/.m2/settings.xml` (read them in a script, never print them). The path is `https://repo.jabel.dev/repository/maven-releases/com/abelurx/core-web/<version>/core-web-<version>.pom` (groupId `com.abelurx`, not `com.abelurx.core`); expect 200, and check the previous version as a control. Anonymous requests and the wrong groupId both answer 404.
   - Known quirk (4.1.25): the build can finish `FAILURE` at the last `release-check.sh verify` ("core-observability jar differs from the tested build") even though `mvn deploy` already uploaded everything. If Nexus has the version, go on, and tell Jake the job is red and why.
   - If the build failed earlier (pre-check, tests) nothing was published: stop.
7. **Point the consumers at it.** From `~/Projects/catalyst`: `make set-core-version V=<version>` (runs `scripts/release/set-core-version.sh`). It edits every Java project POM, including legacy trees.
   - Revert any `backup-java/pom.xml` it touched (`git -C <svc> checkout -- backup-java/pom.xml`): legacy trees stay on their old version.
   - `tests/performance` (the performance-tests module) belongs to the umbrella repo, which usually holds unrelated work. Leave it out unless its `pom.xml` is the only change there and Jake asks.
   - Check each diff is only version lines: `git -C <svc> diff -- pom.xml | grep '^[+-][^+-]'`.
8. **Commit and push each service.** In every service repo with a changed `pom.xml` (`platform/` admin-api, billing-api, invoice-api, license-api, notification-api, audit-api, audit-etl, analytics-service, file-store, webhook-relay; `skeletons/skeleton-spring`. `set-core-version.sh` skips `domains/` until Catalyst LAYOUT-4 is answered): stage and commit `pom.xml` only, subject `Use core <version>`, then `git push origin HEAD`. Leave every other uncommitted file alone. Check the remote is under `abelurx`.
9. **Report.** The core build number and result, each service's commit and push result, and which service builds Jenkins has started (`~/bin/jenkins build <job> main`). Pushes start service builds and may deploy to the lab; say so. Deploying a service to fix something is a separate step.

## Checks

- `git -C foundation/core log --oneline -3` shows the bump as the top commit when you push.
- After step 8, `git -C <svc> rev-list origin/main..HEAD | wc -l` is 0 for every service.
- Do not claim the lab has the change: the services still need building and deploying.
