# C2-SK P004 Hellenistic Method Validation Final Report

## 1. Actual baseline

Remote `main` was rechecked before implementation and remained `0621a40c95158e4aa36e4201ee963a5eb2d8e641` (`feat: add P004 astrology methodology candidate`). The project directory is an exported workspace rather than a Git worktree, so remote identity was verified through the GitHub API.

## 2. Governance state

- Semantic Core Foundation: `FROZEN / COMPLETE`.
- Semantic Knowledge Governance: `FROZEN / REUSABLE`.
- D1 Aspect RULE_GATE: `PENDING`; it remains non-directional fact admission.
- D2 Planet Placement Root: `PENDING`; it remains body/longitude/sign/degree identity only.
- D3 Hellenistic Natal Methodology: `PENDING`.
- Candidate: `AMC-AS-P004-HELLENISTIC-NATAL-V1`, `proposed / inactive`.

## 3. Evidence symmetry

`PASS`. Hellenistic natal has a registry-backed Method Authority. Modern psychological natal has an institutional method source and a defer-boundary claim. Horary application/perfection has two technical sources and an event-versus-natal boundary claim. These are sufficient to justify the three dispositions without pretending equal depth or truth.

## 4. Method authority sources

Only `SK-AS-HELLENISTIC-GEORGE-2019-2022` defines the candidate method. Its two authority claims establish a coherent natal condition procedure and enumerate the full planetary-condition framework.

## 5. Boundary sources

Houlding, Campion, CPA, Skyscript horary glossary, and the project ontology are explicitly boundary-only. The Loader prevents cross-school Sources or Claims from entering Method Authority and rejects overlapping roles.

## 6–10. Condition inventory and materiality

This report's first materiality pass was superseded by `c2-sk-p004-materiality-hardening-final-report.md`. The hardened audit reclassifies method-role-only techniques as `UNRESOLVED`; only automatic transfer of horary application/perfection event timing remains a scoped `NOT_P004` conclusion.

No technique is `P004_REQUIRED`, `P004_MODIFIER`, `P004_CONTEXTUALIZER`, or `P004_COUNTEREVIDENCE`. Consequently:

- Required P004 techniques: none.
- Excluded transfers: horary event logic; good-condition→high; difficult-condition→low; easy-aspect→high; hard-aspect→low; sign shortcut; absence→low.
- Unresolved: a Hellenistic-authority bridge from a governed fact pattern to P004 action initiation/advancement.

## 11–12. Canonical fact and Root gaps

Placement identity remains required to identify any future candidate input; D2 is therefore still pending. Aspects, dignities, and houses are optional until a future mechanism proves P004 materiality. Sect and the other unimplemented condition calculations are not current P004 gaps. No new Evidence Root is required by this validation.

## 13. Candidate contract changes

The candidate now carries machine-separated Method Authority, cross-school boundary, and project-boundary references; a typed condition-technique audit; separate candidate-validation and Product Owner-selection states; and a nullable PO decision reference.

## 14. Product Owner provenance

`PO_APPROVAL_PROVENANCE_ENFORCED`. An `approved_for_semantic_design` candidate must have a non-empty `product_owner_decision_ref` and `SELECTED_FOR_SEMANTIC_DESIGN`. A proposed candidate must remain `PENDING` with a null decision reference. No approval was fabricated.

## 15. Candidate readiness

All four gates pass:

- Evidence Symmetry: `PASS`.
- Authority Purity: `PASS`.
- P004 Materiality Completeness: `PASS`.
- PO Approval Provenance: `PASS`.

Result: `D3_READY_FOR_PRODUCT_OWNER_DECISION`.

## 16–17. Direction readiness

- Astrology High: `BLOCKED_BY_D3_AND_DIRECTION_EVIDENCE`.
- Astrology Low: `NO_DEFENSIBLE_MECHANISM`.
- Bazi High / Low: unchanged at `NO_DEFENSIBLE_MECHANISM`.

## 18–19. New registry assets

New Sources: CPA psychological method description; Skyscript application; Skyscript perfection. Updated Source: Demetra George now points to the Volume One full condition inventory.

New Claims: Hellenistic condition inventory boundary; modern psychological method boundary; horary event boundary; project condition-not-direction boundary.

## 20. Tests

Targeted governance tests cover valid role separation, unknown authority/boundary references, cross-school authority rejection, role overlap, approval provenance, pending-state isolation, and material-role evidence requirements: `14 passed`. Full local verification: `587 passed in 52.72s`. Package verification completed with `package verification passed`.

## 21. Active fingerprints

- Semantic: `256ba053b174a054226301f1b493e0e0c8f9f50e9f2976a72b8045dbf6ed6131`.
- Presentation: `2f1d3866638074485351ada0c6a9aaa9bd1acd916f65973ca2b319a75b99b91d`.

Candidate-only assets do not enter either active bundle.

## 22. Mapping isolation

`mapping_proposal_registry.proposals` remains empty. `mapping_v2_candidate_registry.candidates` remains empty. Proposed PRIMARY_EVIDENCE remains 0; approved Semantic Mechanisms and Mappings remain 0. Legacy remains 14/14 `NO_MAPPING / NO_PORT`. No user birth data, Golden Profile, or Renderer output informed the review.

## 23. Decisions required

D1, D2, and D3 remain independent Product Owner gates. D3 may now be approved, deferred, rejected, or returned for revision. Approval would enable only future P004 semantic-mechanism research within the selected method; it would not authorize PRIMARY_EVIDENCE, Mapping, Primitive state, production behavior, or a scientific-truth claim.

```text
Semantic Core Foundation: FROZEN
Semantic Knowledge Governance: FROZEN / REUSABLE
P004 Astrology Methodology Candidates: 1
Hellenistic Candidate: PROPOSED
Evidence Symmetry: PASS
Authority Purity: PASS
Materiality Audit: PASS
PO Approval Provenance: PASS
D3 Readiness: READY
D1: PENDING
D2: PENDING
D3: PENDING
P004 Astrology High: BLOCKED_BY_D3_AND_DIRECTION_EVIDENCE
P004 Astrology Low: NO_DEFENSIBLE_MECHANISM
Proposed PRIMARY_EVIDENCE: 0
Approved Semantic Mechanisms: 0
Mapping Proposals: 0
Approved Mappings: 0
Next Gate: PRODUCT_OWNER_D3_DECISION
```
