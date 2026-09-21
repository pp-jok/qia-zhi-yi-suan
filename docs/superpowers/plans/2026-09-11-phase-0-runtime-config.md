# Phase 0 Runtime Configuration Implementation Plan

> Historical completed plan. The produced Python package is now classified as a
> development reference validator. Do not use this plan as the current Skill
> delivery roadmap; see `destiny_personality_skill_docs_v2_2/10_CODEX_IMPLEMENTATION_PLAN_V2_2.md`.

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a Python 3.9+ package that safely loads and strictly validates the four frozen V2.2 runtime configuration files.

**Architecture:** Keep models, error representation, loading/validation, and CLI concerns separate. Convert every accepted mutable YAML collection into frozen dataclasses and tuples; reject missing, malformed, mistyped, version-mismatched, or structurally invalid configuration before returning a `RuntimeConfig`.

**Tech Stack:** Python 3.9+, setuptools, PyYAML 6.x, pytest 8.x

## Global Constraints

- Read project data only from the caller-supplied directory under the current project scope.
- Treat `bazi-core-v1.0`, `western-tropical-v1.0`, score model `2.2`, and relation graph `1.0` as frozen versions.
- Never infer or generate missing configuration; raise `CONFIG_GAP`.
- Use `yaml.safe_load` only.
- Do not implement Phase 1 or later inference behavior.
- This directory is not a Git repository, so each task ends with a passing test checkpoint instead of a commit.

---

### Task 1: Package Bootstrap and Stable Configuration Errors

**Files:**
- Create: `pyproject.toml`
- Create: `src/destiny_personality/__init__.py`
- Create: `src/destiny_personality/config_errors.py`
- Test: `tests/test_config_errors.py`

**Interfaces:**
- Produces: `ConfigError(code, message, file=None, field=None)` with stable attributes and string rendering.
- Consumes: None.

- [ ] **Step 1: Write the failing error-contract test**

```python
# tests/test_config_errors.py
from destiny_personality.config_errors import ConfigError


def test_config_error_exposes_machine_readable_context() -> None:
    error = ConfigError(
        code="CONFIG_VALUE_ERROR",
        message="expected tropical",
        file="astrology_methodology_v1.yaml",
        field="core.zodiac",
    )

    assert error.code == "CONFIG_VALUE_ERROR"
    assert error.file == "astrology_methodology_v1.yaml"
    assert error.field == "core.zodiac"
    assert str(error) == (
        "CONFIG_VALUE_ERROR | astrology_methodology_v1.yaml | "
        "core.zodiac: expected tropical"
    )
```

- [ ] **Step 2: Run the test and verify RED**

Run:

```bash
python3 -m pytest tests/test_config_errors.py -v
```

Expected: collection fails with `ModuleNotFoundError: No module named 'destiny_personality'`.

- [ ] **Step 3: Add packaging metadata**

```toml
# pyproject.toml
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[project]
name = "destiny-personality"
version = "0.1.0"
description = "Deterministic runtime for the Destiny Personality V2.2 rules"
requires-python = ">=3.9"
dependencies = ["PyYAML>=6,<7"]

[project.optional-dependencies]
test = ["pytest>=8,<9"]

[project.scripts]
destiny-personality = "destiny_personality.cli:main"

[tool.setuptools.packages.find]
where = ["src"]

[tool.pytest.ini_options]
pythonpath = ["src"]
testpaths = ["tests"]
addopts = "-ra"
```

- [ ] **Step 4: Implement the minimal stable error type**

```python
# src/destiny_personality/config_errors.py
from typing import Optional


class ConfigError(ValueError):
    """A deterministic configuration failure exposed to callers and the CLI."""

    def __init__(
        self,
        code: str,
        message: str,
        *,
        file: Optional[str] = None,
        field: Optional[str] = None,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.file = file
        self.field = field

    def __str__(self) -> str:
        context = [self.code]
        if self.file is not None:
            context.append(self.file)
        if self.field is not None:
            context.append(self.field)
        return f"{' | '.join(context)}: {self.message}"
```

```python
# src/destiny_personality/__init__.py
from .config_errors import ConfigError

__all__ = ["ConfigError"]
```

- [ ] **Step 5: Run the focused test and verify GREEN**

Run:

```bash
python3 -m pytest tests/test_config_errors.py -v
```

Expected: `1 passed`.

---

### Task 2: Frozen Models and Strict Runtime Configuration Loader

**Files:**
- Create: `src/destiny_personality/config_models.py`
- Create: `src/destiny_personality/config_loader.py`
- Modify: `src/destiny_personality/__init__.py`
- Create: `tests/conftest.py`
- Create: `tests/test_config_loader.py`
- Create: `tests/test_config_validation.py`

**Interfaces:**
- Consumes: `ConfigError` from Task 1 and a caller-supplied `Path` containing four fixed YAML filenames.
- Produces: `load_runtime_config(config_dir: Path) -> RuntimeConfig` and frozen model types.

- [ ] **Step 1: Add a project-local valid configuration fixture**

```python
# tests/conftest.py
from pathlib import Path
import shutil

import pytest


CONFIG_FILENAMES = (
    "bazi_methodology_v1.yaml",
    "astrology_methodology_v1.yaml",
    "score_model_v2_2.yaml",
    "primitive_relation_graph_v1.yaml",
)


@pytest.fixture
def valid_config_dir(tmp_path: Path) -> Path:
    project_root = Path(__file__).resolve().parents[1]
    source = project_root / "destiny_personality_skill_docs_v2_2"
    for filename in CONFIG_FILENAMES:
        shutil.copyfile(source / filename, tmp_path / filename)
    return tmp_path
```

- [ ] **Step 2: Write the failing happy-path loader test**

```python
# tests/test_config_loader.py
from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest

from destiny_personality import load_runtime_config


def test_loads_frozen_v2_2_runtime_config(valid_config_dir: Path) -> None:
    config = load_runtime_config(valid_config_dir)

    assert config.bazi.methodology_version == "bazi-core-v1.0"
    assert config.bazi.calendar.day_boundary == "00:00"
    assert config.astrology.methodology_version == "western-tropical-v1.0"
    assert config.astrology.core.zodiac == "tropical"
    assert config.astrology.core.true_node is True
    assert config.score_model.score_model_version == "2.2"
    assert config.relation_graph.relation_graph_version == "1.0"
    assert len(config.relation_graph.relations) == 5
    with pytest.raises(FrozenInstanceError):
        config.bazi.methodology_version = "changed"
```

- [ ] **Step 3: Write failing validation tests**

```python
# tests/test_config_validation.py
from pathlib import Path

import pytest
import yaml

from destiny_personality import ConfigError, load_runtime_config


def _read_yaml(path: Path) -> dict:
    with path.open(encoding="utf-8") as stream:
        return yaml.safe_load(stream)


def _write_yaml(path: Path, data: object) -> None:
    with path.open("w", encoding="utf-8") as stream:
        yaml.safe_dump(data, stream, allow_unicode=True, sort_keys=False)


def test_missing_required_file_is_config_gap(valid_config_dir: Path) -> None:
    (valid_config_dir / "score_model_v2_2.yaml").unlink()

    with pytest.raises(ConfigError) as caught:
        load_runtime_config(valid_config_dir)

    assert caught.value.code == "CONFIG_GAP"
    assert caught.value.file == "score_model_v2_2.yaml"


def test_malformed_yaml_is_parse_error(valid_config_dir: Path) -> None:
    path = valid_config_dir / "bazi_methodology_v1.yaml"
    path.write_text("calendar: [", encoding="utf-8")

    with pytest.raises(ConfigError) as caught:
        load_runtime_config(valid_config_dir)

    assert caught.value.code == "CONFIG_PARSE_ERROR"


def test_non_mapping_root_is_type_error(valid_config_dir: Path) -> None:
    _write_yaml(valid_config_dir / "bazi_methodology_v1.yaml", [])

    with pytest.raises(ConfigError) as caught:
        load_runtime_config(valid_config_dir)

    assert caught.value.code == "CONFIG_TYPE_ERROR"
    assert caught.value.field is None


def test_wrong_frozen_version_is_version_mismatch(valid_config_dir: Path) -> None:
    path = valid_config_dir / "bazi_methodology_v1.yaml"
    data = _read_yaml(path)
    data["methodology_version"] = "bazi-core-v9.9"
    _write_yaml(path, data)

    with pytest.raises(ConfigError) as caught:
        load_runtime_config(valid_config_dir)

    assert caught.value.code == "CONFIG_VERSION_MISMATCH"
    assert caught.value.field == "methodology_version"


def test_missing_required_field_is_config_gap(valid_config_dir: Path) -> None:
    path = valid_config_dir / "score_model_v2_2.yaml"
    data = _read_yaml(path)
    del data["synthesis_priority"]["core_threshold"]
    _write_yaml(path, data)

    with pytest.raises(ConfigError) as caught:
        load_runtime_config(valid_config_dir)

    assert caught.value.code == "CONFIG_GAP"
    assert caught.value.field == "synthesis_priority.core_threshold"


def test_boolean_is_not_accepted_as_integer(valid_config_dir: Path) -> None:
    path = valid_config_dir / "score_model_v2_2.yaml"
    data = _read_yaml(path)
    data["trait_salience"]["max"] = True
    _write_yaml(path, data)

    with pytest.raises(ConfigError) as caught:
        load_runtime_config(valid_config_dir)

    assert caught.value.code == "CONFIG_TYPE_ERROR"
    assert caught.value.field == "trait_salience.max"


def test_unknown_top_level_field_is_rejected(valid_config_dir: Path) -> None:
    path = valid_config_dir / "astrology_methodology_v1.yaml"
    data = _read_yaml(path)
    data["zodaic_typo"] = "tropical"
    _write_yaml(path, data)

    with pytest.raises(ConfigError) as caught:
        load_runtime_config(valid_config_dir)

    assert caught.value.code == "CONFIG_VALUE_ERROR"
    assert caught.value.field == "zodaic_typo"


@pytest.mark.parametrize("primitive_id", ["P12", "p001", "P0001"])
def test_relation_primitive_id_format_is_enforced(
    valid_config_dir: Path, primitive_id: str
) -> None:
    path = valid_config_dir / "primitive_relation_graph_v1.yaml"
    data = _read_yaml(path)
    data["relations"][0]["left"] = primitive_id
    _write_yaml(path, data)

    with pytest.raises(ConfigError) as caught:
        load_runtime_config(valid_config_dir)

    assert caught.value.code == "CONFIG_VALUE_ERROR"
    assert caught.value.field == "relations.0.left"


def test_relation_self_loop_is_rejected(valid_config_dir: Path) -> None:
    path = valid_config_dir / "primitive_relation_graph_v1.yaml"
    data = _read_yaml(path)
    data["relations"][0]["right"] = data["relations"][0]["left"]
    _write_yaml(path, data)

    with pytest.raises(ConfigError) as caught:
        load_runtime_config(valid_config_dir)

    assert caught.value.code == "CONFIG_VALUE_ERROR"
    assert caught.value.field == "relations.0.right"


def test_tension_requires_dynamic_family(valid_config_dir: Path) -> None:
    path = valid_config_dir / "primitive_relation_graph_v1.yaml"
    data = _read_yaml(path)
    del data["relations"][0]["dynamic_family"]
    _write_yaml(path, data)

    with pytest.raises(ConfigError) as caught:
        load_runtime_config(valid_config_dir)

    assert caught.value.code == "CONFIG_GAP"
    assert caught.value.field == "relations.0.dynamic_family"


def test_duplicate_undirected_relation_is_rejected(valid_config_dir: Path) -> None:
    path = valid_config_dir / "primitive_relation_graph_v1.yaml"
    data = _read_yaml(path)
    duplicate = dict(data["relations"][0])
    duplicate["left"], duplicate["right"] = duplicate["right"], duplicate["left"]
    data["relations"].append(duplicate)
    _write_yaml(path, data)

    with pytest.raises(ConfigError) as caught:
        load_runtime_config(valid_config_dir)

    assert caught.value.code == "CONFIG_DUPLICATE_RELATION"
```

- [ ] **Step 4: Run both files and verify RED**

Run:

```bash
python3 -m pytest tests/test_config_loader.py tests/test_config_validation.py -v
```

Expected: collection fails because `load_runtime_config` does not exist.

- [ ] **Step 5: Add frozen configuration models**

```python
# src/destiny_personality/config_models.py
from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass(frozen=True)
class BaziCalendarConfig:
    input_calendar: str
    month_boundary: str
    day_boundary: str
    day_boundary_time_basis: str


@dataclass(frozen=True)
class BaziTimeConfig:
    historical_timezone_required: bool
    dst_correction_required: bool
    true_solar_time_default: bool
    allow_standard_time_mode: bool


@dataclass(frozen=True)
class BaziRelationsConfig:
    heavenly_stem_combinations: bool
    six_combinations: bool
    three_harmonies: bool
    three_meetings: bool
    six_clashes: bool
    six_harms: bool
    three_punishments: bool
    self_punishments: Tuple[str, ...]


@dataclass(frozen=True)
class PersonalityScopeConfig:
    include_luck_cycles: bool
    include_annual_transits: bool


@dataclass(frozen=True)
class BaziMethodologyConfig:
    methodology_version: str
    calendar: BaziCalendarConfig
    time: BaziTimeConfig
    month_mapping: Tuple[Tuple[str, str], ...]
    relations: BaziRelationsConfig
    personality_scope: PersonalityScopeConfig


@dataclass(frozen=True)
class AstrologyCoreConfig:
    zodiac: str
    reference: str
    house_system: str
    true_node: bool


@dataclass(frozen=True)
class AstrologyBodiesConfig:
    planets: Tuple[str, ...]
    angles: Tuple[str, ...]


@dataclass(frozen=True)
class AstrologyAspectsConfig:
    enabled: Tuple[str, ...]
    minor_aspects_enabled: bool
    max_orbs: Tuple[Tuple[str, int], ...]
    luminary_orb_bonus: int
    angle_orb: int


@dataclass(frozen=True)
class SalienceByOrbConfig:
    dominant_max: int
    strong_max: int
    moderate_max: int


@dataclass(frozen=True)
class DignityConfig:
    enabled: bool
    dignity_types: Tuple[str, ...]
    role: str


@dataclass(frozen=True)
class OuterPlanetsConfig:
    require_personal_or_angle_contact_for_high_weight: bool


@dataclass(frozen=True)
class AstrologyMethodologyConfig:
    methodology_version: str
    core: AstrologyCoreConfig
    bodies: AstrologyBodiesConfig
    aspects: AstrologyAspectsConfig
    salience_by_orb: SalienceByOrbConfig
    dignity: DignityConfig
    outer_planets: OuterPlanetsConfig


@dataclass(frozen=True)
class IntegerRange:
    minimum: int
    maximum: int


@dataclass(frozen=True)
class SynthesisPriorityConfig:
    minimum: int
    maximum: int
    core_threshold: int


@dataclass(frozen=True)
class ScoreRulesConfig:
    cross_system_validation_changes_trait_salience: bool
    tension_reduces_trait_salience: bool
    tension_can_raise_synthesis_priority: bool
    unknown_is_not_low: bool


@dataclass(frozen=True)
class ScoreModelConfig:
    score_model_version: str
    trait_salience: IntegerRange
    evidence_stability: Tuple[str, ...]
    cross_system_relation: Tuple[str, ...]
    synthesis_priority: SynthesisPriorityConfig
    rules: ScoreRulesConfig


@dataclass(frozen=True)
class PrimitiveRelation:
    left: str
    right: str
    relation: str
    dynamic_family: Optional[str]


@dataclass(frozen=True)
class PrimitiveRelationGraphConfig:
    relation_graph_version: str
    relations: Tuple[PrimitiveRelation, ...]


@dataclass(frozen=True)
class RuntimeConfig:
    bazi: BaziMethodologyConfig
    astrology: AstrologyMethodologyConfig
    score_model: ScoreModelConfig
    relation_graph: PrimitiveRelationGraphConfig
```

- [ ] **Step 6: Implement strict loading and validation**

Create `src/destiny_personality/config_loader.py` with:

```python
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
        "立春": "寅", "惊蛰": "卯", "清明": "辰", "立夏": "巳",
        "芒种": "午", "小暑": "未", "立秋": "申", "白露": "酉",
        "寒露": "戌", "立冬": "亥", "大雪": "子", "小寒": "丑",
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
            "Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter",
            "Saturn", "Uranus", "Neptune", "Pluto",
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
            "validation", "complement", "contextualization",
            "tension", "correction", "single_system",
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
        raise _error("CONFIG_PARSE_ERROR", "configuration cannot be parsed", filename) from exc
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
            raise _error("CONFIG_VALUE_ERROR", "list does not match frozen values", filename, field)
        for index, expected_item in enumerate(expected):
            _validate_exact(actual[index], expected_item, filename, _join_field(field, index))
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
    if not (salience["dominant_max"] < salience["strong_max"] < salience["moderate_max"]):
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
                "CONFIG_GAP", "required field is missing", RELATION_FILE,
                f"relations.{index}.{key}",
            )
    extra = item.keys() - {"left", "right", "relation", "dynamic_family"}
    if extra:
        key = sorted(extra)[0]
        raise _error(
            "CONFIG_VALUE_ERROR", "unknown field", RELATION_FILE,
            f"relations.{index}.{key}",
        )


def _parse_relation(data: Dict[str, Any], index: int) -> PrimitiveRelation:
    field = f"relations.{index}"
    if type(data) is not dict:
        raise _error("CONFIG_TYPE_ERROR", "relation must be a mapping", RELATION_FILE, field)
    _require_relation_keys(data, index)
    for key in ("left", "right", "relation"):
        if type(data[key]) is not str:
            raise _error(
                "CONFIG_TYPE_ERROR", "value must be a string", RELATION_FILE,
                f"{field}.{key}",
            )
    left = data["left"]
    right = data["right"]
    relation = data["relation"]
    if PRIMITIVE_ID_PATTERN.fullmatch(left) is None:
        raise _error("CONFIG_VALUE_ERROR", "invalid Primitive ID", RELATION_FILE, f"{field}.left")
    if PRIMITIVE_ID_PATTERN.fullmatch(right) is None:
        raise _error("CONFIG_VALUE_ERROR", "invalid Primitive ID", RELATION_FILE, f"{field}.right")
    if left == right:
        raise _error("CONFIG_VALUE_ERROR", "relation cannot be a self-loop", RELATION_FILE, f"{field}.right")
    if relation not in RELATION_TYPES:
        raise _error("CONFIG_VALUE_ERROR", "unknown relation type", RELATION_FILE, f"{field}.relation")
    family = data.get("dynamic_family")
    if family is not None and (type(family) is not str or not family.strip()):
        raise _error(
            "CONFIG_VALUE_ERROR", "dynamic family must be a non-empty string",
            RELATION_FILE, f"{field}.dynamic_family",
        )
    if relation == "potential_tension" and family is None:
        raise _error(
            "CONFIG_GAP", "potential tension requires a dynamic family",
            RELATION_FILE, f"{field}.dynamic_family",
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
        raise _error("CONFIG_TYPE_ERROR", "relations must be a list", RELATION_FILE, "relations")
    relations = tuple(
        _parse_relation(item, index) for index, item in enumerate(data["relations"])
    )
    seen = set()
    for index, relation in enumerate(relations):
        edge = tuple(sorted((relation.left, relation.right)))
        if edge in seen:
            raise _error(
                "CONFIG_DUPLICATE_RELATION", "duplicate undirected Primitive pair",
                RELATION_FILE, f"relations.{index}",
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
```

- [ ] **Step 7: Export the stable public API**

Replace `src/destiny_personality/__init__.py` with:

```python
from .config_errors import ConfigError
from .config_loader import load_runtime_config
from .config_models import RuntimeConfig

__all__ = ["ConfigError", "RuntimeConfig", "load_runtime_config"]
```

- [ ] **Step 8: Run loader and validation tests and verify GREEN**

Run:

```bash
python3 -m pytest tests/test_config_loader.py tests/test_config_validation.py -v
```

Expected: `14 passed`.

- [ ] **Step 9: Run all tests as the task checkpoint**

Run:

```bash
python3 -m pytest -v
```

Expected: `15 passed`, no warnings.

---

### Task 3: Validation CLI and V2.2 Integration Gate

**Files:**
- Create: `src/destiny_personality/cli.py`
- Create: `tests/test_cli.py`
- Create: `tests/test_v2_2_config_integration.py`

**Interfaces:**
- Consumes: `load_runtime_config(Path)` from Task 2.
- Produces: `main(argv: Optional[Sequence[str]] = None) -> int` and the installed `destiny-personality validate-config PATH` command.

- [ ] **Step 1: Write failing CLI behavior tests**

```python
# tests/test_cli.py
import json
from pathlib import Path

from destiny_personality.cli import main


def test_validate_config_prints_machine_readable_summary(
    valid_config_dir: Path, capsys
) -> None:
    exit_code = main(["validate-config", str(valid_config_dir)])

    output = json.loads(capsys.readouterr().out)
    assert exit_code == 0
    assert output == {
        "astrology_methodology_version": "western-tropical-v1.0",
        "bazi_methodology_version": "bazi-core-v1.0",
        "relation_count": 5,
        "relation_graph_version": "1.0",
        "score_model_version": "2.2",
        "status": "ok",
    }


def test_validate_config_reports_error_and_nonzero_exit(
    tmp_path: Path, capsys
) -> None:
    exit_code = main(["validate-config", str(tmp_path)])

    captured = capsys.readouterr()
    assert exit_code == 2
    assert captured.out == ""
    assert "CONFIG_GAP" in captured.err
    assert "bazi_methodology_v1.yaml" in captured.err
```

- [ ] **Step 2: Add a direct integration gate for the frozen project configuration**

```python
# tests/test_v2_2_config_integration.py
from pathlib import Path

from destiny_personality import load_runtime_config


def test_project_v2_2_configuration_is_loadable() -> None:
    project_root = Path(__file__).resolve().parents[1]
    config_dir = project_root / "destiny_personality_skill_docs_v2_2"

    config = load_runtime_config(config_dir)

    assert config.bazi.methodology_version == "bazi-core-v1.0"
    assert config.astrology.methodology_version == "western-tropical-v1.0"
    assert config.score_model.score_model_version == "2.2"
    assert config.relation_graph.relation_graph_version == "1.0"
    assert len(config.relation_graph.relations) == 5
```

- [ ] **Step 3: Run the new tests and verify RED**

Run:

```bash
python3 -m pytest tests/test_cli.py tests/test_v2_2_config_integration.py -v
```

Expected: collection fails because `destiny_personality.cli` does not exist.

- [ ] **Step 4: Implement the CLI**

```python
# src/destiny_personality/cli.py
import argparse
import json
from pathlib import Path
import sys
from typing import Optional, Sequence

from .config_errors import ConfigError
from .config_loader import load_runtime_config


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="destiny-personality")
    subparsers = parser.add_subparsers(dest="command", required=True)
    validate = subparsers.add_parser(
        "validate-config", help="validate a V2.2 runtime configuration directory"
    )
    validate.add_argument("path", type=Path)
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = _build_parser().parse_args(argv)
    if args.command != "validate-config":
        return 2
    try:
        config = load_runtime_config(args.path)
    except ConfigError as error:
        print(str(error), file=sys.stderr)
        return 2
    summary = {
        "status": "ok",
        "bazi_methodology_version": config.bazi.methodology_version,
        "astrology_methodology_version": config.astrology.methodology_version,
        "score_model_version": config.score_model.score_model_version,
        "relation_graph_version": config.relation_graph.relation_graph_version,
        "relation_count": len(config.relation_graph.relations),
    }
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 5: Run the focused CLI and integration tests and verify GREEN**

Run:

```bash
python3 -m pytest tests/test_cli.py tests/test_v2_2_config_integration.py -v
```

Expected: `3 passed`.

- [ ] **Step 6: Run the complete Phase 0 test suite**

Run:

```bash
python3 -m pytest -v
```

Expected: `18 passed`, no warnings.

- [ ] **Step 7: Exercise the real CLI entry path**

Run:

```bash
PYTHONPATH=src python3 -m destiny_personality.cli validate-config destiny_personality_skill_docs_v2_2
```

Expected: exit code `0` and a JSON object containing `"status": "ok"`, all four frozen versions, and `"relation_count": 5`.

---

## Final Verification

- [ ] Run `python3 -m pytest -v` and confirm 18 passing tests with no warnings.
- [ ] Run the CLI against `destiny_personality_skill_docs_v2_2` and confirm exit code 0.
- [ ] Search production code for `golden`, `calibration_expected`, network clients, and project-external absolute paths; confirm there are no matches.
- [ ] Confirm only Phase 0 files listed in this plan were created or modified.
- [ ] Confirm the four source YAML files and all V2.2 Markdown documents remain unchanged.
