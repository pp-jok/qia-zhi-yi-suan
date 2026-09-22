# Qualified Facts Runtime Hardening Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `executing-plans` task-by-task. Steps use checkbox syntax for tracking.

**Goal:** make `deterministic-facts-v1` the only public Core Profile input, derive assurance from its validation evidence, and close the remaining context-scope and contract drift defects.

**Architecture:** The existing chart-facts dataclasses remain the internal semantic transport. A new qualified packet decoder validates the formal envelope, returns facts with `project_verified` assurance, and is the sole path used by the public CLI. Presentation decodes compound context scopes at the boundary without changing the candidate IR schema.

**Tech Stack:** Python 3.9+, dataclasses, JSON, PyYAML, pytest, GitHub Actions.

## Global Constraints

- Freeze P001–P006, mappings, resolver, alignment, calibration, holdout, and all production-disabled layers.
- The public CLI must never accept caller-selected fact assurance.
- `deterministic-facts-v1` must fail closed without provenance, passed validation evidence, matching methodologies, and valid fact scope.
- Preserve `build_candidate_core_profile(..., fact_assurance=...)` only as an internal/test seam; do not expose it through the CLI.
- No chart calculation, provider validation, or new personality semantics.

---

### Task 1: Qualified facts envelope

**Files:**
- Modify: `src/destiny_personality/deterministic_facts_codec.py`
- Modify: `src/destiny_personality/cli.py`
- Test: `tests/test_cli.py`

**Interfaces:**
- Produces `load_validated_deterministic_facts(path: Path) -> DeterministicChartFacts`.
- `build-core-profile FACTS --output PROFILE` uses this loader and always passes derived `project_verified` assurance.

- [ ] Write tests for missing qualification, failed validation, mismatched methodology, and a valid `deterministic-facts-v1` packet.
- [ ] Confirm the old CLI form with `--fact-assurance` is rejected by argument parsing.
- [ ] Implement formal-envelope validation: non-empty provenance, five passed validation fields plus independent comparison, envelope/model methodology equality, and `fact_mode` equality.
- [ ] Replace the public CLI argument with the validated loader.
- [ ] Run `pytest -q tests/test_cli.py`.

### Task 2: Fact scope and context-scope correctness

**Files:**
- Modify: `src/destiny_personality/core_profile_builder.py`
- Modify: `src/destiny_personality/core_profile_validation.py`
- Modify: `src/destiny_personality/core_portrait.py`
- Test: `tests/test_core_profile_builder.py`
- Test: `tests/test_context_scope_presentation.py`

**Interfaces:**
- `parse_context_scope(scope: str) -> Tuple[str, ...]` is used only by presentation localization.
- `CandidateFactScope.bazi_hour_available` reflects the supplied pillar, independent of known birth time.

- [ ] Write a failing known-time/no-hour-pillar test and a failing compound-scope rendering test.
- [ ] Implement exact fact-scope semantics: stable-only plus hour data fails; time-sensitive without hour data is valid.
- [ ] Implement compound-scope splitting and localized labels without raw scope leakage.
- [ ] Run the two focused test modules.

### Task 3: Presentation and schema contracts

**Files:**
- Modify: `destiny-personality/schemas/candidate-profile-summary.md`
- Modify: `destiny-personality/schemas/birth-input.md`
- Modify: `destiny-personality/SKILL.md`
- Test: `tests/test_primitive_presentation_directions.py`
- Test: `tests/test_skill_package.py`

**Interfaces:**
- Summary documents `resolved_direction` and `context_directions` as presentation routing only.
- Birth input accepts `portrait`, `legacy`, `core`, `core_concise`, `core_standard`, `facts_only`, and `audit`; portrait aliases legacy.

- [ ] Write a failing 6×2 high/low rendering matrix and user-output guard test.
- [ ] Document the summary fields and context-direction provenance.
- [ ] Synchronize skill route with qualified facts → profile → render; remove orphan text and state the assurance boundary.
- [ ] Run presentation and skill tests.

### Task 4: Release gate

**Files:**
- Modify: `release/qia-zhi-yi-suan/pyproject.toml`
- Modify: `release/qia-zhi-yi-suan/README.md`
- Create: `docs/domain/qualified-facts-runtime-hardening-v0.3.7.md`

- [ ] Run full pytest and package verifier.
- [ ] Publish `v0.3.7-qualified-facts-runtime-hardening` as a prerelease, preserving v0.3.6 as its frozen baseline.
- [ ] Install and verify the release archive, confirm CI and that generated egg-info is absent from the remote tree.
