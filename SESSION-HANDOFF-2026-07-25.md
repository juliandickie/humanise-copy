# Session Handoff - 2026-07-25 - humanise-copy built, shipped, and run across the fleet

Previous handoff - none. This repo was born this session.

## Goal

Build a voice-preserving de-AI skill (detect and repair the tell-tale signs of AI generation without flattening brand voice), ship it as a public plugin, wire it into the copy pipeline, and run it across the Pro Marketing client fleet plus the Ascot RE production site.

## State - verified against git, live URLs and detector runs as of 2026-07-25 ~18:10 AEST, session fb149135

- code/humanise-copy - PUBLIC at github.com/juliandickie/humanise-copy (MIT), main pushed. v0.2.0: detector (~30 checks incl. spliced-triad + borderline band), 4 references, 20 unit tests green, RED/GREEN evidence in tests/. Listed in BOTH outfit and loadout marketplaces (installed, loads from the outfit cache).
- copy-school - copy-editing-sweeps handoff row committed + pushed (2154097, ed8eb13), copy-editing-sweeps.zip rebuilt. Julian's claude.ai UPLOAD of that zip is STILL PENDING. The installed marketplace clone + cache were synced live.
- idd-writing-style (Institute-of-Digital-Dentistry org repo) - Pre-Ship QA section pushed (5bd356a, 7b7b1b5), bundle rebuilt; Julian confirmed the anthropic-skills redeploy DONE.
- Ascot Homes + Scallywags demos - 49 content files swept (6 Sonnet agents + main-session ear QA, ~500 repairs), variants synced byte-identical, ALL FIVE rebuilt and redeployed --branch=preview, repairs live-verified. Sites are disk-only (not git); originals archived per site in archive-pre-humanise-2026-07-25/.
- Ascot C&I copy (pro-marketing-web-agency, branch stack-2026) - HOMEPAGE + CAPABILITY-STATEMENT verdict SHIP zero repairs; PROCESS-copy.md (a parallel session's untracked draft) repaired on Julian's direction (spliced-triad lead + "sign the contract"). ALL of this remains UNCOMMITTED working-tree state on stack-2026 - the parallel session's branch, not ours to commit.
- pro-marketing-web-agency CLAUDE.md - the copy-pipeline convention (FINAL requires humanise-copy Mode C + the write-for-the-ear block) added, UNCOMMITTED on stack-2026 for the same reason.
- ascot-re-2026 - 14 insights repaired, committed 3a1076a + README deploy-state fde84c5, PUSHED, main level with origin, tree clean. DEPLOYED live at https://pmw-ascot-2026.julian-18d.workers.dev (wrangler version 7f86cc7f, 14-of-14 changed assets, repairs live-verified, admin stripped, noindex intact).
- Memory - project_humanise_copy_skill, project_ascot_homes_scallywags_reimagining, project_ascot_re_2026_production and the MEMORY.md index all current.

## Decisions (chosen AND rejected)

- Standalone plugin repo, NOT a 21st skill inside 10x-copywriting (IP separation, reach beyond conversion copy). amh marketplace registration REJECTED by Julian ("juliandickie not amh"); outfit + loadout listing chosen later, repo flipped public by Julian.
- Detector measures, skill judges - the script never whitelists; signature phrases ("Here's the thing"), 10x techniques, format-native rhythm are editorial keeps.
- Pipeline order is voice, then sweeps, then humanise, always last; any later edit reopens the pass.
- TTR and paragraph-shape SD are out of repair scope on conversion/templated/financial copy (offer-noun word mirrors and designed card grids read low by design).
- Question-heading cadence gets TRIMMED into the 57-70 percent GEO band (closing-CTA questions convert; genuine PAA questions never do) - wholesale conversion rejected.
- Frozen surfaces on principle: testimonials (real people's words), listings (client-authored), About-the-author blocks, TL;DR blocks that mirror Tina frontmatter (desync risk), all financial figures / QLD tenancy law / RTA + Form references / advice-posture sentences, founding-year claims (YMYL gates).

## Tried and failed (do not rediscover)

- Repair agents over-correct in predictable ways: dropped-article telegraphese ("Buyer pool here includes"), convergent tics (two agents independently invented "Honestly,"), amputated purpose-"So" fragments, staccato over-splitting, dangling appositives, wrong connectives ("Then again" for "and again"). Detector-clean does not mean ear-clean.
- My own QA over-restored articles once (innes-park hit 39.5 percent "The" openers); the fix is article-preserving restructures (possessives, natural fronting), not amputation and not blind restoration.
- Deploy-tool 200s and even script-verified deploys can serve stale edge-cache HTML on branch aliases; cache-busted fetch is the true content check (bit twice: Pages branch aliases AND the Workers first-fetch footgun).
- Unquoted bash heredocs mangle \n escapes inside python source being written; use quoted heredocs ('EOF') for codegen.
- detect.py once contained literal NUL bytes from an unescaped sentinel - write \x00 as an escape.

## Julian's feedback this session (verbatim where short)

- "The pattern looks right but the way the Copy in someways feels a little off just like missing some filler words or just said in a slightly wrong way." - led to the spliced-triad check and the read-aloud doctrine. Over-tightening past idiom IS a tell.
- "it should go on juliandickie not amh in github" - marketplace/repo placement.
- "make sure it doesn't use the iDD writing style skill" - Pro Marketing client passes run under the client voice, never iDD.

## Recipes and footguns

- Detector: python3 /Users/juliandickie/code/humanise-copy/scripts/detect.py FILE --format markdown (--gate for CI). Tests: python3 -m unittest discover tests -v from the repo root.
- Fleet runs: fork the batch-runner pattern (mirror extraction for .astro/.json -> detector -> details.json drill -> agents -> ear QA -> re-verify). The session's runners lived in the session scratchpad and DIE WITH IT; the pattern is documented in docs/dev/2026-07-25-fleet-run-learnings.md. Extraction mirrors distort shape metrics - trust only high-precision checks (phrases, triads, hygiene, hedges) on mirrors.
- Agent briefs: prescriptive, with the naturalness rules (no telegraphese, no tic convergence, no amputated-So, read-aloud gate) and domain freezes named. Each wave's QA findings fold into the next wave's brief - the last agents of both fleets needed near-zero corrections.
- Ascot RE deploy recipe (proven this session): npm run build in site/ (74-page gate must hold, withdrawn Bauer St builds nothing), rm -rf dist/admin, npx wrangler deploy from site/, then fetch pages TWICE before judging.
- Demo deploys: node skills/build-site/scripts/deploy.mjs <dist> <slug> --branch=preview from the pro-marketing-web-agency root.

## Open work, ranked

1. Fold the repair-agent failure modes into the skill itself (reference 03 or Common Mistakes) - material ready in docs/dev/2026-07-25-fleet-run-learnings.md.
2. Julian: upload copy-school/10x-copywriting/zips/copy-editing-sweeps.zip to claude.ai (standing since the rollout).
3. scallywags-site-c lacks the founding-year guard comments the primary's about page carries - compliance-note sync gap.
4. Ascot RE: Tina Cloud project (Julian's task 6) then tasks 7-9; go-live blockers unchanged (real photography, ACL guarantee check, noindex flip).
5. Consider porting the astro/json extraction into the plugin as a first-class batch mode.

## Questions for Julian

- "subject to suitable council approval" appears in three C&I files; standard phrasing is "subject to council approval" - Alex's verbatim or drop "suitable"?
- C&I Step 3 "drawings you can price" - deliberate VOC or reword to "drawings ready to price"?

## Kickoff prompt for the next session

See the final assistant message of this session; identical copy below.

---

Working directory ~/code. humanise-copy is its own repo (github.com/juliandickie/humanise-copy, public). The client fleet lives under ~/code/pro-marketing-web-agency (parent repo, branch stack-2026 carries a PARALLEL session's WIP - do not commit or revert there); client demo sites under clients/ are disk-only; ascot-re-2026 is its own nested repo on main.

READ FIRST, in order: ~/code/humanise-copy/SESSION-HANDOFF-2026-07-25.md, ~/code/humanise-copy/README.md, ~/code/humanise-copy/docs/dev/2026-07-25-fleet-run-learnings.md, and memory project_humanise_copy_skill. Treat those over any assumption.

State: humanise-copy v0.2.0 public + listed in outfit and loadout, all integrations pushed and live; all five Ascot Homes/Scallywags demos redeployed with swept copy; ascot-re-2026 insights repaired, committed (3a1076a), pushed, and deployed live (version 7f86cc7f). DONE and trusted - do not re-audit. OPEN, ranked: (1) fold the repair-agent failure modes from the dev-docs note into the skill's reference 03 and Common Mistakes, with a test if a check is mechanical; (2) remind me to upload copy-editing-sweeps.zip to claude.ai; (3) the scallywags-c founding-year guard-comment sync; (4) two C&I copy questions in the handoff.

DO NOT TOUCH: anything uncommitted on pro-marketing-web-agency stack-2026 (parallel session), listings and testimonials collections anywhere, About-the-author blocks, TL;DR blocks mirrored in Tina frontmatter.

Standing rules: verify on the rendered artifact never a status line; Sonnet subagents for fan-outs, chunk of 3; never push unasked; no em or en dashes, no colons in headings, straight quotes.

First action: open docs/dev/2026-07-25-fleet-run-learnings.md and draft the reference-03 additions.
