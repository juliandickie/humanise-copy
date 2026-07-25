# Session Handoff - 2026-07-26 - repair-artifact checks, claude-seo routing, 0.3.0 published

Previous handoff - [SESSION-HANDOFF-2026-07-25.md](SESSION-HANDOFF-2026-07-25.md).

## Goal

Close open item 1 from the previous handoff, fold the fleet run's repair-agent
failure modes into the skill itself, then everything that fell out of it - a
claude-seo integration so answer-engine structure stops reading as a tell, the
Ascot C&I copy decisions, and a machine-wide fix for agent telemetry landing in
project folders.

## State - verified against git, the live URLs and the installed plugin cache as of 2026-07-26, session f8628411

| Repo | Branch | HEAD | Pushed |
|---|---|---|---|
| humanise-copy | main | c41694c | yes, level with origin |
| ai-loadout | main | c52c87f | yes, level with origin |
| outfit (marketplace clone at ~/.claude/plugins/marketplaces/outfit) | main | 508bb45 | yes, level with origin |
| pro-marketing-web-agency | stack-2026 | 6b75806 | UNCOMMITTED work below, HEAD itself level with origin |

- humanise-copy v0.3.0 SHIPPED. 554a4bf carries the work, c41694c the version
  bump. 46 tests. Verified by GitHub API plus anonymous raw fetch, not the push
  output.
- Both marketplace listings updated in lockstep (description plus README row,
  all four surfaces byte-identical) and pushed.
- The INSTALLED plugin is genuinely 0.3.0. The cache clone at
  `~/.claude/plugins/cache/outfit/humanise-copy/0.2.0` was fast-forwarded to
  c41694c and `installed_plugins.json` updated (version, gitCommitSha), with a
  backup at `installed_plugins.json.bak-20260726-humanise`. Verified
  FUNCTIONALLY - the cached detect.py fires the new checks and its 46 tests pass
  from the cache. NOTE the directory is still named `0.2.0`; that is cosmetic,
  and a `/plugin` update in an interactive session will lay down a clean 0.3.0
  directory and regenerate the install manifest.
- Ascot C&I demo REDEPLOYED and live-verified at https://pmw-ascot-ci.pages.dev
  (deployments 615ddc8d then 6e176c3b). Three copy changes live, README no
  longer served, noindex and robots.txt Disallow intact.
- pro-marketing-web-agency stack-2026 carries UNCOMMITTED work, some of it mine
  on Julian's explicit go, some the parallel session's. See Open work.
- Machine config changed - `OMC_STATE_DIR` in `~/.claude/settings.json`,
  `~/.gitignore_global` wired via `core.excludesFile`, and 162 `.omc` dirs
  archived to `~/.claude/archive/omc-2026-07-25/`.

## Decisions (chosen AND rejected)

- Mechanical gets a check plus a test, judgment gets prose. Tic convergence,
  amputated purpose clauses, staccato runs, repeated openers and adjacent echoes
  became checks 12 to 16. Telegraphese, wrong connectives, dangling references
  and meaning-adjacent rewrites stayed prose, because a stdlib check for them
  needs part-of-speech tagging and would over-report.
- The read-aloud gate became STRUCTURAL, a numbered Mode B step plus a required
  READ ALOUD line in the verdict format. Rejected leaving it as a prose reminder
  - per superpowers:writing-skills, an omitted-element failure needs a slot in
  the template, not more words near it.
- Check 15 auto-exempts answer blocks, but ONLY for content-word openers. A
  determiner run ("The software... The technology...") still fails even under a
  question heading. Rejected the naive "exempt anything under a question
  heading", which a test caught immediately - it would have waved the planted
  fixture's metronome straight through.
- Check 1 (question-cadence headings) is deliberately NOT auto-exempted. The
  planted fixture and a real Ascot insights page both run near 100 percent
  question headings and the difference is semantic. Inventing a rule there would
  let real slop through, so the detector reports honestly and raises
  `consult_claude_seo` instead.
- Division of authority, now in SKILL.md - claude-seo owns whether a structure
  is answer-engine optimisation, humanise-copy owns whether it reads human. Both
  must pass, neither overrides.
- "subject to suitable council approval" KEEPS "suitable". It is Alex's verbatim
  (VOC line 123) and Julian's reasoning is that the qualifier positions Ascot as
  the guide to what is suitable.
- OMC telemetry fixed at SOURCE with `OMC_STATE_DIR` rather than only ignoring
  it. Set in Claude's settings.json, not the shell profile, because `.omc` is
  written by Claude sessions and the auto-mode classifier blocks .zshrc edits.
- Archived the 162 `.omc` dirs rather than deleting. `mv` on the same filesystem
  costs nothing and stays reversible.

## Tried and failed (do not rediscover)

- A blanket answer-block exemption for check 15 broke the fixture test instantly.
  The content-word versus determiner split is what makes it safe.
- My first SEO test asserted a GEO page should PASS check 1. Correcting the TEST
  rather than the code was the right call; there is no honest discriminator.
- `du -sh $(cat list)` on paths with spaces reported 3.5 GB for what is really
  3.8 MB, inventing directories like "ASDE" and summing them repeatedly. 25 of
  the 167 `.omc` paths contain spaces. Any bulk operation over that list must be
  null-delimited.
- Counting with `find -maxdepth 3` gave 62 `.omc` dirs; the real number is 167.
- A cache-busted apex fetch reported the README still live seconds after the
  deploy that removed it. It was the Pages edge cache. The deployment-specific
  URL (`https://<id>.pmw-ascot-ci.pages.dev/...`) is the honest check.
- Redeploying the demo folder published the parallel session's `/process/` page
  and `assets/site.css`, which were NOT live before. Diff a folder against the
  previous deployment BEFORE deploying; the wrangler upload profile gives the
  count but not the risk.

## Julian's feedback this session (verbatim where short)

- "The four asks are ok as they are heading questions for SEO optimisation and
  ask engine." - the correction that produced the whole claude-seo integration.
- "so those things don't trigger an issue and the audit understands it is just
  good optimisation as long as they are written well" - "written well" is the
  condition, which is why the exemption warns rather than going silent.
- "keep the suitable the way Alex said it - it makes it a nice qualifier that
  not everything is suitable and positions them as the ones to guide the
  customer to what is suitable."

## Recipes and footguns

- Detector: `python3 scripts/detect.py FILE --format markdown` (`--gate` for CI).
  Tests: `python3 -m unittest discover tests` from the repo root.
- Ascot C&I demo deploy (from the homepage-demo README, NOT deploy.mjs which
  targets the preview branch):
  `npx wrangler pages deploy "$D" --project-name pmw-ascot-ci --branch main --commit-dirty=true`
  Deploy from a cleaned rsync payload, excluding `.omc`, `.DS_Store` and
  `README.md`. Then verify with a cache-busted fetch, twice, and check the
  deployment-specific URL if the apex looks stale.
- The C&I demo HTML is HAND-BUILT, not generated from `copy/*.md`. Every copy
  repair has to be applied twice and the demo redeployed, which is how the live
  site kept serving a spliced triad the copy doc had already fixed.
- Marketplace listings carry no version; they track the repo URL. Publishing a
  new version means bumping plugin.json, pushing, then updating the cache clone.

## Open work, ranked

1. pro-marketing-web-agency stack-2026 has UNCOMMITTED work needing Julian's
   commit decision - `copy/HOMEPAGE-copy.md` and `homepage-demo/index.html`
   (modified by me on his go), plus the parallel session's untracked
   `copy/PROCESS-copy.md`, `homepage-demo/assets/site.css` and
   `homepage-demo/process/`. Coordinate with that session before committing.
2. The three-way phrasing in the C&I copy. "drawings ready to price" now in four
   places, "drawings suitable for pricing" (Alex's near-verbatim) in four others.
   Converging them is Julian's call.
3. `pro-marketing-ads-project/.omc` is TRACKED in git. Needs
   `git rm -r --cached .omc` plus a commit.
4. scallywags-site-c founding-year guard comment is applied but disk-only and
   unbuilt into any deploy (it is a source comment, ships nothing).
5. Consider porting the .astro and .json prose extraction into the plugin as a
   first-class batch mode.
6. `~/.claude/archive/omc-2026-07-25/` can be deleted once nothing has regressed.

## Questions Julian needs to answer

- Commit the stack-2026 C&I copy changes, or leave them for the parallel session
  to fold in with its own work?
- Converge the "drawings" phrasing on Alex's "suitable for pricing", or keep the
  two forms as they read differently in their contexts?

## Kickoff prompt for the next session

See the final assistant message of this session; identical copy in
[NEXT-SESSION.md](NEXT-SESSION.md).
