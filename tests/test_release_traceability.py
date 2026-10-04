from dataclasses import asdict

def test_release_report_is_traceable_to_profile_and_plan(qualified_facts):
    from destiny_personality.core_destiny_profile import build_core_destiny_profile
    from destiny_personality.release_renderer import render_release_report
    from destiny_personality.report_planner import build_release_report_plan

    profile = build_core_destiny_profile(qualified_facts)
    plan = build_release_report_plan(profile, "standard-portrait-v1")
    report = asdict(render_release_report(profile, plan))

    assert report["core_profile_id"] == profile.core_profile_id
    assert set(profile.audit_trail).issubset(report["audit_refs"])
    assert set(plan.audit_trail).issubset(report["audit_refs"])
    assert report["report"]["primitive_interpretations"] == ()


def test_legacy_blueprint_remains_a_frozen_56_chapter_contract():
    from pathlib import Path

    root = Path(__file__).resolve().parents[1]
    blueprint = (root / "destiny-personality" / "references" / "long-form-report-blueprint.md").read_text(encoding="utf-8")

    assert [f"`chapter_{index:02d}`" in blueprint for index in range(1, 57)] == [True] * 56
    assert "legacy-long-form-v2" in blueprint
