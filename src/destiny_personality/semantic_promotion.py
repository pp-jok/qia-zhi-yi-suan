"""Decision-bound, persistent shadow promotion records."""

from dataclasses import dataclass, asdict
import json
from pathlib import Path
from typing import Tuple


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
    payload = json.loads(Path(decision_path).read_text(encoding="utf-8"))
    if payload.get("schema_version") != "semantic-promotion-decision-v1" or payload.get("decision") != "approve_shadow":
        raise ValueError("PROMOTION_DECISION_INVALID")
    if payload.get("candidate_bundle_ref") != candidate_bundle_ref or payload.get("candidate_fingerprint") != candidate_fingerprint or payload.get("allowed_stage") != "shadow":
        raise ValueError("PROMOTION_DECISION_BINDING_MISMATCH")
    if not technical_checks or any(check != "PASS" for check in technical_checks):
        raise ValueError("PROMOTION_TECHNICAL_GATE_FAILED")
    result = PersistedSemanticPromotion("shadow", active_bundle_ref, candidate_bundle_ref, payload["decision_id"], active_bundle_ref, candidate_fingerprint, technical_checks)
    Path(record_path).write_text(json.dumps({"schema_version": "semantic-promotion-record-v1", **asdict(result)}, sort_keys=True) + "\n", encoding="utf-8")
    return result


def rollback_from_record(record_path: Path) -> PersistedSemanticPromotion:
    payload = json.loads(Path(record_path).read_text(encoding="utf-8"))
    if payload.get("schema_version") != "semantic-promotion-record-v1" or payload.get("status") != "shadow":
        raise ValueError("ROLLBACK_RECORD_INVALID")
    return PersistedSemanticPromotion("rolled_back", payload["rollback_target"], payload["candidate_bundle_ref"], payload["decision_ref"], "", payload["candidate_fingerprint"], tuple(payload["validation_refs"]))


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
    return {
        "primitive_activation_delta": count(candidate_core, "primitive_states") - count(active_core, "primitive_states"),
        "unknown_rate": sum(item.get("state") == "unknown" for item in states),
        "mixed_rate": sum(item.get("state") == "mixed" for item in states),
        "context_differentiated_rate": sum(item.get("state") == "context_differentiated" for item in states),
        "signature_count_delta": count(candidate_core, "signatures") - count(active_core, "signatures"),
        "dynamic_count_delta": count(candidate_core, "dynamics") - count(active_core, "dynamics"),
        "theme_count_delta": count(candidate_core, "fate_themes") - count(active_core, "fate_themes"),
    }
