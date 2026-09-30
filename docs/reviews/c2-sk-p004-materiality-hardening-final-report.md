# C2-SK P004 Materiality Hardening Final Report

## 1. Actual baseline

Remote `main` was rechecked before implementation at `027e05cbf34d86b51ef867ac816d65028c4967d9` (`feat: validate P004 Hellenistic method candidate`). D1, D2, and D3 were all pending.

## 2–3. Problem and old taxonomy weakness

The first materiality audit correctly blocked direct condition→P004 direction shortcuts, but it then classified many techniques as `QUALITY_ONLY` or `PROMINENCE_ONLY` from method-role evidence. That conflated “no direct P004 bridge has been found” with “the technique has been affirmatively limited to a non-P004 semantic layer.”

The generic condition-inventory Claim established method membership and absence of automatic direction. It did not prove permanent non-materiality. The old Loader checked reference existence but not whether the evidence class was semantically compatible with the selected role.

## 4–6. New taxonomy, thresholds, and default

The candidate contract now defines four evidence classes and a closed mapping:

- `DIRECT_P004_MATERIALITY` → required, modifier, contextualizer, or counterevidence.
- `DIRECT_NON_P004_BOUNDARY` → quality-only, prominence-only, or scoped not-P004.
- `METHOD_ROLE_ONLY` → unresolved.
- `INSUFFICIENT` → unresolved.

Default rule: method membership without direct materiality or direct exclusion evidence is `UNRESOLVED`. Missing evidence is never low, counterevidence, quality-only, prominence-only, or not-P004.

## 7–8. Reclassification and inventory result

Sect, essential dignity, triplicity, bounds, reception, house/angularity, solar phase, visibility, speed, planetary direction, phasis, bonification, maltreatment, overcoming, and aspects are now `UNRESOLVED / METHOD_ROLE_ONLY`. Mars identity remains `UNRESOLVED / INSUFFICIENT`.

Application/perfection remains scoped `NOT_P004 / DIRECT_NON_P004_BOUNDARY` only for automatic transfer from horary event development/fulfilment into natal P004 personality direction. The classification does not deny possible natal relevance under future evidence.

Final distribution: 16 unresolved entries and one scoped not-P004 entry; zero P004 material roles.

## 9. Candidate contract changes

`contract_version` and `registry_version` advance to the materiality-semantics v2 identifiers while schema filenames and schema identifiers remain v1. Each audit item now requires `materiality_basis` with evidence class, explicit scope, Source refs, and Claim refs.

## 10. Loader changes

The Loader now rejects:

- method-role-only or insufficient evidence used for a definitive non-P004 role;
- method-role-only evidence used for a material P004 role;
- direct non-P004 classifications without candidate-declared boundary Claims;
- direct P004 materiality whose Claims do not have P004-relevant ownership;
- unbound or unknown materiality Source/Claim refs;
- missing or blank materiality scope;
- `required_by_p004` on a non-material role.

`UNRESOLVED` is a first-class valid state and does not block a method candidate by default.

## 11. Tests

The targeted registry suite contains 22 passing tests; the combined governance/isolation suite contains 70 passing tests. Full local verification: `595 passed in 81.59s`. Independent wheel installation and CLI contract checks completed with `package verification passed`.

## 12–16. D3 gates

| Gate | Result | Reason |
|---|---|---|
| Evidence Symmetry | `PASS` | Major candidate/disposition evidence remains registry-backed. |
| Authority Purity | `PASS` | Method authority and boundary roles remain machine-separated. |
| Materiality Semantics | `PASS` | Evidence-class→role mapping prevents unknown collapse. |
| Materiality Completeness | `PASS` | Every identified technique has an evidence-calibrated classification, including legal unresolved states. |
| PO Approval Provenance | `PASS` | Approved status still requires a non-empty decision ref; proposed remains pending/null. |

## 17–22. Readiness and governance states

- D3 readiness: `D3_READY_FOR_PRODUCT_OWNER_DECISION`.
- Candidate validation: `READY_FOR_PO_REVIEW`.
- D1: `PENDING`.
- D2: `PENDING`; placement identity remains relevant to future Mars research.
- D3: `PENDING`; no approval is recorded.
- Astrology High: `BLOCKED_BY_D3_AND_DIRECTION_EVIDENCE`.
- Astrology Low: `NO_DEFENSIBLE_MECHANISM`.

Unresolved materiality does not block D3 because D3 selects a stable methodology boundary for continued research; it does not approve a complete P004 mechanism.

## 23–25. Isolation and fingerprints

- Proposed PRIMARY_EVIDENCE: 0.
- Approved Semantic Mechanisms: 0.
- Aspect RULE_GATE: proposed and unchanged.
- Mapping Proposals: 0.
- Mapping Candidates / Approved Mappings: 0.
- Legacy: 14/14 `NO_MAPPING / NO_PORT`.
- Golden/user birth/report fixtures: not used.
- Active semantic fingerprint: `256ba053b174a054226301f1b493e0e0c8f9f50e9f2976a72b8045dbf6ed6131`.
- Active presentation fingerprint: `2f1d3866638074485351ada0c6a9aaa9bd1acd916f65973ca2b319a75b99b91d`.

Self-audit found no confirmation-bias preservation: old definitive classifications were not retained for appearance; method role was separated from P004 role; generic condition Claims were not reused as universal exclusion proof; uncertainty is represented as unresolved; no new external search was conducted to defend the old taxonomy.

## 26. Next Product Owner decision

The next gate is D3: approve for continued semantic design, defer, reject, or request revision. Approval enables only controlled P004 materiality and mechanism research inside the methodology; it does not authorize PRIMARY_EVIDENCE, Mapping, Primitive state, production behavior, D1, D2, or a scientific-truth claim.

```text
Semantic Core Foundation: FROZEN
Semantic Knowledge Governance: FROZEN / REUSABLE
P004 Astrology Methodology Candidate: AMC-AS-P004-HELLENISTIC-NATAL-V1
Evidence Symmetry: PASS
Authority Purity: PASS
Materiality Semantics: PASS
Materiality Completeness: PASS
PO Approval Provenance: PASS
Candidate Validation: READY_FOR_PO_REVIEW
D1: PENDING
D2: PENDING
D3: PENDING
D3 Readiness: D3_READY_FOR_PRODUCT_OWNER_DECISION
P004 Astrology High: BLOCKED_BY_D3_AND_DIRECTION_EVIDENCE
P004 Astrology Low: NO_DEFENSIBLE_MECHANISM
Proposed PRIMARY_EVIDENCE: 0
Approved Semantic Mechanisms: 0
Mapping Proposals: 0
Approved Mappings: 0
Next Gate: PRODUCT_OWNER_D3_DECISION
```
