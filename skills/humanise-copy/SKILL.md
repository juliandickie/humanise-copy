---
name: humanise-copy
description: Use when written content needs the tell-tale signs of AI generation found or removed before shipping - an AI-assisted draft that "reads like AI", requests to humanise or humanize copy, de-AI a piece, check for AI slop in prose, make writing sound human, or run a final AI-tell QA pass after a voice or copy skill. Covers blogs, emails, sales and landing pages, web copy, social posts, and client deliverables.
---

# Humanise Copy

## Overview

Two-tier detection plus voice-preserving repair. The first tier catches the
phrases everyone knows ("delve into", "game-changer"); the second catches the
structural and statistical patterns that survive a vocabulary swap and that no
read-through can see. Repair always moves toward the active brand voice, never
toward neutral, because neutral is itself the tell.

The measurement loop is the skill. A capable model with a voice skill loaded
still fails two of three detection layers while confidently reporting success
(see `tests/RED-BASELINE.md`). Judgment decides what to fix; only the detector
decides whether it is fixed.

## When to Use

- A draft was AI-assisted and needs its fingerprints removed before shipping
- Someone asks whether a piece "reads as AI" and wants evidence, not vibes
- Final QA gate after idd-writing-style, a brand voice profile, or
  copy-editing-sweeps has done its work
- Auditing published content for AI tells

When NOT to use:

- Code cleanup: that is oh-my-claudecode:ai-slop-cleaner, which shares the
  word "slop" and nothing else; it refactors software, not prose
- The piece has strategy or quality problems (wrong reader, weak proof,
  unclear offer): copy-foundations and copy-editing-sweeps fix those first;
  humanising a strategically broken draft polishes the wrong thing
- No voice source exists yet: run brand-voice:generate-guidelines or
  voc-research first, or ask whose voice the piece belongs to

## Pipeline Position

Always last, and re-run after any later edit.

1. Draft in the active voice (idd-writing-style, a client VOICE.md, a 10x
   writing skill)
2. Content and conversion editing (copy-editing-sweeps for conversion assets)
3. humanise-copy: detect, repair, hygiene, verify
4. Ship

Running this pass before content edits wastes it; every subsequent edit can
reintroduce tells, and the baseline evidence shows repairs themselves regress.

## The Three Modes

### Mode A - Detect (report only)

Run the detector, annotate the results, give a verdict. No edits.

```bash
python3 scripts/detect.py THE-FILE.md --format markdown
```

Then annotate: mark every flagged item as tell or deliberate (see the
whitelist mechanic below) and quote the flagged lines. If the file mixes
production notes with page copy (a copy doc with a drafting header), judge
flags only against the copy that ships. The report may end with a Borderline
section, checks that passed but landed close to their gate; read those lines
aloud before shipping, they are where the last misses hide. Deliver the
report with the verdict format at the end of this file.

### Mode B - Fix (default)

1. Detect: run the detector, keep the report as the before-evidence.
2. Load the voice: identify whose voice the piece belongs to and load that
   source in full ([03-voice-preserving-repair.md](references/03-voice-preserving-repair.md)).
3. Whitelist: check every flagged item against the voice's signature phrases,
   the copy system's prescribed techniques, and format-native rhythm. Matches
   are kept and logged as deliberate.
4. Repair first-order tells in voice
   ([01-first-order-tells.md](references/01-first-order-tells.md)).
5. Repair second-order structure with asset-aware thresholds
   ([02-second-order-tells.md](references/02-second-order-tells.md)).
6. Hygiene pass, always last
   ([04-mechanical-hygiene.md](references/04-mechanical-hygiene.md)).
7. Read the repaired copy aloud, paragraph by paragraph. Repair is itself a
   generation pass and leaves its own tells; this is the only gate that
   catches telegraphese, chop, and references that stopped pointing anywhere
   ([03-voice-preserving-repair.md](references/03-voice-preserving-repair.md),
   "Repairing without introducing new tells").
8. Verify: re-run the detector. The re-run is where repair artifacts surface
   (reference 02, checks 12 to 16), so a first-pass FAIL that becomes a
   different FAIL is progress, not a loop. Repeat until every layer passes or
   every residual is a logged deliberate keep. The before and after reports
   both go in the delivery note.

### Mode C - Verify (pre-ship gate)

Detector run, an eyes-on read for the manual checks the script skips (listed
in reference 02), and the read-aloud pass. Close with an explicit verdict:
ship, or do not ship until the named fixes land. Never "looks mostly good".

If the piece reached you already repaired, treat checks 12 to 16 as the ones
most likely to fire: they measure the repair rather than the draft.

## When to consult claude-seo

Some structure that reads as a tell is search and answer-engine optimisation
doing its job. The detector raises `consult_claude_seo` in the borderline
section when a document looks answer-engine shaped (half or more of its H2s
are questions, with two or more answer blocks under them). Treat that flag,
or any of the triggers below, as a stop before repairing:

- Question-cadence headings on an FAQ, a "questions to ask" page, or any page
  built to be quoted by AI search. Check 1 still reports the percentage
  honestly, because nothing structural separates a real answer-engine page
  from a narrative article with rhetorical headings. Decide with claude-seo,
  then log it as a deliberate keep. Do not rewrite the headings to satisfy a
  threshold.
- Parallel imperative runs inside an answer block ("Ask for... Ask how...").
  Already exempt from check 15, and the exemption is the point.
- Any repair that would change heading structure, split an answer block, or
  push a block outside the citable length band.
- Location pages, service pages, and programmatic sets, where repetition
  across pages is deliberate template work rather than a repair artifact.

`claude-seo:seo-geo` owns passage citability and answer-block shape;
`claude-seo:seo-content` owns E-E-A-T and AI citation readiness. They decide
whether a structure is optimisation. This skill decides whether the sentences
read like a person wrote them. Both have to pass and neither overrides the
other; the full doctrine, including where the two genuinely disagree, is in
[02-second-order-tells.md](references/02-second-order-tells.md).

One caution from seo-content itself: it lists "repetitive structure across
pages" as a low-quality marker. So the exemption covers structure inside a
bounded answer block, never the page's ambient rhythm and never a template
tic repeated site-wide.

## Non-Negotiables

1. No clean detector report, no "done". Run it before and after; deliver
   both. Self-assessment without measurement produced confident false
   completion in baseline testing.
2. Load the voice source before repairing. Every replacement is written in
   that voice and spelling (iDD US, Pro Marketing AU, AU/NZ courses AU/NZ).
3. Whitelist before delete. The detector reports; it never decides. A
   signature phrase deleted is a worse failure than a tell kept.
4. Never fabricate experience, numbers, anecdotes, or timeframes to make
   text feel human. Missing specifics are a question for the user, not an
   invention ([03-voice-preserving-repair.md](references/03-voice-preserving-repair.md)).
5. Thresholds are asset-aware. Apply them through the table in reference 02;
   technique a 10x skill prescribed is not a tell.
6. Advisory checks never fail a layer, and never on their own justify an edit.
   Nine of them now: `paragraph_shape` and `flat_paragraphs` measure layout
   rather than language, and `three_clause_rhythm`, `adjacent_echoes`,
   `spliced_triads`, `repeated_openers`, `staccato_runs`, `amputated_purpose`
   and `hedge_stacking` were demoted in 0.6.0 because they do not separate
   human prose from machine prose. The last three fire MORE on human writing
   than on AI drafts. Treat an advisory line as a prompt to read the passage,
   and repair only what your ear confirms (reference 02, "What the advisory
   demotions mean").
7. A green detector is not a finished piece, and a metric driven to zero is a
   warning. The 27 July run cleared `three_clause_rhythm` on all 22 posts by
   padding paragraphs until the denominator moved, leaving the flagged
   sentences untouched. If a number went to zero, check that the prose changed.
8. Any edit after the hygiene pass reopens the hygiene pass.

## Common Mistakes

Every entry below was observed, none is hypothetical. The first table came
from baseline testing against the planted fixture, the second from eight
agents running this skill over about 620 real sentence repairs.

### Detecting

| Mistake | Reality |
|---------|---------|
| "I removed the AI phrases" (from memory) | "streamlines" survived the baseline's phrase pass in plain sight. Sweep against the detector's list, not recall. |
| "I broke up the repetitive sentences" | The baseline regrouped four metronome sentences into three with the identical internal shape and called it fixed. The detector still failed it. Re-measure after every fix. |
| "I varied the list items" | Shapes varied, lengths stayed uniform (SD 3.1); the flag stood. Vary depth by importance, not just wording. |
| "It reads human now" | The baseline declared success while failing two of three layers. Reading your own repair is not verification. |
| "The count is at the limit, so it passes" | Two "Here" openers passed the gate and one was generic filler. Thresholds gate the verdict; judgment still fixes spotted filler. |
| "I varied the sentences" | 39% of the baseline's sentences still opened with the same three words. No eye catches this; the count does. |
| "The voice skill covered it" | Voice protects register and signature phrases. It does not touch opening-word share, paragraph-shape uniformity, or clause rhythm. Both passes are required. |
| Deleting everything the detector flags | "Here's the thing" is iDD signature voice. Whitelist first, then delete. |

### Repairing

| Mistake | Reality |
|---------|---------|
| "The detector passes, so the repair is done" | Every check the detector had measured the draft. Eight agents passed it and still shipped telegraphese, tics, chop and orphaned pronouns. Five of those are checks now; the read-aloud gate covers the rest. |
| "I varied the openers" | Agents varied them by deleting articles: "The buyer pool includes" became "Buyer pool here includes". Vary by restructuring (possessive, fronted clause, new subject). Amputation is the louder tell. |
| "I split the long sentence" | ", so the team can support them" became a standalone "So the team can support them." A purpose clause with a full stop is a fragment. Reattach it or recast as "That way, ...". |
| "Short sentences read as human" | Three or more short sentences running is chop, and burstiness, flat-paragraph SD and paragraph-shape SD all IMPROVE when you chop. The numbers will congratulate you for it. |
| "I only touched that one sentence" | Echoes, appositives drifting to the wrong noun and pronouns left without an antecedent all come from sentence-local edits. Read the paragraph, not the line. |
| "Same meaning, better rhythm" | "The practical point is simple" sets up a simplification; "it really is that simple" asserts the previous paragraph was simple. Rhetorical function is part of meaning. |
| "My replacement opener sounds natural" | It does, once. Two agents independently converged on "Honestly," across their files and neither could hear it, because each saw only its own work. |

## Verdict Format

```
DETECTOR   first-order PASS/FAIL | second-order PASS/FAIL | hygiene PASS/FAIL
ADVISORY   [advisory checks below their floor, with the judgement made, or none]
READ ALOUD [done, and what it caught, or what it confirmed clean]
DELIBERATE KEEPS  [flagged items kept, with the voice or technique source]
RESIDUALS  [anything still failing and why it is acceptable, or empty]
VERDICT    ship / do not ship until [named fixes]
```

READ ALOUD is a required line in Modes B and C. "Clean" is a valid value; a
missing line means the pass is not finished.

## Handoffs

- Conversion-copy quality beyond AI tells: copy-editing-sweeps (it hands
  back here as its final pass)
- iDD voice authority: idd-writing-style
- Client voice missing or thin: brand-voice:generate-guidelines, then
  brand-voice:enforce-voice
- The words should come from customers: voc-research
- Full blog scoring (SEO, E-E-A-T, citation readiness): claude-blog's
  /blog analyze; its AI-risk layer overlaps this skill's detector
- Whether a structure is answer-engine optimisation rather than a tell:
  claude-seo's seo-geo (passage citability, self-contained answer blocks) and
  seo-content (E-E-A-T, AI citation readiness). They own that call; this skill
  owns whether the sentences read like a person wrote them. Both have to pass,
  and neither overrides the other (reference 02, "Answer blocks are exempt
  from check 15")
- AI slop in code: oh-my-claudecode:ai-slop-cleaner

## Attribution

The two-tier methodology adapts the impeccable plugin v3.1.1 (Paul Bakaus,
Apache 2.0) by way of claude-blog (AgriciDaniel, MIT). Phrase and trigger
lists derive partly from claude-blog's analyze_blog.py (MIT). Voice doctrine
follows Julian Dickie's house style and the idd-writing-style skill; the humor
punch-up process referenced via copy-editing-sweeps remains Copy School IP and
is deliberately not reproduced here.
