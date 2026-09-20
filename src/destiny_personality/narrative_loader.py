from pathlib import Path
from typing import Any, Dict, Optional, Set, Tuple

import yaml

from .config_errors import ConfigError
from .dimension_models import DimensionCoveragePolicyConfig
from .narrative_models import NarrativeRule, NarrativeRulesConfig
from .primitive_models import PrimitiveFoundationConfig


FILE = "narrative_rules_v1.yaml"
SCHEMA = "narrative-rules-v1"
ROOT_KEYS = {"schema_version", "narrative_version", "ontology_version", "dimension_policy_version", "sections", "invariants", "rules"}
RULE_KEYS = {"rule_id", "priority", "target_section", "source_kinds", "requires_chart_anchor", "rendering_constraints", "prohibited_inferences", "limitations"}
INVARIANTS = {
    "complete_ir_required": True,
    "narrative_changes_core_claims": False,
    "unsupported_claims_allowed": False,
    "unknown_may_be_rendered_as_certain": False,
    "secondary_may_be_promoted": False,
    "chart_anchor_required": True,
    "traditional_interpretation_claimed_scientific": False,
}
SOURCE_KINDS = {"primitive", "signature", "core_dynamic", "dimension", "shadow", "mature", "fate", "archetype"}


def _error(code: str, message: str, field: Optional[str] = None) -> ConfigError:
    return ConfigError(code, message, file=FILE, field=field)


def _mapping(value: Any, field: Optional[str] = None) -> Dict[str, Any]:
    if type(value) is not dict:
        raise _error("CONFIG_TYPE_ERROR", "value must be a mapping", field)
    return value


def _exact(data: Dict[str, Any], keys: Set[str], field: Optional[str] = None) -> None:
    for key in sorted(keys):
        if key not in data:
            raise _error("CONFIG_GAP", "required field is missing", f"{field}.{key}" if field else key)
    extra = data.keys() - keys
    if extra:
        key = sorted(extra, key=str)[0]
        raise _error("CONFIG_VALUE_ERROR", "unknown field", f"{field}.{key}" if field else str(key))


def _string(value: Any, field: str) -> str:
    if type(value) is not str:
        raise _error("CONFIG_TYPE_ERROR", "value must be a string", field)
    if not value.strip():
        raise _error("CONFIG_VALUE_ERROR", "value must not be empty", field)
    return value


def _strings(value: Any, field: str, nonempty: bool = False) -> Tuple[str, ...]:
    if type(value) is not list:
        raise _error("CONFIG_TYPE_ERROR", "value must be a list", field)
    result = tuple(_string(item, f"{field}.{index}") for index, item in enumerate(value))
    if nonempty and not result:
        raise _error("CONFIG_VALUE_ERROR", "list must not be empty", field)
    return result


def _freeze(value: Any) -> Any:
    if type(value) is dict:
        return tuple((key, _freeze(item)) for key, item in value.items())
    if type(value) is list:
        return tuple(_freeze(item) for item in value)
    return value


def _load(directory: Path) -> Dict[str, Any]:
    path = directory / FILE
    if not path.is_file():
        raise _error("CONFIG_GAP", "required configuration file is missing")
    try:
        with path.open(encoding="utf-8") as stream:
            return _mapping(yaml.safe_load(stream))
    except (OSError, yaml.YAMLError) as exc:
        raise _error("CONFIG_PARSE_ERROR", "configuration cannot be parsed") from exc


def _version(data: Dict[str, Any], key: str, expected: str) -> str:
    value = _string(data[key], key)
    if value != expected:
        raise _error("CONFIG_VERSION_MISMATCH", f"expected {expected!r}", key)
    return value


def load_narrative_rules(config_dir: Path, primitive_foundation: PrimitiveFoundationConfig, dimension_policy: DimensionCoveragePolicyConfig) -> NarrativeRulesConfig:
    data = _load(Path(config_dir))
    _exact(data, ROOT_KEYS)
    schema = _version(data, "schema_version", SCHEMA)
    narrative_version = _string(data["narrative_version"], "narrative_version")
    ontology_version = _version(data, "ontology_version", primitive_foundation.ontology.ontology_version)
    dimension_version = _version(data, "dimension_policy_version", dimension_policy.policy_version)
    sections = _strings(data["sections"], "sections", True)
    if len(set(sections)) != len(sections):
        raise _error("CONFIG_VALUE_ERROR", "sections must be unique", "sections")
    invariants = _mapping(data["invariants"], "invariants")
    _exact(invariants, set(INVARIANTS), "invariants")
    for key, expected in INVARIANTS.items():
        value = invariants[key]
        if type(value) is not bool:
            raise _error("CONFIG_TYPE_ERROR", "invariant must be boolean", f"invariants.{key}")
        if value != expected:
            raise _error("CONFIG_VALUE_ERROR", f"expected {expected!r}", f"invariants.{key}")
    raw_rules = data["rules"]
    if type(raw_rules) is not list:
        raise _error("CONFIG_TYPE_ERROR", "rules must be a list", "rules")
    if not raw_rules:
        raise _error("CONFIG_VALUE_ERROR", "rules must not be empty", "rules")
    rules = []
    ids, priorities, covered = set(), set(), set()
    for index, raw in enumerate(raw_rules):
        field = f"rules.{index}"
        item = _mapping(raw, field)
        _exact(item, RULE_KEYS, field)
        rule_id = _string(item["rule_id"], f"{field}.rule_id")
        if rule_id in ids:
            raise _error("CONFIG_VALUE_ERROR", "duplicate rule ID", f"{field}.rule_id")
        priority = item["priority"]
        if type(priority) is not int:
            raise _error("CONFIG_TYPE_ERROR", "priority must be an integer", f"{field}.priority")
        if priority < 0 or priority in priorities:
            raise _error("CONFIG_VALUE_ERROR", "invalid or duplicate priority", f"{field}.priority")
        section = _string(item["target_section"], f"{field}.target_section")
        if section not in sections:
            raise _error("CONFIG_VALUE_ERROR", "unknown target section", f"{field}.target_section")
        kinds = _strings(item["source_kinds"], f"{field}.source_kinds", True)
        seen_kinds = set()
        for kind_index, kind in enumerate(kinds):
            if kind not in SOURCE_KINDS or kind in seen_kinds:
                raise _error("CONFIG_VALUE_ERROR", "invalid or duplicate source kind", f"{field}.source_kinds.{kind_index}")
            seen_kinds.add(kind)
        anchor = item["requires_chart_anchor"]
        if type(anchor) is not bool:
            raise _error("CONFIG_TYPE_ERROR", "anchor marker must be boolean", f"{field}.requires_chart_anchor")
        if not anchor:
            raise _error("CONFIG_VALUE_ERROR", "chart anchor is required", f"{field}.requires_chart_anchor")
        constraints = _mapping(item["rendering_constraints"], f"{field}.rendering_constraints")
        if not constraints:
            raise _error("CONFIG_VALUE_ERROR", "rendering constraints must not be empty", f"{field}.rendering_constraints")
        prohibited = _strings(item["prohibited_inferences"], f"{field}.prohibited_inferences", True)
        limitations = _strings(item["limitations"], f"{field}.limitations")
        rules.append(NarrativeRule(rule_id, priority, section, kinds, anchor, _freeze(constraints), prohibited, limitations))
        ids.add(rule_id); priorities.add(priority); covered.add(section)
    if covered != set(sections):
        raise _error("CONFIG_VALUE_ERROR", "rules must cover every section", "rules")
    return NarrativeRulesConfig(schema, narrative_version, ontology_version, dimension_version, sections, _freeze(invariants), tuple(sorted(rules, key=lambda item: item.priority)))
