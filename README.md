# humanise-copy

Claude Code plugin that finds and repairs the tell-tale signs of AI generation
in written content while preserving the active brand voice. Two-tier detection
(phrase and lexical, then structural and rhythmic), voice-preserving repair
with a whitelist for deliberate technique, mechanical hygiene, and a measured
verify loop: no clean detector report, no "done".

## Status

v0.2.0, public at github.com/juliandickie/humanise-copy (MIT), listed in the
outfit and loadout marketplaces. The spliced-subject-triad check, read-aloud
naturalness doctrine, and borderline warning band all came from the first day
of real-copy use. Proven at fleet scale 2026-07-25: ~200 copy surfaces
measured and ~620 sentence repairs across five client demo sites and the
Ascot RE production site (see SESSION-HANDOFF-2026-07-25.md and
docs/dev/2026-07-25-fleet-run-learnings.md). Both sibling-repo integrations
(copy-editing-sweeps handoff, idd-writing-style pre-ship pointer) are live.

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
    test_detect.py                   # 15 tests pinning detector to ground truth
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

15 tests pin the detector to the planted fixture (inventory in
`tests/EXPECTED-FINDINGS.md`) plus a clean human-shaped sample that must pass
every layer. End-to-end verification: a Sonnet agent following the skill took
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
  copy-editing-sweeps pointing here as the post-sweep final pass
  (uncommitted in that repo; the pending claude.ai zip needs regenerating
  once committed)
- `idd-writing-style` - "Pre-Ship QA - AI Tells" section added, with the
  signature-phrase whitelist stated explicitly (uncommitted; the live copy
  runs from the anthropic-skills plugin cache and needs Julian's manual
  redeploy)

## Next steps (each needs Julian's explicit go)

1. git init, first commit, GitHub repo, registration in the private amh
   marketplace
2. Commit the copy-school handoff row; regenerate the claude.ai 10x zip
3. Commit the idd-writing-style section; redeploy the live anthropic-skills
   copy

## Attribution

Two-tier methodology adapted from the impeccable plugin v3.1.1 (Paul Bakaus,
Apache 2.0) by way of claude-blog (AgriciDaniel, MIT); phrase and trigger
lists derive partly from claude-blog's analyze_blog.py (MIT). Voice doctrine
follows the house style and idd-writing-style. The Copy School AI punch-up
process is reached by handoff and deliberately not reproduced here.
