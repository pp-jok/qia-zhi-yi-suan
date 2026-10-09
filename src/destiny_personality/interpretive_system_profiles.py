"""Independent Bazi and astrology profiles from matched audited signals."""

from collections import defaultdict
from typing import DefaultDict, Iterable, Tuple

from .deterministic_facts_codec import QualifiedFacts, require_qualified_facts
from .interpretive_models import (
    InterpretiveSignal,
    InterpretiveSignalProvenance,
    InterpretiveSystem,
    InterpretiveSystemProfile,
    InterpretiveSystemTopic,
)
from .interpretive_rules import BUNDLE_VERSION, extract_interpretive_signals


def build_interpretive_system_profiles(
    qualified_facts: QualifiedFacts,
) -> Tuple[InterpretiveSystemProfile, InterpretiveSystemProfile]:
    """Build two source-local profiles through the qualified-facts boundary."""

    qualified = require_qualified_facts(qualified_facts)
    signals = extract_interpretive_signals(qualified)
    audit_refs = (
        f"deterministic-facts:{qualified.fact_fingerprint}",
        f"fact-qualification:{qualified.qualification_fingerprint}",
        f"interpretive-rules:{BUNDLE_VERSION}",
    )
    return _build_interpretive_system_profiles(signals, audit_refs=audit_refs)


def _build_interpretive_system_profiles(
    signals: Tuple[InterpretiveSignal, ...],
    *,
    audit_refs: Tuple[str, ...] = (),
) -> Tuple[InterpretiveSystemProfile, InterpretiveSystemProfile]:
    return (
        _build_system_profile("bazi", signals, audit_refs),
        _build_system_profile("astrology", signals, audit_refs),
    )


def _build_system_profile(
    system: InterpretiveSystem,
    signals: Tuple[InterpretiveSignal, ...],
    audit_refs: Tuple[str, ...],
) -> InterpretiveSystemProfile:
    system_signals = tuple(
        sorted(
            (signal for signal in signals if signal.system == system),
            key=lambda signal: signal.signal_id,
        )
    )
    by_topic: DefaultDict[str, list[InterpretiveSignal]] = defaultdict(list)
    for signal in system_signals:
        by_topic[signal.topic].append(signal)

    topics = tuple(
        _build_topic(topic, tuple(by_topic[topic]))
        for topic in sorted(by_topic)
    )
    return InterpretiveSystemProfile(
        system=system,
        topics=topics,
        signal_ids=tuple(signal.signal_id for signal in system_signals),
        limitations=_unique(
            limitation
            for signal in system_signals
            for limitation in signal.limitations
        ),
        audit_refs=audit_refs,
    )


def _build_topic(
    topic: str,
    signals: Tuple[InterpretiveSignal, ...],
) -> InterpretiveSystemTopic:
    return InterpretiveSystemTopic(
        topic=topic,
        directions=_unique(signal.direction for signal in signals),
        signal_ids=tuple(signal.signal_id for signal in signals),
        interpretations=_unique(signal.interpretation for signal in signals),
        mechanisms=_unique(
            signal.mechanism for signal in signals if signal.mechanism
        ),
        likely_expressions=_unique(
            signal.likely_expression
            for signal in signals
            if signal.likely_expression
        ),
        contexts=_unique(
            context for signal in signals for context in signal.contexts
        ),
        limitations=_unique(
            limitation
            for signal in signals
            for limitation in signal.limitations
        ),
        signal_provenance=tuple(
            _signal_provenance(signal) for signal in signals
        ),
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
    )


def _unique(values: Iterable[str]) -> Tuple[str, ...]:
    return tuple(dict.fromkeys(values))
