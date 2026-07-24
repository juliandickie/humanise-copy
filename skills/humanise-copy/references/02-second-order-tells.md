# Second-Order Tells - Structural and Rhythmic Layer

The patterns that survive a vocabulary swap. Models converge on safe structure
the way they converge on safe phrases; strip the words and the skeleton still
reads AI. This layer is what separates "phrase-clean" from "reads human".

`scripts/detect.py` computes every threshold below. The script measures; you
judge. Before repairing anything here, load
[03-voice-preserving-repair.md](03-voice-preserving-repair.md) and the active
voice skill, because several of these patterns are also legitimate techniques
when used deliberately (see the asset table at the end).

## The structural patterns

| # | Pattern | Flag at | Repair move |
|---|---------|---------|-------------|
| 1 | Question-cadence H2s - every heading a question | above 70% of H2s | Rewrite to a mix: statements, noun phrases, and a question only where the section genuinely answers one |
| 2 | "Here's..." paragraph openers | more than 2 | Check the voice whitelist FIRST (a signature "Here's the thing" stays); vary or delete the rest |
| 3 | Three-clause metronome - sentence after sentence shaped [clause], [clause], [clause] | half the sentences in a paragraph | Break the rhythm: cut one sentence to a fragment, let another run long, merge two |
| 4 | False-balance framing - "While X, also Y" with no real contrast | above 2 per 1,000 words | Keep only genuine contrasts; otherwise state the single true thing plainly |
| 5 | Hedge stacking - may, often, typically piled into one breath | more than 2 hedges in any 20-word window | Choose the one honest hedge and delete the rest. Measured is one qualifier, not three |
| 6 | Symmetric list bloat - every item the same length and shape | word-count SD below 5 across 3+ items | Vary depth by importance: small items get a line, the big item gets a short paragraph |
| 7 | Wrap-up questions - "What does this mean for you?" closing sections | more than 2 | Cut it, or actually answer it in the next sentence |
| 8 | Capsule transitions - sections opening "First,..." "Next,..." "Additionally,..." | above 50% of section openers | Bury the transition inside the sentence, or trust the heading to carry the sequence |
| 9 | Insight telegraphing - "The key insight is...", "What's important here is..." | any | Delete the frame, keep the insight. The sentence is stronger standing alone |
| 10 | Rhythmic flatness | flat paragraphs (sentence-length SD under 4), opening-word top-3 share above 25%, paragraph-shape SD under 25 on 8+ paragraphs | Vary deliberately: a one-line paragraph after a dense one, different sentence openers, unequal section weights |
| 11 | Spliced subject triads - "It runs..., it puts..., and it ends..." | the same pronoun subject restated 2 or more times across comma-spliced clauses in one sentence | Share the verbs under one subject ("It runs in a fixed order and puts everything in writing"), vary the subjects, or split the sentence |

## Manual checks the script skips

- Listicle intro bloat: more than roughly 250 words of context before the list
  the piece promised. Real listicles get to the list.
- Semantic false balance: the script pattern-matches "while ... also"; only a
  read tells you whether the contrast is real.
- Answer-shaped everything: if every section opens with a one-line answer
  followed by three support sentences, the piece was written to a template
  even if each section passes individually.
- Enumeration commas: the three-clause check counts commas, so a dense list
  of concrete specifics ("Flooding, sewer lines, easements, zoning") flags
  as metronome. Read the flagged paragraph; clause chains are a tell, lists
  of specifics are specificity doing its job.
- Read-aloud naturalness: over-tightened prose drops the small words a
  speaker keeps ("signed off on" clipped to "signed off", missing
  connectives and particles). Read the copy aloud; if a sentence cannot be
  said naturally the way it is written, restore the idiom. Editing past
  natural is itself a tell, and it hides in sentences no threshold flags.

## Asset-aware application

Structure that is a tell in one format is technique in another. Apply the
thresholds through this table, never raw.

| Asset | Adjustments |
|-------|-------------|
| Blog, educational, review | Full thresholds as listed above |
| Conversion copy (sales page, landing page, promo email) | Bucket brigades ("Here's the thing:", "But wait.") and deliberate anaphora are persuasion technique, not tells, when the active copy system prescribes them; parallel CTA lines and symmetric benefit bullets are exempt from #6; punchy fragments are voice, not flatness |
| Email (newsletter, lifecycle) | One wrap-up question can be the CTA; allow it before flagging #7 |
| LinkedIn and social | Short-line rhythm is native to the format; skip the flat-paragraph and paragraph-SD checks entirely |

If the piece came out of a 10x-copywriting skill, assume its repetition and
rhythm choices are deliberate until the sweep record says otherwise, and
confine repairs to patterns that system did not prescribe.

## Attribution

Pattern set and thresholds adapted from claude-blog's ai-slop-detection
reference (AgriciDaniel, MIT), itself an adaptation of the impeccable plugin's
first-order/second-order reflex methodology (Paul Bakaus, Apache 2.0).
