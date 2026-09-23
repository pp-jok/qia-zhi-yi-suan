# C1 Primitive Semantic Review — Approved

## Scope

This is an audit only. No ontology, mapping, state, or presentation asset was modified.

| Primitive | Current high / low boundary | Context and exclusion audit | C1 finding |
|---|---|---|---|
| P001 autonomy | self-directed judgement / external framework reliance | decision and work evidence must not imply affiliation or action | Needs explicit excluded-meaning catalog before v2 |
| P002 stability | predictable structure / openness to change | scoped change and pressure/work evidence must not become global | Needs scope precedence examples |
| P003 affiliation | responsive coordination / independent relating | relationship evidence must not become autonomy evidence | Neighbor boundary with P001 required |
| P004 action | initiation / observation-preparation | action is distinct from autonomy | Neighbor boundary with P001 required |
| P005 affect | structured regulation / open affect flow | pressure context must not imply relationship style | Mixed and unknown prose definitions required |
| P006 structure | order and organization / flexibility | work structure must not imply responsibility or stability | Neighbor boundaries with P002 required |

## Cross-cutting findings

- High/low wording is frozen presentation routing, not a complete semantic-definition artifact.
- `mixed` and `unknown` are correctly fail-closed in runtime but lack per-Primitive reviewed definitions.
- Context vocabulary exists, but global-promotion and exclusion rules need explicit C1 review.

## Decision

The Product Owner approved the six-Primitive semantic cards and D1–D4 on 2026-09-22: D1 Option A, D2 Option A, D3 Option A, and D4 Multi-Context Promotion. Candidate implementation of `primitive_ontology_v2.yaml` and its separate context-promotion policy is now allowed.

Detailed cards, collision severities, decision rationale, and approval record are recorded in the companion C1 documents. Review status: **C1 APPROVED**. C2 Mapping Review remains a separate, unopened gate; no runtime activation or higher-order semantic layer is authorized.
