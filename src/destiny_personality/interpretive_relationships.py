"""Versioned, fact-bound relationship rules for audited interpretive signals."""

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional, Tuple

import yaml

from .interpretive_models import InterpretiveSignal


RELATIONSHIP_FILE = "interpretive_relationships_v1.yaml"
RELATIONSHIP_BUNDLE_VERSION = "audited-interpretive-relationships-v1"
_RULE_KEYS = {
    "relationship_rule_id",
    "source_signal_conditions",
    "relationship_type",
    "pole_a",
    "pole_b",
    "activation_contexts",
    "interaction_mechanism",
    "pressure_hypothesis",
    "integration_hypothesis",
    "counter_conditions",
    "limitations",
    "traditional_rule_ref",
}
_CONDITION_KEYS = {"signal_id", "direction"}
_RELATIONSHIP_TYPES = {
    "reinforcement",
    "contextual_sequence",
    "contextual_switch",
    "tension",
    "compensation",
}


@dataclass(frozen=True)
class RelationshipSignalCondition:
    signal_id: str
    direction: str


@dataclass(frozen=True)
class InterpretiveRelationshipRule:
    relationship_rule_id: str
    source_signal_conditions: Tuple[RelationshipSignalCondition, ...]
    relationship_type: str
    pole_a: str
    pole_b: str
    activation_contexts: Tuple[str, ...]
    interaction_mechanism: str
    pressure_hypothesis: str
    integration_hypothesis: str
    counter_conditions: Tuple[str, ...]
    limitations: Tuple[str, ...]
    traditional_rule_ref: str


@dataclass(frozen=True)
class InterpretiveRelationshipBundle:
    bundle_version: str
    rules: Tuple[InterpretiveRelationshipRule, ...]


@dataclass(frozen=True)
class MatchedInterpretiveRelationship:
    relationship_rule_id: str
    relationship_type: str
    pole_a: str
    pole_b: str
    activation_contexts: Tuple[str, ...]
    interaction_mechanism: str
    pressure_hypothesis: str
    integration_hypothesis: str
    counter_conditions: Tuple[str, ...]
    limitations: Tuple[str, ...]
    traditional_rule_ref: str
    signal_ids: Tuple[str, ...]
    rule_refs: Tuple[str, ...]
    fact_refs: Tuple[str, ...]


def interpretive_relationship_asset_root() -> Path:
    return Path(__file__).resolve().parent / "interpretive_assets" / "v1"


def load_interpretive_relationship_bundle(
    directory: Optional[Path] = None,
) -> InterpretiveRelationshipBundle:
    """Load a closed, versioned relationship contract."""

    root = Path(directory) if directory is not None else interpretive_relationship_asset_root()
    path = root if root.suffix == ".yaml" else root / RELATIONSHIP_FILE
    try:
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as error:
        raise ValueError("INTERPRETIVE_RELATIONSHIP_INVALID") from error
    if not isinstance(payload, dict) or set(payload) != {"bundle_version", "rules"}:
        raise ValueError("INTERPRETIVE_RELATIONSHIP_INVALID")
    if payload["bundle_version"] != RELATIONSHIP_BUNDLE_VERSION:
        raise ValueError("INTERPRETIVE_RELATIONSHIP_INVALID_VERSION")
    raw_rules = payload["rules"]
    if not isinstance(raw_rules, list) or not raw_rules:
        raise ValueError("INTERPRETIVE_RELATIONSHIP_INVALID")
    rules = tuple(_rule(item) for item in raw_rules)
    if len({rule.relationship_rule_id for rule in rules}) != len(rules):
        raise ValueError("INTERPRETIVE_RELATIONSHIP_INVALID")
    return InterpretiveRelationshipBundle(RELATIONSHIP_BUNDLE_VERSION, rules)


def match_interpretive_relationships(
    signals: Tuple[InterpretiveSignal, ...],
    bundle: Optional[InterpretiveRelationshipBundle] = None,
) -> Tuple[MatchedInterpretiveRelationship, ...]:
    """Match only fully satisfied, direction-specific relationship rules."""

    active_bundle = bundle if bundle is not None else load_interpretive_relationship_bundle()
    by_id = {signal.signal_id: signal for signal in signals}
    matches = []
    for rule in active_bundle.rules:
        selected = []
        for condition in rule.source_signal_conditions:
            signal = by_id.get(condition.signal_id)
            if signal is None or signal.direction != condition.direction:
                break
            selected.append(signal)
        else:
            matches.append(
                MatchedInterpretiveRelationship(
                    relationship_rule_id=rule.relationship_rule_id,
                    relationship_type=rule.relationship_type,
                    pole_a=rule.pole_a,
                    pole_b=rule.pole_b,
                    activation_contexts=rule.activation_contexts,
                    interaction_mechanism=rule.interaction_mechanism,
                    pressure_hypothesis=rule.pressure_hypothesis,
                    integration_hypothesis=rule.integration_hypothesis,
                    counter_conditions=rule.counter_conditions,
                    limitations=rule.limitations,
                    traditional_rule_ref=rule.traditional_rule_ref,
                    signal_ids=tuple(signal.signal_id for signal in selected),
                    rule_refs=_unique(
                        signal.traditional_rule_ref for signal in selected
                    ) + (rule.traditional_rule_ref,),
                    fact_refs=_unique(
                        fact_ref for signal in selected for fact_ref in signal.fact_refs
                    ),
                )
            )
    return tuple(matches)


def _rule(value: object) -> InterpretiveRelationshipRule:
    if not isinstance(value, dict) or set(value) != _RULE_KEYS:
        raise ValueError("INTERPRETIVE_RELATIONSHIP_INVALID")
    conditions = value["source_signal_conditions"]
    if not isinstance(conditions, list) or len(conditions) < 2:
        raise ValueError("INTERPRETIVE_RELATIONSHIP_INVALID")
    parsed_conditions = tuple(_condition(item) for item in conditions)
    if len({item.signal_id for item in parsed_conditions}) != len(parsed_conditions):
        raise ValueError("INTERPRETIVE_RELATIONSHIP_INVALID")
    relationship_type = _string(value["relationship_type"])
    if relationship_type not in _RELATIONSHIP_TYPES:
        raise ValueError("INTERPRETIVE_RELATIONSHIP_INVALID")
    return InterpretiveRelationshipRule(
        relationship_rule_id=_string(value["relationship_rule_id"]),
        source_signal_conditions=parsed_conditions,
        relationship_type=relationship_type,
        pole_a=_string(value["pole_a"]),
        pole_b=_string(value["pole_b"]),
        activation_contexts=_strings(value["activation_contexts"]),
        interaction_mechanism=_string(value["interaction_mechanism"]),
        pressure_hypothesis=_string(value["pressure_hypothesis"]),
        integration_hypothesis=_string(value["integration_hypothesis"]),
        counter_conditions=_strings(value["counter_conditions"]),
        limitations=_strings(value["limitations"]),
        traditional_rule_ref=_string(value["traditional_rule_ref"]),
    )


def _condition(value: object) -> RelationshipSignalCondition:
    if not isinstance(value, dict) or set(value) != _CONDITION_KEYS:
        raise ValueError("INTERPRETIVE_RELATIONSHIP_INVALID")
    return RelationshipSignalCondition(
        signal_id=_string(value["signal_id"]), direction=_string(value["direction"])
    )


def _string(value: object) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError("INTERPRETIVE_RELATIONSHIP_INVALID")
    return value


def _strings(value: object) -> Tuple[str, ...]:
    if not isinstance(value, list) or not value:
        raise ValueError("INTERPRETIVE_RELATIONSHIP_INVALID")
    return tuple(_string(item) for item in value)


def _unique(values: Iterable[str]) -> Tuple[str, ...]:
    return tuple(dict.fromkeys(value for value in values if value))
