"""Decision-bound, persistent shadow promotion records."""

from dataclasses import dataclass, asdict
import json
from pathlib import Path
from typing import Mapping, Tuple

from .promotion_authority import PromotionAuthority



@dataclass(frozen=True)
class PersistedSemanticPromotion:
    status: str
    active_bundle_ref: str
    candidate_bundle_ref: str
    decision_ref: str
    rollback_target: str
    candidate_fingerprint: str
    validation_refs: Tuple[str, ...]


def promote_from_decision(active_bundle_ref: str, candidate_bundle_ref: str, candidate_fingerprint: str, decision_path: Path, technical_checks: Tuple[str, ...], record_path: Path) -> PersistedSemanticPromotion:
    try:
        payload = json.loads(Path(decision_path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError("PROMOTION_DECISION_INVALID") from exc
    _validate_decision_payload(payload)
    if payload.get("candidate_bundle_ref") != candidate_bundle_ref or payload.get("candidate_fingerprint") != candidate_fingerprint or payload.get("allowed_stage") != "shadow":
        raise ValueError("PROMOTION_DECISION_BINDING_MISMATCH")
    if not technical_checks or any(check != "PASS" for check in technical_checks):
        raise ValueError("PROMOTION_TECHNICAL_GATE_FAILED")
    result = PersistedSemanticPromotion("shadow", active_bundle_ref, candidate_bundle_ref, payload["decision_id"], active_bundle_ref, candidate_fingerprint, technical_checks)
    Path(record_path).write_text(json.dumps({"schema_version": "semantic-promotion-record-v1", **asdict(result)}, sort_keys=True) + "\n", encoding="utf-8")
    return result


def promote_from_authority(
    active_bundle_ref: str, authority: PromotionAuthority, record_path: Path
) -> PersistedSemanticPromotion:
    """Persist a shadow record only after Authority Store resolution."""
    if Path(record_path).exists():
        raise ValueError("PROMOTION_DUPLICATE_SHADOW_RECORD")
    result = PersistedSemanticPromotion(
        "shadow", active_bundle_ref, authority.candidate_bundle_ref, authority.decision_id,
        active_bundle_ref, authority.candidate_fingerprint,
        (authority.calibration_artifact_ref, authority.holdout_artifact_ref),
    )
    Path(record_path).parent.mkdir(parents=True, exist_ok=True)
    Path(record_path).write_text(json.dumps({"schema_version": "semantic-promotion-record-v1", **asdict(result)}, sort_keys=True) + "\n", encoding="utf-8")
    return result


def rollback_from_record(record_path: Path) -> PersistedSemanticPromotion:
    try:
        payload = json.loads(Path(record_path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError("ROLLBACK_RECORD_INVALID") from exc
    if payload.get("schema_version") != "semantic-promotion-record-v1" or payload.get("status") != "shadow":
        raise ValueError("ROLLBACK_RECORD_INVALID")
    result = PersistedSemanticPromotion("rolled_back", payload["rollback_target"], payload["candidate_bundle_ref"], payload["decision_ref"], "", payload["candidate_fingerprint"], tuple(payload["validation_refs"]))
    Path(record_path).write_text(json.dumps({"schema_version": "semantic-promotion-record-v1", **asdict(result)}, sort_keys=True) + "\n", encoding="utf-8")
    return result


def _validate_decision_payload(payload: object) -> None:
    if not isinstance(payload, Mapping):
        raise ValueError("PROMOTION_DECISION_INVALID")
    required_strings = ("decision_id", "candidate_bundle_ref", "candidate_fingerprint", "decision_timestamp")
    if payload.get("schema_version") != "semantic-promotion-decision-v1" or payload.get("decision") != "approve_shadow":
        raise ValueError("PROMOTION_DECISION_INVALID")
    if any(not isinstance(payload.get(field), str) or not payload[field] for field in required_strings):
        raise ValueError("PROMOTION_DECISION_INVALID")
    if payload.get("allowed_stage") != "shadow" or not isinstance(payload.get("review_refs"), list):
        raise ValueError("PROMOTION_DECISION_INVALID")


def validate_technical_records(candidate_fingerprint: str, calibration_path: Path, holdout_path: Path) -> Tuple[str, ...]:
    """Require independently persisted calibration and holdout evidence."""
    try:
        calibration = json.loads(Path(calibration_path).read_text(encoding="utf-8"))
        holdout = json.loads(Path(holdout_path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return ("TECHNICAL_RECORD_UNAVAILABLE",)
    findings = []
    for name, payload in (("CALIBRATION", calibration), ("HOLDOUT", holdout)):
        if payload.get("bundle_fingerprint") != candidate_fingerprint:
            findings.append(name + "_BUNDLE_MISMATCH")
        if payload.get("run_status") != "pass":
            findings.append(name + "_NOT_PASSED")
    return ("PASS",) if not findings else tuple(findings)


def shadow_diff_metrics(active_core: dict, candidate_core: dict) -> dict:
    """Summarize observable shadow deltas without changing user-facing output."""
    def count(core: dict, key: str) -> int:
        value = core.get(key, ())
        return len(value) if isinstance(value, (list, tuple)) else int(value is not None)
    states = tuple(candidate_core.get("primitive_states", ()))
    state_count = len(states)
    def rate(state: str) -> float:
        return sum(item.get("state") == state for item in states) / state_count if state_count else 0.0
    return {
        "primitive_activation_delta": count(candidate_core, "primitive_states") - count(active_core, "primitive_states"),
        "unknown_count": sum(item.get("state") == "unknown" for item in states),
        "mixed_count": sum(item.get("state") == "mixed" for item in states),
        "context_differentiated_count": sum(item.get("state") == "context_differentiated" for item in states),
        "unknown_rate": rate("unknown"),
        "mixed_rate": rate("mixed"),
        "context_differentiated_rate": rate("context_differentiated"),
        "signature_count_delta": count(candidate_core, "signatures") - count(active_core, "signatures"),
        "dynamic_count_delta": count(candidate_core, "dynamics") - count(active_core, "dynamics"),
        "theme_count_delta": count(candidate_core, "fate_themes") - count(active_core, "fate_themes"),
    }
