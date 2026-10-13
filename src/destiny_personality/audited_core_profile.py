"""Evidence-bounded product Core Destiny Profile for audited interpretations.

This module intentionally does not use candidate mappings, release mappings, or
the formal primitive ``CoreDestinyProfile``.  It turns already matched and
versioned interpretive signals into a separate reader-product IR.
"""

from dataclasses import dataclass
from hashlib import sha256
from typing import Iterable, Optional, Tuple

from .deterministic_facts_codec import QualifiedFacts, require_qualified_facts
from .interpretive_models import (
    InterpretiveSignalProvenance,
    InterpretiveSystemProfile,
    InterpretiveSystemTopic,
    NarrativeSynthesisPacket,
)
from .interpretive_synthesis import build_narrative_synthesis_packet
from .interpretive_rules import extract_interpretive_signals
from .interpretive_relationships import (
    MatchedInterpretiveRelationship,
    match_interpretive_relationships,
)


@dataclass(frozen=True)
class AuditedProfileCandidate:
    candidate_id: str
    system: str
    topic: str
    directions: Tuple[str, ...]
    interpretations: Tuple[str, ...]
    mechanisms: Tuple[str, ...]
    likely_expressions: Tuple[str, ...]
    contexts: Tuple[str, ...]
    signal_ids: Tuple[str, ...]
    rule_refs: Tuple[str, ...]
    fact_refs: Tuple[str, ...]
    limitations: Tuple[str, ...]


@dataclass(frozen=True)
class AuditedCrossSystemAlignment:
    alignment_id: str
    topic: str
    kind: str
    interpretation: str
    directions: Tuple[str, ...]
    signal_ids: Tuple[str, ...]
    rule_refs: Tuple[str, ...]
    fact_refs: Tuple[str, ...]
    limitations: Tuple[str, ...]


@dataclass(frozen=True)
class AuditedProfileItem:
    item_id: str
    topic: str
    title: str
    statement: str
    signal_ids: Tuple[str, ...]
    rule_refs: Tuple[str, ...]
    fact_refs: Tuple[str, ...]
    limitations: Tuple[str, ...]
    salience: int
    kind: str = ""
    source_item_ids: Tuple[str, ...] = ()
    relationship_type: str = ""
    activation_contexts: Tuple[str, ...] = ()
    interaction_mechanism: str = ""
    pressure_pattern: str = ""
    integration_pattern: str = ""
    counter_evidence: Tuple[str, ...] = ()
    derivation_level: str = "rule_matched"


@dataclass(frozen=True)
class AuditedCoreProfile:
    schema_version: str
    core_profile_id: str
    fact_fingerprint: str
    qualification_fingerprint: str
    fact_assurance: str
    semantic_model_assurance: str
    semantic_model_versions: Tuple[Tuple[str, str], ...]
    bazi_candidates: Tuple[AuditedProfileCandidate, ...]
    astrology_candidates: Tuple[AuditedProfileCandidate, ...]
    cross_system_alignments: Tuple[AuditedCrossSystemAlignment, ...]
    dominant_signatures: Tuple[AuditedProfileItem, ...]
    core_dynamics: Tuple[AuditedProfileItem, ...]
    shadow_mature_forms: Tuple[AuditedProfileItem, ...]
    fate_themes: Tuple[AuditedProfileItem, ...]
    archetype: Optional[AuditedProfileItem]
    limitations: Tuple[str, ...]
    audit_trail: Tuple[str, ...]


def build_audited_interpretive_core_profile(
    qualified_facts: QualifiedFacts,
) -> AuditedCoreProfile:
    """Build a product IR only from qualified facts and matched rule signals."""

    qualified = require_qualified_facts(qualified_facts)
    packet = build_narrative_synthesis_packet(qualified)
    bazi_candidates = _candidates(packet.bazi_profile)
    astrology_candidates = _candidates(packet.astrology_profile)
    if not bazi_candidates and not astrology_candidates:
        raise ValueError("TRACEABLE_INTERPRETIVE_SIGNAL_REQUIRED")
    alignments = _alignments(packet)
    signatures = _signatures(alignments, bazi_candidates, astrology_candidates)
    relationships = match_interpretive_relationships(extract_interpretive_signals(qualified))
    dynamics = _dynamics(relationships)
    shadow_mature = _shadow_mature(dynamics)
    themes = _themes(dynamics)
    archetype = _archetype(themes, dynamics)
    profile_seed = "|".join(
        (qualified.fact_fingerprint, qualified.qualification_fingerprint)
        + tuple(item.item_id for item in signatures)
    )
    return AuditedCoreProfile(
        schema_version="audited-interpretive-cdp-v1",
        core_profile_id="audited-cdp-" + sha256(profile_seed.encode("utf-8")).hexdigest()[:16],
        fact_fingerprint=qualified.fact_fingerprint,
        qualification_fingerprint=qualified.qualification_fingerprint,
        fact_assurance=qualified.fact_assurance,
        semantic_model_assurance="audited_interpretive_rule_derived",
        semantic_model_versions=(
            ("interpretive_rules", "interpretive-rules-v1"),
            ("interpretive_relationships", "audited-interpretive-relationships-v1"),
            ("cross_system_synthesis", "narrative-synthesis-v1"),
        ),
        bazi_candidates=bazi_candidates,
        astrology_candidates=astrology_candidates,
        cross_system_alignments=alignments,
        dominant_signatures=signatures,
        core_dynamics=dynamics,
        shadow_mature_forms=shadow_mature,
        fate_themes=themes,
        archetype=archetype,
        limitations=(
            "formal primitive coverage is not asserted",
            "candidate mapping assets are not read by this product profile",
            "traditional interpretive synthesis is reflective, non-diagnostic, and non-predictive",
        ) + packet.limitations,
        audit_trail=packet.audit_refs
        + (
            "profile_builder:audited-interpretive-cdp-v1",
            "profile_boundary:qualified-facts-and-matched-rules-only",
        ),
    )


def _candidates(profile: InterpretiveSystemProfile) -> Tuple[AuditedProfileCandidate, ...]:
    return tuple(
        _candidate(profile.system, topic)
        for topic in profile.topics
    )


def _candidate(system: str, topic: InterpretiveSystemTopic) -> AuditedProfileCandidate:
    provenance = topic.signal_provenance
    return AuditedProfileCandidate(
        candidate_id="{}:{}".format(system, topic.topic),
        system=system,
        topic=topic.topic,
        directions=topic.directions,
        interpretations=topic.interpretations,
        mechanisms=topic.mechanisms,
        likely_expressions=topic.likely_expressions,
        contexts=topic.contexts,
        signal_ids=topic.signal_ids,
        rule_refs=_unique(item.traditional_rule_ref for item in provenance),
        fact_refs=_unique(ref for item in provenance for ref in item.fact_refs),
        limitations=topic.limitations,
    )


def _alignments(packet: NarrativeSynthesisPacket) -> Tuple[AuditedCrossSystemAlignment, ...]:
    result = []
    for relationship in packet.alignments:
        provenance = relationship.signal_provenance
        result.append(
            AuditedCrossSystemAlignment(
                alignment_id="alignment:" + relationship.topic,
                topic=relationship.topic,
                kind=relationship.kind,
                interpretation=relationship.interpretation,
                directions=_unique(
                    direction
                    for source in (relationship.bazi_source, relationship.astrology_source)
                    if source is not None
                    for direction in source.directions
                ),
                signal_ids=relationship.bazi_signal_ids + relationship.astrology_signal_ids,
                rule_refs=_unique(item.traditional_rule_ref for item in provenance),
                fact_refs=_unique(ref for item in provenance for ref in item.fact_refs),
                limitations=relationship.limitations,
            )
        )
    return tuple(result)


def _signatures(
    alignments: Tuple[AuditedCrossSystemAlignment, ...],
    bazi_candidates: Tuple[AuditedProfileCandidate, ...],
    astrology_candidates: Tuple[AuditedProfileCandidate, ...],
) -> Tuple[AuditedProfileItem, ...]:
    items = []
    for alignment in alignments:
        if alignment.kind == "validation":
            items.append(
                AuditedProfileItem(
                    item_id="signature:" + alignment.topic,
                    topic=alignment.topic,
                    title="核心倾向：" + alignment.topic,
                    statement=alignment.interpretation,
                    signal_ids=alignment.signal_ids,
                    rule_refs=alignment.rule_refs,
                    fact_refs=alignment.fact_refs,
                    limitations=alignment.limitations,
                    salience={"validation": 3, "tension": 2, "unresolved": 1}[alignment.kind],
                    source_item_ids=(alignment.alignment_id,),
                    relationship_type="cross_system_validation",
                    derivation_level="controlled_synthesis",
                )
            )
    aligned_topics = {item.topic for item in items}
    for candidate in bazi_candidates + astrology_candidates:
        if (
            candidate.topic not in aligned_topics
            and len(candidate.signal_ids) >= 2
            and len(candidate.fact_refs) >= 2
        ):
            items.append(
                AuditedProfileItem(
                    item_id="signature:" + candidate.candidate_id,
                    topic=candidate.topic,
                    title="核心倾向：{}（{}）".format(
                        candidate.topic, " / ".join(candidate.directions)
                    ),
                    statement="该主题目前由{}体系的已限定信号支持：{}".format(
                        "八字" if candidate.system == "bazi" else "占星",
                        " ".join(candidate.interpretations),
                    ),
                    signal_ids=candidate.signal_ids,
                    rule_refs=candidate.rule_refs,
                    fact_refs=candidate.fact_refs,
                    limitations=candidate.limitations,
                    salience=2,
                    source_item_ids=(candidate.candidate_id,),
                    activation_contexts=candidate.contexts,
                    interaction_mechanism="；".join(candidate.mechanisms),
                    derivation_level="controlled_synthesis",
                )
            )
    return tuple(sorted(items, key=lambda item: (-item.salience, item.topic, item.item_id)))


def _dynamics(
    relationships: Tuple[MatchedInterpretiveRelationship, ...],
) -> Tuple[AuditedProfileItem, ...]:
    """Form Dynamics only from fully matched, versioned relationship rules."""
    items = []
    for relationship in relationships:
        items.append(AuditedProfileItem(
            item_id="dynamic:relationship:" + relationship.relationship_rule_id,
            topic="{} / {}".format(relationship.pole_a, relationship.pole_b),
            title="关键互动：{}与{}".format(relationship.pole_a, relationship.pole_b),
            statement=(
                "已命中的关系规则将“{}”与“{}”限定为{}；"
                "它不是由关键词或信号数量自动推得。"
            ).format(relationship.pole_a, relationship.pole_b, relationship.relationship_type),
            signal_ids=relationship.signal_ids,
            rule_refs=relationship.rule_refs,
            fact_refs=relationship.fact_refs,
            limitations=relationship.limitations + (
                "这是基于已匹配传统关系规则的反思线索，不是行为或事件预测。",
            ),
            salience=2,
            kind=relationship.relationship_type,
            source_item_ids=("relationship:" + relationship.relationship_rule_id,),
            relationship_type=relationship.relationship_type,
            activation_contexts=relationship.activation_contexts,
            interaction_mechanism=relationship.interaction_mechanism,
            pressure_pattern=relationship.pressure_hypothesis,
            integration_pattern=relationship.integration_hypothesis,
            counter_evidence=relationship.counter_conditions,
            derivation_level="relationship_rule_derived",
        ))
    return tuple(sorted(items, key=lambda item: (item.topic, item.item_id))[:7])


def _shadow_mature(dynamics: Tuple[AuditedProfileItem, ...]) -> Tuple[AuditedProfileItem, ...]:
    return tuple(
        AuditedProfileItem(
            item_id="shadow-mature:" + dynamic.item_id,
            topic=dynamic.topic,
            title="压力与成熟调节：" + dynamic.topic,
            statement=(
                "压力下，{}；成熟整合时，{}"
            ).format(dynamic.pressure_pattern, dynamic.integration_pattern),
            signal_ids=dynamic.signal_ids,
            rule_refs=dynamic.rule_refs,
            fact_refs=dynamic.fact_refs,
            limitations=dynamic.limitations + ("这是需要读者自行验证的反思性假设，不是行为预测。",),
            salience=dynamic.salience,
            kind="shadow_mature",
            source_item_ids=(dynamic.item_id,),
            relationship_type=dynamic.relationship_type,
            activation_contexts=dynamic.activation_contexts,
            interaction_mechanism=dynamic.interaction_mechanism,
            pressure_pattern=dynamic.pressure_pattern,
            integration_pattern=dynamic.integration_pattern,
            derivation_level="controlled_synthesis",
        )
        for dynamic in dynamics
    )


def _themes(dynamics: Tuple[AuditedProfileItem, ...]) -> Tuple[AuditedProfileItem, ...]:
    """A theme needs repeated relationship structure plus shared context."""
    by_context = {}
    for dynamic in dynamics:
        for context in dynamic.activation_contexts:
            by_context.setdefault((dynamic.relationship_type, context), []).append(dynamic)
    themes = []
    for (relationship_type, context), supporting in sorted(by_context.items()):
        if len(supporting) < 2:
            continue
        refs = tuple(item.item_id for item in supporting)
        themes.append(AuditedProfileItem(
            item_id="theme:{}:{}".format(relationship_type, context),
            topic=context,
            title="反复调节主题：" + context,
            statement="至少两条由{}关系规则形成的动态都涉及“{}”，因此它可作为需要持续观察的结构主题，而不是预言的人生事件。".format(relationship_type, context),
            signal_ids=_unique(signal for item in supporting for signal in item.signal_ids),
            rule_refs=_unique(rule for item in supporting for rule in item.rule_refs),
            fact_refs=_unique(ref for item in supporting for ref in item.fact_refs),
            limitations=("主题来自重复的关系结构与共同情境，不表示必然发生。",),
            salience=1,
            kind="recurring_pattern",
            source_item_ids=refs,
            activation_contexts=(context,),
            derivation_level="controlled_synthesis",
        ))
    return tuple(themes)


def _archetype(
    themes: Tuple[AuditedProfileItem, ...], dynamics: Tuple[AuditedProfileItem, ...]
) -> Optional[AuditedProfileItem]:
    if not themes or len(dynamics) < 2:
        return None
    theme = themes[0]
    return AuditedProfileItem(
        item_id="archetype:profile",
        topic=theme.topic,
        title="画像原型",
        statement="当前证据可暂时汇聚为“{}中的{}调节”：其主轴来自多条已匹配关系规则，而不是固定人格分类。".format(theme.topic, theme.relationship_type or "结构性"),
        signal_ids=_unique(signal for item in dynamics for signal in item.signal_ids),
        rule_refs=_unique(rule for item in dynamics for rule in item.rule_refs),
        fact_refs=_unique(ref for item in dynamics for ref in item.fact_refs),
        limitations=("原型只在多个动态和反复主题同时存在时生成，不是人格分类。",),
        salience=1,
        kind="archetype",
        source_item_ids=tuple(item.item_id for item in themes + dynamics),
        derivation_level="controlled_synthesis",
    )


def _unique(values: Iterable[str]) -> Tuple[str, ...]:
    return tuple(dict.fromkeys(value for value in values if value))
