# Fact Qualification and Profile Identity Freeze Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `executing-plans` task-by-task. Steps use checkbox syntax for tracking.

**Goal:** bind externally auditable qualification evidence to one formal facts packet, derive assurance accurately, and version Candidate Profile runtime behavior independently of semantic and presentation layers.

**Architecture:** `deterministic-facts-v1` remains the facts object; a separate `fact-qualification-v1` is supplied to the CLI and is fingerprint-bound to decoded facts. A qualified-facts loader returns facts plus derived assurance, while the builder remains a pure consumer. Candidate Profiles gain a profile-runtime version included in identity, normalization, codec, validation, and diff output.

**Tech Stack:** Python 3.9+, dataclasses, JSON, PyYAML, pytest, GitHub Actions.

## Global Constraints

- Do not alter any Primitive, mapping, state resolver, alignment, presentation meaning, calibration, or holdout asset.
- The semantic bundle fingerprint must remain unchanged.
- Public `build-core-profile` requires facts plus qualification and never accepts caller-selected assurance.
- `capability_reported` is a valid generated result; only a passed strict calculation-config evidence gate derives `project_verified`.
- No Signature, Dynamic, Fate Theme, Archetype, or production authorization.

---

### Task 1: Qualification contract and assurance derivation

**Files:**
- Modify: `src/destiny_personality/deterministic_facts_codec.py`
- Modify: `src/destiny_personality/core_profile_builder.py`
- Modify: `src/destiny_personality/cli.py`
- Create: `destiny-personality/schemas/fact-qualification.md`
- Test: `tests/test_cli.py`

**Interfaces:**
- `load_qualified_deterministic_facts(facts_path: Path, qualification_path: Path) -> QualifiedFacts`.
- `QualifiedFacts.facts` is a `DeterministicChartFacts`; `QualifiedFacts.fact_assurance` is derived.
- `derive_fact_assurance(facts, qualification) -> str` returns only `project_verified`, `capability_reported`, or raises a stable qualification error.

- [ ] Write failing tests for required qualification, A/B fingerprint mismatch, capability-reported derivation, project-verified derivation, and optional/required comparison states.
- [ ] Decode and validate `fact-qualification-v1`: fact contract/version, fingerprint, passed status, methods, non-empty audit refs, validation summary, and comparison policy.
- [ ] Derive assurance from qualification evidence; require `calculation_config: passed` for project verification and permit `not_available` only for capability-reported.
- [ ] Update CLI to require `--qualification`.
- [ ] Run `pytest -q tests/test_cli.py`.

### Task 2: Profile runtime identity

**Files:**
- Modify: `src/destiny_personality/core_profile_models.py`
- Modify: `src/destiny_personality/core_profile_builder.py`
- Modify: `src/destiny_personality/core_profile_validation.py`
- Modify: `src/destiny_personality/core_profile_codec.py`
- Modify: `src/destiny_personality/core_portrait.py`
- Test: `tests/test_core_profile_builder.py`
- Test: `tests/test_core_profile_codec.py`
- Test: `tests/test_core_portrait_preview.py`

**Interfaces:**
- `CandidateCoreProfile.profile_runtime_version == "candidate-profile-runtime-v2"`.
- `CandidateProfileVersionDiff.runtime_version_changed` reports runtime-only changes.

- [ ] Write failing tests proving runtime version changes profile identity and diff reason, fact-scope changes normalization, and JSON preserves runtime version.
- [ ] Add runtime version to the IR, profile ID hash, normalized representation, validator, codec, and diff reason.
- [ ] Run codec, builder, and portrait tests.

### Task 3: Contract synchronization and freeze record

**Files:**
- Modify: `destiny-personality/schemas/deterministic-facts.md`
- Modify: `destiny-personality/schemas/execution-report.md`
- Modify: `destiny-personality/checklists/preflight.md`
- Modify: `destiny-personality/SKILL.md`
- Create: `docs/domain/fact-qualification-profile-identity-freeze-v0.3.8.md`
- Modify: `release/qia-zhi-yi-suan/pyproject.toml`
- Modify: `release/qia-zhi-yi-suan/README.md`

- [ ] Document facts versus qualification authority and comparison statuses.
- [ ] Separate execution mode from requested core renderer route while preserving legacy compatibility.
- [ ] Record the v0.3.8 Core Portrait freeze gate and non-goals.

### Task 4: Verification and prerelease

- [ ] Confirm semantic fingerprint equals the v0.3.7 baseline.
- [ ] Run full pytest, calibration/holdout regressions, and package verifier.
- [ ] Publish `v0.3.8-fact-qualification-profile-identity-freeze` as a prerelease.
- [ ] Validate release archive, GitHub CI, and clean remote tree.
