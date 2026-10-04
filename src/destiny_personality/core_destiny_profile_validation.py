"""Invariant checks for the formal Core Destiny Profile."""

from typing import Iterable, Tuple

from .core_profile_models import CoreDestinyProfile, PrimitiveCandidate, PrimitiveState
from .release_manifest import CORE_PRIMITIVE_IDS


_ALLOWED_STATES = {
    "unknown",
    "mixed",
    "supported_high",
    "supported_low",
    "context_differentiated",
}
_ALLOWED_ASSURANCE = {
    "limited_coverage_unknown_only",
    "limited_coverage_approved_mapping",
}


def validate_core_destiny_profile(profile: CoreDestinyProfile) -> Tuple[str, ...]:
    """Return stable formal-profile error codes without modifying the profile."""

    errors = []
    if profile.schema_version != "core-destiny-profile-v1":
        errors.append("FORMAL_CDP_SCHEMA_INVALID")
    if profile.fact_assurance not in {"none", "capability_reported", "project_verified"}:
        errors.append("FORMAL_FACT_ASSURANCE_INVALID")
    if (
        profile.semantic_model_assurance not in _ALLOWED_ASSURANCE
        or profile.semantic_model_assurance == profile.fact_assurance
    ):
        errors.append("FORMAL_SEMANTIC_ASSURANCE_SEPARATION_REQUIRED")
    if set(profile.primitive_states) != set(CORE_PRIMITIVE_IDS):
        errors.append("FORMAL_PRIMITIVE_COVERAGE_INVALID")
    for primitive_id, state in profile.primitive_states.items():
        if state.primitive_id != primitive_id or state.state not in _ALLOWED_STATES:
            errors.append("FORMAL_PRIMITIVE_STATE_INVALID")
        if _is_unknown_as_low_coercion(state):
            errors.append("FORMAL_UNKNOWN_AS_LOW_COERCION")
    if any(item.source_system != "bazi" for item in profile.bazi_primitive_candidates):
        errors.append("FORMAL_BAZI_SOURCE_ISOLATION_FAILED")
    if any(item.source_system != "astrology" for item in profile.astrology_primitive_candidates):
        errors.append("FORMAL_ASTROLOGY_SOURCE_ISOLATION_FAILED")
    if len(profile.cross_system_alignment) != len(CORE_PRIMITIVE_IDS):
        errors.append("FORMAL_ALIGNMENT_COVERAGE_INVALID")
    if any(item.salience_delta != 0 for item in profile.cross_system_alignment):
        errors.append("FORMAL_CROSS_SYSTEM_SALIENCE_INFLATION")
    if _has_candidate_only_refs(_all_rule_refs(profile)):
        errors.append("FORMAL_CANDIDATE_RULE_REF_PROHIBITED")
    if any(
        (profile.dominant_signatures, profile.core_dynamics, profile.shadow_mature_forms, profile.fate_themes)
    ) or profile.archetype is not None:
        errors.append("FORMAL_DOWNSTREAM_UNTRACEABLE")
    if not profile.fact_packet_refs or not profile.audit_trail:
        errors.append("FORMAL_AUDIT_TRAIL_REQUIRED")
    return tuple(sorted(set(errors)))


def _is_unknown_as_low_coercion(state: PrimitiveState) -> bool:
    if state.state != "supported_low":
        return False
    return not state.evidence_refs or not state.counter_candidates


def _all_rule_refs(profile: CoreDestinyProfile) -> Iterable[str]:
    for candidate in profile.bazi_primitive_candidates + profile.astrology_primitive_candidates:
        for reference in candidate.semantic_rule_refs:
            yield reference
    for state in profile.primitive_states.values():
        yield state.resolution_rule_ref
        for reference in state.supporting_candidates + state.counter_candidates:
            yield reference
    for alignment in profile.cross_system_alignment:
        for reference in alignment.bazi_rule_refs + alignment.astrology_rule_refs:
            yield reference


def _has_candidate_only_refs(references: Iterable[str]) -> bool:
    markers = ("candidate", "legacy", "core-profile-v1")
    return any(
        marker in reference.lower()
        for reference in references
        for marker in markers
    )
