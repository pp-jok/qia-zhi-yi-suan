"""Primitive-only, user-readable views over a Candidate Core Profile."""

from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple, Union

import yaml

from .candidate_assets import candidate_asset_root
from .core_profile_models import CandidateCoreProfile, CrossSystemAlignment, PrimitiveCandidate


@dataclass(frozen=True)
class TimeSensitivitySummary:
    available: Tuple[str, ...]
    unavailable: Tuple[str, ...]


@dataclass(frozen=True)
class ProfileSummaryItem:
    item_id: str
    primitive_id: str
    canonical_name: str
    state: str
    contexts: Tuple[str, ...]
    evidence_strength: str
    source_systems: Tuple[str, ...]
    limitations: Tuple[str, ...]


@dataclass(frozen=True)
class CandidateProfileSummary:
    schema_version: str
    profile_ref: str
    user_capability_level: str
    core_supported_primitives: Tuple[ProfileSummaryItem, ...]
    contextual_primitives: Tuple[ProfileSummaryItem, ...]
    mixed_primitives: Tuple[ProfileSummaryItem, ...]
    unknown_primitives: Tuple[ProfileSummaryItem, ...]
    cross_system_validations: Tuple[CrossSystemAlignment, ...]
    cross_system_contextualizations: Tuple[CrossSystemAlignment, ...]
    cross_system_unresolved: Tuple[CrossSystemAlignment, ...]
    evidence_limits: Tuple[str, ...]
    time_sensitivity: TimeSensitivitySummary
    next_available_analysis: Tuple[str, ...]

    @property
    def items(self) -> Tuple[ProfileSummaryItem, ...]:
        return self.core_supported_primitives + self.contextual_primitives + self.mixed_primitives + self.unknown_primitives


@dataclass(frozen=True)
class CorePortraitSection:
    section_id: str
    title: str
    body: str
    profile_refs: Tuple[str, ...]


@dataclass(frozen=True)
class CorePortrait:
    schema_version: str
    mode: str
    profile_ref: str
    sections: Tuple[CorePortraitSection, ...]
    limitations: Tuple[str, ...]


@dataclass(frozen=True)
class ProfileItemExplanation:
    item_id: str
    primitive_id: str
    state: str
    contexts: Tuple[str, ...]
    fact_refs: Tuple[str, ...]
    rule_refs: Tuple[str, ...]
    bazi_evidence: Tuple[PrimitiveCandidate, ...]
    astrology_evidence: Tuple[PrimitiveCandidate, ...]
    counterevidence_refs: Tuple[str, ...]
    limitations: Tuple[str, ...]


@dataclass(frozen=True)
class ChangedPrimitive:
    primitive_id: str
    before_state: str
    after_state: str
    before_contexts: Tuple[Tuple[str, str], ...]
    after_contexts: Tuple[Tuple[str, str], ...]


@dataclass(frozen=True)
class CandidateProfileVersionDiff:
    left_profile_id: str
    right_profile_id: str
    unchanged_primitive_ids: Tuple[str, ...]
    changed_primitives: Tuple[ChangedPrimitive, ...]
    mapping_version_changed: bool
    resolver_version_changed: bool


def build_candidate_profile_summary(profile: CandidateCoreProfile) -> CandidateProfileSummary:
    names = _primitive_names()
    items = tuple(_summary_item(profile, primitive_id, names[primitive_id]) for primitive_id in sorted(profile.primitive_states))
    return CandidateProfileSummary(
        schema_version="candidate-profile-summary-v1",
        profile_ref=profile.candidate_profile_id,
        user_capability_level="core_portrait_preview",
        core_supported_primitives=tuple(item for item in items if item.state not in {"unknown", "mixed", "context_differentiated"}),
        contextual_primitives=tuple(item for item in items if item.state == "context_differentiated" or item.evidence_strength == "情境支持"),
        mixed_primitives=tuple(item for item in items if item.state == "mixed"),
        unknown_primitives=tuple(item for item in items if item.state == "unknown"),
        cross_system_validations=tuple(item for item in profile.cross_system_alignments if item.status == "validation"),
        cross_system_contextualizations=tuple(item for item in profile.cross_system_alignments if item.status == "contextualization"),
        cross_system_unresolved=tuple(item for item in profile.cross_system_alignments if item.status == "unresolved"),
        evidence_limits=profile.limitations,
        time_sensitivity=_time_sensitivity(profile),
        next_available_analysis=("可查看八字、占星或合参证据", "可补充准确出生时间以复核时间敏感部分"),
    )


def render_core_concise(summary: CandidateProfileSummary) -> CorePortrait:
    items = _display_items(summary, 4)
    sections = [
        _section("summary", "核心画像摘要", _item_sentence(item), item)
        for item in items
    ]
    sections.extend((_evidence_section(summary), _time_section(summary), _limits_section(summary)))
    return _portrait("core_concise", summary, tuple(sections[:8]))


def render_core_standard(summary: CandidateProfileSummary) -> CorePortrait:
    items = _display_items(summary, 8)
    sections = [
        _section(f"primitive-{index}", item.canonical_name, _item_sentence(item), item)
        for index, item in enumerate(items, 1)
    ]
    sections.extend((_evidence_section(summary), _comparison_section(summary), _time_section(summary), _limits_section(summary)))
    return _portrait("core_standard", summary, tuple(sections[:14]))


def explain_profile_item(profile: CandidateCoreProfile, item_id: str) -> ProfileItemExplanation:
    primitive_id = item_id.removeprefix("primitive:")
    if primitive_id not in profile.primitive_states:
        raise ValueError("PROFILE_ITEM_NOT_FOUND")
    state = profile.primitive_states[primitive_id]
    bazi = tuple(item for item in profile.bazi_primitive_candidates if item.primitive_id == primitive_id)
    astrology = tuple(item for item in profile.astrology_primitive_candidates if item.primitive_id == primitive_id)
    all_items = bazi + astrology
    return ProfileItemExplanation(
        item_id=f"primitive:{primitive_id}", primitive_id=primitive_id, state=state.state,
        contexts=tuple(sorted({context for item in all_items for context in item.contexts})),
        fact_refs=tuple(ref for item in all_items for ref in item.fact_refs),
        rule_refs=tuple(ref for item in all_items for ref in item.semantic_rule_refs),
        bazi_evidence=bazi, astrology_evidence=astrology,
        counterevidence_refs=tuple(ref for item in all_items for ref in item.counterevidence_refs),
        limitations=state.limitations,
    )


def source_view(profile: CandidateCoreProfile, view: str) -> Union[Tuple[PrimitiveCandidate, ...], Tuple[CrossSystemAlignment, ...]]:
    if view == "combined":
        return profile.bazi_primitive_candidates + profile.astrology_primitive_candidates
    if view == "bazi":
        return profile.bazi_primitive_candidates
    if view == "astrology":
        return profile.astrology_primitive_candidates
    if view == "comparison":
        return profile.cross_system_alignments
    raise ValueError("SOURCE_VIEW_INVALID")


def compare_candidate_profiles_versions(left: CandidateCoreProfile, right: CandidateCoreProfile) -> CandidateProfileVersionDiff:
    changed = []
    unchanged = []
    for primitive_id in sorted(set(left.primitive_states) | set(right.primitive_states)):
        before = left.primitive_states.get(primitive_id)
        after = right.primitive_states.get(primitive_id)
        if before == after:
            unchanged.append(primitive_id)
        else:
            changed.append(ChangedPrimitive(
                primitive_id, before.state if before else "absent", after.state if after else "absent",
                tuple(sorted(before.context_states.items())) if before else (),
                tuple(sorted(after.context_states.items())) if after else (),
            ))
    return CandidateProfileVersionDiff(
        left.candidate_profile_id, right.candidate_profile_id, tuple(unchanged), tuple(changed),
        _version(left, "bazi_mapping") != _version(right, "bazi_mapping") or _version(left, "astrology_mapping") != _version(right, "astrology_mapping"),
        _version(left, "state_resolver") != _version(right, "state_resolver"),
    )


def _summary_item(profile: CandidateCoreProfile, primitive_id: str, name: str) -> ProfileSummaryItem:
    state = profile.primitive_states[primitive_id]
    candidates = tuple(item for item in profile.bazi_primitive_candidates + profile.astrology_primitive_candidates if item.primitive_id == primitive_id)
    alignments = tuple(item for item in profile.cross_system_alignments if item.primitive_id == primitive_id)
    return ProfileSummaryItem(
        item_id=f"primitive:{primitive_id}", primitive_id=primitive_id, canonical_name=name, state=state.state,
        contexts=tuple(sorted({context for item in candidates for context in item.contexts})),
        evidence_strength=_strength(state.state, candidates, alignments),
        source_systems=tuple(sorted({item.source_system for item in candidates})), limitations=state.limitations,
    )


def _strength(state: str, candidates: Tuple[PrimitiveCandidate, ...], alignments: Tuple[CrossSystemAlignment, ...]) -> str:
    if state == "unknown": return "证据不足"
    if state == "mixed": return "证据混合"
    if any(item.status == "validation" for item in alignments) and len({item.source_system for item in candidates}) == 2: return "核心支持"
    if state == "context_differentiated": return "情境支持"
    if len({item.source_system for item in candidates}) == 1: return "单体系支持"
    return "明确支持"


def _primitive_names() -> dict[str, str]:
    payload = yaml.safe_load((candidate_asset_root() / "primitive_ontology_v1.yaml").read_text(encoding="utf-8"))
    return {item["primitive_id"]: item["canonical_name"] for item in payload["primitives"]}


def _time_sensitivity(profile: CandidateCoreProfile) -> TimeSensitivitySummary:
    unknown_time = any(item.evidence_stability == "stable" for item in profile.astrology_primitive_candidates)
    if unknown_time:
        return TimeSensitivitySummary(("稳定行星与相位证据",), ("Ascendant", "MC", "宫位", "角轴相关解释"))
    return TimeSensitivitySummary(("稳定行星与相位证据", "Ascendant", "MC", "宫位与角轴相关解释"), ())


def _display_items(summary: CandidateProfileSummary, maximum: int) -> Tuple[ProfileSummaryItem, ...]:
    priority = summary.core_supported_primitives + summary.contextual_primitives + summary.mixed_primitives
    return (priority or summary.unknown_primitives)[:maximum]


def _item_sentence(item: ProfileSummaryItem) -> str:
    contexts = "、".join(item.contexts) or "当前事实范围"
    return f"{item.canonical_name}：{item.evidence_strength}；状态为 {item.state}；适用情境为 {contexts}。"


def _section(section_id: str, title: str, body: str, item: ProfileSummaryItem) -> CorePortraitSection:
    return CorePortraitSection(section_id, title, body, (f"primitive_states.{item.primitive_id}",))


def _evidence_section(summary: CandidateProfileSummary) -> CorePortraitSection:
    return CorePortraitSection("evidence", "证据与合参", f"跨体系验证 {len(summary.cross_system_validations)} 项；情境化一致 {len(summary.cross_system_contextualizations)} 项。", ())


def _comparison_section(summary: CandidateProfileSummary) -> CorePortraitSection:
    return CorePortraitSection("comparison", "两套体系未统一之处", f"待保留的未解决对齐 {len(summary.cross_system_unresolved)} 项。", ())


def _time_section(summary: CandidateProfileSummary) -> CorePortraitSection:
    return CorePortraitSection("time", "出生时间影响", f"当前可用：{'、'.join(summary.time_sensitivity.available)}；暂不可用：{'、'.join(summary.time_sensitivity.unavailable) or '无'}。", ())


def _limits_section(summary: CandidateProfileSummary) -> CorePortraitSection:
    return CorePortraitSection("limits", "结论边界", "；".join(summary.evidence_limits), ())


def _portrait(mode: str, summary: CandidateProfileSummary, sections: Tuple[CorePortraitSection, ...]) -> CorePortrait:
    return CorePortrait("candidate-core-portrait-v1", mode, summary.profile_ref, sections, ("primitive_only", "candidate preview; not production authorization"))


def _version(profile: CandidateCoreProfile, key: str) -> Optional[str]:
    return dict(profile.semantic_model_versions).get(key)
