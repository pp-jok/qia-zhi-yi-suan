# Semantic Snapshot Stability Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ensure a semantic validation report fingerprints the same stable file
set that the loaders accepted.

**Architecture:** Keep hashing and parsing separate, but run two complete
validation passes with one fingerprint after each pass. Only equal fingerprints
may produce success, and the second pass supplies the reported models.

**Tech Stack:** Python 3.9, argparse, pytest, existing configuration loaders.

## Global Constraints

- Read and write only this project and temporary test locations.
- Preserve the fixed ten-file SHA-256 contract.
- Do not mutate, lock, copy, approve, or promote candidate files.
- Preserve all existing error ordering and `validate-config` output.
- Return `CONFIG_VALUE_ERROR` and empty stdout when snapshots differ.

---

### Task 1: CLI stability gate

**Files:**
- Modify: `tests/test_cli.py`
- Modify: `src/destiny_personality/cli.py`

**Interfaces:**
- Consumes: existing runtime loader, semantic bundle loader, and fingerprint builder.
- Produces: `_load_stable_semantic_snapshot(candidate_dir: Path, runtime_config_dir: Path)` returning the second runtime object, second semantic bundle, and stable fingerprint.

- [x] Update the success test to require two complete validation and fingerprint
  passes in exact order; run it and confirm the current single-pass behavior
  fails.
- [x] Add a test where fingerprints differ and assert exit code `2`, empty
  stdout, and the exact `CONFIG_VALUE_ERROR` message.
- [x] Implement the smallest helper that performs both passes, compares the
  fingerprint mappings, and returns only the second pass objects.
- [x] Run the CLI suite and preserve the original `validate-config` JSON.

### Task 2: Workflow synchronization

**Files:**
- Modify: `tests/test_skill_package.py`
- Modify: `destiny-personality/checklists/semantic-candidate-release.md`
- Modify: `docs/superpowers/specs/2026-09-14-semantic-bundle-fingerprint-design.md`

**Interfaces:**
- Consumes: successful stable-snapshot validation report.
- Produces: release guidance forbidding review of a changed or unstable snapshot.

- [x] Add failing Skill assertions for stable-snapshot validation and retry on
  concurrent change.
- [x] State that only a stable validation report may advance to human review;
  do not introduce a CLI runtime dependency.
- [x] Update the fingerprint design to reference the stability refinement.
- [x] Run focused CLI and Skill tests.

### Task 3: Final verification

**Files:**
- Create: `docs/superpowers/evidence/2026-09-14-semantic-snapshot-stability.md`
- Modify: `docs/superpowers/plans/2026-09-14-semantic-snapshot-stability.md`

**Interfaces:**
- Consumes: final project state.
- Produces: reproducible verification record.

- [x] Run full pytest, official Skill validation, Python syntax, manifest,
  frozen configuration, binary inventory, and isolated Wheel verification.
- [x] Record exact results and mark this plan complete, then rerun all final
  checks after the last file mutation.
