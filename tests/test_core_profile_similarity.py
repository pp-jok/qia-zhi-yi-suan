from destiny_personality.calculation import DeterministicChartFacts, TenGodFact, TenGodSourceKind
from destiny_personality.calculation.models import PillarPosition


def test_candidate_similarity_preserves_structural_difference_without_unapproved_score(
    normalized_time, bazi_facts, astrology_facts
) -> None:
    from destiny_personality.core_profile_builder import build_candidate_core_profile
    from destiny_personality.core_profile_similarity import compare_candidate_profiles

    baseline = build_candidate_core_profile(
        DeterministicChartFacts(normalized_time, bazi_facts, astrology_facts),
        fact_assurance="capability_reported",
    )
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
    contrasted = build_candidate_core_profile(
        DeterministicChartFacts(normalized_time, bazi_with_evidence, astrology_facts),
        fact_assurance="capability_reported",
    )

    comparison = compare_candidate_profiles(baseline, contrasted)

    assert comparison.case_pair == (baseline.candidate_profile_id, contrasted.candidate_profile_id)
    assert comparison.primitive_state_pairs["P001"] == ("unknown", "supported_high")
    assert comparison.primitive_state_context_overlap == 0.0
    assert comparison.primitive_state_context_overlap_status == "calibrated"
    assert comparison.dynamic_family_pole_overlap_status == "not_applicable"
    assert comparison.fate_theme_overlap_status == "not_applicable"
    assert comparison.overall_score == 0.0


def test_candidate_similarity_matrix_has_one_diagnostic_cell_per_unique_pair(
    normalized_time, bazi_facts, astrology_facts
) -> None:
    from destiny_personality.core_profile_builder import build_candidate_core_profile
    from destiny_personality.core_profile_similarity import build_candidate_similarity_matrix

    baseline = build_candidate_core_profile(
        DeterministicChartFacts(normalized_time, bazi_facts, astrology_facts),
        fact_assurance="capability_reported",
    )
    changed_bazi = bazi_facts.__class__(
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
    contrasted = build_candidate_core_profile(
        DeterministicChartFacts(normalized_time, changed_bazi, astrology_facts),
        fact_assurance="capability_reported",
    )

    matrix = build_candidate_similarity_matrix((baseline, contrasted, baseline))

    assert len(matrix) == 1
    assert matrix[0].case_pair == (baseline.candidate_profile_id, contrasted.candidate_profile_id)
    assert matrix[0].primitive_state_context_overlap_status == "calibrated"


def test_candidate_calibration_rejects_a_contrast_pair_above_the_frozen_threshold() -> None:
    from destiny_personality.core_profile_similarity import (
        CandidateProfileComparison,
        evaluate_candidate_similarity_matrix,
    )

    result = evaluate_candidate_similarity_matrix(
        (
            CandidateProfileComparison(
                case_pair=("candidate-a", "candidate-b"),
                primitive_state_pairs={},
                primitive_state_context_overlap=0.8,
                primitive_state_context_overlap_status="calibrated",
                signature_primitive_overlap=None,
                signature_primitive_overlap_status="not_applicable",
                dynamic_family_pole_overlap=None,
                dynamic_family_pole_overlap_status="not_applicable",
                fate_theme_overlap=None,
                fate_theme_overlap_status="not_applicable",
                overall_score=0.8,
            ),
        )
    )

    assert result.max_similarity == 0.8
    assert result.threshold == 0.75
    assert result.errors == ("CANDIDATE_CONTRAST_SIMILARITY_EXCEEDED",)
