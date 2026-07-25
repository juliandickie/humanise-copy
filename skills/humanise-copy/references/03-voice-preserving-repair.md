# Voice-Preserving Repair

Neutral is the tell. Models drift toward an averaged, institutional register,
so a repair pass that merely deletes flagged items moves the text closer to
that average, not further from it. The cure for AI-flavoured prose is one
specific person's flavour. Every fix is written in the active voice, never in
generic "clean" English.

## Load the voice before you repair

1. Identify whose voice the piece belongs to (brand, author, client).
2. Load that voice source in full.
3. Only then repair flagged items, writing every replacement in that voice
   and spelling (iDD is US English; Pro Marketing is Australian English;
   dedicated AU/NZ courses are AU/NZ English).

| Context | Voice source | Notes |
|---------|-------------|-------|
| iDD content | the idd-writing-style skill | First-person clinical register, signature phrases, its own never-use list (which overlaps the first-order tells) |
| Pro Marketing client work | the client's voice profile (VOICE.md, brand-voice guidelines, or brand-voice:enforce-voice) | One profile per client; do not blend clients |
| Conversion assets from the 10x system | 10x-brand-voice plus the originating 10x skill | The sweep record marks which rhythm choices were deliberate |
| No voice source exists | Stop and ask, or run brand-voice:generate-guidelines or voc-research first | Never invent a persona silently |

## The whitelist mechanic

The detector reports; it does not judge. Before deleting anything it flagged,
check the hit against, in order:

1. The voice skill's signature phrases and Right/Wrong examples.
2. The originating copy system's prescribed techniques (bucket brigades,
   deliberate anaphora, parallel CTA lines).
3. Format-native rhythm (short lines on social, a CTA question in email).

A match means keep it and log it as deliberate. Worked example from the test
fixture: the detector flags three "Here" paragraph openers; "Here's why" and
"Here's what" are generic filler and get rewritten, "Here's the thing" is an
iDD signature phrase and stays. A pass that deletes all three has flattened
the voice, which is the exact failure this skill exists to prevent.

## Repair moves

1. Reinstate the person. Third-person drift ("clinicians may find this
   useful") becomes a first-person read ("I found this useful chairside", "we
   have been running it in our clinic since March"). The honesty and the
   opinion belong to a named human, per the voice skill.
2. Trade abstractions for owned specifics. "Significant improvements" becomes
   the number, the timeframe, the case type. Specifics must already exist in
   the source material or come from the user; see the fabrication boundary.
3. Untangle metronome sentences one idea at a time. A three-clause chain
   becomes one short claim plus one supporting sentence, not a longer chain.
4. Take the rhythm from speech. Read the paragraph aloud in the author's
   register; punch short where the voice would land, let a thought run long
   where it genuinely builds.
5. Hedge honestly. Keep the one qualifier the author would actually say,
   delete the performed balance. Measured is one hedge, not three.
6. Humor and personality are a separate dial. When the 10x-copywriting plugin
   is installed, hand the humor pass to copy-editing-sweeps (its AI punch-up
   reference owns that process). Without it, restraint: at most one aside per
   piece, in the brand's register, and cut it if in doubt.

## Repairing without introducing new tells

A repair pass is itself a generation pass, so it leaves its own fingerprints.
Eight agents running this skill over about 620 sentence repairs (the 2026-07-25
fleet run) produced every failure below, and all of them passed the detector
they were re-run against. Five are now mechanical checks
([02-second-order-tells.md](02-second-order-tells.md), items 12 to 16). The
rest cannot be measured, so judgment holds them.

Each is written as the move that produces the right result, because the wrong
results all came from agents doing something reasonable under pressure.

1. Vary openers by restructuring the sentence. A varied opener is a
   possessive ("Bundaberg's buyer pool runs deeper"), a fronted subordinate
   clause ("Because stock is thin, the buyer pool runs deeper"), or a
   different subject. It is not the same sentence with its article removed:
   "The buyer pool here includes" clipped to "Buyer pool here includes" reads
   as telegraphese, which is a louder tell than the repetition it fixed.
2. Keep purpose clauses attached to what they serve. ", so the team can
   support them" belongs on its sentence, or becomes "That way, the team can
   support them." A standalone "So the team can support them." is a fragment
   wearing a full stop. Consequential "So" sentences ("So the question
   becomes whether it pays for itself") are a different construction and are
   fine.
3. Re-read a split sentence for meaning, not just rhythm. Splitting moves
   connectives, and a moved connective changes the logic: "and again only if"
   became "Then again, only if", which idiomatically means "on the other
   hand". Every split gets its two halves read as sentences in their own
   right.
4. Preserve the rhetorical function of the line, not only its content. "The
   practical point is simple" sets up a simplification. "It really is that
   simple" asserts the previous paragraph was simple, which may be false.
   What a sentence is doing in the argument is part of what it means, and
   rewriting the doing is a meaning change even when every fact survives.
5. Read the whole paragraph after editing any sentence in it. Sentence-local
   edits are where echoes ("This guide... This guide"), appositives that drift
   onto the wrong noun, and pronouns left without an antecedent ("These
   priorities", naming nothing) come from. The detector's echo and opener
   checks catch the repeating shapes; only a paragraph read catches a
   reference that no longer points anywhere.
6. Say the repaired sentence out loud before accepting it. This is the gate
   that catches what nothing else does: chop ("Then this is the category."),
   dropped particles, and the general over-tightening that reads written
   rather than spoken. When tight and natural conflict, natural wins.

## Delegating repair to subagents

Repair fans out well, and the fleet run's briefs got measurably better wave
over wave. Three things carried that.

- Name the frozen classes in the brief itself: figures, legal and regulatory
  references, ratios, testimonials, listings, About-the-author blocks, TL;DR
  blocks that mirror CMS frontmatter, founding-year and other YMYL claims.
  Naming them produced zero factual drift across the whole run.
- Name the banned replacement tic. Two agents independently reached for
  "Honestly," as their opener of choice; neither could hear it because each
  saw only its own files. One brief line prevents it, and the detector now
  catches it after the fact.
- Fold each wave's findings into the next wave's brief. The last agents of
  both fleets needed near-zero corrections, which is the only real evidence
  that the brief, not the model, was doing the work.

Give agents the naturalness rules above as brief material, not a pointer to
them. An agent that has read rule 1 does not invent telegraphese.

## The fabrication boundary

Never invent anecdotes, patients, clients, test results, timeframes, or
numbers to make text feel experienced. The boundary includes attribution:
rewriting a generic product claim as a first-person observed outcome
("retakes have come down since we started using it") fabricates experience
even though no new number was invented, and voice phrases like "in my
experience" attach only to claims the source actually grounds in experience.
If the piece needs experience it does not contain, stop and ask the user for
the real detail, or flag the gap in the delivery note. A fabricated experience signal is worse than any AI tell,
for the reader, for compliance, and for the author whose name carries it.

## Handoffs

- Voice profile missing or thin: brand-voice:generate-guidelines, then return.
- The words should come from customers, not the brand: voc-research.
- Conversion-copy quality issues beyond AI tells (weak proof, unclear offer):
  copy-editing-sweeps runs its ladder first; this skill runs after it.
- iDD spelling, structure, or claim conventions in doubt: idd-writing-style
  is the authority, not this file.
