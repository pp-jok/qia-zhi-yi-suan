# Semantic Core Non-Zero Closure Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the candidate-only Semantic Core fully executable with synthetic approved assets while keeping real unapproved semantics blocked.

**Architecture:** Authoritative repository loaders derive mapping eligibility from approval and role policy. A policy-driven, in-memory pipeline turns approved mappings into partial or complete core stages. Promotion consumes a bound decision artifact and persists its rollback record.

**Tech Stack:** Python 3.9, dataclasses, JSON, PyYAML, pytest.

## Global Constraints

- No real semantic approvals, mappings, activations, or active fingerprint changes.
- Synthetic non-zero policies and assets live only in tests.
- Public zero-state behavior remains backward compatible.

### Task 1: Authority and mapping admission

- [x] Add failing authority-path test.
- [x] Derive mapping eligibility from validated approved mechanisms and role policy.
- [x] Verify RULE_GATE remains ineligible and caller IDs are never authority.

### Task 2: Policy-driven semantic pipeline

- [x] Add failing complete synthetic pipeline test.
- [x] Implement mapping-to-primitive, signature, dynamic, theme, and optional archetype formation.
- [x] Preserve partial progression and zero-state stages.

### Task 3: Authoritative promotion persistence

- [x] Add failing decision/record test.
- [x] Validate decision artifact bindings and technical checks; persist promotion and rollback state.

### Task 4: Verification and reporting

- [x] Run focused and full tests, package verification, audit active fingerprint isolation, and update completion report.
