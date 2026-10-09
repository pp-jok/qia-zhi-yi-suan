"""Deterministic Chinese reports built only from qualified chart facts."""

from dataclasses import dataclass, replace
from typing import Iterable, Literal, Optional, Sequence, Tuple

from .deterministic_facts_codec import QualifiedFacts, require_qualified_facts
from .interpretive_models import (
    InterpretiveConclusion,
    InterpretiveCoreProfile,
    InterpretiveSignalProvenance,
    NarrativeSynthesisPacket,
)


InterpretiveReportMode = Literal["standard", "concise"]


@dataclass(frozen=True)
class InterpretiveReportSection:
    """A reader-facing section with an explicit evidence and limitation trail."""

    section_id: str
    title: str
    content: str
    signal_ids: Tuple[str, ...]
    limitation: str
    signal_provenance: Tuple[InterpretiveSignalProvenance, ...]
    kind: Literal["analysis"] = "analysis"


@dataclass(frozen=True)
class InterpretiveReportAuditMetadata:
    """Profile-carried provenance grouped for product and audit consumers."""

    rule_bundle_refs: Tuple[str, ...]
    fact_refs: Tuple[str, ...]
    qualification_refs: Tuple[str, ...]
    profile_audit_refs: Tuple[str, ...]
    fact_mode: str
    birth_time_status: str
    time_sensitivity_reasons: Tuple[str, ...]
    omitted_time_sensitive_claims: Tuple[str, ...]


@dataclass(frozen=True)
class InterpretiveReport:
    """An audited, non-diagnostic traditional-interpretation report."""

    schema_version: Literal["interpretive-report-v1"]
    mode: InterpretiveReportMode
    title: str
    sections: Tuple[InterpretiveReportSection, ...]
    boundary_statement: str
    audit_metadata: InterpretiveReportAuditMetadata


@dataclass(frozen=True)
class _SignalRendering:
    title: str
    body: str
    limitation: str


_STANDARD_TOPIC_ORDER = (
    "核心底色",
    "思考与学习",
    "表达与创造",
    "关系与边界",
    "工作与驱动",
    "压力与能量",
    "成长张力",
    "综合观察",
)

_TOPIC_TITLES = {
    "baseline disposition": "核心底色",
    "thinking and learning": "思考与学习",
    "expression and creation": "表达与创造",
    "expression and resource exchange": "表达与创造",
    "style of expression": "表达与创造",
    "creative output": "表达与创造",
    "thinking and communication": "思考与学习",
    "relationships and boundaries": "关系与边界",
    "contextual dynamics": "关系与边界",
    "relating and values": "关系与边界",
    "work and drive": "工作与驱动",
    "action style": "工作与驱动",
    "stress and energy": "压力与能量",
    "growth tension": "成长张力",
    "interacting tendencies": "成长张力",
    "growth orientation": "成长取向",
    "emotional processing": "情绪与安全感",
    "expression conditions": "表达条件",
    "life arena": "生活重心",
    "agency": "自主与协作",
    "resource handling": "资源与落实",
    "structure and pressure": "责任与压力",
    "recurring emphasis": "反复主题",
    "boundaries and mastery": "边界与长期建设",
    "synthesis": "综合观察",
    "decision rhythm": "决策节奏",
    "核心底色": "核心底色",
    "思考与学习": "思考与学习",
    "表达与创造": "表达与创造",
    "关系与边界": "关系与边界",
    "工作与驱动": "工作与驱动",
    "压力与能量": "压力与能量",
    "成长张力": "成长张力",
    "综合观察": "综合观察",
    "决策节奏": "决策节奏",
}

_SIGNAL_RENDERINGS = {
    "BAZI-TEN-GOD-EXPRESSION": _SignalRendering(
        title="表达与创造",
        body="传统十神关系可用于观察表达、支持与约束之间的互动方式。",
        limitation="需结合完整命局理解，不用于判定实际行为。",
    ),
    "BAZI-RELATION-DYNAMICS": _SignalRendering(
        title="关系与边界",
        body="地支关系可作为观察情境中亲和、拉扯与边界的象征性线索。",
        limitation="局部关系必须放回整体命局，不构成因果预测。",
    ),
    "ASTROLOGY-PLANET-SIGN-EXPRESSION": _SignalRendering(
        title="表达与创造",
        body="行星、星座与宫位的组合可作为观察表达方式的象征性线索。",
        limitation="宫制与出生时间不确定性可能改变解读语境。",
    ),
    "ASTROLOGY-ASPECT-DIGNITY-CONTEXT": _SignalRendering(
        title="成长张力",
        body="相位与尊贵状态可用于整理不同倾向之间的象征性张力。",
        limitation="解读受容许度与整体星盘影响，不用于诊断或预测。",
    ),
}

_CONCISE_TOPIC_ORDER = (
    "核心轮廓",
    "思考与表达",
    "关系与行动",
    "压力与成长",
    "补充观察",
)

_CONCISE_TITLE_BY_STANDARD_TITLE = {
    "核心底色": "核心轮廓",
    "综合观察": "核心轮廓",
    "思考与学习": "思考与表达",
    "表达与创造": "思考与表达",
    "决策节奏": "思考与表达",
    "关系与边界": "关系与行动",
    "工作与驱动": "关系与行动",
    "压力与能量": "压力与成长",
    "成长张力": "压力与成长",
}

_CONFIDENCE_LABELS = {
    "high": "高",
    "moderate": "中等",
    "exploratory": "探索性",
    "insufficient": "证据不足",
}

_BOUNDARY_STATEMENT = (
    "本报告是基于传统命理与占星象意的反思性文本，"
    "不是实证性人格测量、医疗或心理诊断，也不应代替重大生活决策。"
)


def build_interpretive_report(
    qualified_facts: QualifiedFacts,
    mode: InterpretiveReportMode,
) -> InterpretiveReport:
    """Build the public product report through the qualified-facts boundary."""

    qualified = require_qualified_facts(qualified_facts)
    from .interpretive_profile import build_interpretive_core_profile

    return _render_interpretive_report(
        build_interpretive_core_profile(qualified), mode
    )


def _render_interpretive_report(
    profile: InterpretiveCoreProfile,
    mode: InterpretiveReportMode,
) -> InterpretiveReport:
    """Render an internally synthesized profile after provenance validation."""

    if not isinstance(profile, InterpretiveCoreProfile):
        raise TypeError("INTERPRETIVE_CORE_PROFILE_REQUIRED")
    if mode not in {"standard", "concise"}:
        raise ValueError("INTERPRETIVE_REPORT_MODE_UNSUPPORTED")

    try:
        audit_refs = tuple(profile.audit_refs)
    except TypeError as error:
        raise ValueError("AUDITED_INTERPRETIVE_PROFILE_REQUIRED") from error
    if (
        profile.mode != "audited_interpretive"
        or not audit_refs
        or any(not isinstance(ref, str) or not ref for ref in audit_refs)
    ):
        raise ValueError("AUDITED_INTERPRETIVE_PROFILE_REQUIRED")
    audit_metadata = _audit_metadata(profile, audit_refs)
    if (
        not audit_metadata.rule_bundle_refs
        or not audit_metadata.fact_refs
        or not audit_metadata.qualification_refs
    ):
        raise ValueError("AUDITED_INTERPRETIVE_PROFILE_REQUIRED")

    conclusions = tuple(
        conclusion
        for conclusion in tuple(profile.conclusions)
        if _signal_ids((conclusion,))
    )
    if not conclusions:
        raise ValueError("TRACEABLE_INTERPRETIVE_CONCLUSION_REQUIRED")
    if any(not _conclusion_provenance_is_complete(item) for item in conclusions):
        raise ValueError("TRACEABLE_INTERPRETIVE_PROVENANCE_REQUIRED")

    if mode == "standard":
        sections = _build_standard_sections(
            conclusions,
            tuple(profile.limitations),
            profile.synthesis_packet,
        )
        title = "审计型传统命理解读·标准版"
    else:
        sections = _build_concise_sections(
            conclusions,
            tuple(profile.limitations),
            profile.synthesis_packet,
        )
        title = "审计型传统命理解读·精简版"

    if profile.birth_time_status == "unavailable_or_uncertain":
        sections = _include_missing_time_notice(sections)

    return InterpretiveReport(
        schema_version="interpretive-report-v1",
        mode=mode,
        title=title,
        sections=sections,
        boundary_statement=_BOUNDARY_STATEMENT,
        audit_metadata=audit_metadata,
    )


def _build_standard_sections(
    conclusions: Tuple[InterpretiveConclusion, ...],
    profile_limitations: Tuple[str, ...],
    synthesis_packet: Optional[NarrativeSynthesisPacket] = None,
) -> Tuple[InterpretiveReportSection, ...]:
    grouped = _group_standard_conclusions(conclusions)
    ordered_titles = tuple(
        title for title in _STANDARD_TOPIC_ORDER if title in grouped
    ) + tuple(title for title in grouped if title not in _STANDARD_TOPIC_ORDER)
    sections = [
        _section(
            section_id=f"standard-{index:02d}",
            title=title,
            conclusions=tuple(grouped[title]),
            profile_limitations=profile_limitations,
            synthesis_packet=synthesis_packet,
        )
        for index, title in enumerate(ordered_titles[:12], start=1)
    ]
    return tuple(sections)


def _build_concise_sections(
    conclusions: Tuple[InterpretiveConclusion, ...],
    profile_limitations: Tuple[str, ...],
    synthesis_packet: Optional[NarrativeSynthesisPacket] = None,
) -> Tuple[InterpretiveReportSection, ...]:
    standard_groups = _group_standard_conclusions(conclusions)
    grouped = {}
    for standard_title, grouped_conclusions in standard_groups.items():
        concise_title = _CONCISE_TITLE_BY_STANDARD_TITLE.get(
            standard_title, "补充观察"
        )
        grouped.setdefault(concise_title, []).extend(grouped_conclusions)
    sections = [
        _section(
            section_id=f"concise-{index:02d}",
            title=title,
            conclusions=tuple(grouped[title]),
            profile_limitations=profile_limitations,
            synthesis_packet=synthesis_packet,
        )
        for index, title in enumerate(_CONCISE_TOPIC_ORDER, start=1)
        if title in grouped
    ]
    return tuple(sections)


def _group_standard_conclusions(
    conclusions: Tuple[InterpretiveConclusion, ...],
) -> dict:
    grouped = {}
    unknown_titles = {}
    for conclusion in conclusions:
        title = _controlled_title(conclusion)
        if title is None:
            if conclusion.topic not in unknown_titles:
                unknown_titles[conclusion.topic] = (
                    f"补充观察{len(unknown_titles) + 1}"
                )
            title = unknown_titles[conclusion.topic]
        grouped.setdefault(title, []).append(conclusion)
    return grouped


def _controlled_title(
    conclusion: InterpretiveConclusion,
) -> Optional[str]:
    title = _TOPIC_TITLES.get(conclusion.topic.casefold().strip())
    if title is not None:
        return title
    for signal_id in _signal_ids((conclusion,)):
        rendering = _SIGNAL_RENDERINGS.get(signal_id)
        if rendering is not None:
            return rendering.title
    return None


def _section(
    *,
    section_id: str,
    title: str,
    conclusions: Tuple[InterpretiveConclusion, ...],
    profile_limitations: Tuple[str, ...],
    synthesis_packet: Optional[NarrativeSynthesisPacket],
) -> InterpretiveReportSection:
    statements = "\n".join(
        _render_claim(conclusion, synthesis_packet)
        for conclusion in conclusions
    )
    limitation_values = _controlled_limitations(
        conclusions, profile_limitations
    )
    return InterpretiveReportSection(
        section_id=section_id,
        kind="analysis",
        title=title,
        content=statements,
        signal_ids=_signal_ids(conclusions),
        limitation="；".join(limitation_values),
        signal_provenance=_signal_provenance(conclusions),
    )


def _render_claim(
    conclusion: InterpretiveConclusion,
    synthesis_packet: Optional[NarrativeSynthesisPacket],
) -> str:
    conclusion_text = _conclusion_text(conclusion)
    mechanisms, expressions, contexts = _narrative_evidence(
        conclusion, synthesis_packet
    )
    if mechanisms:
        mechanism_text = "。".join(
            _trim_sentence(value) for value in mechanisms
        )
    else:
        mechanism_text = "该结论仅由本主题已命中的受控传统象意信号支持"
    if expressions:
        expression_text = "；".join(
            _trim_sentence(value) for value in expressions
        )
    else:
        expression_text = "实际表现仍需由读者结合自身经验核对"
    context_text = _context_variation(
        conclusion, contexts, synthesis_packet
    )
    confidence = _CONFIDENCE_LABELS[conclusion.confidence]
    return (
        f"结论：{_trim_sentence(conclusion_text)}。"
        f"形成机制：{mechanism_text}。"
        f"常见表现：{expression_text}。"
        f"情境变化：{_trim_sentence(context_text)}。"
        f"这一结论的把握度：{confidence}。"
    )


def _trim_sentence(value: str) -> str:
    return value.rstrip("。； ")


def _conclusion_text(conclusion: InterpretiveConclusion) -> str:
    if _has_chinese(conclusion.interpretation):
        return conclusion.interpretation
    controlled = _unique(
        rendering.body
        for signal_id in _signal_ids((conclusion,))
        for rendering in (_SIGNAL_RENDERINGS.get(signal_id),)
        if rendering is not None
    )
    if controlled:
        return "".join(controlled)
    return (
        "现有受控信号仅支持将该主题作为反思线索，"
        "不补写未命中的具体特质。"
    )


def _narrative_evidence(
    conclusion: InterpretiveConclusion,
    synthesis_packet: Optional[NarrativeSynthesisPacket],
) -> tuple[Tuple[str, ...], Tuple[str, ...], Tuple[str, ...]]:
    if synthesis_packet is None:
        return (), (), ()
    signal_ids = set(conclusion.supporting_signal_ids)
    topics = (
        synthesis_packet.bazi_profile.topics
        + synthesis_packet.astrology_profile.topics
    )
    matched_topics = tuple(
        topic
        for topic in topics
        if topic.topic == conclusion.topic
        and signal_ids.intersection(topic.signal_ids)
    )
    return (
        _unique(
            provenance.mechanism
            for topic in matched_topics
            for provenance in topic.signal_provenance
            if provenance.signal_id in signal_ids
            and _has_chinese(provenance.mechanism)
        ),
        _unique(
            provenance.likely_expression
            for topic in matched_topics
            for provenance in topic.signal_provenance
            if provenance.signal_id in signal_ids
            and _has_chinese(provenance.likely_expression)
        ),
        _unique(
            context
            for topic in matched_topics
            for provenance in topic.signal_provenance
            if provenance.signal_id in signal_ids
            for context in provenance.contexts
            if _has_chinese(context)
        ),
    )


def _context_variation(
    conclusion: InterpretiveConclusion,
    contexts: Tuple[str, ...],
    synthesis_packet: Optional[NarrativeSynthesisPacket],
) -> str:
    if synthesis_packet is not None:
        signal_ids = set(_signal_ids((conclusion,)))
        tension = next(
            (
                item
                for item in synthesis_packet.tensions
                if item.topic == conclusion.topic
                and signal_ids.intersection(
                    item.bazi_signal_ids + item.astrology_signal_ids
                )
            ),
            None,
        )
        if tension is not None:
            return tension.integration
    if contexts:
        return (
            f"可优先在{'、'.join(contexts)}中观察，"
            "不同场景下的具体程度仍需结合对应信号理解"
        )
    return "当前档案未进一步区分具体情境，因而不作额外推断"


def _controlled_limitations(
    conclusions: Tuple[InterpretiveConclusion, ...],
    profile_limitations: Tuple[str, ...],
) -> Tuple[str, ...]:
    controlled = _unique(
        rendering.limitation
        for conclusion in conclusions
        for signal_id in _signal_ids((conclusion,))
        for rendering in (_SIGNAL_RENDERINGS.get(signal_id),)
        if rendering is not None
    )
    source_limitations = tuple(
        limitation
        for conclusion in conclusions
        for limitation in conclusion.limitations
    ) + profile_limitations
    chinese_source_limitations = _unique(
        limitation
        for limitation in source_limitations
        if _has_chinese(limitation)
    )
    return (
        controlled
        + chinese_source_limitations
        + ("传统象意仅作为反思线索，不是实证性诊断。",)
    )


def _has_chinese(value: object) -> bool:
    return isinstance(value, str) and any(
        "\u4e00" <= char <= "\u9fff" for char in value
    )


def _signal_ids(
    conclusions: Sequence[InterpretiveConclusion],
) -> Tuple[str, ...]:
    return _unique(
        signal_id
        for conclusion in conclusions
        for signal_id in (
            conclusion.supporting_signal_ids
            + conclusion.countervailing_signal_ids
        )
    )


def _signal_provenance(
    conclusions: Sequence[InterpretiveConclusion],
) -> Tuple[InterpretiveSignalProvenance, ...]:
    by_id = {}
    for conclusion in conclusions:
        for provenance in conclusion.signal_provenance:
            by_id.setdefault(provenance.signal_id, provenance)
    return tuple(
        by_id[signal_id]
        for signal_id in _signal_ids(conclusions)
        if signal_id in by_id
    )


def _conclusion_provenance_is_complete(
    conclusion: InterpretiveConclusion,
) -> bool:
    expected_ids = _signal_ids((conclusion,))
    provenance = conclusion.signal_provenance
    return (
        tuple(item.signal_id for item in provenance) == expected_ids
        and all(
            item.system in {"bazi", "astrology"}
            and item.fact_refs
            and all(isinstance(ref, str) and ref for ref in item.fact_refs)
            and item.traditional_rule_ref
            for item in provenance
        )
    )


def _include_missing_time_notice(
    sections: Tuple[InterpretiveReportSection, ...],
) -> Tuple[InterpretiveReportSection, ...]:
    if not sections:
        return sections
    first = sections[0]
    notice = (
        "出生时间不可用或存疑；宫位与四轴主张已省略，"
        "本报告仅使用不依赖精确出生时间的受控信号。"
    )
    limitation = "不推断宫位、上升点、天顶点或其他时间敏感结论。"
    return (
        replace(
            first,
            content=f"{first.content}{notice}",
            limitation=f"{first.limitation}；{limitation}",
        ),
        *sections[1:],
    )


def _audit_metadata(
    profile: InterpretiveCoreProfile,
    audit_refs: Tuple[str, ...],
) -> InterpretiveReportAuditMetadata:
    return InterpretiveReportAuditMetadata(
        rule_bundle_refs=tuple(
            ref for ref in audit_refs if ref.startswith("interpretive-rules:")
        ),
        fact_refs=tuple(
            ref for ref in audit_refs if ref.startswith("deterministic-facts:")
        ),
        qualification_refs=tuple(
            ref for ref in audit_refs if ref.startswith("fact-qualification:")
        ),
        profile_audit_refs=audit_refs,
        fact_mode=profile.fact_mode,
        birth_time_status=profile.birth_time_status,
        time_sensitivity_reasons=tuple(profile.time_sensitivity_reasons),
        omitted_time_sensitive_claims=tuple(
            profile.omitted_time_sensitive_claims
        ),
    )


def _unique(values: Iterable[str]) -> Tuple[str, ...]:
    return tuple(dict.fromkeys(values))
