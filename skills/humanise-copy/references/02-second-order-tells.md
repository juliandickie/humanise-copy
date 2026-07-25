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

## Repair artifacts

Checks 1 to 11 measure the draft. The five below measure the repair, so they
earn their keep on the re-run in Mode B step 7 rather than the first pass.
Every one of them came from watching eight agents repair real copy, pass the
detector, and still leave damage an ear caught
([03-voice-preserving-repair.md](03-voice-preserving-repair.md) has the
repair moves that prevent them).

| # | Pattern | Flag at | Repair move |
|---|---------|---------|-------------|
| 12 | Repeated candour openers - "Honestly," opening sentence after sentence | the same opener more than twice in a file | Vary it or cut it. One is register; three is a tic the writer cannot hear because each edit looked fine alone |
| 13 | Amputated purpose clauses - "So the team can support them." standing alone | a sentence opening "So" plus a subject plus an ability modal | Reattach it to the sentence it serves, or recast as "That way, ..." |
| 14 | Staccato runs - chop traded for metronome | 3 or more consecutive sentences of 6 words or fewer | Merge two, or let one run long. Note that burstiness, flat-paragraph SD and paragraph-shape SD all IMPROVE when copy is chopped, so no variance check can see this |
| 15 | Repeated sentence openers - "Ask for... Ask how... Ask whether..." | 3 or more consecutive sentences on one first word, second words varying, NOT inside an answer block | Vary the verb (Request, Find out, Check, Confirm, Insist, Establish). Identical second words are anaphora and are left alone. See the answer-block exemption below before repairing anything under a question heading |
| 16 | Adjacent echoes - "This guide... This guide..." | a pair of consecutive sentences sharing their first two words | Pronoun the second, or restructure it. A run of 3 or more is anaphora and is not flagged |

Checks 15 and 16 read the paragraph, not the document. The opening-word share
in check 10 is a document-wide percentage, so a run packed into one paragraph
hides inside a passing number: a 1,282-word page carrying four "Ask" sentences
back to back scored 16.4 percent against a 25 percent limit and passed.

## Answer blocks are exempt from check 15

Prose under a question heading is an answer block, the unit AI search lifts.
The claude-seo skills are the authority here and both are explicit: seo-content
lists "answer-first formatting for key questions" and "clear question-answer
formats, definition patterns, and step-by-step instructions that AI systems can
extract and cite" as citation-readiness signals, and seo-geo targets
self-contained blocks of 134 to 167 words that survive extraction without
surrounding context. A parallel imperative run is what makes such a block
liftable, so "Ask for... Ask how... Ask whether..." under "What should I look
for in a new property manager?" is the structure working, not a tell.

The detector applies this automatically. A run under a question heading is
recorded and warned on, never failed, and the warning exists because the
exemption is conditional on the block being written well.

Two limits keep the exemption honest.

- It needs a content word. A run sharing a determiner or pronoun ("The
  software... The technology... The platform...") is rhythm collapse and stays
  a fail even under a question heading, because a repeated "The" is never an
  extraction pattern.
- It covers one block, not a habit. seo-content lists "repetitive structure
  across pages" as a low-quality AI marker in its own right, so the two skills
  agree on the line: parallel structure INSIDE a bounded answer block is
  optimisation, the same shape as the page's ambient rhythm or repeated
  template-wise across a site is the tell. Judge the run against the rest of
  the piece, not just its own paragraph.

Where the two skills genuinely pull against each other, claude-seo owns the
answer-block decision and this skill owns whether the sentences read like a
person wrote them. Neither overrides the other; both have to pass.

## Where these checks over-report

Judgment classes, observed on real copy. The script cannot tell these from the
real thing, which is why it reports rather than decides.

- Contrastive pairs read as adjacent echoes. "It is no longer 'can you find me
  a tenant'. It is 'who manages the tenancy well'." is a deliberate
  not-this-but-that construction where the repetition carries the contrast.
  Keep it.
- Bucket brigades read as candour tics. "Look," and "Here's the thing" are
  prescribed technique in conversion copy and iDD voice respectively. Whitelist
  before cutting, as always.
- Instructional and parallel benefit copy repeats opening verbs on purpose.
  Numbered steps and CTA stacks are meant to sound the same.
- Punch is not staccato. Conversion copy and social both use short runs
  deliberately; social skips the flatness checks entirely per the asset table,
  and check 14 goes with them.
- A genuinely consequential "So we can finally stop guessing." carries an
  ability modal and will flag under check 13. Read the sentence before it: if
  nothing there is what the clause attaches to, it is doing its own work and
  stays.

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
| SEO and answer-engine content (question-heading pages, FAQ sections, "questions to ask" blocks) | Question-cadence H2s are the point, so read #1 as a ceiling on the whole page rather than a fault per heading; parallel imperative runs inside an answer block are exempt from #15 (handled automatically); keep blocks self-contained so they survive extraction. claude-seo's seo-geo and seo-content skills are the authority on what the block needs to do |

If the piece came out of a 10x-copywriting skill, assume its repetition and
rhythm choices are deliberate until the sweep record says otherwise, and
confine repairs to patterns that system did not prescribe.

## Attribution

Pattern set and thresholds adapted from claude-blog's ai-slop-detection
reference (AgriciDaniel, MIT), itself an adaptation of the impeccable plugin's
first-order/second-order reflex methodology (Paul Bakaus, Apache 2.0).
