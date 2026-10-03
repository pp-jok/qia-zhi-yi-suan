# C2-SM P004 Bazi Neutral Relation Fact Report

Date: 2026-10-03

## Existing shape

`BaziRelationFact` transports four fields:

```text
relation_type
participant_refs
source_pillars
rule_version
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

The policy is candidate-only and inactive. An explicitly injected candidate
provider can emit the relation, but the default calculation service does not
construct or activate that provider.

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

## Provider boundary

- `CandidateNeutralRelationBaziCalculator` composes a caller-supplied Bazi
  calculator and emits versioned relations only when explicitly selected.
- Visible and hidden Ten-God references must resolve to the same governed
  subject catalogue; unknown kinds, bad indices, and pillar mismatches fail
  closed.
- Existing unrelated relation families are preserved. A pre-existing governed
  relation is rejected so two authorities cannot silently compete.
- `ChartCalculationService`, CLI construction, Evidence Roots, and semantic
  activation registries remain unchanged.

## Root readiness

The candidate family is reproducibly emitted under explicit injection and its
Ten-God join boundary is enforced. It is therefore ready for a separate
Evidence Root proposal review, but it is not added to permitted Evidence Root
sources in this change. No Root is proposed or approved.

```text
Neutral Relation Candidate Implementation:
PASS

Canonical Family Emitted:
CANDIDATE_ONLY_ON_EXPLICIT_INJECTION

Root Ready:
READY_FOR_PROPOSAL_REVIEW_ONLY
```
