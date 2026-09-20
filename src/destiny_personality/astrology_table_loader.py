from pathlib import Path
from typing import Any, Dict, Optional, Set

import yaml

from .astrology_table_models import (
    AstrologyDignityRow,
    AstrologyDignityTableConfig,
)
from .config_errors import ConfigError
from .config_models import RuntimeConfig
from .vocabulary_models import CanonicalFactVocabularyConfig


FILE = "astrology_dignity_table_v1.yaml"
SCHEMA_VERSION = "astrology-dignity-table-v1"
ROOT_KEYS = {
    "schema_version",
    "table_version",
    "methodology_version",
    "vocabulary_version",
    "rows",
}
ROW_KEYS = {"body_id", "sign_id", "dignity_id", "limitations"}
REFERENCE_CATEGORIES = {
    "body_id": "astrology_body",
    "sign_id": "astrology_sign",
    "dignity_id": "astrology_dignity",
}


def _error(code: str, message: str, field: Optional[str] = None) -> ConfigError:
    return ConfigError(code, message, file=FILE, field=field)


def _join(parent: Optional[str], child: object) -> str:
    return str(child) if parent is None else f"{parent}.{child}"


def _mapping(value: Any, field: Optional[str] = None) -> Dict[str, Any]:
    if type(value) is not dict:
        raise _error("CONFIG_TYPE_ERROR", "value must be a mapping", field)
    return value


def _exact(value: Any, keys: Set[str], field: Optional[str] = None) -> Dict[str, Any]:
    data = _mapping(value, field)
    non_strings = [key for key in data if type(key) is not str]
    if non_strings:
        key = min(non_strings, key=lambda item: (type(item).__name__, repr(item)))
        raise _error("CONFIG_TYPE_ERROR", "mapping keys must be strings", _join(field, key))
    for key in sorted(keys):
        if key not in data:
            raise _error("CONFIG_GAP", "required field is missing", _join(field, key))
    extra = data.keys() - keys
    if extra:
        key = sorted(extra)[0]
        raise _error("CONFIG_VALUE_ERROR", "unknown field", _join(field, key))
    return data


def _string(value: Any, field: str) -> str:
    if type(value) is not str:
        raise _error("CONFIG_TYPE_ERROR", "value must be a string", field)
    if not value.strip():
        raise _error("CONFIG_VALUE_ERROR", "value must not be empty", field)
    return value


def _list(value: Any, field: str) -> list:
    if type(value) is not list:
        raise _error("CONFIG_TYPE_ERROR", "value must be a list", field)
    return value


def _version(value: Any, expected: str, field: str) -> str:
    version = _string(value, field)
    if version != expected:
        raise _error("CONFIG_VERSION_MISMATCH", f"expected version {expected!r}", field)
    return version


def _load(config_dir: Path) -> Dict[str, Any]:
    path = Path(config_dir) / FILE
    if not path.is_file():
        raise _error("CONFIG_GAP", "required configuration file is missing")
    try:
        with path.open(encoding="utf-8") as stream:
            value = yaml.safe_load(stream)
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        raise _error("CONFIG_PARSE_ERROR", "configuration cannot be parsed") from exc
    return _exact(value, ROOT_KEYS)


def load_astrology_dignity_table(
    config_dir: Path,
    runtime_config: RuntimeConfig,
    vocabulary: CanonicalFactVocabularyConfig,
) -> AstrologyDignityTableConfig:
    data = _load(config_dir)
    schema_version = _version(data["schema_version"], SCHEMA_VERSION, "schema_version")
    table_version = _string(data["table_version"], "table_version")
    methodology_version = _version(
        data["methodology_version"],
        runtime_config.astrology.methodology_version,
        "methodology_version",
    )
    vocabulary_version = _version(
        data["vocabulary_version"], vocabulary.vocabulary_version, "vocabulary_version"
    )
    vocabulary_lookup = {
        category.category_id: {entry.canonical_id for entry in category.entries}
        for category in vocabulary.categories
    }
    raw_rows = _list(data["rows"], "rows")
    if not raw_rows:
        raise _error("CONFIG_VALUE_ERROR", "rows must not be empty", "rows")

    rows = []
    seen = set()
    for index, value in enumerate(raw_rows):
        field = f"rows.{index}"
        row = _exact(value, ROW_KEYS, field)
        references = {}
        for key, category_id in REFERENCE_CATEGORIES.items():
            reference_field = f"{field}.{key}"
            reference = _string(row[key], reference_field)
            if reference not in vocabulary_lookup.get(category_id, set()):
                raise _error(
                    "CONFIG_VALUE_ERROR",
                    "unknown canonical vocabulary reference",
                    reference_field,
                )
            references[key] = reference
        unique_key = (
            references["body_id"],
            references["sign_id"],
            references["dignity_id"],
        )
        if unique_key in seen:
            raise _error("CONFIG_VALUE_ERROR", "duplicate dignity row", field)
        seen.add(unique_key)
        limitations_field = f"{field}.limitations"
        limitations = tuple(
            _string(item, f"{limitations_field}.{item_index}")
            for item_index, item in enumerate(_list(row["limitations"], limitations_field))
        )
        rows.append(AstrologyDignityRow(limitations=limitations, **references))

    return AstrologyDignityTableConfig(
        schema_version=schema_version,
        table_version=table_version,
        methodology_version=methodology_version,
        vocabulary_version=vocabulary_version,
        rows=tuple(rows),
    )
