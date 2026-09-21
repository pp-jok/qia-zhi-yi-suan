from dataclasses import FrozenInstanceError
from datetime import date
from pathlib import Path

import pytest
import yaml

import destiny_personality


BAZI_FILE = "bazi_mapping_registry_v1.yaml"
ASTROLOGY_FILE = "astrology_mapping_registry_v1.yaml"
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
    primitive_foundation,
    runtime_config,
    code: str,
    filename: str,
    field: str = None,
) -> None:
    with pytest.raises(destiny_personality.ConfigError) as caught:
        destiny_personality.load_mapping_registries(
            config_dir,
            primitive_foundation,
            runtime_config,
        )
    assert caught.value.code == code
    assert caught.value.file == filename
    assert caught.value.field == field


def _ontology_data() -> dict:
    return {
        "schema_version": "primitive-ontology-v1",
        "ontology_version": "test-only-ontology-1",
        "primitives": [
            {
                "primitive_id": primitive_id,
                "canonical_name": f"TEST_ONLY_NAME_{primitive_id}",
                "definition": f"TEST_ONLY_DEFINITION_{primitive_id}",
                "high_expression": f"TEST_ONLY_HIGH_{primitive_id}",
                "low_expression": f"TEST_ONLY_LOW_{primitive_id}",
                "aliases": [],
                "limitations": [],
            }
            for primitive_id in ("P900", "P901")
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
                "rule_id": f"TEST_ONLY_STATE_{state.upper()}",
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


def _mapping_rule(source: str, number: int, primitive_id: str) -> dict:
    return {
        "rule_id": f"TEST_ONLY_{source.upper()}_R{number}",
        "priority": number * 10,
        "primary_condition": {"feature": f"TEST_ONLY_{source.upper()}_FEATURE_{number}"},
        "context": {"all": [{"test_only_context": True}]},
        "outputs": [
            {
                "primitive_id": primitive_id,
                "direction": "TEST_ONLY_INCREASE",
                "salience": number,
                "limitations": [],
            }
        ],
        "modifiers": [
            {
                "when": {"test_only_modifier": True},
                "effects": [{"test_only_effect": "TEST_ONLY_VALUE"}],
            }
        ],
        "limitations": [],
    }


def _registry_data(source: str) -> dict:
    methodology_version = {
        "bazi": "bazi-core-v1.0",
        "astrology": "western-tropical-v1.0",
    }[source]
    rules = [
        _mapping_rule(source, 1, "P900"),
        _mapping_rule(source, 2, "P901"),
    ]
    return {
        "schema_version": "context-aware-mapping-registry-v1",
        "registry_version": f"test-only-{source}-registry-1",
        "source_system": source,
        "methodology_version": methodology_version,
        "fact_schema_version": "deterministic-facts-v1",
        "score_model_version": "2.2",
        "ontology_version": "test-only-ontology-1",
        "rules": rules,
        "interactions": [
            {
                "interaction_id": f"TEST_ONLY_{source.upper()}_I1",
                "requires": [rules[0]["rule_id"], rules[1]["rule_id"]],
                "produces": {"signature_hint": "TEST_ONLY_SIGNATURE"},
                "limitations": [],
            }
        ],
    }


@pytest.fixture
def primitive_foundation(valid_config_dir: Path):
    _write_yaml(valid_config_dir / ONTOLOGY_FILE, _ontology_data())
    _write_yaml(valid_config_dir / RESOLUTION_FILE, _resolution_data())
    return destiny_personality.load_primitive_foundation(valid_config_dir)


@pytest.fixture
def mapping_config_dir(valid_config_dir: Path) -> Path:
    _write_yaml(valid_config_dir / BAZI_FILE, _registry_data("bazi"))
    _write_yaml(valid_config_dir / ASTROLOGY_FILE, _registry_data("astrology"))
    return valid_config_dir


def test_load_mapping_registries_returns_immutable_source_isolated_bundle(
    mapping_config_dir: Path,
    primitive_foundation,
    runtime_config,
) -> None:
    loader = getattr(destiny_personality, "load_mapping_registries", None)
    assert callable(loader), "public Mapping Registry loader is missing"

    bundle = loader(mapping_config_dir, primitive_foundation, runtime_config)

    assert bundle.bazi.source_system == "bazi"
    assert bundle.astrology.source_system == "astrology"
    assert bundle.bazi.score_model_version == "2.2"
    assert bundle.bazi.rules[0].outputs[0].primitive_id == "P900"
    assert bundle.bazi.rules[0].primary_condition == (
        ("feature", "TEST_ONLY_BAZI_FEATURE_1"),
    )
    assert bundle.bazi.rules[0].modifiers[0].effects == (
        (("test_only_effect", "TEST_ONLY_VALUE"),),
    )
    assert bundle.bazi.interactions[0].requires == (
        "TEST_ONLY_BAZI_R1",
        "TEST_ONLY_BAZI_R2",
    )
    with pytest.raises(FrozenInstanceError):
        bundle.bazi.registry_version = "changed"


@pytest.mark.parametrize("filename", (BAZI_FILE, ASTROLOGY_FILE))
def test_missing_registry_is_config_gap(
    mapping_config_dir: Path,
    primitive_foundation,
    runtime_config,
    filename: str,
) -> None:
    (mapping_config_dir / filename).unlink()
    _assert_config_error(
        mapping_config_dir,
        primitive_foundation,
        runtime_config,
        "CONFIG_GAP",
        filename,
    )


def test_bazi_file_is_checked_before_astrology_file(
    mapping_config_dir: Path,
    primitive_foundation,
    runtime_config,
) -> None:
    (mapping_config_dir / BAZI_FILE).unlink()
    (mapping_config_dir / ASTROLOGY_FILE).write_text("rules: [", encoding="utf-8")
    _assert_config_error(
        mapping_config_dir,
        primitive_foundation,
        runtime_config,
        "CONFIG_GAP",
        BAZI_FILE,
    )


@pytest.mark.parametrize("filename", (BAZI_FILE, ASTROLOGY_FILE))
def test_malformed_registry_is_parse_error(
    mapping_config_dir: Path,
    primitive_foundation,
    runtime_config,
    filename: str,
) -> None:
    (mapping_config_dir / filename).write_text("rules: [", encoding="utf-8")
    _assert_config_error(
        mapping_config_dir,
        primitive_foundation,
        runtime_config,
        "CONFIG_PARSE_ERROR",
        filename,
    )


def test_non_mapping_registry_root_is_type_error(
    mapping_config_dir: Path,
    primitive_foundation,
    runtime_config,
) -> None:
    _write_yaml(mapping_config_dir / BAZI_FILE, [])
    _assert_config_error(
        mapping_config_dir,
        primitive_foundation,
        runtime_config,
        "CONFIG_TYPE_ERROR",
        BAZI_FILE,
    )


@pytest.mark.parametrize(
    ("section", "field", "expected_field"),
    (
        (None, "registry_version", "registry_version"),
        ("rules", "context", "rules.0.context"),
        ("outputs", "direction", "rules.0.outputs.0.direction"),
        ("modifiers", "effects", "rules.0.modifiers.0.effects"),
        ("interactions", "produces", "interactions.0.produces"),
    ),
)
def test_missing_required_fields_are_config_gap(
    mapping_config_dir: Path,
    primitive_foundation,
    runtime_config,
    section: str,
    field: str,
    expected_field: str,
) -> None:
    path = mapping_config_dir / BAZI_FILE
    data = _read_yaml(path)
    if section is None:
        del data[field]
    elif section == "rules":
        del data["rules"][0][field]
    elif section == "outputs":
        del data["rules"][0]["outputs"][0][field]
    elif section == "modifiers":
        del data["rules"][0]["modifiers"][0][field]
    else:
        del data["interactions"][0][field]
    _write_yaml(path, data)
    _assert_config_error(
        mapping_config_dir,
        primitive_foundation,
        runtime_config,
        "CONFIG_GAP",
        BAZI_FILE,
        expected_field,
    )


@pytest.mark.parametrize(
    ("field", "value"),
    (
        ("schema_version", "context-aware-mapping-registry-v9"),
        ("source_system", "astrology"),
        ("methodology_version", "test-only-wrong-method"),
        ("fact_schema_version", "deterministic-facts-v9"),
        ("score_model_version", "9.9"),
        ("ontology_version", "test-only-wrong-ontology"),
    ),
)
def test_registry_version_references_must_match(
    mapping_config_dir: Path,
    primitive_foundation,
    runtime_config,
    field: str,
    value: str,
) -> None:
    path = mapping_config_dir / BAZI_FILE
    data = _read_yaml(path)
    data[field] = value
    _write_yaml(path, data)
    _assert_config_error(
        mapping_config_dir,
        primitive_foundation,
        runtime_config,
        "CONFIG_VERSION_MISMATCH",
        BAZI_FILE,
        field,
    )


@pytest.mark.parametrize(
    ("location", "expected_field"),
    (
        ("root", "unexpected"),
        ("rule", "rules.0.unexpected"),
        ("output", "rules.0.outputs.0.unexpected"),
        ("modifier", "rules.0.modifiers.0.unexpected"),
        ("interaction", "interactions.0.unexpected"),
    ),
)
def test_unknown_fields_are_value_error(
    mapping_config_dir: Path,
    primitive_foundation,
    runtime_config,
    location: str,
    expected_field: str,
) -> None:
    path = mapping_config_dir / BAZI_FILE
    data = _read_yaml(path)
    target = {
        "root": data,
        "rule": data["rules"][0],
        "output": data["rules"][0]["outputs"][0],
        "modifier": data["rules"][0]["modifiers"][0],
        "interaction": data["interactions"][0],
    }[location]
    target["unexpected"] = "TEST_ONLY_VALUE"
    _write_yaml(path, data)
    _assert_config_error(
        mapping_config_dir,
        primitive_foundation,
        runtime_config,
        "CONFIG_VALUE_ERROR",
        BAZI_FILE,
        expected_field,
    )


@pytest.mark.parametrize(
    ("mutation", "expected_field"),
    (
        ("rules", "rules"),
        ("context", "rules.0.context"),
        ("outputs", "rules.0.outputs"),
        ("modifier_when", "rules.0.modifiers.0.when"),
        ("modifier_effects", "rules.0.modifiers.0.effects"),
        ("interaction_produces", "interactions.0.produces"),
    ),
)
def test_required_collections_must_not_be_empty(
    mapping_config_dir: Path,
    primitive_foundation,
    runtime_config,
    mutation: str,
    expected_field: str,
) -> None:
    path = mapping_config_dir / BAZI_FILE
    data = _read_yaml(path)
    if mutation == "rules":
        data["rules"] = []
    elif mutation == "context":
        data["rules"][0]["context"] = {}
    elif mutation == "outputs":
        data["rules"][0]["outputs"] = []
    elif mutation == "modifier_when":
        data["rules"][0]["modifiers"][0]["when"] = {}
    elif mutation == "modifier_effects":
        data["rules"][0]["modifiers"][0]["effects"] = []
    else:
        data["interactions"][0]["produces"] = {}
    _write_yaml(path, data)
    _assert_config_error(
        mapping_config_dir,
        primitive_foundation,
        runtime_config,
        "CONFIG_VALUE_ERROR",
        BAZI_FILE,
        expected_field,
    )


def test_duplicate_rule_id_is_value_error(
    mapping_config_dir: Path,
    primitive_foundation,
    runtime_config,
) -> None:
    path = mapping_config_dir / BAZI_FILE
    data = _read_yaml(path)
    data["rules"][1]["rule_id"] = data["rules"][0]["rule_id"]
    _write_yaml(path, data)
    _assert_config_error(
        mapping_config_dir,
        primitive_foundation,
        runtime_config,
        "CONFIG_VALUE_ERROR",
        BAZI_FILE,
        "rules.1.rule_id",
    )


def test_duplicate_rule_priority_is_value_error(
    mapping_config_dir: Path,
    primitive_foundation,
    runtime_config,
) -> None:
    path = mapping_config_dir / BAZI_FILE
    data = _read_yaml(path)
    data["rules"][1]["priority"] = data["rules"][0]["priority"]
    _write_yaml(path, data)
    _assert_config_error(
        mapping_config_dir,
        primitive_foundation,
        runtime_config,
        "CONFIG_VALUE_ERROR",
        BAZI_FILE,
        "rules.1.priority",
    )


def test_boolean_rule_priority_is_type_error(
    mapping_config_dir: Path,
    primitive_foundation,
    runtime_config,
) -> None:
    path = mapping_config_dir / BAZI_FILE
    data = _read_yaml(path)
    data["rules"][0]["priority"] = True
    _write_yaml(path, data)
    _assert_config_error(
        mapping_config_dir,
        primitive_foundation,
        runtime_config,
        "CONFIG_TYPE_ERROR",
        BAZI_FILE,
        "rules.0.priority",
    )


def test_rules_are_returned_in_priority_order(
    mapping_config_dir: Path,
    primitive_foundation,
    runtime_config,
) -> None:
    path = mapping_config_dir / BAZI_FILE
    data = _read_yaml(path)
    data["rules"].reverse()
    _write_yaml(path, data)

    bundle = destiny_personality.load_mapping_registries(
        mapping_config_dir,
        primitive_foundation,
        runtime_config,
    )

    assert tuple(rule.priority for rule in bundle.bazi.rules) == (10, 20)


@pytest.mark.parametrize(
    ("mutation", "expected_field"),
    (
        ("unknown", "rules.0.outputs.0.primitive_id"),
        ("duplicate", "rules.0.outputs.1.primitive_id"),
    ),
)
def test_output_primitive_references_must_resolve_and_be_unique(
    mapping_config_dir: Path,
    primitive_foundation,
    runtime_config,
    mutation: str,
    expected_field: str,
) -> None:
    path = mapping_config_dir / BAZI_FILE
    data = _read_yaml(path)
    if mutation == "unknown":
        data["rules"][0]["outputs"][0]["primitive_id"] = "P999"
    else:
        data["rules"][0]["outputs"].append(
            dict(data["rules"][0]["outputs"][0])
        )
    _write_yaml(path, data)
    _assert_config_error(
        mapping_config_dir,
        primitive_foundation,
        runtime_config,
        "CONFIG_VALUE_ERROR",
        BAZI_FILE,
        expected_field,
    )


@pytest.mark.parametrize("salience", (-1, 5))
def test_output_salience_must_match_score_bounds(
    mapping_config_dir: Path,
    primitive_foundation,
    runtime_config,
    salience: int,
) -> None:
    path = mapping_config_dir / BAZI_FILE
    data = _read_yaml(path)
    data["rules"][0]["outputs"][0]["salience"] = salience
    _write_yaml(path, data)
    _assert_config_error(
        mapping_config_dir,
        primitive_foundation,
        runtime_config,
        "CONFIG_VALUE_ERROR",
        BAZI_FILE,
        "rules.0.outputs.0.salience",
    )


def test_boolean_output_salience_is_type_error(
    mapping_config_dir: Path,
    primitive_foundation,
    runtime_config,
) -> None:
    path = mapping_config_dir / BAZI_FILE
    data = _read_yaml(path)
    data["rules"][0]["outputs"][0]["salience"] = True
    _write_yaml(path, data)
    _assert_config_error(
        mapping_config_dir,
        primitive_foundation,
        runtime_config,
        "CONFIG_TYPE_ERROR",
        BAZI_FILE,
        "rules.0.outputs.0.salience",
    )


@pytest.mark.parametrize(
    ("nested_value", "expected_field"),
    (
        ({7: "TEST_ONLY_VALUE"}, "rules.0.context.7"),
        (date(2026, 9, 13), "rules.0.context.test_only_bad"),
        (float("nan"), "rules.0.context.test_only_bad"),
    ),
)
def test_nested_declarative_values_are_type_checked(
    mapping_config_dir: Path,
    primitive_foundation,
    runtime_config,
    nested_value: object,
    expected_field: str,
) -> None:
    path = mapping_config_dir / BAZI_FILE
    data = _read_yaml(path)
    if isinstance(nested_value, dict):
        data["rules"][0]["context"] = nested_value
    else:
        data["rules"][0]["context"]["test_only_bad"] = nested_value
    _write_yaml(path, data)
    _assert_config_error(
        mapping_config_dir,
        primitive_foundation,
        runtime_config,
        "CONFIG_TYPE_ERROR",
        BAZI_FILE,
        expected_field,
    )


@pytest.mark.parametrize(
    ("requires", "expected_field"),
    (
        (["TEST_ONLY_BAZI_R1"], "interactions.0.requires"),
        (
            ["TEST_ONLY_BAZI_R1", "TEST_ONLY_BAZI_R1"],
            "interactions.0.requires.1",
        ),
        (
            ["TEST_ONLY_BAZI_R1", "TEST_ONLY_ASTROLOGY_R1"],
            "interactions.0.requires.1",
        ),
    ),
)
def test_interaction_requires_two_distinct_local_rules(
    mapping_config_dir: Path,
    primitive_foundation,
    runtime_config,
    requires: list,
    expected_field: str,
) -> None:
    path = mapping_config_dir / BAZI_FILE
    data = _read_yaml(path)
    data["interactions"][0]["requires"] = requires
    _write_yaml(path, data)
    _assert_config_error(
        mapping_config_dir,
        primitive_foundation,
        runtime_config,
        "CONFIG_VALUE_ERROR",
        BAZI_FILE,
        expected_field,
    )


def test_duplicate_interaction_id_is_value_error(
    mapping_config_dir: Path,
    primitive_foundation,
    runtime_config,
) -> None:
    path = mapping_config_dir / BAZI_FILE
    data = _read_yaml(path)
    data["interactions"].append(dict(data["interactions"][0]))
    _write_yaml(path, data)
    _assert_config_error(
        mapping_config_dir,
        primitive_foundation,
        runtime_config,
        "CONFIG_VALUE_ERROR",
        BAZI_FILE,
        "interactions.1.interaction_id",
    )


@pytest.mark.parametrize(
    ("kind", "expected_field"),
    (
        ("rule", "rules.0.rule_id"),
        ("interaction", "interactions.0.interaction_id"),
    ),
)
def test_identifiers_are_globally_unique_across_registries(
    mapping_config_dir: Path,
    primitive_foundation,
    runtime_config,
    kind: str,
    expected_field: str,
) -> None:
    bazi = _read_yaml(mapping_config_dir / BAZI_FILE)
    astrology_path = mapping_config_dir / ASTROLOGY_FILE
    astrology = _read_yaml(astrology_path)
    if kind == "rule":
        astrology["rules"][0]["rule_id"] = bazi["rules"][0]["rule_id"]
        astrology["interactions"][0]["requires"][0] = bazi["rules"][0]["rule_id"]
    else:
        astrology["interactions"][0]["interaction_id"] = bazi["interactions"][0][
            "interaction_id"
        ]
    _write_yaml(astrology_path, astrology)
    _assert_config_error(
        mapping_config_dir,
        primitive_foundation,
        runtime_config,
        "CONFIG_VALUE_ERROR",
        ASTROLOGY_FILE,
        expected_field,
    )
