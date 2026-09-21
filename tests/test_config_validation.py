from pathlib import Path

import pytest
import yaml

from destiny_personality import ConfigError, load_runtime_config


def _read_yaml(path: Path) -> dict:
    with path.open(encoding="utf-8") as stream:
        return yaml.safe_load(stream)


def _write_yaml(path: Path, data: object) -> None:
    with path.open("w", encoding="utf-8") as stream:
        yaml.safe_dump(data, stream, allow_unicode=True, sort_keys=False)


def test_missing_required_file_is_config_gap(valid_config_dir: Path) -> None:
    (valid_config_dir / "score_model_v2_2.yaml").unlink()

    with pytest.raises(ConfigError) as caught:
        load_runtime_config(valid_config_dir)

    assert caught.value.code == "CONFIG_GAP"
    assert caught.value.file == "score_model_v2_2.yaml"


def test_malformed_yaml_is_parse_error(valid_config_dir: Path) -> None:
    path = valid_config_dir / "bazi_methodology_v1.yaml"
    path.write_text("calendar: [", encoding="utf-8")

    with pytest.raises(ConfigError) as caught:
        load_runtime_config(valid_config_dir)

    assert caught.value.code == "CONFIG_PARSE_ERROR"


def test_non_mapping_root_is_type_error(valid_config_dir: Path) -> None:
    _write_yaml(valid_config_dir / "bazi_methodology_v1.yaml", [])

    with pytest.raises(ConfigError) as caught:
        load_runtime_config(valid_config_dir)

    assert caught.value.code == "CONFIG_TYPE_ERROR"
    assert caught.value.field is None


def test_wrong_frozen_version_is_version_mismatch(valid_config_dir: Path) -> None:
    path = valid_config_dir / "bazi_methodology_v1.yaml"
    data = _read_yaml(path)
    data["methodology_version"] = "bazi-core-v9.9"
    _write_yaml(path, data)

    with pytest.raises(ConfigError) as caught:
        load_runtime_config(valid_config_dir)

    assert caught.value.code == "CONFIG_VERSION_MISMATCH"
    assert caught.value.field == "methodology_version"


def test_missing_required_field_is_config_gap(valid_config_dir: Path) -> None:
    path = valid_config_dir / "score_model_v2_2.yaml"
    data = _read_yaml(path)
    del data["synthesis_priority"]["core_threshold"]
    _write_yaml(path, data)

    with pytest.raises(ConfigError) as caught:
        load_runtime_config(valid_config_dir)

    assert caught.value.code == "CONFIG_GAP"
    assert caught.value.field == "synthesis_priority.core_threshold"


def test_boolean_is_not_accepted_as_integer(valid_config_dir: Path) -> None:
    path = valid_config_dir / "score_model_v2_2.yaml"
    data = _read_yaml(path)
    data["trait_salience"]["max"] = True
    _write_yaml(path, data)

    with pytest.raises(ConfigError) as caught:
        load_runtime_config(valid_config_dir)

    assert caught.value.code == "CONFIG_TYPE_ERROR"
    assert caught.value.field == "trait_salience.max"


def test_unknown_top_level_field_is_rejected(valid_config_dir: Path) -> None:
    path = valid_config_dir / "astrology_methodology_v1.yaml"
    data = _read_yaml(path)
    data["zodaic_typo"] = "tropical"
    _write_yaml(path, data)

    with pytest.raises(ConfigError) as caught:
        load_runtime_config(valid_config_dir)

    assert caught.value.code == "CONFIG_VALUE_ERROR"
    assert caught.value.field == "zodaic_typo"


@pytest.mark.parametrize("primitive_id", ["P12", "p001", "P0001"])
def test_relation_primitive_id_format_is_enforced(
    valid_config_dir: Path, primitive_id: str
) -> None:
    path = valid_config_dir / "primitive_relation_graph_v1.yaml"
    data = _read_yaml(path)
    data["relations"][0]["left"] = primitive_id
    _write_yaml(path, data)

    with pytest.raises(ConfigError) as caught:
        load_runtime_config(valid_config_dir)

    assert caught.value.code == "CONFIG_VALUE_ERROR"
    assert caught.value.field == "relations.0.left"


def test_relation_self_loop_is_rejected(valid_config_dir: Path) -> None:
    path = valid_config_dir / "primitive_relation_graph_v1.yaml"
    data = _read_yaml(path)
    data["relations"][0]["right"] = data["relations"][0]["left"]
    _write_yaml(path, data)

    with pytest.raises(ConfigError) as caught:
        load_runtime_config(valid_config_dir)

    assert caught.value.code == "CONFIG_VALUE_ERROR"
    assert caught.value.field == "relations.0.right"


def test_tension_requires_dynamic_family(valid_config_dir: Path) -> None:
    path = valid_config_dir / "primitive_relation_graph_v1.yaml"
    data = _read_yaml(path)
    del data["relations"][0]["dynamic_family"]
    _write_yaml(path, data)

    with pytest.raises(ConfigError) as caught:
        load_runtime_config(valid_config_dir)

    assert caught.value.code == "CONFIG_GAP"
    assert caught.value.field == "relations.0.dynamic_family"


def test_duplicate_undirected_relation_is_rejected(valid_config_dir: Path) -> None:
    path = valid_config_dir / "primitive_relation_graph_v1.yaml"
    data = _read_yaml(path)
    duplicate = dict(data["relations"][0])
    duplicate["left"], duplicate["right"] = duplicate["right"], duplicate["left"]
    data["relations"].append(duplicate)
    _write_yaml(path, data)

    with pytest.raises(ConfigError) as caught:
        load_runtime_config(valid_config_dir)

    assert caught.value.code == "CONFIG_DUPLICATE_RELATION"
