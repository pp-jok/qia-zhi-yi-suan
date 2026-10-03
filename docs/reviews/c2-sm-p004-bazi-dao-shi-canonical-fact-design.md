# C2-SM P004 Bazi Dao-Shi Canonical Fact Design

Date: 2026-10-03

## Design objective

Provide sufficient neutral inputs for a future methodology to evaluate 倒食. Do not compute 倒食 in the fact layer.

## Existing facts

- `BaziPillar`: heavenly stem and earthly branch by year/month/day/optional hour.
- `HiddenStemsFact`: pillar plus hidden stems.
- `TenGodFact`: `subject_ref`, `ten_god`, `source_pillars`, and `source_kind`.
- `BaziRelationFact`: generic shape with `relation_type`, `participant_refs`, and `source_pillars`.
- Candidate `DayMasterEnvironmentFact`: day-master stem/element, month branch, neutral four-season label, provenance, and table version. Its explicit limitation excludes strength, favorable elements, patterns, transits, and outcomes.

`BaziRelationFact` is a data shape, not proof that Dao-Shi-required relations are computed. The repository has only a non-production deterministic-table template and no project-owned `bazi_deterministic_tables_v1.yaml` containing relation rules.

## Missing neutral facts

The smallest missing capability is a governed, deterministic relation output using the existing `BaziRelationFact` boundary:

```yaml
proposed_contract: deterministic_facts.bazi.relations
implementation_status: NOT_IMPLEMENTED
minimum_identity:
  relation_type: <canonical school-neutral relation id>
  participant_refs: [<stable controller subject ref>, <stable controlled subject ref>]
  source_pillars: [<participating pillar provenance>]
required_governance:
  - versioned bazi_relation vocabulary entries
  - project-owned deterministic relation table or equivalent exact algorithm
  - stable subject-reference specification shared with TenGodFact
  - direction/order semantics for participant_refs
  - validation, ordering, uniqueness, provenance, and codec tests
  - independent calculation-envelope confirmation where required
```

Candidate relation types may represent raw element generation/control and mechanically present stem/branch combinations. Exact identifiers are intentionally not invented in this review.

## Facts that must not exist

The following are methodology judgements and must not be admitted as canonical identities:

- `qualification_status` for 倒食;
- `operative_eating_god_status`;
- strength, 得令/失令, 当权, pattern, 顺逆, 清浊, or 制化 outcome;
- `wealth_rescue_status` or “effective rescue” Boolean;
- `combination_exception_status` or “exception resolved” Boolean;
- direct `dao_shi_established`/`inverted_food_active` facts;
- P004 direction or Primitive state.

## Calculation gap and implementation gate

Before a Root can reference `deterministic_facts.bazi.relations`, the project must implement and verify the exact neutral calculation above. Merely having the Python dataclass or schema section is insufficient. Until then:

```text
Canonical Fact Proposal:
DESIGN_ONLY_NOT_IMPLEMENTED

Canonical Fact Boundary:
BLOCKED_BY_CANONICAL_FACT_DESIGN
```
