from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any, Dict, Optional, Set, Tuple

import yaml

from .comparison_policy_models import (
    BoundaryMargin,
    CanonicalPrecision,
    FactComparisonPolicyConfig,
    FieldTolerance,
    LogicalComparisonCategory,
    RepresentationEquivalence,
)
from .config_errors import ConfigError
from .config_models import RuntimeConfig
from .vocabulary_models import CanonicalFactVocabularyConfig


FILE = "fact_comparison_policy_v1.yaml"
SCHEMA_VERSION = "fact-comparison-policy-v1"
FACT_SCHEMA_VERSION = "deterministic-facts-v1"
TRIGGERS = (
    "warning",
    "uncertainty",
    "boundary_sensitivity",
    "historical_time_ambiguity",
    "policy_anomaly",
)
ROOT_KEYS = {
    "schema_version", "policy_version", "methodology_versions",
    "vocabulary_version", "fact_schema_version", "triggers",
    "logical_categories", "boundary_margins", "canonical_precision",
    "tolerances", "representation_equivalences",
}
METHODOLOGY_KEYS = {"bazi", "astrology"}
CATEGORY_KEYS = {"category_id", "comparison_mode"}
MARGIN_KEYS = {"category_id", "margin"}
PRECISION_KEYS = {"category_id", "decimal_places"}
TOLERANCE_KEYS = {"category_id", "absolute_tolerance"}
EQUIVALENCE_KEYS = {
    "logical_category_id", "vocabulary_category_id", "canonical_id",
    "equivalent_values",
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


def _nonnegative_decimal(value: Any, field: str) -> Decimal:
    if type(value) not in (str, int, float):
        raise _error("CONFIG_TYPE_ERROR", "value must be a decimal number", field)
    try:
        number = Decimal(str(value))
    except InvalidOperation as exc:
        raise _error("CONFIG_TYPE_ERROR", "value must be a decimal number", field) from exc
    if not number.is_finite() or number < 0:
        raise _error("CONFIG_VALUE_ERROR", "value must be finite and non-negative", field)
    return number


def _unique_strings(value: Any, field: str, *, nonempty: bool = True) -> Tuple[str, ...]:
    items = _list(value, field)
    if nonempty and not items:
        raise _error("CONFIG_VALUE_ERROR", "list must not be empty", field)
    result = []
    seen = set()
    for index, item in enumerate(items):
        item_field = f"{field}.{index}"
        parsed = _string(item, item_field)
        if parsed in seen:
            raise _error("CONFIG_VALUE_ERROR", "duplicate value", item_field)
        seen.add(parsed)
        result.append(parsed)
    return tuple(result)


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


def _parse_triggers(value: Any) -> Tuple[str, ...]:
    triggers = _unique_strings(value, "triggers")
    present = set(triggers)
    for trigger in TRIGGERS:
        if trigger not in present:
            raise _error("CONFIG_GAP", "required trigger is missing", f"triggers.{trigger}")
    for index, trigger in enumerate(triggers):
        if trigger not in TRIGGERS:
            raise _error("CONFIG_VALUE_ERROR", "unknown trigger", f"triggers.{index}")
    return triggers


def _parse_categories(value: Any) -> Tuple[Tuple[LogicalComparisonCategory, ...], Dict[str, str]]:
    raw_categories = _list(value, "logical_categories")
    if not raw_categories:
        raise _error("CONFIG_VALUE_ERROR", "categories must not be empty", "logical_categories")
    categories = []
    modes = {}
    for index, value in enumerate(raw_categories):
        field = f"logical_categories.{index}"
        data = _exact(value, CATEGORY_KEYS, field)
        category_id = _string(data["category_id"], f"{field}.category_id")
        if category_id in modes:
            raise _error("CONFIG_VALUE_ERROR", "duplicate category identifier", f"{field}.category_id")
        mode = _string(data["comparison_mode"], f"{field}.comparison_mode")
        if mode not in {"exact", "numeric"}:
            raise _error("CONFIG_VALUE_ERROR", "comparison_mode must be exact or numeric", f"{field}.comparison_mode")
        modes[category_id] = mode
        categories.append(LogicalComparisonCategory(category_id, mode))
    return tuple(categories), modes


def _parse_numeric_records(value: Any, field: str, keys: Set[str], value_key: str, modes: Dict[str, str]):
    records = []
    seen = set()
    for index, value in enumerate(_list(value, field)):
        item_field = f"{field}.{index}"
        data = _exact(value, keys, item_field)
        category_id = _string(data["category_id"], f"{item_field}.category_id")
        if category_id not in modes:
            raise _error("CONFIG_VALUE_ERROR", "unknown logical category", f"{item_field}.category_id")
        if modes[category_id] != "numeric":
            raise _error(
                "CONFIG_VALUE_ERROR",
                "numeric policy requires a numeric comparison category",
                f"{item_field}.category_id",
            )
        if category_id in seen:
            raise _error("CONFIG_VALUE_ERROR", "duplicate category policy", f"{item_field}.category_id")
        seen.add(category_id)
        records.append((category_id, data[value_key], item_field))
    return records, seen


def load_fact_comparison_policy(
    config_dir: Path,
    runtime_config: RuntimeConfig,
    vocabulary: CanonicalFactVocabularyConfig,
) -> FactComparisonPolicyConfig:
    data = _load(config_dir)
    schema_version = _version(data["schema_version"], SCHEMA_VERSION, "schema_version")
    policy_version = _string(data["policy_version"], "policy_version")
    methodology = _exact(data["methodology_versions"], METHODOLOGY_KEYS, "methodology_versions")
    bazi_methodology_version = _version(
        methodology["bazi"], runtime_config.bazi.methodology_version, "methodology_versions.bazi"
    )
    astrology_methodology_version = _version(
        methodology["astrology"], runtime_config.astrology.methodology_version, "methodology_versions.astrology"
    )
    vocabulary_version = _version(
        data["vocabulary_version"], vocabulary.vocabulary_version, "vocabulary_version"
    )
    fact_schema_version = _version(
        data["fact_schema_version"], FACT_SCHEMA_VERSION, "fact_schema_version"
    )
    triggers = _parse_triggers(data["triggers"])
    logical_categories, modes = _parse_categories(data["logical_categories"])

    raw_margins, margin_categories = _parse_numeric_records(
        data["boundary_margins"], "boundary_margins", MARGIN_KEYS, "margin", modes
    )
    margins = tuple(
        BoundaryMargin(category_id, _nonnegative_decimal(value, f"{field}.margin"))
        for category_id, value, field in raw_margins
    )
    raw_precision, precision_categories = _parse_numeric_records(
        data["canonical_precision"], "canonical_precision", PRECISION_KEYS, "decimal_places", modes
    )
    precision = []
    for category_id, value, field in raw_precision:
        value_field = f"{field}.decimal_places"
        if type(value) is not int:
            raise _error("CONFIG_TYPE_ERROR", "value must be an integer", value_field)
        if value < 0:
            raise _error("CONFIG_VALUE_ERROR", "value must be non-negative", value_field)
        precision.append(CanonicalPrecision(category_id, value))
    raw_tolerances, tolerance_categories = _parse_numeric_records(
        data["tolerances"], "tolerances", TOLERANCE_KEYS, "absolute_tolerance", modes
    )
    tolerances = tuple(
        FieldTolerance(
            category_id,
            _nonnegative_decimal(value, f"{field}.absolute_tolerance"),
        )
        for category_id, value, field in raw_tolerances
    )

    numeric_categories = {key for key, mode in modes.items() if mode == "numeric"}
    for field, covered in (
        ("boundary_margins", margin_categories),
        ("canonical_precision", precision_categories),
        ("tolerances", tolerance_categories),
    ):
        if numeric_categories - covered:
            raise _error("CONFIG_GAP", "numeric category policy is incomplete", field)

    vocabulary_lookup = {
        category.category_id: {entry.canonical_id for entry in category.entries}
        for category in vocabulary.categories
    }
    equivalences = []
    seen_equivalences = set()
    for index, value in enumerate(_list(data["representation_equivalences"], "representation_equivalences")):
        field = f"representation_equivalences.{index}"
        item = _exact(value, EQUIVALENCE_KEYS, field)
        logical_id = _string(item["logical_category_id"], f"{field}.logical_category_id")
        if logical_id not in modes:
            raise _error("CONFIG_VALUE_ERROR", "unknown logical category", f"{field}.logical_category_id")
        vocabulary_category = _string(
            item["vocabulary_category_id"], f"{field}.vocabulary_category_id"
        )
        if vocabulary_category not in vocabulary_lookup:
            raise _error("CONFIG_VALUE_ERROR", "unknown vocabulary category", f"{field}.vocabulary_category_id")
        canonical_id = _string(item["canonical_id"], f"{field}.canonical_id")
        if canonical_id not in vocabulary_lookup[vocabulary_category]:
            raise _error("CONFIG_VALUE_ERROR", "unknown canonical vocabulary reference", f"{field}.canonical_id")
        unique_key = (logical_id, vocabulary_category, canonical_id)
        if unique_key in seen_equivalences:
            raise _error("CONFIG_VALUE_ERROR", "duplicate representation equivalence", field)
        seen_equivalences.add(unique_key)
        equivalent_values = _unique_strings(
            item["equivalent_values"], f"{field}.equivalent_values"
        )
        equivalences.append(
            RepresentationEquivalence(
                logical_id, vocabulary_category, canonical_id, equivalent_values
            )
        )

    return FactComparisonPolicyConfig(
        schema_version=schema_version,
        policy_version=policy_version,
        bazi_methodology_version=bazi_methodology_version,
        astrology_methodology_version=astrology_methodology_version,
        vocabulary_version=vocabulary_version,
        fact_schema_version=fact_schema_version,
        triggers=triggers,
        logical_categories=logical_categories,
        boundary_margins=margins,
        canonical_precision=tuple(precision),
        tolerances=tolerances,
        representation_equivalences=tuple(equivalences),
    )
