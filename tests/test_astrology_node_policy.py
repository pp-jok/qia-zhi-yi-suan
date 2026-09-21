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


FILE = "astrology_node_policy_v1.yaml"
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
        "schema_version": "astrology-node-policy-v1",
        "policy_version": "TEST_ONLY_NODE_POLICY_V1",
        "methodology_version": runtime_config.astrology.methodology_version,
        "vocabulary_version": "TEST_ONLY_VOCABULARY_V1",
        "node_id": "TEST_ONLY_ASTROLOGY_NODE",
        "output": {
            "included": True,
            "phase": "TEST_ONLY_PHASE",
            "aspect_participation": True,
            "dignity_participation": False,
            "weight_role": "TEST_ONLY_WEIGHT_ROLE",
            "time_sensitive": True,
        },
    }


def _write(path: Path, value: object) -> None:
    with path.open("w", encoding="utf-8") as stream:
        yaml.safe_dump(value, stream, sort_keys=False)


def _assert_error(tmp_path, runtime_config, data, code, field) -> None:
    _write(tmp_path / FILE, data)
    with pytest.raises(destiny_personality.ConfigError) as error:
        destiny_personality.load_astrology_node_policy(
            tmp_path, runtime_config, _vocabulary(runtime_config)
        )
    assert (error.value.code, error.value.file, error.value.field) == (code, FILE, field)


def test_loads_immutable_explicit_astrology_node_policy(tmp_path, runtime_config) -> None:
    _write(tmp_path / FILE, _data(runtime_config))
    loader = getattr(destiny_personality, "load_astrology_node_policy", None)
    assert callable(loader), "public astrology node policy loader is missing"

    config = loader(tmp_path, runtime_config, _vocabulary(runtime_config))

    assert config.node_id == "TEST_ONLY_ASTROLOGY_NODE"
    assert config.output.aspect_participation is True
    with pytest.raises(FrozenInstanceError):
        config.output.included = False


@pytest.mark.parametrize(
    ("mutation", "code", "field"),
    (
        (lambda data: data.pop("output"), "CONFIG_GAP", "output"),
        (lambda data: data.update(extra=True), "CONFIG_VALUE_ERROR", "extra"),
        (lambda data: data.update(schema_version="wrong"), "CONFIG_VERSION_MISMATCH", "schema_version"),
        (lambda data: data.update(methodology_version="wrong"), "CONFIG_VERSION_MISMATCH", "methodology_version"),
        (lambda data: data.update(vocabulary_version="wrong"), "CONFIG_VERSION_MISMATCH", "vocabulary_version"),
        (lambda data: data.update(node_id="TEST_ONLY_UNKNOWN"), "CONFIG_VALUE_ERROR", "node_id"),
        (lambda data: data["output"].pop("phase"), "CONFIG_GAP", "output.phase"),
        (lambda data: data["output"].update(extra=True), "CONFIG_VALUE_ERROR", "output.extra"),
        (lambda data: data["output"].update(included="yes"), "CONFIG_TYPE_ERROR", "output.included"),
        (lambda data: data["output"].update(phase=""), "CONFIG_VALUE_ERROR", "output.phase"),
        (lambda data: data["output"].update(weight_role=""), "CONFIG_VALUE_ERROR", "output.weight_role"),
    ),
)
def test_astrology_node_policy_validation_errors(
    tmp_path, runtime_config, mutation, code, field
) -> None:
    data = _data(runtime_config)
    mutation(data)
    _assert_error(tmp_path, runtime_config, data, code, field)


def test_excluded_node_cannot_participate_in_aspects_or_dignities(
    tmp_path, runtime_config
) -> None:
    data = _data(runtime_config)
    data["output"].update(included=False, aspect_participation=True)
    _assert_error(
        tmp_path,
        runtime_config,
        data,
        "CONFIG_VALUE_ERROR",
        "output.aspect_participation",
    )

    data = _data(runtime_config)
    data["output"].update(included=False, aspect_participation=False, dignity_participation=True)
    _assert_error(
        tmp_path,
        runtime_config,
        data,
        "CONFIG_VALUE_ERROR",
        "output.dignity_participation",
    )


def test_node_inclusion_matches_frozen_astrology_methodology(
    tmp_path, runtime_config
) -> None:
    data = _data(runtime_config)
    data["output"].update(
        included=False,
        aspect_participation=False,
        dignity_participation=False,
    )
    _assert_error(
        tmp_path,
        runtime_config,
        data,
        "CONFIG_VALUE_ERROR",
        "output.included",
    )
