from pathlib import Path

import yaml


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CANDIDATE_ROOT = PROJECT_ROOT / "candidates" / "core-profile-v2"
ONTOLOGY_PATH = CANDIDATE_ROOT / "primitive_ontology_v2.yaml"
POLICY_PATH = CANDIDATE_ROOT / "context_promotion_policy_v1.yaml"
EXPECTED_IDS = {"P001", "P002", "P003", "P004", "P005", "P006"}
REQUIRED_PRIMITIVE_FIELDS = {
    "primitive_id",
    "canonical_name",
    "canonical_definition",
    "semantic_question",
    "high_definition",
    "low_definition",
    "mixed_definition",
    "unknown_definition",
    "included_meanings",
    "excluded_meanings",
    "neighbor_primitives",
    "neighbor_boundaries",
    "valid_contexts",
    "invalid_contexts",
    "global_promotion_eligibility",
    "context_promotion_policy_ref",
    "counter_evidence_semantics",
    "non_evidence_semantics",
    "limitations",
}


def _load(path: Path) -> dict:
    with path.open(encoding="utf-8") as stream:
        return yaml.safe_load(stream)


def _primitive_by_id(ontology: dict, primitive_id: str) -> dict:
    return next(item for item in ontology["primitives"] if item["primitive_id"] == primitive_id)


def test_candidate_ontology_has_exactly_six_complete_unique_primitives() -> None:
    ontology = _load(ONTOLOGY_PATH)

    assert ontology["review_status"] == "approved_candidate"
    assert ontology["schema_version"] == "candidate-primitive-ontology-v2"
    assert ontology["ontology_version"] == "candidate-c1-v2"
    assert len(ontology["primitives"]) == 6
    assert {item["primitive_id"] for item in ontology["primitives"]} == EXPECTED_IDS
    assert len({item["primitive_id"] for item in ontology["primitives"]}) == 6

    for primitive in ontology["primitives"]:
        assert REQUIRED_PRIMITIVE_FIELDS <= primitive.keys()
        assert all(primitive[field] for field in REQUIRED_PRIMITIVE_FIELDS if field not in {"neighbor_primitives", "invalid_contexts"})
        assert primitive["high_definition"] != primitive["low_definition"]
        assert primitive["primitive_id"] not in primitive["neighbor_primitives"]
        assert set(primitive["neighbor_primitives"]) <= EXPECTED_IDS
        assert set(primitive["neighbor_boundaries"]) == set(primitive["neighbor_primitives"])
        assert primitive["context_promotion_policy_ref"] == "context_promotion_policy_v1"


def test_p001_p004_boundary() -> None:
    ontology = _load(ONTOLOGY_PATH)
    p001 = _primitive_by_id(ontology, "P001")
    p004 = _primitive_by_id(ontology, "P004")

    assert "action initiation" in p001["excluded_meanings"]
    assert "judgement ownership" in p004["excluded_meanings"]
    assert "judgement standards" in p001["included_meanings"]
    assert "action initiation" in p004["included_meanings"]


def test_p002_p006_boundary() -> None:
    ontology = _load(ONTOLOGY_PATH)
    p002 = _primitive_by_id(ontology, "P002")
    p006 = _primitive_by_id(ontology, "P006")

    assert "organizational method" in p002["excluded_meanings"]
    assert "predictability preference" in p006["excluded_meanings"]


def test_p003_p001_boundary() -> None:
    ontology = _load(ONTOLOGY_PATH)
    p001 = _primitive_by_id(ontology, "P001")
    p003 = _primitive_by_id(ontology, "P003")

    assert "relational responsiveness" in p001["excluded_meanings"]
    assert "judgement ownership" in p003["excluded_meanings"]
    assert "does not infer lower relational responsiveness" in p001["neighbor_boundaries"]["P003"]
    assert "does not infer lower judgement ownership" in p003["neighbor_boundaries"]["P001"]


def test_context_promotion_policy_encodes_approved_candidate_contract() -> None:
    policy = _load(POLICY_PATH)

    assert policy["review_status"] == "approved_candidate"
    assert policy["schema_version"] == "candidate-context-promotion-policy-v1"
    assert policy["outputs"] == ["global_candidate_evidence", "contextual_variation"]
    assert policy["explicit_global_evidence"]["can_create"] == "global_candidate_evidence"
    assert policy["multi_context_minimum"]["independent_context_count"] == 2
    assert policy["multi_context_minimum"]["same_direction_required"] is True
    assert policy["context_independence"]["two_labels_are_independent_contexts"] is False
    assert policy["evidence_root_independence"]["duplicate_canonical_fact_can_count_twice"] is False
    assert policy["material_counter_context"]["blocks_global_promotion"] is True
    assert policy["contextual_variation"]["opposite_local_directions_create_global_mixed"] is False
    assert policy["global_mixed_scope_rule"]["requires_global_scope_evidence"] is True
    assert policy["state_resolution_boundary"]["promotion_resolves_primitive_state"] is False


def test_context_policy_declares_every_required_boundary_scenario() -> None:
    policy = _load(POLICY_PATH)
    scenarios = policy["verification_scenarios"]

    assert scenarios["single_context_does_not_promote"] == "contextual_variation"
    assert scenarios["duplicate_fact_root_does_not_count_as_independent_context"] == "contextual_variation"
    assert scenarios["two_independent_same_direction_contexts_create_global_candidate"] == "global_candidate_evidence"
    assert scenarios["material_counter_context_blocks_promotion"] == "contextual_variation"
    assert scenarios["opposite_local_contexts_remain_contextual_variation"] == "contextual_variation"
    assert scenarios["local_conflict_does_not_create_global_mixed"] == "contextual_variation"
    assert scenarios["explicit_global_evidence_can_create_global_candidate"] == "global_candidate_evidence"


def test_v2_candidate_assets_are_not_runtime_or_fingerprint_inputs() -> None:
    from destiny_personality.candidate_assets import candidate_asset_root
    from destiny_personality.semantic_fingerprint import CANDIDATE_FILES

    assert candidate_asset_root().name == "core-profile-v1"
    assert "primitive_ontology_v2.yaml" not in CANDIDATE_FILES
    assert "context_promotion_policy_v1.yaml" not in CANDIDATE_FILES
