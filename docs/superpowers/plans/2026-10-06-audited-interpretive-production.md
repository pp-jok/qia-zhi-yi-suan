# Audited Interpretive Production Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `subagent-driven-development` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Deliver `v0.5.0` as the first usable, traceable, differentiated traditional-interpretation report product while preserving Strict / Research Mode unchanged.

**Architecture:** A new `audited_interpretive` runtime consumes only qualified deterministic chart facts. Its versioned Bazi and astrology rules emit traceable signals; a small deterministic synthesizer preserves agreement and tension; a report renderer turns the resulting profile into concise and standard Chinese reports. The existing strict Core Profile, release renderer, semantic mappings, and candidate assets are not imported or altered by this path.

**Tech Stack:** Python 3.9+, dataclasses, PyYAML, pytest, existing qualified-facts codec and console CLI.

## Global Constraints

- The Strict / Research path remains behaviorally unchanged and may still return all `unknown` states.
- Do not create `PRIMARY_EVIDENCE`, activate mappings, mutate primitives, or consume candidate mappings from the production path.
- Every interpretive signal has a stable ID, system, qualified-fact references, traditional-rule reference, topic, direction, interpretation, confidence, and limitations.
- Confidence values are exactly `high`, `moderate`, `exploratory`, and `insufficient`; no numeric personality score is introduced.
- Product reports say they are traditional interpretive output rather than an empirical psychological diagnosis.
- Time-sensitive astrology rules only run when their required chart facts are available; missing birth time must visibly degrade output rather than invent angles or houses.
- `standard` is the primary mode and has 8–12 useful sections; `concise` is supported; legacy long-form modes stay frozen.
- All new rule assets are versioned package data under `src/destiny_personality/interpretive_assets/`; no runtime network access.

---

## File Structure

- `src/destiny_personality/interpretive_models.py`: immutable public report, profile, synthesis, signal, and rule-bundle models.
- `src/destiny_personality/interpretive_rules.py`: load/validate versioned assets and extract deterministic Bazi/astrology signals.
- `src/destiny_personality/interpretive_profile.py`: synthesize signals into an interpretive profile without using strict/candidate components.
- `src/destiny_personality/interpretive_report.py`: format concise/standard report objects and controlled Chinese narrative.
- `src/destiny_personality/interpretive_codec.py`: JSON encode/decode helpers for finished product reports.
- `src/destiny_personality/interpretive_assets/v1/interpretive_rules_v1.yaml`: bounded traditional-rule contract with named methodology/source references.
- `src/destiny_personality/cli.py`: `build-interpretive-report` command only; strict command behavior remains unchanged.
- `tests/test_interpretive_rules.py`, `tests/test_interpretive_profile.py`, `tests/test_interpretive_report.py`, `tests/test_interpretive_cli.py`: test-first behavior and product quality gates.
- `tests/fixtures/interpretive/`: qualified fact and qualification fixture pairs for contrast, tension, and missing-time scenarios.
- `destiny-personality/SKILL.md`, `README.md`, `CHANGELOG.md`, `pyproject.toml`: route normal production to audited interpretation and declare v0.5.0.

### Task 1: Versioned rule contract and public models

**Files:**
- Create: `src/destiny_personality/interpretive_models.py`
- Create: `src/destiny_personality/interpretive_rules.py`
- Create: `src/destiny_personality/interpretive_assets/v1/interpretive_rules_v1.yaml`
- Modify: `pyproject.toml`
- Test: `tests/test_interpretive_rules.py`

**Interfaces:**
- Produces `load_interpretive_rule_bundle() -> InterpretiveRuleBundle`.
- Produces `InterpretiveSignal`, with `confidence: Literal["high", "moderate", "exploratory", "insufficient"]` and non-empty fact/rule provenance.

- [ ] **Step 1: Write failing rule-bundle tests**

```python
def test_rule_bundle_is_versioned_and_contains_both_systems():
    bundle = load_interpretive_rule_bundle()
    assert bundle.bundle_version == "audited-interpretive-rules-v1"
    assert {rule.system for rule in bundle.rules} == {"bazi", "astrology"}

def test_rule_loader_rejects_unknown_confidence(tmp_path):
    with pytest.raises(ValueError, match="INTERPRETIVE_RULE_INVALID_CONFIDENCE"):
        load_interpretive_rule_bundle(tmp_path)
```

- [ ] **Step 2: Run the focused tests and observe import/feature failure**

Run: `python3 -m pytest tests/test_interpretive_rules.py -q`
Expected: FAIL because `interpretive_rules` does not exist.

- [ ] **Step 3: Add the minimum immutable models, YAML asset, and validating loader**

```python
@dataclass(frozen=True)
class InterpretiveSignal:
    signal_id: str
    system: str
    fact_refs: tuple[str, ...]
    traditional_rule_ref: str
    topic: str
    direction: str
    interpretation: str
    confidence: str
    limitations: tuple[str, ...]
```

Asset rules must cover Bazi Ten-God/elemental/relation facts and astrology planet/sign/aspect/dignity facts, carry a named school/method/source reference, and never claim empirical diagnostic status.

- [ ] **Step 4: Re-run focused tests**

Run: `python3 -m pytest tests/test_interpretive_rules.py -q`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add src/destiny_personality/interpretive_models.py src/destiny_personality/interpretive_rules.py src/destiny_personality/interpretive_assets/v1/interpretive_rules_v1.yaml pyproject.toml tests/test_interpretive_rules.py
git commit -m "feat: add audited interpretive rule contract"
```

### Task 2: Fact-to-signal extraction and degradation

**Files:**
- Modify: `src/destiny_personality/interpretive_rules.py`
- Test: `tests/test_interpretive_rules.py`
- Create: `tests/fixtures/interpretive/`

**Interfaces:**
- Consumes `QualifiedFacts` and `InterpretiveRuleBundle`.
- Produces `extract_interpretive_signals(qualified_facts, bundle=None) -> tuple[InterpretiveSignal, ...]`.

- [ ] **Step 1: Write failing behavior tests**

```python
def test_extraction_emits_traceable_bazi_and_astrology_signals(qualified_fixture):
    signals = extract_interpretive_signals(qualified_fixture)
    assert {signal.system for signal in signals} == {"bazi", "astrology"}
    assert all(signal.fact_refs and signal.traditional_rule_ref for signal in signals)

def test_missing_time_skips_house_and_angle_rules(missing_time_fixture):
    signals = extract_interpretive_signals(missing_time_fixture)
    assert all("house" not in signal.signal_id and "angle" not in signal.signal_id for signal in signals)
```

- [ ] **Step 2: Run focused tests and observe missing extractor failure**

Run: `python3 -m pytest tests/test_interpretive_rules.py -q`
Expected: FAIL because the extractor is absent.

- [ ] **Step 3: Implement direct predicate evaluation over qualified facts**

Use only fact paths declared by rule assets. Return an empty tuple for unmatched rules; skip time-sensitive rules when their fact paths are unavailable. Build each `fact_refs` entry from actual qualified-fact identifiers/paths, never inferred text.

- [ ] **Step 4: Re-run focused tests**

Run: `python3 -m pytest tests/test_interpretive_rules.py -q`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add src/destiny_personality/interpretive_rules.py tests/test_interpretive_rules.py tests/fixtures/interpretive
git commit -m "feat: extract qualified-fact interpretive signals"
```

### Task 3: Controlled cross-system synthesis and core profile

**Files:**
- Create: `src/destiny_personality/interpretive_profile.py`
- Modify: `src/destiny_personality/interpretive_models.py`
- Test: `tests/test_interpretive_profile.py`

**Interfaces:**
- Consumes `tuple[InterpretiveSignal, ...]`.
- Produces `build_interpretive_core_profile(qualified_facts) -> InterpretiveCoreProfile`.
- `InterpretiveCoreProfile` preserves per-topic supporting and countervailing signal IDs and supports `mode == "audited_interpretive"`.

- [ ] **Step 1: Write failing profile tests**

```python
def test_profile_preserves_cross_system_agreement_and_tension(qualified_fixture):
    profile = build_interpretive_core_profile(qualified_fixture)
    assert profile.mode == "audited_interpretive"
    assert any(item.supporting_signal_ids for item in profile.conclusions)
    assert any(item.countervailing_signal_ids for item in profile.conclusions)

def test_profile_uses_only_allowed_confidence_labels(qualified_fixture):
    profile = build_interpretive_core_profile(qualified_fixture)
    assert {item.confidence for item in profile.conclusions} <= ALLOWED_CONFIDENCES
```

- [ ] **Step 2: Run focused tests and observe feature failure**

Run: `python3 -m pytest tests/test_interpretive_profile.py -q`
Expected: FAIL because the profile builder is absent.

- [ ] **Step 3: Implement topic grouping, agreement/tension, and confidence policy**

Same-topic, same-direction signals become agreement; different directions become tension. `high` requires support from both systems or multiple independent rules and no direct counter-signal; `moderate` requires one stable matched rule; `exploratory` marks partial/mixed evidence; `insufficient` is used when a requested topic has no matched rule. Do not aggregate into a score.

- [ ] **Step 4: Re-run focused tests**

Run: `python3 -m pytest tests/test_interpretive_profile.py -q`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add src/destiny_personality/interpretive_models.py src/destiny_personality/interpretive_profile.py tests/test_interpretive_profile.py
git commit -m "feat: synthesize audited interpretive profiles"
```

### Task 4: Standard and concise product reports plus codec

**Files:**
- Create: `src/destiny_personality/interpretive_report.py`
- Create: `src/destiny_personality/interpretive_codec.py`
- Test: `tests/test_interpretive_report.py`

**Interfaces (final trusted-boundary revision):**
- Publicly consumes only `QualifiedFacts`; profile rendering remains private.
- Produces `build_interpretive_report(qualified_facts, mode) -> InterpretiveReport`, where mode is `standard` or `concise`.
- Produces `encode_interpretive_report(report) -> dict`.

- [ ] **Step 1: Write failing rendering tests**

```python
def test_standard_report_has_user_readable_depth_and_audit_refs(profile):
    report = build_interpretive_report(profile, mode="standard")
    assert 8 <= len(report.sections) <= 12
    assert all(section.signal_ids for section in report.sections)
    assert "传统命理" in report.boundary_statement

def test_concise_report_is_shorter_than_standard(profile):
    assert len(build_interpretive_report(profile, "concise").sections) < len(build_interpretive_report(profile, "standard").sections)
```

- [ ] **Step 2: Run focused tests and observe feature failure**

Run: `python3 -m pytest tests/test_interpretive_report.py -q`
Expected: FAIL because report modules do not exist.

- [ ] **Step 3: Implement deterministic Chinese report composition**

Use profile conclusions only. Standard report uses eight named topics: baseline disposition, thinking/learning, expression/creation, relationships/boundaries, work/drive, stress/energy, growth tension, and synthesis; add up to four evidence-backed topics. Every section exposes signal IDs and a brief limitation, while report-level audit metadata records rule bundle and fact/qualification provenance.

- [ ] **Step 4: Re-run focused tests**

Run: `python3 -m pytest tests/test_interpretive_report.py -q`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add src/destiny_personality/interpretive_report.py src/destiny_personality/interpretive_codec.py tests/test_interpretive_report.py
git commit -m "feat: render audited interpretive reports"
```

### Task 5: CLI, fixtures, and end-to-end product gates

**Files:**
- Modify: `src/destiny_personality/cli.py`
- Create: `tests/test_interpretive_cli.py`
- Modify: `tests/fixtures/interpretive/`
- Create: `docs/demos/v0.5.0/`

**Interfaces:**
- Adds `build-interpretive-report FACTS.json --qualification QUALIFICATION.json --mode {standard,concise} --output OUTPUT.json`.
- CLI uses `load_qualified_facts`, the interpretive profile builder, and report builder; it never calls strict or candidate profile builders.

- [ ] **Step 1: Write failing CLI/product tests**

```python
def test_cli_builds_traceable_standard_report(tmp_path, fixture_paths):
    exit_code = main(["build-interpretive-report", str(fixture_paths.facts), "--qualification", str(fixture_paths.qualification), "--mode", "standard", "--output", str(tmp_path / "report.json")])
    assert exit_code == 0
    payload = json.loads((tmp_path / "report.json").read_text())
    assert payload["mode"] == "audited_interpretive"

def test_distinct_charts_do_not_collapse_to_identical_reports(fixture_paths):
    assert render_fixture("contrast_a") != render_fixture("contrast_b")
```

- [ ] **Step 2: Run focused tests and observe missing-command failure**

Run: `python3 -m pytest tests/test_interpretive_cli.py -q`
Expected: FAIL because the command is absent.

- [ ] **Step 3: Implement CLI and generate checked-in demo artifacts**

Create five or more synthetic/curated qualified fixture pairs including contrast, tension, and missing-time scenarios. Generate three JSON demo reports only through the new CLI; commit the resulting artifacts and test that they remain parseable and traceable.

- [ ] **Step 4: Re-run focused tests**

Run: `python3 -m pytest tests/test_interpretive_cli.py -q`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add src/destiny_personality/cli.py tests/test_interpretive_cli.py tests/fixtures/interpretive docs/demos/v0.5.0
git commit -m "feat: add interpretive report product CLI"
```

### Task 6: Skill routing, release documentation, package and regression verification

**Files:**
- Modify: `destiny-personality/SKILL.md`
- Modify: `README.md`
- Modify: `CHANGELOG.md`
- Modify: `pyproject.toml`
- Test: existing strict regression tests plus product tests

**Interfaces:**
- Normal user route selects `audited_interpretive`; explicit audit/research route selects `strict`.
- v0.5.0 wheel includes the interpretive YAML asset.

- [ ] **Step 1: Write failing packaging/routing assertions**

```python
def test_package_data_declares_interpretive_assets(pyproject_text):
    assert "interpretive_assets/v1/*.yaml" in pyproject_text

def test_skill_routes_normal_personality_reports_to_audited_interpretive(skill_text):
    assert "audited_interpretive" in skill_text
```

- [ ] **Step 2: Run the relevant tests and observe missing declarations**

Run: `python3 -m pytest tests/test_interpretive_cli.py tests/test_release_end_to_end.py -q`
Expected: FAIL until product declarations are added or, if no direct assertion is appropriate, preserve an explicit package-build inspection command in the final gate.

- [ ] **Step 3: Update routing and release documentation without altering strict behavior**

Document confidence meanings, traceability, missing-time degradation, report modes, and the traditional-interpretation boundary. Bump package version to `0.5.0` and include the YAML glob.

- [ ] **Step 4: Run full verification**

Run: `python3 -m pytest -p no:terminal -o addopts=`
Expected: PASS with no failures.

Run: `python3 -m build --wheel`
Expected: PASS and wheel contains `interpretive_assets/v1/interpretive_rules_v1.yaml`.

- [ ] **Step 5: Commit**

```bash
git add destiny-personality/SKILL.md README.md CHANGELOG.md pyproject.toml tests
git commit -m "docs: route production reports through audited interpretation"
```

## Final Review Checklist

- [ ] Strict release report output is regression-tested and unchanged.
- [ ] A qualified fact packet produces an 8–12-section standard report with auditable signal provenance.
- [ ] At least two contrasting charts produce materially different report JSON.
- [ ] Missing time omits house/angle claims and adds a limitation.
- [ ] No production module imports from `candidate_*`, mapping registries, or strict Core Profile modules.
- [ ] Full test suite, wheel build, and installed-wheel asset inspection pass.
