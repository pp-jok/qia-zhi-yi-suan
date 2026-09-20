from pathlib import Path
import math
import re
from typing import Any, Dict, Optional, Set, Tuple

import yaml

from .config_errors import ConfigError
from .config_models import RuntimeConfig
from .dimension_models import (
    CoveragePolicy,
    DimensionCoveragePolicyConfig,
    DimensionDefinition,
    DimensionRequirement,
)
from .primitive_models import PrimitiveFoundationConfig


POLICY_FILE = "dimension_coverage_policy_v1.yaml"
SCHEMA_VERSION = "dimension-coverage-policy-v1"
DIMENSION_ID_PATTERN = re.compile(r"D[0-9]{2}")
ROOT_KEYS = {"schema_version", "policy_version", "ontology_version", "score_model_version", "dimension_count", "dimensions", "coverage_policy"}
DIMENSION_KEYS = {"dimension_id", "canonical_name", "definition", "primitive_refs", "limitations"}
POLICY_KEYS = {"threshold_status", "coverage_metric", "complete_threshold", "partial_threshold", "partial_portrait_allowed", "partial_status", "warning_code", "missing_config_code", "dimension_requirements"}
REQUIREMENT_KEYS = {"dimension_id", "minimum_supported_primitives"}


def _error(code: str, message: str, field: Optional[str] = None) -> ConfigError:
    return ConfigError(code, message, file=POLICY_FILE, field=field)


def _mapping(value: Any, field: Optional[str] = None) -> Dict[str, Any]:
    if type(value) is not dict:
        raise _error("CONFIG_TYPE_ERROR", "value must be a mapping", field)
    return value


def _exact(data: Dict[str, Any], keys: Set[str], field: Optional[str] = None) -> None:
    for key in data:
        if type(key) is not str:
            raise _error("CONFIG_TYPE_ERROR", "mapping keys must be strings", f"{field}.{key}" if field else str(key))
    for key in sorted(keys):
        if key not in data:
            raise _error("CONFIG_GAP", "required field is missing", f"{field}.{key}" if field else key)
    extra = data.keys() - keys
    if extra:
        key = sorted(extra)[0]
        raise _error("CONFIG_VALUE_ERROR", "unknown field", f"{field}.{key}" if field else key)


def _string(value: Any, field: str) -> str:
    if type(value) is not str:
        raise _error("CONFIG_TYPE_ERROR", "value must be a string", field)
    if not value.strip():
        raise _error("CONFIG_VALUE_ERROR", "value must not be empty", field)
    return value


def _strings(value: Any, field: str) -> Tuple[str, ...]:
    if type(value) is not list:
        raise _error("CONFIG_TYPE_ERROR", "value must be a list", field)
    return tuple(_string(item, f"{field}.{index}") for index, item in enumerate(value))


def _integer(value: Any, field: str) -> int:
    if type(value) is not int:
        raise _error("CONFIG_TYPE_ERROR", "value must be an integer", field)
    return value


def _number(value: Any, field: str) -> float:
    if type(value) not in (int, float):
        raise _error("CONFIG_TYPE_ERROR", "value must be a number", field)
    result = float(value)
    if not math.isfinite(result):
        raise _error("CONFIG_TYPE_ERROR", "value must be finite", field)
    return result


def _version(data: Dict[str, Any], key: str, expected: str) -> str:
    value = _string(data[key], key)
    if value != expected:
        raise _error("CONFIG_VERSION_MISMATCH", f"expected {expected!r}", key)
    return value


def _load(config_dir: Path) -> Dict[str, Any]:
    path = config_dir / POLICY_FILE
    if not path.is_file():
        raise _error("CONFIG_GAP", "required configuration file is missing")
    try:
        with path.open(encoding="utf-8") as stream:
            value = yaml.safe_load(stream)
    except (OSError, yaml.YAMLError) as exc:
        raise _error("CONFIG_PARSE_ERROR", "configuration cannot be parsed") from exc
    return _mapping(value)


def load_dimension_coverage_policy(
    config_dir: Path,
    primitive_foundation: PrimitiveFoundationConfig,
    runtime_config: RuntimeConfig,
) -> DimensionCoveragePolicyConfig:
    data = _load(Path(config_dir))
    _exact(data, ROOT_KEYS)
    schema_version = _version(data, "schema_version", SCHEMA_VERSION)
    policy_version = _string(data["policy_version"], "policy_version")
    ontology_version = _version(data, "ontology_version", primitive_foundation.ontology.ontology_version)
    score_model_version = _version(data, "score_model_version", runtime_config.score_model.score_model_version)
    dimension_count = _integer(data["dimension_count"], "dimension_count")
    if dimension_count != 12:
        raise _error("CONFIG_VALUE_ERROR", "dimension_count must be 12", "dimension_count")
    if type(data["dimensions"]) is not list:
        raise _error("CONFIG_TYPE_ERROR", "dimensions must be a list", "dimensions")
    if len(data["dimensions"]) != 12:
        raise _error("CONFIG_VALUE_ERROR", "dimensions must contain exactly 12 records", "dimensions")

    ontology_ids = {item.primitive_id for item in primitive_foundation.ontology.primitives}
    dimensions = []
    seen_ids: Set[str] = set()
    seen_names: Set[str] = set()
    ref_counts = {}
    for index, raw in enumerate(data["dimensions"]):
        field = f"dimensions.{index}"
        item = _mapping(raw, field)
        _exact(item, DIMENSION_KEYS, field)
        dimension_id = _string(item["dimension_id"], f"{field}.dimension_id")
        if DIMENSION_ID_PATTERN.fullmatch(dimension_id) is None or dimension_id in seen_ids:
            raise _error("CONFIG_VALUE_ERROR", "invalid or duplicate dimension ID", f"{field}.dimension_id")
        name = _string(item["canonical_name"], f"{field}.canonical_name")
        normalized_name = name.strip().casefold()
        if normalized_name in seen_names:
            raise _error("CONFIG_VALUE_ERROR", "duplicate dimension name", f"{field}.canonical_name")
        definition = _string(item["definition"], f"{field}.definition")
        refs = _strings(item["primitive_refs"], f"{field}.primitive_refs")
        if not refs:
            raise _error("CONFIG_VALUE_ERROR", "primitive_refs must not be empty", f"{field}.primitive_refs")
        seen_refs: Set[str] = set()
        for ref_index, ref in enumerate(refs):
            ref_field = f"{field}.primitive_refs.{ref_index}"
            if ref not in ontology_ids or ref in seen_refs:
                raise _error("CONFIG_VALUE_ERROR", "unknown or duplicate Primitive reference", ref_field)
            seen_refs.add(ref)
        limitations = _strings(item["limitations"], f"{field}.limitations")
        dimensions.append(DimensionDefinition(dimension_id, name, definition, refs, limitations))
        seen_ids.add(dimension_id)
        seen_names.add(normalized_name)
        ref_counts[dimension_id] = len(refs)

    policy = _mapping(data["coverage_policy"], "coverage_policy")
    _exact(policy, POLICY_KEYS, "coverage_policy")
    fixed = {"threshold_status": "provisional", "partial_portrait_allowed": True, "partial_status": "partial", "warning_code": "coverage_warning", "missing_config_code": "CONFIG_GAP"}
    parsed_fixed = {}
    for key, expected in fixed.items():
        value = policy[key]
        if type(value) is not type(expected):
            raise _error("CONFIG_TYPE_ERROR", "value has wrong type", f"coverage_policy.{key}")
        if value != expected:
            raise _error("CONFIG_VALUE_ERROR", f"expected {expected!r}", f"coverage_policy.{key}")
        parsed_fixed[key] = value
    metric = _string(policy["coverage_metric"], "coverage_policy.coverage_metric")
    complete = _number(policy["complete_threshold"], "coverage_policy.complete_threshold")
    partial = _number(policy["partial_threshold"], "coverage_policy.partial_threshold")
    if not 0 <= complete <= 1:
        raise _error("CONFIG_VALUE_ERROR", "complete threshold must be in [0, 1]", "coverage_policy.complete_threshold")
    if not 0 <= partial < complete:
        raise _error("CONFIG_VALUE_ERROR", "partial threshold must be below complete threshold", "coverage_policy.partial_threshold")

    raw_requirements = policy["dimension_requirements"]
    if type(raw_requirements) is not list:
        raise _error("CONFIG_TYPE_ERROR", "dimension_requirements must be a list", "coverage_policy.dimension_requirements")
    requirements = {}
    for index, raw in enumerate(raw_requirements):
        field = f"coverage_policy.dimension_requirements.{index}"
        item = _mapping(raw, field)
        _exact(item, REQUIREMENT_KEYS, field)
        dimension_id = _string(item["dimension_id"], f"{field}.dimension_id")
        if dimension_id not in seen_ids or dimension_id in requirements:
            raise _error("CONFIG_VALUE_ERROR", "unknown or duplicate dimension requirement", f"{field}.dimension_id")
        minimum = _integer(item["minimum_supported_primitives"], f"{field}.minimum_supported_primitives")
        if not 1 <= minimum <= ref_counts[dimension_id]:
            raise _error("CONFIG_VALUE_ERROR", "minimum exceeds dimension Primitive references", f"{field}.minimum_supported_primitives")
        requirements[dimension_id] = DimensionRequirement(dimension_id, minimum)
    if set(requirements) != seen_ids:
        raise _error("CONFIG_VALUE_ERROR", "requirements must cover every dimension", "coverage_policy.dimension_requirements")
    ordered_requirements = tuple(requirements[item.dimension_id] for item in dimensions)
    coverage = CoveragePolicy(parsed_fixed["threshold_status"], metric, complete, partial, parsed_fixed["partial_portrait_allowed"], parsed_fixed["partial_status"], parsed_fixed["warning_code"], parsed_fixed["missing_config_code"], ordered_requirements)
    return DimensionCoveragePolicyConfig(schema_version, policy_version, ontology_version, score_model_version, dimension_count, tuple(dimensions), coverage)
