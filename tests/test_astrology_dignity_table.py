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


FILE = "astrology_dignity_table_v1.yaml"
CATEGORIES = (
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


def _vocabulary(runtime_config) -> CanonicalFactVocabularyConfig:
    return CanonicalFactVocabularyConfig(
        "canonical-fact-vocabulary-v1",
        "TEST_ONLY_VOCABULARY_V1",
        runtime_config.bazi.methodology_version,
        runtime_config.astrology.methodology_version,
        tuple(
            VocabularyCategory(
                category,
                (VocabularyEntry(f"TEST_ONLY_{category.upper()}", ()),),
            )
            for category in CATEGORIES
        ),
    )


def _data(runtime_config) -> dict:
    return {
        "schema_version": "astrology-dignity-table-v1",
        "table_version": "TEST_ONLY_ASTROLOGY_DIGNITY_V1",
        "methodology_version": runtime_config.astrology.methodology_version,
        "vocabulary_version": "TEST_ONLY_VOCABULARY_V1",
        "rows": [
            {
                "body_id": "TEST_ONLY_ASTROLOGY_BODY",
                "sign_id": "TEST_ONLY_ASTROLOGY_SIGN",
                "dignity_id": "TEST_ONLY_ASTROLOGY_DIGNITY",
                "limitations": [],
            }
        ],
    }


def _write(path: Path, value: object) -> None:
    with path.open("w", encoding="utf-8") as stream:
        yaml.safe_dump(value, stream, sort_keys=False)


def _assert_error(tmp_path, runtime_config, data, code, field) -> None:
    _write(tmp_path / FILE, data)
    with pytest.raises(destiny_personality.ConfigError) as error:
        destiny_personality.load_astrology_dignity_table(
            tmp_path, runtime_config, _vocabulary(runtime_config)
        )
    assert (error.value.code, error.value.file, error.value.field) == (
        code,
        FILE,
        field,
    )


def test_loads_immutable_astrology_dignity_table(tmp_path, runtime_config) -> None:
    _write(tmp_path / FILE, _data(runtime_config))
    loader = getattr(destiny_personality, "load_astrology_dignity_table", None)
    assert callable(loader), "public astrology dignity table loader is missing"

    config = loader(tmp_path, runtime_config, _vocabulary(runtime_config))

    assert config.table_version == "TEST_ONLY_ASTROLOGY_DIGNITY_V1"
    assert config.rows[0].body_id == "TEST_ONLY_ASTROLOGY_BODY"
    with pytest.raises(FrozenInstanceError):
        config.table_version = "changed"


@pytest.mark.parametrize(
    ("mutation", "code", "field"),
    (
        (lambda data: data.pop("rows"), "CONFIG_GAP", "rows"),
        (lambda data: data.update(extra=True), "CONFIG_VALUE_ERROR", "extra"),
        (lambda data: data.update(schema_version="wrong"), "CONFIG_VERSION_MISMATCH", "schema_version"),
        (lambda data: data.update(methodology_version="wrong"), "CONFIG_VERSION_MISMATCH", "methodology_version"),
        (lambda data: data.update(vocabulary_version="wrong"), "CONFIG_VERSION_MISMATCH", "vocabulary_version"),
        (lambda data: data.update(rows=[]), "CONFIG_VALUE_ERROR", "rows"),
        (lambda data: data["rows"][0].update(extra=True), "CONFIG_VALUE_ERROR", "rows.0.extra"),
        (lambda data: data["rows"][0].update(body_id="TEST_ONLY_UNKNOWN"), "CONFIG_VALUE_ERROR", "rows.0.body_id"),
        (lambda data: data["rows"][0].update(sign_id="TEST_ONLY_UNKNOWN"), "CONFIG_VALUE_ERROR", "rows.0.sign_id"),
        (lambda data: data["rows"][0].update(dignity_id="TEST_ONLY_UNKNOWN"), "CONFIG_VALUE_ERROR", "rows.0.dignity_id"),
    ),
)
def test_astrology_dignity_validation_errors(
    tmp_path, runtime_config, mutation, code, field
) -> None:
    data = _data(runtime_config)
    mutation(data)
    _assert_error(tmp_path, runtime_config, data, code, field)


def test_astrology_dignity_keys_are_unique(tmp_path, runtime_config) -> None:
    data = _data(runtime_config)
    data["rows"].append(dict(data["rows"][0]))
    _assert_error(tmp_path, runtime_config, data, "CONFIG_VALUE_ERROR", "rows.1")
