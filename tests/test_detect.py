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

    def test_repeated_openers(self):
        # S12: the metronome paragraph opens four sentences running on "The".
        runs = self.second["repeated_openers"]
        self.assertEqual(len(runs), 1)
        self.assertEqual(runs[0]["opener"], "the")
        self.assertEqual(runs[0]["count"], 4)

    def test_signature_so_transition_is_not_an_amputation(self):
        # W2 "So the question becomes," is an iDD signature transition. It
        # carries no ability modal, so the purpose-clause check must leave
        # it alone rather than the skill having to whitelist it back.
        self.assertEqual(len(self.second["amputated_purpose_clauses"]), 0)

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


# Observed agent output (left) and the form the repair should have taken
# (right), lifted from the fleet run's ear-QA findings.

TIC_CONVERGED = (
    "Honestly, the buyer pool here runs deeper than most sellers expect.\n\n"
    "Honestly, the timeline is the part people get wrong.\n\n"
    "Honestly, the price guide is only ever a starting point.\n"
)

TIC_VARIED = (
    "The buyer pool here runs deeper than most sellers expect.\n\n"
    "Timing is the part people get wrong.\n\n"
    "Treat the price guide as a starting point, nothing more.\n"
)

TIC_SINGLE = (
    "Honestly, the buyer pool here runs deeper than most sellers expect.\n\n"
    "Timing is the part people get wrong.\n\n"
    "Treat the price guide as a starting point, nothing more.\n"
)

PURPOSE_AMPUTATED = (
    "We brief the whole team the week before a campaign goes live. "
    "So the team can support them.\n"
)

PURPOSE_ATTACHED = (
    "We brief the whole team the week before a campaign goes live, so the "
    "team can support them.\n"
)

CONSEQUENTIAL_SO = (
    "The premium runs to $4,500 upfront on top of the subscription. "
    "So the question becomes whether a single-chair practice sees it back.\n"
)

STACCATO_CHOPPED = (
    "You want a builder who has done this exact work before, on a block "
    "this steep, inside a budget this tight. In your suburb. On your "
    "budget. Then this is the category.\n"
)

STACCATO_MERGED = (
    "You want a builder who has done this exact work before, on a block "
    "this steep, inside a budget this tight. In your suburb, on your "
    "budget. Then this is the category you are shopping in.\n"
)

ECHO_PAIR = (
    "This guide walks through the five checks that matter before you sign. "
    "This guide assumes you have already had the place valued.\n"
)

ECHO_ANAPHORA = (
    "You get the full written report. You get the comparable sales. "
    "You get the call with our director.\n"
)

ECHO_REPAIRED = (
    "This guide walks through the five checks that matter before you sign. "
    "It assumes you have already had the place valued.\n"
)

# Live specimen: switch-property-managers-qld.md line 56 kept four "Ask"
# openers running after the fleet repair, the ear QA and the detector
# re-run. Document-wide opening-word share read 16.4 percent (PASS) because
# a 1,282-word file dilutes a run that sits inside one paragraph.
OPENER_RUN = (
    "Ask for a real communication standard, committed to in writing. "
    "Ask how they monitor and chase arrears, and how quickly. "
    "Ask how often they inspect and what the written report includes. "
    "Ask whether they review your rent against the market each year.\n"
)

# The same run under a question heading is a self-contained answer block, the
# unit claude-seo's seo-geo skill optimises for (134 to 167 words, extractable
# without context). Parallel imperatives are what makes it liftable. Julian's
# call 2026-07-25: "heading questions for SEO optimisation and ask engine".
OPENER_RUN_ANSWER_BLOCK = (
    "## What should I look for in a new property manager?\n\n"
    "Ask for a real communication standard, committed to in writing. "
    "Ask how they monitor and chase arrears, and how quickly. "
    "Ask how often they inspect and what the written report includes. "
    "Ask whether they review your rent against the market each year.\n"
)

OPENER_RUN_STATEMENT_HEADING = (
    "## Choosing a property manager\n\n"
    "Ask for a real communication standard, committed to in writing. "
    "Ask how they monitor and chase arrears, and how quickly. "
    "Ask how often they inspect and what the written report includes. "
    "Ask whether they review your rent against the market each year.\n"
)

OPENER_RUN_VARIED = (
    "Ask for a real communication standard, committed to in writing. "
    "Find out how they monitor and chase arrears, and how quickly. "
    "Check how often they inspect and what the written report includes. "
    "Confirm they review your rent against the market each year.\n"
)


class TestRepairArtifactChecks(unittest.TestCase):
    """The 2026-07-25 fleet run (eight repair agents, ~620 sentence repairs)
    produced failure modes the detector could not see, because every check it
    had measured the draft rather than the repair. Each sample below is the
    observed agent output; each control is the form the repair should have
    taken. Source: docs/dev/2026-07-25-fleet-run-learnings.md."""

    def run_on(self, text):
        tmp = tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False, encoding="utf-8")
        tmp.write(text)
        tmp.close()
        try:
            return detect.analyse_file(tmp.name)
        finally:
            Path(tmp.name).unlink(missing_ok=True)

    # -- Tic convergence -------------------------------------------------
    # Two agents independently adopted "Honestly," as their replacement
    # opener. One is voice; three is a tic the agent cannot hear.

    def test_repeated_conversational_opener_flags(self):
        r = self.run_on(TIC_CONVERGED)
        tics = r["second_order"]["conversational_tics"]
        self.assertEqual(len(tics), 1)
        self.assertEqual(tics[0]["opener"], "honestly")
        self.assertEqual(tics[0]["count"], 3)
        self.assertFalse(r["second_order"]["checks"]["conversational_tics"])

    def test_varied_openers_clean(self):
        r = self.run_on(TIC_VARIED)
        self.assertEqual(len(r["second_order"]["conversational_tics"]), 0)
        self.assertTrue(r["second_order"]["checks"]["conversational_tics"])

    def test_single_conversational_opener_is_voice(self):
        # One candour opener is a legitimate register choice and must not
        # flag, or the check would punish the voice it exists to protect.
        r = self.run_on(TIC_SINGLE)
        self.assertEqual(len(r["second_order"]["conversational_tics"]), 0)

    # -- Amputated purpose clauses ---------------------------------------
    # ", so the team can support them" split into a standalone sentence.
    # Consequential "So X" is fine; a purpose clause left standing is not.

    def test_amputated_purpose_clause_flags(self):
        r = self.run_on(PURPOSE_AMPUTATED)
        amputated = r["second_order"]["amputated_purpose_clauses"]
        self.assertEqual(len(amputated), 1)
        self.assertIn("So the team can support them", amputated[0]["text"])
        self.assertFalse(r["second_order"]["checks"]["amputated_purpose"])

    def test_attached_purpose_clause_clean(self):
        r = self.run_on(PURPOSE_ATTACHED)
        self.assertEqual(
            len(r["second_order"]["amputated_purpose_clauses"]), 0)

    def test_consequential_so_not_flagged(self):
        # "So the question becomes..." carries no ability modal and is a
        # normal discourse move, not an amputation.
        r = self.run_on(CONSEQUENTIAL_SO)
        self.assertEqual(
            len(r["second_order"]["amputated_purpose_clauses"]), 0)

    # -- Staccato over-splitting -----------------------------------------
    # Trading metronome for chop. Burstiness and paragraph SD both IMPROVE
    # when an agent does this, so the existing variance checks are blind.

    def test_staccato_run_flags(self):
        r = self.run_on(STACCATO_CHOPPED)
        runs = r["second_order"]["staccato_runs"]
        self.assertEqual(len(runs), 1)
        self.assertGreaterEqual(len(runs[0]["lengths"]), 3)
        self.assertFalse(r["second_order"]["checks"]["staccato_runs"])

    def test_staccato_passes_the_variance_checks(self):
        # The point of the check: chopped copy scores WELL on burstiness,
        # which is why it survived the fleet run's detector re-runs.
        r = self.run_on(STACCATO_CHOPPED)
        self.assertTrue(r["first_order"]["checks"]["burstiness"])

    def test_merged_run_clean(self):
        r = self.run_on(STACCATO_MERGED)
        self.assertEqual(len(r["second_order"]["staccato_runs"]), 0)

    # -- Adjacent echoes --------------------------------------------------
    # Agents edit sentence-locally, so consecutive sentences drift into the
    # same opener. A run of exactly two is the local-edit artifact; a run of
    # three or more is deliberate anaphora and stays.

    def test_adjacent_echo_flags(self):
        r = self.run_on(ECHO_PAIR)
        echoes = r["second_order"]["adjacent_echoes"]
        self.assertEqual(len(echoes), 1)
        self.assertEqual(echoes[0]["opener"], "this guide")
        self.assertFalse(r["second_order"]["checks"]["adjacent_echoes"])

    def test_anaphora_run_of_three_not_flagged(self):
        # "You get X. You get Y. You get Z." is conversion technique. The
        # global opening-word check owns genuine overuse; this one must not
        # punish a rhetorical run.
        r = self.run_on(ECHO_ANAPHORA)
        self.assertEqual(len(r["second_order"]["adjacent_echoes"]), 0)

    def test_echo_repaired_clean(self):
        r = self.run_on(ECHO_REPAIRED)
        self.assertEqual(len(r["second_order"]["adjacent_echoes"]), 0)

    # -- Repeated sentence openers ---------------------------------------
    # A run of the same opening verb inside one paragraph. The document-wide
    # opening-word share cannot see it: the run is local, the metric is
    # global. Varied second words mark accidental repetition; identical
    # second words mark deliberate anaphora and stay.

    def test_opener_run_flags(self):
        r = self.run_on(OPENER_RUN)
        runs = r["second_order"]["repeated_openers"]
        self.assertEqual(len(runs), 1)
        self.assertEqual(runs[0]["opener"], "ask")
        self.assertEqual(runs[0]["count"], 4)
        self.assertFalse(r["second_order"]["checks"]["repeated_openers"])

    def test_opener_run_invisible_to_document_wide_share(self):
        # The blind spot that let this survive the fleet run. If this ever
        # starts failing, the global check has changed and this check's
        # justification needs re-reading, not deleting.
        r = self.run_on(OPENER_RUN)
        self.assertTrue(
            r["second_order"]["checks"]["opening_word_repetition"])

    def test_imperative_variety_clean(self):
        # The fleet run's own fix: Request / Find out / Check / Confirm.
        r = self.run_on(OPENER_RUN_VARIED)
        self.assertEqual(len(r["second_order"]["repeated_openers"]), 0)
        self.assertTrue(r["second_order"]["checks"]["repeated_openers"])

    def test_anaphora_not_counted_as_opener_run(self):
        r = self.run_on(ECHO_ANAPHORA)
        self.assertEqual(len(r["second_order"]["repeated_openers"]), 0)

    # -- Answer blocks (GEO) ---------------------------------------------
    # A parallel imperative run under a question heading is extraction
    # structure, not a tell. It still gets surfaced, because "written well"
    # is the condition, but it must not fail the gate.

    def test_answer_block_run_does_not_fail(self):
        r = self.run_on(OPENER_RUN_ANSWER_BLOCK)
        self.assertTrue(r["second_order"]["checks"]["repeated_openers"])
        self.assertEqual(len(r["second_order"]["repeated_openers"]), 0)

    def test_answer_block_run_still_surfaces_as_borderline(self):
        r = self.run_on(OPENER_RUN_ANSWER_BLOCK)
        blocks = r["second_order"]["answer_block_openers"]
        self.assertEqual(len(blocks), 1)
        self.assertEqual(blocks[0]["opener"], "ask")
        self.assertIn("answer_block_opener_run",
                      [w["check"] for w in r["warnings"]])

    def test_same_run_under_a_statement_heading_still_fails(self):
        # The exemption is the answer block, not the sentence shape.
        r = self.run_on(OPENER_RUN_STATEMENT_HEADING)
        self.assertEqual(len(r["second_order"]["repeated_openers"]), 1)
        self.assertFalse(r["second_order"]["checks"]["repeated_openers"])

    def test_opener_run_absorbs_its_inner_echo(self):
        # "Ask how" twice sits inside the "Ask" run. One finding, not two.
        r = self.run_on(OPENER_RUN)
        self.assertEqual(len(r["second_order"]["adjacent_echoes"]), 0)


GEO_PAGE = (
    "## Can I change property managers in Queensland mid-lease?\n\n"
    "Yes. Your management agreement and the tenancy agreement are separate "
    "contracts, so ending one does not disturb the other. Check the notice "
    "period in your current agreement before you sign anything new.\n\n"
    "## Will I lose rent or pay extra fees when I switch?\n\n"
    "Usually not. Rent keeps being collected throughout the handover, and the "
    "bond stays lodged with the Residential Tenancies Authority under the same "
    "tenancy. Ask the incoming agency to confirm its fees in writing.\n\n"
    "## How does the handover work, step by step?\n\n"
    "The incoming agency writes to the outgoing one, collects the ledger, the "
    "bond details, the keys and the inspection history, and introduces itself "
    "to the tenant with new payment instructions.\n"
)


class TestSeoRouting(unittest.TestCase):
    """Question-cadence headings are a tell in a narrative article and the
    whole point of an answer-engine page. The planted fixture and a real
    Ascot insights page BOTH run near 100 percent question headings, so no
    mechanical rule separates them. The detector therefore routes the
    judgment to claude-seo instead of pretending to settle it."""

    def run_on(self, text):
        tmp = tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False, encoding="utf-8")
        tmp.write(text)
        tmp.close()
        try:
            return detect.analyse_file(tmp.name)
        finally:
            Path(tmp.name).unlink(missing_ok=True)

    def test_geo_page_raises_the_routing_signal(self):
        r = self.run_on(GEO_PAGE)
        s = r["second_order"]["seo_signals"]
        self.assertEqual(s["question_heading_pct"], 100.0)
        self.assertEqual(s["answer_blocks"], 3)
        self.assertIn("consult_claude_seo",
                      [w["check"] for w in r["warnings"]])

    def test_question_cadence_still_reports_honestly(self):
        # The check does NOT auto-pass on an answer-engine page. There is no
        # honest mechanical rule separating this from the planted fixture,
        # and inventing one would let real slop through. The detector reports
        # 100 percent truthfully; the routing signal tells the skill to log it
        # as a deliberate keep rather than "repair" the headings.
        r = self.run_on(GEO_PAGE)
        self.assertFalse(r["second_order"]["checks"]["h2_question_cadence"])
        self.assertIn("consult_claude_seo",
                      [w["check"] for w in r["warnings"]])

    def test_routing_signal_touches_no_other_check(self):
        r = self.run_on(GEO_PAGE)
        others = {k: v for k, v in r["second_order"]["checks"].items()
                  if k != "h2_question_cadence"}
        self.assertTrue(all(others.values()), msg=str(others))

    def test_prose_without_question_headings_is_not_routed(self):
        r = self.run_on(ECHO_REPAIRED)
        self.assertNotIn("consult_claude_seo",
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


UNIFORM_PARAGRAPHS = """# Margin Detection After Three Weeks

Margin detection earned its place in a busy list after three weeks of routine crown work and a fair few notes.

The first preparation told us plenty. Amber lit along the distal exactly where a lip of material had been left behind.

Refinement happened before the patient stood up, which is the whole argument for having it read the scan at all.

Deep subgingival margins still defeat it. Retraction cord remains necessary and no algorithm yet invented has fixed wet dentine.

Nurses picked it up faster than I expected, and two of them now run the scan unprompted at every checkup appointment.

Reporting sits in a side panel. That suits me, because what I want is the chairside read rather than another dashboard.

Cost is where the argument gets harder to make cleanly, so judge it on remakes avoided across a quarter rather than on a demo.

My advice is to trial it on posterior singles. Anterior work carries expectations a first trial does not need to carry.

Verdict, then. It is worth the seat if your remake rate sits anywhere near where mine sat before we started.
"""


class TestParagraphShapeIsAdvisory(unittest.TestCase):
    """paragraph_shape is measured and reported but must not gate a verdict.

    It measures the spread of paragraph WORD counts, so it responds to where
    paragraph breaks fall rather than to the prose. A readability pass over 22
    long-form posts that split over-long paragraphs at idea boundaries and
    changed zero words cut the second-order pass rate from 20/22 to 10/22 on
    this check alone. Splitting a wall of text into readable paragraphs must
    never be what fails a document.
    """

    @classmethod
    def setUpClass(cls):
        tmp = tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False, encoding="utf-8")
        tmp.write(UNIFORM_PARAGRAPHS)
        tmp.close()
        try:
            cls.report = detect.analyse_file(tmp.name)
        finally:
            Path(tmp.name).unlink(missing_ok=True)

    def test_paragraph_shape_is_declared_advisory(self):
        self.assertIn("paragraph_shape", detect.ADVISORY_CHECKS)

    def test_check_is_still_measured_and_reported(self):
        # Kept in the checks dict so JSON consumers keep working, and so a
        # genuinely uniform paragraph architecture stays visible.
        self.assertIn("paragraph_shape", self.report["second_order"]["checks"])
        self.assertTrue(self.report["second_order"]["paragraph_sd_applicable"])
        self.assertLess(self.report["second_order"]["paragraph_sd"],
                        detect.THRESHOLDS["paragraph_sd_min"])

    def test_failing_check_does_not_fail_the_layer(self):
        self.assertFalse(self.report["second_order"]["checks"]["paragraph_shape"])
        self.assertTrue(self.report["verdict"]["second_order"], msg=str(self.report))
        self.assertTrue(self.report["verdict"]["overall"], msg=str(self.report))

    def test_below_floor_raises_an_advisory_warning(self):
        warn = [w for w in self.report["warnings"]
                if w["check"] == "paragraph_shape_advisory"]
        self.assertEqual(len(warn), 1)
        self.assertEqual(warn[0]["floor"], detect.THRESHOLDS["paragraph_sd_min"])

    def test_markdown_labels_it_advisory_not_fail(self):
        line = [ln for ln in detect.render_markdown(self.report).splitlines()
                if ln.startswith("- Paragraph-shape SD:")]
        self.assertEqual(len(line), 1)
        self.assertIn("ADVISORY", line[0])
        self.assertNotIn("FAIL", line[0])

    def test_gate_exit_code_ignores_advisory(self):
        # --gate exits 1 on a failing layer; an advisory check alone must not
        # trip it, or CI would block on paragraph breaks.
        self.assertTrue(all(self.report["verdict"][k]
                            for k in ("first_order", "second_order", "hygiene")))


PARALLEL_INSTRUCTIONS = """# Five Checks Before You Cement

Before anything goes in permanently there are five simple checks that save most of the remakes I used to see, and not one of them takes long enough to matter on a busy list.

Check the margin under magnification first. Confirm the contact with floss, not by eye. Seat the restoration dry and watch the tissue. Ask the patient to close and listen. Photograph the shade against the adjacent tooth.

Cement choice comes after all five and never before, and the order matters a good deal more than most people expect when they are already running late.
"""


class TestFlatParagraphsIsAdvisory(unittest.TestCase):
    """flat_paragraphs is measured and reported but must not gate a verdict.

    It measures the spread of SENTENCE lengths inside a paragraph, and
    over-fires on parallel instructional lists: a stated count ("five simple
    checks") followed by exactly that many items, uniform in length by design.
    Merging any item breaks the stated count, so the only honest resolution is
    a deliberate keep - which means the check was asking for an edit that must
    not be made. Three of the 22 ASDE launch posts carry exactly that keep.
    """

    @classmethod
    def setUpClass(cls):
        tmp = tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False, encoding="utf-8")
        tmp.write(PARALLEL_INSTRUCTIONS)
        tmp.close()
        try:
            cls.report = detect.analyse_file(tmp.name)
        finally:
            Path(tmp.name).unlink(missing_ok=True)

    def test_flat_paragraphs_is_declared_advisory(self):
        self.assertIn("flat_paragraphs", detect.ADVISORY_CHECKS)

    def test_the_fixture_isolates_this_check(self):
        # If any other gating check also failed here, every assertion below
        # would pass for the wrong reason.
        failing = [n for n, ok
                   in self.report["second_order"]["checks"].items()
                   if not ok and n not in detect.ADVISORY_CHECKS]
        self.assertEqual(failing, [], msg=str(self.report["second_order"]["checks"]))

    def test_check_is_still_measured_and_reported(self):
        # Kept in the checks dict so JSON consumers keep working, and so a
        # genuinely flat run of sentences stays visible to a human.
        self.assertIn("flat_paragraphs", self.report["second_order"]["checks"])
        self.assertEqual(len(self.report["second_order"]["flat_paragraphs"]), 1)

    def test_failing_check_does_not_fail_the_layer(self):
        self.assertFalse(self.report["second_order"]["checks"]["flat_paragraphs"])
        self.assertTrue(self.report["verdict"]["second_order"], msg=str(self.report))
        self.assertTrue(self.report["verdict"]["overall"], msg=str(self.report))

    def test_it_raises_an_advisory_warning(self):
        warn = [w for w in self.report["warnings"]
                if w["check"] == "flat_paragraphs_advisory"]
        self.assertEqual(len(warn), 1)
        self.assertEqual(warn[0]["count"], 1)
        self.assertEqual(warn[0]["floor"],
                         detect.THRESHOLDS["flat_paragraph_sd_min"])

    def test_markdown_labels_it_advisory_not_fail(self):
        line = [ln for ln in detect.render_markdown(self.report).splitlines()
                if ln.startswith("- Flat paragraphs")]
        self.assertEqual(len(line), 1)
        self.assertIn("ADVISORY", line[0])
        self.assertNotIn("FAIL", line[0])

    def test_gate_exit_code_ignores_advisory(self):
        self.assertTrue(all(self.report["verdict"][k]
                            for k in ("first_order", "second_order", "hygiene")))


class TestAdvisoryDoesNotMaskRealFailures(unittest.TestCase):
    """The fixture must still fail second-order on its genuine tells."""

    @classmethod
    def setUpClass(cls):
        cls.report = detect.analyse_file(FIXTURE)

    def test_fixture_still_fails_second_order(self):
        self.assertFalse(self.report["verdict"]["second_order"])

    def test_failure_is_driven_by_gating_checks_not_advisory_ones(self):
        failing = [name for name, ok
                   in self.report["second_order"]["checks"].items()
                   if not ok and name not in detect.ADVISORY_CHECKS]
        self.assertTrue(failing, msg="fixture must fail on real, gating tells")

    def test_demotion_left_the_layer_with_real_teeth(self):
        # Guard against future over-demotion. Every check moved into
        # ADVISORY_CHECKS narrows what can fail. If that set ever grows to the
        # point where the reference AI-slop draft nearly passes, the detector
        # has stopped detecting, and a green verdict becomes false confidence -
        # which is worse than no verdict at all. 12 gating tells still fired
        # here at 0.5.0; this asserts a floor well under that, so a deliberate
        # demotion is easy and an accidental gutting is not.
        failing = [name for name, ok
                   in self.report["second_order"]["checks"].items()
                   if not ok and name not in detect.ADVISORY_CHECKS]
        self.assertGreaterEqual(
            len(failing), 8,
            msg="ADVISORY_CHECKS has grown too far: only %d gating tells still "
                "fire on the reference slop draft (%s)" % (len(failing), failing))


if __name__ == "__main__":
    unittest.main()
