# Mechanical Hygiene

The final pass, always last, because every earlier edit can reintroduce these
characters. A piece is not done until the hygiene layer of `scripts/detect.py`
reports zero across the board.

## The rules

| Rule | Fix |
|------|-----|
| No em dashes or en dashes, anywhere | Comma for a continuing thought, parentheses for an aside, hyphen for compound terms, or split the sentence. Per instance, by ear; never a blind global replace |
| No colons in titles or headings | Separate segments with " - " or parentheses |
| Straight quotes and apostrophes only | Global replace of curly forms is safe |
| No trademark, registered, or copyright glyphs | Strip them; the brand name stands alone |
| Normalise typographic ligatures to plain ASCII | Global replace is safe |
| Number ranges | "to" or a hyphen, never an en dash |

Markdown table syntax (pipes and hyphen rows) and YAML frontmatter are
structural and exempt; the rules apply to cell content and prose.

## Destination-conditional rules

- Spelling follows the brand, not the pass: iDD is US English, Pro Marketing
  is Australian English, dedicated AU/NZ courses are AU/NZ English. Hygiene
  never "corrects" spelling across brands.
- Content headed into a Google Doc gets a full blank line between list items
  and sequential items (single newlines soft-collapse on paste). Local files,
  skills, and code docs use tight standard markdown. Do not force prose into
  lists to satisfy this.
- Filenames and Google Drive names use only letters, digits, spaces, hyphens,
  underscores, parentheses, full stops, and commas; "and" replaces the
  ampersand; slashes become hyphens or commas.

## Mechanics

Safe as global replacements: curly to straight quotes, glyph stripping,
ligature normalisation.

Editorial, one instance at a time: em and en dash replacement (the right
substitute depends on what the dash was doing), heading colons (choose the
" - " split point), hedged range rewrites.

## Verify

Re-run the detector and require a clean hygiene layer:

```bash
python3 scripts/detect.py THE-FILE.md --format markdown
```

Hygiene must show zero em dashes, zero en dashes, zero curly punctuation,
zero glyphs, zero ligatures, zero heading colons before the piece ships.
