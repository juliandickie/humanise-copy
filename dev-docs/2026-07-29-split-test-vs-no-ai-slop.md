# Split test vs petergyang/no-ai-slop - findings for this skill

Dated additive note, 2026-07-29. Pilot split test run the day the juliandickie/no-ai-slop fork was packaged as a Claude plugin. This note carries what matters TO humanise-copy.

**Written client-anonymous on purpose.** The corpus was live client work in a private repo, so the client, the repo and the verbatim source sentences are deliberately left out and the illustrative examples below are synthetic reconstructions of the same shapes. The findings, metrics and caveats are the real ones. Do not "restore" identifying detail to this file - it is public.

## Method (pilot, n=3, honest caveats)

Three real long-form service-sector insights articles. Baseline = the pre-humanise versions from the client repo's history. Arm A = the committed production humanise pass. Arm B = three blind sonnet agents applying no-ai-slop's SKILL.md with house constraints (frontmatter frozen, no dashes, AU English, facts exact). Scored with this repo's detect.py plus a crude regex proxy for no-ai-slop's named patterns, then ear-read word diffs. Caveats - arms not rig-matched (production fleet + QA vs single agents), tiny n, corpus already house-clean, and Arm A's edits partially targeted this skill's own checks.

## Improvement candidates for humanise-copy, ranked

1. **Colon-reveal as a repair artifact (build this).** The humanise pass ITSELF introduced colon-joins in 2 of 3 docs - the exact shape of no-ai-slop's colon-reveal pattern, being `clause: lowercase continuation` (synthetic example of the shape: "the cost is not one number: it is a small stack of them"). Our repair vocabulary reaches for a colon-join when dissolving a two-sentence contrast. This belongs in the repair-artifact checks (the damage-a-repair-introduces family, checks 12-16 territory) - flag a repair that produces that shape and prefer a plain-sentence restructure.
2. **Faux-insight reader-flattery family (gap).** A reader-flattery aside of the "this is the section worth reading twice" type shipped to production through our pass; no-ai-slop cut it under its faux-insight pattern ("what nobody tells you", "most people miss", "worth reading twice"). We have no equivalent check. Small family, high tell value.
3. **Repeated sentence-shape opener runs (gap, judgement-tier).** Four consecutive paragraph openers sharing one sentence shape passed our structural checks; no-ai-slop's robotic-rhythm rule varied them. Candidate as a borderline WARNING not a failure - one of the three agents judged a similar run (repeated imperative openers) an intentional checklist voice and left it, which is the right call, so this check must stay advisory.
4. **An eval harness (adopt the concept).** Upstream no-ai-slop ships eval.md - editing principles plus positive and negative test cases. This repo has tests for the detector but no harness measuring whether an EDIT pass improved a draft. The burstiness result below shows what such a harness should assert.

## Measured validation of this skill's existing doctrine (keep, and say so in the README when relevant)

- **Repair-damage discipline works and is measurable.** Burstiness held flat under our pass on 3/3 docs (0.519 / 0.693 / 0.713 vs pre 0.517 / 0.693 / 0.718) while no-ai-slop's edits lowered it on 3/3 (0.499 / 0.677 / 0.699). Directional, small n, but consistent - dissolve-everything editing flattens cadence, which is precisely what checks 12-16 exist to prevent.
- **Answer-engine routing is a real moat.** No-ai-slop is blind to SEO structure - it left the PAA question headings alone here by luck of scope, and nothing in it would protect them on a corpus where an editor decides headings are slop. Our claude-seo routing rule already handles this.
- **Whitelist behaviour diverges by design.** No-ai-slop dissolved a quoted not-X-but-Y rhetorical question that our pass deliberately kept. Neither is wrong; ours preserves deliberate technique per the whitelist. Worth one line in SKILL.md contrasting the two doctrines now that both skills are installed side by side.

## Contribution candidates upstream (Julian's call, via the fork)

- A dont-flatten-cadence note or check for their eval.md - their SKILL.md states "untangle sentences without flattening the cadence" as principle but nothing measures it; our burstiness metric is the obvious instrument.
- The executable-detector concept (their harness is prose-only). Whether to contribute actual detect.py mechanics is an IP decision, not mine to make.
