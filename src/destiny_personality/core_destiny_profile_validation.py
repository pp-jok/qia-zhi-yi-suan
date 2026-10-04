"""Invariant checks for the formal Core Destiny Profile."""

from typing import Iterable, Tuple

from .core_profile_models import CoreDestinyProfile, PrimitiveCandidate, PrimitiveState
from .release_manifest import CORE_PRIMITIVE_IDS
from .release_mapping_bundle import load_active_release_mapping_bundle


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
_ALLOWED_ALIGNMENT_STATUSES = {"validation", "unresolved", "non_comparable"}
_ALLOWED_DIRECTION_RELATIONS = {
    "agreement",
    "opposed",
    "internal_contradiction",
    "insufficient_approved_evidence",
}


def validate_core_destiny_profile(profile: CoreDestinyProfile) -> Tuple[str, ...]:
    """Return stable formal-profile error codes without modifying the profile."""

    errors = []
    if profile.schema_version != "core-destiny-profile-v1":
        errors.append("FORMAL_CDP_SCHEMA_INVALID")
    if profile.fact_assurance not in {"capability_reported", "project_verified"}:
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
    alignment_ids = tuple(item.primitive_id for item in profile.cross_system_alignment)
    if (
        len(profile.cross_system_alignment) != len(CORE_PRIMITIVE_IDS)
        or set(alignment_ids) != set(CORE_PRIMITIVE_IDS)
        or len(set(alignment_ids)) != len(alignment_ids)
    ):
        errors.append("FORMAL_ALIGNMENT_PRIMITIVE_COVERAGE_INVALID")
    if any(item.salience_delta != 0 for item in profile.cross_system_alignment):
        errors.append("FORMAL_CROSS_SYSTEM_SALIENCE_INFLATION")
    errors.extend(_validate_alignments(profile))
    if _has_candidate_only_refs(_all_rule_refs(profile)):
        errors.append("FORMAL_CANDIDATE_RULE_REF_PROHIBITED")
    if any(
        (profile.dominant_signatures, profile.core_dynamics, profile.shadow_mature_forms, profile.fate_themes)
    ) or profile.archetype is not None:
        errors.append("FORMAL_DOWNSTREAM_UNTRACEABLE")
    if not profile.fact_packet_refs or not profile.audit_trail:
        errors.append("FORMAL_AUDIT_TRAIL_REQUIRED")
    errors.extend(_validate_semantic_state_assurance(profile))
    errors.extend(_validate_release_bundle_binding(profile))
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


def _validate_alignments(profile: CoreDestinyProfile) -> Tuple[str, ...]:
    errors = []
    bazi_refs = _refs_by_primitive(profile.bazi_primitive_candidates)
    astrology_refs = _refs_by_primitive(profile.astrology_primitive_candidates)
    for alignment in profile.cross_system_alignment:
        if (
            alignment.status not in _ALLOWED_ALIGNMENT_STATUSES
            or alignment.direction_relation not in _ALLOWED_DIRECTION_RELATIONS
            or (
                alignment.status == "validation"
                and alignment.direction_relation != "agreement"
            )
            or (
                alignment.status == "unresolved"
                and alignment.direction_relation not in {"opposed", "internal_contradiction"}
            )
            or (
                alignment.status == "non_comparable"
                and alignment.direction_relation != "insufficient_approved_evidence"
            )
        ):
            errors.append("FORMAL_ALIGNMENT_STATUS_INVALID")
        admitted_bazi = bazi_refs.get(alignment.primitive_id, set())
        admitted_astrology = astrology_refs.get(alignment.primitive_id, set())
        if not set(alignment.bazi_rule_refs).issubset(admitted_bazi) or not set(
            alignment.astrology_rule_refs
        ).issubset(admitted_astrology):
            errors.append("FORMAL_ALIGNMENT_REFERENCE_INVALID")
        if not admitted_bazi or not admitted_astrology:
            if (
                alignment.status != "non_comparable"
                or alignment.bazi_rule_refs
                or alignment.astrology_rule_refs
            ):
                errors.append("FORMAL_NON_COMPARABLE_ALIGNMENT_INVALID")
    return tuple(errors)


def _refs_by_primitive(candidates: Iterable[PrimitiveCandidate]) -> dict:
    refs = {}
    for candidate in candidates:
        refs.setdefault(candidate.primitive_id, set()).update(candidate.semantic_rule_refs)
    return refs


def _validate_release_bundle_binding(profile: CoreDestinyProfile) -> Tuple[str, ...]:
    bundle = load_active_release_mapping_bundle()
    versions = dict(profile.semantic_model_versions)
    expected_audit = {
        "active_mapping_bundle:" + bundle.bundle_id,
        "active_mapping_bundle_fingerprint:" + bundle.asset_fingerprint,
    }
    if (
        versions.get("active_mapping_bundle") != bundle.asset_fingerprint
        or not expected_audit.issubset(set(profile.audit_trail))
    ):
        return ("FORMAL_RELEASE_MAPPING_BUNDLE_BINDING_INVALID",)
    if not bundle.mappings and (
        profile.bazi_primitive_candidates
        or profile.astrology_primitive_candidates
        or profile.semantic_model_assurance != "limited_coverage_unknown_only"
        or any(state.state != "unknown" for state in profile.primitive_states.values())
    ):
        return ("FORMAL_RELEASE_MAPPING_BUNDLE_COVERAGE_INVALID",)
    return ()


def _validate_semantic_state_assurance(profile: CoreDestinyProfile) -> Tuple[str, ...]:
    candidates = profile.bazi_primitive_candidates + profile.astrology_primitive_candidates
    if profile.semantic_model_assurance == "limited_coverage_unknown_only":
        if candidates:
            return ("FORMAL_MAPPED_ASSURANCE_TRACEABILITY_REQUIRED",)
        if any(
            state.state != "unknown"
            or state.evidence_refs
            or state.supporting_candidates
            or state.counter_candidates
            or "approved-active-mapping" in state.resolution_rule_ref
            for state in profile.primitive_states.values()
        ):
            return ("FORMAL_UNKNOWN_ONLY_STATE_INVALID",)
        return ()
    if profile.semantic_model_assurance != "limited_coverage_approved_mapping" or not candidates:
        return ("FORMAL_MAPPED_ASSURANCE_TRACEABILITY_REQUIRED",)
    errors = []
    for candidate in candidates:
        state = profile.primitive_states.get(candidate.primitive_id)
        if state is None:
            errors.append("FORMAL_MAPPED_ASSURANCE_TRACEABILITY_REQUIRED")
            continue
        if not set(candidate.fact_refs).issubset(set(state.evidence_refs)) or not set(
            candidate.semantic_rule_refs
        ).issubset(
            set(state.supporting_candidates + state.counter_candidates)
        ):
            errors.append("FORMAL_MAPPED_ASSURANCE_TRACEABILITY_REQUIRED")
    for primitive_id, state in profile.primitive_states.items():
        if state.state == "unknown":
            continue
        matching_candidates = _matching_candidates_for_state(
            candidates, primitive_id, state.state
        )
        if not state.evidence_refs or not _has_required_direction_refs(state):
            errors.append("FORMAL_MAPPED_STATE_EVIDENCE_REQUIRED")
        admitted_facts = {
            reference
            for candidate in matching_candidates
            for reference in candidate.fact_refs
        }
        admitted_rules = {
            reference
            for candidate in matching_candidates
            for reference in candidate.semantic_rule_refs
        }
        if (
            not matching_candidates
            or not set(state.evidence_refs).issubset(admitted_facts)
            or not set(state.supporting_candidates + state.counter_candidates).issubset(
                admitted_rules
            )
        ):
            errors.append("FORMAL_MAPPED_STATE_TRACEABILITY_INVALID")
    return tuple(sorted(set(errors)))


def _matching_candidates_for_state(
    candidates: Iterable[PrimitiveCandidate], primitive_id: str, state: str
) -> Tuple[PrimitiveCandidate, ...]:
    primitive_candidates = tuple(
        candidate for candidate in candidates if candidate.primitive_id == primitive_id
    )
    high = tuple(
        candidate
        for candidate in primitive_candidates
        if candidate.direction in {"high", "supported_high"}
    )
    low = tuple(
        candidate
        for candidate in primitive_candidates
        if candidate.direction in {"low", "supported_low"}
    )
    if state == "supported_high":
        return high
    if state == "supported_low":
        return low
    if state in {"mixed", "context_differentiated"}:
        return high + low
    return ()


def _has_required_direction_refs(state: PrimitiveState) -> bool:
    if state.state == "supported_high":
        return bool(state.supporting_candidates)
    if state.state == "supported_low":
        return bool(state.counter_candidates)
    if state.state in {"mixed", "context_differentiated"}:
        return bool(state.supporting_candidates and state.counter_candidates)
    return False
