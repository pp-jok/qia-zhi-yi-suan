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


FILE = "fact_comparison_policy_v1.yaml"
TRIGGERS = [
    "warning",
    "uncertainty",
    "boundary_sensitivity",
    "historical_time_ambiguity",
    "policy_anomaly",
]
CATEGORIES = (
    "bazi_stem", "bazi_branch", "bazi_ten_god", "bazi_relation",
    "astrology_body", "astrology_sign", "astrology_aspect", "astrology_angle",
    "astrology_dignity", "astrology_node",
)


def _vocabulary(runtime_config) -> CanonicalFactVocabularyConfig:
    return CanonicalFactVocabularyConfig(
        "canonical-fact-vocabulary-v1",
        "TEST_ONLY_VOCABULARY_V1",
        runtime_config.bazi.methodology_version,
        runtime_config.astrology.methodology_version,
        tuple(
            VocabularyCategory(category, (VocabularyEntry(f"TEST_ONLY_{category.upper()}", ()),))
            for category in CATEGORIES
        ),
    )


def _data(runtime_config) -> dict:
    return {
        "schema_version": "fact-comparison-policy-v1",
        "policy_version": "TEST_ONLY_COMPARISON_POLICY_V1",
        "methodology_versions": {
            "bazi": runtime_config.bazi.methodology_version,
            "astrology": runtime_config.astrology.methodology_version,
        },
        "vocabulary_version": "TEST_ONLY_VOCABULARY_V1",
        "fact_schema_version": "deterministic-facts-v1",
        "triggers": list(TRIGGERS),
        "logical_categories": [
            {"category_id": "TEST_ONLY_NUMERIC", "comparison_mode": "numeric"},
            {"category_id": "TEST_ONLY_EXACT", "comparison_mode": "exact"},
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
        "representation_equivalences": [
            {
                "logical_category_id": "TEST_ONLY_EXACT",
                "vocabulary_category_id": "astrology_sign",
                "canonical_id": "TEST_ONLY_ASTROLOGY_SIGN",
                "equivalent_values": ["TEST_ONLY_REPRESENTATION"],
            }
        ],
    }


def _write(path: Path, value: object) -> None:
    with path.open("w", encoding="utf-8") as stream:
        yaml.safe_dump(value, stream, sort_keys=False)


def _assert_error(tmp_path, runtime_config, data, code, field) -> None:
    _write(tmp_path / FILE, data)
    with pytest.raises(destiny_personality.ConfigError) as error:
        destiny_personality.load_fact_comparison_policy(
            tmp_path, runtime_config, _vocabulary(runtime_config)
        )
    assert (error.value.code, error.value.file, error.value.field) == (code, FILE, field)


def test_loads_immutable_complete_fact_comparison_policy(tmp_path, runtime_config) -> None:
    _write(tmp_path / FILE, _data(runtime_config))
    loader = getattr(destiny_personality, "load_fact_comparison_policy", None)
    assert callable(loader), "public fact comparison policy loader is missing"

    config = loader(tmp_path, runtime_config, _vocabulary(runtime_config))

    assert config.policy_version == "TEST_ONLY_COMPARISON_POLICY_V1"
    assert config.canonical_precision[0].decimal_places == 4
    assert str(config.tolerances[0].absolute_tolerance) == "0.01"
    with pytest.raises(FrozenInstanceError):
        config.policy_version = "changed"


@pytest.mark.parametrize(
    ("mutation", "code", "field"),
    (
        (lambda data: data.pop("triggers"), "CONFIG_GAP", "triggers"),
        (lambda data: data.update(extra=True), "CONFIG_VALUE_ERROR", "extra"),
        (lambda data: data.update(schema_version="wrong"), "CONFIG_VERSION_MISMATCH", "schema_version"),
        (lambda data: data["methodology_versions"].update(bazi="wrong"), "CONFIG_VERSION_MISMATCH", "methodology_versions.bazi"),
        (lambda data: data.update(vocabulary_version="wrong"), "CONFIG_VERSION_MISMATCH", "vocabulary_version"),
        (lambda data: data.update(fact_schema_version="wrong"), "CONFIG_VERSION_MISMATCH", "fact_schema_version"),
        (lambda data: data.update(triggers=TRIGGERS[:-1]), "CONFIG_GAP", "triggers.policy_anomaly"),
        (lambda data: data["logical_categories"].append(dict(data["logical_categories"][0])), "CONFIG_VALUE_ERROR", "logical_categories.2.category_id"),
        (lambda data: data["logical_categories"][0].update(comparison_mode="fuzzy"), "CONFIG_VALUE_ERROR", "logical_categories.0.comparison_mode"),
        (lambda data: data["boundary_margins"][0].update(margin=-1), "CONFIG_VALUE_ERROR", "boundary_margins.0.margin"),
        (lambda data: data["canonical_precision"][0].update(decimal_places=True), "CONFIG_TYPE_ERROR", "canonical_precision.0.decimal_places"),
        (lambda data: data["tolerances"][0].update(category_id="TEST_ONLY_UNKNOWN"), "CONFIG_VALUE_ERROR", "tolerances.0.category_id"),
        (lambda data: data["representation_equivalences"][0].update(canonical_id="TEST_ONLY_UNKNOWN"), "CONFIG_VALUE_ERROR", "representation_equivalences.0.canonical_id"),
        (lambda data: data["representation_equivalences"][0].update(equivalent_values=[]), "CONFIG_VALUE_ERROR", "representation_equivalences.0.equivalent_values"),
    ),
)
def test_fact_comparison_policy_validation_errors(
    tmp_path, runtime_config, mutation, code, field
) -> None:
    data = _data(runtime_config)
    mutation(data)
    _assert_error(tmp_path, runtime_config, data, code, field)


@pytest.mark.parametrize(
    ("section", "field"),
    (
        ("boundary_margins", "boundary_margins"),
        ("canonical_precision", "canonical_precision"),
        ("tolerances", "tolerances"),
    ),
)
def test_numeric_categories_require_complete_numeric_policy(
    tmp_path, runtime_config, section, field
) -> None:
    data = _data(runtime_config)
    data[section] = []
    _assert_error(tmp_path, runtime_config, data, "CONFIG_GAP", field)


@pytest.mark.parametrize(
    "section",
    ("boundary_margins", "canonical_precision", "tolerances"),
)
def test_exact_categories_reject_numeric_policy(tmp_path, runtime_config, section) -> None:
    data = _data(runtime_config)
    data[section][0]["category_id"] = "TEST_ONLY_EXACT"
    _assert_error(
        tmp_path,
        runtime_config,
        data,
        "CONFIG_VALUE_ERROR",
        f"{section}.0.category_id",
    )
