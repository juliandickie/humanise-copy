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

Read the GATES column before repairing anything. A check marked ADVISORY was
measured against human prose written before language models existed and did not
separate. It reports, it never fails a layer, and it is never on its own a
reason to edit a sentence. The evidence is in
`docs/dev/2026-08-05-clause-rhythm-checks-have-no-signal.md` and the summary is
under "What the advisory demotions mean" below.

| # | Pattern | Flag at | Gates | Repair move |
|---|---------|---------|-------|-------------|
| 1 | Question-cadence H2s - every heading a question | above 70% of H2s | yes | Rewrite to a mix: statements, noun phrases, and a question only where the section genuinely answers one |
| 2 | "Here's..." paragraph openers | more than 2 | yes | Check the voice whitelist FIRST (a signature "Here's the thing" stays); vary or delete the rest |
| 3 | Three-clause metronome - sentence after sentence shaped [clause], [clause], [clause] | half the sentences in a paragraph | ADVISORY | Do not repair on this number alone. It counts commas and never compares one sentence to another, so it cannot see the repetition its name describes |
| 4 | False-balance framing - "While X, also Y" with no real contrast | above 2 per 1,000 words | yes | Keep only genuine contrasts; otherwise state the single true thing plainly |
| 5 | Hedge stacking - may, often, typically piled into one breath | more than 2 hedges in any 20-word window | ADVISORY | Fires more on human prose than on AI drafts. If a real triple-hedge is there, keep the one honest qualifier; otherwise leave it |
| 6 | Symmetric list bloat - every item the same length and shape | word-count SD below 5 across 3+ items | yes | Vary depth by importance: small items get a line, the big item gets a short paragraph. Parallel CTA and benefit lists in conversion copy are exempt, see the asset table |
| 7 | Wrap-up questions - "What does this mean for you?" closing sections | more than 2 | yes | Cut it, or actually answer it in the next sentence |
| 8 | Capsule transitions - sections opening "First,..." "Next,..." "Additionally,..." | above 50% of section openers | yes | Bury the transition inside the sentence, or trust the heading to carry the sequence |
| 9 | Insight telegraphing - "The key insight is...", "What's important here is..." | any | yes | Delete the frame, keep the insight. The sentence is stronger standing alone |
| 10 | Rhythmic flatness | opening-word top-3 share above 25% (GATES, the strongest signal in this layer after paragraph shape); flat paragraphs, sentence-length SD under 4 (ADVISORY); paragraph-shape SD under 25 on 8+ paragraphs (ADVISORY) | mixed | Vary openers deliberately. For the two advisory members, vary only if the page genuinely looks uniform to a reader |
| 11 | Spliced subject triads - "It runs..., it puts..., and it ends..." | the same pronoun subject restated 2 or more times in one sentence, with at least one restatement at a genuine splice | ADVISORY | Share the verbs under one subject, vary the subjects, or split the sentence. A sentence conjoined at every juncture ("We carry X, and we review Y, so we can Z") is not a splice and is not a finding |

## What the advisory demotions mean

Nine checks report without gating. Two are layout checks (`paragraph_shape`
since 0.4.0, `flat_paragraphs` since 0.5.0). Seven more were demoted in 0.6.0
on measurement, after every second-order check was run over three human corpora
that pre-date language models (Austen 1817, Darwin 1859, fifteen Paul Graham
essays 2004 to 2015) and over the labelled ASDE before-and-after blog set.

Fire rate on AI drafts against fire rate on untouched Paul Graham essays:

| Check | AI draft | Human | Result |
|---|---|---|---|
| three_clause_rhythm | 82% | 73% | no signal |
| adjacent_echoes | 41% | 53% | no signal |
| spliced_triads | 23% | 20% | no signal |
| repeated_openers | 23% | 20% | no signal |
| staccato_runs | 18% | 47% | inverted |
| amputated_purpose | 0% | 40% | inverted |
| hedge_stacking | 0% | 20% | inverted |

An inverted check fires MORE on human prose than on machine prose. Those three
were telling you to edit away the things that make writing read as human:
punch (`staccato_runs` fires on runs of three-word sentences), ordinary
discourse "So" (`amputated_purpose` fires on "So you could say that using Lisp
was an experiment"), and honest qualification.

`three_clause_rhythm` is the one that caused the 4 August review. It counts
commas, never compares one sentence to another, and so cannot detect a
metronome, which by definition is repetition. A narrowed rewrite keying on true
clause boundaries, matched sentence lengths and consecutive runs was built and
swept across the whole parameter space: the best separation available anywhere
was plus 0.05, and several settings inverted at up to minus 0.77. There is no
threshold to raise it to, because clause density tracks how considered the
prose is, not who wrote it.

Beware the shape of the evidence that made it look valid. On the 27 July blog
set the check separated 18 of 22 before against 0 of 22 after, which looks
perfect and is Goodhart's law. A repaired corpus sitting at 0.0% against a
human baseline of 7% is not clean, it is over-edited, and the flagged sentences
had survived byte for byte while agents padded the paragraph until the
denominator cleared the gate. When a gated metric goes to zero, suspect the
gate.

**What none of this means.** All nine still measure, still report, still warn.
A genuinely metronomic run of sentences is still a real tell. What changed is
who decides: a human reading the warning, not a build failing on a number.

## The paragraph-boundary checks in particular

`paragraph_shape` and `flat_paragraphs` are computed per paragraph, so
identical prose scores differently depending only on where the breaks fall.

`paragraph_shape` is the standard deviation of paragraph WORD counts, so it
responds to where the paragraph breaks fall, not to how the sentences read.
Move a break and the score moves, with the prose untouched.

That makes it uniquely easy to satisfy the wrong way and uniquely easy to fail
the right way. Measured on a 22-post long-form set: a pure readability pass that
split over-long paragraphs at idea boundaries, **changing zero words**, cut the
second-order pass rate from 20 of 22 to 10 of 22, essentially all of it on this
one check. The same run's agents, chasing the floor, had produced 150 to 185
word walls of text, which is what the check rewards and what a reader on a phone
suffers for.

It also pulls against house styles that cap paragraphs at 2 to 5 sentences
(idd-writing-style does). Both cannot be satisfied on structured educational
content.

So the detector reports it, warns when it sits below the floor, and does not let
it fail a layer on its own. Read it as a prompt: if the score is low AND the
paragraphs genuinely all look the same on the page, vary them, preferring a
short one-line punch paragraph (a low outlier) over a wall of text (a high one).
If the score is low because you just made a dense page readable, that is the
check doing what it does, and you should ignore it.

`flat_paragraphs` is the same problem one level down. It is the standard
deviation of SENTENCE lengths inside a paragraph, and it over-fires on parallel
instructional lists: a stated count ("five simple, repeatable moves") followed
by exactly that many items, uniform in length because that is the technique.
Merging any item breaks the stated count, so the only honest resolution is a
deliberate keep, which means the check was asking for an edit that must not be
made. Read it the same way: if a run of sentences is flat AND nothing structural
is forcing it, vary the lengths; if the flatness IS the parallel, keep it and
move on.

When the layout noise was removed from the 22-post set, four genuine metronome
and flat-rhythm faults surfaced underneath and were fixed, which is the argument
for demoting these rather than deleting them.

The general lesson is worth carrying to any check added later, and 0.6.0
rewrote it. The original split was prose signals against layout signals, and it
put staccato runs, spliced triads, repeated openers and adjacent echoes in the
trustworthy group. Measurement put all four in the untrustworthy one. The line
that actually holds is different:

- **Checks that discriminate** measure what a writer does not consciously
  control across a whole document. Word choice (trigger phrases, trigger
  density) and document-scale distribution (opening-word share, paragraph
  shape). A writer cannot feel that 26% of their sentences open on the same
  three words.
- **Checks that do not discriminate** measure sentence-level craft. Clause
  density, sentence length, comma placement, local repetition. That is exactly
  what a good writer varies on purpose and what a careful reader notices first,
  which is why human prose scores like AI prose on all of it.

If a proposed check can be satisfied by editing one sentence, it is probably in
the second group. Measure it against a human corpus before it is allowed to
gate anything.

## Repair artifacts

Checks 1 to 11 measure the draft. The five below measure the repair, so they
earn their keep on the re-run in Mode B step 7 rather than the first pass.
Every one of them came from watching eight agents repair real copy, pass the
detector, and still leave damage an ear caught
([03-voice-preserving-repair.md](03-voice-preserving-repair.md) has the
repair moves that prevent them).

Only check 12 still gates. The other four were demoted in 0.6.0 on the corpus
evidence above, and 13 and 14 fire more on human prose than on machine prose.
They are still the right things to LOOK for on a re-run; they are no longer
things a number can decide.

| # | Pattern | Flag at | Gates | Repair move |
|---|---------|---------|-------|-------------|
| 12 | Repeated candour openers - "Honestly," opening sentence after sentence | the same opener more than twice in a file | yes | Vary it or cut it. One is register; three is a tic the writer cannot hear because each edit looked fine alone |
| 13 | Amputated purpose clauses - "So the team can support them." standing alone | a sentence opening "So" plus a subject plus an ability modal | ADVISORY | Reattach it to the sentence it serves, or recast as "That way, ...". Read the sentence before it first: the check cannot tell a severed purpose clause from an ordinary discourse "So", and it fires on 40% of human essays |
| 14 | Staccato runs - chop traded for metronome | 3 or more consecutive sentences of 6 words or fewer | ADVISORY | Merge two, or let one run long, but only if the run is genuinely chop. Short runs are a human signature: this fires on 47% of Paul Graham essays and 18% of AI drafts. Burstiness, flat-paragraph SD and paragraph-shape SD all IMPROVE when copy is chopped, so no variance check can see the difference either |
| 15 | Repeated sentence openers - "Ask for... Ask how... Ask whether..." | 3 or more consecutive sentences on one first word, second words varying, NOT inside an answer block | ADVISORY | Vary the verb (Request, Find out, Check, Confirm, Insist, Establish). Identical second words are anaphora and are left alone. See the answer-block exemption below before repairing anything under a question heading |
| 16 | Adjacent echoes - "This guide... This guide..." | a pair of consecutive sentences sharing their first two words | ADVISORY | Pronoun the second, or restructure it. A run of 3 or more is anaphora and is not flagged. Contrastive and parallel pairs ("They want X. They want Y.") are technique and stay |

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
