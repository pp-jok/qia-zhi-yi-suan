from pathlib import Path

import yaml


def test_d1_candidate_assets_are_present_and_not_production_configs() -> None:
    project_root = Path(__file__).resolve().parents[1]
    candidate_root = project_root / "candidates" / "core-profile-v1"
    production_root = project_root / "destiny-personality" / "configs"

    for filename in (
        "primitive_ontology_v1.yaml",
        "primitive_state_resolution_v1.yaml",
        "bazi_mapping_registry_v1.yaml",
        "bazi_day_master_environment_v1.yaml",
        "astrology_mapping_registry_v1.yaml",
        "primitive_relation_graph_v2.yaml",
        "score_model_v2_3.yaml",
        "core_profile_calibration_policy_v2.yaml",
        "signature_formation_policy_v1.yaml",
        "dynamic_formation_policy_v1.yaml",
        "derived_theme_policy_v1.yaml",
    ):
        text = (candidate_root / filename).read_text(encoding="utf-8")
        assert "review_status: approved" in text
        assert not (production_root / filename).exists()


def test_d1_design_set_contains_only_the_eight_anonymous_calibration_cases() -> None:
    project_root = Path(__file__).resolve().parents[1]
    design_set = project_root / "tests" / "fixtures" / "core_profile_calibration" / "design_set"

    assert {path.stem for path in design_set.glob("*.yaml")} == {
        "high_autonomy_high_change",
        "high_stability_low_change",
        "high_affiliation_low_autonomy",
        "high_action_low_reflection",
        "high_affect_low_structure",
        "high_rules_responsibility",
        "cross_system_tension",
        "unknown_birth_time",
    }
    assert all("reader_facing_text" not in path.read_text(encoding="utf-8") for path in design_set.glob("*.yaml"))


def test_candidate_semantic_bundle_fingerprint_is_stable_and_auditable() -> None:
    from destiny_personality.core_profile_builder import candidate_semantic_bundle_fingerprint

    first = candidate_semantic_bundle_fingerprint()
    second = candidate_semantic_bundle_fingerprint()

    assert first == second
    assert len(first) == 64
    assert set(first) <= set("0123456789abcdef")


def test_c4b_candidate_policy_is_bound_to_the_current_semantic_bundle() -> None:
    from destiny_personality.core_profile_builder import candidate_semantic_bundle_fingerprint

    project_root = Path(__file__).resolve().parents[1]
    policy_path = project_root / "candidates" / "core-profile-v1" / "core_profile_calibration_policy_v2.yaml"
    policy = yaml.safe_load(policy_path.read_text(encoding="utf-8"))

    assert policy["bundle_fingerprint"] == candidate_semantic_bundle_fingerprint()
    assert policy["similarity_weights"]["primitive_state_context_overlap"] == 1.0
    assert policy["contrast_pair_thresholds"]["default_max_similarity"] == 0.75
    assert policy["unsupported_activation_frequency"] == 0
