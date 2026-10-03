from pathlib import Path
import shutil
from typing import Optional

import pytest
import yaml


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
        "SK-BZ-YUANHAI-ZIPING-PROCESS-P004-V1",
        "SK-BZ-SANMING-TONGHUI-DAO-SHI-P004-V1",
        "SK-AS-MARS-HOULDING-2004",
        "SK-AS-ASPECTS-HOULDING-2004",
        "SK-AS-HELLENISTIC-GEORGE-2019-2022",
        "SK-AS-DIGNITY-HOULDING",
        "SK-AS-NATAL-ASPECTS-CAMPION-2003",
        "SK-AS-PSYCHOLOGICAL-CPA",
        "SK-AS-HORARY-APPLICATION-SKYSCRIPT",
        "SK-AS-HORARY-PERFECTION-SKYSCRIPT",
        "SK-PROJECT-P004-ONTOLOGY-V2",
    }
    assert {claim["claim_id"] for claim in claims} == {
        "SKC-BZ-TEN-GODS-STRUCTURAL-ONLY-P004-V1",
        "SKC-BZ-DAO-SHI-ADVANCEMENT-LIMIT-P004-V1",
        "SKC-AS-MARS-ACTION-INITIATIVE-P004-V1",
        "SKC-AS-ASPECT-TECHNIQUE-DISPUTE-P004-V1",
        "SKC-AS-HELLENISTIC-NATAL-CONDITION-V1",
        "SKC-AS-DIGNITY-CONDITION-NOT-DIRECTION-P004-V1",
        "SKC-AS-NATAL-ASPECTS-QUALIFY-NOT-DIRECT-P004-V1",
        "SKC-AS-HELLENISTIC-CONDITION-INVENTORY-P004-V1",
        "SKC-AS-PSYCHOLOGICAL-METHOD-BOUNDARY-P004-V1",
        "SKC-AS-HORARY-EVENT-BOUNDARY-P004-V1",
        "SKC-PROJECT-P004-CONDITION-NOT-DIRECTION-V1",
    }
    audit = build_semantic_knowledge_audit(sources, claims)
    assert audit["source_quality_distribution"] == {"TIER_A": 3, "TIER_B": 9, "TIER_C": 1}
    assert audit["direct_p004_claim_count"] == 2
    assert audit["school_specific_direct_claim_count"] == 2


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
    assert candidates[0]["review_status"] == "approved_for_semantic_design"
    assert candidates[0]["product_owner_decision_ref"] == (
        "PO-P004-D3-HELLENISTIC-METHOD-2026-09-30"
    )
    assert candidates[0]["candidate_validation_status"] == "READY_FOR_PO_REVIEW"
    assert candidates[0]["product_owner_selection_status"] == (
        "SELECTED_FOR_SEMANTIC_DESIGN"
    )


def test_methodology_evidence_roles_are_separated_and_materiality_is_explicit() -> None:
    from destiny_personality.semantic_knowledge import (
        load_astrology_methodology_candidates,
        load_semantic_knowledge_claim_registry,
        load_semantic_knowledge_source_registry,
    )

    sources = load_semantic_knowledge_source_registry(KNOWLEDGE_ROOT)
    claims = load_semantic_knowledge_claim_registry(KNOWLEDGE_ROOT, sources)
    candidate = load_astrology_methodology_candidates(KNOWLEDGE_ROOT, sources, claims)[0]

    assert candidate["method_authority_source_refs"] == ["SK-AS-HELLENISTIC-GEORGE-2019-2022"]
    assert "SK-AS-NATAL-ASPECTS-CAMPION-2003" in candidate["boundary_source_refs"]
    assert candidate["project_boundary_source_refs"] == ["SK-PROJECT-P004-ONTOLOGY-V2"]

    audit = {item["technique"]: item for item in candidate["condition_technique_audit"]}
    assert audit["sect"]["p004_role"] == "UNRESOLVED"
    assert audit["essential dignity"]["p004_role"] == "UNRESOLVED"
    assert audit["house/angularity"]["p004_role"] == "UNRESOLVED"
    assert audit["application/perfection event timing"]["p004_role"] == "NOT_P004"
    assert audit["Mars significator identity"]["p004_role"] == "UNRESOLVED"
    assert audit["sect"]["materiality_basis"]["evidence_class"] == "METHOD_ROLE_ONLY"
    assert audit["Mars significator identity"]["materiality_basis"]["evidence_class"] == "INSUFFICIENT"
    assert (
        audit["application/perfection event timing"]["materiality_basis"]["evidence_class"]
        == "DIRECT_NON_P004_BOUNDARY"
    )
    assert all(item["required_by_p004"] is False for item in audit.values())


def _copy_knowledge_assets(tmp_path: Path) -> Path:
    target = tmp_path / "semantic-knowledge-v1"
    shutil.copytree(KNOWLEDGE_ROOT, target)
    return target


def _rewrite_candidate(root: Path, mutator) -> None:
    path = root / "astrology_methodology_candidate_registry_v1.yaml"
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    mutator(payload["candidates"][0])
    path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")


def _rewrite_bazi_candidate(root: Path, mutator) -> None:
    path = root / "bazi_methodology_candidate_registry_v1.yaml"
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    mutator(payload["candidates"][0])
    path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")


def _load_bazi_candidates(root: Path):
    from destiny_personality.semantic_knowledge import (
        load_bazi_methodology_candidates,
        load_semantic_knowledge_claim_registry,
        load_semantic_knowledge_source_registry,
    )

    sources = load_semantic_knowledge_source_registry(root)
    claims = load_semantic_knowledge_claim_registry(root, sources)
    return load_bazi_methodology_candidates(root, sources, claims)


def test_bazi_methodology_records_source_bound_rule_and_fact_boundary() -> None:
    candidate = _load_bazi_candidates(KNOWLEDGE_ROOT)[0]

    assert candidate["candidate_validation_status"] == "NOT_READY"
    assert candidate["canonical_fact_boundary_status"] == (
        "CANDIDATE_RELATION_PROVIDER_AVAILABLE"
    )
    assert candidate["neutral_relation_fact_status"] == (
        "CANDIDATE_PROVIDER_AVAILABLE_NOT_ACTIVATED"
    )
    assert candidate["evidence_root_status"] == "WITHDRAWN"
    assert candidate["proposed_evidence_root_ref"] is None
    assert len(candidate["method_rule_decomposition"]) == 10
    statuses = {
        item["question"]: item["resolution_status"]
        for item in candidate["method_rule_decomposition"]
    }
    assert set(statuses.values()) == {"PARTIALLY_RESOLVED", "UNRESOLVED"}
    assert statuses["Which Eating God instance is evaluated?"] == (
        "PARTIALLY_RESOLVED"
    )
    assert statuses["How are multiple Eating Gods or Resources handled?"] == (
        "UNRESOLVED"
    )


def test_dao_shi_coexistence_is_not_operational_rule() -> None:
    candidate = _load_bazi_candidates(KNOWLEDGE_ROOT)[0]
    coexistence = candidate["condition_audit"][0]

    assert coexistence["method_role"] == "minimum identity inputs only"
    assert "does not prove" in coexistence["blocker"]
    assert candidate["candidate_validation_status"] == "NOT_READY"


def test_dao_shi_method_requires_source_backed_material_conditions() -> None:
    candidate = _load_bazi_candidates(KNOWLEDGE_ROOT)[0]
    known_sources = set(candidate["method_authority_source_refs"])

    material = [
        item
        for item in candidate["method_rule_decomposition"]
        if item["materiality"] == "MATERIAL"
    ]
    assert material
    assert all(item["source_refs"] for item in material)
    assert all(set(item["source_refs"]).issubset(known_sources) for item in material)
    assert all(item["exact_locator"].strip() for item in material)


def test_dao_shi_unresolved_material_condition_blocks_readiness(tmp_path: Path) -> None:
    from destiny_personality.config_errors import ConfigError

    root = _copy_knowledge_assets(tmp_path)
    _rewrite_bazi_candidate(
        root,
        lambda candidate: candidate.__setitem__(
            "candidate_validation_status", "READY_FOR_PO_REVIEW"
        ),
    )

    with pytest.raises(ConfigError, match="material method conditions are unresolved"):
        _load_bazi_candidates(root)


def test_dao_shi_method_never_supports_low() -> None:
    candidate = _load_bazi_candidates(KNOWLEDGE_ROOT)[0]

    assert "conditional_limits_supported_high" in candidate["direction_semantics"]
    assert "never supports_low" in candidate["direction_semantics"]


def test_dao_shi_candidate_does_not_assert_primitive_state() -> None:
    candidate = _load_bazi_candidates(KNOWLEDGE_ROOT)[0]

    assert "primitive_state" not in candidate
    assert "asserts_primitive_state" not in candidate


@pytest.mark.parametrize(
    ("review_status", "selection_status", "decision_ref", "message"),
    [
        (
            "approved_for_semantic_design",
            "SELECTED_FOR_SEMANTIC_DESIGN",
            None,
            "approved methodology requires non-empty product_owner_decision_ref",
        ),
        (
            "approved_for_semantic_design",
            "PENDING",
            "PO-TEST",
            "approved methodology requires SELECTED_FOR_SEMANTIC_DESIGN",
        ),
        (
            "proposed",
            "SELECTED_FOR_SEMANTIC_DESIGN",
            None,
            "proposed methodology must remain pending",
        ),
        (
            "deferred",
            "SELECTED_FOR_SEMANTIC_DESIGN",
            None,
            "deferred methodology requires DEFERRED",
        ),
        (
            "rejected",
            "SELECTED_FOR_SEMANTIC_DESIGN",
            None,
            "rejected methodology requires REJECTED",
        ),
    ],
)
def test_bazi_methodology_po_provenance_fails_closed(
    tmp_path: Path,
    review_status: str,
    selection_status: str,
    decision_ref: Optional[str],
    message: str,
) -> None:
    from destiny_personality.config_errors import ConfigError

    root = _copy_knowledge_assets(tmp_path)

    def mutate(candidate: dict) -> None:
        candidate["review_status"] = review_status
        candidate["product_owner_selection_status"] = selection_status
        candidate["product_owner_decision_ref"] = decision_ref

    _rewrite_bazi_candidate(root, mutate)

    with pytest.raises(ConfigError, match=message):
        _load_bazi_candidates(root)


def _technique(candidate: dict, name: str) -> dict:
    return next(item for item in candidate["condition_technique_audit"] if item["technique"] == name)


def _load_candidates(root: Path):
    from destiny_personality.semantic_knowledge import (
        load_astrology_methodology_candidates,
        load_semantic_knowledge_claim_registry,
        load_semantic_knowledge_source_registry,
    )

    sources = load_semantic_knowledge_source_registry(root)
    claims = load_semantic_knowledge_claim_registry(root, sources)
    return load_astrology_methodology_candidates(root, sources, claims)


@pytest.mark.parametrize(
    ("field", "replacement", "message"),
    [
        ("method_authority_source_refs", ["SK-MISSING"], "unknown methodology authority source"),
        ("boundary_claim_refs", ["SKC-MISSING"], "unknown methodology boundary claim"),
    ],
)
def test_methodology_role_references_fail_closed(
    tmp_path: Path, field: str, replacement: list[str], message: str
) -> None:
    from destiny_personality.config_errors import ConfigError

    root = _copy_knowledge_assets(tmp_path)
    _rewrite_candidate(root, lambda candidate: candidate.__setitem__(field, replacement))

    with pytest.raises(ConfigError, match=message):
        _load_candidates(root)


def test_cross_school_boundary_source_cannot_become_method_authority(tmp_path: Path) -> None:
    from destiny_personality.config_errors import ConfigError

    root = _copy_knowledge_assets(tmp_path)
    def promote_cross_school_source(candidate: dict) -> None:
        candidate["boundary_source_refs"].remove("SK-AS-NATAL-ASPECTS-CAMPION-2003")
        candidate["method_authority_source_refs"].append("SK-AS-NATAL-ASPECTS-CAMPION-2003")

    _rewrite_candidate(root, promote_cross_school_source)

    with pytest.raises(ConfigError, match="method authority source must match candidate tradition"):
        _load_candidates(root)


def test_method_authority_cannot_overlap_boundary_roles(tmp_path: Path) -> None:
    from destiny_personality.config_errors import ConfigError

    root = _copy_knowledge_assets(tmp_path)
    _rewrite_candidate(
        root,
        lambda candidate: candidate["boundary_source_refs"].append(
            candidate["method_authority_source_refs"][0]
        ),
    )

    with pytest.raises(ConfigError, match="method authority and boundary source roles must be disjoint"):
        _load_candidates(root)


@pytest.mark.parametrize("decision_ref", [None, "", "   "])
def test_approved_methodology_requires_nonempty_po_decision_ref(
    tmp_path: Path, decision_ref: Optional[str]
) -> None:
    from destiny_personality.config_errors import ConfigError

    root = _copy_knowledge_assets(tmp_path)

    def approve(candidate: dict) -> None:
        candidate["review_status"] = "approved_for_semantic_design"
        candidate["product_owner_decision_ref"] = decision_ref
        candidate["product_owner_selection_status"] = "SELECTED_FOR_SEMANTIC_DESIGN"

    _rewrite_candidate(root, approve)

    with pytest.raises(ConfigError, match="approved methodology requires product_owner_decision_ref"):
        _load_candidates(root)


def test_proposed_methodology_cannot_claim_product_owner_selection(tmp_path: Path) -> None:
    from destiny_personality.config_errors import ConfigError

    root = _copy_knowledge_assets(tmp_path)
    def revert_to_invalid_proposed_state(candidate: dict) -> None:
        candidate["review_status"] = "proposed"
        candidate["product_owner_decision_ref"] = None

    _rewrite_candidate(root, revert_to_invalid_proposed_state)

    with pytest.raises(ConfigError, match="proposed methodology must remain pending"):
        _load_candidates(root)


def test_material_p004_role_requires_source_and_claim_evidence(tmp_path: Path) -> None:
    from destiny_personality.config_errors import ConfigError

    root = _copy_knowledge_assets(tmp_path)

    def make_unbacked(candidate: dict) -> None:
        item = _technique(candidate, "sect")
        item["p004_role"] = "P004_MODIFIER"
        item["materiality_basis"]["evidence_class"] = "DIRECT_P004_MATERIALITY"
        item["source_refs"] = []
        item["claim_refs"] = []
        item["materiality_basis"]["source_refs"] = []
        item["materiality_basis"]["claim_refs"] = []

    _rewrite_candidate(root, make_unbacked)

    with pytest.raises(ConfigError, match="P004 material role requires source and claim evidence"):
        _load_candidates(root)


@pytest.mark.parametrize("definitive_role", ["QUALITY_ONLY", "PROMINENCE_ONLY", "NOT_P004"])
def test_method_role_only_does_not_imply_definitive_non_p004_role(
    tmp_path: Path, definitive_role: str
) -> None:
    from destiny_personality.config_errors import ConfigError

    root = _copy_knowledge_assets(tmp_path)

    def collapse_unknown(candidate: dict) -> None:
        _technique(candidate, "sect")["p004_role"] = definitive_role

    _rewrite_candidate(root, collapse_unknown)

    with pytest.raises(ConfigError, match="definitive non-P004 role requires direct boundary evidence"):
        _load_candidates(root)


@pytest.mark.parametrize("material_role", ["P004_REQUIRED", "P004_MODIFIER"])
def test_material_p004_role_requires_direct_materiality_evidence_class(
    tmp_path: Path, material_role: str
) -> None:
    from destiny_personality.config_errors import ConfigError

    root = _copy_knowledge_assets(tmp_path)

    def promote_without_materiality(candidate: dict) -> None:
        _technique(candidate, "sect")["p004_role"] = material_role

    _rewrite_candidate(root, promote_without_materiality)

    with pytest.raises(ConfigError, match="P004 material role requires direct P004 materiality evidence"):
        _load_candidates(root)


def test_definitive_non_p004_requires_candidate_boundary_claim(tmp_path: Path) -> None:
    from destiny_personality.config_errors import ConfigError

    root = _copy_knowledge_assets(tmp_path)

    def replace_boundary(candidate: dict) -> None:
        item = _technique(candidate, "application/perfection event timing")
        authority_claim = "SKC-AS-HELLENISTIC-CONDITION-INVENTORY-P004-V1"
        item["claim_refs"] = [authority_claim]
        item["materiality_basis"]["claim_refs"] = [authority_claim]

    _rewrite_candidate(root, replace_boundary)

    with pytest.raises(ConfigError, match="definitive non-P004 role requires candidate boundary claim"):
        _load_candidates(root)


def test_unresolved_is_valid_and_does_not_block_ready_candidate() -> None:
    candidate = _load_candidates(KNOWLEDGE_ROOT)[0]
    audit = candidate["condition_technique_audit"]

    assert any(item["p004_role"] == "UNRESOLVED" for item in audit)
    assert candidate["candidate_validation_status"] == "READY_FOR_PO_REVIEW"


def test_required_by_method_does_not_imply_required_by_p004() -> None:
    candidate = _load_candidates(KNOWLEDGE_ROOT)[0]
    method_required = [
        item for item in candidate["condition_technique_audit"] if item["required_by_method"]
    ]

    assert method_required
    assert all(item["required_by_p004"] is False for item in method_required)


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
