import json
from pathlib import Path

import pytest
import yaml

import destiny_personality
from destiny_personality.cli import main


CATEGORIES = (
    "bazi_stem", "bazi_branch", "bazi_ten_god", "bazi_relation",
    "astrology_body", "astrology_sign", "astrology_aspect", "astrology_angle",
    "astrology_dignity", "astrology_node",
)


def _write_yaml(path: Path, value: object) -> None:
    with path.open("w", encoding="utf-8") as stream:
        yaml.safe_dump(value, stream, sort_keys=False)


def _write_candidate(directory: Path, runtime_config) -> None:
    directory.mkdir()
    vocabulary_version = "TEST_ONLY_VOCABULARY_V1"
    ids = {category: f"TEST_ONLY_{category.upper()}" for category in CATEGORIES}
    _write_yaml(
        directory / "canonical_fact_vocabulary_v1.yaml",
        {
            "schema_version": "canonical-fact-vocabulary-v1",
            "vocabulary_version": vocabulary_version,
            "methodology_versions": {
                "bazi": runtime_config.bazi.methodology_version,
                "astrology": runtime_config.astrology.methodology_version,
            },
            "categories": {
                category: {"entries": [{"canonical_id": ids[category], "aliases": []}]}
                for category in CATEGORIES
            },
        },
    )
    output_categories = {
        "hidden_stems": "bazi_stem",
        "ten_gods": "bazi_ten_god",
        "relations": "bazi_relation",
    }
    _write_yaml(
        directory / "bazi_deterministic_tables_v1.yaml",
        {
            "schema_version": "bazi-deterministic-tables-v1",
            "table_version": "TEST_ONLY_BAZI_TABLES_V1",
            "methodology_version": runtime_config.bazi.methodology_version,
            "vocabulary_version": vocabulary_version,
            "tables": {
                section: [
                    {
                        "rule_id": f"TEST_ONLY_{section.upper()}",
                        "inputs": {"bazi_branch": [ids["bazi_branch"]]},
                        "outputs": {category: [ids[category]]},
                        "limitations": [],
                    }
                ]
                for section, category in output_categories.items()
            },
        },
    )
    _write_yaml(
        directory / "astrology_dignity_table_v1.yaml",
        {
            "schema_version": "astrology-dignity-table-v1",
            "table_version": "TEST_ONLY_DIGNITY_V1",
            "methodology_version": runtime_config.astrology.methodology_version,
            "vocabulary_version": vocabulary_version,
            "rows": [
                {
                    "body_id": ids["astrology_body"],
                    "sign_id": ids["astrology_sign"],
                    "dignity_id": ids["astrology_dignity"],
                    "limitations": [],
                }
            ],
        },
    )
    _write_yaml(
        directory / "astrology_node_policy_v1.yaml",
        {
            "schema_version": "astrology-node-policy-v1",
            "policy_version": "TEST_ONLY_NODE_V1",
            "methodology_version": runtime_config.astrology.methodology_version,
            "vocabulary_version": vocabulary_version,
            "node_id": ids["astrology_node"],
            "output": {
                "included": runtime_config.astrology.core.true_node,
                "phase": "TEST_ONLY_PHASE",
                "aspect_participation": False,
                "dignity_participation": False,
                "weight_role": "TEST_ONLY_WEIGHT_ROLE",
                "time_sensitive": True,
            },
        },
    )
    _write_yaml(
        directory / "fact_comparison_policy_v1.yaml",
        {
            "schema_version": "fact-comparison-policy-v1",
            "policy_version": "TEST_ONLY_COMPARISON_V1",
            "methodology_versions": {
                "bazi": runtime_config.bazi.methodology_version,
                "astrology": runtime_config.astrology.methodology_version,
            },
            "vocabulary_version": vocabulary_version,
            "fact_schema_version": "deterministic-facts-v1",
            "triggers": [
                "warning", "uncertainty", "boundary_sensitivity",
                "historical_time_ambiguity", "policy_anomaly",
            ],
            "logical_categories": [
                {"category_id": "TEST_ONLY_NUMERIC", "comparison_mode": "numeric"}
            ],
            "boundary_margins": [
                {"category_id": "TEST_ONLY_NUMERIC", "margin": "0.1"}
            ],
            "canonical_precision": [
                {"category_id": "TEST_ONLY_NUMERIC", "decimal_places": 4}
            ],
            "tolerances": [
                {"category_id": "TEST_ONLY_NUMERIC", "absolute_tolerance": "0.01"}
            ],
            "representation_equivalences": [],
        },
    )


def test_calculation_bundle_loads_components_in_gate_order(
    monkeypatch, tmp_path, runtime_config
) -> None:
    import destiny_personality.calculation_bundle as module

    calls = []
    vocabulary = object()
    bazi = object()
    dignity = object()
    node = object()
    comparison = object()
    monkeypatch.setattr(module, "load_canonical_fact_vocabulary", lambda path, runtime: calls.append(("vocabulary", path, runtime)) or vocabulary)
    monkeypatch.setattr(module, "load_bazi_deterministic_tables", lambda path, runtime, vocab: calls.append(("bazi", vocab)) or bazi)
    monkeypatch.setattr(module, "load_astrology_dignity_table", lambda path, runtime, vocab: calls.append(("dignity", vocab)) or dignity)
    monkeypatch.setattr(module, "load_astrology_node_policy", lambda path, runtime, vocab: calls.append(("node", vocab)) or node)
    monkeypatch.setattr(module, "load_fact_comparison_policy", lambda path, runtime, vocab: calls.append(("comparison", vocab)) or comparison)

    loader = getattr(destiny_personality, "load_calculation_contract_bundle", None)
    assert callable(loader), "public calculation bundle loader is missing"
    bundle = loader(tmp_path, runtime_config)

    assert [call[0] for call in calls] == [
        "vocabulary", "bazi", "dignity", "node", "comparison"
    ]
    assert all(call[-1] is vocabulary for call in calls[1:])
    assert bundle.vocabulary is vocabulary
    assert bundle.bazi_tables is bazi
    assert bundle.astrology_dignity_table is dignity
    assert bundle.astrology_node_policy is node
    assert bundle.comparison_policy is comparison


def test_missing_vocabulary_wins_before_later_calculation_assets(
    tmp_path, runtime_config
) -> None:
    with pytest.raises(destiny_personality.ConfigError) as error:
        destiny_personality.load_calculation_contract_bundle(tmp_path, runtime_config)
    assert (error.value.code, error.value.file) == (
        "CONFIG_GAP",
        "canonical_fact_vocabulary_v1.yaml",
    )


def test_real_candidate_loads_and_cli_reports_nine_file_snapshot(
    tmp_path, valid_config_dir, runtime_config, capsys
) -> None:
    candidate_dir = tmp_path / "candidate"
    _write_candidate(candidate_dir, runtime_config)

    bundle = destiny_personality.load_calculation_contract_bundle(
        candidate_dir, runtime_config
    )
    assert bundle.comparison_policy.policy_version == "TEST_ONLY_COMPARISON_V1"

    exit_code = main(
        [
            "validate-calculation-contracts",
            str(candidate_dir),
            "--runtime-config-dir",
            str(valid_config_dir),
        ]
    )
    report = json.loads(capsys.readouterr().out)
    assert exit_code == 0
    assert report["status"] == "ok"
    assert report["counts"]["bazi_rules"] == 3
    assert len(report["fingerprint"]["files"]) == 9
