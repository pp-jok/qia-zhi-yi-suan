"""Repository-owned trust root for candidate Semantic Core shadow promotion."""

from dataclasses import dataclass
from pathlib import Path
from typing import Mapping

import yaml


@dataclass(frozen=True)
class PromotionAuthority:
    decision_id: str
    candidate_bundle_ref: str
    candidate_fingerprint: str
    calibration_artifact_ref: str
    holdout_artifact_ref: str


def load_promotion_authority(
    project_root: Path, candidate_bundle_ref: str, candidate_fingerprint: str, decision_id: str
) -> PromotionAuthority:
    """Resolve all promotion evidence from the project store, never caller paths."""
    root = Path(project_root) / "governance" / "semantic-promotion-v1"
    decisions = _load_registry(root / "decision_registry_v1.yaml", "semantic-promotion-decision-registry-v1", "decisions")
    decision = _find_by_id(decisions, "decision_id", decision_id, "PROMOTION_DECISION_UNKNOWN")
    _validate_decision(decision)
    if any(item.get("supersedes") == decision_id for item in decisions):
        raise ValueError("PROMOTION_DECISION_SUPERSEDED")
    if decision["candidate_bundle_ref"] != candidate_bundle_ref or decision["candidate_fingerprint"] != candidate_fingerprint:
        raise ValueError("PROMOTION_DECISION_BINDING_MISMATCH")
    calibration = _find_matching_artifact(
        _load_registry(root / "calibration_registry_v1.yaml", "semantic-calibration-registry-v1", "artifacts"),
        candidate_bundle_ref, candidate_fingerprint, "PROMOTION_CALIBRATION"
    )
    holdout = _find_matching_artifact(
        _load_registry(root / "holdout_registry_v1.yaml", "semantic-holdout-registry-v1", "artifacts"),
        candidate_bundle_ref, candidate_fingerprint, "PROMOTION_HOLDOUT"
    )
    return PromotionAuthority(decision_id, candidate_bundle_ref, candidate_fingerprint, str(calibration["artifact_id"]), str(holdout["artifact_id"]))


def _load_registry(path: Path, schema_version: str, collection: str) -> tuple[Mapping[str, object], ...]:
    try:
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise ValueError("PROMOTION_AUTHORITY_REGISTRY_UNAVAILABLE") from exc
    items = payload.get(collection) if isinstance(payload, dict) else None
    if payload.get("schema_version") != schema_version or not isinstance(items, list) or not all(isinstance(item, dict) for item in items):
        raise ValueError("PROMOTION_AUTHORITY_REGISTRY_INVALID")
    return tuple(items)


def _find_by_id(items: tuple[Mapping[str, object], ...], key: str, expected: str, error: str) -> Mapping[str, object]:
    matches = tuple(item for item in items if item.get(key) == expected)
    if len(matches) != 1:
        raise ValueError(error)
    return matches[0]


def _validate_decision(item: Mapping[str, object]) -> None:
    required_strings = ("decision_id", "candidate_bundle_ref", "candidate_fingerprint", "decision_timestamp")
    if item.get("schema_version") != "semantic-promotion-decision-v1" or item.get("decision") != "approve_shadow" or item.get("allowed_stage") != "shadow":
        raise ValueError("PROMOTION_DECISION_INVALID")
    if any(not isinstance(item.get(field), str) or not item[field] for field in required_strings):
        raise ValueError("PROMOTION_DECISION_INVALID")
    if not isinstance(item.get("review_refs"), list) or not all(isinstance(ref, str) and ref for ref in item["review_refs"]):
        raise ValueError("PROMOTION_DECISION_INVALID")
    if item.get("supersedes") is not None and (not isinstance(item["supersedes"], str) or not item["supersedes"]):
        raise ValueError("PROMOTION_DECISION_INVALID")


def _find_matching_artifact(items: tuple[Mapping[str, object], ...], bundle_ref: str, fingerprint: str, prefix: str) -> Mapping[str, object]:
    matches = tuple(item for item in items if item.get("candidate_bundle_ref") == bundle_ref and item.get("bundle_fingerprint") == fingerprint)
    if len(matches) != 1:
        raise ValueError(prefix + "_ARTIFACT_REQUIRED")
    artifact = matches[0]
    required = ("artifact_id", "runner_version", "policy_version", "dataset_refs", "timestamp")
    if any(not artifact.get(field) for field in required):
        raise ValueError(prefix + "_ARTIFACT_INVALID")
    if artifact.get("run_status") != "pass":
        raise ValueError(prefix + "_NOT_PASSED")
    return artifact

