from dataclasses import replace

import pytest

def _profile(qualified_facts):
    from destiny_personality.core_destiny_profile import build_core_destiny_profile

    return build_core_destiny_profile(qualified_facts)


def test_sparse_renderer_is_useful_but_does_not_invent_primitive_prose(qualified_facts):
    from destiny_personality.release_renderer import render_release_report
    from destiny_personality.report_planner import build_release_report_plan

    profile = _profile(qualified_facts)
    report = render_release_report(
        profile, build_release_report_plan(profile, "standard-portrait-v1")
    )

    assert report.facts_summary["fact_assurance"] == "capability_reported"
    assert report.core_profile["primitive_state_counts"] == {"unknown": 6}
    assert report.report["primitive_interpretations"] == ()
    assert report.report["summary"]
    assert report.assurance["semantic_model_assurance"] == "limited_coverage_unknown_only"


def test_renderer_cannot_add_unplanned_claim(qualified_facts):
    from destiny_personality.release_renderer import render_release_report
    from destiny_personality.report_planner import build_release_report_plan

    profile = _profile(qualified_facts)
    plan = build_release_report_plan(profile, "standard-portrait-v1")
    tampered = replace(plan, section_ids=plan.section_ids + ("primitive:P001",))

    with pytest.raises(ValueError, match="REPORT_CONTAINMENT_VIOLATION"):
        render_release_report(profile, tampered)


def test_legacy_mode_returns_a_separate_frozen_handoff(qualified_facts):
    from destiny_personality.release_renderer import render_release_report
    from destiny_personality.report_planner import build_release_report_plan

    profile = _profile(qualified_facts)
    report = render_release_report(
        profile, build_release_report_plan(profile, "legacy-long-form-v2")
    )

    assert report.report["kind"] == "legacy_compatibility_handoff"
    assert report.report["status"] == "frozen"
