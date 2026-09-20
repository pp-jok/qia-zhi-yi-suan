from dataclasses import dataclass
from typing import Any, Tuple


@dataclass(frozen=True)
class MappingOutput:
    primitive_id: str
    direction: str
    salience: int
    limitations: Tuple[str, ...]


@dataclass(frozen=True)
class MappingModifier:
    when: Any
    effects: Tuple[Any, ...]


@dataclass(frozen=True)
class MappingRule:
    rule_id: str
    priority: int
    primary_condition: Any
    context: Any
    outputs: Tuple[MappingOutput, ...]
    modifiers: Tuple[MappingModifier, ...]
    limitations: Tuple[str, ...]


@dataclass(frozen=True)
class MappingInteraction:
    interaction_id: str
    requires: Tuple[str, ...]
    produces: Any
    limitations: Tuple[str, ...]


@dataclass(frozen=True)
class ContextAwareMappingRegistryConfig:
    schema_version: str
    registry_version: str
    source_system: str
    methodology_version: str
    fact_schema_version: str
    score_model_version: str
    ontology_version: str
    rules: Tuple[MappingRule, ...]
    interactions: Tuple[MappingInteraction, ...]


@dataclass(frozen=True)
class MappingRegistryBundle:
    bazi: ContextAwareMappingRegistryConfig
    astrology: ContextAwareMappingRegistryConfig
