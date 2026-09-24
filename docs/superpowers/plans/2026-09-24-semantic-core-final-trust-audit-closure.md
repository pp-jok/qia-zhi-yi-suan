# Semantic Core Final Trust and Audit Closure Implementation Plan

> **For agentic workers:** Execute inline with test-first changes; this plan is self-approved by the task request.

**Goal:** Close the remaining candidate-only trust, audit, evaluation, proposal, provenance, and lifecycle engineering gaps without approving or activating semantic assets.

**Architecture:** A repository-owned governance store becomes the only authority source for decisions and evaluation artifacts. Mapping compilation remains proposal-driven and fail-closed; the pipeline persists normalized provenance consumed by views, explain, audit, and diff.

**Tech Stack:** Python 3.9, PyYAML, JSON, pytest.

## Global Constraints

- Do not alter approved/proposed status of existing semantic assets.
- Do not modify active semantic or presentation fingerprints.
- Do not derive Mapping rules from mechanisms automatically.
- Production promotion is limited to recorded shadow state.

### Task 1: Repository Authority Store

- [ ] Add empty, versioned decision/evaluation registries under `governance/semantic-promotion-v1/`.
- [ ] Add a loader that rejects arbitrary paths, unknown IDs, superseded decisions, and unmatched artifacts.
- [ ] Test registry resolution and fail-closed behavior.

### Task 2: Mapping Evaluation and Proposal Contracts

- [ ] Define proposal validation separately from approved Mapping validation.
- [ ] Reuse existing candidate calibration/holdout policy and bind machine-produced result metadata to Mapping fingerprints.
- [ ] Test empty, mismatched, failed, and valid synthetic evaluation cases.

### Task 3: Context and Provenance

- [ ] Resolve exclusions first, preserve counterevidence, and distinguish contextual variation from mixed conflict.
- [ ] Persist one immutable provenance graph from Mapping through formed output.
- [ ] Test explain/source/audit traversal without recomputation.

### Task 4: Lifecycle, CLI, and Verification

- [ ] Retire legacy promotion from authority use and route authorized CLI through repository IDs only.
- [ ] Persist authority and evaluation references in promotion records; block duplicates.
- [ ] Update audit and closure report, then run focused tests, full tests, and package verification.

