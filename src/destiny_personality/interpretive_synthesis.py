"""Bounded cross-system synthesis for audited interpretive signals."""

from collections import defaultdict
from typing import DefaultDict, Iterable, Tuple

from .deterministic_facts_codec import QualifiedFacts, require_qualified_facts
from .interpretive_models import (
    InterpretiveConfidence,
    InterpretiveRelationshipKind,
    InterpretiveSignal,
    InterpretiveSynthesisRelationship,
    InterpretiveTension,
    NarrativeSynthesisPacket,
)
from .interpretive_rules import BUNDLE_VERSION, extract_interpretive_signals
from .interpretive_system_profiles import (
    _build_interpretive_system_profiles,
    _signal_provenance,
)


ALLOWED_RELATIONSHIP_KINDS = frozenset(
    {
        "validation",
        "complement",
        "contextualization",
        "tension",
        "correction",
        "unresolved",
        "non_comparable",
    }
)
_STABLE_CONFIDENCES = frozenset({"high", "moderate"})


def build_narrative_synthesis_packet(
    qualified_facts: QualifiedFacts,
) -> NarrativeSynthesisPacket:
    """Compare only signals extracted from qualification-bound facts."""

    qualified = require_qualified_facts(qualified_facts)
    signals = extract_interpretive_signals(qualified)
    audit_refs = (
        f"deterministic-facts:{qualified.fact_fingerprint}",
        f"fact-qualification:{qualified.qualification_fingerprint}",
        f"interpretive-rules:{BUNDLE_VERSION}",
    )
    return _build_narrative_synthesis_packet(signals, audit_refs=audit_refs)


def _build_narrative_synthesis_packet(
    signals: Tuple[InterpretiveSignal, ...],
    *,
    audit_refs: Tuple[str, ...] = (),
) -> NarrativeSynthesisPacket:
    bazi_profile, astrology_profile = _build_interpretive_system_profiles(
        signals, audit_refs=audit_refs
    )
    by_system_and_topic: DefaultDict[
        tuple[str, str], list[InterpretiveSignal]
    ] = defaultdict(list)
    for signal in signals:
        by_system_and_topic[(signal.system, signal.topic)].append(signal)

    topics = sorted(
        {topic.topic for topic in bazi_profile.topics}
        | {topic.topic for topic in astrology_profile.topics}
    )
    alignments = []
    tensions = []
    for topic in topics:
        bazi_signals = tuple(
            sorted(
                by_system_and_topic[("bazi", topic)],
                key=lambda signal: signal.signal_id,
            )
        )
        astrology_signals = tuple(
            sorted(
                by_system_and_topic[("astrology", topic)],
                key=lambda signal: signal.signal_id,
            )
        )
        relationship = _relationship(topic, bazi_signals, astrology_signals)
        alignments.append(relationship)
        if relationship.kind == "tension":
            tensions.append(_tension(topic, bazi_signals, astrology_signals))

    return NarrativeSynthesisPacket(
        bazi_profile=bazi_profile,
        astrology_profile=astrology_profile,
        alignments=tuple(alignments),
        tensions=tuple(tensions),
        limitations=(
            "Cross-system relationships compare exact matched topics only.",
            "Unmatched evidence remains non-comparable and never implies agreement.",
            "Traditional interpretive synthesis is non-diagnostic and non-predictive.",
        ),
        audit_refs=audit_refs,
    )


def _relationship(
    topic: str,
    bazi_signals: Tuple[InterpretiveSignal, ...],
    astrology_signals: Tuple[InterpretiveSignal, ...],
) -> InterpretiveSynthesisRelationship:
    all_signals = bazi_signals + astrology_signals
    if not bazi_signals or not astrology_signals:
        kind: InterpretiveRelationshipKind = "non_comparable"
        interpretation = (
            f"{topic} 主题只有一个体系命中信号；"
            "另一体系无同主题证据，因此不作一致或冲突判断。"
        )
        confidence: InterpretiveConfidence = "insufficient"
    else:
        bazi_directions = {signal.direction for signal in bazi_signals}
        astrology_directions = {
            signal.direction for signal in astrology_signals
        }
        if bazi_directions == astrology_directions:
            kind = "validation"
            interpretation = (
                f"两个体系在 {topic} 主题上分别命中了"
                "方向相同的独立信号。"
            )
            confidence = _validation_confidence(all_signals)
        elif bazi_directions.isdisjoint(astrology_directions):
            kind = "tension"
            interpretation = (
                f"两个体系在 {topic} 主题上命中了不同方向，"
                "保留为需按情境理解的张力，不互相抵消。"
            )
            confidence = "exploratory"
        else:
            kind = "unresolved"
            interpretation = (
                f"两个体系在 {topic} 主题上既有重叠也有分歧，"
                "当前信号不足以确定稳定关系。"
            )
            confidence = "exploratory"

    return InterpretiveSynthesisRelationship(
        topic=topic,
        kind=kind,
        bazi_signal_ids=tuple(signal.signal_id for signal in bazi_signals),
        astrology_signal_ids=tuple(
            signal.signal_id for signal in astrology_signals
        ),
        interpretation=interpretation,
        confidence=confidence,
        limitations=_unique(
            limitation
            for signal in all_signals
            for limitation in signal.limitations
        ),
        signal_provenance=tuple(
            _signal_provenance(signal) for signal in all_signals
        ),
    )


def _validation_confidence(
    signals: Tuple[InterpretiveSignal, ...],
) -> InterpretiveConfidence:
    if all(signal.confidence in _STABLE_CONFIDENCES for signal in signals):
        return "high"
    return "exploratory"


def _tension(
    topic: str,
    bazi_signals: Tuple[InterpretiveSignal, ...],
    astrology_signals: Tuple[InterpretiveSignal, ...],
) -> InterpretiveTension:
    all_signals = bazi_signals + astrology_signals
    contexts = _unique(
        context for signal in all_signals for context in signal.contexts
    )
    context_text = "、".join(contexts) if contexts else "具体情境"
    return InterpretiveTension(
        topic=topic,
        left_pole=_pole("八字侧", bazi_signals),
        right_pole=_pole("占星侧", astrology_signals),
        contexts=contexts,
        integration=(
            f"在{context_text}中分别观察两端何时更可见；"
            "把它们作为可并存的情境线索，不将一端解释为另一端的否定。"
        ),
        bazi_signal_ids=tuple(signal.signal_id for signal in bazi_signals),
        astrology_signal_ids=tuple(
            signal.signal_id for signal in astrology_signals
        ),
        limitations=_unique(
            limitation
            for signal in all_signals
            for limitation in signal.limitations
        ),
        signal_provenance=tuple(
            _signal_provenance(signal) for signal in all_signals
        ),
    )


def _pole(label: str, signals: Tuple[InterpretiveSignal, ...]) -> str:
    directions = "、".join(
        _unique(signal.direction for signal in signals)
    )
    interpretations = " ".join(
        _unique(signal.interpretation for signal in signals)
    )
    return f"{label}（{directions}）：{interpretations}"


def _unique(values: Iterable[str]) -> Tuple[str, ...]:
    return tuple(dict.fromkeys(values))
