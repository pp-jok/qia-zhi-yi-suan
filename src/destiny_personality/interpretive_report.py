"""Deterministic Chinese reports rendered from an interpretive profile only."""

from dataclasses import dataclass
from typing import Iterable, Literal, Optional, Sequence, Tuple

from .interpretive_models import InterpretiveConclusion, InterpretiveCoreProfile


InterpretiveReportMode = Literal["standard", "concise"]


@dataclass(frozen=True)
class InterpretiveReportSection:
    """A reader-facing section with an explicit evidence and limitation trail."""

    section_id: str
    title: str
    content: str
    signal_ids: Tuple[str, ...]
    limitation: str


@dataclass(frozen=True)
class InterpretiveReportAuditMetadata:
    """Profile-carried provenance grouped for product and audit consumers."""

    rule_bundle_refs: Tuple[str, ...]
    fact_refs: Tuple[str, ...]
    qualification_refs: Tuple[str, ...]
    profile_audit_refs: Tuple[str, ...]


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
    "relationships and boundaries": "关系与边界",
    "contextual dynamics": "关系与边界",
    "work and drive": "工作与驱动",
    "stress and energy": "压力与能量",
    "growth tension": "成长张力",
    "interacting tendencies": "成长张力",
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
    profile: InterpretiveCoreProfile,
    mode: InterpretiveReportMode,
) -> InterpretiveReport:
    """Render a stable product report without reopening chart facts."""

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
    audit_metadata = _audit_metadata(audit_refs)
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

    if mode == "standard":
        sections = _build_standard_sections(
            conclusions, tuple(profile.limitations)
        )
        title = "审计型传统命理解读·标准版"
    else:
        sections = _build_concise_sections(
            conclusions, tuple(profile.limitations)
        )
        title = "审计型传统命理解读·精简版"

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
        )
        for index, title in enumerate(ordered_titles[:12], start=1)
    ]
    if len(sections) < 8:
        sections.append(
            _coverage_section(
                section_id="standard-coverage",
                covered_count=len(sections),
                conclusions=conclusions,
            )
        )
    return tuple(sections)


def _build_concise_sections(
    conclusions: Tuple[InterpretiveConclusion, ...],
    profile_limitations: Tuple[str, ...],
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
        )
        for index, title in enumerate(_CONCISE_TOPIC_ORDER, start=1)
        if title in grouped
    ]
    if len(sections) < 4:
        sections.append(
            _coverage_section(
                section_id="concise-coverage",
                covered_count=len(sections),
                conclusions=conclusions,
            )
        )
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
) -> InterpretiveReportSection:
    statements = _render_bodies(conclusions)
    confidence_labels = _unique(
        _CONFIDENCE_LABELS[conclusion.confidence]
        for conclusion in conclusions
    )
    limitation_values = _controlled_limitations(
        conclusions, profile_limitations
    )
    return InterpretiveReportSection(
        section_id=section_id,
        title=title,
        content=(
            f"【{title}】{statements}"
            f"本节置信度：{'、'.join(confidence_labels)}。"
        ),
        signal_ids=_signal_ids(conclusions),
        limitation="；".join(limitation_values),
    )


def _coverage_section(
    *,
    section_id: str,
    covered_count: int,
    conclusions: Tuple[InterpretiveConclusion, ...],
) -> InterpretiveReportSection:
    return InterpretiveReportSection(
        section_id=section_id,
        title="证据覆盖说明",
        content=(
            f"当前审计档案仅支持上述 {covered_count} 个主题；"
            "未覆盖的主题不作推断或补写。"
        ),
        signal_ids=_signal_ids(conclusions),
        limitation="证据覆盖有限；不将现有结论重标为其他主题。",
    )


def _render_bodies(
    conclusions: Tuple[InterpretiveConclusion, ...],
) -> str:
    bodies = []
    for conclusion in conclusions:
        controlled = _unique(
            rendering.body
            for signal_id in _signal_ids((conclusion,))
            for rendering in (_SIGNAL_RENDERINGS.get(signal_id),)
            if rendering is not None
        )
        if controlled:
            bodies.extend(controlled)
        elif _has_chinese(conclusion.interpretation):
            bodies.append(conclusion.interpretation)
        else:
            bodies.append(
                "现有审计信号仅支持将该主题作为反思线索；"
                "当前未提供可直接呈现的受控中文规则文本。"
            )
    return "".join(_unique(bodies))


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


def _audit_metadata(
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
    )


def _unique(values: Iterable[str]) -> Tuple[str, ...]:
    return tuple(dict.fromkeys(values))
