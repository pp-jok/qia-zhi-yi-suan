# C2-SM Phase 2A Evidence Root Verification

## Scope verified

```text
Phase: C2-SM Phase 2A
Evidence Roots: 2 approved fact-identity definitions
Semantic Mechanism candidates: 0
Mapping v2 candidates: 0
Runtime activation: none
```

The Registry now admits exactly two project-owned deterministic fact identity
definitions: `ER-BZ-TEN-GOD-INSTANCE-V1` and
`ER-AS-ASPECT-INSTANCE-V1`. Their scopes identify source facts only. Neither
entry supplies a Primitive direction, state, score, mechanism, or mapping.

## Validation behavior

The Registry loader validates every root against the root contract before
exposing it. Missing contract fields, duplicate IDs, unsupported review
statuses, non-string statuses, malformed nested structures, and prohibited
provenance origins fail closed. Only roots with `review_status: approved` can
be returned to Semantic Mechanism candidate validation.

```text
Root audit: {root_count: 2, approved_count: 2, non_approved_count: 0}
Semantic Mechanism candidate count: 0
```

## Isolation evidence

```text
Active Semantic Fingerprint: 256ba053b174a054226301f1b493e0e0c8f9f50e9f2976a72b8045dbf6ed6131
Active Presentation Fingerprint: 2f1d3866638074485351ada0c6a9aaa9bd1acd916f65973ca2b319a75b99b91d
Candidate Mechanism Fingerprint: d35242a51e2c2204209c4d2141a10cd884d7807e8d66e7571b9cd4423b323c69
Runtime Identity: candidate-profile-runtime-v2
```

The active fingerprints remain at the frozen C2-M baseline. The candidate
mechanism fingerprint changed as intended because only candidate-only YAML
assets changed.

## Verification

```text
python3 -m pytest -q tests/test_semantic_mechanism_contract.py tests/test_semantic_evidence_roots.py tests/test_semantic_mechanism_legacy_guard.py tests/test_semantic_mechanism_golden_leak.py tests/test_semantic_mechanism_activation_isolation.py
18 passed in 0.73s

python3 -m pytest -q --disable-warnings
486 passed in 41.98s

python3 scripts/verify_package.py
package verification passed
```

## Next gate

```text
C2-SM Phase 2A Evidence Roots: COMPLETE
First Semantic Mechanism candidate review: NOT STARTED
Mapping v2: NOT AUTHORIZED
Signature: NOT AUTHORIZED
C3: NOT AUTHORIZED
```

The next allowable work is a separately reviewed Semantic Mechanism candidate
that cites one or both approved Root IDs, asks an explicit C1 Primitive
question, and remains non-directional. Root approval does not authorize a
mapping or runtime activation.
