# v0.8.0 Core Profile Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the default birth-report rendering path with an auditable, evidence-selected core profile and dynamic report.

**Architecture:** A new audited-interpretive IR sits after qualified facts and existing signal synthesis. A deterministic planner selects only evidence-backed profile items; a renderer consumes only the profile and plan. Formal primitive release components remain untouched.

**Tech Stack:** Python 3.9, dataclasses, existing qualified-facts codecs, pytest.

## Global Constraints

- Do not read candidate mappings or claim formal primitive coverage.
- Preserve `standard-interpretive-v1` and `concise-interpretive-v1` behavior.
- All new public behavior starts with a failing pytest.
- Default birth output must persist all specified audit artifacts.

---

### Task 1: Audited profile contract and builder

**Files:**
- Create: `src/destiny_personality/audited_core_profile.py`
- Test: `tests/test_audited_core_profile.py`

- [x] Write failing tests asserting that a qualified fixture produces an `audited-interpretive-cdp-v1` with two source candidate sets, traceable profile items, and no formal assurance label.
- [x] Run `python -m pytest tests/test_audited_core_profile.py -q`; expect import failure.
- [x] Implement frozen dataclasses plus `build_audited_interpretive_core_profile(qualified_facts)` from extracted signals and existing narrative synthesis.
- [x] Run the test; expect pass.

### Task 2: Dynamic planner and contained renderer

**Files:**
- Create: `src/destiny_personality/audited_profile_report.py`
- Test: `tests/test_audited_profile_report.py`

- [x] Write failing tests for bounded dynamic section selection, no duplicate evidence identities, and renderer containment.
- [x] Run `python -m pytest tests/test_audited_profile_report.py -q`; expect import failure.
- [x] Implement `build_audited_profile_report_plan(profile)` and `render_audited_profile_report(profile, plan)` with profile-only inputs.
- [x] Run the test; expect pass.

### Task 3: Birth entry point and artifacts

**Files:**
- Modify: `src/destiny_personality/birth_report.py`
- Modify: `src/destiny_personality/cli.py`
- Test: `tests/test_birth_report.py`

- [x] Write failing tests proving the default produces CDP, plan and audit artifacts while explicit legacy mode remains unchanged.
- [x] Run `python -m pytest tests/test_birth_report.py -q`; expect failure.
- [x] Wire `core-profile-v1` as the default and keep legacy renderer branch intact.
- [x] Run the test; expect pass.

### Task 4: Multi-case evidence and quality acceptance

**Files:**
- Create: `docs/validation/v0.8.0/`
- Create: `docs/v0.8.0-report-quality-comparison.md`
- Test: `tests/test_v080_product_quality.py`

- [x] Write failing tests asserting three real local calculations differ in plan identity, every selected entry has traceable evidence, and the default output is not the old fixed section set.
- [x] Run `python -m pytest tests/test_v080_product_quality.py -q`; expect failure.
- [x] Generate versioned case artifacts and comparison documentation from the implemented path.
- [x] Run targeted and full test suites; expect pass.
