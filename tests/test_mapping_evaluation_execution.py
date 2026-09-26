from pathlib import Path

import pytest


def _write_fixture(path: Path, case_id: str, *, gods=(), aspects=(), known_birth_time=True, expected_states=None) -> None:
    expected = "" if expected_states is None else "expected_states:\n" + "\n".join(
        f"  {primitive}: {states}" for primitive, states in expected_states.items()
    ) + "\n"
    path.write_text(
        "fixture_schema_version: candidate-core-profile-calibration-facts-v1\n"
        f"case_id: {case_id}\n"
        "fact_assurance: capability_reported\n"
        f"bazi_ten_gods: {list(gods)}\n"
        "astrology:\n"
        f"  known_birth_time: {str(known_birth_time).lower()}\n"
        f"  aspect_pairs: {list(map(list, aspects))}\n"
        + expected,
        encoding="utf-8",
    )


def _dataset_root(tmp_path: Path) -> Path:
    root = tmp_path / "tests" / "fixtures" / "core_profile_calibration"
    (root / "design_set").mkdir(parents=True)
    (root / "holdout_set").mkdir()
    return tmp_path


def test_loader_normalizes_v1_fixture_and_fingerprints_content(tmp_path: Path) -> None:
    from destiny_personality.mapping_evaluation import load_mapping_evaluation_fixture

    path = tmp_path / "case.yaml"
    _write_fixture(path, "case-a", gods=("比肩",), aspects=(("Sun", "Mars"),))
    fixture = load_mapping_evaluation_fixture(path)

    assert fixture.fixture_id == "case-a"
    assert "bazi.ten_god:比肩" in fixture.input_tokens
    assert "astrology.aspect:Mars:Sun" in fixture.input_tokens
    assert fixture.content_fingerprint == load_mapping_evaluation_fixture(path).content_fingerprint


def test_loader_fails_closed_for_invalid_schema_and_missing_fields(tmp_path: Path) -> None:
    from destiny_personality.mapping_evaluation import load_mapping_evaluation_fixture

    invalid = tmp_path / "invalid.yaml"
    invalid.write_text("fixture_schema_version: unknown\ncase_id: x\n", encoding="utf-8")
    with pytest.raises(ValueError, match="MAPPING_EVALUATION_FIXTURE_INVALID"):
        load_mapping_evaluation_fixture(invalid)


def test_dataset_rejects_duplicate_ids_and_cross_set_content_overlap(tmp_path: Path) -> None:
    from destiny_personality.mapping_evaluation import load_mapping_evaluation_datasets

    root = _dataset_root(tmp_path)
    design = root / "tests" / "fixtures" / "core_profile_calibration" / "design_set"
    holdout = root / "tests" / "fixtures" / "core_profile_calibration" / "holdout_set"
    _write_fixture(design / "one.yaml", "same")
    _write_fixture(design / "two.yaml", "same", gods=("食神",))
    _write_fixture(holdout / "holdout.yaml", "holdout")
    with pytest.raises(ValueError, match="MAPPING_EVALUATION_FIXTURE_ID_DUPLICATE"):
        load_mapping_evaluation_datasets(root)
    (design / "two.yaml").unlink()
    (holdout / "holdout.yaml").unlink()
    (holdout / "copy.yaml").write_text((design / "one.yaml").read_text(encoding="utf-8"), encoding="utf-8")
    with pytest.raises(ValueError, match="MAPPING_EVALUATION_DATASET_CONTENT_OVERLAP"):
        load_mapping_evaluation_datasets(root)


def test_dataset_fingerprint_changes_when_fixture_content_changes(tmp_path: Path) -> None:
    from destiny_personality.mapping_evaluation import load_mapping_evaluation_datasets

    root = _dataset_root(tmp_path)
    design = root / "tests" / "fixtures" / "core_profile_calibration" / "design_set"
    holdout = root / "tests" / "fixtures" / "core_profile_calibration" / "holdout_set"
    _write_fixture(design / "design.yaml", "design", gods=("比肩",))
    _write_fixture(holdout / "holdout.yaml", "holdout", gods=("食神",))
    first = load_mapping_evaluation_datasets(root)["calibration"].fingerprint
    _write_fixture(design / "design.yaml", "design", gods=("正官",))
    assert load_mapping_evaluation_datasets(root)["calibration"].fingerprint != first


def test_runner_executes_unknown_mixed_and_context_differentiated_cases(tmp_path: Path) -> None:
    from destiny_personality.mapping_evaluation import execute_mapping_evaluation, load_mapping_evaluation_datasets

    root = _dataset_root(tmp_path)
    design = root / "tests" / "fixtures" / "core_profile_calibration" / "design_set"
    holdout = root / "tests" / "fixtures" / "core_profile_calibration" / "holdout_set"
    _write_fixture(design / "unknown.yaml", "unknown", gods=("比肩",), expected_states={"P1": "unknown"})
    _write_fixture(design / "mixed.yaml", "mixed", gods=("食神",), expected_states={"P2": "mixed"})
    _write_fixture(design / "context.yaml", "context", gods=("正官",), expected_states={"P3": "context_differentiated"})
    _write_fixture(holdout / "holdout.yaml", "holdout", gods=("偏财",))
    mappings = (
        {"mapping_candidate_id": "U", "primitive_id": "P1", "canonical_fact_requirements": ["bazi.ten_god:比肩"], "proposed_direction": {"state": "unknown"}, "contexts": ["work"]},
        {"mapping_candidate_id": "M1", "primitive_id": "P2", "canonical_fact_requirements": ["bazi.ten_god:食神"], "proposed_direction": {"state": "supported_high"}, "contexts": ["work"]},
        {"mapping_candidate_id": "M2", "primitive_id": "P2", "canonical_fact_requirements": ["bazi.ten_god:食神"], "proposed_direction": {"state": "supported_low"}, "contexts": ["work"]},
        {"mapping_candidate_id": "C1", "primitive_id": "P3", "canonical_fact_requirements": ["bazi.ten_god:正官"], "proposed_direction": {"state": "supported_high"}, "contexts": ["work"]},
        {"mapping_candidate_id": "C2", "primitive_id": "P3", "canonical_fact_requirements": ["bazi.ten_god:正官"], "proposed_direction": {"state": "supported_low"}, "contexts": ["relationship"]},
    )

    result = execute_mapping_evaluation("calibration", mappings, load_mapping_evaluation_datasets(root)["calibration"])

    assert result.status == "pass"
    assert result.metrics["unknown_count"] == 1
    assert result.metrics["mixed_count"] == 1
    assert result.metrics["context_differentiated_count"] == 1
    assert result.metrics["determinism_failure_count"] == 0


def test_runner_reports_unexpected_state_and_observed_template_collapse(tmp_path: Path) -> None:
    from destiny_personality.mapping_evaluation import execute_mapping_evaluation, load_mapping_evaluation_datasets

    root = _dataset_root(tmp_path)
    design = root / "tests" / "fixtures" / "core_profile_calibration" / "design_set"
    holdout = root / "tests" / "fixtures" / "core_profile_calibration" / "holdout_set"
    _write_fixture(design / "one.yaml", "one", gods=("比肩",), expected_states={"P1": "supported_low"})
    _write_fixture(design / "two.yaml", "two", gods=("正官",), expected_states={"P1": "supported_low"})
    _write_fixture(holdout / "holdout.yaml", "holdout", gods=("食神",))
    mappings = ({"mapping_candidate_id": "M", "primitive_id": "P1", "canonical_fact_requirements": [], "proposed_direction": {"state": "supported_high"}, "contexts": ["work"]},)

    result = execute_mapping_evaluation("calibration", mappings, load_mapping_evaluation_datasets(root)["calibration"])

    assert result.status == "fail"
    assert result.metrics["unexpected_state_count"] == 2
    assert result.metrics["template_collapse_count"] == 1


def test_artifact_binds_executed_dataset_and_has_deterministic_input_fingerprint(tmp_path: Path) -> None:
    from destiny_personality.mapping_evaluation import execute_mapping_evaluation, load_mapping_evaluation_datasets
    from destiny_personality.mapping_v2 import build_mapping_evaluation_artifact, validate_mapping_evaluation_artifact

    root = _dataset_root(tmp_path)
    design = root / "tests" / "fixtures" / "core_profile_calibration" / "design_set"
    holdout = root / "tests" / "fixtures" / "core_profile_calibration" / "holdout_set"
    _write_fixture(design / "design.yaml", "design", gods=("比肩",), expected_states={"P1": "supported_high"})
    _write_fixture(holdout / "holdout.yaml", "holdout", gods=("食神",))
    dataset = load_mapping_evaluation_datasets(root)["calibration"]
    bundle = ({"mapping_candidate_id": "M", "primitive_id": "P1", "canonical_fact_requirements": ["bazi.ten_god:比肩"], "proposed_direction": {"state": "supported_high"}, "contexts": ["work"]},)
    run = execute_mapping_evaluation("calibration", bundle, dataset)

    first = build_mapping_evaluation_artifact("calibration", bundle, "bundle:test", "f" * 64, dataset.refs, "policy:test", dataset.fingerprint, run)
    second = build_mapping_evaluation_artifact("calibration", bundle, "bundle:test", "f" * 64, dataset.refs, "policy:test", dataset.fingerprint, run)

    assert first["run_status"] == "pass"
    assert first["dataset_fingerprint"] == dataset.fingerprint
    assert first["evaluation_input_fingerprint"] == second["evaluation_input_fingerprint"]
    assert validate_mapping_evaluation_artifact("calibration", first) is None


def test_artifact_validation_rejects_tampered_fingerprint_and_unknown_runner() -> None:
    from destiny_personality.mapping_v2 import build_mapping_evaluation_artifact, validate_mapping_evaluation_artifact

    artifact = build_mapping_evaluation_artifact("holdout", (), "bundle:test", "f" * 64, ("fixture:holdout",), "policy:test")
    forged = {**artifact, "run_status": "pass", "dataset_fingerprint": "a" * 64, "evaluation_input_fingerprint": "b" * 64, "artifact_fingerprint": "c" * 64}
    with pytest.raises(ValueError, match="EVALUATION_ARTIFACT_FINGERPRINT_INVALID"):
        validate_mapping_evaluation_artifact("holdout", forged)
    with pytest.raises(ValueError, match="EVALUATION_ARTIFACT_RUNNER_INVALID"):
        validate_mapping_evaluation_artifact("holdout", {**artifact, "runner_version": "unknown"})
