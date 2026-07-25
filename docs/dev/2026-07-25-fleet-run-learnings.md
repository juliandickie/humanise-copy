# Fleet-run learnings - 2026-07-25 (dated, additive)

First three production-scale runs of the skill (Ascot Homes + Scallywags demos,
Ascot C&I copy docs, Ascot RE production site): 106 + 87 surfaces measured,
~620 sentence repairs via eight Sonnet repair agents plus main-session ear QA.
Everything below is observed, not hypothetical.

FOLDED IN 2026-07-25 (same day, later session). Items 1 to 7 are now covered:
tic convergence, purpose-clause amputation, staccato and the two opener
patterns became mechanical checks 12 to 16 with regression tests built from
the sentences below; telegraphese, wrong connectives, danglers and
meaning-adjacent rewrites became numbered repair moves in reference 03,
because a stdlib check for them would need part-of-speech tagging and would
over-report. The read-aloud gate is now Mode B step 7 and a required line in
the verdict format. See the closing section of this note for what the
calibration and the with-guidance run found.

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

## Fold-in results (2026-07-25, later session)

Calibration, 16 files of already-accepted copy (the 14 repaired Ascot RE
insights plus the two C&I copy docs, about 19,000 words):

- Two findings total. Tics, purpose-clause amputation and staccato returned
  zero, so those three cost nothing in false positives.
- One finding initially read as a true positive, CORRECTED by Julian the same
  day: switch-property-managers-qld.md line 56 opens four consecutive
  sentences with "Ask" under the heading "What should I look for in a new
  property manager?". That is an answer block and the parallel imperatives
  are what make it extractable, so it is deliberate SEO and answer-engine
  optimisation, not a residual. The check now exempts content-word runs under
  question headings automatically (advisory warning, never a fail) and
  reference 02 carries the doctrine. Worth keeping: the fleet run's own
  "imperative-verb variety" fix is right for a run in ORDINARY prose and
  wrong for one in an answer block, and nothing in the note distinguished
  them until now. The document-wide opening-word share still read 16.4
  percent against a 25 percent limit, which remains a real blind spot for
  runs that are NOT answer blocks.
- One judgment-class over-report: "It is no longer 'can you find me a
  tenant'. It is 'who manages the tenancy well'." is a deliberate
  not-this-but-that pair, not an echo. Now documented in reference 02 under
  "Where these checks over-report".

With-guidance run, three fresh Sonnet agents on one draft built to tempt all
seven failure modes (three opener runs, 72.2 percent opening-word share, a
comma purpose clause, a flat paragraph):

- Three for three avoided every failure mode. No article amputation, no
  amputated purpose clause, no chop, no tic, no dangling reference, no
  meaning drift, no factual drift. All three filled the READ ALOUD line and
  used it substantively rather than as a checkbox.
- All three independently converged on the same prescribed moves: possessive,
  fronted clause and subject change for the opener runs, and the
  Request/Find out/Check/Confirm ladder for the "Ask" run. Convergence across
  independent reps is the signal that the wording binds; the baseline for
  comparison is the eight agents in this note who diverged into seven
  different failure modes without it.
- Closest call: one agent dropped articles in the stats sentence ("Vacancy
  sits near 1.0 percent, median rent has moved..."). Judged NOT telegraphese,
  because it read the client's own live copy first and matched its
  construction verbatim. Voice-grounded article choices are not amputation,
  and the distinction is worth keeping in mind if the check is ever
  mechanised.
