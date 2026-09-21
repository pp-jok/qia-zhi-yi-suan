from destiny_personality.calculation import DeterministicChartFacts


def test_candidate_builder_returns_auditable_partial_profile_for_candidate_facts(
    normalized_time, bazi_facts, astrology_facts
) -> None:
    from destiny_personality.core_profile_builder import (
        build_candidate_core_profile,
        normalize_core_profile,
    )

    facts = DeterministicChartFacts(normalized_time, bazi_facts, astrology_facts)

    first = build_candidate_core_profile(facts, fact_assurance="capability_reported")
    second = build_candidate_core_profile(facts, fact_assurance="capability_reported")

    assert first.schema_version == "candidate-core-profile-v1"
    assert first.candidate_profile_id.startswith("candidate-")
    assert first.semantic_capability_level == "primitive_only"
    assert first.fact_assurance == "capability_reported"
    assert first.semantic_model_assurance == "project_semantic_partial"
    assert first.bazi_primitive_candidates == ()
    assert first.astrology_primitive_candidates == ()
    assert set(first.primitive_states) == {"P001", "P002", "P003", "P004", "P005", "P006"}
    assert {state.state for state in first.primitive_states.values()} == {"unknown"}
    assert {
        limitation
        for state in first.primitive_states.values()
        for limitation in state.limitations
    } == {"no candidate evidence matched"}
    assert first.limitations == (
        "candidate mappings are pending production approval; "
        "relation and derived-dynamic rules remain disabled",
    )
    assert not hasattr(first, "core_dynamics")
    assert not hasattr(first, "archetype")
    assert normalize_core_profile(first) == normalize_core_profile(second)


def test_candidate_builder_activates_bazi_rule_only_with_required_evidence(
    normalized_time, bazi_facts, astrology_facts
) -> None:
    from destiny_personality.calculation import TenGodFact, TenGodSourceKind
    from destiny_personality.calculation.models import PillarPosition
    from destiny_personality.core_profile_builder import build_candidate_core_profile

    bazi_with_evidence = bazi_facts.__class__(
        methodology_version=bazi_facts.methodology_version,
        year_pillar=bazi_facts.year_pillar,
        month_pillar=bazi_facts.month_pillar,
        day_pillar=bazi_facts.day_pillar,
        hour_pillar=bazi_facts.hour_pillar,
        hidden_stems=bazi_facts.hidden_stems,
        ten_gods=(
            TenGodFact("peer", "比肩", (PillarPosition.YEAR,), TenGodSourceKind.VISIBLE_STEM),
            TenGodFact("output", "食神", (PillarPosition.MONTH,), TenGodSourceKind.VISIBLE_STEM),
        ),
        relations=bazi_facts.relations,
    )
    facts = DeterministicChartFacts(normalized_time, bazi_with_evidence, astrology_facts)

    profile = build_candidate_core_profile(facts, fact_assurance="capability_reported")

    assert [candidate.primitive_id for candidate in profile.bazi_primitive_candidates] == ["P001"]
    assert profile.primitive_states["P001"].state == "supported_high"


def test_candidate_builder_records_concrete_day_master_environment_evidence(
    normalized_time, bazi_facts, astrology_facts
) -> None:
    from destiny_personality.calculation import TenGodFact, TenGodSourceKind
    from destiny_personality.calculation.models import PillarPosition
    from destiny_personality.core_profile_builder import build_candidate_core_profile

    bazi = bazi_facts.__class__(
        methodology_version=bazi_facts.methodology_version,
        year_pillar=bazi_facts.year_pillar,
        month_pillar=bazi_facts.month_pillar,
        day_pillar=bazi_facts.day_pillar,
        hour_pillar=bazi_facts.hour_pillar,
        hidden_stems=bazi_facts.hidden_stems,
        ten_gods=(
            TenGodFact("peer", "比肩", (PillarPosition.YEAR,), TenGodSourceKind.VISIBLE_STEM),
            TenGodFact("output", "食神", (PillarPosition.MONTH,), TenGodSourceKind.VISIBLE_STEM),
        ),
        relations=bazi_facts.relations,
    )

    profile = build_candidate_core_profile(
        DeterministicChartFacts(normalized_time, bazi, astrology_facts),
        fact_assurance="capability_reported",
    )

    candidate = profile.bazi_primitive_candidates[0]
    assert (
        "bazi.day_master_environment:庚:metal:午:summer:"
        "candidate-bazi-day-master-environment-v1"
    ) in candidate.fact_refs


def test_candidate_builder_requires_bazi_evidence_from_distinct_pillars(
    normalized_time, bazi_facts, astrology_facts
) -> None:
    from destiny_personality.calculation import TenGodFact, TenGodSourceKind
    from destiny_personality.calculation.models import PillarPosition
    from destiny_personality.core_profile_builder import build_candidate_core_profile

    bazi_same_pillar = bazi_facts.__class__(
        methodology_version=bazi_facts.methodology_version,
        year_pillar=bazi_facts.year_pillar,
        month_pillar=bazi_facts.month_pillar,
        day_pillar=bazi_facts.day_pillar,
        hour_pillar=bazi_facts.hour_pillar,
        hidden_stems=bazi_facts.hidden_stems,
        ten_gods=(
            TenGodFact("peer", "比肩", (PillarPosition.YEAR,), TenGodSourceKind.VISIBLE_STEM),
            TenGodFact("output", "食神", (PillarPosition.YEAR,), TenGodSourceKind.VISIBLE_STEM),
        ),
        relations=bazi_facts.relations,
    )

    profile = build_candidate_core_profile(
        DeterministicChartFacts(normalized_time, bazi_same_pillar, astrology_facts),
        fact_assurance="capability_reported",
    )

    assert profile.bazi_primitive_candidates == ()


def test_candidate_builder_rejects_non_major_astrology_aspect(
    normalized_time, bazi_facts, astrology_facts
) -> None:
    from destiny_personality.calculation import AstrologyAspectFact
    from destiny_personality.core_profile_builder import build_candidate_core_profile

    astrology_with_minor_aspect = astrology_facts.__class__(
        methodology_version=astrology_facts.methodology_version,
        placements=astrology_facts.placements,
        aspects=(AstrologyAspectFact("Sun", "Mars", "semi_square", 1),),
        ascendant=astrology_facts.ascendant,
        mc=astrology_facts.mc,
        house_cusps=astrology_facts.house_cusps,
        dignities=astrology_facts.dignities,
    )

    profile = build_candidate_core_profile(
        DeterministicChartFacts(normalized_time, bazi_facts, astrology_with_minor_aspect),
        fact_assurance="capability_reported",
    )

    assert profile.astrology_primitive_candidates == ()


def test_candidate_builder_rejects_unknown_ten_god_origin(
    normalized_time, bazi_facts, astrology_facts
) -> None:
    from destiny_personality.calculation import TenGodFact
    from destiny_personality.calculation.models import PillarPosition
    from destiny_personality.core_profile_builder import build_candidate_core_profile

    bazi = bazi_facts.__class__(
        methodology_version=bazi_facts.methodology_version,
        year_pillar=bazi_facts.year_pillar,
        month_pillar=bazi_facts.month_pillar,
        day_pillar=bazi_facts.day_pillar,
        hour_pillar=bazi_facts.hour_pillar,
        hidden_stems=bazi_facts.hidden_stems,
        ten_gods=(
            TenGodFact("peer", "比肩", (PillarPosition.YEAR,)),
            TenGodFact("output", "食神", (PillarPosition.MONTH,)),
        ),
        relations=bazi_facts.relations,
    )

    profile = build_candidate_core_profile(
        DeterministicChartFacts(normalized_time, bazi, astrology_facts),
        fact_assurance="capability_reported",
    )

    assert profile.bazi_primitive_candidates == ()


def test_candidate_builder_records_dignity_and_angular_context_only_after_major_aspect(
    normalized_time, bazi_facts, astrology_facts
) -> None:
    from destiny_personality.calculation import AstrologyAspectFact, DignityFact
    from destiny_personality.core_profile_builder import build_candidate_core_profile

    astrology = astrology_facts.__class__(
        methodology_version=astrology_facts.methodology_version,
        placements=astrology_facts.placements,
        aspects=(AstrologyAspectFact("Sun", "Mars", "trine", 1),),
        ascendant=astrology_facts.ascendant,
        mc=astrology_facts.mc,
        house_cusps=astrology_facts.house_cusps,
        dignities=(DignityFact("Sun", "domicile"),),
    )

    profile = build_candidate_core_profile(
        DeterministicChartFacts(normalized_time, bazi_facts, astrology),
        fact_assurance="capability_reported",
    )

    candidate = next(item for item in profile.astrology_primitive_candidates if item.primitive_id == "P001")
    assert "astrology.aspects:Sun:trine:Mars:1" in candidate.fact_refs
    assert "astrology.dignities:Sun:domicile" in candidate.fact_refs
    assert "astrology.angular:Sun:1" in candidate.fact_refs


def test_candidate_builder_excludes_dignity_for_body_outside_the_rule(
    normalized_time, bazi_facts, astrology_facts
) -> None:
    from destiny_personality.calculation import AstrologyAspectFact, DignityFact
    from destiny_personality.core_profile_builder import build_candidate_core_profile

    astrology = astrology_facts.__class__(
        methodology_version=astrology_facts.methodology_version,
        placements=astrology_facts.placements,
        aspects=(AstrologyAspectFact("Sun", "Mars", "trine", 1),),
        ascendant=astrology_facts.ascendant,
        mc=astrology_facts.mc,
        house_cusps=astrology_facts.house_cusps,
        dignities=(DignityFact("Venus", "domicile"),),
    )

    profile = build_candidate_core_profile(
        DeterministicChartFacts(normalized_time, bazi_facts, astrology),
        fact_assurance="capability_reported",
    )

    candidate = next(item for item in profile.astrology_primitive_candidates if item.primitive_id == "P001")
    assert "astrology.dignities:Venus:domicile" not in candidate.fact_refs


def test_candidate_builder_keeps_astrology_candidates_source_isolated(
    normalized_time, bazi_facts, astrology_facts
) -> None:
    from destiny_personality.calculation import AstrologyAspectFact
    from destiny_personality.core_profile_builder import build_candidate_core_profile

    astrology_with_aspect = astrology_facts.__class__(
        methodology_version=astrology_facts.methodology_version,
        placements=astrology_facts.placements,
        aspects=(AstrologyAspectFact("Sun", "Mars", "trine", 1),),
        ascendant=astrology_facts.ascendant,
        mc=astrology_facts.mc,
        house_cusps=astrology_facts.house_cusps,
        dignities=astrology_facts.dignities,
    )

    facts = DeterministicChartFacts(normalized_time, bazi_facts, astrology_with_aspect)
    profile = build_candidate_core_profile(facts, fact_assurance="capability_reported")

    assert "P001" in {candidate.primitive_id for candidate in profile.astrology_primitive_candidates}
    assert profile.bazi_primitive_candidates == ()


def test_candidate_builder_returns_stopped_artifact_when_fact_assurance_is_none(
    normalized_time, bazi_facts, astrology_facts
) -> None:
    from destiny_personality.core_profile_builder import build_candidate_core_profile

    stopped = build_candidate_core_profile(
        DeterministicChartFacts(normalized_time, bazi_facts, astrology_facts),
        fact_assurance="none",
    )

    assert stopped.schema_version == "core-profile-stopped-execution-v1"
    assert stopped.fact_assurance == "none"
    assert stopped.failure_code == "FACT_ASSURANCE_NONE"
    assert stopped.semantic_conclusions == ()


def test_candidate_builder_records_cross_system_tension_without_overwriting_sources(
    normalized_time, bazi_facts, astrology_facts
) -> None:
    from destiny_personality.calculation import AstrologyAspectFact, TenGodFact, TenGodSourceKind
    from destiny_personality.calculation.models import PillarPosition
    from destiny_personality.core_profile_builder import build_candidate_core_profile

    bazi_with_evidence = bazi_facts.__class__(
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
    astrology_with_tension = astrology_facts.__class__(
        methodology_version=astrology_facts.methodology_version,
        placements=astrology_facts.placements,
        aspects=(AstrologyAspectFact("Uranus", "Sun", "trine", 1),),
        ascendant=astrology_facts.ascendant,
        mc=astrology_facts.mc,
        house_cusps=astrology_facts.house_cusps,
        dignities=astrology_facts.dignities,
    )

    profile = build_candidate_core_profile(
        DeterministicChartFacts(normalized_time, bazi_with_evidence, astrology_with_tension),
        fact_assurance="capability_reported",
    )

    alignment = next(item for item in profile.cross_system_alignments if item.primitive_id == "P002")
    assert alignment.status == "non_comparable"
    assert profile.primitive_states["P002"].state == "context_differentiated"
    assert profile.bazi_primitive_candidates[0].source_system == "bazi"
    assert profile.astrology_primitive_candidates[0].source_system == "astrology"


def test_candidate_builder_uses_c3_validation_for_matching_system_candidates(
    normalized_time, bazi_facts, astrology_facts
) -> None:
    from destiny_personality.calculation import AstrologyAspectFact, TenGodFact, TenGodSourceKind
    from destiny_personality.calculation.models import PillarPosition
    from destiny_personality.core_profile_builder import build_candidate_core_profile

    bazi = bazi_facts.__class__(
        methodology_version=bazi_facts.methodology_version,
        year_pillar=bazi_facts.year_pillar,
        month_pillar=bazi_facts.month_pillar,
        day_pillar=bazi_facts.day_pillar,
        hour_pillar=bazi_facts.hour_pillar,
        hidden_stems=bazi_facts.hidden_stems,
        ten_gods=(
            TenGodFact("peer", "比肩", (PillarPosition.YEAR,), TenGodSourceKind.VISIBLE_STEM),
            TenGodFact("output", "食神", (PillarPosition.MONTH,), TenGodSourceKind.VISIBLE_STEM),
        ),
        relations=bazi_facts.relations,
    )
    astrology = astrology_facts.__class__(
        methodology_version=astrology_facts.methodology_version,
        placements=astrology_facts.placements,
        aspects=(AstrologyAspectFact("Sun", "Mars", "trine", 1),),
        ascendant=astrology_facts.ascendant,
        mc=astrology_facts.mc,
        house_cusps=astrology_facts.house_cusps,
        dignities=astrology_facts.dignities,
    )

    profile = build_candidate_core_profile(
        DeterministicChartFacts(normalized_time, bazi, astrology),
        fact_assurance="capability_reported",
    )

    alignment = next(item for item in profile.cross_system_alignments if item.primitive_id == "P001")
    assert alignment.status == "validation"
