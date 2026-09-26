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
        (store / f"{name}_registry_v1.yaml").write_text(yaml.safe_dump({"schema_version": f"semantic-{name}-registry-v1", "artifacts": [{"artifact_id": f"{name}:D2", "candidate_bundle_ref": "bundle:test", "bundle_fingerprint": "f" * 64, "run_status": status, "runner_version": "mapping-evaluation-v1", "policy_version": "test-v1", "dataset_refs": ["fixture:test"], "run_timestamp": "2026-09-24T00:00:00Z"}]}), encoding="utf-8")


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


def test_machine_artifact_registration_rejects_nonpassing_artifacts(tmp_path: Path) -> None:
    from destiny_personality.promotion_authority import register_evaluation_artifact

    root = tmp_path / "governance" / "semantic-promotion-v1"
    root.mkdir(parents=True)
    (root / "calibration_registry_v1.yaml").write_text("schema_version: semantic-calibration-registry-v1\nartifacts: []\n", encoding="utf-8")
    artifact = {"schema_version": "semantic-calibration-artifact-v1", "artifact_id": "calibration:T1", "candidate_bundle_ref": "bundle:test", "bundle_fingerprint": "f" * 64, "runner_version": "mapping-evaluation-v1", "policy_version": "policy:test", "dataset_refs": ["fixture:design"], "run_timestamp": "2026-09-26T00:00:00Z", "run_status": "blocked_by_gate", "metrics": {}, "findings": [], "limitations": []}
    with pytest.raises(ValueError, match="EVALUATION_ARTIFACT_NOT_PASSED"):
        register_evaluation_artifact(tmp_path, "calibration", artifact)


def test_machine_artifact_registration_persists_passing_artifact(tmp_path: Path) -> None:
    from destiny_personality.promotion_authority import register_evaluation_artifact

    root = tmp_path / "governance" / "semantic-promotion-v1"
    root.mkdir(parents=True)
    registry = root / "holdout_registry_v1.yaml"
    registry.write_text("schema_version: semantic-holdout-registry-v1\nartifacts: []\n", encoding="utf-8")
    artifact = {"schema_version": "semantic-holdout-artifact-v1", "artifact_id": "holdout:T1", "candidate_bundle_ref": "bundle:test", "bundle_fingerprint": "f" * 64, "runner_version": "mapping-evaluation-v1", "policy_version": "policy:test", "dataset_refs": ["fixture:holdout"], "run_timestamp": "2026-09-26T00:00:00Z", "run_status": "pass", "metrics": {"mapping_count": 2}, "findings": [], "limitations": []}

    register_evaluation_artifact(tmp_path, "holdout", artifact)

    assert yaml.safe_load(registry.read_text(encoding="utf-8"))["artifacts"] == [artifact]


def test_machine_generated_artifacts_round_trip_through_authority_registry(tmp_path: Path) -> None:
    from destiny_personality.mapping_v2 import build_mapping_evaluation_artifact
    from destiny_personality.promotion_authority import load_promotion_authority, register_evaluation_artifact

    root = tmp_path / "governance" / "semantic-promotion-v1"
    root.mkdir(parents=True)
    decision = {"schema_version": "semantic-promotion-decision-v1", "decision_id": "D1", "candidate_bundle_ref": "bundle:test", "candidate_fingerprint": "f" * 64, "decision": "approve_shadow", "allowed_stage": "shadow", "decision_timestamp": "2026-09-26T00:00:00Z", "review_refs": ["review:test"], "supersedes": None}
    (root / "decision_registry_v1.yaml").write_text(yaml.safe_dump({"schema_version": "semantic-promotion-decision-registry-v1", "decisions": [decision]}), encoding="utf-8")
    for kind in ("calibration", "holdout"):
        (root / f"{kind}_registry_v1.yaml").write_text(f"schema_version: semantic-{kind}-registry-v1\nartifacts: []\n", encoding="utf-8")
        artifact = build_mapping_evaluation_artifact(kind, ({"mapping_candidate_id": "M1", "primitive_id": "P1", "contexts": ["work"]},), "bundle:test", "f" * 64, (f"fixture:{kind}",), "policy:test")
        register_evaluation_artifact(tmp_path, kind, artifact)

    assert load_promotion_authority(tmp_path, "bundle:test", "f" * 64, "D1").holdout_artifact_ref.startswith("holdout:")
