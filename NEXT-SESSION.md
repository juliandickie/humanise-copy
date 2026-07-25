# Kickoff prompt for the next session

Paste the block below to start the next session with full context.

---

Working directory ~/code. humanise-copy is its own repo (github.com/juliandickie/humanise-copy, PUBLIC, MIT) on main. The client fleet lives under ~/code/pro-marketing-web-agency (parent repo, branch stack-2026 carries BOTH a parallel session's WIP and some copy edits I made on Julian's explicit go); client demo sites under clients/ are disk-only; ascot-re-2026 is its own nested repo under clients/.

READ FIRST, in order: ~/code/humanise-copy/SESSION-HANDOFF-2026-07-26.md, ~/code/humanise-copy/README.md, ~/code/humanise-copy/docs/dev/2026-07-25-fleet-run-learnings.md, ~/code/pro-marketing-web-agency/research/ascot/commercial/CLAUDE.md, and memory project_humanise_copy_skill. Treat those over any assumption.

State verified 2026-07-26, session f8628411. humanise-copy v0.3.0 SHIPPED and PUBLISHED - main at c41694c (work at 554a4bf, bump at c41694c), 46 tests, repair-artifact checks 12 to 16 plus the claude-seo answer-engine routing signal, read-aloud gate now a required verdict line. Both marketplace listings updated in lockstep and pushed (outfit 508bb45, ai-loadout c52c87f). The INSTALLED plugin cache was fast-forwarded and functionally verified at 0.3.0, though its directory is still named 0.2.0 until a `/plugin` update tidies it. Ascot C&I demo redeployed and live-verified at https://pmw-ascot-ci.pages.dev. Machine-wide, OMC telemetry is fixed at source via OMC_STATE_DIR in ~/.claude/settings.json plus ~/.gitignore_global, and 162 .omc dirs are archived at ~/.claude/archive/omc-2026-07-25/. ALL OF THAT IS DONE AND TRUSTED - do not re-audit.

OPEN, ranked: (1) pro-marketing-web-agency stack-2026 has uncommitted C&I work needing a commit decision, mine (copy/HOMEPAGE-copy.md, homepage-demo/index.html) alongside the parallel session's untracked files - coordinate before committing; (2) the three-way "drawings" phrasing, ready to price vs Alex's suitable for pricing; (3) pro-marketing-ads-project/.omc is tracked in git and needs git rm -r --cached; (4) consider porting the .astro and .json prose extraction into the plugin as a batch mode.

DO NOT TOUCH: the parallel session's untracked files on stack-2026 (copy/PROCESS-copy.md, homepage-demo/assets/site.css, homepage-demo/process/), listings and testimonials collections anywhere, About-the-author blocks, TL;DR blocks mirrored in Tina frontmatter, and the VOC discovery doc or transcripts (they are records, never edited).

Standing rules: verify on the rendered artifact never a status line, and on a deploy use a cache-busted fetch plus the deployment-specific URL if the apex looks stale; Sonnet subagents for fan-outs, chunk of 3; never push unasked; commit, push, merge, tag, deploy and version bumps are separate gos; archive over delete; no em or en dashes, no colons in headings, straight quotes; null-delimit any bulk path operation, 25 of Julian's paths contain spaces.

First action: read the handoff, then ask Julian whether to commit the stack-2026 C&I copy changes or leave them for the parallel session.
