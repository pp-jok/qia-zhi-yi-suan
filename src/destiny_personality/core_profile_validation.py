from typing import Tuple

from .core_profile_models import CandidateCoreProfile


_CANDIDATE_PRIMITIVE_IDS = {"P001", "P002", "P003", "P004", "P005", "P006"}
_ALLOWED_STATES = {"unknown", "mixed", "supported_high", "supported_low", "context_differentiated"}
_ALLOWED_ALIGNMENT_STATUSES = {"validation", "contextualization", "unresolved", "non_comparable"}


def validate_candidate_profile(profile: CandidateCoreProfile) -> Tuple[str, ...]:
    """Return stable error codes for D1-only candidate profile invariants."""

    errors = []
    if profile.fact_assurance not in {"project_verified", "capability_reported"}:
        errors.append("FACT_ASSURANCE_INVALID")
    if profile.semantic_model_assurance != "project_semantic_partial":
        errors.append("D1_SEMANTIC_ASSURANCE_INVALID")
    if profile.schema_version != "candidate-core-profile-v1":
        errors.append("CANDIDATE_IR_SCHEMA_INVALID")
    if profile.semantic_capability_level != "primitive_only":
        errors.append("CANDIDATE_CAPABILITY_LEVEL_INVALID")
    if profile.fact_scope.astrology_time_mode not in {"known_time", "stable_only"}:
        errors.append("FACT_SCOPE_CONTRACT_ERROR")
    if profile.fact_scope.birth_time_known != (profile.fact_scope.astrology_time_mode == "known_time"):
        errors.append("FACT_SCOPE_CONTRACT_ERROR")
    if profile.fact_scope.bazi_hour_available != profile.fact_scope.birth_time_known:
        errors.append("FACT_SCOPE_CONTRACT_ERROR")
    if set(profile.primitive_states) != _CANDIDATE_PRIMITIVE_IDS:
        errors.append("D1_PRIMITIVE_COVERAGE_INVALID")
    if any(state.state not in _ALLOWED_STATES for state in profile.primitive_states.values()):
        errors.append("D1_PRIMITIVE_STATE_INVALID")
    if any(
        state.state == "context_differentiated" and len(set(state.context_states.values())) < 2
        for state in profile.primitive_states.values()
    ):
        errors.append("D1_CONTEXT_STATE_INVALID")
    if any(candidate.source_system != "bazi" for candidate in profile.bazi_primitive_candidates):
        errors.append("D1_BAZI_SOURCE_ISOLATION_FAILED")
    if any(candidate.source_system != "astrology" for candidate in profile.astrology_primitive_candidates):
        errors.append("D1_ASTROLOGY_SOURCE_ISOLATION_FAILED")
    if any(
        item.status not in _ALLOWED_ALIGNMENT_STATUSES
        for item in profile.cross_system_alignments
    ):
        errors.append("D1_ALIGNMENT_STATUS_INVALID")
    return tuple(errors)
