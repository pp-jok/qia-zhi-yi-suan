from dataclasses import replace

import pytest

def _profile(qualified_facts):
    from destiny_personality.core_destiny_profile import build_core_destiny_profile

    return build_core_destiny_profile(qualified_facts)


def test_sparse_profile_still_plans_an_honest_report(qualified_facts):
    from destiny_personality.report_planner import build_release_report_plan

    plan = build_release_report_plan(
        _profile(qualified_facts), "standard-portrait-v1"
    )

    assert "limitations" in plan.section_ids
    assert not any(section.startswith("primitive:") for section in plan.section_ids)
    assert plan.renderer_profile == "standard-portrait-v1"


@pytest.mark.parametrize(
    "renderer_profile",
    (
        "concise-portrait-v1",
        "standard-portrait-v1",
        "dynamic-long-form-v1",
        "legacy-long-form-v2",
    ),
)
def test_all_public_renderer_profiles_have_a_contained_plan(
    qualified_facts, renderer_profile
):
    from destiny_personality.report_planner import build_release_report_plan

    plan = build_release_report_plan(
        _profile(qualified_facts), renderer_profile
    )

    assert plan.schema_version == "release-report-plan-v1"
    assert plan.containment_status == "validated_cdp_only"


def test_planner_rejects_invalid_formal_profile(qualified_facts):
    from destiny_personality.report_planner import build_release_report_plan

    profile = _profile(qualified_facts)
    invalid = replace(profile, audit_trail=())

    with pytest.raises(ValueError, match="FORMAL_CDP_INVALID"):
        build_release_report_plan(invalid, "concise-portrait-v1")
