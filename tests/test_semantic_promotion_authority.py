from pathlib import Path

import pytest
import yaml


def _write_store(root: Path, *, superseded: bool = False, calibration_status: str = "pass", holdout_status: str = "pass") -> None:
    store = root / "governance" / "semantic-promotion-v1"
    store.mkdir(parents=True, exist_ok=True)
    decision = {"schema_version": "semantic-promotion-decision-v1", "decision_id": "D2", "candidate_bundle_ref": "bundle:test", "candidate_fingerprint": "f" * 64, "decision": "approve_shadow", "allowed_stage": "shadow", "decision_timestamp": "2026-09-24T00:00:00Z", "review_refs": ["review:test"], "supersedes": "D1" if superseded else None}
    decisions = [decision]
    if superseded:
        decisions.insert(0, {**decision, "decision_id": "D1", "supersedes": None})
    (store / "decision_registry_v1.yaml").write_text(yaml.safe_dump({"schema_version": "semantic-promotion-decision-registry-v1", "decisions": decisions}), encoding="utf-8")
    for name, status in (("calibration", calibration_status), ("holdout", holdout_status)):
        (store / f"{name}_registry_v1.yaml").write_text(yaml.safe_dump({"schema_version": f"semantic-{name}-registry-v1", "artifacts": [{"artifact_id": f"{name}:D2", "candidate_bundle_ref": "bundle:test", "bundle_fingerprint": "f" * 64, "run_status": status, "runner_version": "mapping-evaluation-v1", "policy_version": "test-v1", "dataset_refs": ["fixture:test"], "timestamp": "2026-09-24T00:00:00Z"}]}), encoding="utf-8")


def test_authority_loader_uses_repository_registry_not_caller_files(tmp_path: Path) -> None:
    from destiny_personality.promotion_authority import load_promotion_authority

    _write_store(tmp_path)
    authority = load_promotion_authority(tmp_path, "bundle:test", "f" * 64, "D2")
    assert authority.decision_id == "D2"
    assert authority.calibration_artifact_ref == "calibration:D2"


def test_authority_loader_rejects_superseded_and_failed_artifacts(tmp_path: Path) -> None:
    from destiny_personality.promotion_authority import load_promotion_authority

    _write_store(tmp_path, superseded=True)
    with pytest.raises(ValueError, match="PROMOTION_DECISION_SUPERSEDED"):
        load_promotion_authority(tmp_path, "bundle:test", "f" * 64, "D1")
    _write_store(tmp_path, calibration_status="fail")
    with pytest.raises(ValueError, match="PROMOTION_CALIBRATION_NOT_PASSED"):
        load_promotion_authority(tmp_path, "bundle:test", "f" * 64, "D2")


def test_authority_promotion_persists_registry_references_and_rejects_duplicates(tmp_path: Path) -> None:
    from destiny_personality.promotion_authority import load_promotion_authority
    from destiny_personality.semantic_promotion import promote_from_authority

    _write_store(tmp_path)
    authority = load_promotion_authority(tmp_path, "bundle:test", "f" * 64, "D2")
    record = tmp_path / "governance" / "semantic-promotion-v1" / "promotion-records" / "D2.json"
    promotion = promote_from_authority("active:test", authority, record)
    assert promotion.validation_refs == ("calibration:D2", "holdout:D2")
    with pytest.raises(ValueError, match="PROMOTION_DUPLICATE_SHADOW_RECORD"):
        promote_from_authority("active:test", authority, record)

