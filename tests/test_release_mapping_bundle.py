from pathlib import Path

import pytest
import yaml


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_active_mapping_bundle_is_governed_and_explicitly_empty():
    from destiny_personality.release_mapping_bundle import load_active_release_mapping_bundle

    bundle = load_active_release_mapping_bundle()
    assert bundle.bundle_id == "ACTIVE-RELEASE-MAPPING-BUNDLE-V1"
    assert bundle.activation_status == "active"
    assert bundle.mappings == ()
    assert bundle.decision_ref == "docs/governance/decisions/auto-release-mapping-bundle-v1.md"


def test_active_mapping_bundle_rejects_nonempty_or_fingerprint_tampering(tmp_path):
    from destiny_personality.release_mapping_bundle import (
        active_release_mapping_bundle_path,
        load_active_release_mapping_bundle,
    )

    payload = yaml.safe_load(active_release_mapping_bundle_path().read_text(encoding="utf-8"))
    payload["mappings"] = [{"mapping_candidate_id": "FORGED"}]
    payload["mapping_count"] = 1
    path = tmp_path / "bundle.yaml"
    path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")
    with pytest.raises(ValueError, match="RELEASE_MAPPING_BUNDLE_INVALID"):
        load_active_release_mapping_bundle(path)


def test_bundle_decision_matches_autonomous_registry():
    from destiny_personality.autonomous_governance import load_autonomous_decisions
    from destiny_personality.release_mapping_bundle import load_active_release_mapping_bundle

    bundle = load_active_release_mapping_bundle()
    record = next(
        item
        for item in load_autonomous_decisions(PROJECT_ROOT).records
        if item.asset_id == bundle.bundle_id
    )
    assert record.outcome == "CLOSE_ZERO"
    assert record.asset_fingerprint == bundle.asset_fingerprint
    assert record.decision_ref == bundle.decision_ref
