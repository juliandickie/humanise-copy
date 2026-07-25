# Fleet-run learnings - 2026-07-25 (dated, additive)

First three production-scale runs of the skill (Ascot Homes + Scallywags demos,
Ascot C&I copy docs, Ascot RE production site): 106 + 87 surfaces measured,
~620 sentence repairs via eight Sonnet repair agents plus main-session ear QA.
Everything below is observed, not hypothetical. TODO: fold the failure modes
into references/03 and SKILL.md Common Mistakes (open work item 1).

## Repair-agent failure modes (all detector-invisible, caught only by ear)

1. Dropped-article telegraphese - agents dodge opening-word counts by
   amputating articles ("The buyer pool includes" becomes "Buyer pool here
   includes"). A worse tell than the one being fixed. Rule: vary openers with
   possessives, subordinate fronting, or subject changes, never amputation.
2. Tic convergence - two agents independently adopted "Honestly," as their
   replacement opener across files. Repair vocabulary must vary per file; a
   brief line naming the banned tic prevents it.
3. Amputated purpose clauses - ", so the team can support them" split into a
   standalone "So the team can support them." which reads broken. Consequential
   "So X" sentences are fine; purpose clauses must stay attached or become
   "That way, ...".
4. Wrong connectives from splitting - "and again only if" became "Then again,
   only if" (idiomatically "on the other hand"). Meaning check every split.
5. Staccato over-splitting - trading metronome for chop ("Then this is the
   category."). The read-aloud gate catches it.
6. Local echoes and danglers - consecutive "This guide... This guide", a
   dangling "These priorities" with no antecedent, an appositive drifting to
   the wrong noun. Agents edit sentence-locally; QA must read paragraphs.
7. Meaning-adjacent rewrites - "The practical point is simple" (sets up a
   simplification) became "it really is that simple" (asserts the prior
   paragraph was simple - false). Rhetorical function is part of meaning.

## What works

- Brief evolution: each wave's QA findings folded into the next wave's brief;
  the final agents of both fleets needed near-zero corrections. The naturalness
  rules block (no telegraphese, no tics, no amputated-So, read-aloud gate) is
  now standard brief material.
- Imperative-verb variety beats structural surgery for "Ask... Ask... Ask..."
  runs (Request / Find out / Check / Confirm / Insist / Put / Establish).
- Freeze-first briefs: naming the frozen classes (figures, law references,
  ratios, About-the-author, TL;DR-frontmatter mirrors, founding-year gates)
  produced zero factual drift across ~620 repairs.

## Detection calibration learned

- Extraction mirrors (.astro/.json string harvest) distort shape metrics (TTR,
  flat, paragraph SD, opening-word); trust only phrases, triads, hedges and
  hygiene on mirrors. Real markdown gets the full stack.
- Enumeration commas false-positive the three-clause check; appositives and
  "so it" causal tails false-positive the triad check at low rates. Judgment
  classes, documented in reference 02.
- Small-sample guards matter: one-line team bios trip burstiness; short docs
  trip opening-word (already gated at 15 sentences).
- Verbatim-repeated wrap-up questions and restated-pronoun splices were both
  promoted from observation to mechanical checks with regression tests - the
  pattern for future promotions: mechanical goes in the detector with a test,
  judgment goes in the references.

## Ops footguns

- Deploy verification: a 200 (even a deploy script's own verify) proves the
  site answers, not that it serves the new build. Cache-busted fetch of a
  changed sentence is the true check; Workers first-fetch and Pages
  branch-alias caches both bit this session.
- Wrangler upload profiles are free audits: "14 of 14 assets changed, 142
  already uploaded" independently confirmed the change surface.
- Unquoted heredocs mangle backslash escapes when writing code from bash;
  quote the delimiter.
