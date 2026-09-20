from pathlib import Path
import math
import re
from typing import Any, Dict, Optional, Set, Tuple

import yaml

from .config_errors import ConfigError
from .config_models import RuntimeConfig
from .mapping_models import (
    ContextAwareMappingRegistryConfig,
    MappingInteraction,
    MappingModifier,
    MappingOutput,
    MappingRegistryBundle,
    MappingRule,
)
from .primitive_models import PrimitiveFoundationConfig


BAZI_MAPPING_FILE = "bazi_mapping_registry_v1.yaml"
ASTROLOGY_MAPPING_FILE = "astrology_mapping_registry_v1.yaml"
MAPPING_SCHEMA_VERSION = "context-aware-mapping-registry-v1"
FACT_SCHEMA_VERSION = "deterministic-facts-v1"
PRIMITIVE_ID_PATTERN = re.compile(r"P[0-9]{3}")

REGISTRY_KEYS = {
    "schema_version",
    "registry_version",
    "source_system",
    "methodology_version",
    "fact_schema_version",
    "score_model_version",
    "ontology_version",
    "rules",
    "interactions",
}
RULE_KEYS = {
    "rule_id",
    "priority",
    "primary_condition",
    "context",
    "outputs",
    "modifiers",
    "limitations",
}
OUTPUT_KEYS = {"primitive_id", "direction", "salience", "limitations"}
MODIFIER_KEYS = {"when", "effects"}
INTERACTION_KEYS = {"interaction_id", "requires", "produces", "limitations"}


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


def _require_list(value: Any, filename: str, field: str) -> list:
    if type(value) is not list:
        raise _error("CONFIG_TYPE_ERROR", "value must be a list", filename, field)
    return value


def _require_non_empty_string(value: Any, filename: str, field: str) -> str:
    if type(value) is not str:
        raise _error("CONFIG_TYPE_ERROR", "value must be a string", filename, field)
    if not value.strip():
        raise _error("CONFIG_VALUE_ERROR", "value must not be empty", filename, field)
    return value


def _require_non_negative_integer(value: Any, filename: str, field: str) -> int:
    if type(value) is not int:
        raise _error("CONFIG_TYPE_ERROR", "value must be an integer", filename, field)
    if value < 0:
        raise _error(
            "CONFIG_VALUE_ERROR", "value must be non-negative", filename, field
        )
    return value


def _require_string_list(value: Any, filename: str, field: str) -> Tuple[str, ...]:
    items = _require_list(value, filename, field)
    return tuple(
        _require_non_empty_string(item, filename, f"{field}.{index}")
        for index, item in enumerate(items)
    )


def _freeze_declarative(value: Any, filename: str, field: str) -> Any:
    if type(value) is dict:
        non_string_keys = [key for key in value if type(key) is not str]
        if non_string_keys:
            key = min(
                non_string_keys,
                key=lambda item: (type(item).__name__, repr(item)),
            )
            raise _error(
                "CONFIG_TYPE_ERROR",
                "declarative mapping keys must be strings",
                filename,
                _join_field(field, key),
            )
        return tuple(
            (key, _freeze_declarative(item, filename, _join_field(field, key)))
            for key, item in value.items()
        )
    if type(value) is list:
        return tuple(
            _freeze_declarative(item, filename, _join_field(field, index))
            for index, item in enumerate(value)
        )
    if type(value) in (str, bool, int, type(None)):
        return value
    if type(value) is float:
        if not math.isfinite(value):
            raise _error(
                "CONFIG_TYPE_ERROR", "float must be finite", filename, field
            )
        return value
    raise _error(
        "CONFIG_TYPE_ERROR",
        "unsupported declarative value type",
        filename,
        field,
    )


def _require_non_empty_declarative_mapping(
    value: Any, filename: str, field: str
) -> Any:
    mapping = _require_mapping(value, filename, field)
    if not mapping:
        raise _error(
            "CONFIG_VALUE_ERROR", "mapping must not be empty", filename, field
        )
    return _freeze_declarative(mapping, filename, field)


def _parse_output(
    data: Any,
    field: str,
    filename: str,
    ontology_ids: Set[str],
    salience_bounds: Tuple[int, int],
) -> MappingOutput:
    item = _require_mapping(data, filename, field)
    _require_exact_keys(item, OUTPUT_KEYS, filename, field)
    primitive_field = f"{field}.primitive_id"
    primitive_id = _require_non_empty_string(
        item["primitive_id"], filename, primitive_field
    )
    if PRIMITIVE_ID_PATTERN.fullmatch(primitive_id) is None:
        raise _error(
            "CONFIG_VALUE_ERROR",
            "invalid Primitive ID",
            filename,
            primitive_field,
        )
    if primitive_id not in ontology_ids:
        raise _error(
            "CONFIG_VALUE_ERROR",
            "Primitive reference is not defined by the accepted ontology",
            filename,
            primitive_field,
        )
    direction = _require_non_empty_string(
        item["direction"], filename, f"{field}.direction"
    )
    salience_field = f"{field}.salience"
    salience = _require_non_negative_integer(
        item["salience"], filename, salience_field
    )
    minimum, maximum = salience_bounds
    if not minimum <= salience <= maximum:
        raise _error(
            "CONFIG_VALUE_ERROR",
            "salience is outside the accepted score-model bounds",
            filename,
            salience_field,
        )
    limitations = _require_string_list(
        item["limitations"], filename, f"{field}.limitations"
    )
    return MappingOutput(
        primitive_id=primitive_id,
        direction=direction,
        salience=salience,
        limitations=limitations,
    )


def _parse_modifier(data: Any, field: str, filename: str) -> MappingModifier:
    item = _require_mapping(data, filename, field)
    _require_exact_keys(item, MODIFIER_KEYS, filename, field)
    when = _require_non_empty_declarative_mapping(
        item["when"], filename, f"{field}.when"
    )
    effects_field = f"{field}.effects"
    raw_effects = _require_list(item["effects"], filename, effects_field)
    if not raw_effects:
        raise _error(
            "CONFIG_VALUE_ERROR",
            "effects must not be empty",
            filename,
            effects_field,
        )
    effects = tuple(
        _require_non_empty_declarative_mapping(
            effect, filename, f"{effects_field}.{index}"
        )
        for index, effect in enumerate(raw_effects)
    )
    return MappingModifier(when=when, effects=effects)


def _parse_rule(
    data: Any,
    index: int,
    filename: str,
    ontology_ids: Set[str],
    salience_bounds: Tuple[int, int],
) -> MappingRule:
    field = f"rules.{index}"
    item = _require_mapping(data, filename, field)
    _require_exact_keys(item, RULE_KEYS, filename, field)
    rule_id = _require_non_empty_string(item["rule_id"], filename, f"{field}.rule_id")
    priority = _require_non_negative_integer(
        item["priority"], filename, f"{field}.priority"
    )
    primary_condition = _require_non_empty_declarative_mapping(
        item["primary_condition"], filename, f"{field}.primary_condition"
    )
    context = _require_non_empty_declarative_mapping(
        item["context"], filename, f"{field}.context"
    )
    outputs_field = f"{field}.outputs"
    raw_outputs = _require_list(item["outputs"], filename, outputs_field)
    if not raw_outputs:
        raise _error(
            "CONFIG_VALUE_ERROR",
            "outputs must not be empty",
            filename,
            outputs_field,
        )
    outputs = []
    seen_primitive_ids: Set[str] = set()
    for output_index, raw_output in enumerate(raw_outputs):
        output = _parse_output(
            raw_output,
            f"{outputs_field}.{output_index}",
            filename,
            ontology_ids,
            salience_bounds,
        )
        if output.primitive_id in seen_primitive_ids:
            raise _error(
                "CONFIG_VALUE_ERROR",
                "duplicate Primitive output",
                filename,
                f"{outputs_field}.{output_index}.primitive_id",
            )
        seen_primitive_ids.add(output.primitive_id)
        outputs.append(output)
    modifiers_field = f"{field}.modifiers"
    raw_modifiers = _require_list(item["modifiers"], filename, modifiers_field)
    modifiers = tuple(
        _parse_modifier(modifier, f"{modifiers_field}.{modifier_index}", filename)
        for modifier_index, modifier in enumerate(raw_modifiers)
    )
    limitations = _require_string_list(
        item["limitations"], filename, f"{field}.limitations"
    )
    return MappingRule(
        rule_id=rule_id,
        priority=priority,
        primary_condition=primary_condition,
        context=context,
        outputs=tuple(outputs),
        modifiers=modifiers,
        limitations=limitations,
    )


def _parse_interaction(
    data: Any,
    index: int,
    filename: str,
    local_rule_ids: Set[str],
) -> MappingInteraction:
    field = f"interactions.{index}"
    item = _require_mapping(data, filename, field)
    _require_exact_keys(item, INTERACTION_KEYS, filename, field)
    interaction_id = _require_non_empty_string(
        item["interaction_id"], filename, f"{field}.interaction_id"
    )
    requires_field = f"{field}.requires"
    raw_requires = _require_list(item["requires"], filename, requires_field)
    if len(raw_requires) < 2:
        raise _error(
            "CONFIG_VALUE_ERROR",
            "interaction requires at least two local rules",
            filename,
            requires_field,
        )
    requires = []
    seen_requirements: Set[str] = set()
    for requirement_index, value in enumerate(raw_requires):
        requirement_field = f"{requires_field}.{requirement_index}"
        rule_id = _require_non_empty_string(value, filename, requirement_field)
        if rule_id in seen_requirements:
            raise _error(
                "CONFIG_VALUE_ERROR",
                "duplicate interaction requirement",
                filename,
                requirement_field,
            )
        if rule_id not in local_rule_ids:
            raise _error(
                "CONFIG_VALUE_ERROR",
                "interaction rule reference is not defined in this registry",
                filename,
                requirement_field,
            )
        seen_requirements.add(rule_id)
        requires.append(rule_id)
    produces = _require_non_empty_declarative_mapping(
        item["produces"], filename, f"{field}.produces"
    )
    limitations = _require_string_list(
        item["limitations"], filename, f"{field}.limitations"
    )
    return MappingInteraction(
        interaction_id=interaction_id,
        requires=tuple(requires),
        produces=produces,
        limitations=limitations,
    )


def _require_exact_version(
    value: Any,
    expected: str,
    filename: str,
    field: str,
) -> str:
    parsed = _require_non_empty_string(value, filename, field)
    if parsed != expected:
        raise _error(
            "CONFIG_VERSION_MISMATCH",
            f"expected {expected!r}",
            filename,
            field,
        )
    return parsed


def _parse_registry(
    data: Dict[str, Any],
    filename: str,
    expected_source: str,
    expected_methodology_version: str,
    expected_score_model_version: str,
    ontology_version: str,
    ontology_ids: Set[str],
    salience_bounds: Tuple[int, int],
    reserved_rule_ids: Set[str],
    reserved_interaction_ids: Set[str],
) -> ContextAwareMappingRegistryConfig:
    _require_exact_keys(data, REGISTRY_KEYS, filename)
    schema_version = _require_exact_version(
        data["schema_version"], MAPPING_SCHEMA_VERSION, filename, "schema_version"
    )
    registry_version = _require_non_empty_string(
        data["registry_version"], filename, "registry_version"
    )
    source_system = _require_exact_version(
        data["source_system"], expected_source, filename, "source_system"
    )
    methodology_version = _require_exact_version(
        data["methodology_version"],
        expected_methodology_version,
        filename,
        "methodology_version",
    )
    fact_schema_version = _require_exact_version(
        data["fact_schema_version"],
        FACT_SCHEMA_VERSION,
        filename,
        "fact_schema_version",
    )
    score_model_version = _require_exact_version(
        data["score_model_version"],
        expected_score_model_version,
        filename,
        "score_model_version",
    )
    accepted_ontology_version = _require_exact_version(
        data["ontology_version"],
        ontology_version,
        filename,
        "ontology_version",
    )

    raw_rules = _require_list(data["rules"], filename, "rules")
    if not raw_rules:
        raise _error("CONFIG_VALUE_ERROR", "rules must not be empty", filename, "rules")
    rules = []
    seen_rule_ids: Set[str] = set()
    seen_priorities: Set[int] = set()
    for index, raw_rule in enumerate(raw_rules):
        rule = _parse_rule(
            raw_rule,
            index,
            filename,
            ontology_ids,
            salience_bounds,
        )
        if rule.rule_id in seen_rule_ids or rule.rule_id in reserved_rule_ids:
            raise _error(
                "CONFIG_VALUE_ERROR",
                "duplicate rule ID",
                filename,
                f"rules.{index}.rule_id",
            )
        if rule.priority in seen_priorities:
            raise _error(
                "CONFIG_VALUE_ERROR",
                "duplicate rule priority",
                filename,
                f"rules.{index}.priority",
            )
        seen_rule_ids.add(rule.rule_id)
        seen_priorities.add(rule.priority)
        rules.append(rule)

    raw_interactions = _require_list(
        data["interactions"], filename, "interactions"
    )
    interactions = []
    seen_interaction_ids: Set[str] = set()
    for index, raw_interaction in enumerate(raw_interactions):
        interaction = _parse_interaction(
            raw_interaction,
            index,
            filename,
            seen_rule_ids,
        )
        if (
            interaction.interaction_id in seen_interaction_ids
            or interaction.interaction_id in reserved_interaction_ids
        ):
            raise _error(
                "CONFIG_VALUE_ERROR",
                "duplicate interaction ID",
                filename,
                f"interactions.{index}.interaction_id",
            )
        seen_interaction_ids.add(interaction.interaction_id)
        interactions.append(interaction)

    return ContextAwareMappingRegistryConfig(
        schema_version=schema_version,
        registry_version=registry_version,
        source_system=source_system,
        methodology_version=methodology_version,
        fact_schema_version=fact_schema_version,
        score_model_version=score_model_version,
        ontology_version=accepted_ontology_version,
        rules=tuple(sorted(rules, key=lambda rule: rule.priority)),
        interactions=tuple(interactions),
    )


def load_mapping_registries(
    config_dir: Path,
    primitive_foundation: PrimitiveFoundationConfig,
    runtime_config: RuntimeConfig,
) -> MappingRegistryBundle:
    directory = Path(config_dir)
    ontology = primitive_foundation.ontology
    ontology_ids = {item.primitive_id for item in ontology.primitives}
    salience_bounds = (
        runtime_config.score_model.trait_salience.minimum,
        runtime_config.score_model.trait_salience.maximum,
    )
    bazi = _parse_registry(
        _load_yaml_mapping(directory, BAZI_MAPPING_FILE),
        BAZI_MAPPING_FILE,
        "bazi",
        runtime_config.bazi.methodology_version,
        runtime_config.score_model.score_model_version,
        ontology.ontology_version,
        ontology_ids,
        salience_bounds,
        set(),
        set(),
    )
    astrology = _parse_registry(
        _load_yaml_mapping(directory, ASTROLOGY_MAPPING_FILE),
        ASTROLOGY_MAPPING_FILE,
        "astrology",
        runtime_config.astrology.methodology_version,
        runtime_config.score_model.score_model_version,
        ontology.ontology_version,
        ontology_ids,
        salience_bounds,
        {rule.rule_id for rule in bazi.rules},
        {interaction.interaction_id for interaction in bazi.interactions},
    )
    return MappingRegistryBundle(bazi=bazi, astrology=astrology)
