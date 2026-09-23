# C2 Mapping Double-Counting and Fact Dominance Report

## Evidence-root finding

Every active mapping rule emits flattened `fact_refs`; none declares a stable rule-level `canonical_fact_ref` or `evidence_root`. This prevents C1 Multi-Context Promotion from proving that two context labels are independently rooted.

```text
Affected rules: 14 / 14
EVIDENCE_ROOT_AMBIGUOUS: 14 major findings
```

## Duplication clusters

| Cluster | Rules | Classification | Risk | Severity | Recommended disposition |
|---|---|---|---|---|---|
| DC-01 | BZ-C2B-02, BZ-C2B-06, BZ-C2B-07 | same-root duplication | The same 印/官 two-group condition can feed P002, P005, and P006 without a root/owner split. | major | split |
| DC-02 | BZ-C2B-03, BZ-C2B-05 | exact duplication | Identical 食伤 + 财 condition feeds P002 low and P004 high; `work` overlaps. | major | split |
| DC-03 | BZ-C2B-01, BZ-C2B-03, BZ-C2B-05 | semantic duplication | Shared 食伤 facts can be repeatedly interpreted as judgement, change preference, and action. | major | rewrite |
| DC-04 | AS-C2B-01, AS-C2B-05 | exact duplication | The identical Sun–Mars aspect family feeds P001 high and P004 high, violating the approved distinction between judgement ownership and action initiation. | major | split |

No reviewed cluster is currently countable as legitimate independent multi-context support, because no cluster can establish distinct canonical fact roots and context origins.

## Fact dominance analysis

| System | Finding |
|---|---|
| Bazi | Each activated two-pillar rule can become a global state in the current resolver. Two pillars increase quantity but do not establish two independent representative contexts. |
| Astrology | One qualified aspect rule can become a global state. Orb-band salience does not establish C1 global candidate eligibility. |

```text
SINGLE_FACT_DOMINANCE_RISK: 14 major findings
CONTEXT_PROMOTION_BYPASS: 14 critical findings
```

## Contradiction handling

- BZ-C2B-02 and BZ-C2B-03 can produce P002 high and low with an overlapping `work` context. Current resolution can make a global `mixed`; C1 requires scope, source quality, modifiers, fact assurance, and roots to be reviewed first.
- AS-C2B-02 and AS-C2B-03 address different contexts (`pressure` and `change`). They are contextual variation, not global mixed.
- No arithmetic voting or cancellation is accepted as a C2 disposition.
