# humanise-copy

Claude Code plugin that finds and repairs the tell-tale signs of AI generation
in written content while preserving the active brand voice. Two-tier detection
(phrase and lexical, then structural and rhythmic), voice-preserving repair
with a whitelist for deliberate technique, mechanical hygiene, and a measured
verify loop: no clean detector report, no "done".

## Status

v0.5.0, public at github.com/juliandickie/humanise-copy (MIT), listed in the
outfit and loadout marketplaces.

0.5.0 makes `flat_paragraphs` advisory too, finishing what 0.4.0 started.
`ADVISORY_CHECKS` now holds both paragraph-boundary checks, and the rule behind
the set is explicit: **gate on the signals that measure the prose, report the
signals that measure the layout.** `flat_paragraphs` measures the spread of
sentence lengths inside a paragraph, and over-fires on parallel instructional
lists - a stated count ("five simple, repeatable moves") followed by exactly
that many items, uniform by design. Merging any item breaks the stated count,
so the only honest resolution was a deliberate keep, which means the check was
asking for an edit that must not be made. On the same 22-post ASDE set,
demoting it took second-order from 19 of 22 to 21 of 22, and the two posts it
freed were both logged deliberate keeps. The one post still failing does so on
`adjacent_echoes`, a genuinely different and separately documented keep - so
the demotion resolved exactly the over-firing it targeted and left the
unrelated residual visible, which is the outcome you want from a demotion.

Guarding against the obvious risk: every check moved into `ADVISORY_CHECKS`
narrows what can fail, and a detector that cannot fail manufactures false
confidence. The reference AI-slop fixture still fails second-order on 12 gating
tells at 0.5.0, and `test_demotion_left_the_layer_with_real_teeth` now asserts
a floor of 8, so a deliberate demotion stays easy and an accidental gutting
does not.

0.4.0 makes `paragraph_shape` advisory. It is still measured, reported, and
warned on when it sits below its floor, but it no longer fails a layer or trips
`--gate`. The evidence is a 22-post long-form set (ASDE launch blogs,
2026-07-27) where a pure readability pass, splitting over-long paragraphs at
idea boundaries and **changing zero words**, cut the second-order pass rate
from 20 of 22 to 10 of 22 almost entirely on this one check. It measures the
spread of paragraph word counts, so it tracks where breaks fall rather than how
the prose reads, and it pulls against house styles that cap paragraphs at 2 to
5 sentences. Demoting it also made the remaining signal actionable rather than
drowned: four genuine metronome and flat-rhythm faults surfaced underneath on
that same set and were fixed. Mechanism is the `ADVISORY_CHECKS` frozenset in
`scripts/detect.py`; doctrine is in reference 02 under "The paragraph-boundary
checks are advisory, not gates". The generalisation worth carrying to any check added
later: separate the signals that measure the prose from the signals that
measure the layout, and only gate on the first group. Full write-up, including
how three subagents independently gamed the comma-counting three-clause check
and the counter-metric that caught them, is in
[docs/dev/2026-07-27-paragraph-shape-advisory.md](docs/dev/2026-07-27-paragraph-shape-advisory.md).

The spliced-subject-triad check, read-aloud
naturalness doctrine, and borderline warning band all came from the first day
of real-copy use. Proven at fleet scale 2026-07-25: ~200 copy surfaces
measured and ~620 sentence repairs across five client demo sites and the
Ascot RE production site (latest handoff SESSION-HANDOFF-2026-07-26.md,
kickoff NEXT-SESSION.md, prior SESSION-HANDOFF-2026-07-25.md and
docs/dev/2026-07-25-fleet-run-learnings.md). Both sibling-repo integrations
(copy-editing-sweeps handoff, idd-writing-style pre-ship pointer) are live.

That fleet run also produced the v0.3.0 work: repair is itself a generation
pass, and every check the detector had measured the draft rather than the
repair. Eight agents passed the detector and still shipped telegraphese,
converged tics, chop, and orphaned pronouns. Five of those failure modes are
now mechanical checks (12 to 16), the rest are repair moves in reference 03,
and the read-aloud gate is a numbered Mode B step plus a required line in the
verdict format. Structure that is search and answer-engine optimisation is
routed to claude-seo rather than repaired, and the detector raises that flag
itself.

## Why it exists

Baseline testing showed that a capable model, even with a brand voice skill
loaded, removes the loud phrases and then confidently reports success while
still failing two of three detection layers: residual listed phrases, rhythm
tells recreated inside its own repairs, and the statistical patterns
(opening-word share, paragraph-shape uniformity) no read-through can see.
Evidence and numbers in [tests/RED-BASELINE.md](tests/RED-BASELINE.md).

## Layout

```
humanise-copy/
  .claude-plugin/plugin.json
  skills/humanise-copy/
    SKILL.md                          # Modes, non-negotiables, verdict format
    references/
      01-first-order-tells.md        # Phrase families, lexical metrics
      02-second-order-tells.md       # Structural patterns, asset-aware thresholds
      03-voice-preserving-repair.md  # Voice sources, whitelist mechanic, fabrication boundary
      04-mechanical-hygiene.md       # House-style character rules, always last
  scripts/detect.py                  # Stdlib detector, JSON or markdown reports
  tests/
    fixtures/idd-draft-sloppy.md     # Planted fixture (violates house style BY DESIGN)
    EXPECTED-FINDINGS.md             # Plant inventory / ground truth
    RED-BASELINE.md                  # What a capable model does without the skill
    test_detect.py                   # 62 tests pinning detector to ground truth
  README.md
```

## Usage

Once installed as a plugin, requests like "humanise this draft", "does this
read as AI", or "de-AI this post" trigger the skill. Until then, point a
session at `skills/humanise-copy/SKILL.md` and have it follow Mode A
(detect-only report), Mode B (fix, the default), or Mode C (pre-ship gate).

Detector on its own:

```bash
python3 scripts/detect.py FILE.md --format markdown
```

```bash
python3 scripts/detect.py FILE.md --gate
```

`--gate` exits 1 on any failing layer, for CI or scripted pipelines. The
script measures and reports with line numbers; the skill layer judges what is
a tell versus deliberate voice.

## Tests

```bash
python3 -m unittest discover tests -v
```

62 tests pin the detector to the planted fixture (inventory in
`tests/EXPECTED-FINDINGS.md`) plus a clean human-shaped sample that must pass
every layer. Two of them are characterization tests that pin the blind spots
the repair-artifact checks exist to cover: chopped copy scores 1.09 on
burstiness against a 0.30 floor, and four consecutive "Ask" sentences score
16.4 percent on document-wide opening-word share against a 25 percent limit.
Both pass every older check. If either starts failing, the check it justifies
needs re-reading, not deleting. Fifteen more pin the two paragraph-boundary
checks as advisory. A document with deliberately uniform paragraph lengths
scores 1.4 against a floor of 25 and must still return second-order PASS; a
document whose only fault is a parallel five-item instruction list must do the
same on `flat_paragraphs`, and each of those fixtures asserts that it isolates
its own check, or the demotion tests would pass for the wrong reason. Against
that, the planted fixture must still fail second-order on its genuine gating
tells, and `test_demotion_left_the_layer_with_real_teeth` holds a floor of 8
such tells so `ADVISORY_CHECKS` cannot be grown until the detector stops
detecting. End-to-end verification: a Sonnet agent following the skill took
the fixture from triple-FAIL to triple-PASS, kept all six whitelisted voice
items including the "Here's the thing" signature-phrase trap, and used the
verdict format with real detector output. The fixture violates house style on
purpose; never "fix" it.

## Pipeline position

Draft in the active voice (idd-writing-style, a client VOICE.md, a 10x
writing skill), then content and conversion editing (copy-editing-sweeps),
then humanise-copy, then ship. Always last; any later edit reopens the pass.

## Integrations

- `copy-school/10x-copywriting` - sister-skill handoff row added to
  copy-editing-sweeps pointing here as the post-sweep final pass. Committed
  2154097, the zip rebuilt with the row at ed8eb13, and uploaded to
  claude.ai. Nothing outstanding.
- `idd-writing-style` - "Pre-Ship QA - AI Tells" section added, with the
  signature-phrase whitelist stated explicitly. Committed 5bd356a and
  7b7b1b5, the skill bundle rebuilt, and the anthropic-skills live copy
  redeployed. Nothing outstanding.

## Next steps (each needs Julian's explicit go)

1. Consider porting the .astro and .json prose extraction into the plugin as
   a first-class batch mode (the fleet run's extractor lived in a session
   scratchpad and died with it).
2. **Push and release 0.5.0.** The `flat_paragraphs` demotion is committed on
   `main` locally with 62 tests green, and held there because this repo has no
   `handoff:` policy line. One `git push origin main` when you want it.
3. Run a `/plugin` update in an interactive session. The installed cache was
   fast-forwarded to 0.4.0 and verified (54 tests at the time, advisory
   behaviour live), but its directory is still named 0.2.0 and it does not yet
   carry 0.5.0. Cosmetic plus one version behind; the update lays down a clean
   directory and regenerates the install manifest.

Shipped and needing nothing further: v0.4.0 published (310d673 on main) with
its dev-docs evidence note (fd2552d), the public repo and MIT licence, the
copy-school handoff row with its claude.ai upload, and the idd-writing-style
pre-ship section with its anthropic-skills redeploy. Both marketplace listings
needed no edit for 0.4.0 or 0.5.0, because they carry no version and track the
repo URL, and their descriptions do not mention the checks that changed.

## Attribution

Two-tier methodology adapted from the impeccable plugin v3.1.1 (Paul Bakaus,
Apache 2.0) by way of claude-blog (AgriciDaniel, MIT); phrase and trigger
lists derive partly from claude-blog's analyze_blog.py (MIT). Voice doctrine
follows the house style and idd-writing-style. The Copy School AI punch-up
process is reached by handoff and deliberately not reproduced here.
