from hashlib import sha256
from pathlib import Path

import yaml

from destiny_personality.calculation import (
    AstrologyAspectFact,
    DeterministicChartFacts,
    TenGodFact,
    TenGodSourceKind,
)
from destiny_personality.calculation.models import PillarPosition


def test_candidate_profile_uses_its_own_ir_contract(normalized_time, bazi_facts, astrology_facts) -> None:
    from destiny_personality.core_profile_builder import build_candidate_core_profile

    profile = build_candidate_core_profile(
        DeterministicChartFacts(normalized_time, bazi_facts, astrology_facts),
        fact_assurance="capability_reported",
    )

    assert profile.schema_version == "candidate-core-profile-v1"
    assert profile.candidate_profile_id.startswith("candidate-")
    assert profile.semantic_capability_level == "primitive_only"


def test_opposing_candidates_in_different_contexts_are_not_mixed(
    normalized_time, bazi_facts, astrology_facts
) -> None:
    from destiny_personality.core_profile_builder import build_candidate_core_profile

    bazi = bazi_facts.__class__(
        methodology_version=bazi_facts.methodology_version,
        year_pillar=bazi_facts.year_pillar,
        month_pillar=bazi_facts.month_pillar,
        day_pillar=bazi_facts.day_pillar,
        hour_pillar=bazi_facts.hour_pillar,
        hidden_stems=bazi_facts.hidden_stems,
        ten_gods=(
            TenGodFact("resource", "正印", (PillarPosition.YEAR,), TenGodSourceKind.VISIBLE_STEM),
            TenGodFact("authority", "正官", (PillarPosition.MONTH,), TenGodSourceKind.VISIBLE_STEM),
        ),
        relations=bazi_facts.relations,
    )
    astrology = astrology_facts.__class__(
        methodology_version=astrology_facts.methodology_version,
        placements=astrology_facts.placements,
        aspects=(AstrologyAspectFact("Uranus", "Sun", "trine", 1),),
        ascendant=astrology_facts.ascendant,
        mc=astrology_facts.mc,
        house_cusps=astrology_facts.house_cusps,
        dignities=astrology_facts.dignities,
    )
    profile = build_candidate_core_profile(
        DeterministicChartFacts(normalized_time, bazi, astrology),
        fact_assurance="capability_reported",
    )

    state = profile.primitive_states["P002"]
    assert state.state == "context_differentiated"
    assert state.context_states == {
        "change": "supported_low",
        "pressure+work": "supported_high",
    }


def test_unknown_time_keeps_stable_aspect_evidence_but_removes_angular_modifier(
    normalized_time, bazi_facts, astrology_facts
) -> None:
    from destiny_personality.core_profile_builder import build_candidate_core_profile

    astrology = astrology_facts.__class__(
        methodology_version=astrology_facts.methodology_version,
        placements=astrology_facts.placements,
        aspects=(AstrologyAspectFact("Sun", "Mars", "square", 1),),
        ascendant=None,
        mc=None,
        house_cusps=(),
        dignities=astrology_facts.dignities,
    )
    profile = build_candidate_core_profile(
        DeterministicChartFacts(normalized_time, bazi_facts, astrology),
        fact_assurance="capability_reported",
    )

    candidate = next(item for item in profile.astrology_primitive_candidates if item.primitive_id == "P001")
    assert "astrology.aspects:Sun:square:Mars:1" in candidate.fact_refs
    assert not any(ref.startswith("astrology.angular:") for ref in candidate.modifier_refs)
    assert "astrology.aspect_expression:effortful:high" in candidate.modifier_refs


def test_hidden_only_bazi_evidence_cannot_activate_rule(
    normalized_time, bazi_facts, astrology_facts
) -> None:
    from destiny_personality.core_profile_builder import build_candidate_core_profile

    bazi = bazi_facts.__class__(
        methodology_version=bazi_facts.methodology_version,
        year_pillar=bazi_facts.year_pillar,
        month_pillar=bazi_facts.month_pillar,
        day_pillar=bazi_facts.day_pillar,
        hour_pillar=bazi_facts.hour_pillar,
        hidden_stems=bazi_facts.hidden_stems,
        ten_gods=(
            TenGodFact("peer", "比肩", (PillarPosition.YEAR,), TenGodSourceKind.HIDDEN_STEM),
            TenGodFact("output", "食神", (PillarPosition.MONTH,), TenGodSourceKind.HIDDEN_STEM),
        ),
        relations=bazi_facts.relations,
    )
    profile = build_candidate_core_profile(
        DeterministicChartFacts(normalized_time, bazi, astrology_facts),
        fact_assurance="capability_reported",
    )

    assert profile.bazi_primitive_candidates == ()


def test_bazi_counterweight_contextualizes_low_predictability_candidate(
    normalized_time, bazi_facts, astrology_facts
) -> None:
    from destiny_personality.core_profile_builder import build_candidate_core_profile

    bazi = bazi_facts.__class__(
        methodology_version=bazi_facts.methodology_version,
        year_pillar=bazi_facts.year_pillar,
        month_pillar=bazi_facts.month_pillar,
        day_pillar=bazi_facts.day_pillar,
        hour_pillar=bazi_facts.hour_pillar,
        hidden_stems=bazi_facts.hidden_stems,
        ten_gods=(
            TenGodFact("output", "食神", (PillarPosition.YEAR,), TenGodSourceKind.VISIBLE_STEM),
            TenGodFact("wealth", "正财", (PillarPosition.MONTH,), TenGodSourceKind.VISIBLE_STEM),
            TenGodFact("resource", "正印", (PillarPosition.DAY,), TenGodSourceKind.VISIBLE_STEM),
        ),
        relations=bazi_facts.relations,
    )
    profile = build_candidate_core_profile(
        DeterministicChartFacts(normalized_time, bazi, astrology_facts),
        fact_assurance="capability_reported",
    )

    candidate = next(
        candidate
        for candidate in profile.bazi_primitive_candidates
        if candidate.semantic_rule_refs == ("BZ-C2B-03",)
    )
    assert candidate.counterweight_effect == "contextualize"


def test_packaged_candidate_assets_match_canonical_assets() -> None:
    project_root = Path(__file__).resolve().parents[1]
    canonical_root = project_root / "candidates" / "core-profile-v1"
    packaged_root = project_root / "src" / "destiny_personality" / "candidate_assets" / "core-profile-v1"

    assert {path.name for path in canonical_root.glob("*.yaml")} == {
        path.name for path in packaged_root.glob("*.yaml")
    }
    for canonical_path in canonical_root.glob("*.yaml"):
        packaged_path = packaged_root / canonical_path.name
        assert sha256(canonical_path.read_bytes()).digest() == sha256(packaged_path.read_bytes()).digest(), (
            "CANDIDATE_ASSET_DRIFT_ERROR",
            canonical_path.name,
        )


def test_mapping_assets_declare_the_executable_candidate_guards() -> None:
    project_root = Path(__file__).resolve().parents[1]
    candidate_root = project_root / "candidates" / "core-profile-v1"
    bazi = yaml.safe_load((candidate_root / "bazi_mapping_registry_v1.yaml").read_text(encoding="utf-8"))
    astrology = yaml.safe_load((candidate_root / "astrology_mapping_registry_v1.yaml").read_text(encoding="utf-8"))

    low_predictability = next(rule for rule in bazi["rules"] if rule["rule_id"] == "BZ-C2B-03")
    assert low_predictability["requires_visible_evidence_per_group"] is True
    assert low_predictability["counterweight_rules"][0]["effect"] == "contextualize"
    assert all(rule["requires_known_time"] is False for rule in astrology["rules"])
    assert astrology["aspect_semantics"]["square"]["tension_level"] == "high"
