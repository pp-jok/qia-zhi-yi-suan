"""Dynamic, contained report planning for ``audited-interpretive-cdp-v1``."""

from dataclasses import asdict, dataclass, replace
from hashlib import sha256
from typing import Dict, Iterable, Tuple

from .audited_core_profile import AuditedCoreProfile, AuditedProfileItem


@dataclass(frozen=True)
class AuditedProfilePlannedSection:
    section_id: str
    title: str
    item_ids: Tuple[str, ...]
    deduplication_key: str
    reason: str
    evidence_fingerprint: str


@dataclass(frozen=True)
class AuditedProfileReportPlan:
    schema_version: str
    core_profile_id: str
    profile_fingerprint: str
    sections: Tuple[AuditedProfilePlannedSection, ...]
    omitted_item_ids: Tuple[str, ...]
    audit_trail: Tuple[str, ...]


@dataclass(frozen=True)
class AuditedProfileReportSection:
    section_id: str
    title: str
    content: str
    item_ids: Tuple[str, ...]
    signal_ids: Tuple[str, ...]
    rule_refs: Tuple[str, ...]
    fact_refs: Tuple[str, ...]
    limitations: Tuple[str, ...]


@dataclass(frozen=True)
class AuditedProfileReport:
    schema_version: str
    mode: str
    title: str
    core_profile_id: str
    sections: Tuple[AuditedProfileReportSection, ...]
    boundary_statement: str
    limitations: Tuple[str, ...]
    audit_refs: Tuple[str, ...]


def build_audited_profile_report_plan(
    profile: AuditedCoreProfile,
) -> AuditedProfileReportPlan:
    """Select a bounded set of non-repetitive reader sections from the profile."""

    if not isinstance(profile, AuditedCoreProfile):
        raise TypeError("AUDITED_CORE_PROFILE_REQUIRED")
    items = _item_index(profile)
    sections = []
    observations = _candidate_observations(profile)
    core_items = profile.dominant_signatures[:2]
    if core_items and len(core_items) < 2:
        core_items = core_items + observations[:1]
    if not core_items:
        core_items = observations[:2]
    if core_items:
        title = "核心主轴" if profile.dominant_signatures else "当前可支持观察"
        sections.append(_section("core-profile", title, tuple(item.item_id for item in core_items), "core-profile", "evidence-ranked-core"))
    for dynamic in profile.core_dynamics[:2]:
        sections.append(_section("dynamic-" + dynamic.item_id, dynamic.title, (dynamic.item_id,), "dynamic:" + dynamic.item_id, "mechanism-bearing-dynamic"))
    for item in profile.shadow_mature_forms[:2]:
        sections.append(_section("shadow-mature-" + item.item_id, item.title, (item.item_id,), "shadow-mature:" + item.item_id, "dynamic-derived-regulation"))
    for item in profile.fate_themes[:2]:
        sections.append(_section("theme-" + item.item_id, item.title, (item.item_id,), "theme:" + item.item_id, "recurring-dynamic-pattern"))
    if profile.archetype is not None:
        sections.append(_section("archetype", profile.archetype.title, (profile.archetype.item_id,), "archetype", "profile-index"))
    sections = [
        replace(section, evidence_fingerprint=_section_evidence_fingerprint(section, items))
        for section in sections
    ]
    selected_ids = {item_id for section in sections for item_id in section.item_ids}
    omitted = tuple(item_id for item_id in sorted(items) if item_id not in selected_ids)
    if len({section.deduplication_key for section in sections}) != len(sections):
        raise ValueError("AUDITED_PROFILE_PLAN_DUPLICATE_SECTION")
    return AuditedProfileReportPlan(
        schema_version="audited-profile-report-plan-v1",
        core_profile_id=profile.core_profile_id,
        profile_fingerprint=_profile_fingerprint(profile),
        sections=tuple(sections),
        omitted_item_ids=omitted,
        audit_trail=profile.audit_trail + ("report_planner:audited-profile-report-plan-v1",),
    )


def render_audited_profile_report(
    profile: AuditedCoreProfile, plan: AuditedProfileReportPlan
) -> AuditedProfileReport:
    """Render only profile items selected by the exact deterministic plan."""

    if not isinstance(profile, AuditedCoreProfile) or not isinstance(plan, AuditedProfileReportPlan):
        raise TypeError("AUDITED_PROFILE_REPORT_CONTAINMENT_VIOLATION")
    if plan != build_audited_profile_report_plan(profile):
        raise ValueError("AUDITED_PROFILE_REPORT_CONTAINMENT_VIOLATION")
    items = _item_index(profile)
    sections = tuple(_render_section(section, items) for section in plan.sections)
    return AuditedProfileReport(
        schema_version="audited-profile-report-v1",
        mode="core-profile-v1",
        title="审计型命格人格画像",
        core_profile_id=profile.core_profile_id,
        sections=sections,
        boundary_statement=(
            "本报告基于传统命理与占星象意的已审计规则生成，"
            "用于反思，不是实证人格测量、医疗或心理诊断，也不应代替重大生活决策。"
        ),
        limitations=profile.limitations,
        audit_refs=plan.audit_trail,
    )


def _section(
    section_id: str, title: str, item_ids: Tuple[str, ...], deduplication_key: str, reason: str
) -> AuditedProfilePlannedSection:
    return AuditedProfilePlannedSection(section_id, title, item_ids, deduplication_key, reason, "")


def _item_index(profile: AuditedCoreProfile) -> Dict[str, AuditedProfileItem]:
    items = (
        _candidate_observations(profile)
        + profile.dominant_signatures
        + profile.core_dynamics
        + profile.shadow_mature_forms
        + profile.fate_themes
        + (() if profile.archetype is None else (profile.archetype,))
    )
    return {item.item_id: item for item in items}


def _candidate_observations(profile: AuditedCoreProfile) -> Tuple[AuditedProfileItem, ...]:
    observations = []
    for candidate in profile.bazi_candidates + profile.astrology_candidates:
        observations.append(AuditedProfileItem(
            item_id="observation:" + candidate.candidate_id,
            topic=candidate.topic,
            title="可支持观察：" + candidate.topic,
            statement="{}体系的已限定线索显示：{}".format("八字" if candidate.system == "bazi" else "占星", " ".join(candidate.interpretations)),
            signal_ids=candidate.signal_ids,
            rule_refs=candidate.rule_refs,
            fact_refs=candidate.fact_refs,
            limitations=candidate.limitations,
            salience=1,
            source_item_ids=(candidate.candidate_id,),
            activation_contexts=candidate.contexts,
            interaction_mechanism="；".join(candidate.mechanisms),
        ))
    return tuple(sorted(observations, key=lambda item: (item.topic, item.item_id)))


def _render_section(
    section: AuditedProfilePlannedSection, items: Dict[str, AuditedProfileItem]
) -> AuditedProfileReportSection:
    selected = tuple(items[item_id] for item_id in section.item_ids)
    return AuditedProfileReportSection(
        section_id=section.section_id,
        title=section.title,
        content="\n\n".join(_narrative(item) for item in selected),
        item_ids=section.item_ids,
        signal_ids=_unique(signal_id for item in selected for signal_id in item.signal_ids),
        rule_refs=_unique(rule_ref for item in selected for rule_ref in item.rule_refs),
        fact_refs=_unique(fact_ref for item in selected for fact_ref in item.fact_refs),
        limitations=_unique(limitation for item in selected for limitation in item.limitations),
    )


def _narrative(item: AuditedProfileItem) -> str:
    parts = [item.statement]
    if item.kind == "shadow_mature":
        parts.append("这是一条由前述内在节奏导出的待验证反思，不是对实际行为的断言。")
        return "\n".join(parts)
    if item.interaction_mechanism:
        parts.append("形成机制：" + item.interaction_mechanism.replace("。；", "；"))
    if item.activation_contexts:
        parts.append("较适合观察的情境：" + "、".join(item.activation_contexts))
    if item.pressure_pattern:
        parts.append("压力下的可能失衡：" + item.pressure_pattern)
    if item.integration_pattern:
        parts.append("整合方向：" + item.integration_pattern)
    return "\n".join(parts)


def _section_evidence_fingerprint(
    section: AuditedProfilePlannedSection, items: Dict[str, AuditedProfileItem]
) -> str:
    evidence = tuple(
        (
            item.item_id,
            item.statement,
            item.signal_ids,
            item.rule_refs,
            item.fact_refs,
        )
        for item in (items[item_id] for item_id in section.item_ids)
    )
    return sha256(repr(evidence).encode("utf-8")).hexdigest()


def _profile_fingerprint(profile: AuditedCoreProfile) -> str:
    return sha256(repr(asdict(profile)).encode("utf-8")).hexdigest()


def _unique(values: Iterable[str]) -> Tuple[str, ...]:
    return tuple(dict.fromkeys(value for value in values if value))
