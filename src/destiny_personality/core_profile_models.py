from dataclasses import dataclass
from typing import Mapping, Optional, Tuple


@dataclass(frozen=True)
class PrimitiveCandidate:
    primitive_id: str
    source_system: str
    direction: str
    fact_refs: Tuple[str, ...]
    semantic_rule_refs: Tuple[str, ...]
    contexts: Tuple[str, ...]
    salience: str
    evidence_stability: str
    modifier_refs: Tuple[str, ...]
    counterevidence_refs: Tuple[str, ...]
    expression_mode: str
    tension_level: str
    counterweight_effect: Optional[str]
    limitations: Tuple[str, ...]


@dataclass(frozen=True)
class PrimitiveState:
    primitive_id: str
    state: str
    evidence_refs: Tuple[str, ...]
    resolution_rule_ref: str
    context_states: Mapping[str, str]
    supporting_candidates: Tuple[str, ...]
    counter_candidates: Tuple[str, ...]
    contradictions: Tuple[str, ...]
    unresolved_contexts: Tuple[str, ...]
    limitations: Tuple[str, ...]


@dataclass(frozen=True)
class CrossSystemAlignment:
    alignment_id: str
    primitive_id: str
    context_refs: Tuple[str, ...]
    status: str
    direction_relation: str
    bazi_rule_refs: Tuple[str, ...]
    astrology_rule_refs: Tuple[str, ...]
    limitations: Tuple[str, ...]


@dataclass(frozen=True)
class CandidateCoreProfile:
    schema_version: str
    candidate_profile_id: str
    fact_assurance: str
    semantic_model_assurance: str
    semantic_capability_level: str
    semantic_bundle_fingerprint: str
    semantic_model_versions: Tuple[Tuple[str, str], ...]
    bazi_primitive_candidates: Tuple[PrimitiveCandidate, ...]
    astrology_primitive_candidates: Tuple[PrimitiveCandidate, ...]
    cross_system_alignments: Tuple[CrossSystemAlignment, ...]
    primitive_states: Mapping[str, PrimitiveState]
    limitations: Tuple[str, ...]


@dataclass(frozen=True)
class CoreDestinyProfile:
    """Reserved formal production IR; candidate execution must not instantiate it."""

    schema_version: str
    core_profile_id: str
    fact_packet_refs: Tuple[str, ...]
    fact_assurance: str
    semantic_model_assurance: str
    semantic_model_versions: Tuple[Tuple[str, str], ...]
    bazi_primitive_candidates: Tuple[PrimitiveCandidate, ...]
    astrology_primitive_candidates: Tuple[PrimitiveCandidate, ...]
    primitive_states: Mapping[str, PrimitiveState]
    cross_system_alignment: Tuple[CrossSystemAlignment, ...]
    dominant_signatures: Tuple[object, ...]
    core_dynamics: Tuple[object, ...]
    shadow_mature_forms: Tuple[object, ...]
    fate_themes: Tuple[object, ...]
    archetype: Optional[object]
    contradictions: Tuple[str, ...]
    limitations: Tuple[str, ...]
    unresolved_questions: Tuple[str, ...]
    audit_trail: Tuple[str, ...]


@dataclass(frozen=True)
class StoppedCoreProfileExecution:
    """Audit artifact emitted when facts are insufficient for semantic inference."""

    schema_version: str
    core_profile_id: str
    fact_assurance: str
    failure_code: str
    semantic_conclusions: Tuple[object, ...]
    limitations: Tuple[str, ...]
