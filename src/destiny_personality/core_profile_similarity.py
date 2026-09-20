from dataclasses import dataclass
from itertools import combinations
from pathlib import Path
from typing import Mapping, Optional, Tuple

import yaml

from .core_profile_builder import candidate_semantic_bundle_fingerprint
from .core_profile_models import CoreDestinyProfile


@dataclass(frozen=True)
class CandidateProfileComparison:
    """Diagnostic-only comparison while C4b policy values remain unapproved."""

    case_pair: Tuple[str, str]
    primitive_state_pairs: Mapping[str, Tuple[str, str]]
    weighted_primitive_overlap: Optional[float]
    weighted_primitive_overlap_status: str
    signature_primitive_overlap: Optional[float]
    signature_primitive_overlap_status: str
    dynamic_family_pole_overlap: Optional[float]
    dynamic_family_pole_overlap_status: str
    fate_theme_overlap: Optional[float]
    fate_theme_overlap_status: str
    overall_score: Optional[float]


@dataclass(frozen=True)
class CandidateCalibrationResult:
    max_similarity: Optional[float]
    threshold: Optional[float]
    errors: Tuple[str, ...]


def compare_candidate_profiles(
    left: CoreDestinyProfile,
    right: CoreDestinyProfile,
) -> CandidateProfileComparison:
    """Expose comparable structures without inventing C4b weights or thresholds."""

    primitive_ids = sorted(set(left.primitive_states) | set(right.primitive_states))
    primitive_state_pairs = {
        primitive_id: (
            left.primitive_states[primitive_id].state if primitive_id in left.primitive_states else "absent",
            right.primitive_states[primitive_id].state if primitive_id in right.primitive_states else "absent",
        )
        for primitive_id in primitive_ids
    }
    primitive_overlap, primitive_status = _weighted_primitive_overlap(left, right)
    return CandidateProfileComparison(
        case_pair=(left.core_profile_id, right.core_profile_id),
        primitive_state_pairs=primitive_state_pairs,
        weighted_primitive_overlap=primitive_overlap,
        weighted_primitive_overlap_status=primitive_status,
        signature_primitive_overlap=None,
        signature_primitive_overlap_status="not_applicable",
        dynamic_family_pole_overlap=None,
        dynamic_family_pole_overlap_status="not_applicable",
        fate_theme_overlap=None,
        fate_theme_overlap_status="not_applicable",
        overall_score=primitive_overlap,
    )


def build_candidate_similarity_matrix(
    profiles: Tuple[CoreDestinyProfile, ...],
) -> Tuple[CandidateProfileComparison, ...]:
    """Build a stable diagnostic matrix without treating duplicate IDs as cases."""

    unique_profiles = []
    seen_ids = set()
    for profile in profiles:
        if profile.core_profile_id not in seen_ids:
            unique_profiles.append(profile)
            seen_ids.add(profile.core_profile_id)
    return tuple(
        compare_candidate_profiles(left, right)
        for left, right in combinations(unique_profiles, 2)
    )


def evaluate_candidate_similarity_matrix(
    matrix: Tuple[CandidateProfileComparison, ...],
) -> CandidateCalibrationResult:
    """Apply the frozen candidate contrast threshold without enabling production use."""

    policy = _load_current_candidate_policy()
    if policy is None:
        return CandidateCalibrationResult(None, None, ("CALIBRATION_POLICY_GAP",))
    threshold = policy["contrast_pair_thresholds"]["default_max_similarity"]
    scores = [
        comparison.overall_score
        for comparison in matrix
        if comparison.overall_score is not None
    ]
    if not scores:
        return CandidateCalibrationResult(None, threshold, ())
    max_similarity = max(scores)
    errors = (
        ("CANDIDATE_CONTRAST_SIMILARITY_EXCEEDED",)
        if max_similarity > threshold
        else ()
    )
    return CandidateCalibrationResult(max_similarity, threshold, errors)


def _weighted_primitive_overlap(
    left: CoreDestinyProfile,
    right: CoreDestinyProfile,
) -> Tuple[Optional[float], str]:
    policy = _load_current_candidate_policy()
    if policy is None:
        return None, "CALIBRATION_POLICY_GAP"
    weights = policy["primitive_salience_weights"]
    left_tokens = {
        (primitive_id, state.state)
        for primitive_id, state in left.primitive_states.items()
        if state.state != "unknown"
    }
    right_tokens = {
        (primitive_id, state.state)
        for primitive_id, state in right.primitive_states.items()
        if state.state != "unknown"
    }
    union = left_tokens | right_tokens
    if not union:
        return None, "not_applicable"
    overlap = left_tokens & right_tokens
    denominator = sum(weights[primitive_id] for primitive_id, _ in union)
    numerator = sum(weights[primitive_id] for primitive_id, _ in overlap)
    return numerator / denominator, "calibrated"


def _load_current_candidate_policy() -> Optional[dict]:
    policy_path = (
        Path(__file__).resolve().parents[2]
        / "candidates"
        / "core-profile-v1"
        / "core_profile_calibration_policy_v1.yaml"
    )
    policy = yaml.safe_load(policy_path.read_text(encoding="utf-8"))
    if policy["bundle_fingerprint"] != candidate_semantic_bundle_fingerprint():
        return None
    if policy["similarity_weights"]["weighted_primitive_overlap"] != 1.0:
        return None
    return policy
