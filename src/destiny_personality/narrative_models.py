from dataclasses import dataclass
from typing import Any, Tuple


@dataclass(frozen=True)
class NarrativeRule:
    rule_id: str
    priority: int
    target_section: str
    source_kinds: Tuple[str, ...]
    requires_chart_anchor: bool
    rendering_constraints: Any
    prohibited_inferences: Tuple[str, ...]
    limitations: Tuple[str, ...]


@dataclass(frozen=True)
class NarrativeRulesConfig:
    schema_version: str
    narrative_version: str
    ontology_version: str
    dimension_policy_version: str
    sections: Tuple[str, ...]
    invariants: Any
    rules: Tuple[NarrativeRule, ...]
