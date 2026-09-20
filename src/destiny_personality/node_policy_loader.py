from pathlib import Path
from typing import Any, Dict, Optional, Set

import yaml

from .config_errors import ConfigError
from .config_models import RuntimeConfig
from .node_policy_models import AstrologyNodeOutputPolicy, AstrologyNodePolicyConfig
from .vocabulary_models import CanonicalFactVocabularyConfig


FILE = "astrology_node_policy_v1.yaml"
SCHEMA_VERSION = "astrology-node-policy-v1"
ROOT_KEYS = {
    "schema_version", "policy_version", "methodology_version",
    "vocabulary_version", "node_id", "output",
}
OUTPUT_KEYS = {
    "included", "phase", "aspect_participation", "dignity_participation",
    "weight_role", "time_sensitive",
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


def _boolean(value: Any, field: str) -> bool:
    if type(value) is not bool:
        raise _error("CONFIG_TYPE_ERROR", "value must be a boolean", field)
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


def load_astrology_node_policy(
    config_dir: Path,
    runtime_config: RuntimeConfig,
    vocabulary: CanonicalFactVocabularyConfig,
) -> AstrologyNodePolicyConfig:
    data = _load(config_dir)
    schema_version = _version(data["schema_version"], SCHEMA_VERSION, "schema_version")
    policy_version = _string(data["policy_version"], "policy_version")
    methodology_version = _version(
        data["methodology_version"],
        runtime_config.astrology.methodology_version,
        "methodology_version",
    )
    vocabulary_version = _version(
        data["vocabulary_version"], vocabulary.vocabulary_version, "vocabulary_version"
    )
    node_id = _string(data["node_id"], "node_id")
    node_ids = {
        entry.canonical_id
        for category in vocabulary.categories
        if category.category_id == "astrology_node"
        for entry in category.entries
    }
    if node_id not in node_ids:
        raise _error(
            "CONFIG_VALUE_ERROR", "unknown canonical vocabulary reference", "node_id"
        )

    output = _exact(data["output"], OUTPUT_KEYS, "output")
    included = _boolean(output["included"], "output.included")
    phase = _string(output["phase"], "output.phase")
    aspect_participation = _boolean(
        output["aspect_participation"], "output.aspect_participation"
    )
    dignity_participation = _boolean(
        output["dignity_participation"], "output.dignity_participation"
    )
    weight_role = _string(output["weight_role"], "output.weight_role")
    time_sensitive = _boolean(output["time_sensitive"], "output.time_sensitive")
    if not included and aspect_participation:
        raise _error(
            "CONFIG_VALUE_ERROR",
            "an excluded node cannot participate in aspects",
            "output.aspect_participation",
        )
    if not included and dignity_participation:
        raise _error(
            "CONFIG_VALUE_ERROR",
            "an excluded node cannot participate in dignities",
            "output.dignity_participation",
        )
    if included != runtime_config.astrology.core.true_node:
        raise _error(
            "CONFIG_VALUE_ERROR",
            "node inclusion must match the accepted astrology methodology",
            "output.included",
        )

    return AstrologyNodePolicyConfig(
        schema_version=schema_version,
        policy_version=policy_version,
        methodology_version=methodology_version,
        vocabulary_version=vocabulary_version,
        node_id=node_id,
        output=AstrologyNodeOutputPolicy(
            included=included,
            phase=phase,
            aspect_participation=aspect_participation,
            dignity_participation=dignity_participation,
            weight_role=weight_role,
            time_sensitive=time_sensitive,
        ),
    )
