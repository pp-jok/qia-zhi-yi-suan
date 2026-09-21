from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest
import yaml

import destiny_personality
from destiny_personality.primitive_models import (
    PrimitiveDefinition,
    PrimitiveFoundationConfig,
    PrimitiveOntologyConfig,
    PrimitiveStateResolutionConfig,
)


POLICY_FILE = "dimension_coverage_policy_v1.yaml"


def _write(path: Path, data: object) -> None:
    with path.open("w", encoding="utf-8") as stream:
        yaml.safe_dump(data, stream, sort_keys=False)


def _read(path: Path) -> dict:
    with path.open(encoding="utf-8") as stream:
        return yaml.safe_load(stream)


@pytest.fixture
def primitive_foundation() -> PrimitiveFoundationConfig:
    ontology = PrimitiveOntologyConfig(
        schema_version="primitive-ontology-v1",
        ontology_version="test-only-ontology-1",
        primitives=(
            PrimitiveDefinition(
                primitive_id="P900",
                canonical_name="TEST_ONLY_PRIMITIVE",
                definition="TEST_ONLY_DEFINITION",
                high_expression="TEST_ONLY_HIGH",
                low_expression="TEST_ONLY_LOW",
                aliases=(),
                limitations=(),
            ),
        ),
    )
    resolution = PrimitiveStateResolutionConfig(
        schema_version="primitive-state-resolution-v1",
        resolution_version="test-only-resolution-1",
        ontology_version=ontology.ontology_version,
        score_model_version="2.2",
        states=("supported_high", "supported_low", "mixed", "unknown"),
        invariants=(),
        rules=(),
    )
    return PrimitiveFoundationConfig(ontology=ontology, resolution=resolution)


def _policy_data() -> dict:
    dimensions = [
        {
            "dimension_id": f"D{index:02d}",
            "canonical_name": f"TEST_ONLY_DIMENSION_{index:02d}",
            "definition": f"TEST_ONLY_DEFINITION_{index:02d}",
            "primitive_refs": ["P900"],
            "limitations": [],
        }
        for index in range(1, 13)
    ]
    return {
        "schema_version": "dimension-coverage-policy-v1",
        "policy_version": "test-only-policy-1",
        "ontology_version": "test-only-ontology-1",
        "score_model_version": "2.2",
        "dimension_count": 12,
        "dimensions": dimensions,
        "coverage_policy": {
            "threshold_status": "provisional",
            "coverage_metric": "TEST_ONLY_METRIC",
            "complete_threshold": 0.8,
            "partial_threshold": 0.4,
            "partial_portrait_allowed": True,
            "partial_status": "partial",
            "warning_code": "coverage_warning",
            "missing_config_code": "CONFIG_GAP",
            "dimension_requirements": [
                {
                    "dimension_id": item["dimension_id"],
                    "minimum_supported_primitives": 1,
                }
                for item in dimensions
            ],
        },
    }


@pytest.fixture
def policy_dir(tmp_path: Path) -> Path:
    _write(tmp_path / POLICY_FILE, _policy_data())
    return tmp_path


def _assert_error(policy_dir, foundation, runtime, code, field=None):
    with pytest.raises(destiny_personality.ConfigError) as caught:
        destiny_personality.load_dimension_coverage_policy(
            policy_dir, foundation, runtime
        )
    assert caught.value.code == code
    assert caught.value.file == POLICY_FILE
    assert caught.value.field == field


def test_load_dimension_policy_returns_immutable_twelve_dimension_config(
    policy_dir, primitive_foundation, runtime_config
) -> None:
    loader = getattr(destiny_personality, "load_dimension_coverage_policy", None)
    assert callable(loader), "public dimension coverage loader is missing"
    config = loader(policy_dir, primitive_foundation, runtime_config)
    assert config.dimension_count == 12
    assert tuple(item.dimension_id for item in config.dimensions) == tuple(
        f"D{index:02d}" for index in range(1, 13)
    )
    assert config.coverage_policy.threshold_status == "provisional"
    assert config.coverage_policy.dimension_requirements[0].dimension_id == "D01"
    with pytest.raises(FrozenInstanceError):
        config.policy_version = "changed"


def test_missing_policy_is_config_gap(tmp_path, primitive_foundation, runtime_config):
    _assert_error(tmp_path, primitive_foundation, runtime_config, "CONFIG_GAP")


def test_malformed_policy_is_parse_error(policy_dir, primitive_foundation, runtime_config):
    (policy_dir / POLICY_FILE).write_text("dimensions: [", encoding="utf-8")
    _assert_error(policy_dir, primitive_foundation, runtime_config, "CONFIG_PARSE_ERROR")


@pytest.mark.parametrize(
    ("field", "value"),
    (
        ("schema_version", "dimension-coverage-policy-v9"),
        ("ontology_version", "wrong"),
        ("score_model_version", "9.9"),
    ),
)
def test_versions_must_match(policy_dir, primitive_foundation, runtime_config, field, value):
    path = policy_dir / POLICY_FILE
    data = _read(path)
    data[field] = value
    _write(path, data)
    _assert_error(policy_dir, primitive_foundation, runtime_config, "CONFIG_VERSION_MISMATCH", field)


@pytest.mark.parametrize("count", (11, 13))
def test_exactly_twelve_dimensions_are_required(policy_dir, primitive_foundation, runtime_config, count):
    path = policy_dir / POLICY_FILE
    data = _read(path)
    data["dimensions"] = data["dimensions"][:count] if count < 12 else data["dimensions"] + [dict(data["dimensions"][-1])]
    data["dimension_count"] = count
    _write(path, data)
    _assert_error(policy_dir, primitive_foundation, runtime_config, "CONFIG_VALUE_ERROR", "dimension_count")


@pytest.mark.parametrize(
    ("mutation", "field"),
    (
        ("duplicate_id", "dimensions.1.dimension_id"),
        ("duplicate_name", "dimensions.1.canonical_name"),
        ("unknown_primitive", "dimensions.0.primitive_refs.0"),
        ("duplicate_primitive", "dimensions.0.primitive_refs.1"),
    ),
)
def test_dimension_identity_and_references(policy_dir, primitive_foundation, runtime_config, mutation, field):
    path = policy_dir / POLICY_FILE
    data = _read(path)
    if mutation == "duplicate_id": data["dimensions"][1]["dimension_id"] = "D01"
    elif mutation == "duplicate_name": data["dimensions"][1]["canonical_name"] = " test_only_dimension_01 "
    elif mutation == "unknown_primitive": data["dimensions"][0]["primitive_refs"][0] = "P999"
    else: data["dimensions"][0]["primitive_refs"].append("P900")
    _write(path, data)
    _assert_error(policy_dir, primitive_foundation, runtime_config, "CONFIG_VALUE_ERROR", field)


@pytest.mark.parametrize(
    ("field", "value", "code"),
    (
        ("threshold_status", "final", "CONFIG_VALUE_ERROR"),
        ("partial_portrait_allowed", False, "CONFIG_VALUE_ERROR"),
        ("partial_status", "complete", "CONFIG_VALUE_ERROR"),
        ("warning_code", "OTHER", "CONFIG_VALUE_ERROR"),
        ("missing_config_code", "coverage_warning", "CONFIG_VALUE_ERROR"),
        ("complete_threshold", 1.1, "CONFIG_VALUE_ERROR"),
        ("complete_threshold", True, "CONFIG_TYPE_ERROR"),
        ("partial_threshold", 0.8, "CONFIG_VALUE_ERROR"),
    ),
)
def test_coverage_policy_fixed_values_and_thresholds(policy_dir, primitive_foundation, runtime_config, field, value, code):
    path = policy_dir / POLICY_FILE
    data = _read(path)
    data["coverage_policy"][field] = value
    _write(path, data)
    _assert_error(policy_dir, primitive_foundation, runtime_config, code, f"coverage_policy.{field}")


@pytest.mark.parametrize(
    ("mutation", "field"),
    (
        ("missing", "coverage_policy.dimension_requirements"),
        ("duplicate", "coverage_policy.dimension_requirements.1.dimension_id"),
        ("unknown", "coverage_policy.dimension_requirements.0.dimension_id"),
        ("too_high", "coverage_policy.dimension_requirements.0.minimum_supported_primitives"),
        ("bool", "coverage_policy.dimension_requirements.0.minimum_supported_primitives"),
    ),
)
def test_dimension_requirements_are_complete_and_bounded(policy_dir, primitive_foundation, runtime_config, mutation, field):
    path = policy_dir / POLICY_FILE
    data = _read(path)
    requirements = data["coverage_policy"]["dimension_requirements"]
    if mutation == "missing": requirements.pop()
    elif mutation == "duplicate": requirements[1]["dimension_id"] = "D01"
    elif mutation == "unknown": requirements[0]["dimension_id"] = "D99"
    elif mutation == "too_high": requirements[0]["minimum_supported_primitives"] = 2
    else: requirements[0]["minimum_supported_primitives"] = True
    _write(path, data)
    _assert_error(policy_dir, primitive_foundation, runtime_config, "CONFIG_TYPE_ERROR" if mutation == "bool" else "CONFIG_VALUE_ERROR", field)
