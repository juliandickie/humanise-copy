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
