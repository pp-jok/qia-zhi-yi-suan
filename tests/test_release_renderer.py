from dataclasses import replace

import pytest

from destiny_personality.calculation import DeterministicChartFacts


def _profile(normalized_time, bazi_facts, astrology_facts):
    from destiny_personality.core_destiny_profile import build_core_destiny_profile

    return build_core_destiny_profile(
        DeterministicChartFacts(normalized_time, bazi_facts, astrology_facts),
        fact_assurance="capability_reported",
    )


def test_sparse_renderer_is_useful_but_does_not_invent_primitive_prose(
    normalized_time, bazi_facts, astrology_facts
):
    from destiny_personality.release_renderer import render_release_report
    from destiny_personality.report_planner import build_release_report_plan

    profile = _profile(normalized_time, bazi_facts, astrology_facts)
    report = render_release_report(
        profile, build_release_report_plan(profile, "standard-portrait-v1")
    )

    assert report.facts_summary["fact_assurance"] == "capability_reported"
    assert report.core_profile["primitive_state_counts"] == {"unknown": 6}
    assert report.report["primitive_interpretations"] == ()
    assert report.report["summary"]
    assert report.assurance["semantic_model_assurance"] == "limited_coverage_unknown_only"


def test_renderer_cannot_add_unplanned_claim(normalized_time, bazi_facts, astrology_facts):
    from destiny_personality.release_renderer import render_release_report
    from destiny_personality.report_planner import build_release_report_plan

    profile = _profile(normalized_time, bazi_facts, astrology_facts)
    plan = build_release_report_plan(profile, "standard-portrait-v1")
    tampered = replace(plan, section_ids=plan.section_ids + ("primitive:P001",))

    with pytest.raises(ValueError, match="REPORT_CONTAINMENT_VIOLATION"):
        render_release_report(profile, tampered)


def test_renderer_restates_only_an_admitted_primitive_state(
    normalized_time, bazi_facts, astrology_facts
):
    from destiny_personality.core_destiny_profile import build_core_destiny_profile
    from destiny_personality.release_renderer import render_release_report
    from destiny_personality.report_planner import build_release_report_plan

    mapping = {
        "mapping_candidate_id": "MAP-RELEASE-1",
        "primitive_id": "P001",
        "source_system": "bazi",
        "review_status": "approved",
        "activation_status": "active",
        "proposed_direction": {"state": "supported_high"},
        "contexts": [],
        "global_authority": True,
        "canonical_fact_requirements": ["fact:admitted"],
        "semantic_mechanism_refs": ["SMC-ADMITTED"],
        "evidence_root_refs": ["ER-ADMITTED"],
    }
    profile = build_core_destiny_profile(
        DeterministicChartFacts(normalized_time, bazi_facts, astrology_facts),
        fact_assurance="capability_reported",
        approved_mappings=(mapping,),
    )

    report = render_release_report(
        profile, build_release_report_plan(profile, "standard-portrait-v1")
    )

    assert report.report["primitive_interpretations"] == (
        {
            "primitive_id": "P001",
            "state": "supported_high",
            "statement": "P001 is reported as supported_high from approved active mapping evidence.",
            "evidence_refs": ("fact:admitted",),
            "semantic_rule_refs": ("SMC-ADMITTED",),
            "limitations": (
                "approved mapping evidence remains bounded by declared contexts",
            ),
        },
    )


def test_legacy_mode_returns_a_separate_frozen_handoff(
    normalized_time, bazi_facts, astrology_facts
):
    from destiny_personality.release_renderer import render_release_report
    from destiny_personality.report_planner import build_release_report_plan

    profile = _profile(normalized_time, bazi_facts, astrology_facts)
    report = render_release_report(
        profile, build_release_report_plan(profile, "legacy-long-form-v2")
    )

    assert report.report["kind"] == "legacy_compatibility_handoff"
    assert report.report["status"] == "frozen"
