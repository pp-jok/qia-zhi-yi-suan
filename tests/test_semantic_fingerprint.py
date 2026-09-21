import hashlib
from pathlib import Path

import pytest

from destiny_personality import ConfigError
from destiny_personality.semantic_fingerprint import (
    build_semantic_bundle_fingerprint,
)


RUNTIME_FILES = (
    "bazi_methodology_v1.yaml",
    "astrology_methodology_v1.yaml",
    "score_model_v2_2.yaml",
    "primitive_relation_graph_v1.yaml",
)
CANDIDATE_FILES = (
    "primitive_ontology_v1.yaml",
    "primitive_state_resolution_v1.yaml",
    "bazi_mapping_registry_v1.yaml",
    "astrology_mapping_registry_v1.yaml",
    "dimension_coverage_policy_v1.yaml",
    "narrative_rules_v1.yaml",
)


def write_fingerprint_inputs(
    runtime_dir: Path, candidate_dir: Path
) -> dict:
    expected = {}
    for directory, scope, filenames in (
        (runtime_dir, "runtime", RUNTIME_FILES),
        (candidate_dir, "candidate", CANDIDATE_FILES),
    ):
        directory.mkdir()
        for index, filename in enumerate(filenames):
            content = f"{scope}:{index}:{filename}\n".encode("utf-8")
            (directory / filename).write_bytes(content)
            expected[f"{scope}/{filename}"] = hashlib.sha256(content).hexdigest()
    return expected


def test_builds_raw_file_digests_and_canonical_bundle_digest(
    tmp_path: Path,
) -> None:
    runtime_dir = tmp_path / "runtime"
    candidate_dir = tmp_path / "candidate"
    expected_files = write_fingerprint_inputs(runtime_dir, candidate_dir)

    result = build_semantic_bundle_fingerprint(candidate_dir, runtime_dir)

    canonical = "".join(
        f"{key}:{expected_files[key]}\n" for key in sorted(expected_files)
    ).encode("utf-8")
    assert result == {
        "algorithm": "sha256",
        "bundle_sha256": hashlib.sha256(canonical).hexdigest(),
        "files": {key: expected_files[key] for key in sorted(expected_files)},
    }


def test_missing_fingerprint_input_is_config_gap(tmp_path: Path) -> None:
    runtime_dir = tmp_path / "runtime"
    candidate_dir = tmp_path / "candidate"
    write_fingerprint_inputs(runtime_dir, candidate_dir)
    missing = candidate_dir / "narrative_rules_v1.yaml"
    missing.unlink()

    with pytest.raises(ConfigError) as error:
        build_semantic_bundle_fingerprint(candidate_dir, runtime_dir)

    assert error.value.code == "CONFIG_GAP"
    assert error.value.file == "narrative_rules_v1.yaml"
    assert error.value.field is None


def test_unreadable_fingerprint_input_is_parse_error(
    tmp_path: Path, monkeypatch
) -> None:
    runtime_dir = tmp_path / "runtime"
    candidate_dir = tmp_path / "candidate"
    write_fingerprint_inputs(runtime_dir, candidate_dir)
    original_read_bytes = Path.read_bytes

    def fail_one_file(path: Path) -> bytes:
        if path.name == "narrative_rules_v1.yaml":
            raise PermissionError("TEST_ONLY_DENIED")
        return original_read_bytes(path)

    monkeypatch.setattr(Path, "read_bytes", fail_one_file)

    with pytest.raises(ConfigError) as error:
        build_semantic_bundle_fingerprint(candidate_dir, runtime_dir)

    assert error.value.code == "CONFIG_PARSE_ERROR"
    assert error.value.file == "narrative_rules_v1.yaml"
    assert error.value.field is None

