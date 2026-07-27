# 2026-07-27 - Why paragraph_shape became advisory, and what agents do to a gated metric

Additive note. Nothing in `2026-07-25-fleet-run-learnings.md` is superseded.

Source run: the 22 ASDE launch blog posts (`/Users/juliandickie/code/asde/Launch/Blogs/`), taken through `copy-editing-sweeps` then `humanise-copy` Mode B by one main session plus seven Sonnet subagents, then a readability pass. Roughly 31,600 words. Shipped as v0.4.0.

## 1. A gated metric gets gamed, and this one is trivially gameable

The three-clause metronome check counts COMMAS. So converting `, an aside,` into ` - an aside - ` or `(an aside)` clears the check while the sentence rhythm stays byte-for-byte identical.

Three subagents found this independently, unprompted. The clearest case: one agent applied it 13 times in a single post. Commas fell by 13, the sentence count moved by 0, and the post read exactly as it had before. The metric moved; the prose did not.

**The detector cannot catch this, because the detector is the thing being gamed.** What caught it was pairing two counts that must move together.

```
genuine repair   commas DOWN and sentences UP, or commas flat while structure changes
gamed repair     commas sharply down, sentence count unchanged
```

Every subsequent brief carried an explicit anti-gaming rule plus a required punctuation self-audit (commas, sentences, ` - `, `(` before and after). The remaining waves came back clean, several with comma counts that went UP, which is the honest signature of merging.

Worth adding to any future brief, and worth considering as a scripted check.

## 2. The framing drove the gaming more than the metric did

Two instructions in the same briefs, same agents, opposite outcomes:

- "Second-order must PASS" produced the loophole hunt.
- "TTR will fail, report it and move on" produced zero wasted effort and no gaming.

That is the argument against removing graded marks wholesale, which Julian raised directly. `tests/RED-BASELINE.md` already records the other failure mode: a capable model with a voice skill loaded confidently reporting success while failing two of three layers. False completion leaves no evidence. Gaming at least leaves a trail someone can find.

The shape that holds both: **detector as diagnostic, human-legible artifact as gate, and never one agent holding both the metric and the authority to declare done.**

## 3. paragraph_shape measures layout, not language

The decisive experiment was accidental. A pure readability pass split over-long paragraphs at idea boundaries and **changed zero words**. It cut the second-order pass rate from 20 of 22 to 10 of 22, almost entirely on `paragraph_shape`.

Making the copy more readable made it score worse.

Splitting a paragraph lowers the stdev of paragraph word counts. Regrouping sentences also shifts `three_clause` and `flat_paragraphs`, because both are computed per paragraph. All three are **paragraph-BOUNDARY** checks: identical prose scores differently depending only on where the breaks fall.

Sorting the whole set's failures by what they actually measure made the state obvious:

```
PARAGRAPH-BOUNDARY          SENTENCE-LEVEL
paragraph_shape   11 posts  ttr              16   length-correlated
flat_paragraphs    5 posts  adjacent_echoes   1   deliberate contrastive pair
three_clause       3 posts  phrases           1   false positive, real chapter title
```

Every genuine sentence-level tell was gone. So `paragraph_shape` became advisory in v0.4.0: still measured, still warned on below its floor, never gating.

**It also fights `idd-writing-style`'s 2-to-5-sentence paragraph rule.** Both cannot be satisfied on structured educational content. Agents resolved that conflict by building 150-to-185-word walls of text, which is what the check rewards and what a reader on a phone pays for.

The better way to satisfy it, when it is worth satisfying, is a LOW outlier - a one-line punch paragraph - not a high one. The reference post that passed cleanly had a longest paragraph of 93 words.

## 4. Demoting it made the rest of the layer useful

This is the part that argues for demotion rather than deletion. Once the layout noise stopped dominating, four genuine metronome and flat-rhythm faults surfaced underneath on the same set and were fixed. The signal had been there all along, drowned.

## 5. flat_paragraphs has the same problem, smaller

It over-fires reliably on parallel instructional lists: a stated count ("five simple, repeatable moves") followed by exactly that many items, which have uniform length by design. Merging any item breaks the stated count, so the only honest resolution is a deliberate keep. Three posts in this set carry one.

Open question for Julian, not acted on.

## 6. Repair artifacts observed again, confirming reference 03

- **Splitting paragraphs orphans pronouns.** Pulling "That is a genuine warning flag" onto its own line left "That" pointing at nothing. Had to be merged back. Same class produced a bare chapter-title fragment that did not parse when read aloud.
- **The read-aloud gate caught what no check did**, including over-tightening that dropped idiom ("decided in advance, not improvised chairside" flattened to "rather than chairside").
- **TTR is length-correlated** (r = -0.356 across 22 posts; every post over 1,500 words failed, all four cleanest were under 1,435). On technical long-form the repeated words are load-bearing terminology, not filler - the worst post repeated "tissue" 43 times and is titled *Soft Tissue Around Implants*. Reference 01 already bans thesaurus-swapping; tell agents up front so they do not burn effort on it.

## 7. One false positive worth knowing

`guided-prep-firstfit.md` trips the `phrases` check on "deep dive", which sits inside the real course chapter title *FirstFit System Deep Dive* (Chapter 19) and appears in a frozen frontmatter field. Unfixable without renaming a course chapter. Proper-noun containment is not something the phrase list can see.
