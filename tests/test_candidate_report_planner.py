from dataclasses import replace

from destiny_personality.calculation import DeterministicChartFacts, TenGodFact, TenGodSourceKind
from destiny_personality.calculation.models import PillarPosition
import pytest


def test_candidate_report_planner_selects_only_supported_profile_topics(
    normalized_time, bazi_facts, astrology_facts
) -> None:
    from destiny_personality.core_profile_builder import build_candidate_core_profile
    from destiny_personality.report_planner import build_candidate_report_plan
    from destiny_personality.report_plan_validation import validate_candidate_report_plan

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

    plan = build_candidate_report_plan(profile)

    assert plan.schema_version == "candidate-report-plan-v1"
    assert plan.core_profile_ref == profile.candidate_profile_id
    assert [(topic.topic_id, topic.profile_refs) for topic in plan.selected_topics] == [
        ("primitive:P001", ("primitive_states.P001",)),
    ]
    assert {topic.topic_id for topic in plan.omitted_candidate_topics} == {
        "primitive:P002",
        "primitive:P003",
        "primitive:P004",
        "primitive:P005",
        "primitive:P006",
    }
    assert plan.rendering_constraints == ("no_new_semantic_conclusions",)
    assert validate_candidate_report_plan(plan, profile) == ()


def test_candidate_report_planner_rejects_a_stopped_execution_artifact(
    normalized_time, bazi_facts, astrology_facts
) -> None:
    from destiny_personality.core_profile_builder import build_candidate_core_profile
    from destiny_personality.report_planner import build_candidate_report_plan

    stopped = build_candidate_core_profile(
        DeterministicChartFacts(normalized_time, bazi_facts, astrology_facts),
        fact_assurance="none",
    )

    with pytest.raises(ValueError, match="stopped execution artifact"):
        build_candidate_report_plan(stopped)


def test_candidate_report_plan_validator_rejects_selected_topic_without_profile_reference(
    normalized_time, bazi_facts, astrology_facts
) -> None:
    from destiny_personality.core_profile_builder import build_candidate_core_profile
    from destiny_personality.report_plan_models import CandidateReportTopic
    from destiny_personality.report_planner import build_candidate_report_plan
    from destiny_personality.report_plan_validation import validate_candidate_report_plan

    profile = build_candidate_core_profile(
        DeterministicChartFacts(normalized_time, bazi_facts, astrology_facts),
        fact_assurance="capability_reported",
    )
    plan = build_candidate_report_plan(profile)
    invalid = replace(
        plan,
        selected_topics=(
            CandidateReportTopic("primitive:P001", (), "state:supported_high"),
        ),
    )

    assert validate_candidate_report_plan(invalid, profile) == (
        "REPORT_PLAN_PROFILE_REF_MISSING",
    )


def test_candidate_report_plan_validator_rejects_non_primitive_topic(
    normalized_time, bazi_facts, astrology_facts
) -> None:
    from destiny_personality.core_profile_builder import build_candidate_core_profile
    from destiny_personality.report_plan_models import CandidateReportTopic
    from destiny_personality.report_planner import build_candidate_report_plan
    from destiny_personality.report_plan_validation import validate_candidate_report_plan

    profile = build_candidate_core_profile(
        DeterministicChartFacts(normalized_time, bazi_facts, astrology_facts),
        fact_assurance="capability_reported",
    )
    plan = build_candidate_report_plan(profile)
    invalid = replace(
        plan,
        selected_topics=(
            CandidateReportTopic(
                "dynamic:D001", ("primitive_states.P001",), "state:supported_high"
            ),
        ),
    )

    assert validate_candidate_report_plan(invalid, profile) == (
        "REPORT_PLAN_TOPIC_NOT_PRIMITIVE",
        "REPORT_PLAN_UNKNOWN_TOPIC_SELECTED",
    )
