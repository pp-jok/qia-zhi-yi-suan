"""Reproducible, machine-readable runners for frozen candidate evaluations."""

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from pathlib import Path
from typing import Mapping, Optional, Tuple

from .core_profile_builder import candidate_semantic_bundle_fingerprint, normalize_candidate_profile
from .core_profile_models import CandidateCoreProfile
from .core_profile_similarity import build_candidate_similarity_matrix, evaluate_candidate_similarity_matrix


@dataclass(frozen=True)
class CandidateCalibrationRun:
    schema_version: str
    bundle_fingerprint: str
    algorithm_versions: Tuple[str, ...]
    case_count: int
    case_ids: Tuple[str, ...]
    normalized_profile_hashes: Mapping[str, str]
    max_similarity: Optional[float]
    threshold: Optional[float]
    threshold_failures: Tuple[str, ...]
    unsupported_activation_frequency: int
    run_status: str


@dataclass(frozen=True)
class CandidateHoldoutRun:
    schema_version: str
    bundle_fingerprint: str
    calibration_policy_sha256: str
    calibration_run_sha256: str
    case_count: int
    case_ids: Tuple[str, ...]
    assertion_failures: Tuple[str, ...]
    run_status: str


def run_candidate_calibration(
    profiles_by_case: Mapping[str, CandidateCoreProfile], output_path: Optional[Path] = None
) -> CandidateCalibrationRun:
    profiles = tuple(profiles_by_case[key] for key in sorted(profiles_by_case))
    evaluation = evaluate_candidate_similarity_matrix(build_candidate_similarity_matrix(profiles))
    result = CandidateCalibrationRun(
        schema_version="candidate-calibration-result-v1",
        bundle_fingerprint=candidate_semantic_bundle_fingerprint(),
        algorithm_versions=("candidate-builder-semantic-v3", "candidate-state-resolver-v3", "candidate-alignment-resolver-v3"),
        case_count=len(profiles), case_ids=tuple(sorted(profiles_by_case)),
        normalized_profile_hashes={key: sha256(repr(normalize_candidate_profile(profiles_by_case[key])).encode()).hexdigest() for key in sorted(profiles_by_case)},
        max_similarity=evaluation.max_similarity, threshold=evaluation.threshold,
        threshold_failures=evaluation.errors, unsupported_activation_frequency=0,
        run_status="pass" if not evaluation.errors else "fail",
    )
    _write_json(output_path, result)
    return result


def run_candidate_holdout(
    profiles_by_case: Mapping[str, CandidateCoreProfile], calibration_result_path: Path, output_path: Optional[Path] = None
) -> CandidateHoldoutRun:
    calibration_bytes = calibration_result_path.read_bytes()
    calibration = json.loads(calibration_bytes)
    bundle = candidate_semantic_bundle_fingerprint()
    failures = []
    if calibration.get("bundle_fingerprint") != bundle:
        failures.append("HOLDOUT_BUNDLE_MISMATCH")
    if calibration.get("run_status") != "pass":
        failures.append("HOLDOUT_CALIBRATION_NOT_PASSED")
    if any(profile.semantic_bundle_fingerprint != bundle for profile in profiles_by_case.values()):
        failures.append("HOLDOUT_PROFILE_BUNDLE_MISMATCH")
    result = CandidateHoldoutRun(
        schema_version="candidate-holdout-result-v1", bundle_fingerprint=bundle,
        calibration_policy_sha256=_active_calibration_policy_sha256(),
        calibration_run_sha256=sha256(calibration_bytes).hexdigest(), case_count=len(profiles_by_case),
        case_ids=tuple(sorted(profiles_by_case)), assertion_failures=tuple(failures),
        run_status="pass" if not failures else "fail",
    )
    _write_json(output_path, result)
    return result


def _active_calibration_policy_sha256() -> str:
    from .candidate_assets import candidate_asset_root
    return sha256((candidate_asset_root() / "core_profile_calibration_policy_v2.yaml").read_bytes()).hexdigest()


def _write_json(path: Optional[Path], value: object) -> None:
    if path is not None:
        path.write_text(json.dumps(asdict(value), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
