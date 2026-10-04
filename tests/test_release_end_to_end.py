from dataclasses import asdict, replace
from pathlib import Path

import pytest
import yaml

from destiny_personality.calculation import DeterministicChartFacts, FactMode


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCENARIOS_PATH = PROJECT_ROOT / "tests" / "fixtures" / "end_to_end" / "scenarios_v1.yaml"


def _scenarios():
    payload = yaml.safe_load(SCENARIOS_PATH.read_text(encoding="utf-8"))
    assert payload["schema_version"] == "release-e2e-scenarios-v1"
    return payload["scenarios"]


def _mapping(mapping_id, direction, *, context=(), global_authority=False):
    return {
        "mapping_candidate_id": mapping_id,
        "primitive_id": "P001",
        "source_system": "bazi",
        "review_status": "approved",
        "activation_status": "active",
        "proposed_direction": {"state": direction},
        "semantic_mechanism_refs": ["release-mechanism:" + mapping_id],
        "evidence_root_refs": ["release-root:" + mapping_id],
        "canonical_fact_requirements": ["synthetic-fact:" + mapping_id],
        "contexts": list(context),
        "global_authority": global_authority,
    }


def _mappings(variant):
    if variant == "zero":
        return ()
    if variant == "high":
        return (_mapping("high", "supported_high", global_authority=True),)
    if variant == "contradiction":
        return (
            _mapping("high", "supported_high", global_authority=True),
            _mapping("low", "supported_low", global_authority=True),
        )
    if variant == "context":
        return (
            _mapping("work-high", "supported_high", context=("work",)),
            _mapping("relationship-low", "supported_low", context=("relationship",)),
        )
    raise AssertionError(variant)


def _facts_for_variant(base, variant):
    normalized = base.normalized_time
    bazi = base.bazi
    astrology = base.astrology
    if variant == "unknown_hour":
        normalized = replace(
            normalized,
            historical_civil_time=None,
            local_standard_time=None,
            utc_time=None,
            true_solar_time=None,
            fact_mode=FactMode.STABLE_ONLY,
            sensitivity_reasons=("birth_time_unknown",),
        )
        bazi = replace(bazi, hour_pillar=None)
        astrology = replace(
            astrology, ascendant=None, mc=None, house_cusps=(),
            placements=tuple(replace(item, house=None) for item in astrology.placements),
        )
    elif variant == "time_boundary":
        normalized = replace(
            normalized,
            sensitivity_reasons=("hour_boundary",),
        )
    elif variant == "timezone":
        normalized = replace(normalized, timezone_name="America/New_York")
    elif variant == "dst":
        normalized = replace(normalized, dst_was_applied=True)
    elif variant == "bazi_structure":
        bazi = replace(bazi, hour_pillar=bazi.day_pillar)
    elif variant == "astrology_structure":
        astrology = replace(astrology, placements=tuple(reversed(astrology.placements)))
    elif variant != "known_time":
        raise AssertionError(variant)
    return DeterministicChartFacts(normalized, bazi, astrology)


def _execute_precomputed_provider_flow(scenario, base_facts):
    from destiny_personality.core_destiny_profile import build_core_destiny_profile
    from destiny_personality.release_renderer import render_release_report
    from destiny_personality.report_planner import build_release_report_plan

    facts = _facts_for_variant(base_facts, scenario["fact_variant"])
    profile = build_core_destiny_profile(
        facts,
        fact_assurance="capability_reported",
        approved_mappings=_mappings(scenario["semantic_variant"]),
    )
    plan = build_release_report_plan(profile, "standard-portrait-v1")
    report = render_release_report(profile, plan)
    return facts, profile, asdict(report)


@pytest.mark.parametrize("scenario", _scenarios(), ids=lambda item: item["id"])
def test_precomputed_facts_to_cdp_to_report(
    scenario, normalized_time, bazi_facts, astrology_facts
):
    base = DeterministicChartFacts(normalized_time, bazi_facts, astrology_facts)

    facts, profile, report = _execute_precomputed_provider_flow(scenario, base)

    assert report["audit_refs"]
    assert report["assurance"]["fact_assurance"] != report["assurance"]["semantic_model_assurance"]
    assert profile.primitive_states["P001"].state == scenario["expected_state"]
    assert all(item.salience_delta == 0 for item in profile.cross_system_alignment)
    if facts.normalized_time.fact_mode is FactMode.STABLE_ONLY:
        assert facts.bazi.hour_pillar is None
        assert facts.astrology.ascendant is None
        assert facts.astrology.house_cusps == ()


def test_scenario_matrix_covers_required_release_cases():
    ids = {item["id"] for item in _scenarios()}
    assert ids == {
        "known-time-zero-coverage", "unknown-hour-stable-only", "time-boundary",
        "timezone-normalization", "dst-normalization", "diverse-bazi-structure",
        "diverse-astrology-structure", "test-only-high-coverage", "contradiction",
        "context-differentiation",
    }


def test_repeat_execution_is_normalized_equivalent(
    normalized_time, bazi_facts, astrology_facts
):
    scenario = _scenarios()[0]
    base = DeterministicChartFacts(normalized_time, bazi_facts, astrology_facts)

    first = _execute_precomputed_provider_flow(scenario, base)
    second = _execute_precomputed_provider_flow(scenario, base)

    assert first[1] == second[1]
    assert first[2] == second[2]
