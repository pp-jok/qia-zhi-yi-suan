import json

import pytest

from destiny_personality.interpretive_codec import encode_interpretive_report
from destiny_personality.interpretive_models import (
    InterpretiveConclusion,
    InterpretiveCoreProfile,
)
from destiny_personality.interpretive_report import build_interpretive_report


@pytest.fixture
def profile() -> InterpretiveCoreProfile:
    topics = (
        ("baseline disposition", "steady", "核心倾向展现为稳定且谨慎。"),
        ("thinking and learning", "reflective", "思考与学习更倾向先观察再整合。"),
        ("expression and creation", "expressive", "表达与创作中容易主动呈现想法。"),
        ("relationships and boundaries", "selective", "关系中重视双向回应与边界感。"),
        ("work and drive", "structured", "工作推进偏好明确的目标和节奏。"),
        ("stress and energy", "paced", "压力下需要通过节奏切换恢复能量。"),
        ("growth tension", "adaptive", "成长往往发生在稳定与变化的拉扯中。"),
        ("synthesis", "integrated", "整体上可将观察、表达与行动连成一致节奏。"),
        ("decision rhythm", "deliberate", "决策节奏倾向先收集线索再落定。"),
    )
    conclusions = tuple(
        InterpretiveConclusion(
            topic=topic,
            direction=direction,
            interpretation=interpretation,
            supporting_signal_ids=(f"SIG-{index:02d}",),
            countervailing_signal_ids=(f"COUNTER-{index:02d}",)
            if topic == "growth tension"
            else (),
            confidence="exploratory" if topic == "growth tension" else "moderate",
            limitations=("仅作为传统象意的反思线索。",),
        )
        for index, (topic, direction, interpretation) in enumerate(topics, start=1)
    )
    return InterpretiveCoreProfile(
        mode="audited_interpretive",
        conclusions=conclusions,
        limitations=("不是实证性人格诊断。",),
        audit_refs=(
            "deterministic-facts:fact-123",
            "fact-qualification:qualification-456",
            "interpretive-rules:audited-interpretive-rules-v1",
            "source:test-fixture",
        ),
    )


def test_standard_report_has_user_readable_depth_and_audit_refs(profile):
    report = build_interpretive_report(profile, mode="standard")

    assert 8 <= len(report.sections) <= 12
    assert all(section.signal_ids for section in report.sections)
    assert all(section.limitation for section in report.sections)
    assert "传统命理" in report.boundary_statement
    assert report.audit_metadata.rule_bundle_refs == (
        "interpretive-rules:audited-interpretive-rules-v1",
    )
    assert report.audit_metadata.fact_refs == ("deterministic-facts:fact-123",)
    assert report.audit_metadata.qualification_refs == (
        "fact-qualification:qualification-456",
    )


def test_standard_report_contains_the_eight_named_topics(profile):
    report = build_interpretive_report(profile, mode="standard")

    assert tuple(section.title for section in report.sections[:8]) == (
        "核心底色",
        "思考与学习",
        "表达与创造",
        "关系与边界",
        "工作与驱动",
        "压力与能量",
        "成长张力",
        "综合观察",
    )
    assert report.sections[6].signal_ids == ("SIG-07", "COUNTER-07")
    assert report.sections[-1].title == "补充观察：decision rhythm"


def test_concise_report_is_shorter_than_standard(profile):
    concise = build_interpretive_report(profile, "concise")
    standard = build_interpretive_report(profile, "standard")

    assert len(concise.sections) < len(standard.sections)
    assert tuple(section.title for section in concise.sections) == (
        "核心轮廓",
        "思考与表达",
        "关系与行动",
        "压力与成长",
    )
    assert all(section.signal_ids for section in concise.sections)


def test_report_and_codec_are_deterministic_plain_data(profile):
    first = build_interpretive_report(profile, "standard")
    second = build_interpretive_report(profile, "standard")

    assert first == second
    payload = encode_interpretive_report(first)
    assert payload == encode_interpretive_report(second)
    assert payload["schema_version"] == "interpretive-report-v1"
    assert payload["mode"] == "standard"
    assert payload["sections"][0]["signal_ids"] == ["SIG-01"]
    assert payload["audit_metadata"]["profile_audit_refs"] == [
        "deterministic-facts:fact-123",
        "fact-qualification:qualification-456",
        "interpretive-rules:audited-interpretive-rules-v1",
        "source:test-fixture",
    ]
    json.dumps(payload, ensure_ascii=False)


def test_report_rejects_unsupported_mode_and_non_profile_input(profile):
    with pytest.raises(ValueError, match="INTERPRETIVE_REPORT_MODE_UNSUPPORTED"):
        build_interpretive_report(profile, "verbose")
    with pytest.raises(TypeError, match="INTERPRETIVE_CORE_PROFILE_REQUIRED"):
        build_interpretive_report({"conclusions": []}, "standard")


def test_report_rejects_profile_without_traceable_evidence():
    profile = InterpretiveCoreProfile(
        mode="audited_interpretive",
        conclusions=(
            InterpretiveConclusion(
                topic="stress",
                direction="unresolved",
                interpretation="No matched rule.",
                supporting_signal_ids=(),
                countervailing_signal_ids=(),
                confidence="insufficient",
                limitations=("No matched rule.",),
            ),
        ),
        limitations=("No supported conclusion.",),
        audit_refs=("source:test",),
    )

    with pytest.raises(ValueError, match="TRACEABLE_INTERPRETIVE_CONCLUSION_REQUIRED"):
        build_interpretive_report(profile, "concise")
