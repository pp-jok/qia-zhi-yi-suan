from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest
import yaml

import destiny_personality


ONTOLOGY_FILE = "primitive_ontology_v1.yaml"
RESOLUTION_FILE = "primitive_state_resolution_v1.yaml"


def _write_yaml(path: Path, data: object) -> None:
    with path.open("w", encoding="utf-8") as stream:
        yaml.safe_dump(data, stream, allow_unicode=True, sort_keys=False)


def _read_yaml(path: Path) -> dict:
    with path.open(encoding="utf-8") as stream:
        return yaml.safe_load(stream)


def _assert_config_error(
    config_dir: Path,
    code: str,
    filename: str,
    field: str = None,
) -> None:
    with pytest.raises(destiny_personality.ConfigError) as caught:
        destiny_personality.load_primitive_foundation(config_dir)
    assert caught.value.code == code
    assert caught.value.file == filename
    assert caught.value.field == field


def _ontology_data() -> dict:
    return {
        "schema_version": "primitive-ontology-v1",
        "ontology_version": "test-only-ontology-1",
        "primitives": [
            {
                "primitive_id": "P900",
                "canonical_name": "TEST_ONLY_STRUCTURE",
                "definition": "TEST_ONLY_DEFINITION",
                "high_expression": "TEST_ONLY_HIGH",
                "low_expression": "TEST_ONLY_LOW",
                "aliases": ["TEST_ONLY_ALIAS"],
                "limitations": ["TEST_ONLY_LIMITATION"],
            }
        ],
    }


def _resolution_data() -> dict:
    states = ["supported_high", "supported_low", "mixed", "unknown"]
    return {
        "schema_version": "primitive-state-resolution-v1",
        "resolution_version": "test-only-resolution-1",
        "ontology_version": "test-only-ontology-1",
        "score_model_version": "2.2",
        "states": states,
        "invariants": {
            "no_evidence_state": "unknown",
            "low_requires_explicit_reverse_evidence": True,
            "unknown_is_not_low": True,
            "preserve_system_salience": True,
            "cross_system_validation_changes_trait_salience": False,
            "tension_reduces_trait_salience": False,
        },
        "rules": [
            {
                "rule_id": f"TEST_ONLY_{state.upper()}",
                "target_state": state,
                "priority": index * 10,
                "description": f"TEST_ONLY_{state}_RULE",
                "requires_explicit_reverse_evidence": state == "supported_low",
                "evidence_requirements": {"test_only_mode": state},
                "thresholds": {},
                "limitations": [],
            }
            for index, state in enumerate(states, start=1)
        ],
    }


@pytest.fixture
def primitive_config_dir(tmp_path: Path) -> Path:
    _write_yaml(tmp_path / ONTOLOGY_FILE, _ontology_data())
    _write_yaml(tmp_path / RESOLUTION_FILE, _resolution_data())
    return tmp_path


def test_load_primitive_foundation_returns_immutable_bundle(
    primitive_config_dir: Path,
) -> None:
    loader = getattr(destiny_personality, "load_primitive_foundation", None)
    assert callable(loader), "public Primitive foundation loader is missing"

    bundle = loader(primitive_config_dir)

    assert bundle.ontology.schema_version == "primitive-ontology-v1"
    assert bundle.ontology.primitives[0].primitive_id == "P900"
    assert bundle.ontology.primitives[0].aliases == ("TEST_ONLY_ALIAS",)
    assert bundle.resolution.states == (
        "supported_high",
        "supported_low",
        "mixed",
        "unknown",
    )
    assert bundle.resolution.ontology_version == bundle.ontology.ontology_version
    assert bundle.resolution.rules[0].priority == 10
    assert isinstance(bundle.resolution.invariants, tuple)
    assert isinstance(bundle.resolution.rules[0].evidence_requirements, tuple)
    with pytest.raises(FrozenInstanceError):
        bundle.ontology.ontology_version = "changed"


def test_missing_ontology_is_config_gap(primitive_config_dir: Path) -> None:
    (primitive_config_dir / ONTOLOGY_FILE).unlink()
    _assert_config_error(primitive_config_dir, "CONFIG_GAP", ONTOLOGY_FILE)


def test_missing_resolution_is_config_gap(primitive_config_dir: Path) -> None:
    (primitive_config_dir / RESOLUTION_FILE).unlink()
    _assert_config_error(primitive_config_dir, "CONFIG_GAP", RESOLUTION_FILE)


def test_missing_required_primitive_field_is_config_gap(
    primitive_config_dir: Path,
) -> None:
    path = primitive_config_dir / ONTOLOGY_FILE
    data = _read_yaml(path)
    del data["primitives"][0]["definition"]
    _write_yaml(path, data)
    _assert_config_error(
        primitive_config_dir,
        "CONFIG_GAP",
        ONTOLOGY_FILE,
        "primitives.0.definition",
    )


def test_malformed_ontology_is_parse_error(primitive_config_dir: Path) -> None:
    (primitive_config_dir / ONTOLOGY_FILE).write_text("primitives: [", encoding="utf-8")
    _assert_config_error(primitive_config_dir, "CONFIG_PARSE_ERROR", ONTOLOGY_FILE)


def test_non_mapping_ontology_root_is_type_error(
    primitive_config_dir: Path,
) -> None:
    _write_yaml(primitive_config_dir / ONTOLOGY_FILE, [])
    _assert_config_error(primitive_config_dir, "CONFIG_TYPE_ERROR", ONTOLOGY_FILE)


def test_malformed_resolution_is_parse_error(primitive_config_dir: Path) -> None:
    (primitive_config_dir / RESOLUTION_FILE).write_text("rules: [", encoding="utf-8")
    _assert_config_error(primitive_config_dir, "CONFIG_PARSE_ERROR", RESOLUTION_FILE)


def test_non_mapping_resolution_root_is_type_error(
    primitive_config_dir: Path,
) -> None:
    _write_yaml(primitive_config_dir / RESOLUTION_FILE, [])
    _assert_config_error(primitive_config_dir, "CONFIG_TYPE_ERROR", RESOLUTION_FILE)


def test_unsupported_ontology_schema_is_version_mismatch(
    primitive_config_dir: Path,
) -> None:
    path = primitive_config_dir / ONTOLOGY_FILE
    data = _read_yaml(path)
    data["schema_version"] = "primitive-ontology-v9"
    _write_yaml(path, data)
    _assert_config_error(
        primitive_config_dir,
        "CONFIG_VERSION_MISMATCH",
        ONTOLOGY_FILE,
        "schema_version",
    )


def test_unsupported_resolution_schema_is_version_mismatch(
    primitive_config_dir: Path,
) -> None:
    path = primitive_config_dir / RESOLUTION_FILE
    data = _read_yaml(path)
    data["schema_version"] = "primitive-state-resolution-v9"
    _write_yaml(path, data)
    _assert_config_error(
        primitive_config_dir,
        "CONFIG_VERSION_MISMATCH",
        RESOLUTION_FILE,
        "schema_version",
    )


def test_missing_required_resolution_field_is_config_gap(
    primitive_config_dir: Path,
) -> None:
    path = primitive_config_dir / RESOLUTION_FILE
    data = _read_yaml(path)
    del data["rules"][0]["description"]
    _write_yaml(path, data)
    _assert_config_error(
        primitive_config_dir,
        "CONFIG_GAP",
        RESOLUTION_FILE,
        "rules.0.description",
    )


def test_empty_primitive_list_is_value_error(primitive_config_dir: Path) -> None:
    path = primitive_config_dir / ONTOLOGY_FILE
    data = _read_yaml(path)
    data["primitives"] = []
    _write_yaml(path, data)
    _assert_config_error(
        primitive_config_dir, "CONFIG_VALUE_ERROR", ONTOLOGY_FILE, "primitives"
    )


@pytest.mark.parametrize("primitive_id", ["P90", "p900", "P0900"])
def test_invalid_primitive_id_is_value_error(
    primitive_config_dir: Path, primitive_id: str
) -> None:
    path = primitive_config_dir / ONTOLOGY_FILE
    data = _read_yaml(path)
    data["primitives"][0]["primitive_id"] = primitive_id
    _write_yaml(path, data)
    _assert_config_error(
        primitive_config_dir,
        "CONFIG_VALUE_ERROR",
        ONTOLOGY_FILE,
        "primitives.0.primitive_id",
    )


def test_duplicate_primitive_id_is_value_error(primitive_config_dir: Path) -> None:
    path = primitive_config_dir / ONTOLOGY_FILE
    data = _read_yaml(path)
    duplicate = dict(data["primitives"][0])
    duplicate["canonical_name"] = "TEST_ONLY_SECOND"
    duplicate["aliases"] = []
    data["primitives"].append(duplicate)
    _write_yaml(path, data)
    _assert_config_error(
        primitive_config_dir,
        "CONFIG_VALUE_ERROR",
        ONTOLOGY_FILE,
        "primitives.1.primitive_id",
    )


def test_alias_cannot_collide_with_another_canonical_name(
    primitive_config_dir: Path,
) -> None:
    path = primitive_config_dir / ONTOLOGY_FILE
    data = _read_yaml(path)
    data["primitives"].append(
        {
            "primitive_id": "P901",
            "canonical_name": " test_only_alias ",
            "definition": "TEST_ONLY_SECOND_DEFINITION",
            "high_expression": "TEST_ONLY_SECOND_HIGH",
            "low_expression": "TEST_ONLY_SECOND_LOW",
            "aliases": [],
            "limitations": [],
        }
    )
    _write_yaml(path, data)
    _assert_config_error(
        primitive_config_dir,
        "CONFIG_VALUE_ERROR",
        ONTOLOGY_FILE,
        "primitives.1.canonical_name",
    )


def test_identical_high_and_low_expression_is_value_error(
    primitive_config_dir: Path,
) -> None:
    path = primitive_config_dir / ONTOLOGY_FILE
    data = _read_yaml(path)
    data["primitives"][0]["low_expression"] = " TEST_ONLY_HIGH "
    _write_yaml(path, data)
    _assert_config_error(
        primitive_config_dir,
        "CONFIG_VALUE_ERROR",
        ONTOLOGY_FILE,
        "primitives.0.low_expression",
    )


@pytest.mark.parametrize(
    ("field", "value"),
    (
        ("ontology_version", "wrong-ontology"),
        ("score_model_version", "9.9"),
    ),
)
def test_resolution_version_references_must_match(
    primitive_config_dir: Path, field: str, value: str
) -> None:
    path = primitive_config_dir / RESOLUTION_FILE
    data = _read_yaml(path)
    data[field] = value
    _write_yaml(path, data)
    _assert_config_error(
        primitive_config_dir,
        "CONFIG_VERSION_MISMATCH",
        RESOLUTION_FILE,
        field,
    )


def test_states_must_match_exact_wire_set(primitive_config_dir: Path) -> None:
    path = primitive_config_dir / RESOLUTION_FILE
    data = _read_yaml(path)
    data["states"][-1] = "unsupported_state"
    _write_yaml(path, data)
    _assert_config_error(
        primitive_config_dir, "CONFIG_VALUE_ERROR", RESOLUTION_FILE, "states"
    )


def test_duplicate_state_is_value_error(primitive_config_dir: Path) -> None:
    path = primitive_config_dir / RESOLUTION_FILE
    data = _read_yaml(path)
    data["states"][-1] = data["states"][0]
    _write_yaml(path, data)
    _assert_config_error(
        primitive_config_dir, "CONFIG_VALUE_ERROR", RESOLUTION_FILE, "states"
    )


def test_state_values_must_be_strings(primitive_config_dir: Path) -> None:
    path = primitive_config_dir / RESOLUTION_FILE
    data = _read_yaml(path)
    data["states"][0] = True
    _write_yaml(path, data)
    _assert_config_error(
        primitive_config_dir, "CONFIG_TYPE_ERROR", RESOLUTION_FILE, "states.0"
    )


@pytest.mark.parametrize(
    ("invariant", "value"),
    (
        ("no_evidence_state", "supported_low"),
        ("low_requires_explicit_reverse_evidence", False),
        ("unknown_is_not_low", False),
        ("preserve_system_salience", False),
        ("cross_system_validation_changes_trait_salience", True),
        ("tension_reduces_trait_salience", True),
    ),
)
def test_safety_invariants_are_exact(
    primitive_config_dir: Path, invariant: str, value: object
) -> None:
    path = primitive_config_dir / RESOLUTION_FILE
    data = _read_yaml(path)
    data["invariants"][invariant] = value
    _write_yaml(path, data)
    _assert_config_error(
        primitive_config_dir,
        "CONFIG_VALUE_ERROR",
        RESOLUTION_FILE,
        f"invariants.{invariant}",
    )


def test_rules_must_cover_every_state(primitive_config_dir: Path) -> None:
    path = primitive_config_dir / RESOLUTION_FILE
    data = _read_yaml(path)
    data["rules"] = data["rules"][:-1]
    _write_yaml(path, data)
    _assert_config_error(
        primitive_config_dir, "CONFIG_VALUE_ERROR", RESOLUTION_FILE, "rules"
    )


def test_duplicate_rule_id_is_value_error(primitive_config_dir: Path) -> None:
    path = primitive_config_dir / RESOLUTION_FILE
    data = _read_yaml(path)
    data["rules"][1]["rule_id"] = data["rules"][0]["rule_id"]
    _write_yaml(path, data)
    _assert_config_error(
        primitive_config_dir,
        "CONFIG_VALUE_ERROR",
        RESOLUTION_FILE,
        "rules.1.rule_id",
    )


def test_boolean_rule_priority_is_type_error(primitive_config_dir: Path) -> None:
    path = primitive_config_dir / RESOLUTION_FILE
    data = _read_yaml(path)
    data["rules"][0]["priority"] = True
    _write_yaml(path, data)
    _assert_config_error(
        primitive_config_dir,
        "CONFIG_TYPE_ERROR",
        RESOLUTION_FILE,
        "rules.0.priority",
    )


def test_duplicate_rule_priority_is_value_error(primitive_config_dir: Path) -> None:
    path = primitive_config_dir / RESOLUTION_FILE
    data = _read_yaml(path)
    data["rules"][1]["priority"] = data["rules"][0]["priority"]
    _write_yaml(path, data)
    _assert_config_error(
        primitive_config_dir,
        "CONFIG_VALUE_ERROR",
        RESOLUTION_FILE,
        "rules.1.priority",
    )


def test_duplicate_rule_precedes_later_rule_type_error(
    primitive_config_dir: Path,
) -> None:
    path = primitive_config_dir / RESOLUTION_FILE
    data = _read_yaml(path)
    data["rules"][1]["rule_id"] = data["rules"][0]["rule_id"]
    data["rules"][2]["priority"] = True
    _write_yaml(path, data)
    _assert_config_error(
        primitive_config_dir,
        "CONFIG_VALUE_ERROR",
        RESOLUTION_FILE,
        "rules.1.rule_id",
    )


def test_supported_low_requires_reverse_evidence_marker(
    primitive_config_dir: Path,
) -> None:
    path = primitive_config_dir / RESOLUTION_FILE
    data = _read_yaml(path)
    low_rule = next(
        rule for rule in data["rules"] if rule["target_state"] == "supported_low"
    )
    low_rule["requires_explicit_reverse_evidence"] = False
    low_index = data["rules"].index(low_rule)
    _write_yaml(path, data)
    _assert_config_error(
        primitive_config_dir,
        "CONFIG_VALUE_ERROR",
        RESOLUTION_FILE,
        f"rules.{low_index}.requires_explicit_reverse_evidence",
    )


def test_rules_are_returned_in_priority_order(primitive_config_dir: Path) -> None:
    path = primitive_config_dir / RESOLUTION_FILE
    data = _read_yaml(path)
    data["rules"].reverse()
    _write_yaml(path, data)

    bundle = destiny_personality.load_primitive_foundation(primitive_config_dir)

    assert tuple(rule.priority for rule in bundle.resolution.rules) == (10, 20, 30, 40)


def test_evidence_requirements_must_not_be_empty(
    primitive_config_dir: Path,
) -> None:
    path = primitive_config_dir / RESOLUTION_FILE
    data = _read_yaml(path)
    data["rules"][0]["evidence_requirements"] = {}
    _write_yaml(path, data)
    _assert_config_error(
        primitive_config_dir,
        "CONFIG_VALUE_ERROR",
        RESOLUTION_FILE,
        "rules.0.evidence_requirements",
    )


def test_rule_thresholds_must_be_a_mapping(primitive_config_dir: Path) -> None:
    path = primitive_config_dir / RESOLUTION_FILE
    data = _read_yaml(path)
    data["rules"][0]["thresholds"] = []
    _write_yaml(path, data)
    _assert_config_error(
        primitive_config_dir,
        "CONFIG_TYPE_ERROR",
        RESOLUTION_FILE,
        "rules.0.thresholds",
    )


def test_non_string_unknown_key_is_a_type_error(primitive_config_dir: Path) -> None:
    path = primitive_config_dir / ONTOLOGY_FILE
    data = _read_yaml(path)
    data[7] = "TEST_ONLY_INTEGER_KEY"
    data["unexpected"] = "TEST_ONLY_STRING_KEY"
    _write_yaml(path, data)
    _assert_config_error(
        primitive_config_dir, "CONFIG_TYPE_ERROR", ONTOLOGY_FILE, "7"
    )


@pytest.mark.parametrize(
    ("filename", "section", "field"),
    (
        (ONTOLOGY_FILE, None, "unexpected"),
        (ONTOLOGY_FILE, "primitives", "unexpected"),
        (RESOLUTION_FILE, None, "unexpected"),
        (RESOLUTION_FILE, "rules", "unexpected"),
    ),
)
def test_unknown_fields_are_rejected(
    primitive_config_dir: Path, filename: str, section: str, field: str
) -> None:
    path = primitive_config_dir / filename
    data = _read_yaml(path)
    if section is None:
        data[field] = "TEST_ONLY"
        expected_field = field
    else:
        data[section][0][field] = "TEST_ONLY"
        expected_field = f"{section}.0.{field}"
    _write_yaml(path, data)
    _assert_config_error(
        primitive_config_dir,
        "CONFIG_VALUE_ERROR",
        filename,
        expected_field,
    )
