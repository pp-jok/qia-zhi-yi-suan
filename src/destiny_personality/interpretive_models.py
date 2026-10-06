"""Immutable public models for audited traditional interpretations."""

from dataclasses import dataclass
from typing import Literal, Tuple


InterpretiveConfidence = Literal["high", "moderate", "exploratory", "insufficient"]


@dataclass(frozen=True)
class InterpretiveSignal:
    """A traceable traditional interpretation grounded in chart facts."""

    signal_id: str
    system: str
    fact_refs: Tuple[str, ...]
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
