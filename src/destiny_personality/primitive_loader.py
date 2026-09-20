from pathlib import Path
import re
from typing import Any, Dict, Optional, Set, Tuple

import yaml

from .config_errors import ConfigError
from .primitive_models import (
    PrimitiveDefinition,
    PrimitiveFoundationConfig,
    PrimitiveOntologyConfig,
    PrimitiveStateResolutionConfig,
    PrimitiveStateRule,
)


ONTOLOGY_FILE = "primitive_ontology_v1.yaml"
RESOLUTION_FILE = "primitive_state_resolution_v1.yaml"
ONTOLOGY_SCHEMA_VERSION = "primitive-ontology-v1"
RESOLUTION_SCHEMA_VERSION = "primitive-state-resolution-v1"
SCORE_MODEL_VERSION = "2.2"
PRIMITIVE_ID_PATTERN = re.compile(r"P[0-9]{3}")
WIRE_STATES = ("supported_high", "supported_low", "mixed", "unknown")
ONTOLOGY_KEYS = {"schema_version", "ontology_version", "primitives"}
PRIMITIVE_KEYS = {
    "primitive_id",
    "canonical_name",
    "definition",
    "high_expression",
    "low_expression",
    "aliases",
    "limitations",
}
RESOLUTION_KEYS = {
    "schema_version",
    "resolution_version",
    "ontology_version",
    "score_model_version",
    "states",
    "invariants",
    "rules",
}
INVARIANTS = {
    "no_evidence_state": "unknown",
    "low_requires_explicit_reverse_evidence": True,
    "unknown_is_not_low": True,
    "preserve_system_salience": True,
    "cross_system_validation_changes_trait_salience": False,
    "tension_reduces_trait_salience": False,
}
RULE_KEYS = {
    "rule_id",
    "target_state",
    "priority",
    "description",
    "requires_explicit_reverse_evidence",
    "evidence_requirements",
    "thresholds",
    "limitations",
}


def _error(
    code: str,
    message: str,
    filename: str,
    field: Optional[str] = None,
) -> ConfigError:
    return ConfigError(code, message, file=filename, field=field)


def _join_field(parent: Optional[str], child: object) -> str:
    return str(child) if parent is None else f"{parent}.{child}"


def _load_yaml_mapping(config_dir: Path, filename: str) -> Dict[str, Any]:
    path = config_dir / filename
    if not path.is_file():
        raise _error("CONFIG_GAP", "required configuration file is missing", filename)
    try:
        with path.open(encoding="utf-8") as stream:
            data = yaml.safe_load(stream)
    except (OSError, yaml.YAMLError) as exc:
        raise _error(
            "CONFIG_PARSE_ERROR", "configuration cannot be parsed", filename
        ) from exc
    if type(data) is not dict:
        raise _error("CONFIG_TYPE_ERROR", "document root must be a mapping", filename)
    return data


def _require_exact_keys(
    data: Dict[str, Any],
    required: Set[str],
    filename: str,
    field: Optional[str] = None,
) -> None:
    non_string_keys = [key for key in data if type(key) is not str]
    if non_string_keys:
        key = min(non_string_keys, key=lambda item: (type(item).__name__, repr(item)))
        raise _error(
            "CONFIG_TYPE_ERROR",
            "mapping keys must be strings",
            filename,
            _join_field(field, key),
        )
    for key in sorted(required):
        if key not in data:
            raise _error(
                "CONFIG_GAP",
                "required field is missing",
                filename,
                _join_field(field, key),
            )
    extra = data.keys() - required
    if extra:
        key = sorted(extra)[0]
        raise _error(
            "CONFIG_VALUE_ERROR",
            "unknown field",
            filename,
            _join_field(field, key),
        )


def _require_mapping(value: Any, filename: str, field: str) -> Dict[str, Any]:
    if type(value) is not dict:
        raise _error("CONFIG_TYPE_ERROR", "value must be a mapping", filename, field)
    return value


def _require_non_empty_string(value: Any, filename: str, field: str) -> str:
    if type(value) is not str:
        raise _error("CONFIG_TYPE_ERROR", "value must be a string", filename, field)
    if not value.strip():
        raise _error("CONFIG_VALUE_ERROR", "value must not be empty", filename, field)
    return value


def _require_string_list(value: Any, filename: str, field: str) -> Tuple[str, ...]:
    if type(value) is not list:
        raise _error("CONFIG_TYPE_ERROR", "value must be a list", filename, field)
    values = []
    for index, item in enumerate(value):
        item_field = _join_field(field, index)
        values.append(_require_non_empty_string(item, filename, item_field))
    return tuple(values)


def _require_schema_version(
    data: Dict[str, Any], expected: str, filename: str
) -> None:
    value = _require_non_empty_string(data["schema_version"], filename, "schema_version")
    if value != expected:
        raise _error(
            "CONFIG_VERSION_MISMATCH",
            f"expected schema version {expected!r}",
            filename,
            "schema_version",
        )


def _freeze(value: Any) -> Any:
    if type(value) is dict:
        return tuple((key, _freeze(item)) for key, item in value.items())
    if type(value) is list:
        return tuple(_freeze(item) for item in value)
    return value


def _normalized_name(value: str) -> str:
    return value.strip().casefold()


def _parse_primitive(
    data: Any,
    index: int,
    seen_ids: Set[str],
    seen_names: Set[str],
) -> PrimitiveDefinition:
    field = f"primitives.{index}"
    item = _require_mapping(data, ONTOLOGY_FILE, field)
    _require_exact_keys(item, PRIMITIVE_KEYS, ONTOLOGY_FILE, field)

    primitive_id = _require_non_empty_string(
        item["primitive_id"], ONTOLOGY_FILE, f"{field}.primitive_id"
    )
    if PRIMITIVE_ID_PATTERN.fullmatch(primitive_id) is None:
        raise _error(
            "CONFIG_VALUE_ERROR",
            "invalid Primitive ID",
            ONTOLOGY_FILE,
            f"{field}.primitive_id",
        )
    if primitive_id in seen_ids:
        raise _error(
            "CONFIG_VALUE_ERROR",
            "duplicate Primitive ID",
            ONTOLOGY_FILE,
            f"{field}.primitive_id",
        )
    seen_ids.add(primitive_id)

    canonical_name = _require_non_empty_string(
        item["canonical_name"], ONTOLOGY_FILE, f"{field}.canonical_name"
    )
    normalized_canonical = _normalized_name(canonical_name)
    if normalized_canonical in seen_names:
        raise _error(
            "CONFIG_VALUE_ERROR",
            "ambiguous Primitive name or alias",
            ONTOLOGY_FILE,
            f"{field}.canonical_name",
        )
    seen_names.add(normalized_canonical)

    definition = _require_non_empty_string(
        item["definition"], ONTOLOGY_FILE, f"{field}.definition"
    )
    high_expression = _require_non_empty_string(
        item["high_expression"], ONTOLOGY_FILE, f"{field}.high_expression"
    )
    low_expression = _require_non_empty_string(
        item["low_expression"], ONTOLOGY_FILE, f"{field}.low_expression"
    )
    if high_expression.strip() == low_expression.strip():
        raise _error(
            "CONFIG_VALUE_ERROR",
            "high and low expressions must be distinct",
            ONTOLOGY_FILE,
            f"{field}.low_expression",
        )

    aliases = _require_string_list(item["aliases"], ONTOLOGY_FILE, f"{field}.aliases")
    for alias_index, alias in enumerate(aliases):
        normalized_alias = _normalized_name(alias)
        if normalized_alias in seen_names:
            raise _error(
                "CONFIG_VALUE_ERROR",
                "ambiguous Primitive name or alias",
                ONTOLOGY_FILE,
                f"{field}.aliases.{alias_index}",
            )
        seen_names.add(normalized_alias)

    limitations = _require_string_list(
        item["limitations"], ONTOLOGY_FILE, f"{field}.limitations"
    )
    return PrimitiveDefinition(
        primitive_id=primitive_id,
        canonical_name=canonical_name,
        definition=definition,
        high_expression=high_expression,
        low_expression=low_expression,
        aliases=aliases,
        limitations=limitations,
    )


def _parse_ontology(data: Dict[str, Any]) -> PrimitiveOntologyConfig:
    _require_exact_keys(data, ONTOLOGY_KEYS, ONTOLOGY_FILE)
    _require_schema_version(data, ONTOLOGY_SCHEMA_VERSION, ONTOLOGY_FILE)
    ontology_version = _require_non_empty_string(
        data["ontology_version"], ONTOLOGY_FILE, "ontology_version"
    )
    if type(data["primitives"]) is not list:
        raise _error(
            "CONFIG_TYPE_ERROR", "primitives must be a list", ONTOLOGY_FILE, "primitives"
        )
    if not data["primitives"]:
        raise _error(
            "CONFIG_VALUE_ERROR",
            "primitives must not be empty",
            ONTOLOGY_FILE,
            "primitives",
        )
    seen_ids: Set[str] = set()
    seen_names: Set[str] = set()
    primitives = tuple(
        _parse_primitive(item, index, seen_ids, seen_names)
        for index, item in enumerate(data["primitives"])
    )
    return PrimitiveOntologyConfig(
        schema_version=data["schema_version"],
        ontology_version=ontology_version,
        primitives=primitives,
    )


def _parse_rule(data: Any, index: int) -> PrimitiveStateRule:
    field = f"rules.{index}"
    item = _require_mapping(data, RESOLUTION_FILE, field)
    _require_exact_keys(item, RULE_KEYS, RESOLUTION_FILE, field)
    rule_id = _require_non_empty_string(
        item["rule_id"], RESOLUTION_FILE, f"{field}.rule_id"
    )
    target_state = _require_non_empty_string(
        item["target_state"], RESOLUTION_FILE, f"{field}.target_state"
    )
    if target_state not in WIRE_STATES:
        raise _error(
            "CONFIG_VALUE_ERROR",
            "unknown Primitive state",
            RESOLUTION_FILE,
            f"{field}.target_state",
        )
    priority = item["priority"]
    if type(priority) is not int:
        raise _error(
            "CONFIG_TYPE_ERROR",
            "priority must be an integer",
            RESOLUTION_FILE,
            f"{field}.priority",
        )
    if priority < 0:
        raise _error(
            "CONFIG_VALUE_ERROR",
            "priority must be non-negative",
            RESOLUTION_FILE,
            f"{field}.priority",
        )
    description = _require_non_empty_string(
        item["description"], RESOLUTION_FILE, f"{field}.description"
    )
    reverse_evidence = item["requires_explicit_reverse_evidence"]
    if type(reverse_evidence) is not bool:
        raise _error(
            "CONFIG_TYPE_ERROR",
            "reverse-evidence marker must be a boolean",
            RESOLUTION_FILE,
            f"{field}.requires_explicit_reverse_evidence",
        )
    if target_state == "supported_low" and not reverse_evidence:
        raise _error(
            "CONFIG_VALUE_ERROR",
            "supported_low requires explicit reverse evidence",
            RESOLUTION_FILE,
            f"{field}.requires_explicit_reverse_evidence",
        )
    evidence_requirements = _require_mapping(
        item["evidence_requirements"],
        RESOLUTION_FILE,
        f"{field}.evidence_requirements",
    )
    if not evidence_requirements:
        raise _error(
            "CONFIG_VALUE_ERROR",
            "evidence requirements must not be empty",
            RESOLUTION_FILE,
            f"{field}.evidence_requirements",
        )
    thresholds = _require_mapping(
        item["thresholds"], RESOLUTION_FILE, f"{field}.thresholds"
    )
    limitations = _require_string_list(
        item["limitations"], RESOLUTION_FILE, f"{field}.limitations"
    )
    return PrimitiveStateRule(
        rule_id=rule_id,
        target_state=target_state,
        priority=priority,
        description=description,
        requires_explicit_reverse_evidence=reverse_evidence,
        evidence_requirements=_freeze(evidence_requirements),
        thresholds=_freeze(thresholds),
        limitations=limitations,
    )


def _parse_resolution(
    data: Dict[str, Any], ontology: PrimitiveOntologyConfig
) -> PrimitiveStateResolutionConfig:
    _require_exact_keys(data, RESOLUTION_KEYS, RESOLUTION_FILE)
    _require_schema_version(data, RESOLUTION_SCHEMA_VERSION, RESOLUTION_FILE)
    resolution_version = _require_non_empty_string(
        data["resolution_version"], RESOLUTION_FILE, "resolution_version"
    )
    ontology_version = _require_non_empty_string(
        data["ontology_version"], RESOLUTION_FILE, "ontology_version"
    )
    if ontology_version != ontology.ontology_version:
        raise _error(
            "CONFIG_VERSION_MISMATCH",
            "ontology version does not match the loaded ontology",
            RESOLUTION_FILE,
            "ontology_version",
        )
    score_model_version = _require_non_empty_string(
        data["score_model_version"], RESOLUTION_FILE, "score_model_version"
    )
    if score_model_version != SCORE_MODEL_VERSION:
        raise _error(
            "CONFIG_VERSION_MISMATCH",
            f"expected score model version {SCORE_MODEL_VERSION!r}",
            RESOLUTION_FILE,
            "score_model_version",
        )
    if type(data["states"]) is not list:
        raise _error(
            "CONFIG_TYPE_ERROR", "states must be a list", RESOLUTION_FILE, "states"
        )
    for index, state in enumerate(data["states"]):
        if type(state) is not str:
            raise _error(
                "CONFIG_TYPE_ERROR",
                "state must be a string",
                RESOLUTION_FILE,
                f"states.{index}",
            )
    states = tuple(data["states"])
    if states != WIRE_STATES:
        raise _error(
            "CONFIG_VALUE_ERROR",
            "states must match the canonical wire-state list",
            RESOLUTION_FILE,
            "states",
        )
    invariants = _require_mapping(data["invariants"], RESOLUTION_FILE, "invariants")
    _require_exact_keys(invariants, set(INVARIANTS), RESOLUTION_FILE, "invariants")
    for key, expected in INVARIANTS.items():
        if type(invariants[key]) is not type(expected):
            raise _error(
                "CONFIG_TYPE_ERROR",
                "invariant has the wrong type",
                RESOLUTION_FILE,
                f"invariants.{key}",
            )
        if invariants[key] != expected:
            raise _error(
                "CONFIG_VALUE_ERROR",
                f"expected {expected!r}",
                RESOLUTION_FILE,
                f"invariants.{key}",
            )
    if type(data["rules"]) is not list:
        raise _error(
            "CONFIG_TYPE_ERROR", "rules must be a list", RESOLUTION_FILE, "rules"
        )
    if not data["rules"]:
        raise _error(
            "CONFIG_VALUE_ERROR", "rules must not be empty", RESOLUTION_FILE, "rules"
        )
    parsed_rules = []
    seen_rule_ids: Set[str] = set()
    seen_priorities: Set[int] = set()
    for index, item in enumerate(data["rules"]):
        rule = _parse_rule(item, index)
        if rule.rule_id in seen_rule_ids:
            raise _error(
                "CONFIG_VALUE_ERROR",
                "duplicate rule ID",
                RESOLUTION_FILE,
                f"rules.{index}.rule_id",
            )
        if rule.priority in seen_priorities:
            raise _error(
                "CONFIG_VALUE_ERROR",
                "duplicate rule priority",
                RESOLUTION_FILE,
                f"rules.{index}.priority",
            )
        seen_rule_ids.add(rule.rule_id)
        seen_priorities.add(rule.priority)
        parsed_rules.append(rule)
    rules = tuple(sorted(parsed_rules, key=lambda rule: rule.priority))
    if {rule.target_state for rule in rules} != set(WIRE_STATES):
        raise _error(
            "CONFIG_VALUE_ERROR",
            "rules must cover every wire state",
            RESOLUTION_FILE,
            "rules",
        )
    return PrimitiveStateResolutionConfig(
        schema_version=data["schema_version"],
        resolution_version=resolution_version,
        ontology_version=ontology_version,
        score_model_version=score_model_version,
        states=states,
        invariants=_freeze(invariants),
        rules=rules,
    )


def load_primitive_foundation(config_dir: Path) -> PrimitiveFoundationConfig:
    directory = Path(config_dir)
    ontology = _parse_ontology(_load_yaml_mapping(directory, ONTOLOGY_FILE))
    resolution = _parse_resolution(
        _load_yaml_mapping(directory, RESOLUTION_FILE), ontology
    )
    return PrimitiveFoundationConfig(ontology=ontology, resolution=resolution)
