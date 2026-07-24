# First-Order Tells - Phrase and Lexical Layer

The obvious fingerprints: trained-in phrases, spiked vocabulary, and flat
lexical statistics. `scripts/detect.py` computes everything in this file; run
it before doing anything by hand and work from its line numbers.

A draft that passes this layer can still be obviously AI. First-order clean is
necessary, never sufficient. Always proceed to
[02-second-order-tells.md](02-second-order-tells.md).

## Trigger phrases by family

| Family | Examples | Default repair |
|--------|----------|----------------|
| Scene-setting openers | "In today's digital landscape", "In today's rapidly evolving...", "In the ever-evolving world of..." | Delete the sentence. Open with the specific fact, claim, or scene the piece is actually about. |
| Throat-clearers | "It's important to note that", "It is worth mentioning", "It goes without saying" | Delete the frame, keep the content. The sentence almost always survives without it. |
| Hype vocabulary | "game-changer", "revolutionize", "revolutionary", "cutting-edge", "state-of-the-art", "groundbreaking", "paradigm shift", "transformative" | Replace with the measured, specific claim. What did it actually change, by how much, for whom? |
| Corporate verbs | "leverage", "harness the power", "unlock the potential", "streamline", "empower", "embrace", "elevate", "supercharge", "utilize", "facilitate" | Use the plain verb: use, run, cut, speed up, let. |
| Tour-guide moves | "delve into", "dive into", "deep dive", "let's explore", "embark on", "navigate the complexities" | State the thing directly instead of announcing the journey to it. |
| Transition overload | "Furthermore", "Moreover", "Additionally" as sentence openers | Delete, or bury the connection inside the sentence. Real prose rarely needs the signpost. |
| Wrap-up cliches | "In conclusion", "To summarize", "In summary" | Delete. End on the strongest specific point instead. |
| Smoothness claims | "seamlessly", "seamless integration", "effortlessly" | Say what actually happens: exports directly, needs no re-entry, one click. |

The full machine-checkable list lives in `AI_PHRASES` and `AI_TRIGGER_WORDS`
inside `scripts/detect.py`. Keep the two in sync if either grows.

## Lexical metrics and thresholds

| Metric | Threshold | Meaning |
|--------|-----------|---------|
| Trigger-word density | fail above 5 per 1,000 words | Single words that spiked in AI text (delve, robust, pivotal, multifaceted, realm...) |
| Type-Token Ratio | fail below 0.40 on 400+ word docs | Repetitive vocabulary reads machine-made |
| Burstiness (sentence-length SD divided by mean) | fail below 0.30 | Humans mix short punches with long builds; models write medium everywhere |

TTR calibration - the 0.40 floor is calibrated for editorial long-form.
Conversion copy that deliberately mirrors its offer nouns (the fixed price,
the land check, the certificate) reads low by design; judge whether the
repeated words are load-bearing offer language or filler before treating a
low TTR as a tell.

## Repair discipline

1. Delete before you replace. Most throat-clearers, signposts, and wrap-ups
   delete clean and the prose tightens.
2. Never thesaurus-swap. Replacing "delve into" with "let's explore" trades
   one listed tell for another. Rebuild the sentence around the concrete fact
   it carries.
3. Replacement vocabulary comes from the active voice skill (see
   [03-voice-preserving-repair.md](03-voice-preserving-repair.md)), not from a
   synonym list. If the brand says "Here's the thing", that is the register to
   reach for.
4. Fix burstiness by ear, not by formula. Read the paragraph aloud; where every
   sentence takes the same breath, cut one to a fragment or fuse two.

## Attribution

Phrase and trigger-word lists adapted from claude-blog's analyze_blog.py
(AgriciDaniel, MIT). Threshold values follow claude-blog's ai-slop-detection
reference, which adapts the impeccable plugin's two-tier methodology
(Paul Bakaus, Apache 2.0).
