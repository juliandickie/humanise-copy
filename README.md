# humanise-copy

Claude Code plugin that finds and repairs the tell-tale signs of AI generation
in written content while preserving the active brand voice. Two-tier detection
(phrase and lexical, then structural and rhythmic), voice-preserving repair
with a whitelist for deliberate technique, mechanical hygiene, and a measured
verify loop: no clean detector report, no "done".

## Status

v0.3.0, public at github.com/juliandickie/humanise-copy (MIT), listed in the
outfit and loadout marketplaces. The spliced-subject-triad check, read-aloud
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
    test_detect.py                   # 46 tests pinning detector to ground truth
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

46 tests pin the detector to the planted fixture (inventory in
`tests/EXPECTED-FINDINGS.md`) plus a clean human-shaped sample that must pass
every layer. Two of them are characterization tests that pin the blind spots
the repair-artifact checks exist to cover: chopped copy scores 1.09 on
burstiness against a 0.30 floor, and four consecutive "Ask" sentences score
16.4 percent on document-wide opening-word share against a 25 percent limit.
Both pass every older check. If either starts failing, the check it justifies
needs re-reading, not deleting. End-to-end verification: a Sonnet agent following the skill took
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
2. Run a `/plugin` update in an interactive session. The installed cache
   holds 0.3.0 and was verified functionally, but its directory is still
   named 0.2.0. The update lays down a clean directory and regenerates the
   install manifest.

Shipped and needing nothing further: v0.3.0 published, the public repo and
MIT licence, both marketplace listings updated in lockstep, the copy-school
handoff row with its claude.ai upload, and the idd-writing-style pre-ship
section with its anthropic-skills redeploy.

## Attribution

Two-tier methodology adapted from the impeccable plugin v3.1.1 (Paul Bakaus,
Apache 2.0) by way of claude-blog (AgriciDaniel, MIT); phrase and trigger
lists derive partly from claude-blog's analyze_blog.py (MIT). Voice doctrine
follows the house style and idd-writing-style. The Copy School AI punch-up
process is reached by handoff and deliberately not reproduced here.
