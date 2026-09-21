# Phase 1.1 Calculation Contract Hardening Implementation Plan

> Historical completed plan. Its tests and validators remain development assets;
> they are not required contents of the distributable Skill. Follow the current
> V2.2 roadmap for all subsequent work.

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add mechanically validated Bazi pillar provenance, close `stable_only` hour-source leakage, characterize existing astrology guards, split validation from orchestration, and provide an isolated package-install smoke command.

**Architecture:** Keep immutable contracts in `models.py` and orchestration in `service.py`. Move pure contract checks into four domain validators plus a small shared helper module; do not add a framework or public validator API. Package verification remains an explicit release command because its isolated PEP 517 build may need network access.

**Tech Stack:** Python 3.9+, standard-library dataclasses/Decimal/Enum/Protocol/subprocess/tempfile/venv, PyYAML 6.x, pytest 8.x

## Global Constraints

- Read and modify only the current project; do not read other project business files.
- Do not implement timezone, true-solar-time, Bazi, or astrology algorithms.
- Do not add Primitive, Mapping, Signature, Dynamic, Narrative, or LLM behavior.
- Do not infer Bazi semantics from `subject_ref` or `participant_refs` strings.
- Keep `ChartCalculationService.calculate(...)`, backend order, exception conversion, short-circuiting, and aggregate output stable.
- Use `CALCULATION_CONTRACT_ERROR` for all new backend-contract violations.
- Preserve Python 3.9 compatibility and add no runtime dependency.
- This directory is not a Git repository; focused and full verification runs are the implementation checkpoints.

## File Map

```text
src/destiny_personality/calculation/
├── __init__.py                 export PillarPosition
├── models.py                   define provenance contracts
├── service.py                  retain orchestration only
└── validation/
    ├── __init__.py             package marker
    ├── common.py               shared primitive guards/errors
    ├── input.py                BirthInput validation
    ├── time.py                 NormalizedBirthTime validation
    ├── bazi.py                 Bazi facts/provenance validation
    └── astrology.py            astrology facts validation
tests/
├── conftest.py                 canonical facts after contract change
├── test_birth_input_contract.py public model construction
├── test_bazi_provenance.py      new provenance behavior
└── test_astrology_guard_coverage.py missing guard evidence
scripts/
└── verify_package.py            explicit wheel/install/CLI smoke
```

---

### Task 1: Add Bazi Pillar Provenance and Enforce Stable-Only Boundaries

**Files:**
- Create: `tests/test_bazi_provenance.py`
- Modify: `tests/test_birth_input_contract.py`
- Modify: `tests/conftest.py`
- Modify: `src/destiny_personality/calculation/models.py`
- Modify: `src/destiny_personality/calculation/__init__.py`
- Modify: `src/destiny_personality/calculation/service.py`

**Interfaces:**
- Produces: `PillarPosition`, `HiddenStemsFact.pillar: PillarPosition`, `TenGodFact.source_pillars`, and `BaziRelationFact.source_pillars`.
- Consumes: existing `FactMode`, `CalculationError`, `ChartCalculationService`, and runtime config fixtures.

- [ ] **Step 1: Write the failing public-contract test**

Add imports and assertions that define the exact public API:

```python
from destiny_personality.calculation import (
    BaziRelationFact,
    HiddenStemsFact,
    PillarPosition,
    TenGodFact,
)


def test_bazi_provenance_models_are_public_and_immutable() -> None:
    assert [position.value for position in PillarPosition] == [
        "year", "month", "day", "hour"
    ]
    hidden = HiddenStemsFact(PillarPosition.YEAR, ("庚",))
    ten_god = TenGodFact("year.stem", "peer", (PillarPosition.YEAR, PillarPosition.DAY))
    relation = BaziRelationFact(
        "clash",
        ("year.branch", "hour.branch"),
        (PillarPosition.YEAR, PillarPosition.HOUR),
    )

    assert hidden.pillar is PillarPosition.YEAR
    assert ten_god.source_pillars == (PillarPosition.YEAR, PillarPosition.DAY)
    assert relation.source_pillars[-1] is PillarPosition.HOUR
```

- [ ] **Step 2: Run the public-contract test and verify RED**

Run:

```bash
python3 -m pytest tests/test_birth_input_contract.py -v
```

Expected: collection fails because `PillarPosition` and the new constructor fields do not exist.

- [ ] **Step 3: Implement the minimal immutable model change**

Add to `models.py`:

```python
class PillarPosition(str, Enum):
    YEAR = "year"
    MONTH = "month"
    DAY = "day"
    HOUR = "hour"


@dataclass(frozen=True)
class HiddenStemsFact:
    pillar: PillarPosition
    stems: Tuple[str, ...]


@dataclass(frozen=True)
class TenGodFact:
    subject_ref: str
    ten_god: str
    source_pillars: Tuple[PillarPosition, ...]


@dataclass(frozen=True)
class BaziRelationFact:
    relation_type: str
    participant_refs: Tuple[str, ...]
    source_pillars: Tuple[PillarPosition, ...]
```

Export `PillarPosition` through `calculation.__init__.__all__`. Update every project-local construction of these dataclasses to pass typed provenance; do not add default values that allow provenance to be omitted.

- [ ] **Step 4: Run the public-contract test until GREEN**

Run:

```bash
python3 -m pytest tests/test_birth_input_contract.py -v
```

Expected: all model-contract tests pass.

- [ ] **Step 5: Write failing provenance-validation tests**

In `test_bazi_provenance.py`, call the public service with fixed backends and parameterize these exact invalid outputs and expected field paths:

```python
INVALID_PROVENANCE_CASES = (
    (
        HiddenStemsFact("year", ("庚",)),
        None,
        None,
        "hidden_stems.0.pillar",
    ),
    (
        None,
        TenGodFact("year.stem", "peer", ()),
        None,
        "ten_gods.0.source_pillars",
    ),
    (
        None,
        TenGodFact("year.stem", "peer", (PillarPosition.YEAR, PillarPosition.YEAR)),
        None,
        "ten_gods.0.source_pillars.1",
    ),
    (
        None,
        None,
        BaziRelationFact("clash", ("year.branch", "day.branch"), ("year",)),
        "relations.0.source_pillars.0",
    ),
)
```

For each case, replace only the matching Bazi collection, assert:

```python
assert caught.value.code == "CALCULATION_CONTRACT_ERROR"
assert caught.value.system == "bazi"
assert caught.value.field == expected_field
assert calls == ["time", "bazi"]
```

Add three `STABLE_ONLY` cases using:

```python
HiddenStemsFact(PillarPosition.HOUR, ("庚",))
TenGodFact("hour.stem", "peer", (PillarPosition.HOUR, PillarPosition.DAY))
BaziRelationFact(
    "clash",
    ("year.branch", "hour.branch"),
    (PillarPosition.YEAR, PillarPosition.HOUR),
)
```

Assert exact fields `hidden_stems.0.pillar`, `ten_gods.0.source_pillars.0`, and `relations.0.source_pillars.1`. Add one `TIME_SENSITIVE` happy path containing all three hour-sourced facts and assert the returned `bazi` object is identical.

- [ ] **Step 6: Run the provenance tests and verify RED**

Run:

```bash
python3 -m pytest tests/test_bazi_provenance.py -v
```

Expected: invalid or stable-only hour provenance is accepted by the existing validator.

- [ ] **Step 7: Add the minimal provenance guards to the existing Bazi validator**

Use this exact helper behavior before the later module split:

```python
def _validate_source_pillars(
    value: object, field: str, fact_mode: FactMode
) -> None:
    if type(value) is not tuple or not value:
        raise _contract_error(
            "bazi", "source pillars must be a non-empty tuple", field
        )
    seen = set()
    for index, position in enumerate(value):
        item_field = f"{field}.{index}"
        if type(position) is not PillarPosition:
            raise _contract_error(
                "bazi", "source pillar must be a PillarPosition", item_field
            )
        if position in seen:
            raise _contract_error("bazi", "duplicate source pillar", item_field)
        if fact_mode is FactMode.STABLE_ONLY and position is PillarPosition.HOUR:
            raise _contract_error(
                "bazi", "stable-only facts cannot use an hour source", item_field
            )
        seen.add(position)
```

Validate `HiddenStemsFact.pillar` with an exact type check; reject `HOUR` in stable-only mode. Call `_validate_source_pillars` for every Ten God and relation fact after their existing string checks.

- [ ] **Step 8: Run focused and full tests until GREEN**

Run:

```bash
python3 -m pytest tests/test_birth_input_contract.py tests/test_bazi_provenance.py tests/test_calculation_contract_validation.py -v
python3 -m pytest -v
```

Expected: all tests pass without warnings.

---

### Task 2: Characterize Existing Astrology Contract Guards

**Files:**
- Create: `tests/test_astrology_guard_coverage.py`
- No permanent production-code change in this task.

**Interfaces:**
- Consumes: public `ChartCalculationService` behavior and existing canonical fixtures.
- Produces: regression evidence for every astrology guard listed in the Phase 1.1 design.

- [ ] **Step 1: Add public-path guard tests**

Use fixed normalizer/Bazi/astrology backends and `dataclasses.replace`. Cover this exact matrix:

```text
placements.1.body          duplicate configured planet
aspects.1                  reversed duplicate of the same typed aspect
dignities.1                duplicate body/dignity pair
house_cusps.0.house        integer 0
house_cusps.1.house        duplicate house 1
house_cusps.0.longitude    Decimal("360")
house_cusps                only houses 1..11
aspects.0                  Ascendant paired with MC
aspects.0.aspect_type      Ascendant trine planet
aspects.0.orb              planet/Ascendant orb above angle_orb
placements                 list instead of tuple
aspects.0                  object() instead of AstrologyAspectFact
house_cusps.0              object() instead of HouseCusp
dignities.0                object() instead of DignityFact
```

For each case, assert `CALCULATION_CONTRACT_ERROR`, `system == "astrology"`, the exact field above, and calls equal `['time', 'bazi', 'astrology']`.

Construct the three angle-aspect inputs exactly as follows so their failure reason is unambiguous:

```python
AstrologyAspectFact("Ascendant", "MC", "square", Decimal("1"))
AstrologyAspectFact("Sun", "Ascendant", "trine", Decimal("1"))
AstrologyAspectFact(
    "Sun",
    "Ascendant",
    "conjunction",
    Decimal(runtime_config.astrology.aspects.angle_orb) + Decimal("0.1"),
)
```

- [ ] **Step 2: Run the new tests and record the baseline GREEN**

Run:

```bash
python3 -m pytest tests/test_astrology_guard_coverage.py -v
```

Expected: tests pass because the guards already exist; this establishes behavior before refactoring, not TDD evidence for a new feature.

- [ ] **Step 3: Prove the characterization tests detect regression**

Temporarily remove one guard at a time from the current `service.py` for these four groups, run only its matching node IDs, observe the expected assertion failure, then immediately restore the guard with `apply_patch` before moving to the next group:

```text
duplicate set membership guard: placement/aspect/dignity duplicate tests fail
cusp range/completeness guard: cusp boundary tests fail
angle_count branch: angle pairing/type/orb tests fail
collection item type loop: nested-object tests fail
```

Do not retain any experimental deletion. If a test remains green with its target guard removed, strengthen the test before continuing.

- [ ] **Step 4: Re-run the characterization file after all guards are restored**

Run:

```bash
python3 -m pytest tests/test_astrology_guard_coverage.py -v
```

Expected: all tests pass.

---

### Task 3: Split Pure Validation from Orchestration

**Files:**
- Create: `src/destiny_personality/calculation/validation/__init__.py`
- Create: `src/destiny_personality/calculation/validation/common.py`
- Create: `src/destiny_personality/calculation/validation/input.py`
- Create: `src/destiny_personality/calculation/validation/time.py`
- Create: `src/destiny_personality/calculation/validation/bazi.py`
- Create: `src/destiny_personality/calculation/validation/astrology.py`
- Modify: `src/destiny_personality/calculation/service.py`

**Interfaces:**
- Produces internal functions `validate_birth_input`, `validate_normalized_time`, `validate_bazi_facts`, and `validate_astrology_facts`.
- Consumes existing models, `RuntimeConfig`, and `CalculationError`; public exports remain unchanged.

- [ ] **Step 1: Verify the complete behavioral safety net before moving code**

Run:

```bash
python3 -m pytest tests/test_calculation_service.py tests/test_calculation_contract_validation.py tests/test_calculation_failures.py tests/test_bazi_provenance.py tests/test_astrology_guard_coverage.py -v
```

Expected: all focused contract tests pass.

- [ ] **Step 2: Create shared primitive guards**

`validation/common.py` must contain only these reusable functions with existing error wording preserved at call sites:

```python
def input_error(
    message: str, field: Optional[str] = None
) -> CalculationError:
    return CalculationError("BIRTH_INPUT_ERROR", message, field=field)

def contract_error(
    system: str, message: str, field: Optional[str] = None
) -> CalculationError:
    return CalculationError(
        "CALCULATION_CONTRACT_ERROR", message, system=system, field=field
    )

def validate_nonempty_string(
    value: object, system: str, field: str
) -> None:
    if type(value) is not str or not value.strip():
        raise contract_error(system, "value must be a non-empty string", field)

def validate_decimal_range(
    value: object,
    minimum: Decimal,
    maximum: Decimal,
    system: str,
    field: str,
) -> None:
    if type(value) is not Decimal or not value.is_finite():
        raise contract_error(system, "value must be a finite Decimal", field)
    if not minimum <= value < maximum:
        raise contract_error(
            system, f"value must be in [{minimum}, {maximum})", field
        )
```

`validate_decimal_range` requires an exact finite `Decimal` and enforces the half-open interval `[minimum, maximum)`.

- [ ] **Step 3: Move each domain validator without behavior changes**

Use these exact module-level signatures:

- `validation/input.py`: `validate_birth_input(birth_input: BirthInput, config: RuntimeConfig) -> None`
- `validation/time.py`: `validate_normalized_time(birth_input: BirthInput, normalized_time: NormalizedBirthTime) -> None`
- `validation/bazi.py`: `validate_bazi_facts(facts: BaziChartFacts, fact_mode: FactMode, config: RuntimeConfig) -> None`
- `validation/astrology.py`: `validate_astrology_facts(facts: AstrologyChartFacts, fact_mode: FactMode, config: RuntimeConfig) -> None`

Move all private helpers next to their sole caller. Keep only the nonempty-string, decimal-range, input-error, and contract-error primitives in `common.py`. Do not export validators from `calculation.__init__`.

- [ ] **Step 4: Reduce `service.py` to orchestration**

Import the four functions and replace static-method calls:

```python
from .validation.astrology import validate_astrology_facts
from .validation.bazi import validate_bazi_facts
from .validation.input import validate_birth_input
from .validation.time import validate_normalized_time


class ChartCalculationService:
    def __init__(
        self,
        time_normalizer: TimeNormalizer,
        bazi_calculator: BaziChartCalculator,
        astrology_calculator: AstrologyChartCalculator,
    ) -> None:
        self._time_normalizer = time_normalizer
        self._bazi_calculator = bazi_calculator
        self._astrology_calculator = astrology_calculator

    def calculate(
        self, birth_input: BirthInput, config: RuntimeConfig
    ) -> DeterministicChartFacts:
        validate_birth_input(birth_input, config)
        try:
            normalized_time = self._time_normalizer.normalize(birth_input, config)
        except CalculationError:
            raise
        except Exception as error:
            raise CalculationError(
                "TIME_NORMALIZATION_ERROR",
                "birth time normalization failed",
                system="time",
            ) from error
        validate_normalized_time(birth_input, normalized_time)

        try:
            bazi = self._bazi_calculator.calculate(
                birth_input, normalized_time, config.bazi
            )
        except CalculationError:
            raise
        except Exception as error:
            raise CalculationError(
                "CALCULATION_FATAL", "Bazi calculation failed", system="bazi"
            ) from error
        validate_bazi_facts(bazi, normalized_time.fact_mode, config)

        try:
            astrology = self._astrology_calculator.calculate(
                birth_input, normalized_time, config.astrology
            )
        except CalculationError:
            raise
        except Exception as error:
            raise CalculationError(
                "CALCULATION_FATAL",
                "astrology calculation failed",
                system="astrology",
            ) from error
        validate_astrology_facts(astrology, normalized_time.fact_mode, config)

        return DeterministicChartFacts(normalized_time, bazi, astrology)
```

The finished file must contain no field-level validation logic.

- [ ] **Step 5: Run focused tests immediately after the refactor**

Run:

```bash
python3 -m pytest tests/test_calculation_service.py tests/test_calculation_contract_validation.py tests/test_calculation_failures.py tests/test_bazi_provenance.py tests/test_astrology_guard_coverage.py -v
```

Expected: all tests pass with identical error codes, systems, fields, and call order.

- [ ] **Step 6: Run the full regression suite**

Run:

```bash
python3 -m pytest -v
```

Expected: all Phase 0, Phase 1, and Phase 1.1 tests pass without warnings.

---

### Task 4: Add an Explicit Isolated Package Verification Command

**Files:**
- Create: `scripts/verify_package.py`

**Interfaces:**
- Produces: `python3 scripts/verify_package.py` release verification command.
- Consumes: current Python interpreter, pip, venv, project `pyproject.toml`, and project-local V2.2 configuration directory.

- [ ] **Step 1: Verify RED before creating the script**

Run:

```bash
python3 scripts/verify_package.py
```

Expected: exit nonzero because the script does not exist.

- [ ] **Step 2: Implement the complete smoke script**

Create this direct standard-library implementation:

```python
from pathlib import Path
import os
import subprocess
import sys
import tempfile


def run(command, *, cwd=None) -> None:
    subprocess.run([str(part) for part in command], cwd=cwd, check=True)


def main() -> int:
    project_root = Path(__file__).resolve().parents[1]
    config_dir = project_root / "destiny_personality_skill_docs_v2_2"

    with tempfile.TemporaryDirectory(prefix="destiny-personality-package-") as raw:
        workspace = Path(raw)
        wheelhouse = workspace / "wheelhouse"
        wheelhouse.mkdir()

        run(
            [
                sys.executable,
                "-m",
                "pip",
                "wheel",
                ".",
                "--wheel-dir",
                wheelhouse,
            ],
            cwd=project_root,
        )
        project_wheels = tuple(wheelhouse.glob("destiny_personality-*.whl"))
        if len(project_wheels) != 1:
            raise RuntimeError(
                f"expected one project wheel, found {len(project_wheels)}"
            )

        venv_dir = workspace / "venv"
        run([sys.executable, "-m", "venv", venv_dir])
        bin_dir = venv_dir / ("Scripts" if os.name == "nt" else "bin")
        python = bin_dir / ("python.exe" if os.name == "nt" else "python")
        cli = bin_dir / (
            "destiny-personality.exe" if os.name == "nt" else "destiny-personality"
        )

        run(
            [
                python,
                "-m",
                "pip",
                "install",
                "--no-index",
                "--find-links",
                wheelhouse,
                project_wheels[0],
            ]
        )
        run(
            [
                python,
                "-c",
                "from destiny_personality.calculation import "
                "BirthInput, ChartCalculationService, PillarPosition",
            ]
        )
        run([cli, "validate-config", config_dir])

    print("package verification passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 3: Run the package verification with explicit network authority if needed**

Run:

```bash
python3 scripts/verify_package.py
```

Expected: a project wheel and dependency wheels are built only in a temporary directory; a fresh venv imports `PillarPosition`; installed CLI prints `configuration valid`; script ends with `package verification passed` and exit code 0.

If PEP 517 cannot fetch `setuptools>=68` or pip cannot fetch PyYAML because network is restricted, request user approval for this exact release verification rather than changing build requirements or using global installation.

---

### Task 5: Final Scope and Regression Verification

**Files:**
- Verify only; no planned source changes.

**Interfaces:**
- Confirms the Phase 1.1 acceptance criteria and project-boundary rules.

- [ ] **Step 1: Run all automated tests freshly**

Run:

```bash
python3 -m pytest -v
```

Expected: zero failures and no warnings.

- [ ] **Step 2: Run the source-mode CLI regression**

Run:

```bash
PYTHONPATH=src python3 -m destiny_personality.cli validate-config destiny_personality_skill_docs_v2_2
```

Expected: `configuration valid` and exit code 0.

- [ ] **Step 3: Run the explicit package smoke freshly**

Run:

```bash
python3 scripts/verify_package.py
```

Expected: `package verification passed` and exit code 0.

- [ ] **Step 4: Scan the changed runtime scope**

Run:

```bash
rg -n "requests|urllib|httpx|aiohttp|openai|anthropic|Primitive|Mapping|Signature|Dynamic|Narrative|/Users/" src/destiny_personality/calculation scripts/verify_package.py
```

Expected: no matches. The script may refer to its project root only through `Path(__file__)`, never through a hard-coded absolute path.

- [ ] **Step 5: Confirm orchestration remains small and validators are isolated**

Run:

```bash
wc -l src/destiny_personality/calculation/service.py
rg -n "validate_birth_input|validate_normalized_time|validate_bazi_facts|validate_astrology_facts" src/destiny_personality/calculation/service.py
```

Expected: `service.py` contains the four validator imports/calls and orchestration only; no field-level validation helpers remain.

## Final Review Checklist

- [ ] Every new provenance behavior was observed RED before implementation and GREEN afterward.
- [ ] Characterization tests were proven by temporary guard-removal experiments, with every guard restored.
- [ ] Every Bazi derived fact has typed declared pillar provenance.
- [ ] `STABLE_ONLY` rejects all declared hour provenance with precise field paths.
- [ ] `TIME_SENSITIVE` accepts valid hour provenance.
- [ ] `service.py` contains orchestration only and exposes no new public validator API.
- [ ] Existing error codes, call order, short-circuit behavior, and complete-only aggregate remain stable.
- [ ] Full pytest, source CLI, isolated wheel install, and installed CLI all pass freshly.
- [ ] No real chart algorithm, inference rule, external business data, network client, or hard-coded external path was introduced.
