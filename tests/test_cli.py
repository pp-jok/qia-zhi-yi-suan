import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from destiny_personality import ConfigError
from destiny_personality.cli import main


def test_validate_config_prints_machine_readable_summary(
    valid_config_dir: Path, capsys
) -> None:
    exit_code = main(["validate-config", str(valid_config_dir)])

    output = json.loads(capsys.readouterr().out)
    assert exit_code == 0
    assert output == {
        "astrology_methodology_version": "western-tropical-v1.0",
        "bazi_methodology_version": "bazi-core-v1.0",
        "relation_count": 5,
        "relation_graph_version": "1.0",
        "score_model_version": "2.2",
        "status": "ok",
    }


def test_validate_config_reports_error_and_nonzero_exit(
    tmp_path: Path, capsys
) -> None:
    exit_code = main(["validate-config", str(tmp_path)])

    captured = capsys.readouterr()
    assert exit_code == 2
    assert captured.out == ""
    assert "CONFIG_GAP" in captured.err
    assert "bazi_methodology_v1.yaml" in captured.err


def test_validate_semantic_contracts_loads_explicit_baseline_then_candidate(
    tmp_path: Path, monkeypatch, capsys
) -> None:
    import destiny_personality.cli as cli

    candidate_dir = tmp_path / "candidate"
    runtime_dir = tmp_path / "runtime"
    calls = []
    runtime = SimpleNamespace(
        relation_graph=SimpleNamespace(relations=(object(), object()))
    )
    bundle = SimpleNamespace(
        primitive_foundation=SimpleNamespace(
            ontology=SimpleNamespace(
                ontology_version="TEST_ONLY_ONTOLOGY_V1",
                primitives=(object(), object(), object()),
            ),
            resolution=SimpleNamespace(
                resolution_version="TEST_ONLY_RESOLUTION_V1",
                rules=(object(),),
            ),
        ),
        mapping_registries=SimpleNamespace(
            bazi=SimpleNamespace(
                registry_version="TEST_ONLY_BAZI_REGISTRY_V1",
                rules=(object(), object()),
            ),
            astrology=SimpleNamespace(
                registry_version="TEST_ONLY_ASTROLOGY_REGISTRY_V1",
                rules=(object(),),
            ),
        ),
        dimension_coverage_policy=SimpleNamespace(
            policy_version="TEST_ONLY_DIMENSIONS_V1",
            dimensions=tuple(object() for _ in range(12)),
        ),
        narrative_rules=SimpleNamespace(
            narrative_version="TEST_ONLY_NARRATIVE_V1",
            rules=(object(), object()),
        ),
    )

    def fake_load_runtime(path: Path):
        calls.append(("runtime", path))
        return runtime

    def fake_load_bundle(path: Path, accepted_runtime):
        calls.append(("semantic", path, accepted_runtime))
        return bundle

    fingerprint = {
        "algorithm": "sha256",
        "bundle_sha256": "a" * 64,
        "files": {"candidate/TEST_ONLY.yaml": "b" * 64},
    }

    def fake_fingerprint(candidate: Path, baseline: Path):
        calls.append(("fingerprint", candidate, baseline))
        return fingerprint

    monkeypatch.setattr(cli, "load_runtime_config", fake_load_runtime)
    monkeypatch.setattr(cli, "load_semantic_contract_bundle", fake_load_bundle)
    monkeypatch.setattr(cli, "build_semantic_bundle_fingerprint", fake_fingerprint)

    exit_code = main(
        [
            "validate-semantic-contracts",
            str(candidate_dir),
            "--runtime-config-dir",
            str(runtime_dir),
        ]
    )

    assert exit_code == 0
    assert calls == [
        ("runtime", runtime_dir),
        ("semantic", candidate_dir, runtime),
        ("fingerprint", candidate_dir, runtime_dir),
        ("runtime", runtime_dir),
        ("semantic", candidate_dir, runtime),
        ("fingerprint", candidate_dir, runtime_dir),
    ]
    assert json.loads(capsys.readouterr().out) == {
        "command": "validate-semantic-contracts",
        "counts": {
            "astrology_mapping_rules": 1,
            "bazi_mapping_rules": 2,
            "dimensions": 12,
            "narrative_rules": 2,
            "primitives": 3,
            "relation_graph_relations": 2,
            "state_rules": 1,
        },
        "fingerprint": fingerprint,
        "status": "ok",
        "versions": {
            "astrology_registry": "TEST_ONLY_ASTROLOGY_REGISTRY_V1",
            "bazi_registry": "TEST_ONLY_BAZI_REGISTRY_V1",
            "dimension_policy": "TEST_ONLY_DIMENSIONS_V1",
            "narrative": "TEST_ONLY_NARRATIVE_V1",
            "ontology": "TEST_ONLY_ONTOLOGY_V1",
            "primitive_resolution": "TEST_ONLY_RESOLUTION_V1",
        },
    }


def test_validate_semantic_contracts_requires_explicit_runtime_baseline(
    tmp_path: Path
) -> None:
    with pytest.raises(SystemExit) as error:
        main(["validate-semantic-contracts", str(tmp_path)])

    assert error.value.code == 2


def test_validate_semantic_contracts_rejects_changed_snapshot(
    tmp_path: Path, monkeypatch, capsys
) -> None:
    import destiny_personality.cli as cli

    calls = []
    runtime = object()
    bundle = object()

    def fake_load_runtime(path: Path):
        calls.append(("runtime", path))
        return runtime

    def fake_load_bundle(path: Path, accepted_runtime):
        calls.append(("semantic", path, accepted_runtime))
        return bundle

    fingerprints = iter(
        (
            {"algorithm": "sha256", "bundle_sha256": "a" * 64, "files": {}},
            {"algorithm": "sha256", "bundle_sha256": "b" * 64, "files": {}},
        )
    )

    def fake_fingerprint(candidate: Path, baseline: Path):
        calls.append(("fingerprint", candidate, baseline))
        return next(fingerprints)

    monkeypatch.setattr(cli, "load_runtime_config", fake_load_runtime)
    monkeypatch.setattr(cli, "load_semantic_contract_bundle", fake_load_bundle)
    monkeypatch.setattr(cli, "build_semantic_bundle_fingerprint", fake_fingerprint)
    monkeypatch.setattr(
        cli,
        "_semantic_contract_summary",
        lambda _bundle, _runtime, _fingerprint: {"status": "ok"},
    )

    candidate_dir = tmp_path / "candidate"
    runtime_dir = tmp_path / "runtime"
    exit_code = main(
        [
            "validate-semantic-contracts",
            str(candidate_dir),
            "--runtime-config-dir",
            str(runtime_dir),
        ]
    )

    captured = capsys.readouterr()
    assert exit_code == 2
    assert captured.out == ""
    assert captured.err == (
        "CONFIG_VALUE_ERROR: configuration files changed during validation; "
        "retry with an immutable candidate snapshot\n"
    )
    assert calls == [
        ("runtime", runtime_dir),
        ("semantic", candidate_dir, runtime),
        ("fingerprint", candidate_dir, runtime_dir),
        ("runtime", runtime_dir),
        ("semantic", candidate_dir, runtime),
        ("fingerprint", candidate_dir, runtime_dir),
    ]


def test_validate_semantic_contracts_reports_config_error(
    tmp_path: Path, monkeypatch, capsys
) -> None:
    import destiny_personality.cli as cli

    runtime = object()
    monkeypatch.setattr(cli, "load_runtime_config", lambda _path: runtime)

    def fail(_path: Path, _runtime) -> None:
        raise ConfigError(
            "CONFIG_GAP",
            "required candidate asset is missing",
            file="primitive_ontology_v1.yaml",
        )

    monkeypatch.setattr(cli, "load_semantic_contract_bundle", fail)
    fingerprint_called = False

    def fingerprint_should_not_run(_candidate: Path, _baseline: Path):
        nonlocal fingerprint_called
        fingerprint_called = True

    monkeypatch.setattr(
        cli, "build_semantic_bundle_fingerprint", fingerprint_should_not_run
    )

    exit_code = main(
        [
            "validate-semantic-contracts",
            str(tmp_path / "candidate"),
            "--runtime-config-dir",
            str(tmp_path / "runtime"),
        ]
    )

    captured = capsys.readouterr()
    assert exit_code == 2
    assert captured.out == ""
    assert captured.err == (
        "CONFIG_GAP | primitive_ontology_v1.yaml: "
        "required candidate asset is missing\n"
    )
    assert fingerprint_called is False


def test_validate_calculation_contracts_loads_stable_candidate(
    tmp_path: Path, monkeypatch, capsys
) -> None:
    import destiny_personality.cli as cli

    candidate_dir = tmp_path / "candidate"
    runtime_dir = tmp_path / "runtime"
    calls = []
    runtime = object()
    bundle = SimpleNamespace(
        vocabulary=SimpleNamespace(
            vocabulary_version="TEST_ONLY_VOCABULARY_V1",
            categories=tuple(
                SimpleNamespace(entries=(object(),)) for _ in range(10)
            ),
        ),
        bazi_tables=SimpleNamespace(
            table_version="TEST_ONLY_BAZI_TABLES_V1",
            tables=tuple(
                SimpleNamespace(rules=(object(),)) for _ in range(3)
            ),
        ),
        astrology_dignity_table=SimpleNamespace(
            table_version="TEST_ONLY_DIGNITY_V1",
            rows=(object(), object()),
        ),
        astrology_node_policy=SimpleNamespace(
            policy_version="TEST_ONLY_NODE_V1"
        ),
        comparison_policy=SimpleNamespace(
            policy_version="TEST_ONLY_COMPARISON_V1",
            logical_categories=(object(), object()),
            boundary_margins=(object(),),
            canonical_precision=(object(),),
            tolerances=(object(),),
            representation_equivalences=(object(),),
        ),
    )
    fingerprint = {
        "algorithm": "sha256",
        "bundle_sha256": "a" * 64,
        "files": {"candidate/TEST_ONLY.yaml": "b" * 64},
    }

    monkeypatch.setattr(
        cli,
        "load_runtime_config",
        lambda path: calls.append(("runtime", path)) or runtime,
    )
    monkeypatch.setattr(
        cli,
        "load_calculation_contract_bundle",
        lambda path, accepted: calls.append(("bundle", path, accepted)) or bundle,
    )
    monkeypatch.setattr(
        cli,
        "build_calculation_bundle_fingerprint",
        lambda candidate, baseline: calls.append(("fingerprint", candidate, baseline))
        or fingerprint,
    )

    exit_code = main(
        [
            "validate-calculation-contracts",
            str(candidate_dir),
            "--runtime-config-dir",
            str(runtime_dir),
        ]
    )

    assert exit_code == 0
    assert [call[0] for call in calls] == [
        "runtime", "bundle", "fingerprint",
        "runtime", "bundle", "fingerprint",
    ]
    assert json.loads(capsys.readouterr().out) == {
        "command": "validate-calculation-contracts",
        "counts": {
            "astrology_dignity_rows": 2,
            "bazi_rules": 3,
            "boundary_margins": 1,
            "comparison_categories": 2,
            "canonical_precision": 1,
            "representation_equivalences": 1,
            "tolerances": 1,
            "vocabulary_categories": 10,
            "vocabulary_entries": 10,
        },
        "fingerprint": fingerprint,
        "status": "ok",
        "versions": {
            "astrology_dignity_table": "TEST_ONLY_DIGNITY_V1",
            "astrology_node_policy": "TEST_ONLY_NODE_V1",
            "bazi_tables": "TEST_ONLY_BAZI_TABLES_V1",
            "comparison_policy": "TEST_ONLY_COMPARISON_V1",
            "vocabulary": "TEST_ONLY_VOCABULARY_V1",
        },
    }


def test_validate_calculation_contracts_rejects_changed_snapshot(
    tmp_path: Path, monkeypatch, capsys
) -> None:
    import destiny_personality.cli as cli

    monkeypatch.setattr(cli, "load_runtime_config", lambda _path: object())
    monkeypatch.setattr(
        cli, "load_calculation_contract_bundle", lambda _path, _runtime: object()
    )
    fingerprints = iter(
        (
            {"algorithm": "sha256", "bundle_sha256": "a" * 64, "files": {}},
            {"algorithm": "sha256", "bundle_sha256": "b" * 64, "files": {}},
        )
    )
    monkeypatch.setattr(
        cli,
        "build_calculation_bundle_fingerprint",
        lambda _candidate, _runtime: next(fingerprints),
    )

    exit_code = main(
        [
            "validate-calculation-contracts",
            str(tmp_path / "candidate"),
            "--runtime-config-dir",
            str(tmp_path / "runtime"),
        ]
    )

    captured = capsys.readouterr()
    assert exit_code == 2
    assert captured.out == ""
    assert captured.err == (
        "CONFIG_VALUE_ERROR: configuration files changed during validation; "
        "retry with an immutable candidate snapshot\n"
    )


def test_validate_calculation_contracts_requires_runtime_baseline(tmp_path) -> None:
    with pytest.raises(SystemExit) as error:
        main(["validate-calculation-contracts", str(tmp_path)])
    assert error.value.code == 2
