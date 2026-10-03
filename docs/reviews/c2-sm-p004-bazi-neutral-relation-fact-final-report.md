# C2-SM P004 Bazi Neutral Relation Fact Final Report

Date: 2026-10-03

## Result

Track B delivers a candidate provider for raw `five_element_controls`
derivation while deliberately withholding Evidence Root and production
authority.

| Gate | Result | Evidence |
|---|---|---|
| Project-owned lookup | `PASS` | Versioned candidate contract defines ten stems and five control pairs. |
| School neutrality | `PASS` | Output is raw element relation, independent of Dao-Shi or any personality meaning. |
| Direction semantics | `PASS` | Participant 0 is controller; participant 1 is controlled. |
| Stable subject refs | `PASS_CANDIDATE` | Visible and hidden templates are deterministic. |
| Stable ordering | `PASS` | Generator uses canonical relation/ref/pillar ordering. |
| Deduplication | `PASS` | Relation identity is emitted once. |
| Prohibited fields | `PASS` | Methodology and semantic fields are excluded by model and contract. |
| Provider emission | `PASS_CANDIDATE` | Explicit provider decorator emits immutable facts; default runtime remains unchanged. |
| Ten-God join conformance | `PASS` | Visible/hidden kind, governed ref, index, and source pillar are enforced. |
| Emitted rule provenance | `PASS` | `rule_version: wuxing-control-v1` survives codec round-trip. |
| Evidence Root readiness | `PROPOSAL_REVIEW_ONLY` | No Root is created or approved by this engineering change. |

## Tests

The focused tests cover all five control pairs, direction, deterministic repeatability, canonical ordering, deduplication, visible/hidden refs, unknown-stem rejection, and methodology-field exclusion. They do not test any personality or Dao-Shi outcome.

```text
Neutral Bazi Relation Facts:
CANDIDATE_PROVIDER_AVAILABLE_NOT_ACTIVATED

deterministic_facts.bazi.relations:
CANDIDATE_EMITTED_ON_EXPLICIT_INJECTION

Evidence Root Proposal:
NOT_CREATED
```
