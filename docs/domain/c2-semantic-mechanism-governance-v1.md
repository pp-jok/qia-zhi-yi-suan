# C2 Semantic Mechanism Governance v1

## Status and scope

```text
Program: C2-SM
Authorization: PHASE 1 infrastructure + Phase 2A fact-identity Roots + Phase 2B proposed gate review
Runtime status: INACTIVE
Semantic Mechanism candidates: 1 (proposed)
Approved Semantic Mechanisms: 0
Approved Evidence Roots: 2
Mapping v2 candidates: 0
```

C2-SM is a candidate-only governance layer. It creates a reviewable bridge
format between a project-approved Evidence Root and one C1 Primitive question;
it is not an interpretation engine and cannot produce a Primitive state.

Its assets live only in `candidates/semantic-mechanisms-v1/`. They are not
loaded by the active runtime and are excluded from active semantic and
presentation fingerprints.

## Required mechanism shape

Every future Semantic Mechanism candidate must declare all of the following:

- stable candidate identifier and candidate-only review state;
- one or more approved `evidence_root_refs`;
- one or more target C1 Primitive questions;
- one of the allowed roles: `PRIMARY_EVIDENCE`, `MODIFIER`,
  `CONTEXTUALIZER`, `COUNTER_EVIDENCE`, `EXCLUSION`, or `RULE_GATE`;
- a non-directional explanation of what evidence can be considered; and
- provenance and a legacy-similarity comparison.

A mechanism must not directly assert a Primitive state. Missing roots, missing
Primitive questions, unapproved roots, direct state assertions, and
Golden-Sample origin are blocking errors. Material equivalence to a legacy rule
is a review warning, never an automatic admission.

## Lifecycle

```text
candidate draft
  -> contract and guard validation
  -> evidence-root review
  -> Semantic Mechanism Product Owner decision
  -> eligible for separate Mapping Candidate design
  -> separate Mapping v2 authorization required
```

Approval of a mechanism only makes it eligible to be considered in Mapping
Candidate design. It does not create a mapping, change a C1 result, or enable a
runtime path.

## Explicit exclusions

This version contains two approved fact-identity Evidence Roots and one
proposed Semantic Mechanism:
`SMC-AS-ASPECT-ELIGIBILITY-GATE-P004-V1`. It is a `RULE_GATE` that permits an
identified astrology aspect instance to enter later P004 evidence review. It
cannot establish P004 direction, magnitude, score, or Primitive state.

The candidate is not an approved mechanism and cannot be cited by a Mapping
Candidate. It has no runtime path. Neither Root nor the proposed mechanism
contains a Primitive direction, state, score, or mapping. This work does not
modify legacy rules, Mapping v2, calibration, holdout, Signature, C3, or the
active runtime.
