from dataclasses import replace
from pathlib import Path

import pytest

from destiny_personality.audited_core_profile import build_audited_interpretive_core_profile
from destiny_personality.audited_profile_report import (
    build_audited_profile_report_plan,
    render_audited_profile_report,
)
from destiny_personality.deterministic_facts_codec import load_qualified_deterministic_facts


ROOT = Path(__file__).parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "interpretive" / "v060"


def _profile(name: str):
    qualified = load_qualified_deterministic_facts(
        FIXTURES / f"{name}-facts.json",
        FIXTURES / f"{name}-qualification.json",
    )
    return build_audited_interpretive_core_profile(qualified)


def test_plan_selects_a_bounded_non_repetitive_reader_path():
    profile = _profile("cross-system-tension")

    plan = build_audited_profile_report_plan(profile)
    report = render_audited_profile_report(profile, plan)

    assert 4 <= len(plan.sections) <= 8
    assert plan.core_profile_id == profile.core_profile_id
    assert len({section.deduplication_key for section in plan.sections}) == len(plan.sections)
    assert report.sections
    assert all(section.signal_ids and section.rule_refs and section.fact_refs for section in report.sections)
    assert "formal primitive coverage is not asserted" in report.limitations


def test_renderer_rejects_a_plan_not_bound_to_the_profile():
    profile = _profile("cross-system-agreement")
    plan = build_audited_profile_report_plan(profile)

    with pytest.raises(ValueError, match="AUDITED_PROFILE_REPORT_CONTAINMENT_VIOLATION"):
        render_audited_profile_report(profile, replace(plan, core_profile_id="other"))
