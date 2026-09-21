# Semantic Bundle Fingerprint Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Bind a successful semantic candidate validation report to the exact
runtime and candidate file bytes with deterministic SHA-256 digests.

**Architecture:** A focused `semantic_fingerprint` module hashes the fixed ten
validated files and returns a JSON-ready result. The CLI adds that result only
after the existing semantic loader succeeds. The Skill checklist uses the
digest as identity evidence while preserving human approval.

**Tech Stack:** Python 3.9, hashlib, pathlib, argparse, pytest, Markdown.

## Global Constraints

- Read and write only this project and temporary test locations.
- Do not create, infer, repair, copy, approve, or promote semantic assets.
- Use raw file bytes and SHA-256; do not normalize YAML before hashing.
- Output no absolute paths.
- Preserve `validate-config` output and existing failure behavior.
- Keep the distributable Skill free of Python and runtime tool dependencies.

---

### Task 1: Fingerprint module

**Files:**
- Create: `src/destiny_personality/semantic_fingerprint.py`
- Create: `tests/test_semantic_fingerprint.py`

**Interfaces:**
- Consumes: candidate and runtime configuration directories.
- Produces: `build_semantic_bundle_fingerprint(candidate_dir: Path, runtime_config_dir: Path) -> Dict[str, object]`.

- [x] Write a failing test that creates all ten files, checks every raw-byte
  digest, and independently reconstructs the canonical bundle digest.
- [x] Run `python3 -m pytest tests/test_semantic_fingerprint.py -q` and confirm
  failure because the module is absent.
- [x] Implement fixed inventories, raw-byte hashing, scoped keys, sorted
  canonical bundle hashing, and JSON-ready output.
- [x] Add failing then passing tests for a missing file (`CONFIG_GAP`) and an
  unreadable file (`CONFIG_PARSE_ERROR`).

### Task 2: CLI integration

**Files:**
- Modify: `src/destiny_personality/cli.py`
- Modify: `tests/test_cli.py`
- Modify: `scripts/verify_package.py`

**Interfaces:**
- Consumes: accepted semantic bundle and both explicit CLI directories.
- Produces: existing success JSON plus a `fingerprint` mapping.

- [x] Extend the CLI test first and confirm it fails because `fingerprint` is
  absent.
- [x] Call `build_semantic_bundle_fingerprint` only after semantic validation
  succeeds and include its result in the summary.
- [x] Assert loader failure never invokes fingerprinting and preserves empty
  stdout plus exit code `2`.
- [x] Extend isolated package verification to require the command in the
  installed Wheel while preserving its current missing-candidate failure.

### Task 3: Skill release semantics

**Files:**
- Modify: `destiny-personality/checklists/semantic-candidate-release.md`
- Modify: `tests/test_skill_package.py`

**Interfaces:**
- Consumes: the bundle SHA-256 recorded by a validation report.
- Produces: human workflow rules that bind review and approval to exact bytes.

- [x] Add failing assertions for same-digest review and approval, digest-change
  invalidation, and the statement that fingerprint identity is not approval.
- [x] Update the checklist without introducing any CLI invocation requirement.
- [x] Run focused fingerprint, CLI, and Skill tests.

### Task 4: Final verification

**Files:**
- Create: `docs/superpowers/evidence/2026-09-14-semantic-bundle-fingerprint.md`
- Modify: `docs/superpowers/plans/2026-09-14-semantic-bundle-fingerprint.md`

**Interfaces:**
- Consumes: final project state.
- Produces: reproducible verification evidence.

- [x] Run full pytest, official Skill validation, syntax and manifest checks,
  frozen-config comparison, forbidden-binary scan, production inventory, and
  isolated Wheel build-install-run verification.
- [x] Record exact results, mark plan steps complete, then rerun verification
  after the last file mutation.
