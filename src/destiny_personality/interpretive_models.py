"""Immutable public models for audited traditional interpretations."""

from dataclasses import dataclass
from typing import Literal, Optional, Tuple


InterpretiveConfidence = Literal["high", "moderate", "exploratory", "insufficient"]


@dataclass(frozen=True)
class InterpretiveValuePredicate:
    """A supported value-level condition for an audited interpretive rule."""

    fact_ref: str
    values: Tuple[str, ...]
    body: Optional[str] = None
    other_body: Optional[str] = None


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


@dataclass(frozen=True)
class InterpretiveRuleBundle:
    """Versioned collection of non-diagnostic interpretive signals."""

    bundle_version: str
    rules: Tuple[InterpretiveSignal, ...]
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


@dataclass(frozen=True)
class InterpretiveCoreProfile:
    """Controlled synthesis of matched audited-interpretive signals."""

    mode: Literal["audited_interpretive"]
    conclusions: Tuple[InterpretiveConclusion, ...]
    limitations: Tuple[str, ...]
    audit_refs: Tuple[str, ...]
