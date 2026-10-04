"""Regression coverage for delegated autonomous Evidence Root approval."""

import copy
import shutil
from pathlib import Path

import pytest
import yaml

from destiny_personality.config_errors import ConfigError


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = PROJECT_ROOT / "candidates" / "semantic-mechanisms-v1"


def _root_by_id(root_id: str) -> dict:
    from destiny_personality.semantic_mechanisms import load_evidence_root_registry

    return next(
        root
        for root in load_evidence_root_registry(SOURCE_ROOT)
        if root["evidence_root_id"] == root_id
    )


def _copied_candidate_root(tmp_path: Path) -> Path:
    candidate_root = tmp_path / "candidates" / "semantic-mechanisms-v1"
    candidate_root.parent.mkdir(parents=True)
    shutil.copytree(SOURCE_ROOT, candidate_root)
    return candidate_root


def _write_registry(root: Path, registry: dict) -> None:
    (root / "semantic_evidence_root_registry_v1.yaml").write_text(
        yaml.safe_dump(registry, allow_unicode=True, sort_keys=False), encoding="utf-8"
    )


def _copy_project_decision_registry(root: Path) -> Path:
    governance = root / "governance" / "autonomous-completion-v1"
    governance.mkdir(parents=True)
    source = PROJECT_ROOT / "governance" / "autonomous-completion-v1" / "decision_registry_v1.yaml"
    shutil.copy(source, governance / "decision_registry_v1.yaml")
    return governance


def test_generic_relation_root_is_identity_only_and_autonomously_decided() -> None:
    root = _root_by_id("ER-BZ-RELATION-INSTANCE-V1")

    assert root["source_ref"] == "deterministic_facts.bazi.relations"
    assert root["scope"]["identity_fields"] == [
        "relation_type",
        "participant_refs",
        "rule_version",
    ]
    assert root["decision_authority"] == "delegated_autonomous_executor"
    assert root["decision_mode"] == "AUTONOMOUS_COMPLETION"
    assert root["decision_ref"] == (
        "docs/governance/decisions/auto-er-bz-relation-instance-v1.md"
    )
    assert "dao_shi_assertion" in root["prohibited_use"]
    assert "effective_control_assertion" in root["prohibited_use"]
    assert "mapping_rule_creation" in root["prohibited_use"]


def test_legacy_human_roots_remain_valid_without_autonomous_fields() -> None:
    root = _root_by_id("ER-BZ-TEN-GOD-INSTANCE-V1")

    assert root["product_owner_decision_ref"]
    assert "decision_authority" not in root
    assert "decision_mode" not in root
    assert "decision_ref" not in root


def test_autonomous_root_cannot_claim_product_owner_decision(tmp_path: Path) -> None:
    from destiny_personality.semantic_mechanisms import load_evidence_root_registry

    candidate_root = _copied_candidate_root(tmp_path)
    registry = yaml.safe_load(
        (candidate_root / "semantic_evidence_root_registry_v1.yaml").read_text(
            encoding="utf-8"
        )
    )
    autonomous_root = next(
        item
        for item in registry["roots"]
        if item["evidence_root_id"] == "ER-BZ-RELATION-INSTANCE-V1"
    )
    autonomous_root["product_owner_decision_ref"] = "PO-FORGED"
    _write_registry(candidate_root, registry)

    with pytest.raises(ConfigError, match="cannot claim a Product Owner"):
        load_evidence_root_registry(candidate_root)


def test_autonomous_root_rejects_explicit_null_product_owner_field(
    tmp_path: Path,
) -> None:
    from destiny_personality.semantic_mechanisms import load_evidence_root_registry

    candidate_root = _copied_candidate_root(tmp_path)
    registry = yaml.safe_load(
        (candidate_root / "semantic_evidence_root_registry_v1.yaml").read_text(
            encoding="utf-8"
        )
    )
    autonomous_root = next(
        item
        for item in registry["roots"]
        if item["evidence_root_id"] == "ER-BZ-RELATION-INSTANCE-V1"
    )
    autonomous_root["product_owner_decision_ref"] = None
    _write_registry(candidate_root, registry)
    _copy_project_decision_registry(tmp_path)

    with pytest.raises(ConfigError, match="cannot claim a Product Owner"):
        load_evidence_root_registry(candidate_root)


def test_autonomous_root_without_registry_decision_fails_closed(tmp_path: Path) -> None:
    from destiny_personality.semantic_mechanisms import load_evidence_root_registry

    candidate_root = _copied_candidate_root(tmp_path)
    governance = tmp_path / "governance" / "autonomous-completion-v1"
    governance.mkdir(parents=True)
    (governance / "decision_registry_v1.yaml").write_text(
        yaml.safe_dump(
            {
                "schema_version": "autonomous-completion-decision-registry-v1",
                "delegation_mode": "AUTONOMOUS_COMPLETION",
                "decisions": [],
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )

    with pytest.raises(ConfigError, match="autonomous decision"):
        load_evidence_root_registry(candidate_root)


def test_autonomous_root_fails_closed_when_registry_binding_is_forged(
    tmp_path: Path,
) -> None:
    from destiny_personality.semantic_mechanisms import load_evidence_root_registry

    candidate_root = _copied_candidate_root(tmp_path)
    governance = tmp_path / "governance" / "autonomous-completion-v1"
    governance.mkdir(parents=True)
    registry = yaml.safe_load(
        (PROJECT_ROOT / "governance" / "autonomous-completion-v1" / "decision_registry_v1.yaml").read_text(
            encoding="utf-8"
        )
    )
    registry["decisions"] = copy.deepcopy(registry["decisions"])
    decision = next(
        item
        for item in registry["decisions"]
        if item["asset_id"] == "ER-BZ-RELATION-INSTANCE-V1"
    )
    decision["asset_id"] = "ER-FORGED"
    (governance / "decision_registry_v1.yaml").write_text(
        yaml.safe_dump(registry, sort_keys=False), encoding="utf-8"
    )

    with pytest.raises(ConfigError, match="autonomous decision"):
        load_evidence_root_registry(candidate_root)


@pytest.mark.parametrize("outcome", ("FAIL", "DEFER", "CLOSE_ZERO"))
def test_autonomous_root_requires_a_passing_bound_decision(
    tmp_path: Path, outcome: str
) -> None:
    from destiny_personality.semantic_mechanisms import load_evidence_root_registry

    candidate_root = _copied_candidate_root(tmp_path)
    governance = tmp_path / "governance" / "autonomous-completion-v1"
    governance.mkdir(parents=True)
    registry = yaml.safe_load(
        (PROJECT_ROOT / "governance" / "autonomous-completion-v1" / "decision_registry_v1.yaml").read_text(
            encoding="utf-8"
        )
    )
    registry["decisions"] = copy.deepcopy(registry["decisions"])
    decision = next(
        item
        for item in registry["decisions"]
        if item["asset_id"] == "ER-BZ-RELATION-INSTANCE-V1"
    )
    decision["outcome"] = outcome
    (governance / "decision_registry_v1.yaml").write_text(
        yaml.safe_dump(registry, sort_keys=False), encoding="utf-8"
    )

    with pytest.raises(ConfigError, match="requires a passing autonomous decision"):
        load_evidence_root_registry(candidate_root)
