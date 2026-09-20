from dataclasses import dataclass
from typing import Any, Tuple


@dataclass(frozen=True)
class PrimitiveDefinition:
    primitive_id: str
    canonical_name: str
    definition: str
    high_expression: str
    low_expression: str
    aliases: Tuple[str, ...]
    limitations: Tuple[str, ...]


@dataclass(frozen=True)
class PrimitiveOntologyConfig:
    schema_version: str
    ontology_version: str
    primitives: Tuple[PrimitiveDefinition, ...]


@dataclass(frozen=True)
class PrimitiveStateRule:
    rule_id: str
    target_state: str
    priority: int
    description: str
    requires_explicit_reverse_evidence: bool
    evidence_requirements: Tuple[Tuple[str, Any], ...]
    thresholds: Tuple[Tuple[str, Any], ...]
    limitations: Tuple[str, ...]


@dataclass(frozen=True)
class PrimitiveStateResolutionConfig:
    schema_version: str
    resolution_version: str
    ontology_version: str
    score_model_version: str
    states: Tuple[str, ...]
    invariants: Tuple[Tuple[str, Any], ...]
    rules: Tuple[PrimitiveStateRule, ...]


@dataclass(frozen=True)
class PrimitiveFoundationConfig:
    ontology: PrimitiveOntologyConfig
    resolution: PrimitiveStateResolutionConfig
