from destiny_personality.calculation import (
    AstrologyAspectFact,
    DeterministicChartFacts,
    TenGodFact,
    TenGodSourceKind,
)
from destiny_personality.calculation.models import PillarPosition


def test_candidate_mapping_uses_versioned_context_tags() -> None:
    from destiny_personality.core_profile_builder import candidate_semantic_bundle_fingerprint
    from destiny_personality.context_taxonomy import load_candidate_context_taxonomy

    taxonomy = load_candidate_context_taxonomy()

    assert taxonomy.contexts == {"action", "change", "decision", "pressure", "relationship", "work"}
    assert taxonomy.comparison_policy["partial_overlap"] == "contextualization"
    assert len(candidate_semantic_bundle_fingerprint()) == 64


def test_alignment_validates_shared_context_without_merging_other_contexts(
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
        aspects=(AstrologyAspectFact("Saturn", "Sun", "trine", 1),),
        ascendant=astrology_facts.ascendant,
        mc=astrology_facts.mc,
        house_cusps=astrology_facts.house_cusps,
        dignities=astrology_facts.dignities,
    )

    profile = build_candidate_core_profile(
        DeterministicChartFacts(normalized_time, bazi, astrology),
        fact_assurance="capability_reported",
    )

    alignment = next(item for item in profile.cross_system_alignments if item.primitive_id == "P002")
    assert alignment.status == "contextualization"
    assert alignment.context_refs == ("pressure",)
    assert alignment.direction_relation == "same"


def test_counterweight_is_retained_as_auditable_counterevidence(
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

    candidate = next(item for item in profile.bazi_primitive_candidates if item.semantic_rule_refs == ("BZ-C2B-03",))
    assert candidate.counterevidence_refs == ("bazi.ten_gods:正印",)
    assert candidate.counterweight_effect == "contextualize"


def test_overlapping_opposed_contexts_resolve_to_mixed() -> None:
    from destiny_personality.core_profile_builder import _resolve_global_state
    from destiny_personality.core_profile_models import PrimitiveCandidate

    high = PrimitiveCandidate("P002", "bazi", "high", (), ("high",), ("pressure", "work"), "moderate", "stable", (), (), "direct", "low", None, ())
    low = PrimitiveCandidate("P002", "astrology", "low", (), ("low",), ("pressure",), "moderate", "stable", (), (), "direct", "low", None, ())

    assert _resolve_global_state({"pressure+work": "supported_high", "pressure": "supported_low"}, {"high", "low"}, (high, low)) == "mixed"


def test_candidate_identity_binds_facts_and_semantic_bundle(
    normalized_time, bazi_facts, astrology_facts
) -> None:
    from destiny_personality.core_profile_builder import build_candidate_core_profile

    profile = build_candidate_core_profile(
        DeterministicChartFacts(normalized_time, bazi_facts, astrology_facts),
        fact_assurance="capability_reported",
    )

    assert profile.fact_fingerprint
    assert profile.candidate_profile_id != f"candidate-{profile.fact_fingerprint[:16]}"


def test_counterweight_is_reflected_in_state_audit(
    normalized_time, bazi_facts, astrology_facts
) -> None:
    from destiny_personality.core_profile_builder import build_candidate_core_profile

    bazi = bazi_facts.__class__(
        methodology_version=bazi_facts.methodology_version,
        year_pillar=bazi_facts.year_pillar, month_pillar=bazi_facts.month_pillar,
        day_pillar=bazi_facts.day_pillar, hour_pillar=bazi_facts.hour_pillar,
        hidden_stems=bazi_facts.hidden_stems,
        ten_gods=(
            TenGodFact("output", "食神", (PillarPosition.YEAR,), TenGodSourceKind.VISIBLE_STEM),
            TenGodFact("wealth", "正财", (PillarPosition.MONTH,), TenGodSourceKind.VISIBLE_STEM),
            TenGodFact("resource", "正印", (PillarPosition.DAY,), TenGodSourceKind.VISIBLE_STEM),
        ), relations=bazi_facts.relations,
    )
    profile = build_candidate_core_profile(DeterministicChartFacts(normalized_time, bazi, astrology_facts), fact_assurance="capability_reported")

    assert "counterweight contextualization retained" in profile.primitive_states["P002"].limitations
