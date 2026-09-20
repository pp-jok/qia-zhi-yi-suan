from pathlib import Path
from typing import Any, Dict, Optional, Set, Tuple

import yaml

from .bazi_table_models import (
    BaziDeterministicTablesConfig,
    BaziTableRule,
    BaziTableSection,
)
from .config_errors import ConfigError
from .config_models import RuntimeConfig
from .vocabulary_models import CanonicalFactVocabularyConfig


FILE = "bazi_deterministic_tables_v1.yaml"
SCHEMA_VERSION = "bazi-deterministic-tables-v1"
SECTIONS = ("hidden_stems", "ten_gods", "relations")
OUTPUT_CATEGORIES = {
    "hidden_stems": "bazi_stem",
    "ten_gods": "bazi_ten_god",
    "relations": "bazi_relation",
}
ROOT_KEYS = {
    "schema_version",
    "table_version",
    "methodology_version",
    "vocabulary_version",
    "tables",
}
RULE_KEYS = {"rule_id", "inputs", "outputs", "limitations"}


def _error(code: str, message: str, field: Optional[str] = None) -> ConfigError:
    return ConfigError(code, message, file=FILE, field=field)


def _join(parent: Optional[str], child: object) -> str:
    return str(child) if parent is None else f"{parent}.{child}"


def _require_mapping(value: Any, field: Optional[str] = None) -> Dict[str, Any]:
    if type(value) is not dict:
        raise _error("CONFIG_TYPE_ERROR", "value must be a mapping", field)
    return value


def _require_exact_keys(
    value: Any, required: Set[str], field: Optional[str] = None
) -> Dict[str, Any]:
    data = _require_mapping(value, field)
    non_string_keys = [key for key in data if type(key) is not str]
    if non_string_keys:
        key = min(non_string_keys, key=lambda item: (type(item).__name__, repr(item)))
        raise _error(
            "CONFIG_TYPE_ERROR", "mapping keys must be strings", _join(field, key)
        )
    for key in sorted(required):
        if key not in data:
            raise _error("CONFIG_GAP", "required field is missing", _join(field, key))
    extra = data.keys() - required
    if extra:
        key = sorted(extra)[0]
        raise _error("CONFIG_VALUE_ERROR", "unknown field", _join(field, key))
    return data


def _require_string(value: Any, field: str) -> str:
    if type(value) is not str:
        raise _error("CONFIG_TYPE_ERROR", "value must be a string", field)
    if not value.strip():
        raise _error("CONFIG_VALUE_ERROR", "value must not be empty", field)
    return value


def _require_list(value: Any, field: str) -> list:
    if type(value) is not list:
        raise _error("CONFIG_TYPE_ERROR", "value must be a list", field)
    return value


def _validate_version(value: Any, expected: str, field: str) -> str:
    version = _require_string(value, field)
    if version != expected:
        raise _error(
            "CONFIG_VERSION_MISMATCH", f"expected version {expected!r}", field
        )
    return version


def _vocabulary_lookup(
    vocabulary: CanonicalFactVocabularyConfig,
) -> Dict[str, Set[str]]:
    return {
        category.category_id: {entry.canonical_id for entry in category.entries}
        for category in vocabulary.categories
    }


def _parse_references(
    value: Any, field: str, vocabulary: Dict[str, Set[str]]
) -> Tuple[Tuple[str, Tuple[str, ...]], ...]:
    data = _require_mapping(value, field)
    if not data:
        raise _error("CONFIG_VALUE_ERROR", "references must not be empty", field)
    non_string_keys = [key for key in data if type(key) is not str]
    if non_string_keys:
        key = min(non_string_keys, key=lambda item: (type(item).__name__, repr(item)))
        raise _error(
            "CONFIG_TYPE_ERROR", "mapping keys must be strings", _join(field, key)
        )

    result = []
    for category_id, raw_references in data.items():
        category_field = f"{field}.{category_id}"
        if not category_id.startswith("bazi_") or category_id not in vocabulary:
            raise _error(
                "CONFIG_VALUE_ERROR", "unknown Bazi vocabulary category", category_field
            )
        references = _require_list(raw_references, category_field)
        if not references:
            raise _error(
                "CONFIG_VALUE_ERROR", "references must not be empty", category_field
            )
        parsed = []
        seen: Set[str] = set()
        for index, value in enumerate(references):
            reference_field = f"{category_field}.{index}"
            reference = _require_string(value, reference_field)
            if reference not in vocabulary[category_id]:
                raise _error(
                    "CONFIG_VALUE_ERROR",
                    "unknown canonical vocabulary reference",
                    reference_field,
                )
            if reference in seen:
                raise _error(
                    "CONFIG_VALUE_ERROR", "duplicate vocabulary reference", reference_field
                )
            seen.add(reference)
            parsed.append(reference)
        result.append((category_id, tuple(parsed)))
    return tuple(result)


def _parse_rule(
    value: Any,
    field: str,
    vocabulary: Dict[str, Set[str]],
    seen_rule_ids: Set[str],
    expected_output_category: str,
) -> BaziTableRule:
    data = _require_exact_keys(value, RULE_KEYS, field)
    rule_field = f"{field}.rule_id"
    rule_id = _require_string(data["rule_id"], rule_field)
    if rule_id in seen_rule_ids:
        raise _error("CONFIG_VALUE_ERROR", "duplicate rule identifier", rule_field)
    seen_rule_ids.add(rule_id)

    limitations_field = f"{field}.limitations"
    limitations = tuple(
        _require_string(item, f"{limitations_field}.{index}")
        for index, item in enumerate(_require_list(data["limitations"], limitations_field))
    )
    outputs_field = f"{field}.outputs"
    outputs = _parse_references(data["outputs"], outputs_field, vocabulary)
    output_categories = {category_id for category_id, _ in outputs}
    unexpected = output_categories - {expected_output_category}
    if unexpected:
        category_id = sorted(unexpected)[0]
        raise _error(
            "CONFIG_VALUE_ERROR",
            "category is not valid for this Bazi table section",
            f"{outputs_field}.{category_id}",
        )
    if expected_output_category not in output_categories:
        raise _error(
            "CONFIG_GAP",
            "required output category is missing",
            f"{outputs_field}.{expected_output_category}",
        )
    return BaziTableRule(
        rule_id=rule_id,
        inputs=_parse_references(data["inputs"], f"{field}.inputs", vocabulary),
        outputs=outputs,
        limitations=limitations,
    )


def _load_document(config_dir: Path) -> Dict[str, Any]:
    path = Path(config_dir) / FILE
    if not path.is_file():
        raise _error("CONFIG_GAP", "required configuration file is missing")
    try:
        with path.open(encoding="utf-8") as stream:
            value = yaml.safe_load(stream)
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        raise _error("CONFIG_PARSE_ERROR", "configuration cannot be parsed") from exc
    return _require_exact_keys(value, ROOT_KEYS)


def load_bazi_deterministic_tables(
    config_dir: Path,
    runtime_config: RuntimeConfig,
    vocabulary: CanonicalFactVocabularyConfig,
) -> BaziDeterministicTablesConfig:
    data = _load_document(config_dir)
    schema_version = _validate_version(
        data["schema_version"], SCHEMA_VERSION, "schema_version"
    )
    table_version = _require_string(data["table_version"], "table_version")
    methodology_version = _validate_version(
        data["methodology_version"],
        runtime_config.bazi.methodology_version,
        "methodology_version",
    )
    vocabulary_version = _validate_version(
        data["vocabulary_version"],
        vocabulary.vocabulary_version,
        "vocabulary_version",
    )
    raw_tables = _require_exact_keys(data["tables"], set(SECTIONS), "tables")
    vocabulary_lookup = _vocabulary_lookup(vocabulary)
    seen_rule_ids: Set[str] = set()
    tables = []
    for section_id in SECTIONS:
        field = f"tables.{section_id}"
        raw_rules = _require_list(raw_tables[section_id], field)
        if not raw_rules:
            raise _error("CONFIG_VALUE_ERROR", "rules must not be empty", field)
        rules = tuple(
            _parse_rule(
                rule,
                f"{field}.{index}",
                vocabulary_lookup,
                seen_rule_ids,
                OUTPUT_CATEGORIES[section_id],
            )
            for index, rule in enumerate(raw_rules)
        )
        tables.append(BaziTableSection(section_id=section_id, rules=rules))

    return BaziDeterministicTablesConfig(
        schema_version=schema_version,
        table_version=table_version,
        methodology_version=methodology_version,
        vocabulary_version=vocabulary_version,
        tables=tuple(tables),
    )
