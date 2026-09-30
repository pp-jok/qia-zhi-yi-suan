from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
KNOWLEDGE_ROOT = PROJECT_ROOT / "candidates" / "semantic-knowledge-v1"


def test_loads_candidate_only_p004_semantic_knowledge_registries() -> None:
    from destiny_personality.semantic_knowledge import (
        build_semantic_knowledge_audit,
        load_semantic_knowledge_claim_registry,
        load_semantic_knowledge_source_registry,
    )

    sources = load_semantic_knowledge_source_registry(KNOWLEDGE_ROOT)
    claims = load_semantic_knowledge_claim_registry(KNOWLEDGE_ROOT, sources)

    assert {source["source_id"] for source in sources} == {
        "SK-BZ-TEN-GODS-YAP-2010",
        "SK-BZ-PATTERNS-ALSAYED-2026",
        "SK-AS-MARS-HOULDING-2004",
        "SK-AS-ASPECTS-HOULDING-2004",
        "SK-AS-HELLENISTIC-GEORGE-2019-2022",
        "SK-AS-DIGNITY-HOULDING",
        "SK-AS-NATAL-ASPECTS-CAMPION-2003",
        "SK-PROJECT-P004-ONTOLOGY-V2",
    }
    assert {claim["claim_id"] for claim in claims} == {
        "SKC-BZ-TEN-GODS-STRUCTURAL-ONLY-P004-V1",
        "SKC-AS-MARS-ACTION-INITIATIVE-P004-V1",
        "SKC-AS-ASPECT-TECHNIQUE-DISPUTE-P004-V1",
        "SKC-AS-HELLENISTIC-NATAL-CONDITION-V1",
        "SKC-AS-DIGNITY-CONDITION-NOT-DIRECTION-P004-V1",
        "SKC-AS-NATAL-ASPECTS-QUALIFY-NOT-DIRECT-P004-V1",
    }
    audit = build_semantic_knowledge_audit(sources, claims)
    assert audit["source_quality_distribution"] == {"TIER_A": 1, "TIER_B": 6, "TIER_C": 1}
    assert audit["direct_p004_claim_count"] == 1
    assert audit["school_specific_direct_claim_count"] == 1


def test_methodology_candidate_is_inactive_and_references_known_assets() -> None:
    from destiny_personality.semantic_knowledge import (
        load_astrology_methodology_candidates,
        load_semantic_knowledge_claim_registry,
        load_semantic_knowledge_source_registry,
    )

    sources = load_semantic_knowledge_source_registry(KNOWLEDGE_ROOT)
    claims = load_semantic_knowledge_claim_registry(KNOWLEDGE_ROOT, sources)
    candidates = load_astrology_methodology_candidates(KNOWLEDGE_ROOT, sources, claims)

    assert len(candidates) == 1
    assert candidates[0]["methodology_candidate_id"] == "AMC-AS-P004-HELLENISTIC-NATAL-V1"
    assert candidates[0]["review_status"] == "proposed"


def test_claim_with_unknown_source_reference_is_rejected(tmp_path: Path) -> None:
    from destiny_personality.config_errors import ConfigError
    from destiny_personality.semantic_knowledge import load_semantic_knowledge_claim_registry

    (tmp_path / "semantic_knowledge_claim_contract_v1.yaml").write_text(
        """schema_version: semantic-knowledge-claim-v1
required_claim_fields: [claim_id, system, citations, related_claims, tradition_or_school, canonical_fact_family, semantic_claim, target_primitive_id, target_primitive_question, p004_relevance, direction_relevance, scope, contexts, conditions, counter_conditions, exclusions, support_class, limitations, review_status]
allowed_review_statuses: [proposed]
allowed_support_classes: [AMBIGUOUS]
allowed_p004_relevance: [NOT_P004]
allowed_relation_types: [limits]
allowed_citation_support_roles: [primary]
""",
        encoding="utf-8",
    )
    (tmp_path / "semantic_knowledge_claim_registry_v1.yaml").write_text(
        """schema_version: semantic-knowledge-claim-registry-v1
registry_version: test
review_status: candidate_only
activation_status: inactive
claims:
  - claim_id: SKC-TEST
    system: bazi
    citations: [{source_ref: SK-MISSING, locator: chapter, support_role: primary}]
    related_claims: []
    tradition_or_school: test
    canonical_fact_family: deterministic_facts.bazi.ten_gods
    semantic_claim: Test only.
    target_primitive_id: P004
    target_primitive_question: When and how is concrete action started and advanced?
    p004_relevance: NOT_P004
    direction_relevance: none
    scope: none
    contexts: []
    conditions: []
    counter_conditions: []
    exclusions: []
    support_class: AMBIGUOUS
    limitations: []
    review_status: proposed
""",
        encoding="utf-8",
    )

    with pytest.raises(ConfigError, match="unknown source"):
        load_semantic_knowledge_claim_registry(tmp_path, ())


def test_claim_relations_and_citations_fail_closed(tmp_path: Path) -> None:
    from destiny_personality.config_errors import ConfigError
    from destiny_personality.semantic_knowledge import load_semantic_knowledge_claim_registry

    (tmp_path / "semantic_knowledge_claim_contract_v1.yaml").write_text(
        """schema_version: semantic-knowledge-claim-v1
required_claim_fields: [claim_id, system, citations, related_claims, tradition_or_school, canonical_fact_family, semantic_claim, target_primitive_id, target_primitive_question, p004_relevance, direction_relevance, scope, contexts, conditions, counter_conditions, exclusions, support_class, limitations, review_status]
allowed_review_statuses: [proposed]
allowed_support_classes: [AMBIGUOUS]
allowed_p004_relevance: [NOT_P004]
allowed_relation_types: [limits]
allowed_citation_support_roles: [primary]
""",
        encoding="utf-8",
    )
    (tmp_path / "semantic_knowledge_claim_registry_v1.yaml").write_text(
        """schema_version: semantic-knowledge-claim-registry-v1
registry_version: test
review_status: candidate_only
activation_status: inactive
claims:
  - claim_id: SKC-TEST
    system: bazi
    citations: [{source_ref: SK-ONE, locator: section 1, support_role: primary}]
    related_claims: [{claim_ref: SKC-TEST, relation: limits}]
    tradition_or_school: test
    canonical_fact_family: deterministic_facts.bazi.ten_gods
    semantic_claim: Test only.
    target_primitive_id: P004
    target_primitive_question: When and how is concrete action started and advanced?
    p004_relevance: NOT_P004
    direction_relevance: none
    scope: none
    contexts: []
    conditions: []
    counter_conditions: []
    exclusions: []
    support_class: AMBIGUOUS
    limitations: []
    review_status: proposed
""",
        encoding="utf-8",
    )
    sources = ({"source_id": "SK-ONE"},)

    with pytest.raises(ConfigError, match="self relation"):
        load_semantic_knowledge_claim_registry(tmp_path, sources)
