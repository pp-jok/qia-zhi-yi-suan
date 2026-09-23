from pathlib import Path
from typing import Optional

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONTRACT_ROOT = PROJECT_ROOT / "candidates" / "semantic-mechanisms-v1"


def _candidate(**overrides: object) -> dict:
    candidate = {
        "candidate_id": "SMC-TEST-001",
        "review_status": "proposed",
        "source_system": "bazi",
        "source_fact_classes": ["bazi.ten_gods"],
        "evidence_root_refs": ["ER-TEST-001"],
        "proposed_mechanism": "A reviewed fact mechanism stated without a Primitive direction.",
        "target_primitive_questions": ["How is judgement formed and to whom do its standards belong?"],
        "evidence_role": "PRIMARY_EVIDENCE",
        "asserts_primitive_state": False,
        "origin": "approved_evidence_root",
        "legacy_similarity": {
            "same_source_conditions": False,
            "same_target_primitive": False,
            "same_direction": False,
        },
    }
    candidate.update(overrides)
    return candidate


def test_loads_aspect_eligibility_gate_candidate_without_findings() -> None:
    from destiny_personality.semantic_mechanisms import (
        load_semantic_mechanism_candidates,
        load_semantic_mechanism_contracts,
        validate_semantic_mechanism_candidate,
    )

    contracts = load_semantic_mechanism_contracts(CONTRACT_ROOT)

    assert contracts.mechanism_schema_version == "semantic-mechanism-v1"
    assert contracts.evidence_root_schema_version == "semantic-evidence-root-v1"
    assert contracts.allowed_roles == (
        "PRIMARY_EVIDENCE",
        "MODIFIER",
        "CONTEXTUALIZER",
        "COUNTER_EVIDENCE",
        "EXCLUSION",
        "RULE_GATE",
    )
    candidates = load_semantic_mechanism_candidates(CONTRACT_ROOT)

    assert len(candidates) == 1
    assert candidates[0]["candidate_id"] == "SMC-AS-ASPECT-ELIGIBILITY-GATE-P004-V1"
    assert validate_semantic_mechanism_candidate(
        candidates[0], {"ER-AS-ASPECT-INSTANCE-V1"}
    ) == ()


def test_mechanism_without_primitive_question_is_rejected() -> None:
    from destiny_personality.semantic_mechanisms import (
        validate_semantic_mechanism_candidate,
    )

    findings = validate_semantic_mechanism_candidate(
        _candidate(target_primitive_questions=[]), {"ER-TEST-001"}
    )

    assert {finding.code for finding in findings} == {
        "SEMANTIC_MECHANISM_PRIMITIVE_QUESTION_REQUIRED"
    }


def test_direct_primitive_state_assertion_is_rejected() -> None:
    from destiny_personality.semantic_mechanisms import (
        validate_semantic_mechanism_candidate,
    )

    findings = validate_semantic_mechanism_candidate(
        _candidate(asserts_primitive_state=True), {"ER-TEST-001"}
    )

    assert {finding.code for finding in findings} == {
        "SEMANTIC_MECHANISM_DIRECT_STATE_ASSERTION"
    }


@pytest.mark.parametrize(
    ("field", "value", "expected_code"),
    [
        ("candidate_id", 42, "SEMANTIC_MECHANISM_INVALID_CANDIDATE_ID"),
        (
            "source_fact_classes",
            "bazi.ten_gods",
            "SEMANTIC_MECHANISM_INVALID_SOURCE_FACT_CLASSES",
        ),
        (
            "source_system",
            42,
            "SEMANTIC_MECHANISM_INVALID_SOURCE_SYSTEM",
        ),
        (
            "proposed_mechanism",
            ["not", "a", "statement"],
            "SEMANTIC_MECHANISM_INVALID_PROPOSED_MECHANISM",
        ),
        ("origin", ["approved_evidence_root"], "SEMANTIC_MECHANISM_INVALID_ORIGIN"),
        (
            "asserts_primitive_state",
            "false",
            "SEMANTIC_MECHANISM_INVALID_STATE_ASSERTION",
        ),
        (
            "legacy_similarity",
            {"same_source_conditions": False},
            "SEMANTIC_MECHANISM_INVALID_LEGACY_SIMILARITY",
        ),
    ],
)
def test_malformed_candidate_fields_are_blocking(
    field: str, value: object, expected_code: str
) -> None:
    from destiny_personality.semantic_mechanisms import (
        validate_semantic_mechanism_candidate,
    )

    findings = validate_semantic_mechanism_candidate(
        _candidate(**{field: value}), {"ER-TEST-001"}
    )

    assert (expected_code, "error") in {
        (finding.code, finding.severity) for finding in findings
    }


@pytest.mark.parametrize("decision_ref", [None, "", "   "])
def test_approved_mechanism_requires_product_owner_decision_reference(
    decision_ref: Optional[str],
) -> None:
    from destiny_personality.semantic_mechanisms import (
        validate_semantic_mechanism_candidate,
    )

    candidate = _candidate(review_status="approved")
    if decision_ref is not None:
        candidate["product_owner_decision_ref"] = decision_ref

    findings = validate_semantic_mechanism_candidate(
        candidate, {"ER-TEST-001"}
    )

    assert ("SEMANTIC_MECHANISM_APPROVAL_REFERENCE_REQUIRED", "error") in {
        (finding.code, finding.severity) for finding in findings
    }


def test_aspect_eligibility_gate_has_a_valid_admission_audit_report() -> None:
    from destiny_personality.semantic_mechanisms import (
        build_semantic_mechanism_audit_report,
        load_semantic_mechanism_candidates,
    )

    report = build_semantic_mechanism_audit_report(
        load_semantic_mechanism_candidates(CONTRACT_ROOT),
        {"ER-AS-ASPECT-INSTANCE-V1"},
    )

    assert report == {
        "candidate_count": 1,
        "error_count": 0,
        "warning_count": 0,
        "admission_eligible_count": 1,
    }


@pytest.mark.parametrize(
    ("field", "value", "expected_code"),
    [
        ("candidate_id", None, "SEMANTIC_MECHANISM_CONTRACT_FIELD_REQUIRED"),
        ("evidence_role", "UNKNOWN", "SEMANTIC_MECHANISM_INVALID_ROLE"),
        (
            "review_status",
            "unreviewed",
            "SEMANTIC_MECHANISM_INVALID_REVIEW_STATUS",
        ),
        ("origin", "legacy_output", "SEMANTIC_MECHANISM_PROHIBITED_ORIGIN"),
    ],
)
def test_contract_admission_defects_are_rejected(
    field: str, value: Optional[object], expected_code: str
) -> None:
    from destiny_personality.semantic_mechanisms import (
        validate_semantic_mechanism_candidate,
    )

    candidate = _candidate()
    if value is None:
        candidate.pop(field)
    else:
        candidate[field] = value

    findings = validate_semantic_mechanism_candidate(candidate, {"ER-TEST-001"})

    assert expected_code in {finding.code for finding in findings}


def test_loaded_candidate_uses_its_originating_contract_root(tmp_path: Path) -> None:
    from destiny_personality.semantic_mechanisms import (
        load_semantic_mechanism_candidates,
        validate_semantic_mechanism_candidate,
    )

    (tmp_path / "mechanism_candidates").mkdir()
    (tmp_path / "semantic_mechanism_contract_v1.yaml").write_text(
        """schema_version: semantic-mechanism-v1
required_candidate_fields: [candidate_id, review_status, source_system, source_fact_classes, evidence_root_refs, proposed_mechanism, target_primitive_questions, evidence_role, asserts_primitive_state, origin, legacy_similarity]
allowed_roles: [PRIMARY_EVIDENCE]
allowed_review_statuses: [proposed]
prohibited_origins: [approved_evidence_root]
""",
        encoding="utf-8",
    )
    (tmp_path / "mechanism_candidates" / "candidate.yaml").write_text(
        """candidate_id: SMC-CUSTOM-ROOT-V1
review_status: proposed
source_system: bazi
source_fact_classes: [bazi.ten_gods]
evidence_root_refs: [ER-TEST-001]
proposed_mechanism: Candidate only.
target_primitive_questions:
  - "How is judgement formed?"
evidence_role: PRIMARY_EVIDENCE
asserts_primitive_state: false
origin: approved_evidence_root
legacy_similarity:
  same_source_conditions: false
  same_target_primitive: false
  same_direction: false
""",
        encoding="utf-8",
    )

    (candidate,) = load_semantic_mechanism_candidates(tmp_path)
    findings = validate_semantic_mechanism_candidate(candidate, {"ER-TEST-001"})

    assert {finding.code for finding in findings} == {
        "SEMANTIC_MECHANISM_PROHIBITED_ORIGIN"
    }
