"""Immutable public models for audited traditional interpretations."""

from dataclasses import dataclass
from typing import FrozenSet, Literal, Optional, Tuple


InterpretiveConfidence = Literal["high", "moderate", "exploratory", "insufficient"]
InterpretiveSystem = Literal["bazi", "astrology"]
InterpretiveRelationshipKind = Literal[
    "validation",
    "complement",
    "contextualization",
    "tension",
    "correction",
    "unresolved",
    "non_comparable",
]


@dataclass(frozen=True)
class InterpretiveValuePredicate:
    """A supported value-level condition for an audited interpretive rule."""

    fact_ref: str
    values: Tuple[str, ...]
    body: Optional[str] = None
    other_body: Optional[str] = None
    positions: Tuple[str, ...] = ()
    source_kinds: Tuple[str, ...] = ()
    participants: Tuple[str, ...] = ()
    minimum_occurrences: int = 1


@dataclass(frozen=True)
class InterpretiveMatchedValue:
    """One exact qualified value that caused a family predicate to match."""

    fact_ref: str
    fact_path: str
    value: str


@dataclass(frozen=True)
class InterpretiveSignal:
    """A traceable traditional interpretation grounded in chart facts."""

    signal_id: str
    system: str
    fact_refs: Tuple[str, ...]
    value_predicates: Tuple[InterpretiveValuePredicate, ...]
    traditional_rule_ref: str
    topic: str
    direction: str
    interpretation: str
    confidence: InterpretiveConfidence
    limitations: Tuple[str, ...]
    family: str = "legacy"
    mechanism: str = ""
    likely_expression: str = ""
    contexts: Tuple[str, ...] = ()
    modifiers: Tuple[str, ...] = ()
    requires_exact_demo_chart: bool = False
    matched_values: Tuple[InterpretiveMatchedValue, ...] = ()


@dataclass(frozen=True)
class InterpretiveRuleBundle:
    """Versioned collection of non-diagnostic interpretive signals."""

    bundle_version: str
    rules: Tuple[InterpretiveSignal, ...]
    limitations: Tuple[str, ...]
    covered_ten_gods: FrozenSet[str] = frozenset()
    covered_planets: FrozenSet[str] = frozenset()


@dataclass(frozen=True)
class InterpretiveSignalProvenance:
    """Concrete qualified-fact and rule provenance for one matched signal."""

    signal_id: str
    system: str
    fact_refs: Tuple[str, ...]
    traditional_rule_ref: str
    limitations: Tuple[str, ...]


@dataclass(frozen=True)
class InterpretiveConclusion:
    """A topic-bound conclusion that keeps its supporting and opposing signals."""

    topic: str
    direction: str
    interpretation: str
    supporting_signal_ids: Tuple[str, ...]
    countervailing_signal_ids: Tuple[str, ...]
    confidence: InterpretiveConfidence
    limitations: Tuple[str, ...]
    signal_provenance: Tuple[InterpretiveSignalProvenance, ...] = ()


@dataclass(frozen=True)
class InterpretiveSystemTopic:
    """One system's independently derived evidence for an exact topic."""

    topic: str
    directions: Tuple[str, ...]
    signal_ids: Tuple[str, ...]
    interpretations: Tuple[str, ...]
    mechanisms: Tuple[str, ...]
    likely_expressions: Tuple[str, ...]
    contexts: Tuple[str, ...]
    limitations: Tuple[str, ...]
    signal_provenance: Tuple[InterpretiveSignalProvenance, ...]


@dataclass(frozen=True)
class InterpretiveSystemProfile:
    """Topic-bound matched signals from one interpretive system only."""

    system: InterpretiveSystem
    topics: Tuple[InterpretiveSystemTopic, ...]
    signal_ids: Tuple[str, ...]
    limitations: Tuple[str, ...]
    audit_refs: Tuple[str, ...] = ()


@dataclass(frozen=True)
class InterpretiveSynthesisRelationship:
    """A bounded comparison that never substitutes for its source signals."""

    topic: str
    kind: InterpretiveRelationshipKind
    bazi_signal_ids: Tuple[str, ...]
    astrology_signal_ids: Tuple[str, ...]
    interpretation: str
    confidence: InterpretiveConfidence
    limitations: Tuple[str, ...]
    signal_provenance: Tuple[InterpretiveSignalProvenance, ...]


@dataclass(frozen=True)
class InterpretiveTension:
    """A concrete cross-system tension with two poles and bounded integration."""

    topic: str
    left_pole: str
    right_pole: str
    contexts: Tuple[str, ...]
    integration: str
    bazi_signal_ids: Tuple[str, ...]
    astrology_signal_ids: Tuple[str, ...]
    limitations: Tuple[str, ...]
    signal_provenance: Tuple[InterpretiveSignalProvenance, ...]


@dataclass(frozen=True)
class NarrativeSynthesisPacket:
    """Independent system profiles plus their auditable bounded comparisons."""

    bazi_profile: InterpretiveSystemProfile
    astrology_profile: InterpretiveSystemProfile
    alignments: Tuple[InterpretiveSynthesisRelationship, ...]
    tensions: Tuple[InterpretiveTension, ...]
    limitations: Tuple[str, ...]
    audit_refs: Tuple[str, ...]


@dataclass(frozen=True)
class InterpretiveCoreProfile:
    """Controlled synthesis of matched audited-interpretive signals."""

    mode: Literal["audited_interpretive"]
    conclusions: Tuple[InterpretiveConclusion, ...]
    limitations: Tuple[str, ...]
    audit_refs: Tuple[str, ...]
    fact_mode: str = "time_sensitive"
    birth_time_status: str = "available"
    time_sensitivity_reasons: Tuple[str, ...] = ()
    omitted_time_sensitive_claims: Tuple[str, ...] = ()
    synthesis_packet: Optional[NarrativeSynthesisPacket] = None
