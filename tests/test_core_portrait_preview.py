from pathlib import Path
from shutil import copytree
from dataclasses import replace

import yaml

from destiny_personality.calculation import AstrologyAspectFact, DeterministicChartFacts, TenGodFact, TenGodSourceKind
from destiny_personality.calculation.models import PillarPosition


def _profile(normalized_time, bazi_facts, astrology_facts):
    from destiny_personality.core_profile_builder import build_candidate_core_profile

    bazi = bazi_facts.__class__(
        methodology_version=bazi_facts.methodology_version, year_pillar=bazi_facts.year_pillar,
        month_pillar=bazi_facts.month_pillar, day_pillar=bazi_facts.day_pillar,
        hour_pillar=bazi_facts.hour_pillar, hidden_stems=bazi_facts.hidden_stems,
        ten_gods=(
            TenGodFact("fixture", "正印", (PillarPosition.YEAR,), TenGodSourceKind.VISIBLE_STEM),
            TenGodFact("fixture", "正官", (PillarPosition.MONTH,), TenGodSourceKind.VISIBLE_STEM),
        ), relations=bazi_facts.relations,
    )
    return build_candidate_core_profile(
        DeterministicChartFacts(normalized_time, bazi, astrology_facts),
        fact_assurance="capability_reported",
    )


def test_core_summary_and_renderers_are_primitive_contained(normalized_time, bazi_facts, astrology_facts) -> None:
    from destiny_personality.core_portrait import build_candidate_profile_summary, render_core_concise, render_core_standard

    profile = _profile(normalized_time, bazi_facts, astrology_facts)
    summary = build_candidate_profile_summary(profile)

    assert summary.user_capability_level == "core_portrait_preview"
    assert summary.time_sensitivity.available
    assert render_core_concise(summary).mode == "core_concise"
    assert 4 <= len(render_core_concise(summary).sections) <= 8
    assert render_core_standard(summary).mode == "core_standard"
    assert 8 <= len(render_core_standard(summary).sections) <= 14
    assert all("Signature" not in section.body and "Archetype" not in section.body for section in render_core_standard(summary).sections)


def test_source_views_explanation_and_profile_diff_are_auditable(normalized_time, bazi_facts, astrology_facts) -> None:
    from dataclasses import replace
    from destiny_personality.core_portrait import (
        build_candidate_profile_summary,
        compare_candidate_profiles_versions,
        explain_profile_item,
        source_view,
    )

    profile = _profile(normalized_time, bazi_facts, astrology_facts)
    summary = build_candidate_profile_summary(profile)
    item = next(item for item in summary.items if item.state != "unknown")

    explanation = explain_profile_item(profile, item.item_id)
    assert explanation.primitive_id == item.primitive_id
    assert explanation.fact_refs and explanation.rule_refs
    assert all(candidate.source_system == "bazi" for candidate in source_view(profile, "bazi"))
    assert source_view(profile, "comparison") == profile.cross_system_alignments
    diff = compare_candidate_profiles_versions(profile, profile)
    assert diff.unchanged_primitive_ids == tuple(sorted(profile.primitive_states))
    assert not diff.changed_primitives
    runtime_diff = compare_candidate_profiles_versions(profile, replace(profile, profile_runtime_version="candidate-profile-runtime-v3"))
    assert runtime_diff.runtime_version_changed is True
    assert "profile_runtime_version_changed" in runtime_diff.change_reasons


def test_unknown_birth_time_explains_available_and_unavailable_evidence(normalized_time, bazi_facts, astrology_facts) -> None:
    from destiny_personality.core_portrait import build_candidate_profile_summary
    from destiny_personality.core_profile_builder import build_candidate_core_profile
    from destiny_personality.calculation.models import FactMode

    astrology = astrology_facts.__class__(
        methodology_version=astrology_facts.methodology_version, placements=astrology_facts.placements,
        aspects=(AstrologyAspectFact("Saturn", "Sun", "trine", 1),), ascendant=None, mc=None,
        house_cusps=(), dignities=(),
    )
    stable_time = normalized_time.__class__(**{**normalized_time.__dict__, "fact_mode": FactMode.STABLE_ONLY})
    bazi = bazi_facts.__class__(**{**bazi_facts.__dict__, "hour_pillar": None})
    placements = tuple(item.__class__(item.body, item.longitude, item.sign, item.degree_in_sign, None) for item in astrology.placements)
    astrology = astrology.__class__(**{**astrology.__dict__, "placements": placements})
    profile = build_candidate_core_profile(DeterministicChartFacts(stable_time, bazi, astrology), fact_assurance="capability_reported")
    summary = build_candidate_profile_summary(profile)

    assert "稳定行星与相位证据" in summary.time_sensitivity.available
    assert "Ascendant" in summary.time_sensitivity.unavailable


def test_user_portrait_preserves_direction_and_hides_internal_identifiers(normalized_time, bazi_facts, astrology_facts) -> None:
    from destiny_personality.core_portrait import build_candidate_profile_summary, render_core_standard

    profile = _profile(normalized_time, bazi_facts, astrology_facts)
    summary = build_candidate_profile_summary(profile)
    portrait = render_core_standard(summary)
    user_text = "\n".join(section.body for section in portrait.sections)

    assert any(item.resolved_direction == "high" for item in summary.items)
    assert "更倾向寻求稳定、明确和可预期的结构" in user_text
    assert "P001" not in user_text
    assert "decision" not in user_text
    assert portrait.presentation_bundle_fingerprint


def test_context_differentiated_summary_keeps_scoped_direction(normalized_time, bazi_facts, astrology_facts) -> None:
    from destiny_personality.core_portrait import build_candidate_profile_summary

    profile = _profile(normalized_time, bazi_facts, astrology_facts)
    state = replace(
        profile.primitive_states["P001"],
        state="context_differentiated",
        context_states={"decision": "high", "relationship": "low"},
    )
    profile = replace(profile, primitive_states={**profile.primitive_states, "P001": state})

    item = next(item for item in build_candidate_profile_summary(profile).items if item.primitive_id == "P001")

    assert item.resolved_direction == "contextual"
    assert item.context_directions == (("decision", "high"), ("relationship", "low"))


def test_promotion_uses_the_bundle_being_checked(tmp_path) -> None:
    from destiny_personality.core_profile_promotion import validate_candidate_promotion_authorization

    source = Path(__file__).resolve().parents[1] / "candidates" / "core-profile-v1"
    target = tmp_path / "bundle-b"
    copytree(source, target)
    mapping_path = target / "bazi_mapping_registry_v1.yaml"
    mapping = yaml.safe_load(mapping_path.read_text(encoding="utf-8"))
    mapping["rules"][0]["contexts"] = ["work"]
    mapping_path.write_text(yaml.safe_dump(mapping, allow_unicode=True), encoding="utf-8")

    blockers = validate_candidate_promotion_authorization(target)

    assert "CALIBRATION_POLICY_GAP" in blockers
    assert "CANDIDATE_HOLDOUT_VALIDATION_REQUIRED" in blockers
    assert "HUMAN_PRODUCTION_APPROVAL_REQUIRED" in blockers
