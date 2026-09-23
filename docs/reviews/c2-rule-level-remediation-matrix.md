# C2-R Rule-Level Remediation Matrix

## Disposition basis

All recommendations apply the approved C2 D1–D6 policy. All fourteen listed dispositions are now **APPROVED — NO LEGACY MIGRATION (NO_MAPPING / NO_PORT)**. Current runtime remains untouched. `UNKNOWN_ROOT` is audit-visible but aggregation-, promotion-, and validation-ineligible. Every current rule has a local context; none is approved as `GLOBAL_ELIGIBLE`.

| Rule | Current source facts | Primitive / direction / context | Root and identity result | Owner, direction, strength result | Aspect role / duplication result | Recommended disposition |
|---|---|---|---|---|---|---|
| BZ-C2B-01 | 比肩/劫财 + 食神/伤官; ≥2 visible/hidden pillars; environment | P001 / high / decision, work | UNKNOWN_ROOT; canonical derivative but no stable root ID | P001 judgement ownership not proven; direction unsupported; technical moderate only | N/A; DC-03 semantic overlap | NO_MAPPING |
| BZ-C2B-02 | 正印/偏印 + 正官/七杀; ≥2 pillars; environment | P002 / high / pressure, work | UNKNOWN_ROOT | P002 preference not separated from P006 method; direction unsupported; technical moderate only | N/A; DC-01 same-root risk | NO_MAPPING |
| BZ-C2B-03 | 食神/伤官 + 正财/偏财; ≥2 pillars; environment/counterweight | P002 / low / change, work | UNKNOWN_ROOT | Change preference not established; technical moderate only | N/A; DC-02 exact and DC-03 semantic overlap | NO_MAPPING |
| BZ-C2B-04 | Broad two-group Ten-God presence; ≥2 pillars; environment | P003 / high / relationship | UNKNOWN_ROOT | Relationship label does not establish relational attunement; technical moderate only | N/A; no valid primary mechanism | NO_MAPPING |
| BZ-C2B-05 | 食神/伤官 + 正财/偏财; ≥2 pillars; environment | P004 / high / work, action | UNKNOWN_ROOT | Action initiation not established; technical moderate only | N/A; DC-02 exact and DC-03 semantic overlap | NO_MAPPING |
| BZ-C2B-06 | 正印/偏印 + 正官/七杀; ≥2 pillars; environment | P005 / high / pressure | UNKNOWN_ROOT | P005 regulation mechanism absent; technical moderate only | N/A; DC-01 same-root risk | NO_MAPPING |
| BZ-C2B-07 | 正印/偏印 + 正官/七杀; ≥2 pillars; environment | P006 / high / work, decision | UNKNOWN_ROOT | P006 ordering method not separated from P002; technical moderate only | N/A; DC-01 same-root risk | NO_MAPPING |
| AS-C2B-01 | Sun/Mars placement + Sun–Mars aspect ≤8; optional dignity/angle | P001 / high / decision, work | UNKNOWN_ROOT; deterministic placement/aspect but no root ID | P001 judgement ownership not proven; orb band is technical only | Aspect gate/modifier only; DC-04 exact overlap | NO_MAPPING |
| AS-C2B-02 | Saturn placement + Saturn–Sun aspect ≤8 | P002 / high / pressure | UNKNOWN_ROOT | P002 preference not separated from P006; orb band is technical only | Aspect gate/modifier only; no approved primary mechanism | NO_MAPPING |
| AS-C2B-03 | Uranus placement + Uranus–Sun aspect ≤8 | P002 / low / change | UNKNOWN_ROOT | Reverse preference semantics not proven; orb band is technical only | Aspect gate/modifier only; no approved primary mechanism | NO_MAPPING |
| AS-C2B-04 | Moon/Venus placement + Moon–Venus aspect ≤8 | P003 / high / relationship | UNKNOWN_ROOT | Relational attunement not separated from affection/emotionality; orb band technical only | Aspect gate/modifier only; relationship-local if ever remapped | NO_MAPPING |
| AS-C2B-05 | Mars placement + Mars–Sun aspect ≤8 | P004 / high / work, action | UNKNOWN_ROOT | Action initiation not proven; orb band technical only | Aspect gate/modifier only; DC-04 exact overlap | NO_MAPPING |
| AS-C2B-06 | Moon placement + Moon–Mercury aspect ≤8 | P005 / high / pressure, relationship | UNKNOWN_ROOT | Emotion-related is not affect regulation; orb band technical only | Aspect gate/modifier only; no P005 primary mechanism | NO_MAPPING |
| AS-C2B-07 | Mercury placement + Mercury–Saturn aspect ≤8 | P006 / high / work, decision | UNKNOWN_ROOT | P006 ordering method not separated from P002/cognition style; orb band technical only | Aspect gate/modifier only; no approved primary mechanism | NO_MAPPING |

## Rule-level findings

### Context result

All current context labels are valid v1 taxonomy values, but each rule currently feeds direct global-state resolution. Under D2, all fourteen must be contextual evidence only if a future mapping is approved. Because every recommended disposition is `NO_MAPPING`, no proposed replacement emits local or global evidence.

### Evidence identity result

All fourteen current rules have deterministic source families but no `canonical_fact_ref`, `evidence_root_id`, or `evidence_instance_id`. They therefore fail D1 independence and are fail-closed. No new independent root can be created by mapping rule, context, aspect wording, or renderer text.

### Exclusions and counter-conditions

No current rule carries a C1-compatible explicit exclusion sufficient to survive remediation. BZ-C2B-03 has a contextualizing counterweight, but it does not supply an exclusion or an evidence-root identity.

### Replacement design

For each of the fourteen rules: retain its canonical chart fact family as a non-mapped audit subject; emit no Primitive Evidence; do not create a modifier or contextualizer in the absence of an approved primary semantic mechanism. The legacy formulation has resolution `RESOLVED_BY_NON_MIGRATION`; its active-v1 runtime defect remains `OPEN_RUNTIME_LEGACY`; any replacement is `V2_REDESIGN_REQUIRED` and `IMPLEMENTATION_PENDING`. A later approved mapping candidate may only be designed with D1 fields, a C1 owner bridge, explicit exclusions, contextual-only output, and independently auditable roots.

## Primitive coverage after proposed remediation

| Primitive | Primary Evidence Rules | Modifier Rules | Contextualizer Rules | No Mapping recommendations |
|---|---:|---:|---:|---:|
| P001 | 0 | 0 | 0 | 2 |
| P002 | 0 | 0 | 0 | 4 |
| P003 | 0 | 0 | 0 | 2 |
| P004 | 0 | 0 | 0 | 2 |
| P005 | 0 | 0 | 0 | 2 |
| P006 | 0 | 0 | 0 | 2 |

`P005 Primary Evidence Rules = 0` is intentional and permitted by approved D5. The matrix does not seek numeric balance.
