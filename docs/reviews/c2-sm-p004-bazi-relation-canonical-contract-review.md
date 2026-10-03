# C2-SM P004 Bazi Relation Canonical Contract Review

Date: 2026-10-04

## Decision

`deterministic_facts.bazi.relations` is recognized as a canonical optional fact
family under `bazi-relation-canonical-v1`. Its currently allowed vocabulary is:

```text
relation_type: five_element_controls
participant 0: controller
participant 1: controlled
arity: 2
rule_version: wuxing-control-v1
```

The rule table is project-owned and versioned: wood controls earth, earth
controls water, water controls fire, fire controls metal, and metal controls
wood. This is a raw directed structural relationship that remains useful if
Dao-Shi is never implemented; it is therefore school-neutral at this fact
boundary.

## Identity, provenance, and order

Canonical identity and deduplication use
`(relation_type, participant_refs, rule_version)`. `source_pillars` is derived
provenance and validation data, not a second identity axis. Canonical relation
subsets are sorted by that same identity, producing deterministic codec order.

The validator resolves actual stems, recomputes the control direction, accepts
only the approved rule version, checks exact source pillars, rejects duplicate
identity, and rejects unstable canonical order. The closed dataclass and
contract prohibit effective control, strength, rescue, exception, Dao-Shi,
personality, Primitive state, and direction fields.

## Authority separation

The contract is canonical; `CandidateNeutralRelationBaziCalculator` is only a
conformance reference provider and remains absent from the default runtime.
Empty relation tuples and unrelated legacy relation families remain valid. No
Bazi methodology or payload schema version is bumped because default output is
unchanged and the family is optional.

```text
five_element_controls:
CANONICAL

Canonical Provider Authority:
CONFORMANCE_REFERENCE_ONLY

Default Production Provider:
UNCHANGED
```
