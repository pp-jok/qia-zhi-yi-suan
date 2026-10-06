"""Deterministic Chinese reports rendered from an interpretive profile only."""

from dataclasses import dataclass
from typing import Iterable, Literal, Sequence, Tuple

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
class _TopicSpec:
    title: str
    keywords: Tuple[str, ...]


_STANDARD_TOPICS = (
    _TopicSpec("核心底色", ("baseline", "disposition", "temperament", "核心", "底色")),
    _TopicSpec("思考与学习", ("thinking", "learning", "cognition", "思考", "学习")),
    _TopicSpec("表达与创造", ("expression", "creation", "creative", "表达", "创造")),
    _TopicSpec("关系与边界", ("relationship", "boundary", "relating", "关系", "边界")),
    _TopicSpec("工作与驱动", ("work", "drive", "career", "motivation", "工作", "驱动")),
    _TopicSpec("压力与能量", ("stress", "energy", "pressure", "压力", "能量")),
    _TopicSpec("成长张力", ("growth", "tension", "development", "成长", "张力")),
    _TopicSpec("综合观察", ("synthesis", "integrated", "overview", "综合", "整体")),
)

_CONCISE_TOPICS = (
    ("核心轮廓", (0, 7)),
    ("思考与表达", (1, 2)),
    ("关系与行动", (3, 4)),
    ("压力与成长", (5, 6)),
)

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

    conclusions = tuple(
        conclusion
        for conclusion in profile.conclusions
        if _signal_ids((conclusion,))
    )
    if not conclusions:
        raise ValueError("TRACEABLE_INTERPRETIVE_CONCLUSION_REQUIRED")

    if mode == "standard":
        sections = _build_standard_sections(conclusions, profile.limitations)
        title = "审计型传统命理解读·标准版"
    else:
        sections = _build_concise_sections(conclusions, profile.limitations)
        title = "审计型传统命理解读·精简版"

    return InterpretiveReport(
        schema_version="interpretive-report-v1",
        mode=mode,
        title=title,
        sections=sections,
        boundary_statement=_BOUNDARY_STATEMENT,
        audit_metadata=_audit_metadata(profile.audit_refs),
    )


def _build_standard_sections(
    conclusions: Tuple[InterpretiveConclusion, ...],
    profile_limitations: Tuple[str, ...],
) -> Tuple[InterpretiveReportSection, ...]:
    matched_indexes = set()
    sections = []
    for index, spec in enumerate(_STANDARD_TOPICS, start=1):
        matches = _matches(conclusions, spec.keywords)
        if matches:
            matched_indexes.update(
                conclusion_index
                for conclusion_index, conclusion in enumerate(conclusions)
                if conclusion in matches
            )
        else:
            # Sparse audited profiles still receive the complete product frame;
            # the section text states exactly which available conclusion it uses.
            matches = (conclusions[(index - 1) % len(conclusions)],)
        sections.append(
            _section(
                section_id=f"standard-{index:02d}",
                title=spec.title,
                conclusions=matches,
                profile_limitations=profile_limitations,
            )
        )

    extras = tuple(
        conclusion
        for conclusion_index, conclusion in enumerate(conclusions)
        if conclusion_index not in matched_indexes
    )[:4]
    for offset, conclusion in enumerate(extras, start=1):
        sections.append(
            _section(
                section_id=f"standard-extra-{offset:02d}",
                title=f"补充观察：{conclusion.topic}",
                conclusions=(conclusion,),
                profile_limitations=profile_limitations,
            )
        )
    return tuple(sections)


def _build_concise_sections(
    conclusions: Tuple[InterpretiveConclusion, ...],
    profile_limitations: Tuple[str, ...],
) -> Tuple[InterpretiveReportSection, ...]:
    sections = []
    for index, (title, topic_indexes) in enumerate(_CONCISE_TOPICS, start=1):
        keywords = tuple(
            keyword
            for topic_index in topic_indexes
            for keyword in _STANDARD_TOPICS[topic_index].keywords
        )
        matches = _matches(conclusions, keywords)
        if not matches:
            matches = (conclusions[(index - 1) % len(conclusions)],)
        sections.append(
            _section(
                section_id=f"concise-{index:02d}",
                title=title,
                conclusions=matches,
                profile_limitations=profile_limitations,
            )
        )
    return tuple(sections)


def _matches(
    conclusions: Tuple[InterpretiveConclusion, ...],
    keywords: Sequence[str],
) -> Tuple[InterpretiveConclusion, ...]:
    return tuple(
        conclusion
        for conclusion in conclusions
        if any(keyword in conclusion.topic.casefold() for keyword in keywords)
    )


def _section(
    *,
    section_id: str,
    title: str,
    conclusions: Tuple[InterpretiveConclusion, ...],
    profile_limitations: Tuple[str, ...],
) -> InterpretiveReportSection:
    statements = " ".join(
        (
            f"档案结论「{conclusion.topic}」"
            f"（方向：{conclusion.direction}；"
            f"置信度：{_CONFIDENCE_LABELS[conclusion.confidence]}）："
            f"{conclusion.interpretation}"
        )
        for conclusion in conclusions
    )
    limitation_values = _unique(
        limitation
        for conclusion in conclusions
        for limitation in conclusion.limitations
    ) + _unique(profile_limitations)
    limitation = "；".join(limitation_values) or "仅作为反思线索。"
    return InterpretiveReportSection(
        section_id=section_id,
        title=title,
        content=f"【{title}】{statements}",
        signal_ids=_signal_ids(conclusions),
        limitation=limitation,
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
