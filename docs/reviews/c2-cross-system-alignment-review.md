# C2 Cross-System Alignment Review

## Preconditions and review rule

This review follows the separate Bazi and astrology audits. A relationship may be `validation` only when sources are independent, the Primitive owner is the same, direction is the same, contexts are comparable, and evidence roots are independently auditable. Current candidates lack stable rule-level evidence roots and have unresolved semantic ownership; no current runtime “validation” label is approved as C2 validation.

## Coverage matrix

| Primitive | Bazi Rule Count | Astrology Rule Count | Context Coverage | High Evidence | Low Evidence | Gaps |
|---|---:|---:|---|---:|---:|---|
| P001 | 1 | 1 | decision, work | 2 | 0 | D1 ownership and root proof |
| P002 | 2 | 2 | pressure, work, change | 2 | 2 | preference bridge; overlapping Bazi conflict |
| P003 | 1 | 1 | relationship | 2 | 0 | response/coordination semantics; constrained global eligibility |
| P004 | 1 | 1 | work, action | 2 | 0 | initiation versus generic energy/output |
| P005 | 1 | 1 | pressure, relationship | 2 | 0 | affect regulation versus expression/structure |
| P006 | 1 | 1 | work, decision | 2 | 0 | organization method versus predictability preference |

## Alignment assessment

| Primitive / rule pairing | Current runtime relation | C2 relation | Reason |
|---|---|---|---|
| P001 BZ-C2B-01 / AS-C2B-01 | validation | unresolved | Exact contexts/direction but both have unresolved P001/P004 ownership and no auditable roots. |
| P002 high BZ-C2B-02 / AS-C2B-02 | contextualization | unresolved | Shared pressure but Bazi adds work; P002/P006 ownership remains unresolved. |
| P002 low BZ-C2B-03 / AS-C2B-03 | contextualization | unresolved | Shared change but Bazi adds work; neither rule establishes explicit reverse-preference semantics. |
| P002 cross-direction pairs | non_comparable | non_comparable | High and low conditions use different contexts; no vote or cancellation is allowed. |
| P003 BZ-C2B-04 / AS-C2B-04 | validation | unresolved | Same relationship context/direction, but Bazi has no relational-response source bridge. |
| P004 BZ-C2B-05 / AS-C2B-05 | validation | unresolved | Same work/action context/direction, but action initiation semantics are not established. |
| P005 BZ-C2B-06 / AS-C2B-06 | contextualization | unresolved | Pressure overlaps; relationship is additional only on astrology; P005 meaning remains unproven. |
| P006 BZ-C2B-07 / AS-C2B-07 | validation | unresolved | Same work/decision context/direction, but P002/P006 separation is unresolved. |

## Cross-system findings

- **Validation is not voting.** The active runtime currently calls exact, same-direction context pairs validation, but it does not prove C1 source-root independence or approved semantic ownership. Finding: `CROSS_SYSTEM_VALIDATION_PREMATURE` for P001, P003, P004, and P006 (4 major findings).
- **non_comparable is used.** Cross-direction P002 pairs remain non-comparable because their contexts differ; no neutralization is inferred.
- **No correction relation is established.** Neither system currently supplies an approved rule that corrects another system's semantic conclusion.
- **No approved tension relation is established.** Context difference is not automatically tension or mixed.

## Rule density, collapse, and positive bias

- Both systems have the same raw count distribution: P002 has two rules; each other Primitive has one. Equal counts do not establish equal evidence quality.
- Each system has six high-direction rules and one low-direction rule. Combined: 12 high, 2 low. Finding: `POSITIVE_BIAS` major; no 50/50 target is implied.
- Heterogeneous Bazi and astrology signals repeatedly map high to P001, P003, P004, P005, and P006. Because all those high paths can become global, there is a material `MAPPING_COLLAPSE` risk (major).
- `RULE_DENSITY_BIAS` is also major: P002 is the only Primitive with bidirectional coverage, while the other five lack explicit low evidence.

## Cross-system outcome

```text
Approved C2 validations: 0
Conditional validation candidates: 0
Unresolved alignment decisions: 6 Primitive-level decisions
Non-comparable relationships retained: 2 P002 cross-direction pairings
```
