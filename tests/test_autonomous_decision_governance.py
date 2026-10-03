from pathlib import Path

import pytest
import yaml

from destiny_personality.autonomous_governance import (
    load_autonomous_decisions,
    validate_autonomous_decision,
    validate_decision_binding,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = Path("governance/autonomous-completion-v1/decision_registry_v1.yaml")
VALID = {
    "decision_id": "AUTO-TEST-001",
    "asset_id": "TEST-ASSET-V1",
    "asset_type": "test_asset",
    "outcome": "PASS",
    "decision_authority": "delegated_autonomous_executor",
    "decision_mode": "AUTONOMOUS_COMPLETION",
    "decision_ref": "docs/governance/decisions/auto-test-001.md",
    "reason": "Test-only autonomous decision.",
    "evidence_refs": ["tests/fixtures/evidence.yaml"],
    "test_refs": ["tests/test_autonomous_decision_governance.py"],
    "timestamp": "2026-10-04T00:00:00Z",
    "version": "autonomous-completion-v1",
    "asset_fingerprint": "sha256:test-fingerprint",
}


def _write_registry(root: Path, decisions: list[dict]) -> None:
    path = root / REGISTRY_PATH
    path.parent.mkdir(parents=True)
    path.write_text(
        yaml.safe_dump(
            {
                "schema_version": "autonomous-completion-decision-registry-v1",
                "delegation_mode": "AUTONOMOUS_COMPLETION",
                "decisions": decisions,
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )


def test_autonomous_decision_requires_delegated_authority_and_complete_audit() -> None:
    decisions = load_autonomous_decisions(PROJECT_ROOT)

    assert decisions.delegation_mode == "AUTONOMOUS_COMPLETION"
    assert all(item.decision_authority == "delegated_autonomous_executor" for item in decisions.records)


def test_empty_registry_is_valid_until_later_tasks_create_decisions(tmp_path: Path) -> None:
    _write_registry(tmp_path, [])

    decisions = load_autonomous_decisions(tmp_path)

    assert decisions.records == ()


@pytest.mark.parametrize(
    ("mutation", "error_code"),
    (
        (lambda record: record.pop("reason"), "AUTONOMOUS_DECISION_AUDIT_INCOMPLETE"),
        (lambda record: record.update(outcome="APPROVED"), "AUTONOMOUS_DECISION_OUTCOME_INVALID"),
        (lambda record: record.update(decision_authority="human_product_owner"), "AUTONOMOUS_DECISION_AUTHORITY_INVALID"),
        (lambda record: record.update(decision_mode="MANUAL"), "AUTONOMOUS_DECISION_MODE_INVALID"),
        (lambda record: record.update(evidence_refs=[]), "AUTONOMOUS_DECISION_AUDIT_INCOMPLETE"),
        (lambda record: record.update(test_refs=[]), "AUTONOMOUS_DECISION_AUDIT_INCOMPLETE"),
    ),
)
def test_autonomous_decision_rejects_invalid_audit_record(mutation, error_code: str) -> None:
    record = dict(VALID)
    mutation(record)

    with pytest.raises(ValueError, match=error_code):
        validate_autonomous_decision(record)


def test_autonomous_decision_cannot_claim_human_product_owner() -> None:
    with pytest.raises(ValueError, match="AUTONOMOUS_DECISION_AUTHORITY_INVALID"):
        validate_autonomous_decision({**VALID, "decision_authority": "human_product_owner"})


def test_loader_rejects_duplicate_decision_ids(tmp_path: Path) -> None:
    _write_registry(tmp_path, [VALID, dict(VALID)])

    with pytest.raises(ValueError, match="AUTONOMOUS_DECISION_ID_DUPLICATE"):
        load_autonomous_decisions(tmp_path)


def test_decision_binding_rejects_another_asset_or_fingerprint() -> None:
    record = validate_autonomous_decision(VALID)

    assert validate_decision_binding(
        record,
        asset_id="TEST-ASSET-V1",
        asset_fingerprint="sha256:test-fingerprint",
    ) == record
    with pytest.raises(ValueError, match="AUTONOMOUS_DECISION_BINDING_MISMATCH"):
        validate_decision_binding(
            record,
            asset_id="OTHER-ASSET-V1",
            asset_fingerprint="sha256:test-fingerprint",
        )
    with pytest.raises(ValueError, match="AUTONOMOUS_DECISION_BINDING_MISMATCH"):
        validate_decision_binding(
            record,
            asset_id="TEST-ASSET-V1",
            asset_fingerprint="sha256:other-fingerprint",
        )
