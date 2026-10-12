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
    dynamics = _dynamics(alignments)
    shadow_mature = _shadow_mature(signatures)
    themes = _themes(signatures)
    archetype = _archetype(signatures)
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
        if alignment.kind in {"validation", "tension", "unresolved"}:
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
                )
            )
    if not items:
        for candidate in bazi_candidates + astrology_candidates:
            items.append(
                AuditedProfileItem(
                    item_id="signature:" + candidate.candidate_id,
                    topic=candidate.topic,
                    title="核心倾向：" + candidate.topic,
                    statement="该主题目前由{}体系的已限定信号支持：{}".format(
                        "八字" if candidate.system == "bazi" else "占星",
                        " ".join(candidate.interpretations),
                    ),
                    signal_ids=candidate.signal_ids,
                    rule_refs=candidate.rule_refs,
                    fact_refs=candidate.fact_refs,
                    limitations=candidate.limitations,
                    salience=1,
                )
            )
    return tuple(sorted(items, key=lambda item: (-item.salience, item.topic, item.item_id)))


def _dynamics(
    alignments: Tuple[AuditedCrossSystemAlignment, ...],
) -> Tuple[AuditedProfileItem, ...]:
    return tuple(
        AuditedProfileItem(
            item_id="dynamic:" + alignment.topic,
            topic=alignment.topic,
            title=("张力与调节：" if alignment.kind == "tension" else "双重线索：") + alignment.topic,
            statement=alignment.interpretation,
            signal_ids=alignment.signal_ids,
            rule_refs=alignment.rule_refs,
            fact_refs=alignment.fact_refs,
            limitations=alignment.limitations,
            salience=2 if alignment.kind == "tension" else 1,
            kind=alignment.kind,
        )
        for alignment in alignments
        if alignment.kind in {"tension", "validation", "unresolved"}
    )


def _shadow_mature(signatures: Tuple[AuditedProfileItem, ...]) -> Tuple[AuditedProfileItem, ...]:
    return tuple(
        AuditedProfileItem(
            item_id="shadow-mature:" + signature.topic,
            topic=signature.topic,
            title="影子与成熟表达：" + signature.topic,
            statement=(
                "若把这一倾向单独放大，容易忽略与它并存的条件；"
                "较成熟的用法，是把它放回具体情境，与其他已命中线索一并观察。"
            ),
            signal_ids=signature.signal_ids,
            rule_refs=signature.rule_refs,
            fact_refs=signature.fact_refs,
            limitations=signature.limitations + ("这是反思性表达，不是行为预测。",),
            salience=signature.salience,
        )
        for signature in signatures[:3]
    )


def _themes(signatures: Tuple[AuditedProfileItem, ...]) -> Tuple[AuditedProfileItem, ...]:
    return tuple(
        AuditedProfileItem(
            item_id="theme:" + signature.topic,
            topic=signature.topic,
            title="生命主题：" + signature.topic,
            statement="这一主题在当前画像中具有较高的证据密度：" + signature.statement,
            signal_ids=signature.signal_ids,
            rule_refs=signature.rule_refs,
            fact_refs=signature.fact_refs,
            limitations=signature.limitations,
            salience=signature.salience,
        )
        for signature in signatures[:4]
    )


def _archetype(signatures: Tuple[AuditedProfileItem, ...]) -> Optional[AuditedProfileItem]:
    if not signatures:
        return None
    primary = signatures[0]
    companion = signatures[1].topic if len(signatures) > 1 else None
    topics = primary.topic if companion is None else primary.topic + "与" + companion
    return AuditedProfileItem(
        item_id="archetype:profile",
        topic=primary.topic,
        title="画像原型",
        statement="可将当前画像暂称为“围绕{}展开的整合者”；这只是对已命中主题的阅读索引。".format(topics),
        signal_ids=primary.signal_ids + (() if companion is None else signatures[1].signal_ids),
        rule_refs=primary.rule_refs + (() if companion is None else signatures[1].rule_refs),
        fact_refs=primary.fact_refs + (() if companion is None else signatures[1].fact_refs),
        limitations=primary.limitations + ("原型不是分类诊断，也不取代个体自我理解。",),
        salience=primary.salience,
    )


def _unique(values: Iterable[str]) -> Tuple[str, ...]:
    return tuple(dict.fromkeys(value for value in values if value))
