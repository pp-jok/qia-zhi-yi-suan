from dataclasses import dataclass
from typing import Mapping, Optional, Tuple


@dataclass(frozen=True)
class PrimitiveCandidate:
    primitive_id: str
    source_system: str
    direction: str
    fact_refs: Tuple[str, ...]
    semantic_rule_refs: Tuple[str, ...]
    limitations: Tuple[str, ...]


@dataclass(frozen=True)
class PrimitiveState:
    primitive_id: str
    state: str
    evidence_refs: Tuple[str, ...]
    resolution_rule_ref: str
    limitations: Tuple[str, ...]


@dataclass(frozen=True)
class CrossSystemAlignment:
    primitive_id: str
    status: str
    bazi_rule_refs: Tuple[str, ...]
    astrology_rule_refs: Tuple[str, ...]
    limitations: Tuple[str, ...]


@dataclass(frozen=True)
class CoreDestinyProfile:
    schema_version: str
    core_profile_id: str
    fact_assurance: str
    semantic_model_assurance: str
    semantic_model_versions: Tuple[Tuple[str, str], ...]
    bazi_primitive_candidates: Tuple[PrimitiveCandidate, ...]
    astrology_primitive_candidates: Tuple[PrimitiveCandidate, ...]
    cross_system_alignments: Tuple[CrossSystemAlignment, ...]
    primitive_states: Mapping[str, PrimitiveState]
    core_dynamics: Tuple[object, ...]
    archetype: Optional[object]
    limitations: Tuple[str, ...]


@dataclass(frozen=True)
class StoppedCoreProfileExecution:
    """Audit artifact emitted when facts are insufficient for semantic inference."""

    schema_version: str
    core_profile_id: str
    fact_assurance: str
    failure_code: str
    semantic_conclusions: Tuple[object, ...]
    limitations: Tuple[str, ...]
