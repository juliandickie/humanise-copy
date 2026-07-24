# RED Baseline - What a Capable Model Does Without This Skill

Recorded 2026-07-24. A Sonnet subagent was given the planted fixture
(`tests/fixtures/idd-draft-sloppy.md`) and asked to remove the tell-tale signs
of AI generation, with no access to this skill. It self-loaded the
idd-writing-style voice skill, so this baseline represents the realistic
starting point in this stack: capable model plus voice skill, no humanise-copy.

## What the baseline did well

- Removed 18 of 19 planted first-order phrase families
- Rewrote the question-cadence H2s to a 1-of-4 mix
- Collapsed both hedge stacks to single hedges
- Converted third-person drift back to first person
- Cut both verbatim wrap-up questions, all capsule transitions, both
  false-balance framings, and the key-insight opener
- Preserved all six whitelisted voice items (W1-W6), including "Here's the
  thing" (credit to the loaded voice skill)
- Passed mechanical hygiene (em dashes out, straight quotes)

## What survived or regressed, per the detector

| Check | Fixture | Baseline output |
|-------|---------|-----------------|
| First-order phrases | 19 distinct | 1 ("streamlines") - FAIL |
| Trigger-word density per 1k | 17.82 FAIL | 0.00 PASS |
| Question-cadence H2s | 4 of 4 FAIL | 1 of 4 PASS |
| "Here" openers | 3 FAIL | 2 at the limit, one of them generic filler |
| Three-clause metronome | 1 FAIL | 1 FAIL, recreated inside its own fix |
| Symmetric list | 1 FAIL | 1 FAIL, shapes varied but lengths still uniform |
| Flat paragraphs | 2 FAIL | 1 FAIL |
| Opening-word top-3 share | 41.7% FAIL | 39.0% FAIL |
| Paragraph-shape SD | 19.5 FAIL | 17.1 FAIL |
| Hygiene | FAIL | PASS |
| Overall | FAIL | FAIL |

## The five lessons this skill encodes

1. Models sweep phrases from memory, not from the list; residuals survive
   ("streamlines" stood in plain sight).
2. Models recreate rhythm tells inside their own repairs; the baseline
   reported the metronome paragraph as "the single most obvious AI tell,
   fixed" while its three replacement sentences kept the identical internal
   shape.
3. The statistical tells (opening-word share, paragraph-shape uniformity)
   are invisible to a read-through; only counting finds them.
4. Self-assessment without measurement produces confident false "done"
   reports; the baseline declared success while failing two of three layers.
5. A loaded voice skill protects signature phrases and register; it does not
   protect structure or statistics. Both passes are required.
