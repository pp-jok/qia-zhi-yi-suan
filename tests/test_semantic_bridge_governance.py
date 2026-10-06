"""Acceptance contract for candidate-only Semantic Bridge governance."""

from copy import deepcopy
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SEMANTIC_MECHANISM_ROOT = PROJECT_ROOT / "candidates" / "semantic-mechanisms-v1"
TEN_BRIDGE_GATES = {
    "source_behavior_explicitness",
    "subject_match",
    "process_match",
    "primitive_ownership",
    "direction_entailment",
    "context_match",
    "alternative_interpretation_resolution",
    "traditional_method_reproducibility",
    "counterevidence_definition",
    "scientific_boundary_declaration",
}


@pytest.fixture
def direct_bridge() -> dict:
    return {
        "bridge_id": "SB-P006-DIRECT-TEST-V1",
        "bridge_class": "DIRECT_CONSTRUCT_BRIDGE",
        "source_claim_refs": ["SK-TEST-DIRECT-001"],
        "source_behavior": "The source explicitly describes repeatedly arranging work before acting.",
        "subject_kind": "person",
        "process_meaning": "pre-set task organization",
        "primitive_id": "P006",
        "primitive_ownership_rationale": "P006 uniquely owns task organization, not capability or outcome.",
        "direction_rationale": "Pre-set arrangement entails the supported_high direction.",
        "direction": "supported_high",
        "contexts": ["work"],
        "alternative_interpretations": ["capability"],
        "excluded_interpretations": ["The passage does not claim competence or achievement."],
        "traditional_method_status": "reproducible",
        "counterevidence": "Do not admit a passage that only reports successful outcomes.",
        "scientific_boundary": "traditional_system_semantic_translation",
        "admission_gates": {gate: True for gate in TEN_BRIDGE_GATES},
    }


@pytest.fixture
def behavioral_bridge(direct_bridge: dict) -> dict:
    bridge = deepcopy(direct_bridge)
    bridge.update(
        {
            "bridge_id": "SB-P006-BEHAVIORAL-TEST-V1",
            "bridge_class": "BEHAVIORAL_MECHANISM_BRIDGE",
            "source_claim_refs": ["SK-TEST-BEHAVIOR-001"],
            "source_behavior": "The source describes a person repeatedly preparing a work sequence before beginning it.",
        }
    )
    return bridge


def _approved_primary_evidence(**overrides: object) -> dict:
    candidate = {
        "candidate_id": "SMC-P006-PRIMARY-EVIDENCE-TEST-V1",
        "review_status": "approved",
        "product_owner_decision_ref": "PO-P006-TEST-001",
        "source_system": "bazi",
        "source_fact_classes": ["bazi.ten_gods"],
        "evidence_root_refs": ["ER-TEST-001"],
        "proposed_mechanism": "A governed bridge candidate for P006 review.",
        "target_primitive_questions": ["How is task organization approached?"],
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


@pytest.mark.parametrize("fixture_name", ["direct_bridge", "behavioral_bridge"])
def test_admissible_bridge_classes_pass_every_mandatory_gate(
    request: pytest.FixtureRequest, fixture_name: str
) -> None:
    from destiny_personality.semantic_mechanisms import (
        load_semantic_bridge_policy,
        validate_semantic_bridge_candidate,
    )

    bridge = request.getfixturevalue(fixture_name)
    policy = load_semantic_bridge_policy(PROJECT_ROOT)

    assert set(bridge["admission_gates"]) == TEN_BRIDGE_GATES
    assert validate_semantic_bridge_candidate(bridge, policy) == ()


def test_supported_low_bridge_passes_without_a_supported_high_bridge(
    direct_bridge: dict,
) -> None:
    from destiny_personality.semantic_mechanisms import (
        load_semantic_bridge_policy,
        validate_semantic_bridge_candidate,
    )

    bridge = deepcopy(direct_bridge)
    bridge.update(
        {
            "bridge_id": "SB-P006-DIRECT-LOW-TEST-V1",
            "direction": "supported_low",
            "direction_rationale": "Flexible task sequencing entails the supported_low direction.",
        }
    )

    assert validate_semantic_bridge_candidate(
        bridge, load_semantic_bridge_policy(PROJECT_ROOT)
    ) == ()


@pytest.mark.parametrize(
    ("bridge_class", "expected_code"),
    [
        ("CAPABILITY_OR_ROLE_BRIDGE", "SEMANTIC_BRIDGE_CAPABILITY_OR_ROLE_BLOCKED"),
        ("TEMPERAMENT_BRIDGE", "SEMANTIC_BRIDGE_TEMPERAMENT_BLOCKED"),
        ("OUTCOME_BRIDGE", "SEMANTIC_BRIDGE_OUTCOME_BLOCKED"),
        ("ANALOGICAL_SYMBOLIC_BRIDGE", "SEMANTIC_BRIDGE_SYMBOLIC_ANALOGY_BLOCKED"),
    ],
)
def test_non_behavioral_bridge_classes_are_blocked(
    direct_bridge: dict, bridge_class: str, expected_code: str
) -> None:
    from destiny_personality.semantic_mechanisms import (
        load_semantic_bridge_policy,
        validate_semantic_bridge_candidate,
    )

    bridge = deepcopy(direct_bridge)
    bridge["bridge_class"] = bridge_class

    findings = validate_semantic_bridge_candidate(
        bridge, load_semantic_bridge_policy(PROJECT_ROOT)
    )

    assert (expected_code, "error") in {
        (finding.code, finding.severity) for finding in findings
    }


@pytest.mark.parametrize("gate", sorted(TEN_BRIDGE_GATES))
def test_each_failed_admission_gate_blocks_a_bridge(
    direct_bridge: dict, gate: str
) -> None:
    from destiny_personality.semantic_mechanisms import (
        load_semantic_bridge_policy,
        validate_semantic_bridge_candidate,
    )

    bridge = deepcopy(direct_bridge)
    bridge["admission_gates"][gate] = False

    findings = validate_semantic_bridge_candidate(
        bridge, load_semantic_bridge_policy(PROJECT_ROOT)
    )

    assert any(finding.severity == "error" for finding in findings)


@pytest.mark.parametrize(
    ("field", "value", "expected_code"),
    [
        ("source_behavior", "", "SEMANTIC_BRIDGE_SOURCE_BEHAVIOR_REQUIRED"),
        ("subject_kind", "organization", "SEMANTIC_BRIDGE_SUBJECT_MISMATCH"),
        (
            "primitive_ownership_rationale",
            "",
            "SEMANTIC_BRIDGE_PRIMITIVE_OWNERSHIP_REQUIRED",
        ),
        (
            "excluded_interpretations",
            [],
            "SEMANTIC_BRIDGE_ALTERNATIVES_UNRESOLVED",
        ),
        (
            "scientific_boundary",
            "empirical_psychology",
            "SEMANTIC_BRIDGE_EMPIRICAL_PSYCHOLOGY_CLAIM",
        ),
    ],
)
def test_incomplete_or_empirical_bridge_claims_fail_closed(
    direct_bridge: dict, field: str, value: object, expected_code: str
) -> None:
    from destiny_personality.semantic_mechanisms import (
        load_semantic_bridge_policy,
        validate_semantic_bridge_candidate,
    )

    bridge = deepcopy(direct_bridge)
    bridge[field] = value

    findings = validate_semantic_bridge_candidate(
        bridge, load_semantic_bridge_policy(PROJECT_ROOT)
    )

    assert (expected_code, "error") in {
        (finding.code, finding.severity) for finding in findings
    }


def test_approved_primary_evidence_requires_a_passing_bridge_audit() -> None:
    from destiny_personality.semantic_mechanisms import validate_semantic_mechanism_candidate

    findings = validate_semantic_mechanism_candidate(
        _approved_primary_evidence(), {"ER-TEST-001"}, SEMANTIC_MECHANISM_ROOT
    )

    assert ("SEMANTIC_MECHANISM_BRIDGE_AUDIT_REQUIRED", "error") in {
        (finding.code, finding.severity) for finding in findings
    }


def test_approved_primary_evidence_rejects_unregistered_source_claim(
    direct_bridge: dict,
) -> None:
    from destiny_personality.semantic_mechanisms import validate_semantic_mechanism_candidate

    findings = validate_semantic_mechanism_candidate(
        _approved_primary_evidence(semantic_bridge=direct_bridge),
        {"ER-TEST-001"},
        SEMANTIC_MECHANISM_ROOT,
    )

    assert ("SEMANTIC_BRIDGE_SOURCE_CLAIM_UNRESOLVED", "error") in {
        (finding.code, finding.severity) for finding in findings
    }


def test_approved_primary_evidence_rejects_cross_primitive_claim_binding(
    direct_bridge: dict,
) -> None:
    from destiny_personality.semantic_mechanisms import validate_semantic_mechanism_candidate

    bridge = deepcopy(direct_bridge)
    bridge["source_claim_refs"] = ["SKC-BZ-DAO-SHI-ADVANCEMENT-LIMIT-P004-V1"]
    findings = validate_semantic_mechanism_candidate(
        _approved_primary_evidence(semantic_bridge=bridge),
        {"ER-TEST-001"},
        SEMANTIC_MECHANISM_ROOT,
    )

    assert ("SEMANTIC_BRIDGE_CLAIM_PRIMITIVE_MISMATCH", "error") in {
        (finding.code, finding.severity) for finding in findings
    }


@pytest.mark.parametrize(
    ("field", "value"),
    [("primitive_id", []), ("source_claim_refs", [["not-hashable"]])],
)
def test_malformed_bridge_identifiers_fail_closed_without_crashing(
    direct_bridge: dict, field: str, value: object
) -> None:
    from destiny_personality.semantic_mechanisms import validate_semantic_mechanism_candidate

    bridge = deepcopy(direct_bridge)
    bridge[field] = value

    findings = validate_semantic_mechanism_candidate(
        _approved_primary_evidence(semantic_bridge=bridge),
        {"ER-TEST-001"},
        SEMANTIC_MECHANISM_ROOT,
    )

    assert any(finding.severity == "error" for finding in findings)


def test_method_blocked_bridge_cannot_approve_primary_evidence(
    direct_bridge: dict,
) -> None:
    from destiny_personality.semantic_mechanisms import validate_semantic_mechanism_candidate

    bridge = deepcopy(direct_bridge)
    bridge["traditional_method_status"] = "blocked"
    findings = validate_semantic_mechanism_candidate(
        _approved_primary_evidence(semantic_bridge=bridge),
        {"ER-TEST-001"},
        SEMANTIC_MECHANISM_ROOT,
    )

    assert ("SEMANTIC_MECHANISM_BRIDGE_METHOD_NOT_REPRODUCIBLE", "error") in {
        (finding.code, finding.severity) for finding in findings
    }


@pytest.mark.parametrize(
    "bridge_override",
    [
        {"bridge_class": "CAPABILITY_OR_ROLE_BRIDGE"},
        {"bridge_class": "ANALOGICAL_SYMBOLIC_BRIDGE"},
        {"admission_gates": {**{gate: True for gate in TEN_BRIDGE_GATES}, "process_match": False}},
    ],
)
def test_invalid_bridge_cannot_approve_primary_evidence_when_method_is_reproducible(
    direct_bridge: dict, bridge_override: dict
) -> None:
    from destiny_personality.semantic_mechanisms import validate_semantic_mechanism_candidate

    bridge = deepcopy(direct_bridge)
    bridge.update(bridge_override)
    findings = validate_semantic_mechanism_candidate(
        _approved_primary_evidence(semantic_bridge=bridge),
        {"ER-TEST-001"},
        SEMANTIC_MECHANISM_ROOT,
    )

    assert any(finding.severity == "error" for finding in findings)


def test_rule_gate_remains_valid_without_bridge_fields() -> None:
    from destiny_personality.semantic_mechanisms import validate_semantic_mechanism_candidate

    findings = validate_semantic_mechanism_candidate(
        _approved_primary_evidence(
            candidate_id="SMC-RULE-GATE-TEST-V1",
            evidence_role="RULE_GATE",
        ),
        {"ER-TEST-001"},
        SEMANTIC_MECHANISM_ROOT,
    )

    assert findings == ()
