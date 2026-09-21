# Phase 1 Deterministic Chart Calculation Contract Implementation Plan

> Historical completed plan. It implemented the development reference contract,
> not the final Skill runtime. Do not continue from it into a bundled calculator;
> follow the current V2.2 roadmap instead.

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement immutable birth-input and deterministic chart-fact contracts, injectable calculator protocols, and an orchestration service that enforces V2.2 time, methodology, isolation, and fatal-failure rules without implementing chart algorithms.

**Architecture:** Add a focused `calculation` subpackage. Models contain no calculation logic; Protocols define replaceable backends; `ChartCalculationService` validates inputs, calls the three backends in order, validates outputs against `RuntimeConfig`, and returns only a complete `DeterministicChartFacts` object.

**Tech Stack:** Python 3.9+, standard-library dataclasses/Decimal/Enum/Protocol, pytest 8.x

## Global Constraints

- Use only current-project data and caller-supplied in-memory facts.
- Do not implement timezone, true-solar-time, Bazi, or astrology algorithms.
- Do not use dictionaries as an escape hatch for unspecified facts.
- Never generate Primitive, Mapping, Signature, Dynamic, or Narrative output.
- Preserve all 18 Phase 0 tests.
- Unknown birth time and explicit `stable_only` must reject every time-sensitive fact.
- No partial result may escape after a fatal error.
- This project has no Git repository; passing tests are the checkpoints.

---

### Task 1: Immutable Calculation Models and Errors

**Files:**
- Create: `src/destiny_personality/calculation/__init__.py`
- Create: `src/destiny_personality/calculation/errors.py`
- Create: `src/destiny_personality/calculation/models.py`
- Test: `tests/test_birth_input_contract.py`

**Interfaces:**
- Produces: `TimeBasis`, `FactMode`, `BirthInput`, `NormalizedBirthTime`, all approved Bazi/Astrology fact dataclasses, `DeterministicChartFacts`, and `CalculationError`.
- Consumes: standard-library value types only.

- [ ] Write the failing model-contract test. It must import every public model, verify enum wire values, construct a complete aggregate, assert all collection fields are tuples, and confirm mutation raises `FrozenInstanceError`.

Use this canonical exact-time input:

```python
BirthInput(
    birth_date=date(1990, 1, 2),
    birth_time=time(3, 4, 5),
    timezone_name="Asia/Shanghai",
    latitude=Decimal("31.2304"),
    longitude=Decimal("121.4737"),
    time_basis=TimeBasis.TRUE_SOLAR_TIME,
    fact_mode=FactMode.TIME_SENSITIVE,
)
```

- [ ] Run `python3 -m pytest tests/test_birth_input_contract.py -v`.

Expected RED: `ModuleNotFoundError` for `destiny_personality.calculation`.

- [ ] Implement `CalculationError(code, message, system=None, field=None)` with stable public attributes, deterministic string rendering, and original exception chaining support.

- [ ] Implement exactly the enums and frozen dataclasses listed in the approved Phase 1 design. Use Python 3.9-compatible `Optional` and `Tuple`; add no validation or calculation behavior to `models.py`.

- [ ] Export those public types from `calculation/__init__.py`.

- [ ] Run the focused test until GREEN, then run `python3 -m pytest -v` and confirm the Phase 0 tests remain green.

---

### Task 2: Protocols, Orchestration, and Birth Input Validation

**Files:**
- Create: `src/destiny_personality/calculation/protocols.py`
- Create: `src/destiny_personality/calculation/service.py`
- Modify: `src/destiny_personality/calculation/__init__.py`
- Modify: `tests/conftest.py`
- Test: `tests/test_calculation_service.py`

**Interfaces:**
- Produces: `TimeNormalizer`, `BaziChartCalculator`, `AstrologyChartCalculator`, and `ChartCalculationService.calculate(birth_input, runtime_config)`.
- Consumes: `RuntimeConfig`, Phase 1 models, and three injected protocol implementations.

- [ ] Add `runtime_config` and canonical fact fixtures to `tests/conftest.py`. They may load only the project-local V2.2 configuration through `load_runtime_config`.

- [ ] Write a failing happy-path test with three recording fake backends. Assert call order `time → bazi → astrology`, assert each calculator receives only its own methodology, and assert the aggregate contains the exact returned objects.

- [ ] Write failing input tests for:

```text
datetime used as birth_date           -> BIRTH_INPUT_ERROR / birth_date
aware birth_time                      -> BIRTH_INPUT_ERROR / birth_time
blank timezone_name                   -> BIRTH_INPUT_ERROR / timezone_name
non-Decimal, NaN, or infinite value   -> BIRTH_INPUT_ERROR / coordinate field
latitude outside -90..90              -> BIRTH_INPUT_ERROR / latitude
longitude outside -180..180           -> BIRTH_INPUT_ERROR / longitude
unknown time with TIME_SENSITIVE      -> BIRTH_INPUT_ERROR / fact_mode
disallowed STANDARD_TIME              -> BIRTH_INPUT_ERROR / time_basis
```

- [ ] Run the focused file.

Expected RED: protocol/service imports or unimplemented validation fail.

- [ ] Implement the three Protocols with the exact approved signatures.

- [ ] Implement the service constructor, `_validate_birth_input`, and ordered backend calls. Use exact type checks so `datetime` is not accepted as `date`.

- [ ] Unexpected normalizer exceptions become `TIME_NORMALIZATION_ERROR`; unexpected calculator exceptions become `CALCULATION_FATAL` with the correct system. Existing `CalculationError` instances propagate unchanged.

- [ ] Run the focused test until GREEN, then run the complete suite.

---

### Task 3: Normalized-Time and Bazi Contract Guards

**Files:**
- Modify: `src/destiny_personality/calculation/service.py`
- Test: `tests/test_calculation_contract_validation.py`

**Interfaces:**
- Validates normalizer and Bazi outputs before astrology is called.
- Produces precise `CALCULATION_CONTRACT_ERROR` or `METHODOLOGY_VERSION_MISMATCH` errors.

- [ ] Write failing normalized-time cases for wrong object type, input metadata mismatch, illegal unknown-time values, missing known-time values, timezone-awareness errors, incompatible true-solar value, and invalid sensitivity reasons.

- [ ] Write failing Bazi cases for wrong object type, version mismatch, invalid required pillars, empty structural strings, stable-only hour leakage, time-sensitive missing hour, and invalid tuple/nested fact structures.

- [ ] In every pre-astrology failure test, assert the astrology fake was not called.

- [ ] Run the focused tests and confirm RED for missing guards.

- [ ] Implement `_validate_normalized_time`, `_validate_bazi_facts`, pillar checks, and tuple/nested checks. Do not hard-code stem, branch, Ten God, or Bazi-relation vocabularies because the project has not supplied them.

- [ ] Compare the Bazi output version only with `runtime_config.bazi.methodology_version`.

- [ ] Run the focused tests until GREEN, then run the complete suite.

---

### Task 4: Astrology Guards and Fatal Short-Circuiting

**Files:**
- Modify: `src/destiny_personality/calculation/service.py`
- Modify: `tests/test_calculation_contract_validation.py`
- Test: `tests/test_calculation_failures.py`

**Interfaces:**
- Validates `AstrologyChartFacts` against the frozen astrology configuration.
- Returns a complete aggregate only after all guards succeed.

- [ ] Write failing astrology cases for:

```text
wrong object type or methodology version
missing, duplicate, or unknown planet placement
invalid longitude, degree, sign, or house
stable_only leaking house, Asc, MC, cusp, or angle aspect
time_sensitive missing house, Asc, MC, or any of 12 cusps
invalid or duplicate house cusp
aspect self-reference, unknown body, disabled type, negative/excessive orb
angle aspect with disallowed type or excessive angle orb
unknown dignity body/type
non-tuple collection or invalid nested object
```

- [ ] Derive planetary orb limits from `max_orbs`; apply luminary bonus only for Sun/Moon. Angle aspects must pair one planet with Ascendant/MC, use only conjunction/opposition/square, and use `angle_orb` without luminary bonus.

- [ ] Write failure-order tests proving normalizer failure skips both calculators, Bazi failure skips astrology, astrology failure returns no aggregate, existing `CalculationError` propagates unchanged, and wrapped exceptions retain `__cause__`.

- [ ] Run the focused files and confirm RED for missing guards.

- [ ] Implement astrology placement, aspect, cusp, dignity, decimal-range, and stable-only validators. Construct `DeterministicChartFacts` only after they all pass.

- [ ] Run all new focused tests until GREEN.

- [ ] Run `python3 -m pytest -v`; require all Phase 0 and Phase 1 tests to pass without warnings.

- [ ] Run the Phase 0 CLI regression command:

```bash
PYTHONPATH=src python3 -m destiny_personality.cli validate-config destiny_personality_skill_docs_v2_2
```

- [ ] Scan `src/destiny_personality/calculation` for network imports, project-external absolute paths, LLM/Primitive/Mapping/Narrative logic, and concrete chart algorithms; require no matches.

---

## Final Review Checklist

- [ ] Every new behavior was observed failing before implementation.
- [ ] Input, normalized time, Bazi facts, and astrology facts are immutable and structurally validated.
- [ ] Unknown time and explicit stable-only cannot leak time-sensitive facts.
- [ ] Methodology versions come exclusively from `RuntimeConfig`.
- [ ] Calculator backends never receive one another's facts or methodology.
- [ ] Fatal failures short-circuit and never return partial output.
- [ ] Phase 0 tests and CLI remain green.
- [ ] No real calculation algorithm or external project data entered Phase 1.
