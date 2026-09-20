from pathlib import Path
from typing import Any, Dict, Optional, Set, Tuple

import yaml

from .config_errors import ConfigError
from .config_models import RuntimeConfig
from .vocabulary_models import (
    CanonicalFactVocabularyConfig,
    VocabularyCategory,
    VocabularyEntry,
)


FILE = "canonical_fact_vocabulary_v1.yaml"
SCHEMA_VERSION = "canonical-fact-vocabulary-v1"
CATEGORY_IDS: Tuple[str, ...] = (
    "bazi_stem",
    "bazi_branch",
    "bazi_ten_god",
    "bazi_relation",
    "astrology_body",
    "astrology_sign",
    "astrology_aspect",
    "astrology_angle",
    "astrology_dignity",
    "astrology_node",
)
ROOT_KEYS = {
    "schema_version",
    "vocabulary_version",
    "methodology_versions",
    "categories",
}
METHODOLOGY_KEYS = {"bazi", "astrology"}
CATEGORY_KEYS = {"entries"}
ENTRY_KEYS = {"canonical_id", "aliases"}


def _error(
    code: str, message: str, field: Optional[str] = None
) -> ConfigError:
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
            raise _error(
                "CONFIG_GAP", "required field is missing", _join(field, key)
            )
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
            "CONFIG_VERSION_MISMATCH",
            f"expected version {expected!r}",
            field,
        )
    return version


def _normalized(value: str) -> str:
    return value.strip().casefold()


def _parse_entry(
    value: Any,
    field: str,
    seen_tokens: Set[str],
) -> VocabularyEntry:
    data = _require_exact_keys(value, ENTRY_KEYS, field)
    canonical_field = f"{field}.canonical_id"
    canonical_id = _require_string(data["canonical_id"], canonical_field)
    normalized_id = _normalized(canonical_id)
    if normalized_id in seen_tokens:
        raise _error(
            "CONFIG_VALUE_ERROR", "ambiguous canonical identifier or alias", canonical_field
        )
    seen_tokens.add(normalized_id)

    aliases_field = f"{field}.aliases"
    raw_aliases = _require_list(data["aliases"], aliases_field)
    aliases = []
    for index, value in enumerate(raw_aliases):
        alias_field = f"{aliases_field}.{index}"
        alias = _require_string(value, alias_field)
        normalized_alias = _normalized(alias)
        if normalized_alias in seen_tokens:
            raise _error(
                "CONFIG_VALUE_ERROR",
                "ambiguous canonical identifier or alias",
                alias_field,
            )
        seen_tokens.add(normalized_alias)
        aliases.append(alias)
    return VocabularyEntry(canonical_id=canonical_id, aliases=tuple(aliases))


def _parse_category(category_id: str, value: Any) -> VocabularyCategory:
    field = f"categories.{category_id}"
    data = _require_exact_keys(value, CATEGORY_KEYS, field)
    entries_field = f"{field}.entries"
    raw_entries = _require_list(data["entries"], entries_field)
    if not raw_entries:
        raise _error(
            "CONFIG_VALUE_ERROR", "entries must not be empty", entries_field
        )
    seen_tokens: Set[str] = set()
    entries = tuple(
        _parse_entry(item, f"{entries_field}.{index}", seen_tokens)
        for index, item in enumerate(raw_entries)
    )
    return VocabularyCategory(category_id=category_id, entries=entries)


def _load_document(config_dir: Path) -> Dict[str, Any]:
    path = Path(config_dir) / FILE
    if not path.is_file():
        raise _error("CONFIG_GAP", "required configuration file is missing")
    try:
        with path.open(encoding="utf-8") as stream:
            value = yaml.safe_load(stream)
    except (OSError, yaml.YAMLError) as exc:
        raise _error("CONFIG_PARSE_ERROR", "configuration cannot be parsed") from exc
    return _require_exact_keys(value, ROOT_KEYS)


def load_canonical_fact_vocabulary(
    config_dir: Path,
    runtime_config: RuntimeConfig,
) -> CanonicalFactVocabularyConfig:
    data = _load_document(config_dir)
    schema_version = _validate_version(
        data["schema_version"], SCHEMA_VERSION, "schema_version"
    )
    vocabulary_version = _require_string(
        data["vocabulary_version"], "vocabulary_version"
    )

    methodology = _require_exact_keys(
        data["methodology_versions"],
        METHODOLOGY_KEYS,
        "methodology_versions",
    )
    bazi_version = _validate_version(
        methodology["bazi"],
        runtime_config.bazi.methodology_version,
        "methodology_versions.bazi",
    )
    astrology_version = _validate_version(
        methodology["astrology"],
        runtime_config.astrology.methodology_version,
        "methodology_versions.astrology",
    )

    categories = _require_exact_keys(
        data["categories"], set(CATEGORY_IDS), "categories"
    )
    parsed_categories = tuple(
        _parse_category(category_id, categories[category_id])
        for category_id in CATEGORY_IDS
    )
    return CanonicalFactVocabularyConfig(
        schema_version=schema_version,
        vocabulary_version=vocabulary_version,
        bazi_methodology_version=bazi_version,
        astrology_methodology_version=astrology_version,
        categories=parsed_categories,
    )
