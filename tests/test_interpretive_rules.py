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


FIXTURE_PATH = (
    Path(__file__).parent / "fixtures" / "interpretive" / "extraction_cases_v1.yaml"
)


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
                "resource",
                (PillarPosition.YEAR,),
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
    if case["time_available"]:
        normalized_time = facts.normalized_time
        astrology = replace(
            facts.astrology,
            aspects=(
                AstrologyAspectFact("Sun", "Moon", "conjunction", Decimal("0")),
            ),
            dignities=(DignityFact("Sun", "domicile"),),
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


def test_rule_bundle_is_versioned_and_contains_both_systems():
    bundle = load_interpretive_rule_bundle()

    assert bundle.bundle_version == "audited-interpretive-rules-v1"
    assert {rule.system for rule in bundle.rules} == {"bazi", "astrology"}


def test_extraction_emits_traceable_bazi_and_astrology_signals(
    qualified_interpretive_facts, extraction_cases
):
    signals = extract_interpretive_signals(qualified_interpretive_facts)

    assert {signal.system for signal in signals} == {"bazi", "astrology"}
    assert {signal.signal_id for signal in signals} == set(
        extraction_cases["known_time"]["expected_signal_ids"]
    )
    assert all(signal.fact_refs and signal.traditional_rule_ref for signal in signals)
    assert all(
        reference.startswith(("bazi.", "astrology."))
        for signal in signals
        for reference in signal.fact_refs
    )


def test_missing_time_skips_house_and_angle_rules(
    missing_time_interpretive_facts, extraction_cases
):
    signals = extract_interpretive_signals(missing_time_interpretive_facts)

    assert {signal.signal_id for signal in signals} == set(
        extraction_cases["missing_time"]["expected_signal_ids"]
    )
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
    (tmp_path / "interpretive_rules_v1.yaml").write_text(
        "bundle_version: audited-interpretive-rules-v1\n"
        "limitations: [Traditional, non-diagnostic rules.]\n"
        "rules:\n"
        "  - signal_id: TEST-001\n"
        "    system: bazi\n"
        "    fact_refs: [bazi.ten_god]\n"
        "    traditional_rule_ref: Test school\n"
        "    topic: Test topic\n"
        "    direction: Test direction\n"
        "    interpretation: Traditional, non-diagnostic interpretation.\n"
        "    confidence: certain\n"
        "    limitations: [Not an empirical diagnostic.]\n",
        encoding="utf-8",
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
    (tmp_path / "interpretive_rules_v1.yaml").write_text(
        "bundle_version: audited-interpretive-rules-v1\n"
        "limitations: [Traditional, non-diagnostic rules.]\n"
        "rules:\n"
        "  - signal_id: TEST-FACT-REF\n"
        "    system: bazi\n"
        f"    fact_refs: {fact_refs}\n"
        "    traditional_rule_ref: Test school\n"
        "    topic: Test topic\n"
        "    direction: Test direction\n"
        "    interpretation: Traditional, non-diagnostic interpretation.\n"
        "    confidence: moderate\n"
        "    limitations: [Not an empirical diagnostic.]\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match=error):
        load_interpretive_rule_bundle(tmp_path)
