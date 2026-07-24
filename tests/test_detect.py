#!/usr/bin/env python3
"""Unit tests for scripts/detect.py against the planted fixture.

The fixture at tests/fixtures/idd-draft-sloppy.md carries a documented plant
inventory (tests/EXPECTED-FINDINGS.md). These tests pin the detector to that
ground truth, plus one clean human-shaped sample that must pass every layer.

Run from the repo root:
    python3 -m unittest discover tests -v
"""

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import detect  # noqa: E402

FIXTURE = ROOT / "tests" / "fixtures" / "idd-draft-sloppy.md"

CLEAN_SAMPLE = """# Margin Detection In Daily Use

We ran the module chairside for three weeks. Short version, it earns its seat.

The first crown prep told the story. I scanned, the margin lit up amber where I had left a lip on the distal, and I refined it before the patient left the chair. One remake avoided pays for a month of the subscription.

## Where It Struggles

Deep subgingival margins still beat it. Retraction cord remains your friend, and no software fixes wet dentine.

My advice? Trial it on posterior singles and judge it on remakes, not the demo.
"""


class TestFixtureDetection(unittest.TestCase):
    """Every planted tell must be caught; whitelisted items must be visible."""

    @classmethod
    def setUpClass(cls):
        cls.report = detect.analyse_file(FIXTURE)
        cls.first = cls.report["first_order"]
        cls.second = cls.report["second_order"]
        cls.hygiene = cls.report["hygiene"]

    def phrase_counts(self):
        return {h["phrase"]: h["count"] for h in self.first["phrases"]}

    def test_all_three_layers_fail(self):
        v = self.report["verdict"]
        self.assertFalse(v["first_order"])
        self.assertFalse(v["second_order"])
        self.assertFalse(v["hygiene"])
        self.assertFalse(v["overall"])

    def test_first_order_phrases(self):
        phrases = self.phrase_counts()
        self.assertIn("delve into", phrases)
        self.assertIn("harness the power", phrases)
        self.assertIn("unlock the full potential", phrases)
        self.assertIn("paradigm shift", phrases)
        self.assertEqual(phrases.get("game-changer"), 2)
        self.assertEqual(phrases.get("seamlessly"), 2)

    def test_trigger_density_fails(self):
        self.assertGreater(self.first["trigger_density_per_1k"], 5.0)
        self.assertFalse(self.first["checks"]["trigger_density"])

    def test_h2_question_cadence(self):
        self.assertEqual(self.second["h2_total"], 4)
        self.assertEqual(self.second["h2_questions"], 4)
        self.assertFalse(self.second["checks"]["h2_question_cadence"])

    def test_here_openers_include_signature(self):
        openers = self.second["here_openers"]
        self.assertEqual(len(openers), 3)
        texts = " | ".join(o["text"] for o in openers)
        # The signature phrase must be visible so the editorial layer can
        # whitelist it rather than the script silently deciding.
        self.assertIn("Here's the thing", texts)

    def test_three_clause_metronome(self):
        self.assertEqual(len(self.second["three_clause_paragraphs"]), 1)

    def test_false_balance(self):
        self.assertEqual(len(self.second["false_balance"]), 2)
        self.assertFalse(self.second["checks"]["false_balance"])

    def test_hedge_stacking(self):
        self.assertEqual(len(self.second["hedge_windows"]), 2)

    def test_symmetric_list(self):
        lists = self.second["symmetric_lists"]
        self.assertEqual(len(lists), 1)
        self.assertEqual(lists[0]["items"], 4)

    def test_wrapup_verbatim_repeat_fails(self):
        self.assertEqual(len(self.second["wrapup_questions"]), 2)
        self.assertTrue(self.second["wrapup_verbatim_repeat"])
        self.assertFalse(self.second["checks"]["wrapup_questions"])

    def test_capsule_transitions(self):
        self.assertEqual(self.second["capsule_opener_pct"], 75.0)
        self.assertFalse(self.second["checks"]["capsule_transitions"])

    def test_key_insight_opener(self):
        self.assertEqual(len(self.second["key_insight_openers"]), 1)

    def test_spliced_triads(self):
        # The four planted metronome sentences each restate "it" twice
        # across comma splices.
        self.assertEqual(len(self.second["spliced_triads"]), 4)

    def test_hygiene_counts(self):
        self.assertEqual(self.hygiene["em_dashes"]["count"], 4)
        self.assertEqual(self.hygiene["curly_punctuation"]["count"], 1)
        self.assertEqual(self.hygiene["en_dashes"]["count"], 0)
        self.assertEqual(self.hygiene["tm_r_c_glyphs"]["count"], 0)
        self.assertEqual(self.hygiene["heading_colons"]["count"], 0)


ASCOT_LEAD_ORIGINAL = (
    "Most building projects go wrong in the paperwork, not the construction. "
    "Our process exists to stop that. It runs in a fixed order, it puts "
    "everything in writing, and it ends with a building the certifier has "
    "signed off, at the price we agreed at the start.\n"
)

ASCOT_LEAD_REPAIRED = (
    "Most building projects go wrong in the paperwork, not the construction. "
    "Our process exists to stop that. It runs in a fixed order, everything "
    "goes in writing, and it finishes with a certified building at the price "
    "we agreed at the start.\n"
)


class TestSplicedTriadRegression(unittest.TestCase):
    """Julian's ear caught this sentence on real copy after the detector and
    an eyes-on pass both missed it. The restated-pronoun splice is now a
    check; the repaired form must stay clean."""

    def run_on(self, text):
        tmp = tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False, encoding="utf-8")
        tmp.write(text)
        tmp.close()
        try:
            return detect.analyse_file(tmp.name)
        finally:
            Path(tmp.name).unlink(missing_ok=True)

    def test_original_lead_flags(self):
        r = self.run_on(ASCOT_LEAD_ORIGINAL)
        triads = r["second_order"]["spliced_triads"]
        self.assertEqual(len(triads), 1)
        self.assertIn("It runs in a fixed order", triads[0]["text"])

    def test_repaired_lead_clean(self):
        r = self.run_on(ASCOT_LEAD_REPAIRED)
        self.assertEqual(len(r["second_order"]["spliced_triads"]), 0)

    def test_repaired_lead_surfaces_as_borderline(self):
        # The repaired lead sits at 1 of 3 multi-clause sentences (0.33),
        # under the 0.5 gate. It must pass the check but appear in the
        # borderline warnings so a human reads it aloud.
        r = self.run_on(ASCOT_LEAD_REPAIRED)
        self.assertTrue(r["second_order"]["checks"]["three_clause_rhythm"])
        self.assertIn("three_clause_borderline",
                      [w["check"] for w in r["warnings"]])


class TestCleanSamplePasses(unittest.TestCase):
    """Human-shaped writing must not trip the detector."""

    @classmethod
    def setUpClass(cls):
        tmp = tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False, encoding="utf-8")
        tmp.write(CLEAN_SAMPLE)
        tmp.close()
        cls.path = tmp.name
        cls.report = detect.analyse_file(cls.path)

    @classmethod
    def tearDownClass(cls):
        Path(cls.path).unlink(missing_ok=True)

    def test_overall_pass(self):
        self.assertTrue(self.report["verdict"]["overall"],
                        msg=str(self.report))

    def test_short_doc_guards(self):
        self.assertFalse(self.report["first_order"]["ttr_applicable"])
        self.assertFalse(self.report["second_order"]["opening_word_applicable"])
        self.assertFalse(self.report["second_order"]["paragraph_sd_applicable"])

    def test_borderline_warnings_are_advisory(self):
        # The crown-prep paragraph carries one long multi-clause sentence in
        # three (0.33): a borderline warning, and the verdict stays PASS.
        self.assertIn("three_clause_borderline",
                      [w["check"] for w in self.report["warnings"]])
        self.assertTrue(self.report["verdict"]["overall"])


if __name__ == "__main__":
    unittest.main()
