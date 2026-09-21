from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest
import yaml

import destiny_personality
from destiny_personality.vocabulary_models import (
    CanonicalFactVocabularyConfig,
    VocabularyCategory,
    VocabularyEntry,
)


FILE = "bazi_deterministic_tables_v1.yaml"
SECTIONS = ("hidden_stems", "ten_gods", "relations")


def _vocabulary(runtime_config) -> CanonicalFactVocabularyConfig:
    categories = tuple(
        VocabularyCategory(
            category_id=category,
            entries=(VocabularyEntry(f"TEST_ONLY_{category.upper()}", ()),),
        )
        for category in (
            "bazi_stem",
            "bazi_branch",
            "bazi_ten_god",
            "bazi_relation",
            "astrology_body",
            "astrology_sign",
            "astrology_aspect",
            "astrology_angle",
            "astrology_dignity",
            "astrology_node",
        )
    )
    return CanonicalFactVocabularyConfig(
        "canonical-fact-vocabulary-v1",
        "TEST_ONLY_VOCABULARY_V1",
        runtime_config.bazi.methodology_version,
        runtime_config.astrology.methodology_version,
        categories,
    )


def _data(runtime_config) -> dict:
    output_categories = {
        "hidden_stems": "bazi_stem",
        "ten_gods": "bazi_ten_god",
        "relations": "bazi_relation",
    }
    return {
        "schema_version": "bazi-deterministic-tables-v1",
        "table_version": "TEST_ONLY_BAZI_TABLES_V1",
        "methodology_version": runtime_config.bazi.methodology_version,
        "vocabulary_version": "TEST_ONLY_VOCABULARY_V1",
        "tables": {
            section: [
                {
                    "rule_id": f"TEST_ONLY_{section.upper()}_RULE",
                    "inputs": {"bazi_branch": ["TEST_ONLY_BAZI_BRANCH"]},
                    "outputs": {
                        output_categories[section]: [
                            f"TEST_ONLY_{output_categories[section].upper()}"
                        ]
                    },
                    "limitations": [],
                }
            ]
            for section in SECTIONS
        },
    }


def test_loads_immutable_bazi_deterministic_tables(tmp_path: Path, runtime_config) -> None:
    with (tmp_path / FILE).open("w", encoding="utf-8") as stream:
        yaml.safe_dump(_data(runtime_config), stream, sort_keys=False)
    loader = getattr(destiny_personality, "load_bazi_deterministic_tables", None)
    assert callable(loader), "public Bazi deterministic table loader is missing"

    config = loader(tmp_path, runtime_config, _vocabulary(runtime_config))

    assert config.schema_version == "bazi-deterministic-tables-v1"
    assert config.table_version == "TEST_ONLY_BAZI_TABLES_V1"
    assert tuple(section.section_id for section in config.tables) == SECTIONS
    assert config.tables[0].rules[0].inputs == (
        ("bazi_branch", ("TEST_ONLY_BAZI_BRANCH",)),
    )
    with pytest.raises(FrozenInstanceError):
        config.table_version = "changed"


def _write(path: Path, data: object) -> None:
    with path.open("w", encoding="utf-8") as stream:
        yaml.safe_dump(data, stream, sort_keys=False)


def _assert_error(tmp_path, runtime_config, data, code, field) -> None:
    _write(tmp_path / FILE, data)
    with pytest.raises(destiny_personality.ConfigError) as error:
        destiny_personality.load_bazi_deterministic_tables(
            tmp_path, runtime_config, _vocabulary(runtime_config)
        )
    assert (error.value.code, error.value.file, error.value.field) == (
        code,
        FILE,
        field,
    )


@pytest.mark.parametrize(
    ("mutation", "code", "field"),
    (
        (lambda data: data.pop("table_version"), "CONFIG_GAP", "table_version"),
        (lambda data: data.update(extra=True), "CONFIG_VALUE_ERROR", "extra"),
        (lambda data: data.update(schema_version="wrong"), "CONFIG_VERSION_MISMATCH", "schema_version"),
        (lambda data: data.update(methodology_version="wrong"), "CONFIG_VERSION_MISMATCH", "methodology_version"),
        (lambda data: data.update(vocabulary_version="wrong"), "CONFIG_VERSION_MISMATCH", "vocabulary_version"),
        (lambda data: data["tables"].pop("relations"), "CONFIG_GAP", "tables.relations"),
        (lambda data: data["tables"].update(extra=[]), "CONFIG_VALUE_ERROR", "tables.extra"),
        (lambda data: data["tables"].update(hidden_stems=[]), "CONFIG_VALUE_ERROR", "tables.hidden_stems"),
        (lambda data: data["tables"]["hidden_stems"][0].update(extra=True), "CONFIG_VALUE_ERROR", "tables.hidden_stems.0.extra"),
        (lambda data: data["tables"]["hidden_stems"][0].update(inputs={"astrology_body": ["TEST_ONLY_ASTROLOGY_BODY"]}), "CONFIG_VALUE_ERROR", "tables.hidden_stems.0.inputs.astrology_body"),
        (lambda data: data["tables"]["hidden_stems"][0].update(inputs={"bazi_branch": ["TEST_ONLY_UNKNOWN"]}), "CONFIG_VALUE_ERROR", "tables.hidden_stems.0.inputs.bazi_branch.0"),
    ),
)
def test_bazi_table_validation_errors(tmp_path, runtime_config, mutation, code, field) -> None:
    data = _data(runtime_config)
    mutation(data)
    _assert_error(tmp_path, runtime_config, data, code, field)


def test_bazi_rule_ids_are_unique_across_sections(tmp_path, runtime_config) -> None:
    data = _data(runtime_config)
    data["tables"]["ten_gods"][0]["rule_id"] = data["tables"]["hidden_stems"][0]["rule_id"]
    _assert_error(
        tmp_path,
        runtime_config,
        data,
        "CONFIG_VALUE_ERROR",
        "tables.ten_gods.0.rule_id",
    )


def test_each_bazi_section_requires_its_declared_output_category(
    tmp_path, runtime_config
) -> None:
    data = _data(runtime_config)
    data["tables"]["ten_gods"][0]["outputs"] = {
        "bazi_stem": ["TEST_ONLY_BAZI_STEM"]
    }
    _assert_error(
        tmp_path,
        runtime_config,
        data,
        "CONFIG_VALUE_ERROR",
        "tables.ten_gods.0.outputs.bazi_stem",
    )
