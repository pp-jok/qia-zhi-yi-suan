# Semantic Core Final Closure Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Close the remaining candidate-only Semantic Core engineering gaps without changing active runtime semantics.

**Architecture:** Mapping v2 will validate and compile only independently approved, mechanism-backed candidate records; an empty registry remains a successful blocked state. Semantic Core will expose bounded source, explain, diff, and review interfaces which report engineering readiness separately from semantic readiness.

**Tech Stack:** Python 3, PyYAML, pytest, JSON CLI.

## Global Constraints

- Do not read or alter files outside this project.
- Do not change active semantic or presentation fingerprints.
- Do not create, approve, activate, or infer a real semantic mechanism or Mapping candidate.
- Synthetic records are test fixtures only and may not be written into candidate assets.
- A zero/blocked candidate state is valid and must be machine-readable.

---

### Task 1: Mapping v2 compiler and admission guard

**Files:**
- Modify: `src/destiny_personality/mapping_v2.py`
- Test: `tests/test_semantic_core_completion.py`

**Interfaces:**
- Consumes: `compile_mapping_v2_candidate_bundle(candidates, approved_mapping_eligible_ids=())`
- Produces: a `MappingV2CandidateBundle` with only Bazi/Astrology candidate records.

- [x] Write a failing test for an approved synthetic Mapping candidate and for legacy/direct-fact rejection.
- [x] Run `python3 -m pytest tests/test_semantic_core_completion.py -q` and observe import/behavior failure.
- [x] Implement strict candidate validation and a deterministic approved-only compiler.
- [x] Run the focused test and confirm it passes.

### Task 2: Bounded source, explain, diff, and readiness surfaces

**Files:**
- Modify: `src/destiny_personality/semantic_core.py`
- Modify: `src/destiny_personality/cli.py`
- Test: `tests/test_semantic_core_completion.py`

**Interfaces:**
- Produces: `semantic_core_source_view`, `build_semantic_core_review_packet`, and three JSON CLI commands.

- [x] Write failing tests for profile-contained source view and dual readiness reporting.
- [x] Run focused pytest and observe missing symbol/command failure.
- [x] Implement the bounded APIs and CLI commands.
- [x] Run focused pytest and confirm it passes.

### Task 3: Final acceptance and documentation

**Files:**
- Modify: `docs/reviews/master-semantic-core-engineering-completion.md`
- Test: complete test suite and package verifier.

- [x] Record final engineering versus semantic readiness with no activation claim.
- [x] Run `python3 -m pytest -q --disable-warnings` and package verification.
- [x] Confirm candidate fingerprint isolation and the zero-state CLI outputs.
