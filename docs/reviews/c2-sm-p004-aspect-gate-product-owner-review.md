# C2-SM P004 Astrology Aspect Gate - Product Owner Review

## Decision subject

`SMC-AS-ASPECT-ELIGIBILITY-GATE-P004-V1` is a proposed Astrology `RULE_GATE`, supported by the approved fact-identity Root `ER-AS-ASPECT-INSTANCE-V1`.

It asks only whether an identified aspect instance may be admitted to a later P004 evidence review. It does not state that the aspect is positive, negative, strong, weak, activating, restraining, or sufficient for any Primitive result.

## What the mechanism solves

It creates an auditable admission boundary: `identified aspect instance -> later evidence review eligibility`. The Root identifies bodies, aspect type, and orb. The Gate preserves that identity and prevents later consumers from treating an unrecorded aspect claim as evidence.

## What it does not solve

It does not answer P004's question, “When and how is concrete action started and advanced?” It cannot establish P004 high, low, mixed, unknown, magnitude, or a global state. It does not map Mars, Saturn, or any aspect type to action.

`RULE_GATE` is the correct role because its Role Authority grants evidence admission only; `mapping_origin`, `primitive_direction`, and `primitive_state` are all false. It is not `PRIMARY_EVIDENCE` because no project-owned direction bridge shows that aspect identity directly answers action initiation rather than energy, conflict, assertion, judgement ownership, or other neighboring meanings.

## Audit result

- Evidence Root is approved and identifies a deterministic fact instance.
- P004 ownership is preserved: no judgement ownership, predictability, or organizational-method claim is made.
- `asserts_primitive_state: false` and no direction is present.
- The candidate is not runtime-loaded and has no Mapping eligibility.
- Legacy review found Sun-Mars -> P004-high to be `NO_MAPPING`; this Gate does not reintroduce that direction or source-target-direction rule.
- No Golden Sample, renderer wording, or runtime output is used as origin.

## Decision options

### D1 - `SMC-AS-ASPECT-ELIGIBILITY-GATE-P004-V1`

| Option | Meaning | Consequence |
|---|---|---|
| Approve as RULE_GATE | Approve the non-directional admission boundary only. | The candidate becomes an approved Gate, but Mapping-eligible mechanisms remain unchanged at 0. |
| Defer | Retain the candidate as proposed pending further review. | No behavior changes. |
| Reject | Reject this proposed Gate. | No behavior changes; a future replacement would need a new review. |

**Recommendation: APPROVE_AS_RULE_GATE.** The mechanism is narrow, Root-bound, and explicitly prevents the unsupported aspect-to-direction shortcut. Even if approved, it cannot create a Mapping, P004 direction, Primitive state, or runtime activation. A separately approved `PRIMARY_EVIDENCE` mechanism would still be required before Mapping design can begin.

## Product Owner record

```text
D1 decision: [ ] approve as RULE_GATE  [ ] defer  [ ] reject
Decision reference: ____________________
Date: ____________________
Rationale: ____________________
```
