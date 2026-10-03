from pathlib import Path

import yaml


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MECHANISM_ROOT = PROJECT_ROOT / "candidates" / "semantic-mechanisms-v1"
KNOWLEDGE_ROOT = PROJECT_ROOT / "candidates" / "semantic-knowledge-v1"
MAPPING_ROOT = PROJECT_ROOT / "candidates" / "mapping-v2"
REVIEW_ROOT = PROJECT_ROOT / "docs" / "reviews"


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


def test_construct_discovery_closes_only_the_current_astrology_p004_path() -> None:
    required_reports = {
        "c2-sm-p004-hellenistic-construct-source-corpus.md",
        "c2-sm-p004-hellenistic-construct-candidate-matrix.md",
        "c2-sm-p004-hellenistic-construct-discovery-final-report.md",
    }
    assert required_reports.issubset(
        {path.name for path in REVIEW_ROOT.glob("*.md")}
    )

    final_report = (
        REVIEW_ROOT / "c2-sm-p004-hellenistic-construct-discovery-final-report.md"
    ).read_text(encoding="utf-8")
    for expected_state in (
        "P004 Hellenistic Construct Discovery:\nNO_DEFENSIBLE_P004_CONSTRUCT",
        "Direct High Constructs:\n0",
        "Direct Low Constructs:\n0",
        "Proposed PRIMARY_EVIDENCE:\n0",
        "Mapping Proposals:\n0",
        "P004 Astrology Path:\nCLOSED_UNDER_CURRENT_METHODOLOGY",
        "Primitive P004 Status:\nVALID",
        "Next Gate:\nP004_BAZI_CONSTRUCT_DISCOVERY",
    ):
        assert expected_state in final_report


def test_bazi_construct_discovery_is_superseded_only_for_advancement() -> None:
    required_reports = {
        "c2-sm-p004-bazi-construct-source-corpus.md",
        "c2-sm-p004-bazi-construct-candidate-matrix.md",
        "c2-sm-p004-bazi-methodology-coverage.md",
        "c2-sm-p004-bazi-structural-gap-matrix.md",
        "c2-sm-p004-bazi-construct-discovery-final-report.md",
    }
    assert required_reports.issubset(
        {path.name for path in REVIEW_ROOT.glob("*.md")}
    )

    final_report = (
        REVIEW_ROOT / "c2-sm-p004-bazi-construct-discovery-final-report.md"
    ).read_text(encoding="utf-8")
    for expected_state in (
        "P004 Astrology:\nCLOSED_UNDER_CURRENT_HELLENISTIC_METHODOLOGY",
        "P004 Bazi Construct Discovery:\nPARTIALLY_SUPERSEDED_FOR_ADVANCEMENT",
        "Direct High Support Constructs:\n0",
        "Direct Advancement Limitation Constructs:\n1",
        "Direct Low Constructs:\n0",
        "Bazi Methodology Candidate:\n1",
        "New Sources:\n2",
        "New Claims:\n1",
        "Proposed Evidence Roots:\n1",
        "Proposed PRIMARY_EVIDENCE:\n0",
        "Mapping Proposals:\n0",
        "P004 Bazi Path:\nOPEN",
        "Next Gate:\nP004_BAZI_METHOD_AND_ROOT_PO_REVIEW",
    ):
        assert expected_state in final_report


def test_bazi_advancement_review_records_the_reopened_counterevidence_path() -> None:
    required_reports = {
        "c2-sm-p004-bazi-advancement-source-audit.md",
        "c2-sm-p004-bazi-advancement-semantic-matrix.md",
        "c2-sm-p004-bazi-advancement-method-condition-audit.md",
        "c2-sm-p004-bazi-advancement-readiness.md",
        "c2-sm-p004-bazi-advancement-counterevidence-final-report.md",
    }
    assert required_reports.issubset(
        {path.name for path in REVIEW_ROOT.glob("*.md")}
    )

    final_report = (
        REVIEW_ROOT
        / "c2-sm-p004-bazi-advancement-counterevidence-final-report.md"
    ).read_text(encoding="utf-8")
    for expected_state in (
        "P004 Bazi Initiation:\nSATURATED",
        "P004 Bazi Pre-action Low:\nSATURATED",
        "P004 Bazi Advancement Review:\nDIRECT_ADVANCEMENT_LIMITATION_FOUND",
        "始勤终惰:\nNEARBY_DILIGENCE_AND_PERSISTENCE",
        "有始无终:\nNEARBY_COMPLETION_STANDALONE",
        "Direct Advancement Constructs:\n1",
        "Advancement Counterevidence Candidates:\n1",
        "Bazi Methodology Candidate:\n1",
        "Proposed Evidence Roots:\n1",
        "Proposed PRIMARY_EVIDENCE:\n0",
        "Mapping Proposals:\n0",
        "P004 Bazi Path:\nOPEN",
        "Next Gate:\nP004_BAZI_METHOD_AND_ROOT_PO_REVIEW",
    ):
        assert expected_state in final_report


def test_bazi_advancement_candidate_chain_is_governed_but_not_activated() -> None:
    from destiny_personality.semantic_knowledge import (
        load_bazi_methodology_candidates,
        load_semantic_knowledge_claim_registry,
        load_semantic_knowledge_source_registry,
    )
    from destiny_personality.semantic_mechanisms import (
        load_approved_evidence_root_ids,
        load_evidence_root_registry,
        load_semantic_mechanism_candidates,
    )

    sources = load_semantic_knowledge_source_registry(KNOWLEDGE_ROOT)
    claims = load_semantic_knowledge_claim_registry(KNOWLEDGE_ROOT, sources)
    methodologies = load_bazi_methodology_candidates(
        KNOWLEDGE_ROOT, sources, claims
    )

    assert {
        "SK-BZ-YUANHAI-ZIPING-PROCESS-P004-V1",
        "SK-BZ-SANMING-TONGHUI-DAO-SHI-P004-V1",
    }.issubset({item["source_id"] for item in sources})
    claim = next(
        item
        for item in claims
        if item["claim_id"] == "SKC-BZ-DAO-SHI-ADVANCEMENT-LIMIT-P004-V1"
    )
    assert claim["p004_relevance"] == "ACTION_ADVANCEMENT"
    assert claim["direction_relevance"] == "conditional_limits_supported_high"
    assert claim["support_class"] == "DIRECT_BUT_SCHOOL_SPECIFIC"

    assert len(methodologies) == 1
    methodology = methodologies[0]
    assert methodology["methodology_candidate_id"] == "BMC-BZ-P004-DAO-SHI-V1"
    assert methodology["review_status"] == "proposed"
    assert methodology["candidate_validation_status"] == "NOT_READY"
    assert methodology["product_owner_selection_status"] == "PENDING"
    assert methodology["product_owner_decision_ref"] is None
    assert methodology["canonical_fact_boundary_status"] == (
        "BLOCKED_BY_CANONICAL_FACT_DESIGN"
    )
    assert methodology["evidence_root_status"] == "WITHDRAWN"
    assert methodology["proposed_evidence_root_ref"] is None

    roots = load_evidence_root_registry(MECHANISM_ROOT)
    assert "ER-BZ-TEN-GOD-INTERACTION-V1" not in {
        item["evidence_root_id"] for item in roots
    }
    assert "ER-BZ-TEN-GOD-INTERACTION-V1" not in load_approved_evidence_root_ids(
        MECHANISM_ROOT
    )
    assert [
        item
        for item in load_semantic_mechanism_candidates(MECHANISM_ROOT)
        if item["evidence_role"] == "PRIMARY_EVIDENCE"
    ] == []


def test_bazi_dao_shi_boundary_review_closes_without_a_fake_po_gate() -> None:
    required_reports = {
        "c2-sm-p004-bazi-dao-shi-canonical-boundary-matrix.md",
        "c2-sm-p004-bazi-dao-shi-method-rule-decomposition.md",
        "c2-sm-p004-bazi-dao-shi-canonical-fact-design.md",
        "c2-sm-p004-bazi-dao-shi-evidence-root-review.md",
        "c2-sm-p004-bazi-dao-shi-methodology-readiness.md",
        "c2-sm-p004-bazi-dao-shi-boundary-final-report.md",
    }
    assert required_reports.issubset({path.name for path in REVIEW_ROOT.glob("*.md")})
    assert not (
        REVIEW_ROOT / "c2-sm-p004-bazi-dao-shi-product-owner-packet.md"
    ).exists()

    report = (
        REVIEW_ROOT / "c2-sm-p004-bazi-dao-shi-boundary-final-report.md"
    ).read_text(encoding="utf-8")
    for state in (
        "Bazi Dao-Shi Methodology Candidate:\nNOT_READY",
        "Canonical Fact Boundary:\nBLOCKED_BY_CANONICAL_FACT_DESIGN",
        "Current ER-BZ-TEN-GOD-INTERACTION-V1:\nWITHDRAWN",
        "Evidence Root Ready:\nNO",
        "Bazi Method Ready:\nNO",
        "Proposed PRIMARY_EVIDENCE:\n0",
        "Mapping Proposals:\n0",
        "Production Activation:\nNOT AUTHORIZED",
        "Next Gate:\nP004_BAZI_DAO_SHI_METHOD_RESEARCH_AND_CANONICAL_FACT_DESIGN",
    ):
        assert state in report
