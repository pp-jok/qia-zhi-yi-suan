from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
KNOWLEDGE_ROOT = PROJECT_ROOT / "candidates" / "semantic-knowledge-v1"


def test_loads_candidate_only_p004_semantic_knowledge_registries() -> None:
    from destiny_personality.semantic_knowledge import (
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
        "SK-PROJECT-P004-ONTOLOGY-V2",
    }
    assert {claim["claim_id"] for claim in claims} == {
        "SKC-BZ-TEN-GODS-STRUCTURAL-ONLY-P004-V1",
        "SKC-AS-MARS-ACTION-INITIATIVE-P004-V1",
        "SKC-AS-ASPECT-TECHNIQUE-DISPUTE-P004-V1",
    }


def test_claim_with_unknown_source_reference_is_rejected(tmp_path: Path) -> None:
    from destiny_personality.config_errors import ConfigError
    from destiny_personality.semantic_knowledge import load_semantic_knowledge_claim_registry

    (tmp_path / "semantic_knowledge_claim_contract_v1.yaml").write_text(
        """schema_version: semantic-knowledge-claim-v1
required_claim_fields: [claim_id, system, source_refs, source_locators, tradition_or_school, canonical_fact_family, semantic_claim, target_primitive_id, target_primitive_question, p004_relevance, direction_relevance, scope, contexts, conditions, counter_conditions, exclusions, support_class, conflicting_claim_refs, limitations, review_status]
allowed_review_statuses: [proposed]
allowed_support_classes: [AMBIGUOUS]
allowed_p004_relevance: [NOT_P004]
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
    source_refs: [SK-MISSING]
    source_locators: [chapter]
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
    conflicting_claim_refs: []
    limitations: []
    review_status: proposed
""",
        encoding="utf-8",
    )

    with pytest.raises(ConfigError, match="unknown source"):
        load_semantic_knowledge_claim_registry(tmp_path, ())
