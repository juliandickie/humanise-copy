#!/usr/bin/env python3
"""
humanise-copy detector - measures the tell-tale signs of AI generation in
markdown or plain-text prose and reports them as pass/fail checks across three
layers: first-order (phrase and lexical), second-order (structural and
rhythmic), and mechanical hygiene.

The script measures; the skill judges. Nothing here whitelists deliberate
technique (signature phrases, bucket brigades, emphasis fragments). The script
reports every hit with enough context for the editorial layer to decide what is
a tell and what is voice.

Usage:
    python3 detect.py FILE [FILE ...]            # JSON report (default)
    python3 detect.py FILE --format markdown     # human-readable report
    python3 detect.py FILE --gate                # exit 1 if any layer fails

Attribution: the two-tier methodology is adapted from the impeccable plugin
v3.1.1 (Paul Bakaus, Apache 2.0) by way of claude-blog (AgriciDaniel, MIT).
Portions of the phrase and trigger-word lists derive from claude-blog's
analyze_blog.py (MIT). Thresholds follow claude-blog's
skills/blog/references/ai-slop-detection.md with house-style additions
(em and en dashes, curly punctuation, trademark glyphs, ligatures).

Stdlib only. Python 3.9+.
"""

import argparse
import json
import re
import statistics
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

EM_DASH = "—"
EN_DASH = "–"
CURLY = ["‘", "’", "“", "”"]
GLYPHS = ["™", "®", "©"]  # trademark, registered, copyright
LIGATURES = ["ﬀ", "ﬁ", "ﬂ", "ﬃ", "ﬄ"]  # ff fi fl ffi ffl

AI_PHRASES = [
    "in today's digital landscape", "in today's rapidly evolving",
    "in today's fast-paced", "in the ever-evolving", "ever-evolving",
    "it's important to note", "it is important to note",
    "it is worth mentioning", "it's worth mentioning",
    "navigating the complexities", "navigate the landscape",
    "delve into", "dive into", "deep dive", "let's explore",
    "embark on", "game-changer", "game changer", "revolutionize",
    "revolutionary approach", "paradigm shift", "cutting-edge",
    "state-of-the-art", "harness the power", "unlock the potential",
    "unlock the full potential", "seamless integration", "seamlessly",
    "rich tapestry", "comprehensive guide", "at its core",
    "in conclusion", "to summarize", "in summary",
    "actionable insights", "best practices", "key takeaways",
    "look no further", "elevate your", "supercharge", "streamline",
]

AI_TRIGGER_WORDS = [
    "delve", "tapestry", "multifaceted", "testament", "pivotal", "robust",
    "furthermore", "moreover", "utilize", "leverage", "leverages",
    "comprehensive", "landscape", "crucial", "foster", "illuminate",
    "underscore", "embark", "endeavor", "facilitate", "paramount",
    "nuanced", "intricate", "meticulous", "realm", "empower", "empowers",
    "embrace", "elevate", "holistic", "synergy", "transformative",
]

HEDGE_WORDS = [
    "may", "might", "often", "typically", "generally", "usually",
    "perhaps", "somewhat", "likely", "potentially", "could", "arguably",
]

CAPSULE_TRANSITIONS = [
    "first", "second", "third", "next", "then", "additionally",
    "moreover", "furthermore", "finally", "crucially", "importantly",
    "notably", "ultimately", "essentially",
]

WRAPUP_PATTERNS = [
    r"what does this mean for .{0,60}\?",
    r"why does this matter\??",
    r"what'?s the bottom line\??",
]

KEY_INSIGHT_OPENERS = [
    "the key insight is", "what's important here is",
    "what is important here is", "the key takeaway is",
]

ABBREVIATIONS = [
    "Dr.", "Mr.", "Mrs.", "Ms.", "Prof.", "vs.", "e.g.", "i.e.", "etc.",
    "approx.", "No.", "U.S.", "a.m.", "p.m.",
]

THRESHOLDS = {
    "trigger_density_per_1k": 5.0,     # fail above
    "ttr_min": 0.40,                    # fail below (docs >= 400 words)
    "burstiness_min": 0.30,             # SD/mean, fail below
    "h2_question_pct_max": 70.0,        # fail above
    "here_openers_max": 2,              # fail above
    "false_balance_per_1k_max": 2.0,    # fail above
    "wrapup_questions_max": 2,          # fail above
    "capsule_opener_pct_max": 50.0,     # fail above
    "opening_word_top3_pct_max": 25.0,  # fail above
    "paragraph_sd_min": 25.0,           # fail below (docs >= 8 paragraphs)
    "symmetric_list_sd_min": 5.0,       # flag lists below
    "flat_paragraph_sd_min": 4.0,       # flag paragraphs below
    "three_clause_fraction": 0.5,       # flag paragraphs at/above
}

# ---------------------------------------------------------------------------
# Text preparation
# ---------------------------------------------------------------------------


def clean_lines(raw):
    """Return the file's lines with frontmatter, HTML comments, and fenced
    code blanked out (replaced by empty strings) so line numbers survive."""
    lines = raw.split("\n")
    out = list(lines)

    # YAML frontmatter
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                for j in range(0, i + 1):
                    out[j] = ""
                break

    # Fenced code blocks
    in_fence = False
    for i, line in enumerate(lines):
        if line.strip().startswith("```"):
            in_fence = not in_fence
            out[i] = ""
        elif in_fence:
            out[i] = ""

    # HTML comments (may span lines)
    in_comment = False
    for i, line in enumerate(out):
        if not line:
            continue
        work = line
        if in_comment:
            if "-->" in work:
                work = work.split("-->", 1)[1]
                in_comment = False
            else:
                out[i] = ""
                continue
        while "<!--" in work:
            before, rest = work.split("<!--", 1)
            if "-->" in rest:
                work = before + rest.split("-->", 1)[1]
            else:
                work = before
                in_comment = True
        out[i] = work
    return out


def split_sentences(text):
    """Split prose into sentences. Masks common abbreviations first."""
    masked = text
    for abbr in ABBREVIATIONS:
        masked = masked.replace(abbr, abbr.replace(".", "\x00"))
    parts = re.split(r"(?<=[.!?])\s+", masked)
    return [p.replace("\x00", ".").strip() for p in parts if p.strip()]


def words_of(text):
    return re.findall(r"[A-Za-z][A-Za-z'’-]*", text.lower())


def parse_blocks(lines):
    """Parse cleaned lines into blocks: headings, list groups, prose
    paragraphs. Returns a list of dicts with type, text, line, and (for
    lists) items."""
    blocks = []
    buf = []
    buf_start = None

    def flush():
        nonlocal buf, buf_start
        if buf:
            blocks.append({
                "type": "prose",
                "text": " ".join(buf).strip(),
                "line": buf_start,
            })
            buf = []
            buf_start = None

    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        stripped = line.strip()
        if not stripped:
            flush()
            i += 1
            continue
        m = re.match(r"^(#{1,6})\s+(.*)$", stripped)
        if m:
            flush()
            blocks.append({
                "type": "heading",
                "level": len(m.group(1)),
                "text": m.group(2).strip(),
                "line": i + 1,
            })
            i += 1
            continue
        if re.match(r"^([-*+]|\d+[.)])\s+", stripped):
            flush()
            items = []
            start = i + 1
            while i < n:
                s = lines[i].strip()
                if re.match(r"^([-*+]|\d+[.)])\s+", s):
                    items.append(re.sub(r"^([-*+]|\d+[.)])\s+", "", s))
                    i += 1
                elif not s:
                    # blank line inside a list only ends it if the next
                    # non-blank line is not a list item
                    k = i + 1
                    while k < n and not lines[k].strip():
                        k += 1
                    if k < n and re.match(r"^([-*+]|\d+[.)])\s+", lines[k].strip()):
                        i = k
                    else:
                        break
                else:
                    break
            blocks.append({"type": "list", "items": items, "line": start})
            continue
        if buf_start is None:
            buf_start = i + 1
        buf.append(stripped)
        i += 1
    flush()
    return blocks


# ---------------------------------------------------------------------------
# First-order checks
# ---------------------------------------------------------------------------


def check_first_order(lines, all_words, sentences):
    text_lower = "\n".join(lines).lower()

    phrase_hits = []
    for phrase in AI_PHRASES:
        count = text_lower.count(phrase)
        if count:
            hit_lines = [i + 1 for i, ln in enumerate(lines)
                         if phrase in ln.lower()]
            phrase_hits.append({"phrase": phrase, "count": count,
                                "lines": hit_lines})

    trigger_count = sum(1 for w in all_words if w in AI_TRIGGER_WORDS)
    total = len(all_words)
    trigger_density = (trigger_count / total * 1000) if total else 0.0

    ttr = (len(set(all_words)) / total) if total else 0.0

    slens = [len(words_of(s)) for s in sentences if words_of(s)]
    if len(slens) >= 2 and statistics.mean(slens) > 0:
        burstiness = statistics.stdev(slens) / statistics.mean(slens)
    else:
        burstiness = 0.0

    ttr_applicable = total >= 400
    return {
        "phrases": phrase_hits,
        "phrase_total": sum(h["count"] for h in phrase_hits),
        "trigger_density_per_1k": round(trigger_density, 2),
        "ttr": round(ttr, 3),
        "ttr_applicable": ttr_applicable,
        "burstiness": round(burstiness, 3),
        "checks": {
            "phrases": len(phrase_hits) == 0,
            "trigger_density": trigger_density <= THRESHOLDS["trigger_density_per_1k"],
            "ttr": (not ttr_applicable) or ttr >= THRESHOLDS["ttr_min"],
            "burstiness": burstiness >= THRESHOLDS["burstiness_min"],
        },
    }


# ---------------------------------------------------------------------------
# Second-order checks
# ---------------------------------------------------------------------------


def check_second_order(blocks, all_words, sentences):
    prose = [b for b in blocks if b["type"] == "prose"]
    h2s = [b for b in blocks if b["type"] == "heading" and b["level"] == 2]
    lists = [b for b in blocks if b["type"] == "list"]
    total_words = len(all_words)

    # 1. Question-cadence H2s
    h2_q = sum(1 for h in h2s if h["text"].rstrip().endswith("?"))
    h2_q_pct = (h2_q / len(h2s) * 100) if h2s else 0.0

    # 2. "Here" paragraph openers (reported with context for whitelisting)
    here_openers = []
    for b in prose:
        if re.match(r"^Here(’s|'s| is| are)\b", b["text"]):
            here_openers.append({"line": b["line"], "text": b["text"][:70]})

    # 3. Three-clause metronome paragraphs (near-misses recorded separately;
    # a paragraph-level gate is blind to single-sentence faults, so anything
    # in the borderline zone gets surfaced for a human read)
    three_clause = []
    three_clause_borderline = []
    for b in prose:
        sents = split_sentences(b["text"])
        if len(sents) < 3:
            continue
        multi = [s for s in sents
                 if s.count(",") >= 2 and len(words_of(s)) >= 12]
        frac = len(multi) / len(sents)
        entry = {"line": b["line"], "fraction": round(frac, 2),
                 "sentences": len(sents)}
        if frac >= THRESHOLDS["three_clause_fraction"]:
            three_clause.append(entry)
        elif frac >= THRESHOLDS["three_clause_fraction"] * 0.66:
            three_clause_borderline.append(entry)

    # 4. False-balance framing
    fb = 0
    fb_examples = []
    for b in prose:
        for m in re.finditer(r"\bwhile\b[^.!?]{0,80}\balso\b", b["text"],
                             re.IGNORECASE):
            fb += 1
            fb_examples.append({"line": b["line"], "text": m.group(0)[:70]})
        for m in re.finditer(r"\bon one hand\b", b["text"], re.IGNORECASE):
            fb += 1
            fb_examples.append({"line": b["line"], "text": m.group(0)[:70]})
    fb_per_1k = (fb / total_words * 1000) if total_words else 0.0

    # 5. Hedge stacking (any 20-word window with > 2 hedges)
    hedge_windows = []
    for b in prose:
        toks = words_of(b["text"])
        for start in range(0, max(1, len(toks) - 19)):
            window = toks[start:start + 20]
            hits = [t for t in window if t in HEDGE_WORDS]
            if len(hits) > 2:
                hedge_windows.append({"line": b["line"],
                                      "hedges": hits,
                                      "window": " ".join(window)[:80]})
                break  # one report per paragraph is enough

    # 6. Symmetric list bloat
    symmetric = []
    for lst in lists:
        counts = [len(words_of(item)) for item in lst["items"]]
        if len(counts) >= 3:
            sd = statistics.stdev(counts)
            if sd < THRESHOLDS["symmetric_list_sd_min"]:
                symmetric.append({"line": lst["line"], "items": len(counts),
                                  "word_counts": counts, "sd": round(sd, 2)})

    # 7. Wrap-up questions (verbatim repetition is a fingerprint on its own)
    wrapups = []
    for b in prose:
        t = b["text"].strip()
        for pat in WRAPUP_PATTERNS:
            if re.search(pat, t, re.IGNORECASE):
                wrapups.append({"line": b["line"], "text": t[:70]})
                break
    wrapup_seen = {}
    for w in wrapups:
        key = re.sub(r"\s+", " ", w["text"].lower())
        wrapup_seen[key] = wrapup_seen.get(key, 0) + 1
    wrapup_repeat = any(c > 1 for c in wrapup_seen.values())

    # 8. Capsule transitions on the first paragraph after a heading
    section_openers = []
    for i, b in enumerate(blocks):
        if b["type"] == "heading" and b["level"] == 2:
            for nxt in blocks[i + 1:]:
                if nxt["type"] == "prose":
                    section_openers.append(nxt)
                    break
                if nxt["type"] == "heading":
                    break
    capsule = []
    for b in section_openers:
        first = re.match(r"^([A-Za-z]+),", b["text"])
        if first and first.group(1).lower() in CAPSULE_TRANSITIONS:
            capsule.append({"line": b["line"], "opener": first.group(1)})
    capsule_pct = (len(capsule) / len(section_openers) * 100) if section_openers else 0.0

    # 9. "Key insight" openers
    key_insight = []
    for b in prose:
        low = b["text"].lower()
        for opener in KEY_INSIGHT_OPENERS:
            idx = low.find(opener)
            if idx >= 0:
                key_insight.append({"line": b["line"], "text": opener})

    # 10. Sentence-length flat paragraphs (with a borderline zone)
    flat = []
    flat_borderline = []
    for b in prose:
        sents = split_sentences(b["text"])
        lens = [len(words_of(s)) for s in sents if words_of(s)]
        if len(lens) >= 3:
            sd = statistics.stdev(lens)
            if sd < THRESHOLDS["flat_paragraph_sd_min"]:
                flat.append({"line": b["line"], "lengths": lens})
            elif sd < THRESHOLDS["flat_paragraph_sd_min"] * 1.25:
                flat_borderline.append({"line": b["line"], "sd": round(sd, 2)})

    # 11. Opening-word repetition
    firsts = []
    for s in sentences:
        w = words_of(s)
        if w:
            firsts.append(w[0])
    top3_pct = 0.0
    top3 = []
    if firsts:
        freq = {}
        for w in firsts:
            freq[w] = freq.get(w, 0) + 1
        ranked = sorted(freq.items(), key=lambda kv: kv[1], reverse=True)[:3]
        top3 = [{"word": w, "count": c} for w, c in ranked]
        top3_pct = sum(c for _, c in ranked) / len(firsts) * 100
    ow_applicable = len(firsts) >= 15

    # 12. Paragraph-shape flatness
    para_lens = [len(words_of(b["text"])) for b in prose]
    para_sd_applicable = len(para_lens) >= 8
    para_sd = statistics.stdev(para_lens) if len(para_lens) >= 2 else 0.0

    # 13. Spliced subject triads - "It runs..., it puts..., and it ends..."
    # The same pronoun subject restated across comma-spliced clauses reads
    # machine-tightened; a natural writer shares the verbs under one subject
    # or splits the sentence.
    pronouns = ("it", "we", "you", "they", "he", "she", "i")
    spliced = []
    for b in prose:
        for sent in split_sentences(b["text"]):
            segs = [seg.strip() for seg in sent.split(",") if seg.strip()]
            if len(segs) < 3:
                continue
            starts = []
            for seg in segs:
                w = words_of(seg)
                if not w:
                    continue
                first = w[0]
                if first in ("and", "but", "so", "then") and len(w) > 1:
                    first = w[1]
                starts.append(first)
            if len(starts) < 3:
                continue
            if any(starts[1:].count(p) >= 2 for p in pronouns):
                spliced.append({"line": b["line"], "text": sent[:70]})

    return {
        "h2_total": len(h2s),
        "h2_questions": h2_q,
        "h2_question_pct": round(h2_q_pct, 1),
        "here_openers": here_openers,
        "three_clause_paragraphs": three_clause,
        "three_clause_borderline": three_clause_borderline,
        "false_balance": fb_examples,
        "false_balance_per_1k": round(fb_per_1k, 2),
        "hedge_windows": hedge_windows,
        "symmetric_lists": symmetric,
        "wrapup_questions": wrapups,
        "wrapup_verbatim_repeat": wrapup_repeat,
        "capsule_openers": capsule,
        "capsule_opener_pct": round(capsule_pct, 1),
        "key_insight_openers": key_insight,
        "flat_paragraphs": flat,
        "flat_borderline": flat_borderline,
        "spliced_triads": spliced,
        "opening_word_top3": top3,
        "opening_word_top3_pct": round(top3_pct, 1),
        "opening_word_applicable": ow_applicable,
        "paragraph_sd": round(para_sd, 1),
        "paragraph_sd_applicable": para_sd_applicable,
        "checks": {
            "h2_question_cadence": h2_q_pct <= THRESHOLDS["h2_question_pct_max"],
            "here_openers": len(here_openers) <= THRESHOLDS["here_openers_max"],
            "three_clause_rhythm": len(three_clause) == 0,
            "false_balance": fb_per_1k <= THRESHOLDS["false_balance_per_1k_max"],
            "hedge_stacking": len(hedge_windows) == 0,
            "symmetric_lists": len(symmetric) == 0,
            "wrapup_questions": (len(wrapups) <= THRESHOLDS["wrapup_questions_max"]
                                 and not wrapup_repeat),
            "capsule_transitions": capsule_pct <= THRESHOLDS["capsule_opener_pct_max"],
            "key_insight_openers": len(key_insight) == 0,
            "flat_paragraphs": len(flat) == 0,
            "spliced_triads": len(spliced) == 0,
            "opening_word_repetition": (not ow_applicable) or top3_pct <= THRESHOLDS["opening_word_top3_pct_max"],
            "paragraph_shape": (not para_sd_applicable) or para_sd >= THRESHOLDS["paragraph_sd_min"],
        },
    }


# ---------------------------------------------------------------------------
# Hygiene checks
# ---------------------------------------------------------------------------


def check_hygiene(lines):
    joined = "\n".join(lines)

    def count_with_lines(chars):
        total = 0
        where = []
        for i, ln in enumerate(lines):
            c = sum(ln.count(ch) for ch in chars)
            if c:
                total += c
                where.append(i + 1)
        return total, where

    em, em_lines = count_with_lines([EM_DASH])
    en, en_lines = count_with_lines([EN_DASH])
    curly, curly_lines = count_with_lines(CURLY)
    glyphs, glyph_lines = count_with_lines(GLYPHS)
    liga, liga_lines = count_with_lines(LIGATURES)

    heading_colons = []
    for i, ln in enumerate(lines):
        m = re.match(r"^#{1,6}\s+(.*)$", ln.strip())
        if m and ":" in m.group(1):
            heading_colons.append(i + 1)

    return {
        "em_dashes": {"count": em, "lines": em_lines},
        "en_dashes": {"count": en, "lines": en_lines},
        "curly_punctuation": {"count": curly, "lines": curly_lines},
        "tm_r_c_glyphs": {"count": glyphs, "lines": glyph_lines},
        "ligatures": {"count": liga, "lines": liga_lines},
        "heading_colons": {"count": len(heading_colons), "lines": heading_colons},
        "checks": {
            "em_dashes": em == 0,
            "en_dashes": en == 0,
            "curly_punctuation": curly == 0,
            "glyphs": glyphs == 0,
            "ligatures": liga == 0,
            "heading_colons": len(heading_colons) == 0,
        },
    }


# ---------------------------------------------------------------------------
# Borderline warnings
# ---------------------------------------------------------------------------


def collect_warnings(first, second):
    """Passed-but-close results worth a human read-aloud. Advisory only;
    warnings never affect verdicts. Max-style checks warn inside the top 20%
    of their allowance, min-style checks within 10% above their floor,
    count-style checks exactly at their limit."""
    w = []

    def near_max(name, value, limit, factor=0.8):
        if value <= limit and value > limit * factor:
            w.append({"check": name, "value": value, "limit": limit})

    def near_min(name, value, floor, factor=1.1):
        if value >= floor and value < floor * factor:
            w.append({"check": name, "value": value, "floor": floor})

    if first["checks"]["trigger_density"]:
        near_max("trigger_density_per_1k", first["trigger_density_per_1k"],
                 THRESHOLDS["trigger_density_per_1k"])
    if first["ttr_applicable"] and first["checks"]["ttr"]:
        near_min("ttr", first["ttr"], THRESHOLDS["ttr_min"])
    if first["checks"]["burstiness"]:
        near_min("burstiness", first["burstiness"], THRESHOLDS["burstiness_min"])
    if second["checks"]["h2_question_cadence"]:
        near_max("h2_question_pct", second["h2_question_pct"],
                 THRESHOLDS["h2_question_pct_max"])
    if (second["checks"]["here_openers"]
            and len(second["here_openers"]) == THRESHOLDS["here_openers_max"]):
        w.append({"check": "here_openers_at_limit",
                  "value": len(second["here_openers"])})
    if second["checks"]["false_balance"]:
        near_max("false_balance_per_1k", second["false_balance_per_1k"],
                 THRESHOLDS["false_balance_per_1k_max"])
    if (second["checks"]["wrapup_questions"]
            and len(second["wrapup_questions"]) == THRESHOLDS["wrapup_questions_max"]):
        w.append({"check": "wrapup_questions_at_limit",
                  "value": len(second["wrapup_questions"])})
    if second["checks"]["capsule_transitions"]:
        near_max("capsule_opener_pct", second["capsule_opener_pct"],
                 THRESHOLDS["capsule_opener_pct_max"])
    if second["opening_word_applicable"] and second["checks"]["opening_word_repetition"]:
        near_max("opening_word_top3_pct", second["opening_word_top3_pct"],
                 THRESHOLDS["opening_word_top3_pct_max"])
    if second["paragraph_sd_applicable"] and second["checks"]["paragraph_shape"]:
        near_min("paragraph_sd", second["paragraph_sd"],
                 THRESHOLDS["paragraph_sd_min"])
    for item in second["three_clause_borderline"]:
        w.append({"check": "three_clause_borderline", "line": item["line"],
                  "fraction": item["fraction"]})
    for item in second["flat_borderline"]:
        w.append({"check": "flat_paragraph_borderline", "line": item["line"],
                  "sd": item["sd"]})
    return w


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------


def analyse_file(path):
    raw = Path(path).read_text(encoding="utf-8")
    lines = clean_lines(raw)
    blocks = parse_blocks(lines)
    prose_text = " ".join(b["text"] for b in blocks if b["type"] == "prose")
    list_text = " ".join(" ".join(b["items"]) for b in blocks if b["type"] == "list")
    all_words = words_of(prose_text + " " + list_text)
    sentences = split_sentences(prose_text)

    first = check_first_order(lines, all_words, sentences)
    second = check_second_order(blocks, all_words, sentences)
    hygiene = check_hygiene(lines)

    verdicts = {
        "first_order": all(first["checks"].values()),
        "second_order": all(second["checks"].values()),
        "hygiene": all(hygiene["checks"].values()),
    }
    verdicts["overall"] = all(verdicts.values())

    return {
        "file": str(path),
        "words": len(all_words),
        "sentences": len(sentences),
        "paragraphs": sum(1 for b in blocks if b["type"] == "prose"),
        "first_order": first,
        "second_order": second,
        "hygiene": hygiene,
        "warnings": collect_warnings(first, second),
        "verdict": verdicts,
    }


def fmt_check(ok):
    return "PASS" if ok else "FAIL"


def render_markdown(report):
    f = report["first_order"]
    s = report["second_order"]
    h = report["hygiene"]
    v = report["verdict"]
    out = []
    out.append("## Humanise-Copy Detection Report - %s" % report["file"])
    out.append("")
    out.append("%d words, %d sentences, %d paragraphs" % (
        report["words"], report["sentences"], report["paragraphs"]))
    out.append("")
    out.append("### First-order (phrase and lexical) - %s" % fmt_check(v["first_order"]))
    if f["phrases"]:
        for hit in f["phrases"]:
            out.append("- \"%s\" x%d (lines %s)" % (
                hit["phrase"], hit["count"],
                ", ".join(str(n) for n in hit["lines"])))
    else:
        out.append("- No trigger phrases found")
    out.append("- Trigger-word density: %.2f per 1k [%s, limit %.0f]" % (
        f["trigger_density_per_1k"], fmt_check(f["checks"]["trigger_density"]),
        THRESHOLDS["trigger_density_per_1k"]))
    ttr_note = "" if f["ttr_applicable"] else " (n/a under 400 words)"
    out.append("- TTR: %.3f [%s, min %.2f]%s" % (
        f["ttr"], fmt_check(f["checks"]["ttr"]), THRESHOLDS["ttr_min"], ttr_note))
    out.append("- Burstiness (SD/mean): %.3f [%s, min %.2f]" % (
        f["burstiness"], fmt_check(f["checks"]["burstiness"]),
        THRESHOLDS["burstiness_min"]))
    out.append("")
    out.append("### Second-order (structural and rhythmic) - %s" % fmt_check(v["second_order"]))
    out.append("- Question-cadence H2s: %d of %d (%.0f%%) [%s, limit %.0f%%]" % (
        s["h2_questions"], s["h2_total"], s["h2_question_pct"],
        fmt_check(s["checks"]["h2_question_cadence"]),
        THRESHOLDS["h2_question_pct_max"]))
    out.append("- \"Here\" paragraph openers: %d [%s, limit %d]" % (
        len(s["here_openers"]), fmt_check(s["checks"]["here_openers"]),
        THRESHOLDS["here_openers_max"]))
    for hz in s["here_openers"]:
        out.append("    line %d: %s" % (hz["line"], hz["text"]))
    out.append("- Three-clause metronome paragraphs: %d [%s]" % (
        len(s["three_clause_paragraphs"]),
        fmt_check(s["checks"]["three_clause_rhythm"])))
    out.append("- False-balance framings: %.2f per 1k [%s, limit %.0f]" % (
        s["false_balance_per_1k"], fmt_check(s["checks"]["false_balance"]),
        THRESHOLDS["false_balance_per_1k_max"]))
    out.append("- Hedge-stacked windows: %d [%s]" % (
        len(s["hedge_windows"]), fmt_check(s["checks"]["hedge_stacking"])))
    out.append("- Symmetric lists: %d [%s]" % (
        len(s["symmetric_lists"]), fmt_check(s["checks"]["symmetric_lists"])))
    repeat_note = ", verbatim repeat" if s["wrapup_verbatim_repeat"] else ""
    out.append("- Wrap-up questions: %d%s [%s, limit %d, no verbatim repeats]" % (
        len(s["wrapup_questions"]), repeat_note,
        fmt_check(s["checks"]["wrapup_questions"]),
        THRESHOLDS["wrapup_questions_max"]))
    out.append("- Capsule transitions on section openers: %.0f%% [%s, limit %.0f%%]" % (
        s["capsule_opener_pct"], fmt_check(s["checks"]["capsule_transitions"]),
        THRESHOLDS["capsule_opener_pct_max"]))
    out.append("- \"Key insight\" openers: %d [%s]" % (
        len(s["key_insight_openers"]),
        fmt_check(s["checks"]["key_insight_openers"])))
    out.append("- Flat paragraphs (sentence-length SD < %.0f): %d [%s]" % (
        THRESHOLDS["flat_paragraph_sd_min"], len(s["flat_paragraphs"]),
        fmt_check(s["checks"]["flat_paragraphs"])))
    out.append("- Spliced subject triads: %d [%s]" % (
        len(s["spliced_triads"]), fmt_check(s["checks"]["spliced_triads"])))
    for sp in s["spliced_triads"]:
        out.append("    line %d: %s" % (sp["line"], sp["text"]))
    ow_note = "" if s["opening_word_applicable"] else " (n/a under 15 sentences)"
    out.append("- Opening-word top-3 share: %.1f%% [%s, limit %.0f%%]%s" % (
        s["opening_word_top3_pct"],
        fmt_check(s["checks"]["opening_word_repetition"]),
        THRESHOLDS["opening_word_top3_pct_max"], ow_note))
    psd_note = "" if s["paragraph_sd_applicable"] else " (n/a under 8 paragraphs)"
    out.append("- Paragraph-shape SD: %.1f [%s, min %.0f]%s" % (
        s["paragraph_sd"], fmt_check(s["checks"]["paragraph_shape"]),
        THRESHOLDS["paragraph_sd_min"], psd_note))
    out.append("")
    out.append("### Mechanical hygiene - %s" % fmt_check(v["hygiene"]))
    out.append("- Em dashes: %d [%s]" % (h["em_dashes"]["count"], fmt_check(h["checks"]["em_dashes"])))
    out.append("- En dashes: %d [%s]" % (h["en_dashes"]["count"], fmt_check(h["checks"]["en_dashes"])))
    out.append("- Curly punctuation: %d [%s]" % (h["curly_punctuation"]["count"], fmt_check(h["checks"]["curly_punctuation"])))
    out.append("- TM/R/C glyphs: %d [%s]" % (h["tm_r_c_glyphs"]["count"], fmt_check(h["checks"]["glyphs"])))
    out.append("- Ligatures: %d [%s]" % (h["ligatures"]["count"], fmt_check(h["checks"]["ligatures"])))
    out.append("- Colons in headings: %d [%s]" % (h["heading_colons"]["count"], fmt_check(h["checks"]["heading_colons"])))
    out.append("")
    if report["warnings"]:
        out.append("### Borderline (passed, read these aloud)")
        for wn in report["warnings"]:
            detail = ", ".join("%s %s" % (k, v) for k, v in wn.items()
                               if k != "check")
            out.append("- %s (%s)" % (wn["check"], detail))
        out.append("")
    out.append("### Verdict")
    out.append("First-order: %s | Second-order: %s | Hygiene: %s | Overall: %s" % (
        fmt_check(v["first_order"]), fmt_check(v["second_order"]),
        fmt_check(v["hygiene"]), fmt_check(v["overall"])))
    return "\n".join(out)


def main():
    parser = argparse.ArgumentParser(description="Detect AI-generation tells in prose.")
    parser.add_argument("files", nargs="+", help="Markdown or text files to analyse")
    parser.add_argument("--format", choices=["json", "markdown"], default="json")
    parser.add_argument("--gate", action="store_true",
                        help="Exit 1 if any file fails any layer")
    args = parser.parse_args()

    reports = []
    for path in args.files:
        if not Path(path).is_file():
            print("Not a file: %s" % path, file=sys.stderr)
            return 2
        reports.append(analyse_file(path))

    if args.format == "json":
        payload = reports[0] if len(reports) == 1 else reports
        print(json.dumps(payload, indent=2))
    else:
        print("\n\n".join(render_markdown(r) for r in reports))

    if args.gate and any(not r["verdict"]["overall"] for r in reports):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
