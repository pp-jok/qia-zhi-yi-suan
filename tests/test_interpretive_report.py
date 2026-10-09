from dataclasses import replace
import json
from pathlib import Path

import pytest

from destiny_personality.interpretive_codec import encode_interpretive_report
from destiny_personality.interpretive_models import (
    InterpretiveConclusion,
    InterpretiveCoreProfile,
    InterpretiveSignalProvenance,
    InterpretiveSystemProfile,
    InterpretiveSystemTopic,
    NarrativeSynthesisPacket,
)
from destiny_personality.interpretive_profile import build_interpretive_core_profile
from destiny_personality.interpretive_report import (
    _render_interpretive_report,
    build_interpretive_report,
)


def _provenance(*signal_ids: str) -> tuple[InterpretiveSignalProvenance, ...]:
    return tuple(
        InterpretiveSignalProvenance(
            signal_id=signal_id,
            system="bazi",
            fact_refs=(f"bazi.test[{index}].value",),
            traditional_rule_ref=f"tradition:{signal_id}",
            limitations=("仅作为传统象意的反思线索。",),
        )
        for index, signal_id in enumerate(signal_ids)
    )


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
            signal_provenance=_provenance(
                f"SIG-{index:02d}",
                *((f"COUNTER-{index:02d}",) if topic == "growth tension" else ()),
            ),
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
    report = _render_interpretive_report(profile, mode="standard")

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
    report = _render_interpretive_report(profile, mode="standard")

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
    assert report.sections[-1].title == "决策节奏"


def test_standard_report_consolidates_supported_topics_beyond_twelve(profile):
    extra_conclusions = tuple(
        InterpretiveConclusion(
            topic=f"supported extra topic {index}",
            direction="bounded",
            interpretation=f"额外受支持结论 {index}。",
            supporting_signal_ids=(f"EXTRA-{index:02d}",),
            countervailing_signal_ids=(),
            confidence="moderate",
            limitations=("仅作为传统象意的反思线索。",),
            signal_provenance=_provenance(f"EXTRA-{index:02d}"),
        )
        for index in range(10, 14)
    )
    expanded = replace(
        profile,
        conclusions=profile.conclusions + extra_conclusions,
    )

    report = _render_interpretive_report(expanded, "standard")

    expected_signal_ids = {
        signal_id
        for conclusion in expanded.conclusions
        for signal_id in (
            conclusion.supporting_signal_ids
            + conclusion.countervailing_signal_ids
        )
    }
    rendered_signal_ids = {
        signal_id
        for section in report.sections
        for signal_id in section.signal_ids
    }
    assert len(report.sections) == 12
    assert rendered_signal_ids == expected_signal_ids
    assert all(
        tuple(item.signal_id for item in section.signal_provenance)
        == section.signal_ids
        for section in report.sections
    )
    assert "额外受支持结论 13" in report.sections[-1].content


def test_concise_report_is_shorter_than_standard(profile):
    concise = _render_interpretive_report(profile, "concise")
    standard = _render_interpretive_report(profile, "standard")

    assert len(concise.sections) < len(standard.sections)
    assert tuple(section.title for section in concise.sections) == (
        "核心轮廓",
        "思考与表达",
        "关系与行动",
        "压力与成长",
    )
    assert all(section.signal_ids for section in concise.sections)


def test_report_and_codec_are_deterministic_plain_data(profile):
    first = _render_interpretive_report(profile, "standard")
    second = _render_interpretive_report(profile, "standard")

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
        _render_interpretive_report(profile, "verbose")
    with pytest.raises(TypeError, match="INTERPRETIVE_CORE_PROFILE_REQUIRED"):
        _render_interpretive_report({"conclusions": []}, "standard")


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
        audit_refs=(
            "deterministic-facts:fact-123",
            "fact-qualification:qualification-456",
            "interpretive-rules:audited-interpretive-rules-v1",
        ),
    )

    with pytest.raises(ValueError, match="TRACEABLE_INTERPRETIVE_CONCLUSION_REQUIRED"):
        _render_interpretive_report(profile, "concise")


def test_sparse_profile_does_not_relabel_or_duplicate_a_conclusion():
    interpretation = "仅有的证据结论。"
    sparse_profile = InterpretiveCoreProfile(
        mode="audited_interpretive",
        conclusions=(
            InterpretiveConclusion(
                topic="expression and creation",
                direction="expressive",
                interpretation=interpretation,
                supporting_signal_ids=("SIG-SPARSE",),
                countervailing_signal_ids=(),
                confidence="moderate",
                limitations=("只覆盖表达主题。",),
                signal_provenance=_provenance("SIG-SPARSE"),
            ),
        ),
        limitations=("当前证据覆盖有限。",),
        audit_refs=(
            "deterministic-facts:fact-sparse",
            "fact-qualification:qualification-sparse",
            "interpretive-rules:audited-interpretive-rules-v1",
        ),
    )

    standard = _render_interpretive_report(sparse_profile, "standard")
    concise = _render_interpretive_report(sparse_profile, "concise")

    assert tuple(section.title for section in standard.sections) == (
        "表达与创造",
    )
    assert tuple(section.title for section in concise.sections) == (
        "思考与表达",
    )
    assert all(section.kind == "analysis" for section in standard.sections)
    assert sum(
        section.content.count(interpretation) for section in standard.sections
    ) == 1
    assert standard.sections[0].signal_ids == ("SIG-SPARSE",)
    assert "核心底色" not in {section.title for section in standard.sections}
    assert "关系与边界" not in {section.title for section in standard.sections}


def test_actual_bundle_profile_renders_controlled_chinese_only(qualified_facts):
    profile = build_interpretive_core_profile(qualified_facts)

    report = _render_interpretive_report(profile, "standard")
    visible_text = "".join(
        section.title + section.content + section.limitation
        for section in report.sections
    )

    assert report.sections
    assert all(
        any("\u4e00" <= char <= "\u9fff" for char in section.content)
        for section in report.sections
    )
    assert not any("a" <= char.casefold() <= "z" for char in visible_text)
    assert "Planet-sign symbolism" not in visible_text
    assert "traditional interpretive lens" not in visible_text
    assert "House system and birth-time uncertainty" not in visible_text
    assert "style of expression" not in visible_text


def test_rule_family_evidence_values_survive_public_report_rendering():
    def report_text(
        sun_quality: str, aspect_type: str, ten_god: str
    ) -> str:
        conclusions = (
            InterpretiveConclusion(
                topic="style of expression",
                direction="outward",
                interpretation=(
                    "太阳所在星座的元素与模式，提供核心意志如何定义和表达"
                    f"自我的象征语言。（命中依据：元素：{sun_quality}；"
                    f"模式：{'开创' if sun_quality == '火象' else '固定'}；"
                    f"十神：{ten_god}）"
                ),
                supporting_signal_ids=(
                    "BAZI-TEN-GOD-EXPRESSION",
                    "ASTROLOGY-PLANET-SIGN-EXPRESSION",
                ),
                countervailing_signal_ids=(),
                confidence="moderate",
                limitations=("仅作为传统象意的反思线索。",),
                signal_provenance=_provenance(
                    "BAZI-TEN-GOD-EXPRESSION",
                    "ASTROLOGY-PLANET-SIGN-EXPRESSION",
                ),
            ),
            InterpretiveConclusion(
                topic="interacting tendencies",
                direction="integrative",
                interpretation=(
                    "日月主要相位用于观察自我意志与情绪需求如何互动。"
                    f"（命中依据：相位：{aspect_type}）"
                ),
                supporting_signal_ids=("ASTROLOGY-ASPECT-DIGNITY-CONTEXT",),
                countervailing_signal_ids=(),
                confidence="exploratory",
                limitations=("仅作为传统象意的反思线索。",),
                signal_provenance=_provenance(
                    "ASTROLOGY-ASPECT-DIGNITY-CONTEXT",
                ),
            ),
        )
        profile = InterpretiveCoreProfile(
            mode="audited_interpretive",
            conclusions=conclusions,
            limitations=("不是实证性人格诊断。",),
            audit_refs=(
                "deterministic-facts:report-values",
                "fact-qualification:report-values",
                "interpretive-rules:audited-interpretive-rules-v2",
            ),
        )
        return "".join(
            section.content
            for section in _render_interpretive_report(profile, "standard").sections
        )

    known = report_text("火象", "合相", "正印")
    changed = report_text("土象", "对冲", "正财")

    for value in ("火象", "开创", "合相", "正印"):
        assert value in known
        assert value not in changed
    for value in ("土象", "固定", "对冲", "正财"):
        assert value in changed
        assert value not in known


@pytest.mark.parametrize(
    ("mode", "audit_refs"),
    (
        (
            "not_audited",
            (
                "deterministic-facts:fact-123",
                "fact-qualification:qualification-456",
                "interpretive-rules:audited-interpretive-rules-v1",
            ),
        ),
        (
            "audited_interpretive",
            (
                "fact-qualification:qualification-456",
                "interpretive-rules:audited-interpretive-rules-v1",
            ),
        ),
        (
            "audited_interpretive",
            (
                "deterministic-facts:fact-123",
                "interpretive-rules:audited-interpretive-rules-v1",
            ),
        ),
        (
            "audited_interpretive",
            (
                "deterministic-facts:fact-123",
                "fact-qualification:qualification-456",
            ),
        ),
        ("audited_interpretive", None),
        (
            "audited_interpretive",
            (
                "deterministic-facts:fact-123",
                "fact-qualification:qualification-456",
                7,
            ),
        ),
    ),
)
def test_report_rejects_non_audited_or_partial_profile(profile, mode, audit_refs):
    invalid = InterpretiveCoreProfile(
        mode=mode,
        conclusions=profile.conclusions,
        limitations=profile.limitations,
        audit_refs=audit_refs,
    )

    with pytest.raises(ValueError, match="AUDITED_INTERPRETIVE_PROFILE_REQUIRED"):
        _render_interpretive_report(invalid, "standard")


def test_report_snapshots_mutable_profile_audit_refs(profile):
    audit_refs = list(profile.audit_refs)
    mutable_profile = InterpretiveCoreProfile(
        mode="audited_interpretive",
        conclusions=profile.conclusions,
        limitations=profile.limitations,
        audit_refs=audit_refs,
    )

    report = _render_interpretive_report(mutable_profile, "standard")
    audit_refs.append("source:mutated-after-build")

    assert report.audit_metadata.profile_audit_refs == profile.audit_refs


def test_public_report_builder_rejects_caller_forged_profile(profile):
    forged = InterpretiveCoreProfile(
        mode="audited_interpretive",
        conclusions=(
            InterpretiveConclusion(
                topic="baseline disposition",
                direction="diagnostic",
                interpretation="你有临床人格障碍，必须立即服药。",
                supporting_signal_ids=("FORGED-SIGNAL",),
                countervailing_signal_ids=(),
                confidence="high",
                limitations=(),
            ),
        ),
        limitations=(),
        audit_refs=(
            "deterministic-facts:forged",
            "fact-qualification:forged",
            "interpretive-rules:audited-interpretive-rules-v1",
        ),
    )

    with pytest.raises(ValueError, match="QUALIFIED_FACTS_REQUIRED"):
        build_interpretive_report(forged, "standard")


def test_public_report_builder_accepts_only_valid_qualified_route(qualified_facts):
    report = build_interpretive_report(qualified_facts, "standard")

    assert report.sections
    assert report.audit_metadata.fact_refs == (
        f"deterministic-facts:{qualified_facts.fact_fingerprint}",
    )


def _fixture_facts(scenario: str):
    from destiny_personality.deterministic_facts_codec import (
        load_qualified_deterministic_facts,
    )

    fixture_directory = Path(__file__).parent / "fixtures" / "interpretive"
    return load_qualified_deterministic_facts(
        fixture_directory / f"{scenario}-facts.json",
        fixture_directory / f"{scenario}-qualification.json",
    )


@pytest.fixture
def sparse_facts():
    return _fixture_facts("contrast_a")


@pytest.fixture
def rich_facts():
    return _fixture_facts("tension")


def test_sparse_report_stays_short_without_audit_sections(sparse_facts):
    report = build_interpretive_report(sparse_facts, "standard")

    assert 3 <= len(report.sections) <= 4
    assert all(section.kind == "analysis" for section in report.sections)


def test_rich_report_has_multiple_deep_reader_topics(rich_facts):
    assert len(build_interpretive_report(rich_facts, "standard").sections) >= 6


def test_reader_sections_are_conclusion_first_and_evidence_backed(rich_facts):
    report = build_interpretive_report(rich_facts, "standard")

    for section in report.sections:
        assert section.content.startswith("结论：")
        claim_count = section.content.count("结论：")
        assert section.content.count("形成机制：") == claim_count
        assert section.content.count("常见表现：") == claim_count
        assert section.content.count("情境变化：") == claim_count
        assert section.content.count("把握度：") == claim_count


def test_reader_body_does_not_invent_maturity_or_imbalance(rich_facts):
    visible_text = "".join(
        section.content for section in build_interpretive_report(
            rich_facts, "standard"
        ).sections
    )

    assert "成熟表现" not in visible_text
    assert "失衡表现" not in visible_text


def test_each_claim_uses_only_its_supporting_mechanism(rich_facts):
    report = build_interpretive_report(rich_facts, "standard")
    expression = next(
        section for section in report.sections if section.title == "表达与创造"
    )
    outward_claim, reflective_claim = expression.content.splitlines()
    outward_mechanism = outward_claim.split("形成机制：", 1)[1].split(
        "常见表现：", 1
    )[0]
    reflective_mechanism = reflective_claim.split("形成机制：", 1)[1].split(
        "常见表现：", 1
    )[0]

    assert "核心意志借由" in outward_mechanism
    assert "通过接收信息" not in outward_mechanism
    assert "通过接收信息" in reflective_mechanism
    assert "核心意志借由" not in reflective_mechanism


def test_same_system_claim_uses_only_its_exact_supporting_narrative_evidence():
    supporting = (
        InterpretiveSignalProvenance(
            signal_id="SIG-OUTWARD",
            system="bazi",
            fact_refs=("bazi.test[0].value",),
            traditional_rule_ref="tradition:SIG-OUTWARD",
            limitations=("仅作为传统象意的反思线索。",),
            mechanism="外向机制。",
            likely_expression="外向表现。",
            contexts=("公开场景",),
        ),
        InterpretiveSignalProvenance(
            signal_id="SIG-REFLECTIVE",
            system="bazi",
            fact_refs=("bazi.test[1].value",),
            traditional_rule_ref="tradition:SIG-REFLECTIVE",
            limitations=("仅作为传统象意的反思线索。",),
            mechanism="反思机制。",
            likely_expression="反思表现。",
            contexts=("独处场景",),
        ),
    )
    outward_provenance = supporting
    reflective_provenance = tuple(reversed(supporting))
    shared_topic = InterpretiveSystemTopic(
        topic="style of expression",
        directions=("outward", "reflective"),
        signal_ids=("SIG-OUTWARD", "SIG-REFLECTIVE"),
        interpretations=("外向表达。", "反思表达。"),
        mechanisms=("外向机制。", "反思机制。"),
        likely_expressions=("外向表现。", "反思表现。"),
        contexts=("公开场景", "独处场景"),
        limitations=("仅作为传统象意的反思线索。",),
        signal_provenance=supporting,
    )
    packet = NarrativeSynthesisPacket(
        bazi_profile=InterpretiveSystemProfile(
            system="bazi",
            topics=(shared_topic,),
            signal_ids=("SIG-OUTWARD", "SIG-REFLECTIVE"),
            limitations=(),
        ),
        astrology_profile=InterpretiveSystemProfile(
            system="astrology", topics=(), signal_ids=(), limitations=()
        ),
        alignments=(),
        tensions=(),
        limitations=(),
        audit_refs=(),
    )
    profile = InterpretiveCoreProfile(
        mode="audited_interpretive",
        conclusions=(
            InterpretiveConclusion(
                topic="style of expression",
                direction="outward",
                interpretation="外向表达。",
                supporting_signal_ids=("SIG-OUTWARD",),
                countervailing_signal_ids=("SIG-REFLECTIVE",),
                confidence="exploratory",
                limitations=("仅作为传统象意的反思线索。",),
                signal_provenance=outward_provenance,
            ),
            InterpretiveConclusion(
                topic="style of expression",
                direction="reflective",
                interpretation="反思表达。",
                supporting_signal_ids=("SIG-REFLECTIVE",),
                countervailing_signal_ids=("SIG-OUTWARD",),
                confidence="exploratory",
                limitations=("仅作为传统象意的反思线索。",),
                signal_provenance=reflective_provenance,
            ),
        ),
        limitations=(),
        audit_refs=(
            "deterministic-facts:same-system",
            "fact-qualification:same-system",
            "interpretive-rules:audited-interpretive-rules-v2",
        ),
        synthesis_packet=packet,
    )

    claims = _render_interpretive_report(profile, "standard").sections[0].content.splitlines()

    assert "外向机制" in claims[0]
    assert "反思机制" not in claims[0]
    assert "外向表现" in claims[0]
    assert "反思表现" not in claims[0]
    assert "公开场景" in claims[0]
    assert "独处场景" not in claims[0]
    assert "反思机制" in claims[1]
    assert "外向机制" not in claims[1]


def test_reader_body_keeps_audit_terms_out_of_narrative(rich_facts):
    report = build_interpretive_report(rich_facts, "standard")
    visible_text = "".join(section.content for section in report.sections)

    assert not any("a" <= char.casefold() <= "z" for char in visible_text)
    assert "BAZI-TEN-GOD-EXPRESSION" not in visible_text
    assert "astrology.placements" not in visible_text
