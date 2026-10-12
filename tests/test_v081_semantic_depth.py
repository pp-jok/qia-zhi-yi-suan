from pathlib import Path
import json

from destiny_personality.audited_core_profile import (
    build_audited_interpretive_core_profile,
)
from destiny_personality.audited_profile_report import (
    build_audited_profile_report_plan,
)
from destiny_personality.deterministic_facts_codec import (
    load_qualified_deterministic_facts,
)
from destiny_personality.birth_report import build_birth_report


FIXTURES = Path(__file__).parent / "fixtures" / "interpretive" / "v060"


def _profile(name: str):
    return build_audited_interpretive_core_profile(
        load_qualified_deterministic_facts(
            FIXTURES / f"{name}-facts.json",
            FIXTURES / f"{name}-qualification.json",
        )
    )


def test_alignment_is_not_by_itself_promoted_to_a_core_dynamic():
    profile = _profile("cross-system-agreement")

    assert profile.cross_system_alignments
    assert profile.core_dynamics == ()
    assert profile.shadow_mature_forms == ()
    assert profile.fate_themes == ()
    assert profile.archetype is None


def test_depth_items_are_derived_from_dynamic_lineage_not_signature_rank():
    profile = _profile("cross-system-tension")
    dynamic_ids = {item.item_id for item in profile.core_dynamics}

    assert all(
        set(item.source_item_ids) <= dynamic_ids
        for item in profile.shadow_mature_forms
    )
    assert all(len(item.source_item_ids) >= 2 for item in profile.fate_themes)
    if profile.archetype is not None:
        assert profile.fate_themes


def test_planner_allows_a_short_evidence_limited_profile():
    profile = _profile("cross-system-agreement")

    plan = build_audited_profile_report_plan(profile)

    assert len(plan.sections) < 4


def test_shadow_section_does_not_repeat_the_dynamic_mechanism(tmp_path):
    build_birth_report(
        "1992年7月14日 15:30，上海，女",
        tmp_path / "report.json",
        tmp_path / "artifacts",
    )
    report = json.loads((tmp_path / "report.json").read_text())
    shadow = next(section for section in report["sections"] if "压力与成熟调节" in section["title"])

    assert "形成机制：" not in shadow["content"]
