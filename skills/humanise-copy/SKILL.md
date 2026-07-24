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
whitelist mechanic below) and quote the flagged lines. Deliver the report with
the verdict format at the end of this file.

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
7. Verify: re-run the detector. Repeat repair passes until every layer
   passes or every residual is a logged deliberate keep. The before and
   after reports both go in the delivery note.

### Mode C - Verify (pre-ship gate)

Detector run plus an eyes-on read for the manual checks the script skips
(listed in reference 02). Close with an explicit verdict: ship, or do not
ship until the named fixes land. Never "looks mostly good".

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
6. Any edit after the hygiene pass reopens the hygiene pass.

## Common Mistakes

Every entry below was observed in baseline testing against the planted
fixture; none is hypothetical.

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

## Verdict Format

```
DETECTOR   first-order PASS/FAIL | second-order PASS/FAIL | hygiene PASS/FAIL
DELIBERATE KEEPS  [flagged items kept, with the voice or technique source]
RESIDUALS  [anything still failing and why it is acceptable, or empty]
VERDICT    ship / do not ship until [named fixes]
```

## Handoffs

- Conversion-copy quality beyond AI tells: copy-editing-sweeps (it hands
  back here as its final pass)
- iDD voice authority: idd-writing-style
- Client voice missing or thin: brand-voice:generate-guidelines, then
  brand-voice:enforce-voice
- The words should come from customers: voc-research
- Full blog scoring (SEO, E-E-A-T, citation readiness): claude-blog's
  /blog analyze; its AI-risk layer overlaps this skill's detector
- AI slop in code: oh-my-claudecode:ai-slop-cleaner

## Attribution

The two-tier methodology adapts the impeccable plugin v3.1.1 (Paul Bakaus,
Apache 2.0) by way of claude-blog (AgriciDaniel, MIT). Phrase and trigger
lists derive partly from claude-blog's analyze_blog.py (MIT). Voice doctrine
follows Julian Dickie's house style and the idd-writing-style skill; the humor
punch-up process referenced via copy-editing-sweeps remains Copy School IP and
is deliberately not reproduced here.
