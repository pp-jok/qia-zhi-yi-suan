from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest
import yaml

import destiny_personality


FILE = "canonical_fact_vocabulary_v1.yaml"
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


def _write(path: Path, data: object) -> None:
    with path.open("w", encoding="utf-8") as stream:
        yaml.safe_dump(data, stream, allow_unicode=True, sort_keys=False)


def _data() -> dict:
    return {
        "schema_version": "canonical-fact-vocabulary-v1",
        "vocabulary_version": "TEST_ONLY_VOCABULARY_V1",
        "methodology_versions": {
            "bazi": "bazi-core-v1.0",
            "astrology": "western-tropical-v1.0",
        },
        "categories": {
            category: {
                "entries": [
                    {
                        "canonical_id": f"TEST_ONLY_{category.upper()}",
                        "aliases": [f"TEST_ONLY_{category.upper()}_ALIAS"],
                    }
                ]
            }
            for category in CATEGORIES
        },
    }


@pytest.fixture
def vocabulary_dir(tmp_path: Path) -> Path:
    _write(tmp_path / FILE, _data())
    return tmp_path


def test_loads_immutable_canonical_fact_vocabulary(
    vocabulary_dir: Path, runtime_config
) -> None:
    loader = getattr(destiny_personality, "load_canonical_fact_vocabulary", None)
    assert callable(loader), "public canonical vocabulary loader is missing"

    vocabulary = loader(vocabulary_dir, runtime_config)

    assert vocabulary.schema_version == "canonical-fact-vocabulary-v1"
    assert vocabulary.vocabulary_version == "TEST_ONLY_VOCABULARY_V1"
    assert vocabulary.bazi_methodology_version == "bazi-core-v1.0"
    assert vocabulary.astrology_methodology_version == "western-tropical-v1.0"
    assert tuple(item.category_id for item in vocabulary.categories) == CATEGORIES
    assert vocabulary.categories[0].entries[0].canonical_id == "TEST_ONLY_BAZI_STEM"
    assert vocabulary.categories[0].entries[0].aliases == (
        "TEST_ONLY_BAZI_STEM_ALIAS",
    )
    with pytest.raises(FrozenInstanceError):
        vocabulary.vocabulary_version = "changed"


def _assert_error(
    directory: Path, runtime_config, code: str, field: str = None
) -> None:
    with pytest.raises(destiny_personality.ConfigError) as error:
        destiny_personality.load_canonical_fact_vocabulary(directory, runtime_config)
    assert error.value.code == code
    assert error.value.file == FILE
    assert error.value.field == field


def test_missing_and_malformed_vocabulary_errors(tmp_path: Path, runtime_config) -> None:
    _assert_error(tmp_path, runtime_config, "CONFIG_GAP")
    (tmp_path / FILE).write_text("categories: [", encoding="utf-8")
    _assert_error(tmp_path, runtime_config, "CONFIG_PARSE_ERROR")


@pytest.mark.parametrize(
    ("mutation", "code", "field"),
    (
        (lambda data: data.pop("vocabulary_version"), "CONFIG_GAP", "vocabulary_version"),
        (lambda data: data.update(extra=True), "CONFIG_VALUE_ERROR", "extra"),
        (lambda data: data.update(schema_version="wrong"), "CONFIG_VERSION_MISMATCH", "schema_version"),
        (lambda data: data.update(categories=[]), "CONFIG_TYPE_ERROR", "categories"),
        (lambda data: data.update(methodology_versions=[]), "CONFIG_TYPE_ERROR", "methodology_versions"),
    ),
)
def test_root_contract_errors(
    vocabulary_dir: Path, runtime_config, mutation, code: str, field: str
) -> None:
    path = vocabulary_dir / FILE
    data = _data()
    mutation(data)
    _write(path, data)
    _assert_error(vocabulary_dir, runtime_config, code, field)


@pytest.mark.parametrize("system", ("bazi", "astrology"))
def test_methodology_version_must_match_runtime(
    vocabulary_dir: Path, runtime_config, system: str
) -> None:
    data = _data()
    data["methodology_versions"][system] = "TEST_ONLY_WRONG"
    _write(vocabulary_dir / FILE, data)
    _assert_error(
        vocabulary_dir,
        runtime_config,
        "CONFIG_VERSION_MISMATCH",
        f"methodology_versions.{system}",
    )


def test_non_mapping_root_and_non_string_key_are_type_errors(
    vocabulary_dir: Path, runtime_config
) -> None:
    _write(vocabulary_dir / FILE, [])
    _assert_error(vocabulary_dir, runtime_config, "CONFIG_TYPE_ERROR")

    data = _data()
    data[1] = "TEST_ONLY_BAD_KEY"
    _write(vocabulary_dir / FILE, data)
    _assert_error(vocabulary_dir, runtime_config, "CONFIG_TYPE_ERROR", "1")


def test_required_category_set_is_exact(vocabulary_dir: Path, runtime_config) -> None:
    data = _data()
    del data["categories"]["astrology_node"]
    _write(vocabulary_dir / FILE, data)
    _assert_error(
        vocabulary_dir, runtime_config, "CONFIG_GAP", "categories.astrology_node"
    )

    data = _data()
    data["categories"]["TEST_ONLY_EXTRA"] = {"entries": []}
    _write(vocabulary_dir / FILE, data)
    _assert_error(
        vocabulary_dir,
        runtime_config,
        "CONFIG_VALUE_ERROR",
        "categories.TEST_ONLY_EXTRA",
    )


@pytest.mark.parametrize(
    ("mutation", "code", "field"),
    (
        (lambda category: category.update(extra=True), "CONFIG_VALUE_ERROR", "categories.bazi_stem.extra"),
        (lambda category: category.update(entries=[]), "CONFIG_VALUE_ERROR", "categories.bazi_stem.entries"),
        (lambda category: category.update(entries={}), "CONFIG_TYPE_ERROR", "categories.bazi_stem.entries"),
        (lambda category: category["entries"][0].pop("aliases"), "CONFIG_GAP", "categories.bazi_stem.entries.0.aliases"),
        (lambda category: category["entries"][0].update(extra=True), "CONFIG_VALUE_ERROR", "categories.bazi_stem.entries.0.extra"),
        (lambda category: category["entries"][0].update(canonical_id=1), "CONFIG_TYPE_ERROR", "categories.bazi_stem.entries.0.canonical_id"),
        (lambda category: category["entries"][0].update(canonical_id="  "), "CONFIG_VALUE_ERROR", "categories.bazi_stem.entries.0.canonical_id"),
        (lambda category: category["entries"][0].update(aliases={}), "CONFIG_TYPE_ERROR", "categories.bazi_stem.entries.0.aliases"),
        (lambda category: category["entries"][0].update(aliases=["  "]), "CONFIG_VALUE_ERROR", "categories.bazi_stem.entries.0.aliases.0"),
    ),
)
def test_category_and_entry_contract_errors(
    vocabulary_dir: Path, runtime_config, mutation, code: str, field: str
) -> None:
    data = _data()
    mutation(data["categories"]["bazi_stem"])
    _write(vocabulary_dir / FILE, data)
    _assert_error(vocabulary_dir, runtime_config, code, field)


@pytest.mark.parametrize(
    "second_entry",
    (
        {"canonical_id": " test_only_bazi_stem ", "aliases": []},
        {"canonical_id": "TEST_ONLY_SECOND", "aliases": [" test_only_bazi_stem_alias "]},
    ),
)
def test_category_tokens_are_unambiguous_after_trim_and_casefold(
    vocabulary_dir: Path, runtime_config, second_entry: dict
) -> None:
    data = _data()
    data["categories"]["bazi_stem"]["entries"].append(second_entry)
    _write(vocabulary_dir / FILE, data)
    _assert_error(
        vocabulary_dir,
        runtime_config,
        "CONFIG_VALUE_ERROR",
        "categories.bazi_stem.entries.1.canonical_id"
        if second_entry["canonical_id"].strip().casefold()
        == "test_only_bazi_stem"
        else "categories.bazi_stem.entries.1.aliases.0",
    )
