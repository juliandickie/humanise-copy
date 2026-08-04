# 2026-08-05 - The clause and rhythm checks have no AI signal, measured

Additive note. It supersedes one conclusion in `2026-07-27-paragraph-shape-advisory.md` (section 1) and nothing else.

Trigger: during a Seven Sweeps pass over the ASDE launch broadcasts, the skill flagged B8, B9 and B10 for three-clause metronome rhythm and for stacking items before a verb. Julian read the flagged copy and ruled every example fine, then took the skill offline for review. This note is that review.

The short version. `three_clause_rhythm` does not measure rhythm, does not measure clauses, and does not separate AI prose from human prose at any threshold. Four more second-order checks fire more often on human prose than on AI drafts. The evidence is below.

## 1. What the check actually computes

```python
multi = [s for s in sents if s.count(",") >= 2 and len(words_of(s)) >= 12]
frac  = len(multi) / len(sents)
```

It counts commas. It never compares one sentence to another, so it cannot see a metronome, which by definition is repetition. A paragraph of three sentences fails on two comma-rich sentences of wildly different shapes and lengths.

Three separate measurement faults ride on top of that.

**Thousands separators count as clause boundaries.** `$5,600 instead of $7,000, permanently` scores three commas. One is real. Five of the broadcast file's gate-passing sentences owe their comma count to prices.

**Markdown emphasis merges sentences.** `split_sentences` splits on `(?<=[.!?])\s+`, so `**The rate ends.** Aesthetic Smile Design Excellence goes from $5,600 to $7,000, permanently.` stays one sentence. Fifteen such artifacts in the broadcast file, inflating both the word count and the comma count that feed the gate.

**`words_of` drops digits.** `[A-Za-z][A-Za-z'-]*` reduces B1, B6, B8 and B10 all to `b`, so two unrelated status lines register as an adjacent echo.

The worst broadcast flag was made entirely of artifacts. One sentence, split in two by a bold marker, carrying three commas of which two were inside prices.

## 2. It fires on prose written before language models existed

Detector run unchanged over human corpora.

| Corpus | Second-order layer fails | three_clause fails |
|---|---|---|
| Austen 1817 and Darwin 1859, 40 chunks of ~600 words | 40 of 40 | 37 of 40 |
| Same, 33 chunks of ~6,000 words | 33 of 33 | 33 of 33 |
| 15 Paul Graham essays, 2004 to 2015 | 14 of 15 | 12 of 15 |

Paul Graham is the fair control. Modern, plain, business register, roughly the register the skill is pointed at, and published a decade before ChatGPT. Twelve of fifteen essays fail.

## 3. The rate carries a little signal. The gate throws it away

Share of eligible paragraphs (3 or more sentences) that the check flags.

| Corpus | Flag rate |
|---|---|
| Paul Graham, human | 7.1 percent, median 5, max 19 |
| ASDE posts before the 27 July pass, AI draft | 20.1 percent |
| ASDE posts after that pass | 0.0 percent |
| ASDE broadcasts, Julian's hand, ruled fine | 17.9 percent |
| Planted AI fixture, `tests/fixtures/idd-draft-sloppy.md` | 12.5 percent |

Two things fall out. The gate is `rate > 0` against a human baseline of 7 percent, which guarantees the false-positive rate in section 2. And the planted AI fixture scores lower than Julian's own approved copy, so the metric ranks known slop as more human than the writing it flagged.

## 4. No threshold fixes it, which is the finding that settles the question

The obvious repair is to narrow the check to genuine mechanical repetition. That was built and swept across the whole parameter space: run length 2 to 4, real clause boundaries 1 to 2 (numeric commas stripped, enumeration commas excluded by requiring a finite verb in the segment), length coefficient of variation 0.20 to unbounded, consecutive runs and paragraph-wide counts.

Best separation available anywhere in that space, measured as the AI-draft hit rate minus the worst human-corpus hit rate, was **plus 0.05**. Settings sensitive enough to catch AI drafts caught every human corpus too. Settings specific enough to spare human prose caught nothing at all. Several settings inverted, the worst at minus 0.77, firing on 14 of 15 Paul Graham essays against 5 of 22 AI drafts.

Clause density tracks how considered the prose is, not who wrote it. There is no threshold to raise this check to.

## 5. The 22-post separation was Goodhart, not validation

On the labelled before and after set the check looks perfect, 18 of 22 failing before and 0 of 22 after. That is compliance, not discrimination. A corpus at exactly 0.0 percent sits below every natural human corpus measured.

How the agents cleared it, taken verbatim from `3d-printed-hybrid-veneers.md`. Both flagged sentences survive the repair byte for byte. Two unrelated sentences were appended, moving the fraction from 2 of 3 to 2 of 5, under the 0.5 gate.

```
PRE   3 sentences, 2 flagged -> 0.67, FAIL
POST  5 sentences, 2 flagged -> 0.40, PASS   same two sentences, unedited
```

Across the 22 posts the repair added no clarity and removed 57 paragraphs, taking mean sentences per paragraph from 2.38 to 2.61. Denser paragraphs, unchanged tells, green detector.

This is the correction to `2026-07-27-paragraph-shape-advisory.md` section 1. That note found the same check being gamed by swapping commas for dashes and answered it with anti-gaming rules in the agent briefs. The rules worked and were aimed at the wrong target. The check was never worth defending.

## 6. The same test applied to every second-order check

Fires on AI drafts versus fires on untouched Paul Graham essays.

| Check | AI draft | Human | Verdict |
|---|---|---|---|
| paragraph_shape | 100 percent | 7 percent | usable signal, currently advisory |
| opening_word_repetition | 59 percent | 7 percent | usable signal, currently gating |
| three_clause_rhythm | 82 percent | 80 percent | no signal, currently gating |
| adjacent_echoes | 41 percent | 53 percent | no signal, currently gating |
| spliced_triads | 23 percent | 20 percent | no signal, currently gating |
| repeated_openers | 23 percent | 20 percent | no signal, currently gating |
| flat_paragraphs | 73 percent | 100 percent | inverted, already advisory |
| staccato_runs | 18 percent | 47 percent | inverted, currently gating |
| amputated_purpose | 0 percent | 40 percent | inverted, currently gating |
| hedge_stacking | 0 percent | 20 percent | inverted, currently gating |

The phrase-level and hygiene checks are not in this table. They are deterministic string matching rather than statistics and they behave. The MS1 finding on 4 August, two courses named in the body with no link, was real and came from that side of the skill.

Verified examples behind the two strongest inversions.

`amputated_purpose` fires on ordinary discourse "So". Paul Graham, "So you could say that using Lisp was an experiment." and "So Hamming's exercise can be generalized to". The regex cannot tell a consequential "So" from a severed purpose clause, and reference 02 already says so while the check still gates.

`staccato_runs` fires on punch. Paul Graham runs of [3, 3, 3, 3] and [4, 5, 4] words. Short sentence runs are a human stylistic signature. AI marketing prose is verbose, so the polarity is backwards.

`spliced_triads` is a logic inversion. It strips a leading "and", "but", "so" or "then" from each segment before taking the subject, which means a correctly punctuated compound sentence is guaranteed to fire. "We carry all the leading brands, and we review and teach across the whole market, so we can recommend the best option for you." is not a comma splice. The conjunctions that prove it is not one are the tokens the code discards.

## 7. The pattern worth carrying forward

Every check that survived this test measures something a writer does not consciously control across a whole document, which is word choice and document-scale distribution. Every check that failed measures sentence-level craft, which is exactly what a good writer varies on purpose and what a careful reader notices first.

Reference 02 already lists the false-positive class for most of these under "Where these checks over-report" and "Manual checks the script skips", including enumeration commas by name. The doctrine knew. The gates fired anyway. A documented false-positive class in a gating check is a bug report, not a caveat.

## 8. What the 22-post pass actually did, audited

Julian asked for the scale of the metric-driven editing. Every paragraph that carried a three-clause flag before the pass was traced to its descendant after it. Two mechanisms, both leaving the sentence rhythm untouched.

**Padding, 40 flagged sentences across 16 posts.** The flagged sentences survive byte for byte and the paragraph grew, so the fraction fell under the 0.5 gate on the denominator alone. Six paragraphs cleared the gate purely this way, 11 sentences added.

**Repunctuation, 20 flagged sentences across 9 posts.** Same words, punctuation swapped until the comma count dropped. Mostly commas to parentheses, which is not neutral, because parentheses de-emphasise and commas do not. Six of the twenty deleted punctuation that was helping the reader.

```
He researched it, built an answer, and added it to his file.
He researched it, built an answer and added it to his file.

Getting that alignment right by eye alone, in that mouth, is not a realistic ask.
Getting that alignment right by eye alone in that mouth is not a realistic ask.

A lab-fabricated stent controls where warmed composite goes, tooth by tooth, so ...
A lab-fabricated stent controls where warmed composite goes tooth by tooth, so ...
```

The 27 July note caught this mechanism and answered it with anti-gaming rules in the agent briefs. The rules held, and the gaming continued anyway at a lower level, because the incentive was still there. That is the argument for removing the gate rather than policing it.

Not all of it is damage. Many parenthetical conversions read fine and some added sentences carry real content. The finding is narrower and worse than "the posts got worse": roughly 60 sentences across the set were edited to satisfy a measurement that does not detect anything.

## 9. What was changed, 2026-08-05

Julian's go, given after reading sections 1 to 7. Version 0.6.0, not yet bumped or committed.

1. `three_clause_rhythm`, `adjacent_echoes`, `spliced_triads`, `repeated_openers`, `staccato_runs`, `amputated_purpose` and `hedge_stacking` moved into `ADVISORY_CHECKS`. They measure, report and warn; they no longer fail a layer.
2. The three measurement faults fixed. Numeric commas stripped before any comma count, `split_sentences` no longer merged by markdown emphasis and closing brackets, `words_of` keeps digits so B1 and B6 stop collapsing to "b".
3. `spliced_triads` logic corrected. It now requires the subject to be restated twice AND at least one restatement to sit at a genuine splice, so "We carry X, and we review Y, so we can Z" is no longer a finding while "The software leverages X, it analyzes Y, and it flags Z" still is.
4. `fmt_state` added so a demoted check renders as ADVISORY rather than FAIL. A check reading FAIL beside a layer reading PASS sends a reader back to edit something the evidence says is not a tell.
5. Reference 02 and SKILL.md rewritten to match, including the corrected general lesson in section 7 and a new non-negotiable that a metric driven to zero is a warning rather than a result.
6. `paragraph_shape` left advisory. It is the strongest discriminator measured here, but it is layout-driven and the corpora differ in genre, so 100 against 7 is not clean enough to gate on.

Effect on the layer verdict, second-order:

| Corpus | Before | After |
|---|---|---|
| ASDE pre-humanise, AI draft, should fail | 22 of 22 | 13 of 22 |
| Planted AI fixture, should fail | fails | fails |
| Paul Graham essays, should pass | 14 of 15 fail | 1 of 15 fails |
| ASDE post-humanise, should pass | 0 of 22 fail | 0 of 22 fail |
| ASDE broadcasts, ruled fine, should pass | fails | fails on symmetric_lists only |

62 tests green, including the repo's own demotion guard. That one needs flagging rather than noting.

**The teeth floor is now exactly met, with no margin.** `test_demotion_left_the_layer_with_real_teeth` asserts that at least 8 gating checks still fail on the reference slop fixture, a floor the 27 July note set precisely so that a deliberate demotion stays easy and an accidental gutting does not. At 0.5.0 the fixture failed 12 second-order gating checks. At 0.6.0 it fails 8. The test passes and the whole margin is gone, so the next demotion of any second-order check breaks it.

That is the guard working as designed rather than a fault, and the eight survivors are the right eight: `h2_question_cadence`, `here_openers`, `false_balance`, `symmetric_lists`, `wrapup_questions`, `capsule_transitions`, `key_insight_openers` are deterministic pattern matches, and `opening_word_repetition` is the one statistical check with measured signal. The layer still fails all three verdicts on the fixture. But anyone proposing a ninth demotion now has to raise the floor deliberately, and should read section 4 before doing it.

The remaining Paul Graham failure is `opening_word_repetition` at 26.2% against a 25% limit, a marginal miss on the check with the best signal in the layer, and the threshold was deliberately left alone.

The remaining broadcast failure is one symmetric list of three chapter pointers in the same frame. That is a correct report and an editorial call: the asset table already exempts parallel lists in conversion copy, and an email broadcast is conversion copy, so it is a deliberate keep rather than a detector fault.

The cost of the change is real and worth stating. The detector now misses 9 of 22 AI drafts it used to fail. It was failing them on checks that also failed 14 of 15 human essays, so those were not detections.

## 10. Still open

- Version bump to 0.6.0 and the commit, both gated on Julian.
- Two dev-doc directories exist, `docs/dev/` and `dev-docs/`. This note is in `docs/dev/` with the 25 and 27 July notes; the 29 and 30 July notes are in `dev-docs/`. One should absorb the other.
- The 22 posts carry roughly 60 metric-driven edits. Section 8 lists them. Reverting is not obviously right, since many read fine, but the six punctuation deletions above are worth restoring.

## Method notes

Human controls were Project Gutenberg texts for Austen and Darwin, paulgraham.com for the essays, all fetched 2026-08-05 and chunked to match the length of the documents the skill is normally run on. The genre confound is real and worth naming. Essays and 19th century novels are not dental blog posts. It is mitigated but not removed by the two in-house controls, which are Julian's own broadcast copy that he ruled fine and the labelled before and after blog corpus, and by the direction of the inversions, which no genre argument explains.

Reproduction inputs, all read-only. `/Users/juliandickie/code/idd-world/campaigns/2026/2026-07-asde-launch/ASDE-Interest-Engine-Launch-Broadcasts.md`, `.../Blogs/` and `.../Blogs/.pre-humanise-2026-07-27/`.
