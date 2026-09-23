import copy
from pathlib import Path

import pytest
import yaml

from destiny_personality.config_errors import ConfigError

from test_semantic_mechanism_contract import _candidate


def _candidate_root() -> Path:
    return Path(__file__).resolve().parents[1] / "candidates" / "semantic-mechanisms-v1"


def _registry_with_root(tmp_path: Path) -> dict:
    source = _candidate_root() / "semantic_evidence_root_registry_v1.yaml"
    registry = yaml.safe_load(source.read_text(encoding="utf-8"))
    registry["roots"] = [
        {
            "evidence_root_id": "ER-TEST-FACT-INSTANCE-V1",
            "system": "test",
            "source_type": "canonical_fact_instance",
            "source_ref": "deterministic_facts.test.instances",
            "version": "deterministic-chart-facts-v1",
            "scope": {"identity_fields": ["fact_id"]},
            "approved_use": ["fact_instance_identification"],
            "prohibited_use": ["direct_primitive_state_assertion"],
            "provenance": {"origin": "project_owned_deterministic_facts"},
            "review_status": "approved",
            "product_owner_decision_ref": "PO-TEST",
        }
    ]
    return registry


def _write_registry(tmp_path: Path, registry: dict) -> None:
    for filename in (
        "semantic_mechanism_contract_v1.yaml",
        "semantic_evidence_root_contract_v1.yaml",
    ):
        source = _candidate_root() / filename
        (tmp_path / filename).write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
    (tmp_path / "semantic_evidence_root_registry_v1.yaml").write_text(
        yaml.safe_dump(registry, allow_unicode=True, sort_keys=False), encoding="utf-8"
    )


def test_mechanism_without_evidence_root_is_rejected() -> None:
    from destiny_personality.semantic_mechanisms import (
        validate_semantic_mechanism_candidate,
    )

    findings = validate_semantic_mechanism_candidate(
        _candidate(evidence_root_refs=[]), set()
    )

    assert {finding.code for finding in findings} == {
        "SEMANTIC_MECHANISM_EVIDENCE_ROOT_REQUIRED"
    }


def test_registry_loads_the_two_approved_fact_identity_roots() -> None:
    from destiny_personality.semantic_mechanisms import (
        load_approved_evidence_root_ids,
        load_evidence_root_registry,
    )

    roots = load_evidence_root_registry(_candidate_root())

    assert {root["evidence_root_id"] for root in roots} == {
        "ER-BZ-TEN-GOD-INSTANCE-V1",
        "ER-AS-ASPECT-INSTANCE-V1",
    }
    assert load_approved_evidence_root_ids(_candidate_root()) == {
        "ER-BZ-TEN-GOD-INSTANCE-V1",
        "ER-AS-ASPECT-INSTANCE-V1",
    }


@pytest.mark.parametrize(
    ("mutation", "expected_code"),
    [
        (lambda root: root.pop("scope"), "CONFIG_GAP"),
        (lambda root: root.__setitem__("review_status", "unreviewed"), "CONFIG_VALUE_ERROR"),
        (lambda root: root.__setitem__("review_status", []), "CONFIG_VALUE_ERROR"),
        (
            lambda root: root["provenance"].__setitem__("origin", "golden_sample"),
            "CONFIG_VALUE_ERROR",
        ),
    ],
)
def test_registry_rejects_invalid_root_entries(mutation, expected_code, tmp_path) -> None:
    from destiny_personality.semantic_mechanisms import load_evidence_root_registry

    registry = _registry_with_root(tmp_path)
    mutation(registry["roots"][0])
    _write_registry(tmp_path, registry)

    with pytest.raises(ConfigError) as error:
        load_evidence_root_registry(tmp_path)

    assert error.value.code == expected_code


def test_registry_rejects_duplicate_root_ids(tmp_path) -> None:
    from destiny_personality.semantic_mechanisms import load_evidence_root_registry

    registry = _registry_with_root(tmp_path)
    registry["roots"].append(copy.deepcopy(registry["roots"][0]))
    _write_registry(tmp_path, registry)

    with pytest.raises(ConfigError) as error:
        load_evidence_root_registry(tmp_path)

    assert error.value.code == "CONFIG_VALUE_ERROR"


def test_root_audit_reports_two_approved_and_zero_other_roots() -> None:
    from destiny_personality.semantic_mechanisms import (
        build_evidence_root_audit_report,
        load_evidence_root_registry,
    )

    report = build_evidence_root_audit_report(
        load_evidence_root_registry(_candidate_root())
    )

    assert report == {
        "root_count": 2,
        "approved_count": 2,
        "non_approved_count": 0,
    }


def test_mechanism_using_unapproved_root_is_rejected() -> None:
    from destiny_personality.semantic_mechanisms import (
        validate_semantic_mechanism_candidate,
    )

    findings = validate_semantic_mechanism_candidate(_candidate(), set())

    assert {finding.code for finding in findings} == {
        "SEMANTIC_MECHANISM_UNAPPROVED_ROOT"
    }


def test_proposed_mechanism_cannot_be_made_eligible_by_caller_supplied_id() -> None:
    from destiny_personality.semantic_mechanisms import mapping_candidate_eligibility

    findings = mapping_candidate_eligibility(
        {"mapping_candidate_id": "MC-001", "mechanism_ref": "SMC-TEST-001"},
        {"SMC-TEST-001"},
    )

    assert {finding.code for finding in findings} == {
        "MAPPING_CANDIDATE_UNAPPROVED_MECHANISM"
    }


def test_authoritative_loader_does_not_approve_current_proposed_mechanism() -> None:
    from destiny_personality.semantic_mechanisms import (
        load_approved_semantic_mechanism_ids,
    )

    assert load_approved_semantic_mechanism_ids(_candidate_root()) == frozenset()
