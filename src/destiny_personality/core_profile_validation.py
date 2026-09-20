from typing import Tuple

from .core_profile_models import CoreDestinyProfile


_CANDIDATE_PRIMITIVE_IDS = {"P001", "P002", "P003", "P004", "P005", "P006"}
_ALLOWED_STATES = {"unknown", "mixed", "supported_high", "supported_low"}
_ALLOWED_ALIGNMENT_STATUSES = {"validation", "unresolved", "non_comparable"}


def validate_candidate_profile(profile: CoreDestinyProfile) -> Tuple[str, ...]:
    """Return stable error codes for D1-only candidate profile invariants."""

    errors = []
    if profile.fact_assurance not in {"project_verified", "capability_reported"}:
        errors.append("FACT_ASSURANCE_INVALID")
    if profile.semantic_model_assurance != "project_semantic_partial":
        errors.append("D1_SEMANTIC_ASSURANCE_INVALID")
    if set(profile.primitive_states) != _CANDIDATE_PRIMITIVE_IDS:
        errors.append("D1_PRIMITIVE_COVERAGE_INVALID")
    if any(state.state not in _ALLOWED_STATES for state in profile.primitive_states.values()):
        errors.append("D1_PRIMITIVE_STATE_INVALID")
    if any(candidate.source_system != "bazi" for candidate in profile.bazi_primitive_candidates):
        errors.append("D1_BAZI_SOURCE_ISOLATION_FAILED")
    if any(candidate.source_system != "astrology" for candidate in profile.astrology_primitive_candidates):
        errors.append("D1_ASTROLOGY_SOURCE_ISOLATION_FAILED")
    if any(
        item.status not in _ALLOWED_ALIGNMENT_STATUSES
        for item in profile.cross_system_alignments
    ):
        errors.append("D1_ALIGNMENT_STATUS_INVALID")
    if profile.core_dynamics:
        errors.append("D1_DYNAMIC_DERIVATION_DISABLED")
    if profile.archetype is not None:
        errors.append("D1_ARCHETYPE_DERIVATION_DISABLED")
    return tuple(errors)
