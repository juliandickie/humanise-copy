# Expected Findings - idd-draft-sloppy.md

This is the plant inventory for the synthetic test fixture at
`tests/fixtures/idd-draft-sloppy.md`. The fixture deliberately violates house
style (em dashes, curly punctuation, AI phrases, structural tics). Never "fix"
the fixture and never publish it; it exists so the detector and the skill can be
tested against a known ground truth.

## Planted tells that MUST be flagged and repaired

### First-order (phrase and lexical)

| ID | Plant | Location hint |
|----|-------|---------------|
| F1 | "In today's rapidly evolving dental landscape" | opening paragraph |
| F2 | "delve into" | opening paragraph |
| F3 | "Game-Changer" / "game-changer" (x2) | H2 one, closing paragraph |
| F4 | "leverages" | section one |
| F5 | "seamlessly" (x2) | section one, closing paragraph |
| F6 | "It's important to note that" | opening paragraph |
| F7 | "Furthermore," and "Moreover," | sections one and two |
| F8 | "cutting-edge" | section one |
| F9 | "unlock the full potential" | section two |
| F10 | "harness the power" | section one |
| F11 | Em dashes (x3, plus one in the H1) | pricing line, comparison line, upgrade line, title |
| F12 | "revolutionary" / "revolutionizes" | section three, closing |
| F13 | "it is worth mentioning" | section three |
| F14 | "ever-evolving" | closing paragraph |
| F15 | "paradigm shift" | section three |
| F16 | "comprehensive" (x2) | H1, section two |
| F17 | "streamlines" / "empowers" / "Embrace" | section one, closing |
| F18 | "let's explore" / "explore" | opening, section two |
| F19 | "To summarize," | closing paragraph |

### Second-order (structural and rhythmic)

| ID | Plant | Detail |
|----|-------|--------|
| S1 | Question-cadence H2s | 4 of 4 H2 headings are questions (100%, threshold is 70%) |
| S2 | "Here's" openers | "Here's why" and "Here's what" are naive plants; "Here's the thing" is W1 and must be distinguished |
| S3 | Three-clause metronome | Section one, paragraph one: four consecutive sentences shaped [clause], [clause], [clause] |
| S4 | Hedge stacking | "may often typically be able to"; "may potentially ... could perhaps be argued ... typically favors" |
| S5 | Symmetric list bloat | Four bullets, identical "X that helps Y verb Z every N" shape, 11-12 words each |
| S6 | Wrap-up question (x2) | "What does this mean for your practice?" closes two sections |
| S7 | Capsule transitions | "First, let's explore" / "Next, it is worth mentioning" / "Additionally, timing matters" open sections; second "Additionally," mid-section |
| S8 | "The key insight is that" | section three |
| S9 | Third-person voice drift | "Clinicians may find this feature useful." and "Practitioners will appreciate" (exact idd-writing-style Wrong examples) |
| S10 | False-balance framing (x2) | "while the hardware remains unchanged, the software also delivers"; "While some features are diagnostic, others are also workflow-focused." |

### Mechanical hygiene

| ID | Plant | Detail |
|----|-------|--------|
| H1 | Curly apostrophe | "practice's" in section three uses U+2019 |
| H2 | Em dash in H1 | title uses an em dash rather than " - " |

## Deliberate voice and technique that MUST survive

| ID | Item | Why it stays |
|----|------|--------------|
| W1 | "Here's the thing." | iDD signature phrase (idd-writing-style, Signature Phrases) |
| W2 | "So the question becomes," | iDD signature transition |
| W3 | "The plaque detection? Less impressive." | Single-line emphasis paragraph, explicitly allowed by iDD style |
| W4 | "$4,500 USD plus a $149 per month subscription" | Price format and market context required by iDD style |
| W5 | "We have been using the AI suite extensively in our clinic..." plus "my honest read", "I would not want to prep another crown without it" | First-person experience signal, the core of the iDD voice |
| W6 | "In saying that," | iDD pivot phrase |

## Baseline hypothesis (RED phase)

A capable model without the skill is expected to strip most first-order phrases,
miss most structural tells (question-cadence H2s, the symmetric list, capsule
transitions, three-clause rhythm), and over-correct voice, removing one or more
W items. The likeliest casualty is "Here's the thing" being swept up with the
"Here's why / Here's what" plants. Whatever the actual baseline shows goes into
the skill's Common Mistakes section.
