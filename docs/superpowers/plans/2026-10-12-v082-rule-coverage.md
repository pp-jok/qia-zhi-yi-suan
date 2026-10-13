# v0.8.2 Rule Coverage and Semantic Relations Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `executing-plans` task-by-task. Steps use checkbox syntax for tracking.

**Goal:** Increase audited interpretive coverage through traceable rules and explicit, fact-bound relationship evidence without relaxing qualification or formal semantic-core governance.

**Architecture:** Keep the existing versioned interpretive-rule bundle as the only source of reader signals. Add a second, versioned relationship bundle whose rules select already matched signal IDs; the audited profile builder consumes only those matched relationship records for Dynamics, Shadow/Mature, Themes and any Archetype. A conservative single-system signature gate admits only multi-signal, multi-fact candidates.

**Tech Stack:** Python 3.9+, dataclasses, PyYAML, pytest, existing deterministic facts and qualification codecs.

## Global Constraints

- Do not change local chart providers, fact qualification, Primitive, Mapping, or PRIMARY_EVIDENCE status.
- A Dynamic requires an explicit matched relationship rule; signal count alone is insufficient.
- Rules remain traditional, non-diagnostic, non-predictive and traceable to fact paths and cited method references.
- Do not hard-code dates, case IDs, stochastic copy, or forced deep sections.
- Preserve strict and legacy report routes.

---

### Task 1: Rule coverage audit and relation contract

**Files:**
- Create: `src/destiny_personality/interpretive_relationships.py`
- Create: `src/destiny_personality/interpretive_assets/v1/interpretive_relationships_v1.yaml`
- Test: `tests/test_v082_semantic_relations.py`

- [ ] Write failing tests for a validated relationship asset, a matched relationship, a missing prerequisite, and rejection of invalid relationship fields.
- [ ] Run the targeted tests and confirm they fail because the relationship module is absent.
- [ ] Implement the smallest validated loader and signal-ID matcher; return exact rule, signal and fact provenance.
- [ ] Run targeted relation tests and confirm they pass.

### Task 2: Evidence-driven profile synthesis

**Files:**
- Modify: `src/destiny_personality/audited_core_profile.py`
- Test: `tests/test_v082_semantic_relations.py`

- [ ] Write failing tests proving multi-direction candidates do not form Dynamics without a relationship rule.
- [ ] Write failing tests proving an explicit relationship forms a traceable Dynamic and its specific pressure/integration text.
- [ ] Implement relationship-driven Dynamics, relationship-derived Shadow/Mature, structurally shared Themes, and a non-fixed Archetype summary.
- [ ] Add a conservative single-system Signature gate requiring multiple matched signals and distinct fact paths.
- [ ] Run targeted tests and confirm they pass.

### Task 3: Coverage expansion and report contract

**Files:**
- Modify: `src/destiny_personality/interpretive_assets/v1/interpretive_rules_v1.yaml`
- Modify: `src/destiny_personality/audited_profile_report.py`
- Test: `tests/test_v082_semantic_relations.py`

- [ ] Write failing tests for expanded, non-demo-specific rules and visible fact-bound report evidence.
- [ ] Add only general fact predicates with cited method references, explicit limits, and no Primary Evidence effect.
- [ ] Make planning select additional evidence only when it is already signature/rule supported; retain sparse-report degradation.
- [ ] Run targeted tests and confirm they pass.

### Task 4: Audits, ten-case validation and release documentation

**Files:**
- Create: `docs/v0.8.2-rule-coverage-audit.md`
- Create: `docs/v0.8.2-evidence-funnel-analysis.md`
- Create: `docs/validation/v0.8.2/`
- Create: `docs/v0.8.2-report-quality-comparison.md`
- Modify: `README.md`, `CHANGELOG.md`, `pyproject.toml`

- [ ] Generate ten qualified birth-input validation artifacts, including a missing-time case, using the public product route.
- [ ] Record per-stage counts/IDs/exclusions for A-D, rule coverage, relationship coverage and known gaps.
- [ ] Compare v0.8.1 and v0.8.2 without claiming an unsupported quality improvement.
- [ ] Run the complete test suite, package verification, and a clean end-to-end report generation.
- [ ] Commit only after fresh verification evidence is available.
