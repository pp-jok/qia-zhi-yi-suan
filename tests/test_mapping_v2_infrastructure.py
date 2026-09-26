from pathlib import Path


def test_mapping_v2_engine_returns_valid_zero_state_when_no_mapping_eligible_mechanisms() -> None:
    from destiny_personality.mapping_v2 import (
        build_fresh_mapping_candidates,
        compile_mapping_v2_candidate_bundle,
        mapping_v2_candidate_fingerprint,
    )

    candidates = build_fresh_mapping_candidates(())
    bundle = compile_mapping_v2_candidate_bundle(candidates)

    assert candidates == ()
    assert bundle.status == "blocked_by_gate"
    assert bundle.bazi_rules == () and bundle.astrology_rules == ()
    assert len(mapping_v2_candidate_fingerprint(Path(__file__).resolve().parents[1])) == 64


def test_mapping_candidate_requires_approved_mapping_eligible_mechanism() -> None:
    from destiny_personality.mapping_v2 import validate_mapping_candidate

    findings = validate_mapping_candidate(
        {
            "mapping_candidate_id": "MC-TEST",
            "semantic_mechanism_refs": ["SMC-1"],
            "primitive_id": "P004",
            "primitive_question": "When and how is concrete action started and advanced?",
        },
        approved_mapping_eligible_ids=(),
    )

    assert findings == ("APPROVED_MAPPING_ELIGIBLE_MECHANISM_REQUIRED",)


def test_mapping_registry_loader_accepts_future_reviewed_registry(tmp_path: Path) -> None:
    from destiny_personality.mapping_v2 import load_mapping_v2_candidate_registry

    path = tmp_path / "candidates" / "mapping-v2"
    path.mkdir(parents=True)
    (path / "mapping_v2_candidate_registry_v1.yaml").write_text(
        "schema_version: mapping-v2-candidate-registry-v1\nreview_status: approved\ncandidates: []\n",
        encoding="utf-8",
    )
    assert load_mapping_v2_candidate_registry(tmp_path).review_status == "approved"


def test_mapping_proposals_are_loaded_and_validated_without_auto_approval(tmp_path: Path) -> None:
    from destiny_personality.mapping_v2 import load_mapping_proposal_registry, validate_mapping_proposal

    directory = tmp_path / "candidates" / "mapping-v2"
    directory.mkdir(parents=True)
    (directory / "mapping_proposal_registry_v1.yaml").write_text(
        "schema_version: mapping-v2-proposal-registry-v1\nproposals: []\n", encoding="utf-8"
    )
    assert load_mapping_proposal_registry(tmp_path) == ()
    assert "MAPPING_PROPOSAL_REVIEW_REQUIRED" in validate_mapping_proposal(
        {"proposal_id": "P1", "semantic_mechanism_refs": ["SMC-1"], "primitive_id": "P001", "primitive_question": "q", "source_system": "bazi", "review_status": "proposed"},
        {"SMC-1"},
    )


def test_mapping_evaluation_rejects_template_collapse() -> None:
    from destiny_personality.mapping_v2 import run_mapping_v2_calibration

    result = run_mapping_v2_calibration((
        {"mapping_candidate_id": "M1", "primitive_id": "P001", "contexts": ["work"]},
        {"mapping_candidate_id": "M2", "primitive_id": "P001", "contexts": ["work"]},
    ))
    assert result.status == "fail"
    assert "MAPPING_TEMPLATE_COLLAPSE" in result.blockers


def test_reviewed_proposal_becomes_unapproved_mapping_candidate() -> None:
    from destiny_personality.mapping_v2 import build_fresh_mapping_candidates

    proposal = {"proposal_id": "P1", "source_system": "bazi", "canonical_fact_requirements": ["fact:1"], "semantic_mechanism_refs": ["SMC-1"], "primitive_id": "P001", "primitive_question": "q", "proposed_direction": {"state": "supported_high"}, "contexts": ["work"], "modifiers": ["m"], "contextualizers": ["work"], "counterevidence": ["c"], "exclusions": ["e"], "evidence_root_refs": ["ER-1"], "limitations": ["l"], "legacy_similarity": {"status": "none"}, "origin": "author", "review_status": "reviewed"}
    candidate = build_fresh_mapping_candidates((proposal,), {"SMC-1"})[0]
    assert candidate["mapping_candidate_id"] == "P1"
    assert candidate["review_status"] == "candidate"


def test_mapping_calibration_artifact_is_machine_generated_and_binds_dataset() -> None:
    from destiny_personality.mapping_v2 import build_mapping_evaluation_artifact

    artifact = build_mapping_evaluation_artifact("calibration", (), "bundle:test", "f" * 64, ("fixture:design-a",), "policy:test")
    assert artifact["schema_version"] == "semantic-calibration-artifact-v1"
    assert artifact["run_status"] == "blocked_by_gate"
    assert artifact["runner_version"] == "mapping-evaluation-v1"


def test_mapping_evaluation_uses_disjoint_repository_design_and_holdout_datasets(tmp_path: Path) -> None:
    from destiny_personality.mapping_v2 import mapping_evaluation_dataset_refs

    for name in ("design_set", "holdout_set"):
        directory = tmp_path / "tests" / "fixtures" / "core_profile_calibration" / name
        directory.mkdir(parents=True)
        (directory / f"{name}.yaml").write_text(
            "fixture_schema_version: candidate-core-profile-calibration-facts-v1\n"
            f"case_id: {name}\nfact_assurance: capability_reported\nbazi_ten_gods: []\n"
            "astrology:\n  known_birth_time: true\n  aspect_pairs: []\n",
            encoding="utf-8",
        )

    calibration = mapping_evaluation_dataset_refs(tmp_path, "calibration")
    holdout = mapping_evaluation_dataset_refs(tmp_path, "holdout")

    assert calibration == ("tests/fixtures/core_profile_calibration/design_set/design_set.yaml",)
    assert holdout == ("tests/fixtures/core_profile_calibration/holdout_set/holdout_set.yaml",)
    assert not set(calibration) & set(holdout)


def test_proposal_allows_empty_qualifier_collections_when_required_fields_exist() -> None:
    from destiny_personality.mapping_v2 import validate_mapping_proposal

    proposal = {"proposal_id": "P1", "source_system": "bazi", "canonical_fact_requirements": ["fact:1"], "semantic_mechanism_refs": ["SMC-1"], "primitive_id": "P001", "primitive_question": "q", "proposed_direction": {"state": "supported_high"}, "contexts": ["work"], "modifiers": [], "contextualizers": [], "counterevidence": [], "exclusions": [], "evidence_root_refs": ["ER-1"], "limitations": ["l"], "legacy_similarity": {"status": "none"}, "origin": "author", "review_status": "reviewed"}
    assert validate_mapping_proposal(proposal, {"SMC-1"}) == ()
