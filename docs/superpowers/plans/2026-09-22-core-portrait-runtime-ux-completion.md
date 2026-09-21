# Core Portrait Runtime and UX Completion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Complete the remaining Candidate Core Portrait runtime, user presentation, audit binding, CI, and release work without enabling Signature, Dynamic, Fate Theme, Archetype, or production authorization.

**Architecture:** Keep `CandidateCoreProfile` as the audited primitive-only IR. Add a lossless JSON codec and CLI bridge around it, then render only through the versioned presentation assets and `CandidateProfileSummary`. Treat calibration, holdout, clean-install tests, and fresh-clone verification as release gates.

**Tech Stack:** Python 3.9+, dataclasses, argparse, JSON, PyYAML, pytest, GitHub Actions.

## Global Constraints

- Keep `semantic_capability_level: primitive_only`.
- Do not add or infer new Primitive, Signature, Dynamic, Fate Theme, or Archetype semantics.
- User prose must not expose internal state tokens or rule IDs unless an explicit explanation/audit command is used.
- All fixtures remain synthetic and anonymous.
- Use TDD for every behavior change.
- Release only after a fresh clone passes `python -m pip install -e '.[test]'` and `python -m pytest -q`.

---

### Task 1: Freeze the current Fact Scope and presentation behavior

**Files:**
- Modify: `tests/test_core_portrait_preview.py`
- Modify: `src/destiny_personality/core_portrait.py`
- Modify: `destiny-personality/schemas/candidate-profile-summary.md`

**Interfaces:**
- Consumes: `CandidateCoreProfile.fact_scope`, presentation YAML assets.
- Produces: stable `CandidateProfileSummary`, unique user-facing sections, token-free prose.

- [ ] Add regression tests for unknown time with zero astrology candidates, known time without astrology candidates, `context_differentiated` priority, unique section IDs, exactly one `overview`, sparse evidence, and forbidden internal tokens.
- [ ] Run `python -m pytest -q tests/test_core_portrait_preview.py` and confirm the new assertions fail for the intended reasons.
- [ ] Refactor `render_core_concise()` and `render_core_standard()` so unknown primitives are not promoted to portrait themes and section count remains evidence-driven.
- [ ] Replace remaining raw context/state/Primitive tokens in ordinary portrait text with the versioned presentation assets.
- [ ] Run the focused tests and commit as `fix: freeze core portrait presentation behavior`.

### Task 2: Make Evidence and Comparison findings concrete and traceable

**Files:**
- Modify: `src/destiny_personality/core_portrait.py`
- Modify: `tests/test_core_portrait_presentation.py`

**Interfaces:**
- Produces: `build_overview_summary(summary)`, concrete evidence findings, concrete unresolved/contextualized findings, each with `profile_refs`.

- [ ] Write failing tests requiring every user-visible evidence/comparison sentence to reference at least one `primitive_states.Pxxx` path.
- [ ] Require validation, contextualization, unresolved, and single-system cases to name the presented Primitive and localized contexts rather than counts or rule IDs.
- [ ] Implement `build_overview_summary(summary) -> CorePortraitSection` using only selected summary items and alignment records.
- [ ] Verify no output contains `supported_high`, `context_differentiated`, `BZ-C2B`, `AS-C2B`, or English canonical Primitive names.
- [ ] Commit as `feat: render traceable core portrait findings`.

### Task 3: Add lossless Candidate Profile JSON codecs

**Files:**
- Create: `src/destiny_personality/core_profile_codec.py`
- Create: `tests/test_core_profile_codec.py`

**Interfaces:**
- Produces: `candidate_profile_to_dict(profile) -> dict`, `candidate_profile_from_dict(payload) -> CandidateCoreProfile`, `load_candidate_profile(path)`, `write_candidate_profile(profile, path)`.

- [ ] Write a round-trip test asserting `candidate_profile_from_dict(candidate_profile_to_dict(profile)) == profile` and exact preservation of tuples, mappings, fact scope, versions, evidence refs, and limitations.
- [ ] Add rejection tests for wrong schema, missing `fact_scope`, non-`primitive_only` capability, and invalid alignment/state values.
- [ ] Implement explicit field-by-field codecs; do not deserialize arbitrary class names.
- [ ] Run codec and profile-validation tests.
- [ ] Commit as `feat: add candidate profile json codec`.

### Task 4: Add the Core Portrait runtime CLI

**Files:**
- Modify: `src/destiny_personality/cli.py`
- Modify: `tests/test_cli.py`
- Modify: `destiny-personality/SKILL.md`

**Interfaces:**
- Produces commands `render-core-portrait`, `explain-profile-item`, `profile-source-view`, and `profile-diff`.

- [ ] Add failing CLI tests using temporary JSON profiles and captured stdout/stderr.
- [ ] Implement `render-core-portrait PROFILE --mode core|core_concise|core_standard`.
- [ ] Implement `explain-profile-item PROFILE primitive:P001`, preserving rule/fact refs only in this audit-oriented output.
- [ ] Implement `profile-source-view PROFILE --view combined|bazi|astrology|comparison`.
- [ ] Implement `profile-diff LEFT RIGHT`, including `fact_changed`, `mapping_version_changed`, `resolver_version_changed`, and `context_resolution_changed` reasons.
- [ ] Return exit code `2` with stable error codes for invalid JSON, schema, mode, view, or item ID.
- [ ] Update Skill execution instructions to use these deterministic commands.
- [ ] Commit as `feat: add core portrait runtime cli`.

### Task 5: Complete Calibration-to-Holdout policy binding

**Files:**
- Modify: `src/destiny_personality/calibration.py`
- Modify: `tests/test_candidate_calibration_runner.py`
- Modify: `candidates/core-profile-v1/holdout_validation_v2.yaml`
- Mirror: `src/destiny_personality/candidate_assets/core-profile-v1/holdout_validation_v2.yaml`

**Interfaces:**
- Consumes: active calibration policy version/SHA and calibration result JSON.
- Produces: holdout failure `HOLDOUT_CALIBRATION_POLICY_MISMATCH` whenever the run or current policy differs.

- [ ] Add failing tests for changed policy bytes, changed policy version, changed bundle, and a valid exact binding.
- [ ] Verify `run_candidate_holdout()` compares the calibration result's policy SHA/version with the active policy before evaluating cases.
- [ ] Regenerate the machine-readable calibration and holdout records from the frozen synthetic sets; do not tune mapping or threshold from holdout output.
- [ ] Update both source and packaged assets byte-identically.
- [ ] Commit as `fix: bind calibration run to holdout policy`.

### Task 6: Enforce clean-install CI and publish a verified release

**Files:**
- Modify: `.github/workflows/tests.yml`
- Modify: `README.md` in the release tree
- Modify: `agents/openai.yaml`
- Modify: `pyproject.toml` in the release tree

**Interfaces:**
- Produces: Python 3.9/3.11/3.12 CI and a fresh-clone-verifiable Candidate Preview release.

- [ ] Add a public-bootstrap test checking fixtures, scripts, schemas, presentation assets, and workflow presence.
- [ ] Validate the workflow runs `python -m pip install -e '.[test]'` before `python -m pytest -q` on all three Python versions.
- [ ] Update README with a prominent Core Portrait Preview section, mode differences, explanation and source-view examples, and the Candidate boundary.
- [ ] Update `agents/openai.yaml` so the default prompt advertises Core and legacy choices without forcing either.
- [ ] Run local full pytest.
- [ ] Clone the GitHub repository into a temporary directory, install test extras, and run full pytest there.
- [ ] Publish a new pre-release only when both runs pass and confirm main, annotated tag, package version, and release URL all reference the same commit.
- [ ] Commit/release as `release: core portrait runtime and ux baseline`.

## Final acceptance

- [ ] Gate R passes: codec, CLI, calibration/holdout binding, CI, clean install, and fresh-clone pytest.
- [ ] Gate U passes: localized presentation, one overview, unique IDs, concrete traceable findings, correct time scope, no padding, no internal tokens in ordinary portrait output.
- [ ] Technical readiness has no blocker; production authorization still returns `HUMAN_PRODUCTION_APPROVAL_REQUIRED`.
- [ ] Signature and Dynamic formation remain disabled and empty.
