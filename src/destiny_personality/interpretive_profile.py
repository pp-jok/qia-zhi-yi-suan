"""Controlled synthesis for the audited interpretive product path."""

from collections import defaultdict
from typing import DefaultDict, Iterable, Optional, Sequence, Tuple

from .deterministic_facts_codec import QualifiedFacts, require_qualified_facts
from .interpretive_models import (
    InterpretiveConclusion,
    InterpretiveConfidence,
    InterpretiveCoreProfile,
    NarrativeSynthesisPacket,
    InterpretiveSignal,
    InterpretiveSignalProvenance,
)
from .interpretive_rules import BUNDLE_VERSION, extract_interpretive_signals
from .interpretive_synthesis import _build_narrative_synthesis_packet


ALLOWED_CONFIDENCES = frozenset(
    {"high", "moderate", "exploratory", "insufficient"}
)
_STABLE_SIGNAL_CONFIDENCES = frozenset({"high", "moderate"})


def build_interpretive_core_profile(
    qualified_facts: QualifiedFacts,
) -> InterpretiveCoreProfile:
    """Build a traceable profile from qualification-bound matched signals."""

    qualified = require_qualified_facts(qualified_facts)
    signals = extract_interpretive_signals(qualified)
    audit_refs = (
        f"deterministic-facts:{qualified.fact_fingerprint}",
        f"fact-qualification:{qualified.qualification_fingerprint}",
        f"interpretive-rules:{BUNDLE_VERSION}",
    )
    return _synthesize_interpretive_core_profile(
        signals,
        audit_refs=audit_refs,
        fact_mode=qualified.facts.normalized_time.fact_mode.value,
        time_sensitivity_reasons=tuple(
            qualified.facts.normalized_time.sensitivity_reasons
        ),
        synthesis_packet=_build_narrative_synthesis_packet(
            signals, audit_refs=audit_refs
        ),
    )


def _synthesize_interpretive_core_profile(
    signals: Tuple[InterpretiveSignal, ...],
    *,
    requested_topics: Sequence[str] = (),
    audit_refs: Tuple[str, ...] = (),
    fact_mode: str = "time_sensitive",
    time_sensitivity_reasons: Tuple[str, ...] = (),
    synthesis_packet: Optional[NarrativeSynthesisPacket] = None,
) -> InterpretiveCoreProfile:
    """Group exact topics and directions without converting evidence to scores."""

    by_topic: DefaultDict[str, list[InterpretiveSignal]] = defaultdict(list)
    for signal in signals:
        by_topic[signal.topic].append(signal)

    conclusions = []
    all_topics = set(by_topic).union(requested_topics)
    for topic in sorted(all_topics):
        topic_signals = by_topic.get(topic, [])
        if not topic_signals:
            conclusions.append(_insufficient_conclusion(topic))
            continue

        by_direction: DefaultDict[str, list[InterpretiveSignal]] = defaultdict(list)
        for signal in topic_signals:
            by_direction[signal.direction].append(signal)
        for direction in sorted(by_direction):
            supporting = tuple(
                sorted(by_direction[direction], key=lambda signal: signal.signal_id)
            )
            countervailing = tuple(
                sorted(
                    (
                        signal
                        for other_direction, direction_signals in by_direction.items()
                        if other_direction != direction
                        for signal in direction_signals
                    ),
                    key=lambda signal: signal.signal_id,
                )
            )
            conclusions.append(
                InterpretiveConclusion(
                    topic=topic,
                    direction=direction,
                    interpretation=" ".join(
                        _unique(signal.interpretation for signal in supporting)
                    ),
                    supporting_signal_ids=tuple(
                        signal.signal_id for signal in supporting
                    ),
                    countervailing_signal_ids=tuple(
                        signal.signal_id for signal in countervailing
                    ),
                    confidence=_confidence(supporting, countervailing),
                    limitations=_unique(
                        limitation
                        for signal in supporting + countervailing
                        for limitation in signal.limitations
                    ),
                    signal_provenance=tuple(
                        _signal_provenance(signal)
                        for signal in supporting + countervailing
                    ),
                )
            )

    birth_time_unavailable = fact_mode == "stable_only"

    return InterpretiveCoreProfile(
        mode="audited_interpretive",
        conclusions=tuple(conclusions),
        limitations=(
            "Traditional interpretive heuristics are not empirical personality diagnoses.",
            "Evidence is grouped by exact topic and direction without numeric scoring.",
        ),
        audit_refs=audit_refs,
        fact_mode=fact_mode,
        birth_time_status=(
            "unavailable_or_uncertain"
            if birth_time_unavailable
            else "available"
        ),
        time_sensitivity_reasons=time_sensitivity_reasons,
        omitted_time_sensitive_claims=(
            ("astrology.houses", "astrology.angles")
            if birth_time_unavailable
            else ()
        ),
        synthesis_packet=synthesis_packet,
    )


def _signal_provenance(
    signal: InterpretiveSignal,
) -> InterpretiveSignalProvenance:
    return InterpretiveSignalProvenance(
        signal_id=signal.signal_id,
        system=signal.system,
        fact_refs=signal.fact_refs,
        traditional_rule_ref=signal.traditional_rule_ref,
        limitations=signal.limitations,
        mechanism=signal.mechanism,
        likely_expression=signal.likely_expression,
        contexts=signal.contexts,
    )


def _confidence(
    supporting: Tuple[InterpretiveSignal, ...],
    countervailing: Tuple[InterpretiveSignal, ...],
) -> InterpretiveConfidence:
    if countervailing or any(
        signal.confidence not in _STABLE_SIGNAL_CONFIDENCES
        for signal in supporting
    ):
        return "exploratory"
    systems = {signal.system for signal in supporting}
    independent_rules = {signal.traditional_rule_ref for signal in supporting}
    if len(systems) > 1 or len(independent_rules) > 1:
        return "high"
    return "moderate"


def _insufficient_conclusion(topic: str) -> InterpretiveConclusion:
    return InterpretiveConclusion(
        topic=topic,
        direction="unresolved",
        interpretation="No matched interpretive rule is available for this requested topic.",
        supporting_signal_ids=(),
        countervailing_signal_ids=(),
        confidence="insufficient",
        limitations=("No matched rule supports a topic-level interpretation.",),
    )


def _unique(values: Iterable[str]) -> Tuple[str, ...]:
    return tuple(dict.fromkeys(values))
