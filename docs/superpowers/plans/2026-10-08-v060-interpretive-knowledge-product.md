# v0.6.0 Interpretive Knowledge Product Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `subagent-driven-development` to implement task-by-task. Steps use checkbox (`- [ ]`) syntax.

**Goal:** Turn v0.5.0's auditable report engine into a differentiated, internal-test-ready Bazi × astrology personality product.

**Architecture:** Replace demo-shaped rules with validated, reusable product rule families; derive independent Bazi and astrology profiles; synthesize concrete alignments/tensions; render only evidence-backed reader analysis while retaining audit data separately. Strict remains frozen.

**Tech Stack:** Python 3.9+, dataclasses, PyYAML, pytest, existing qualified-facts and CLI contracts.

## Global Constraints

- Preserve strict/candidate/primitive/semantic-bridge behavior and tests.
- Rule families use only qualified deterministic facts and versioned local assets.
- Reader sections never contain audit-padding or unsupported claims.
- Missing time removes house/angle claims and visibly explains the scope.
- Normal birth-input flow uses a calculation provider when available, otherwise returns `CAPABILITY_GAP` without free-form calculation.
- Release v0.6.0 requires 12+ differentiated fixtures, 5 reader demos, traceability, strict regression, package verification, and CI readiness.

### Task 1: Rule-family contract and knowledge-asset replacement

**Files:**
- Modify: `src/destiny_personality/interpretive_models.py`, `interpretive_rules.py`
- Replace: `src/destiny_personality/interpretive_assets/v1/interpretive_rules_v1.yaml`
- Test: `tests/test_interpretive_rules.py`

- [ ] **Step 1: Write failing contract and anti-demo tests**

```python
def test_v060_rule_families_cover_all_ten_gods_and_core_planets():
    bundle = load_interpretive_rule_bundle()
    assert TEN_GODS <= bundle.covered_ten_gods
    assert CORE_PLANETS <= bundle.covered_planets

def test_no_rule_requires_a_demo_specific_full_configuration():
    assert all(not rule.requires_exact_demo_chart for rule in load_interpretive_rule_bundle().rules)
```

- [ ] **Step 2: Run RED**

Run: `python3 -m pytest tests/test_interpretive_rules.py -q`
Expected: FAIL because family metadata/coverage does not exist.

- [ ] **Step 3: Implement minimal v2 rule-family selectors**

Add bounded predicates for ten-god position/source/repetition, branch relations,
planet sign quality, house context, major aspects, and dignity. Add Chinese
mechanism/likely-expression/context fields and validate every declared selector.

- [ ] **Step 4: Run GREEN and commit**

Run: `python3 -m pytest tests/test_interpretive_rules.py -q`
Expected: PASS.

```bash
git add src/destiny_personality/interpretive_* tests/test_interpretive_rules.py
git commit -m "feat: expand interpretive rule families"
```

### Task 2: System profiles and cross-system synthesis packet

**Files:**
- Create: `src/destiny_personality/interpretive_system_profiles.py`, `interpretive_synthesis.py`
- Modify: `interpretive_models.py`, `interpretive_profile.py`, `interpretive_codec.py`
- Test: `tests/test_interpretive_system_profiles.py`, `tests/test_interpretive_synthesis.py`

- [ ] **Step 1: Write failing tests**

```python
def test_system_profiles_are_independent_and_topic_bound(qualified_facts):
    packet = build_narrative_synthesis_packet(qualified_facts)
    assert packet.bazi_profile.signal_ids
    assert packet.astrology_profile.signal_ids
    assert packet.alignments

def test_tension_explains_poles_context_and_integration(tension_facts):
    tension = build_narrative_synthesis_packet(tension_facts).tensions[0]
    assert tension.left_pole and tension.right_pole and tension.integration
```

- [ ] **Step 2: Run RED**

Run: `python3 -m pytest tests/test_interpretive_system_profiles.py tests/test_interpretive_synthesis.py -q`
Expected: FAIL because modules are absent.

- [ ] **Step 3: Implement independently-derived profiles and bounded synthesis**

Use only matched signals. Emit structured relationship kinds: validation,
complement, contextualization, tension, correction, unresolved, non_comparable.
Preserve provenance and prohibit unsupported cross-system agreement.

- [ ] **Step 4: Run GREEN and commit**

```bash
git add src/destiny_personality/interpretive_* tests/test_interpretive_system_profiles.py tests/test_interpretive_synthesis.py
git commit -m "feat: synthesize system-specific interpretive profiles"
```

### Task 3: Reader-first report and controlled narrative packet

**Files:**
- Modify: `interpretive_report.py`, `interpretive_codec.py`, `cli.py`
- Test: `tests/test_interpretive_report.py`, `tests/test_interpretive_cli.py`

- [ ] **Step 1: Write failing reader-body tests**

```python
def test_sparse_report_stays_short_without_audit_sections(sparse_facts):
    report = build_interpretive_report(sparse_facts, "standard")
    assert 3 <= len(report.sections) <= 4
    assert all(section.kind == "analysis" for section in report.sections)

def test_rich_report_has_multiple_deep_reader_topics(rich_facts):
    assert len(build_interpretive_report(rich_facts, "standard").sections) >= 6
```

- [ ] **Step 2: Run RED**

Run: `python3 -m pytest tests/test_interpretive_report.py -q`
Expected: FAIL because current report pads audit sections.

- [ ] **Step 3: Render conclusion-first Chinese narrative**

Each section includes conclusion, mechanism, likely expression, contextual
variation, and maturity/imbalance only when supplied signals support it. Move
audit data to metadata/appendix; render confidence naturally once per claim.

- [ ] **Step 4: Run GREEN and commit**

```bash
git add src/destiny_personality/interpretive_report.py src/destiny_personality/interpretive_codec.py src/destiny_personality/cli.py tests/test_interpretive_report.py tests/test_interpretive_cli.py
git commit -m "feat: render reader-first interpretive reports"
```

### Task 4: Product fixtures, differentiation matrix, and demos

**Files:**
- Create: `tests/fixtures/interpretive/v060/`, `docs/demos/v0.6.0/`
- Create: `docs/interpretive-rule-coverage.md`, `docs/product-differentiation-review.md`
- Test: `tests/test_interpretive_product_quality.py`

- [ ] **Step 1: Write failing product-quality tests**

```python
def test_normal_chart_has_multiple_real_topics(product_fixture):
    assert len(reader_topics(product_fixture)) >= 6

def test_reports_are_reader_semantically_distinct(product_fixtures):
    assert len({core_reader_text(item) for item in product_fixtures}) == len(product_fixtures)
```

- [ ] **Step 2: Run RED**

Run: `python3 -m pytest tests/test_interpretive_product_quality.py -q`
Expected: FAIL before 12-fixture matrix and reader demos exist.

- [ ] **Step 3: Add 12+ qualified facts fixtures and 5 pipeline-generated reader demos**

Cover Bazi/astrology emphasis, agreement, tension, rich/sparse and missing-time.
Generate all demos through the official CLI; write a topic × system coverage
matrix and template-collapse review from actual reports.

- [ ] **Step 4: Run GREEN and commit**

```bash
git add tests/fixtures/interpretive/v060 tests/test_interpretive_product_quality.py docs/demos/v0.6.0 docs/interpretive-rule-coverage.md docs/product-differentiation-review.md
git commit -m "test: add v060 product differentiation gates"
```

### Task 5: Birth-input product workflow and release readiness

**Files:**
- Modify: `destiny-personality/SKILL.md`, `README.md`, `CHANGELOG.md`, `pyproject.toml`
- Create: `docs/v0.6.0-product-readiness.md`, `docs/release/v0.6.0-release-notes.md`
- Test: `tests/test_skill_package.py`, `tests/test_interpretive_product_flow.py`

- [ ] **Step 1: Write failing workflow tests**

```python
def test_birth_input_uses_provider_or_returns_capability_gap():
    assert "CAPABILITY_GAP" in skill_product_flow()

def test_v060_readiness_machine_summary_is_complete():
    assert load_readiness_summary()["release_ready"] is True
```

- [ ] **Step 2: Run RED**

Run: `python3 -m pytest tests/test_interpretive_product_flow.py tests/test_skill_package.py -q`
Expected: FAIL because v0.6 workflow/readiness contracts are absent.

- [ ] **Step 3: Document provider boundary and v0.6 release contract**

Normal users supply birth information only. The Skill invokes an available
provider/qualification capability or returns `CAPABILITY_GAP`; facts JSON stays
an internal interface. Bump version to 0.6.0 and retain all v0.5 strict routes.

- [ ] **Step 4: Verify and commit**

Run: `python3 -m pytest -p no:terminal -o addopts=`
Expected: PASS.

Run: `python3 -m build --wheel`
Expected: PASS; wheel includes interpretive assets.

```bash
git add destiny-personality README.md CHANGELOG.md pyproject.toml docs tests
git commit -m "docs: prepare v060 internal test product release"
```

## Final Review

- [ ] Reader body contains only supported analytic content.
- [ ] Normal complete fixtures have six or more real topics; sparse fixtures remain short.
- [ ] All final conclusions/sections map to matched signal fact/rule provenance.
- [ ] Missing-time reports visibly state omitted time-sensitive scope.
- [ ] Strict regression, full pytest, wheel inspection, and CI matrix are green.
