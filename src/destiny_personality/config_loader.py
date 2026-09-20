from pathlib import Path
import re
from typing import Any, Dict, Optional

import yaml

from .config_errors import ConfigError
from .config_models import (
    AstrologyAspectsConfig,
    AstrologyBodiesConfig,
    AstrologyCoreConfig,
    AstrologyMethodologyConfig,
    BaziCalendarConfig,
    BaziMethodologyConfig,
    BaziRelationsConfig,
    BaziTimeConfig,
    DignityConfig,
    IntegerRange,
    OuterPlanetsConfig,
    PersonalityScopeConfig,
    PrimitiveRelation,
    PrimitiveRelationGraphConfig,
    RuntimeConfig,
    SalienceByOrbConfig,
    ScoreModelConfig,
    ScoreRulesConfig,
    SynthesisPriorityConfig,
)


BAZI_FILE = "bazi_methodology_v1.yaml"
ASTROLOGY_FILE = "astrology_methodology_v1.yaml"
SCORE_FILE = "score_model_v2_2.yaml"
RELATION_FILE = "primitive_relation_graph_v1.yaml"

RELATION_TYPES = {
    "reinforcing",
    "adjacent",
    "complementary",
    "potential_tension",
    "contextualizing",
    "independent",
}
PRIMITIVE_ID_PATTERN = re.compile(r"P[0-9]{3}")

EXPECTED_BAZI = {
    "methodology_version": "bazi-core-v1.0",
    "calendar": {
        "input_calendar": "gregorian",
        "month_boundary": "solar_terms_jie",
        "day_boundary": "00:00",
        "day_boundary_time_basis": "true_solar_time",
    },
    "time": {
        "historical_timezone_required": True,
        "dst_correction_required": True,
        "true_solar_time_default": True,
        "allow_standard_time_mode": True,
    },
    "month_mapping": {
        "立春": "寅",
        "惊蛰": "卯",
        "清明": "辰",
        "立夏": "巳",
        "芒种": "午",
        "小暑": "未",
        "立秋": "申",
        "白露": "酉",
        "寒露": "戌",
        "立冬": "亥",
        "大雪": "子",
        "小寒": "丑",
    },
    "relations": {
        "heavenly_stem_combinations": True,
        "six_combinations": True,
        "three_harmonies": True,
        "three_meetings": True,
        "six_clashes": True,
        "six_harms": True,
        "three_punishments": True,
        "self_punishments": ["辰", "午", "酉", "亥"],
    },
    "personality_scope": {
        "include_luck_cycles": False,
        "include_annual_transits": False,
    },
}

EXPECTED_ASTROLOGY = {
    "methodology_version": "western-tropical-v1.0",
    "core": {
        "zodiac": "tropical",
        "reference": "geocentric",
        "house_system": "placidus",
        "node": True,
    },
    "bodies": {
        "planets": [
            "Sun",
            "Moon",
            "Mercury",
            "Venus",
            "Mars",
            "Jupiter",
            "Saturn",
            "Uranus",
            "Neptune",
            "Pluto",
        ],
        "angles": ["Ascendant", "MC"],
    },
    "aspects": {
        "enabled": ["conjunction", "opposition", "square", "trine", "sextile"],
        "minor_aspects_enabled": False,
        "max_orbs": {
            "conjunction": 8,
            "opposition": 8,
            "square": 7,
            "trine": 7,
            "sextile": 5,
        },
        "luminary_orb_bonus": 1,
        "angle_orb": 4,
    },
    "salience_by_orb": {
        "dominant_max": 1,
        "strong_max": 3,
        "moderate_max": 5,
    },
    "dignity": {
        "enabled": True,
        "types": ["domicile", "detriment", "exaltation", "fall"],
        "role": "modifier_only",
    },
    "outer_planets": {
        "require_personal_or_angle_contact_for_high_weight": True,
    },
}

EXPECTED_SCORE = {
    "score_model_version": "2.2",
    "trait_salience": {"min": 0, "max": 4},
    "evidence_stability": {"values": ["high", "medium", "low", "unstable"]},
    "cross_system_relation": {
        "values": [
            "validation",
            "complement",
            "contextualization",
            "tension",
            "correction",
            "single_system",
        ]
    },
    "synthesis_priority": {"min": 0, "max": 4, "core_threshold": 3},
    "rules": {
        "cross_system_validation_changes_trait_salience": False,
        "tension_reduces_trait_salience": False,
        "tension_can_raise_synthesis_priority": True,
        "unknown_is_not_low": True,
    },
}


def _error(
    code: str,
    message: str,
    filename: str,
    field: Optional[str] = None,
) -> ConfigError:
    return ConfigError(code, message, file=filename, field=field)


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


def _join_field(parent: Optional[str], child: object) -> str:
    return str(child) if parent is None else f"{parent}.{child}"


def _validate_exact(
    actual: Any,
    expected: Any,
    filename: str,
    field: Optional[str] = None,
) -> None:
    if type(actual) is not type(expected):
        raise _error(
            "CONFIG_TYPE_ERROR",
            f"expected {type(expected).__name__}, got {type(actual).__name__}",
            filename,
            field,
        )
    if isinstance(expected, dict):
        for key in expected:
            child = _join_field(field, key)
            if key not in actual:
                raise _error("CONFIG_GAP", "required field is missing", filename, child)
            _validate_exact(actual[key], expected[key], filename, child)
        extra = actual.keys() - expected.keys()
        if extra:
            child = _join_field(field, sorted(extra)[0])
            raise _error("CONFIG_VALUE_ERROR", "unknown field", filename, child)
        return
    if isinstance(expected, list):
        if len(actual) != len(expected):
            raise _error(
                "CONFIG_VALUE_ERROR", "list does not match frozen values", filename, field
            )
        for index, expected_item in enumerate(expected):
            _validate_exact(
                actual[index], expected_item, filename, _join_field(field, index)
            )
        return
    if actual != expected:
        raise _error("CONFIG_VALUE_ERROR", f"expected {expected!r}", filename, field)


def _validate_version(
    data: Dict[str, Any],
    field: str,
    expected: str,
    filename: str,
) -> None:
    if field not in data:
        raise _error("CONFIG_GAP", "required version is missing", filename, field)
    if type(data[field]) is not str:
        raise _error("CONFIG_TYPE_ERROR", "version must be a string", filename, field)
    if data[field] != expected:
        raise _error(
            "CONFIG_VERSION_MISMATCH",
            f"expected version {expected!r}",
            filename,
            field,
        )


def _parse_bazi(data: Dict[str, Any]) -> BaziMethodologyConfig:
    _validate_version(data, "methodology_version", "bazi-core-v1.0", BAZI_FILE)
    _validate_exact(data, EXPECTED_BAZI, BAZI_FILE)
    calendar = data["calendar"]
    time = data["time"]
    relations = data["relations"]
    scope = data["personality_scope"]
    return BaziMethodologyConfig(
        methodology_version=data["methodology_version"],
        calendar=BaziCalendarConfig(
            input_calendar=calendar["input_calendar"],
            month_boundary=calendar["month_boundary"],
            day_boundary=calendar["day_boundary"],
            day_boundary_time_basis=calendar["day_boundary_time_basis"],
        ),
        time=BaziTimeConfig(
            historical_timezone_required=time["historical_timezone_required"],
            dst_correction_required=time["dst_correction_required"],
            true_solar_time_default=time["true_solar_time_default"],
            allow_standard_time_mode=time["allow_standard_time_mode"],
        ),
        month_mapping=tuple(data["month_mapping"].items()),
        relations=BaziRelationsConfig(
            heavenly_stem_combinations=relations["heavenly_stem_combinations"],
            six_combinations=relations["six_combinations"],
            three_harmonies=relations["three_harmonies"],
            three_meetings=relations["three_meetings"],
            six_clashes=relations["six_clashes"],
            six_harms=relations["six_harms"],
            three_punishments=relations["three_punishments"],
            self_punishments=tuple(relations["self_punishments"]),
        ),
        personality_scope=PersonalityScopeConfig(
            include_luck_cycles=scope["include_luck_cycles"],
            include_annual_transits=scope["include_annual_transits"],
        ),
    )


def _parse_astrology(data: Dict[str, Any]) -> AstrologyMethodologyConfig:
    _validate_version(
        data, "methodology_version", "western-tropical-v1.0", ASTROLOGY_FILE
    )
    _validate_exact(data, EXPECTED_ASTROLOGY, ASTROLOGY_FILE)
    salience = data["salience_by_orb"]
    if not (
        salience["dominant_max"]
        < salience["strong_max"]
        < salience["moderate_max"]
    ):
        raise _error(
            "CONFIG_VALUE_ERROR",
            "salience thresholds must be strictly increasing",
            ASTROLOGY_FILE,
            "salience_by_orb",
        )
    return AstrologyMethodologyConfig(
        methodology_version=data["methodology_version"],
        core=AstrologyCoreConfig(
            zodiac=data["core"]["zodiac"],
            reference=data["core"]["reference"],
            house_system=data["core"]["house_system"],
            true_node=data["core"]["node"],
        ),
        bodies=AstrologyBodiesConfig(
            planets=tuple(data["bodies"]["planets"]),
            angles=tuple(data["bodies"]["angles"]),
        ),
        aspects=AstrologyAspectsConfig(
            enabled=tuple(data["aspects"]["enabled"]),
            minor_aspects_enabled=data["aspects"]["minor_aspects_enabled"],
            max_orbs=tuple(data["aspects"]["max_orbs"].items()),
            luminary_orb_bonus=data["aspects"]["luminary_orb_bonus"],
            angle_orb=data["aspects"]["angle_orb"],
        ),
        salience_by_orb=SalienceByOrbConfig(
            dominant_max=salience["dominant_max"],
            strong_max=salience["strong_max"],
            moderate_max=salience["moderate_max"],
        ),
        dignity=DignityConfig(
            enabled=data["dignity"]["enabled"],
            dignity_types=tuple(data["dignity"]["types"]),
            role=data["dignity"]["role"],
        ),
        outer_planets=OuterPlanetsConfig(
            require_personal_or_angle_contact_for_high_weight=data["outer_planets"]
            ["require_personal_or_angle_contact_for_high_weight"]
        ),
    )


def _parse_score(data: Dict[str, Any]) -> ScoreModelConfig:
    _validate_version(data, "score_model_version", "2.2", SCORE_FILE)
    _validate_exact(data, EXPECTED_SCORE, SCORE_FILE)
    rules = data["rules"]
    return ScoreModelConfig(
        score_model_version=data["score_model_version"],
        trait_salience=IntegerRange(
            minimum=data["trait_salience"]["min"],
            maximum=data["trait_salience"]["max"],
        ),
        evidence_stability=tuple(data["evidence_stability"]["values"]),
        cross_system_relation=tuple(data["cross_system_relation"]["values"]),
        synthesis_priority=SynthesisPriorityConfig(
            minimum=data["synthesis_priority"]["min"],
            maximum=data["synthesis_priority"]["max"],
            core_threshold=data["synthesis_priority"]["core_threshold"],
        ),
        rules=ScoreRulesConfig(
            cross_system_validation_changes_trait_salience=rules[
                "cross_system_validation_changes_trait_salience"
            ],
            tension_reduces_trait_salience=rules["tension_reduces_trait_salience"],
            tension_can_raise_synthesis_priority=rules[
                "tension_can_raise_synthesis_priority"
            ],
            unknown_is_not_low=rules["unknown_is_not_low"],
        ),
    )


def _require_relation_keys(item: Dict[str, Any], index: int) -> None:
    for key in ("left", "right", "relation"):
        if key not in item:
            raise _error(
                "CONFIG_GAP",
                "required field is missing",
                RELATION_FILE,
                f"relations.{index}.{key}",
            )
    extra = item.keys() - {"left", "right", "relation", "dynamic_family"}
    if extra:
        key = sorted(extra)[0]
        raise _error(
            "CONFIG_VALUE_ERROR",
            "unknown field",
            RELATION_FILE,
            f"relations.{index}.{key}",
        )


def _parse_relation(data: Dict[str, Any], index: int) -> PrimitiveRelation:
    field = f"relations.{index}"
    if type(data) is not dict:
        raise _error(
            "CONFIG_TYPE_ERROR", "relation must be a mapping", RELATION_FILE, field
        )
    _require_relation_keys(data, index)
    for key in ("left", "right", "relation"):
        if type(data[key]) is not str:
            raise _error(
                "CONFIG_TYPE_ERROR",
                "value must be a string",
                RELATION_FILE,
                f"{field}.{key}",
            )
    left = data["left"]
    right = data["right"]
    relation = data["relation"]
    if PRIMITIVE_ID_PATTERN.fullmatch(left) is None:
        raise _error(
            "CONFIG_VALUE_ERROR", "invalid Primitive ID", RELATION_FILE, f"{field}.left"
        )
    if PRIMITIVE_ID_PATTERN.fullmatch(right) is None:
        raise _error(
            "CONFIG_VALUE_ERROR",
            "invalid Primitive ID",
            RELATION_FILE,
            f"{field}.right",
        )
    if left == right:
        raise _error(
            "CONFIG_VALUE_ERROR",
            "relation cannot be a self-loop",
            RELATION_FILE,
            f"{field}.right",
        )
    if relation not in RELATION_TYPES:
        raise _error(
            "CONFIG_VALUE_ERROR",
            "unknown relation type",
            RELATION_FILE,
            f"{field}.relation",
        )
    family = data.get("dynamic_family")
    if family is not None and (type(family) is not str or not family.strip()):
        raise _error(
            "CONFIG_VALUE_ERROR",
            "dynamic family must be a non-empty string",
            RELATION_FILE,
            f"{field}.dynamic_family",
        )
    if relation == "potential_tension" and family is None:
        raise _error(
            "CONFIG_GAP",
            "potential tension requires a dynamic family",
            RELATION_FILE,
            f"{field}.dynamic_family",
        )
    return PrimitiveRelation(left, right, relation, family)


def _parse_relation_graph(data: Dict[str, Any]) -> PrimitiveRelationGraphConfig:
    _validate_version(data, "relation_graph_version", "1.0", RELATION_FILE)
    for key in ("relation_graph_version", "relations"):
        if key not in data:
            raise _error("CONFIG_GAP", "required field is missing", RELATION_FILE, key)
    extra = data.keys() - {"relation_graph_version", "relations"}
    if extra:
        key = sorted(extra)[0]
        raise _error("CONFIG_VALUE_ERROR", "unknown field", RELATION_FILE, key)
    if type(data["relations"]) is not list:
        raise _error(
            "CONFIG_TYPE_ERROR", "relations must be a list", RELATION_FILE, "relations"
        )
    relations = tuple(
        _parse_relation(item, index) for index, item in enumerate(data["relations"])
    )
    seen = set()
    for index, relation in enumerate(relations):
        edge = tuple(sorted((relation.left, relation.right)))
        if edge in seen:
            raise _error(
                "CONFIG_DUPLICATE_RELATION",
                "duplicate undirected Primitive pair",
                RELATION_FILE,
                f"relations.{index}",
            )
        seen.add(edge)
    return PrimitiveRelationGraphConfig(data["relation_graph_version"], relations)


def load_runtime_config(config_dir: Path) -> RuntimeConfig:
    directory = Path(config_dir)
    bazi = _parse_bazi(_load_yaml_mapping(directory, BAZI_FILE))
    astrology = _parse_astrology(_load_yaml_mapping(directory, ASTROLOGY_FILE))
    score = _parse_score(_load_yaml_mapping(directory, SCORE_FILE))
    relation_graph = _parse_relation_graph(_load_yaml_mapping(directory, RELATION_FILE))
    return RuntimeConfig(bazi, astrology, score, relation_graph)
