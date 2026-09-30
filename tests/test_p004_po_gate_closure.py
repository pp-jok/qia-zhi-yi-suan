from pathlib import Path

import yaml


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MECHANISM_ROOT = PROJECT_ROOT / "candidates" / "semantic-mechanisms-v1"
KNOWLEDGE_ROOT = PROJECT_ROOT / "candidates" / "semantic-knowledge-v1"
MAPPING_ROOT = PROJECT_ROOT / "candidates" / "mapping-v2"


def test_p004_po_decisions_close_only_the_authorized_gates() -> None:
    from destiny_personality.semantic_knowledge import (
        load_astrology_methodology_candidates,
        load_semantic_knowledge_claim_registry,
        load_semantic_knowledge_source_registry,
    )
    from destiny_personality.semantic_mechanisms import (
        load_approved_evidence_root_ids,
        load_semantic_mechanism_candidates,
    )

    mechanism = load_semantic_mechanism_candidates(MECHANISM_ROOT)[0]
    assert mechanism["evidence_role"] == "RULE_GATE"
    assert mechanism["review_status"] == "approved"
    assert mechanism["product_owner_decision_ref"] == (
        "PO-P004-D1-ASPECT-RULE-GATE-2026-09-30"
    )
    assert mechanism["asserts_primitive_state"] is False

    assert "ER-AS-PLANET-PLACEMENT-V1" in load_approved_evidence_root_ids(
        MECHANISM_ROOT
    )

    sources = load_semantic_knowledge_source_registry(KNOWLEDGE_ROOT)
    claims = load_semantic_knowledge_claim_registry(KNOWLEDGE_ROOT, sources)
    methodology = load_astrology_methodology_candidates(
        KNOWLEDGE_ROOT, sources, claims
    )[0]
    assert methodology["review_status"] == "approved_for_semantic_design"
    assert methodology["product_owner_selection_status"] == (
        "SELECTED_FOR_SEMANTIC_DESIGN"
    )
    assert methodology["product_owner_decision_ref"] == (
        "PO-P004-D3-HELLENISTIC-METHOD-2026-09-30"
    )


def test_p004_po_gate_closure_does_not_create_direction_or_mapping() -> None:
    from destiny_personality.semantic_authority import (
        load_mapping_eligible_semantic_mechanisms,
    )
    from destiny_personality.semantic_core import load_semantic_mechanism_role_policy
    from destiny_personality.semantic_mechanisms import (
        load_semantic_mechanism_candidates,
    )

    mechanisms = load_semantic_mechanism_candidates(MECHANISM_ROOT)
    assert [item for item in mechanisms if item["evidence_role"] == "PRIMARY_EVIDENCE"] == []
    assert load_mapping_eligible_semantic_mechanisms(
        MECHANISM_ROOT, load_semantic_mechanism_role_policy(PROJECT_ROOT)
    ).mechanism_ids == frozenset()

    proposal_registry = yaml.safe_load(
        (MAPPING_ROOT / "mapping_proposal_registry_v1.yaml").read_text(
            encoding="utf-8"
        )
    )
    candidate_registry = yaml.safe_load(
        (MAPPING_ROOT / "mapping_v2_candidate_registry_v1.yaml").read_text(
            encoding="utf-8"
        )
    )
    assert proposal_registry["proposals"] == []
    assert candidate_registry["candidates"] == []


def test_p004_po_gate_closure_keeps_active_fingerprints_frozen() -> None:
    from destiny_personality.core_profile_builder import (
        candidate_presentation_bundle_fingerprint,
        candidate_semantic_bundle_fingerprint,
    )

    assert candidate_semantic_bundle_fingerprint() == (
        "256ba053b174a054226301f1b493e0e0c8f9f50e9f2976a72b8045dbf6ed6131"
    )
    assert candidate_presentation_bundle_fingerprint() == (
        "2f1d3866638074485351ada0c6a9aaa9bd1acd916f65973ca2b319a75b99b91d"
    )
