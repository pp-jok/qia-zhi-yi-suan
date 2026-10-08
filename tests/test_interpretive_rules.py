from dataclasses import replace
from decimal import Decimal
import json
from pathlib import Path

import pytest
import yaml

from destiny_personality.calculation import (
    AstrologyAspectFact,
    BaziRelationFact,
    DignityFact,
    FactMode,
    HiddenStemsFact,
    PillarPosition,
    TenGodFact,
    TenGodSourceKind,
)
from destiny_personality.deterministic_facts_codec import (
    deterministic_facts_fingerprint,
    deterministic_facts_to_dict,
    load_qualified_deterministic_facts,
)
from destiny_personality.interpretive_rules import (
    extract_interpretive_signals,
    load_interpretive_rule_bundle,
)
from destiny_personality.interpretive_profile import build_interpretive_core_profile
from destiny_personality.interpretive_report import (
    _render_interpretive_report,
    build_interpretive_report,
)


FIXTURE_PATH = (
    Path(__file__).parent / "fixtures" / "interpretive" / "extraction_cases_v1.yaml"
)
RULE_PATH = (
    Path(__file__).parents[1]
    / "src"
    / "destiny_personality"
    / "interpretive_assets"
    / "v1"
    / "interpretive_rules_v1.yaml"
)
TEN_GODS = {
    "比肩",
    "劫财",
    "食神",
    "伤官",
    "正财",
    "偏财",
    "正官",
    "七杀",
    "正印",
    "偏印",
}
CORE_PLANETS = {"Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn"}


@pytest.fixture(scope="module")
def extraction_cases():
    return yaml.safe_load(FIXTURE_PATH.read_text(encoding="utf-8"))["cases"]


def _qualified_interpretive_facts(qualified_facts, tmp_path, case):
    facts = qualified_facts.facts
    bazi = replace(
        facts.bazi,
        hidden_stems=(HiddenStemsFact(PillarPosition.YEAR, ("癸",)),),
        ten_gods=(
            TenGodFact(
                "day_master",
                "正印",
                (PillarPosition.YEAR,),
                TenGodSourceKind.VISIBLE_STEM,
            ),
            TenGodFact(
                "day_master",
                "正财",
                (PillarPosition.MONTH,),
                TenGodSourceKind.VISIBLE_STEM,
            ),
        ),
        relations=(
            BaziRelationFact(
                "combination",
                ("year.branch", "month.branch"),
                (PillarPosition.YEAR, PillarPosition.MONTH),
                "test-rule-v1",
            ),
        ),
    )
    if case.get("matching_values", True) is False:
        bazi = replace(
            bazi,
            hidden_stems=(HiddenStemsFact(PillarPosition.YEAR, ("甲",)),),
            ten_gods=(
                TenGodFact(
                    "day_master",
                    "正财",
                    (PillarPosition.YEAR,),
                    TenGodSourceKind.VISIBLE_STEM,
                ),
            ),
            relations=(
                BaziRelationFact(
                    "clash",
                    ("year.branch", "month.branch"),
                    (PillarPosition.YEAR, PillarPosition.MONTH),
                    "test-rule-v1",
                ),
            ),
        )
    if case["time_available"]:
        normalized_time = facts.normalized_time
        astrology = replace(
            facts.astrology,
            placements=tuple(
                replace(placement, sign="Taurus")
                if (
                    placement.body == "Sun"
                    and case.get("matching_values", True) is False
                )
                else placement
                for placement in facts.astrology.placements
            ),
            aspects=(
                AstrologyAspectFact(
                    "Moon" if case.get("reversed_aspect", False) else "Sun",
                    "Sun" if case.get("reversed_aspect", False) else "Moon",
                    "opposition" if case.get("matching_values", True) is False else "conjunction",
                    Decimal("0"),
                ),
            ),
            dignities=(
                DignityFact(
                    "Sun",
                    "detriment" if case.get("matching_values", True) is False else "domicile",
                ),
            ),
        )
    else:
        normalized_time = replace(
            facts.normalized_time,
            historical_civil_time=None,
            local_standard_time=None,
            utc_time=None,
            true_solar_time=None,
            fact_mode=FactMode.STABLE_ONLY,
            sensitivity_reasons=("birth_time_unknown",),
        )
        bazi = replace(bazi, hour_pillar=None)
        astrology = replace(
            facts.astrology,
            placements=tuple(
                replace(placement, house=None)
                for placement in facts.astrology.placements
            ),
            ascendant=None,
            mc=None,
            house_cusps=(),
            aspects=(
                AstrologyAspectFact("Sun", "Moon", "conjunction", Decimal("0")),
            ),
            dignities=(DignityFact("Sun", "domicile"),),
        )
    facts = facts.__class__(normalized_time, bazi, astrology)
    payload = deterministic_facts_to_dict(facts)
    payload.update(
        {
            "schema_version": "deterministic-facts-v1",
            "fact_mode": facts.normalized_time.fact_mode.value,
            "methodology_versions": {
                "bazi": facts.bazi.methodology_version,
                "astrology": facts.astrology.methodology_version,
            },
            "provenance_refs": ["test:interpretive-facts"],
            "validation_summary": {"structure": "passed"},
        }
    )
    qualification = {
        "schema_version": "fact-qualification-v1",
        "fact_fingerprint": deterministic_facts_fingerprint(facts),
        "qualification_status": "passed",
        "derived_fact_assurance": "capability_reported",
        "fact_contract_version": "deterministic-facts-v1",
        "methodology_versions": payload["methodology_versions"],
        "validation_refs": ["test:validation"],
        "provenance_refs": ["test:provenance"],
        "calculation_envelope_refs": ["test:envelope"],
        "comparison": {"required": False, "status": "not_required"},
        "validation_summary": {
            "structure": "passed",
            "methodology": "passed",
            "provenance": "passed",
            "internal_consistency": "passed",
            "time_scope": "passed",
            "calculation_config": "not_available",
        },
    }
    facts_path = tmp_path / "interpretive-facts.json"
    qualification_path = tmp_path / "interpretive-qualification.json"
    facts_path.write_text(json.dumps(payload), encoding="utf-8")
    qualification_path.write_text(json.dumps(qualification), encoding="utf-8")
    return load_qualified_deterministic_facts(facts_path, qualification_path)


@pytest.fixture
def qualified_interpretive_facts(qualified_facts, tmp_path, extraction_cases):
    return _qualified_interpretive_facts(
        qualified_facts, tmp_path, extraction_cases["known_time"]
    )


@pytest.fixture
def missing_time_interpretive_facts(qualified_facts, tmp_path, extraction_cases):
    return _qualified_interpretive_facts(
        qualified_facts, tmp_path, extraction_cases["missing_time"]
    )


@pytest.fixture
def non_matching_interpretive_facts(qualified_facts, tmp_path, extraction_cases):
    return _qualified_interpretive_facts(
        qualified_facts, tmp_path, extraction_cases["non_matching_values"]
    )


@pytest.fixture
def reversed_aspect_interpretive_facts(qualified_facts, tmp_path, extraction_cases):
    return _qualified_interpretive_facts(
        qualified_facts, tmp_path, extraction_cases["reversed_aspect"]
    )


def test_rule_bundle_is_versioned_and_contains_both_systems():
    bundle = load_interpretive_rule_bundle()

    assert bundle.bundle_version == "audited-interpretive-rules-v2"
    assert {rule.system for rule in bundle.rules} == {"bazi", "astrology"}


def test_v060_rule_families_cover_all_ten_gods_and_core_planets():
    bundle = load_interpretive_rule_bundle()

    assert TEN_GODS <= bundle.covered_ten_gods
    assert CORE_PLANETS <= bundle.covered_planets


def test_no_rule_requires_a_demo_specific_full_configuration():
    raw_rules = yaml.safe_load(RULE_PATH.read_text(encoding="utf-8"))["rules"]

    assert all("requires_exact_demo_chart" not in rule for rule in raw_rules)
    assert all(
        not rule.requires_exact_demo_chart
        for rule in load_interpretive_rule_bundle().rules
    )


def test_v060_rule_families_expose_bounded_selectors_and_chinese_narrative_fields():
    bundle = load_interpretive_rule_bundle()
    predicate_families = {
        predicate.fact_ref
        for rule in bundle.rules
        for predicate in rule.value_predicates
    }

    assert {
        "bazi.ten_god.day_master_relation",
        "bazi.branch_relation",
        "astrology.sign_element",
        "astrology.sign_modality",
        "astrology.house_placement",
        "astrology.aspect",
        "astrology.essential_dignity",
    } <= predicate_families
    assert all(rule.family for rule in bundle.rules)
    assert all(rule.mechanism and rule.likely_expression for rule in bundle.rules)
    assert all(rule.contexts for rule in bundle.rules)
    assert any(
        predicate.participants
        for rule in bundle.rules
        for predicate in rule.value_predicates
        if predicate.fact_ref == "bazi.branch_relation"
    )
    assert all(
        any("\u4e00" <= character <= "\u9fff" for character in rule.interpretation)
        and any("\u4e00" <= character <= "\u9fff" for character in rule.mechanism)
        and any("\u4e00" <= character <= "\u9fff" for character in rule.likely_expression)
        for rule in bundle.rules
    )


def test_rule_bundle_defines_a_value_matched_cross_system_tension_pair():
    rules = {
        rule.signal_id: rule for rule in load_interpretive_rule_bundle().rules
    }
    bazi = rules["BAZI-TEN-GOD-EXPRESSION"]
    astrology = rules["ASTROLOGY-PLANET-SIGN-EXPRESSION"]

    assert bazi.topic == astrology.topic == "style of expression"
    assert {bazi.direction, astrology.direction} == {"reflective", "outward"}
    assert bazi.value_predicates
    assert astrology.value_predicates


def test_extraction_emits_traceable_bazi_and_astrology_signals(
    qualified_interpretive_facts, extraction_cases
):
    signals = extract_interpretive_signals(qualified_interpretive_facts)

    assert {signal.system for signal in signals} == {"bazi", "astrology"}
    assert set(
        extraction_cases["known_time"]["expected_signal_ids"]
    ) <= {signal.signal_id for signal in signals}
    assert all(signal.fact_refs and signal.traditional_rule_ref for signal in signals)
    assert all(
        reference.startswith(("bazi.", "astrology."))
        for signal in signals
        for reference in signal.fact_refs
    )
    ten_god_signal = next(
        signal for signal in signals if signal.signal_id == "BAZI-TEN-GOD-EXPRESSION"
    )
    assert "bazi.ten_gods[0].ten_god" in ten_god_signal.fact_refs
    assert "bazi.ten_gods[1].ten_god" not in ten_god_signal.fact_refs


def test_extraction_requires_matching_value_predicates(non_matching_interpretive_facts):
    signals = extract_interpretive_signals(non_matching_interpretive_facts)

    signal_ids = {signal.signal_id for signal in signals}
    assert "BAZI-TEN-GOD-EXPRESSION" not in signal_ids
    assert "ASTROLOGY-PLANET-SIGN-EXPRESSION" in signal_ids


def test_reusable_rules_preserve_exact_matched_values_for_narrative_selection(
    qualified_interpretive_facts,
    non_matching_interpretive_facts,
):
    def matched(signal_id, qualified):
        signal = next(
            item
            for item in extract_interpretive_signals(qualified)
            if item.signal_id == signal_id
        )
        return {
            (item.fact_ref, item.value)
            for item in signal.matched_values
        }

    assert matched(
        "ASTROLOGY-PLANET-SIGN-EXPRESSION", qualified_interpretive_facts
    ) == {
        ("astrology.sign_element", "fire"),
        ("astrology.sign_modality", "cardinal"),
    }
    assert matched(
        "ASTROLOGY-PLANET-SIGN-EXPRESSION", non_matching_interpretive_facts
    ) == {
        ("astrology.sign_element", "earth"),
        ("astrology.sign_modality", "fixed"),
    }
    assert matched("BAZI-TEN-GOD-EXPRESSION", qualified_interpretive_facts) == {
        ("bazi.ten_god.day_master_relation", "正印")
    }


def test_extraction_makes_matched_astrology_values_reader_visible(
    qualified_interpretive_facts,
    non_matching_interpretive_facts,
):
    def interpretations(qualified):
        return {
            signal.signal_id: signal.interpretation
            for signal in extract_interpretive_signals(qualified)
        }

    known = interpretations(qualified_interpretive_facts)
    changed = interpretations(non_matching_interpretive_facts)

    assert "火象" in known["ASTROLOGY-PLANET-SIGN-EXPRESSION"]
    assert "开创" in known["ASTROLOGY-PLANET-SIGN-EXPRESSION"]
    assert "土象" in changed["ASTROLOGY-PLANET-SIGN-EXPRESSION"]
    assert "固定" in changed["ASTROLOGY-PLANET-SIGN-EXPRESSION"]
    assert (
        known["ASTROLOGY-PLANET-SIGN-EXPRESSION"]
        != changed["ASTROLOGY-PLANET-SIGN-EXPRESSION"]
    )
    assert "第1宫" in known["ASTROLOGY-SUN-HOUSE-CONTEXT"]
    assert "合相" in known["ASTROLOGY-ASPECT-DIGNITY-CONTEXT"]
    assert "入庙" in known["ASTROLOGY-SUN-DIGNITY-CONTEXT"]
    assert "对冲" in changed["ASTROLOGY-ASPECT-DIGNITY-CONTEXT"]
    assert "失势" in changed["ASTROLOGY-SUN-DIGNITY-CONTEXT"]


def test_qualified_facts_pipeline_keeps_changed_family_evidence_reader_visible(
    qualified_facts,
    tmp_path,
    extraction_cases,
):
    """The public report must reflect qualified fixture mutations, not rule defaults."""

    known_path = tmp_path / "known"
    changed_path = tmp_path / "changed"
    known_path.mkdir()
    changed_path.mkdir()
    known_facts = _qualified_interpretive_facts(
        qualified_facts, known_path, extraction_cases["known_time"]
    )
    changed_facts = _qualified_interpretive_facts(
        qualified_facts,
        changed_path,
        extraction_cases["non_matching_values"],
    )

    def public_pipeline(facts):
        signals = extract_interpretive_signals(facts)
        profile = build_interpretive_core_profile(facts)
        report = build_interpretive_report(facts, "standard")

        assert signals
        assert profile.conclusions
        assert report.sections
        assert report == _render_interpretive_report(profile, "standard")
        return signals, report

    known_signals, known_report = public_pipeline(known_facts)
    changed_signals, changed_report = public_pipeline(changed_facts)

    def evidence(report, signal_id):
        return "".join(
            section.content
            for section in report.sections
            if signal_id in section.signal_ids
        )

    assert {
        (item.signal_id, tuple(value.value for value in item.matched_values))
        for item in known_signals
        if item.signal_id in {
            "BAZI-TEN-GOD-EXPRESSION",
            "BAZI-RELATION-DYNAMICS",
            "ASTROLOGY-PLANET-SIGN-EXPRESSION",
            "ASTROLOGY-ASPECT-DIGNITY-CONTEXT",
        }
    } == {
        ("BAZI-TEN-GOD-EXPRESSION", ("正印",)),
        ("BAZI-RELATION-DYNAMICS", ("combination",)),
        ("ASTROLOGY-PLANET-SIGN-EXPRESSION", ("fire", "cardinal")),
        ("ASTROLOGY-ASPECT-DIGNITY-CONTEXT", ("conjunction",)),
    }
    assert {
        (item.signal_id, tuple(value.value for value in item.matched_values))
        for item in changed_signals
        if item.signal_id in {
            "BAZI-TEN-GOD-WEALTH",
            "BAZI-RELATION-DYNAMICS",
            "ASTROLOGY-PLANET-SIGN-EXPRESSION",
            "ASTROLOGY-ASPECT-DIGNITY-CONTEXT",
        }
    } == {
        ("BAZI-TEN-GOD-WEALTH", ("正财",)),
        ("BAZI-RELATION-DYNAMICS", ("clash",)),
        ("ASTROLOGY-PLANET-SIGN-EXPRESSION", ("earth", "fixed")),
        ("ASTROLOGY-ASPECT-DIGNITY-CONTEXT", ("opposition",)),
    }

    assert "火象" in evidence(known_report, "ASTROLOGY-PLANET-SIGN-EXPRESSION")
    assert "土象" in evidence(changed_report, "ASTROLOGY-PLANET-SIGN-EXPRESSION")
    assert "合相" in evidence(known_report, "ASTROLOGY-ASPECT-DIGNITY-CONTEXT")
    assert "对冲" in evidence(changed_report, "ASTROLOGY-ASPECT-DIGNITY-CONTEXT")
    assert "正印" in evidence(known_report, "BAZI-TEN-GOD-EXPRESSION")
    assert "正财" in evidence(changed_report, "BAZI-TEN-GOD-WEALTH")
    assert "合" in evidence(known_report, "BAZI-RELATION-DYNAMICS")
    assert "冲" in evidence(changed_report, "BAZI-RELATION-DYNAMICS")
    assert "combination" not in evidence(known_report, "BAZI-RELATION-DYNAMICS")
    assert "clash" not in evidence(changed_report, "BAZI-RELATION-DYNAMICS")


def test_ten_god_repetition_requires_the_same_identity(
    qualified_interpretive_facts,
):
    signal_ids = {
        signal.signal_id
        for signal in extract_interpretive_signals(qualified_interpretive_facts)
    }

    assert "BAZI-TEN-GOD-REPETITION" not in signal_ids


def test_extraction_matches_reversed_aspect_bodies(reversed_aspect_interpretive_facts):
    signals = extract_interpretive_signals(reversed_aspect_interpretive_facts)

    aspect_signal = next(
        signal
        for signal in signals
        if signal.signal_id == "ASTROLOGY-ASPECT-DIGNITY-CONTEXT"
    )
    assert aspect_signal.fact_refs == ("astrology.aspects[0].aspect_type",)
    dignity_signal = next(
        signal
        for signal in signals
        if signal.signal_id == "ASTROLOGY-SUN-DIGNITY-CONTEXT"
    )
    assert dignity_signal.fact_refs == ("astrology.dignities[0].dignity",)


def test_missing_time_skips_house_and_angle_rules(
    missing_time_interpretive_facts, extraction_cases
):
    signals = extract_interpretive_signals(missing_time_interpretive_facts)

    assert set(
        extraction_cases["missing_time"]["expected_signal_ids"]
    ) <= {signal.signal_id for signal in signals}
    assert all("house" not in signal.signal_id.lower() for signal in signals)
    assert all("angle" not in signal.signal_id.lower() for signal in signals)
    assert all(
        ".house" not in reference
        and ".ascendant" not in reference
        and ".mc" not in reference
        for signal in signals
        for reference in signal.fact_refs
    )


def test_rule_loader_rejects_unknown_confidence(tmp_path: Path):
    payload = yaml.safe_load(RULE_PATH.read_text(encoding="utf-8"))
    payload["rules"][0]["confidence"] = "certain"
    (tmp_path / "interpretive_rules_v1.yaml").write_text(
        yaml.safe_dump(payload, allow_unicode=True), encoding="utf-8"
    )

    with pytest.raises(ValueError, match="INTERPRETIVE_RULE_INVALID_CONFIDENCE"):
        load_interpretive_rule_bundle(tmp_path)


@pytest.mark.parametrize(
    ("fact_refs", "error"),
    [
        ("[ten_god]", "INTERPRETIVE_RULE_INVALID_FACT_REF"),
        ("[astrology.aspect]", "INTERPRETIVE_RULE_INVALID_FACT_REF"),
        ("[]", "INTERPRETIVE_RULE_INVALID_PROVENANCE"),
    ],
)
def test_rule_loader_rejects_unqualified_or_wrong_system_fact_references(
    tmp_path: Path, fact_refs: str, error: str
):
    payload = yaml.safe_load(RULE_PATH.read_text(encoding="utf-8"))
    payload["rules"][0]["fact_refs"] = yaml.safe_load(fact_refs)
    (tmp_path / "interpretive_rules_v1.yaml").write_text(
        yaml.safe_dump(payload, allow_unicode=True), encoding="utf-8"
    )

    with pytest.raises(ValueError, match=error):
        load_interpretive_rule_bundle(tmp_path)


def test_rule_loader_rejects_unsupported_predicate_value(tmp_path: Path):
    payload = yaml.safe_load(RULE_PATH.read_text(encoding="utf-8"))
    payload["rules"][0]["value_predicates"][0]["values"] = ["resource"]
    (tmp_path / "interpretive_rules_v1.yaml").write_text(
        yaml.safe_dump(payload, allow_unicode=True), encoding="utf-8"
    )

    with pytest.raises(ValueError, match="INTERPRETIVE_RULE_INVALID_PREDICATE_VALUE"):
        load_interpretive_rule_bundle(tmp_path)


def test_rule_loader_structurally_rejects_single_sign_configuration(tmp_path: Path):
    payload = yaml.safe_load(RULE_PATH.read_text(encoding="utf-8"))
    rule = next(
        item
        for item in payload["rules"]
        if item["signal_id"] == "ASTROLOGY-PLANET-SIGN-EXPRESSION"
    )
    rule["value_predicates"][0]["values"] = ["fire"]
    rule["value_predicates"][1]["values"] = ["cardinal"]
    (tmp_path / "interpretive_rules_v1.yaml").write_text(
        yaml.safe_dump(payload, allow_unicode=True), encoding="utf-8"
    )

    with pytest.raises(ValueError, match="INTERPRETIVE_RULE_DEMO_SPECIFIC"):
        load_interpretive_rule_bundle(tmp_path)


def test_rule_loader_rejects_duplicate_predicate_values_that_bypass_demo_guard(
    tmp_path: Path,
):
    payload = yaml.safe_load(RULE_PATH.read_text(encoding="utf-8"))
    rule = next(
        item
        for item in payload["rules"]
        if item["signal_id"] == "ASTROLOGY-PLANET-SIGN-EXPRESSION"
    )
    rule["value_predicates"][0]["values"] = ["fire", "fire"]
    rule["value_predicates"][1]["values"] = ["cardinal", "cardinal"]
    (tmp_path / "interpretive_rules_v1.yaml").write_text(
        yaml.safe_dump(payload, allow_unicode=True), encoding="utf-8"
    )

    with pytest.raises(ValueError, match="INTERPRETIVE_RULE_INVALID_PREDICATE_VALUE"):
        load_interpretive_rule_bundle(tmp_path)


def test_asset_boolean_cannot_hide_a_structural_demo_condition(tmp_path: Path):
    payload = yaml.safe_load(RULE_PATH.read_text(encoding="utf-8"))
    rule = next(
        item
        for item in payload["rules"]
        if item["signal_id"] == "ASTROLOGY-PLANET-SIGN-EXPRESSION"
    )
    rule["value_predicates"][0]["values"] = ["fire"]
    rule["value_predicates"][1]["values"] = ["cardinal"]
    rule["requires_exact_demo_chart"] = False
    (tmp_path / "interpretive_rules_v1.yaml").write_text(
        yaml.safe_dump(payload, allow_unicode=True), encoding="utf-8"
    )

    with pytest.raises(ValueError, match="INTERPRETIVE_RULE_DEMO_SPECIFIC"):
        load_interpretive_rule_bundle(tmp_path)


def test_rule_loader_structurally_rejects_cross_family_demo_join(tmp_path: Path):
    payload = yaml.safe_load(RULE_PATH.read_text(encoding="utf-8"))
    rule = payload["rules"][0]
    rule["fact_refs"].append("bazi.elemental_balance")
    rule["value_predicates"].append(
        {"fact_ref": "bazi.elemental_balance", "values": ["year", "month"]}
    )
    (tmp_path / "interpretive_rules_v1.yaml").write_text(
        yaml.safe_dump(payload, allow_unicode=True), encoding="utf-8"
    )

    with pytest.raises(ValueError, match="INTERPRETIVE_RULE_DEMO_SPECIFIC"):
        load_interpretive_rule_bundle(tmp_path)


@pytest.mark.parametrize(
    ("selector", "value", "error"),
    [
        ("positions", ["season"], "INTERPRETIVE_RULE_INVALID_PREDICATE_VALUE"),
        ("source_kinds", ["computed"], "INTERPRETIVE_RULE_INVALID_PREDICATE_VALUE"),
        ("participants", ["season.branch"], "INTERPRETIVE_RULE_INVALID_PREDICATE"),
        ("minimum_occurrences", 0, "INTERPRETIVE_RULE_INVALID_PREDICATE_VALUE"),
        ("unknown_selector", ["value"], "INTERPRETIVE_RULE_INVALID_PREDICATE"),
    ],
)
def test_rule_loader_rejects_unbounded_selector_values(
    tmp_path: Path, selector: str, value, error: str
):
    payload = yaml.safe_load(RULE_PATH.read_text(encoding="utf-8"))
    payload["rules"][0]["value_predicates"][0][selector] = value
    (tmp_path / "interpretive_rules_v1.yaml").write_text(
        yaml.safe_dump(payload, allow_unicode=True), encoding="utf-8"
    )

    with pytest.raises(ValueError, match=error):
        load_interpretive_rule_bundle(tmp_path)
