from destiny_personality.calculation import DeterministicChartFacts, TenGodFact, TenGodSourceKind
from destiny_personality.calculation.models import PillarPosition


def test_candidate_pipeline_returns_valid_profile_and_contained_plan(
    normalized_time, bazi_facts, astrology_facts
) -> None:
    from destiny_personality.candidate_pipeline import execute_candidate_pipeline

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

    execution = execute_candidate_pipeline(
        DeterministicChartFacts(normalized_time, bazi, astrology_facts),
        fact_assurance="capability_reported",
    )

    assert execution.status == "candidate_complete"
    assert execution.profile_validation_errors == ()
    assert execution.report_plan_validation_errors == ()
    assert execution.report_plan is not None
    assert execution.report_plan.selected_topics[0].topic_id == "primitive:P001"


def test_candidate_pipeline_stops_before_planning_when_fact_assurance_is_none(
    normalized_time, bazi_facts, astrology_facts
) -> None:
    from destiny_personality.candidate_pipeline import execute_candidate_pipeline

    execution = execute_candidate_pipeline(
        DeterministicChartFacts(normalized_time, bazi_facts, astrology_facts),
        fact_assurance="none",
    )

    assert execution.status == "stopped"
    assert execution.report_plan is None
    assert execution.profile_validation_errors == ("FACT_ASSURANCE_NONE",)
