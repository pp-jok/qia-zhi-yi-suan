from dataclasses import replace

from destiny_personality.calculation import DeterministicChartFacts


def test_candidate_profile_validator_accepts_auditable_partial_profile(
    normalized_time, bazi_facts, astrology_facts
) -> None:
    from destiny_personality.core_profile_builder import build_candidate_core_profile
    from destiny_personality.core_profile_validation import validate_candidate_profile

    profile = build_candidate_core_profile(
        DeterministicChartFacts(normalized_time, bazi_facts, astrology_facts),
        fact_assurance="capability_reported",
    )

    assert validate_candidate_profile(profile) == ()


def test_candidate_profile_has_no_disabled_dynamic_or_archetype_fields(
    normalized_time, bazi_facts, astrology_facts
) -> None:
    from destiny_personality.core_profile_builder import build_candidate_core_profile
    from destiny_personality.core_profile_validation import validate_candidate_profile

    profile = build_candidate_core_profile(
        DeterministicChartFacts(normalized_time, bazi_facts, astrology_facts),
        fact_assurance="capability_reported",
    )

    assert not hasattr(profile, "core_dynamics")
    assert not hasattr(profile, "archetype")


def test_candidate_profile_validator_rejects_unknown_alignment_status(
    normalized_time, bazi_facts, astrology_facts
) -> None:
    from destiny_personality.calculation import AstrologyAspectFact, TenGodFact, TenGodSourceKind
    from destiny_personality.calculation.models import PillarPosition
    from destiny_personality.core_profile_builder import build_candidate_core_profile
    from destiny_personality.core_profile_validation import validate_candidate_profile

    bazi = replace(
        bazi_facts,
        ten_gods=(
            TenGodFact("resource", "正印", (PillarPosition.YEAR,), TenGodSourceKind.VISIBLE_STEM),
            TenGodFact("authority", "正官", (PillarPosition.MONTH,), TenGodSourceKind.VISIBLE_STEM),
        ),
    )
    astrology = replace(
        astrology_facts,
        aspects=(AstrologyAspectFact("Uranus", "Sun", "trine", 1),),
    )
    profile = build_candidate_core_profile(
        DeterministicChartFacts(normalized_time, bazi, astrology),
        fact_assurance="capability_reported",
    )
    invalid_alignment = replace(profile.cross_system_alignments[0], status="forced")

    assert validate_candidate_profile(
        replace(profile, cross_system_alignments=(invalid_alignment,))
    ) == ("D1_ALIGNMENT_STATUS_INVALID",)
