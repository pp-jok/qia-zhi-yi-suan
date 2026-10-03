# C2-SM P004 Bazi Neutral Relation Fact Report

Date: 2026-10-03

## Existing shape

`BaziRelationFact` already transports three fields:

```text
relation_type
participant_refs
source_pillars
```

The codec preserves those fields and calculation validation checks non-empty values and pillar provenance. Before this work, however, no project-owned policy generated relations, participant order was undefined, and the model was only a shape.

## Candidate policy

`candidates/calculation-v1/bazi_neutral_relation_contract_v1.yaml` now defines one minimal relation:

```text
relation_type: five_element_controls
participant_refs[0]: controller
participant_refs[1]: controlled
rule_version: wuxing-control-v1
```

It contains the ten-stem element lookup and five neutral control pairs:

```text
wood -> earth
earth -> water
water -> fire
fire -> metal
metal -> wood
```

The policy is candidate-only, inactive, and explicitly not emitted by the calculation service.

## Stable subject references

Visible stems use:

```text
{pillar}.stem
```

Hidden stems use their canonical order within each pillar:

```text
{pillar}.hidden_stem.{index}
```

The pure generator derives relations from actual chart stem subjects, sorts them canonically, removes duplicate identities, orders source pillars by year/month/day/hour, and fails closed on unknown stems or duplicate hidden-stem provenance.

## Canonical boundary

The relation says only that one stem's element controls another stem's element. It contains none of:

```text
operative
qualification
rescue
effective
strength_score
dao_shi
primitive_direction
```

It does not reference the Dao-Shi Claim or any Semantic Knowledge asset.

## Remaining gaps

- `ChartCalculationService` does not invoke the generator.
- No provider merges these candidate relations into its emitted deterministic facts.
- Existing `TenGodFact.subject_ref` is required to be non-empty but is not yet constrained to the candidate subject-reference convention.
- Calculation-rule version is governed by the candidate policy, not yet carried through an emitted provider provenance envelope.
- Backward-compatible provider integration and independent calculation comparison have not been completed.

## Root readiness

Because the canonical family is not emitted and joinability to Ten-God instances is not enforced, `deterministic_facts.bazi.relations` is not added to permitted Evidence Root sources. No Root is proposed.

```text
Neutral Relation Candidate Implementation:
PASS

Canonical Family Emitted:
NO

Root Ready:
NO
```
