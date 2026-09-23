# C2-SM Infrastructure Verification

## Scope verified

```text
Program: C2-SM Phase 1
Authorization: infrastructure only
Semantic Mechanism candidates: 0
Evidence Root registry entries: 0
Approved Evidence Roots: 0
Mapping v2 candidates: 0
Runtime activation: none
```

This document is the historical Phase 1 verification snapshot. It was
subsequently extended by the Phase 2A Evidence Root verification; its recorded
zero-entry Registry state must not be read as the current Registry state.

The implementation supplies candidate-only contracts, an empty valid Evidence
Root Registry, a loader, candidate validation, audit summaries, legacy and
Golden-Sample guards, Mapping Candidate eligibility checks, and a separate
candidate-mechanism fingerprint. No real semantic content was introduced.

## Required guard coverage

| Requirement | Verified behavior |
|---|---|
| No root | Blocking error. |
| Unapproved root | Blocking error. |
| No Primitive question | Blocking error. |
| Direct state assertion | Blocking error. |
| Legacy-equivalent candidate | Review warning. |
| Golden Sample-derived candidate | Blocking error. |
| Unapproved mechanism consumed by Mapping design | Blocking error. |
| Approved mechanism consumed by Mapping design | Design eligibility only; not runtime activation. |
| Empty registries | Valid Phase 1 state. |
| Candidate changes | Change only the separate candidate-mechanism fingerprint. |

## Isolation evidence

```text
Active Semantic Fingerprint: 256ba053b174a054226301f1b493e0e0c8f9f50e9f2976a72b8045dbf6ed6131
Active Presentation Fingerprint: 2f1d3866638074485351ada0c6a9aaa9bd1acd916f65973ca2b319a75b99b91d
Candidate Mechanism Fingerprint: d901b3e97e44824a7664c44115f20f59f9f4a89480c759490d3fe0899b9e4f8f
Runtime Identity: candidate-profile-runtime-v2
```

The active fingerprints match the frozen C2-M baseline. The separate candidate
fingerprint covers only YAML files under `candidates/semantic-mechanisms-v1/`.

## Verification commands

```text
python3 -m pytest -q tests/test_semantic_mechanism_contract.py tests/test_semantic_evidence_roots.py tests/test_semantic_mechanism_legacy_guard.py tests/test_semantic_mechanism_golden_leak.py tests/test_semantic_mechanism_activation_isolation.py
12 passed in 0.35s

python3 -m pytest -q --disable-warnings
480 passed in 24.49s

python3 scripts/verify_package.py
package verification passed
```

## Gate status

```text
C2-SM Phase 1 infrastructure: READY FOR PRODUCT OWNER REVIEW
C2-SM semantic asset admission: NOT STARTED
Mapping v2: NOT AUTHORIZED
Signature: NOT AUTHORIZED
C3: NOT AUTHORIZED
```

The next allowable work is a separately scoped Evidence Root or Semantic
Mechanism submission under the governance documents. No such asset may be
created or activated without its own review and Product Owner decision.
