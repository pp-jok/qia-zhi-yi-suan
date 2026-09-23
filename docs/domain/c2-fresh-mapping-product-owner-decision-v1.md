# C2 Fresh Mapping Product Owner Decision v1

## Gate

```text
Gate: C2 FRESH MAPPING PRODUCT OWNER GATE
Current Candidate Count: 0
Reason: NO_CURRENT_DEFENSIBLE_MAPPING
```

The zero-candidate result is a valid fail-closed C2-M outcome. It means current canonical facts lack a project-approved Semantic Mechanism that can form an auditable bridge to a C1 Primitive question. It does not permanently prohibit any canonical fact family from future mapping.

## Independent Product Owner decisions

### Decision A — Current result

```text
Decision: ACCEPT_ZERO_CANDIDATES
Question: Accept CURRENT FRESH MAPPING RESULT = 0 DEFENSIBLE CANDIDATES?
Recommended choice: ACCEPT_ZERO_CANDIDATES
```

Accepting this result closes the current C2-M candidate run as correctly fail-closed. It does not abandon future Mapping research.

### Decision B — New product investment

```text
Decision: AUTHORIZED
Question: Authorize C2-SM Semantic Mechanism Asset Program?
Allowed values: AUTHORIZED | NOT_AUTHORIZED
```

Decision B is independent of Decision A. It determines whether the project will build a governed, project-owned Semantic Mechanism knowledge layer; it cannot retroactively make the current zero-candidate result incorrect.

## Authorization state

```text
Mapping v2 authorization: NONE
Signature authorization: NONE
C2-SM authorization: AUTHORIZED — Phase 1 infrastructure, Phase 2A fact-identity Evidence Roots, and Phase 2B proposed candidate review only
Phase 2B candidate authorization: SMC-AS-ASPECT-ELIGIBILITY-GATE-P004-V1 may be drafted and reviewed as proposed
Semantic Mechanism approval: NONE
Primitive Ontology v2 runtime activation: NONE
```

## Frozen baseline

```text
Active Semantic Fingerprint: 256ba053b174a054226301f1b493e0e0c8f9f50e9f2976a72b8045dbf6ed6131
Active Presentation Fingerprint: 2f1d3866638074485351ada0c6a9aaa9bd1acd916f65973ca2b319a75b99b91d
Runtime Identity: candidate-profile-runtime-v2
```

## Gate outcomes

| Decision A | Decision B | Outcome |
|---|---|---|
| ACCEPT_ZERO_CANDIDATES | NOT_AUTHORIZED | Close Fresh Mapping; do not create Mapping v2 or C2-SM. |
| ACCEPT_ZERO_CANDIDATES | AUTHORIZED | Close current C2-M run; open C2-SM infrastructure-only work after explicit task authorization. |
| Any other state | Any state | Keep this gate open; do not build semantic mechanisms or mappings. |

## Recorded decision

```text
Decision A: ACCEPT_ZERO_CANDIDATES
Decision B: AUTHORIZED
Recorded: 2026-09-22
```

The current C2-M run is closed as a valid zero-candidate result. Decision B
initially opened C2-SM Phase 1: candidate-only contracts, registry, validation,
audit, and review documentation. A delegated Product Owner authorization on
2026-09-22 subsequently admitted the two Phase 2A fact-identity Root
definitions. A further authorization on 2026-09-22 permitted Phase 2B to draft
and review `SMC-AS-ASPECT-ELIGIBILITY-GATE-P004-V1` in `proposed` state only.

Phase 2B candidate authorization is not Semantic Mechanism approval. The
candidate has no `product_owner_decision_ref`, is absent from the authoritative
approved-mechanism set, and cannot be consumed by Mapping Candidate design.
Mapping v2, Signature, and runtime activation remain unauthorized.
