import hashlib
from pathlib import Path

import pytest

from destiny_personality import ConfigError
from destiny_personality.calculation_fingerprint import (
    build_calculation_bundle_fingerprint,
)


RUNTIME_FILES = (
    "bazi_methodology_v1.yaml",
    "astrology_methodology_v1.yaml",
    "score_model_v2_2.yaml",
    "primitive_relation_graph_v1.yaml",
)
CANDIDATE_FILES = (
    "canonical_fact_vocabulary_v1.yaml",
    "bazi_deterministic_tables_v1.yaml",
    "astrology_dignity_table_v1.yaml",
    "astrology_node_policy_v1.yaml",
    "fact_comparison_policy_v1.yaml",
)


def _write_inputs(runtime_dir: Path, candidate_dir: Path) -> dict:
    expected = {}
    for directory, scope, filenames in (
        (runtime_dir, "runtime", RUNTIME_FILES),
        (candidate_dir, "candidate", CANDIDATE_FILES),
    ):
        directory.mkdir()
        for index, filename in enumerate(filenames):
            content = f"{scope}:{index}:{filename}\n".encode()
            (directory / filename).write_bytes(content)
            expected[f"{scope}/{filename}"] = hashlib.sha256(content).hexdigest()
    return expected


def test_builds_nine_raw_digests_and_canonical_calculation_digest(tmp_path) -> None:
    runtime_dir = tmp_path / "runtime"
    candidate_dir = tmp_path / "candidate"
    expected = _write_inputs(runtime_dir, candidate_dir)

    result = build_calculation_bundle_fingerprint(candidate_dir, runtime_dir)

    canonical = "".join(
        f"{key}:{expected[key]}\n" for key in sorted(expected)
    ).encode()
    assert result == {
        "algorithm": "sha256",
        "bundle_sha256": hashlib.sha256(canonical).hexdigest(),
        "files": {key: expected[key] for key in sorted(expected)},
    }
    assert len(result["files"]) == 9


def test_missing_calculation_fingerprint_input_is_config_gap(tmp_path) -> None:
    runtime_dir = tmp_path / "runtime"
    candidate_dir = tmp_path / "candidate"
    _write_inputs(runtime_dir, candidate_dir)
    (candidate_dir / "astrology_node_policy_v1.yaml").unlink()

    with pytest.raises(ConfigError) as error:
        build_calculation_bundle_fingerprint(candidate_dir, runtime_dir)

    assert (error.value.code, error.value.file, error.value.field) == (
        "CONFIG_GAP", "astrology_node_policy_v1.yaml", None
    )
