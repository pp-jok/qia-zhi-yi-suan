"""Strict loading and binding for delegated autonomous decisions."""

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Tuple, Union

import yaml


REGISTRY_PATH = Path("governance/autonomous-completion-v1/decision_registry_v1.yaml")
SCHEMA_VERSION = "autonomous-completion-decision-registry-v1"
DELEGATION_MODE = "AUTONOMOUS_COMPLETION"
DECISION_AUTHORITY = "delegated_autonomous_executor"
OUTCOMES = frozenset(("PASS", "FAIL", "DEFER", "CLOSE_ZERO"))
REQUIRED_FIELDS = frozenset(
    (
        "decision_id",
        "asset_id",
        "asset_type",
        "outcome",
        "decision_authority",
        "decision_mode",
        "decision_ref",
        "reason",
        "evidence_refs",
        "test_refs",
        "timestamp",
        "version",
        "asset_fingerprint",
    )
)


@dataclass(frozen=True)
class AutonomousDecision:
    decision_id: str
    asset_id: str
    asset_type: str
    outcome: str
    decision_authority: str
    decision_mode: str
    decision_ref: str
    reason: str
    evidence_refs: Tuple[str, ...]
    test_refs: Tuple[str, ...]
    timestamp: str
    version: str
    asset_fingerprint: str


@dataclass(frozen=True)
class AutonomousDecisionRegistry:
    delegation_mode: str
    records: Tuple[AutonomousDecision, ...]


def _error(code: str) -> ValueError:
    return ValueError(code)


def _required_string(record: Mapping[str, Any], field: str) -> str:
    value = record.get(field)
    if not isinstance(value, str) or not value.strip():
        raise _error("AUTONOMOUS_DECISION_AUDIT_INCOMPLETE")
    return value


def _nonempty_references(record: Mapping[str, Any], field: str) -> Tuple[str, ...]:
    value = record.get(field)
    if not isinstance(value, list) or not value:
        raise _error("AUTONOMOUS_DECISION_AUDIT_INCOMPLETE")
    if any(not isinstance(item, str) or not item.strip() for item in value):
        raise _error("AUTONOMOUS_DECISION_AUDIT_INCOMPLETE")
    return tuple(value)


def validate_autonomous_decision(record: Mapping[str, Any]) -> AutonomousDecision:
    """Validate a complete record without accepting human or manual authority."""
    if not isinstance(record, Mapping) or set(record) != REQUIRED_FIELDS:
        raise _error("AUTONOMOUS_DECISION_AUDIT_INCOMPLETE")

    outcome = _required_string(record, "outcome")
    if outcome not in OUTCOMES:
        raise _error("AUTONOMOUS_DECISION_OUTCOME_INVALID")

    authority = _required_string(record, "decision_authority")
    if authority != DECISION_AUTHORITY:
        raise _error("AUTONOMOUS_DECISION_AUTHORITY_INVALID")

    mode = _required_string(record, "decision_mode")
    if mode != DELEGATION_MODE:
        raise _error("AUTONOMOUS_DECISION_MODE_INVALID")

    return AutonomousDecision(
        decision_id=_required_string(record, "decision_id"),
        asset_id=_required_string(record, "asset_id"),
        asset_type=_required_string(record, "asset_type"),
        outcome=outcome,
        decision_authority=authority,
        decision_mode=mode,
        decision_ref=_required_string(record, "decision_ref"),
        reason=_required_string(record, "reason"),
        evidence_refs=_nonempty_references(record, "evidence_refs"),
        test_refs=_nonempty_references(record, "test_refs"),
        timestamp=_required_string(record, "timestamp"),
        version=_required_string(record, "version"),
        asset_fingerprint=_required_string(record, "asset_fingerprint"),
    )


def validate_decision_binding(
    record: Union[AutonomousDecision, Mapping[str, Any]], *, asset_id: str, asset_fingerprint: str
) -> AutonomousDecision:
    """Return a validated decision only when it belongs to the exact asset revision."""
    if isinstance(record, AutonomousDecision):
        record = {
            "decision_id": record.decision_id,
            "asset_id": record.asset_id,
            "asset_type": record.asset_type,
            "outcome": record.outcome,
            "decision_authority": record.decision_authority,
            "decision_mode": record.decision_mode,
            "decision_ref": record.decision_ref,
            "reason": record.reason,
            "evidence_refs": list(record.evidence_refs),
            "test_refs": list(record.test_refs),
            "timestamp": record.timestamp,
            "version": record.version,
            "asset_fingerprint": record.asset_fingerprint,
        }
    decision = validate_autonomous_decision(record)
    if decision.asset_id != asset_id or decision.asset_fingerprint != asset_fingerprint:
        raise _error("AUTONOMOUS_DECISION_BINDING_MISMATCH")
    return decision


def load_autonomous_decisions(root: Path) -> AutonomousDecisionRegistry:
    """Load the repository's autonomous registry, allowing no implicit authority."""
    path = Path(root) / REGISTRY_PATH
    try:
        with path.open(encoding="utf-8") as stream:
            registry = yaml.safe_load(stream)
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        raise _error("AUTONOMOUS_DECISION_REGISTRY_INVALID") from exc

    if not isinstance(registry, dict) or set(registry) != {
        "schema_version", "delegation_mode", "decisions"
    }:
        raise _error("AUTONOMOUS_DECISION_REGISTRY_INVALID")
    if registry["schema_version"] != SCHEMA_VERSION or registry["delegation_mode"] != DELEGATION_MODE:
        raise _error("AUTONOMOUS_DECISION_REGISTRY_INVALID")
    if not isinstance(registry["decisions"], list):
        raise _error("AUTONOMOUS_DECISION_REGISTRY_INVALID")

    records = tuple(validate_autonomous_decision(item) for item in registry["decisions"])
    ids = tuple(record.decision_id for record in records)
    if len(ids) != len(set(ids)):
        raise _error("AUTONOMOUS_DECISION_ID_DUPLICATE")
    return AutonomousDecisionRegistry(DELEGATION_MODE, records)
