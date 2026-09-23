# C2 Product Owner Decision Packet

## Status

**C2 HIGH-LEVEL POLICY DECISIONS: APPROVED.** The Product Owner approved D1–D6 on 2026-09-22. This packet preserves the original rationale. Rule-level dispositions are still **AWAITING PRODUCT OWNER DECISION** and no mapping change is authorized.

## Cross-cutting decisions

### D1 — Evidence identity contract

Every future rule needs a canonical fact reference, a stable evidence root, provenance requirement, context origin, explicit exclusion, and a declared primary/modifier/contextualizer role. Current flattened fact references cannot prove C1 Multi-Context independence.

- Options: `rewrite` all retained rules with this contract; `remove` rules that cannot supply it; `needs_product_decision` for fact families with uncertain ownership.
- Recommendation: **rewrite as a prerequisite**. This is a future mapping-v2 contract decision, not a request to create v2 now.

### D2 — Local evidence must not resolve global state

All 14 current rules can feed active direct global-state resolution. C1 allows only explicit qualified global evidence or independently rooted, representative, same-direction multi-context candidate evidence.

- Options: `re-scope` all future mappings to local candidate evidence; `remove` mappings that cannot be scoped; `needs_product_decision` for a narrowly defined explicit-global fact class.
- Recommendation: **re-scope**. No current rule is approved as an explicit global fact.

### D3 — P001/P004 ownership

BZ-C2B-01 and AS-C2B-01 currently target P001 using conditions with action/output content; BZ-C2B-05 and AS-C2B-05 target P004.

- Options: `rewrite` rules to prove judgement ownership versus action initiation; `split` a fact family only if independent semantic conditions exist; `remove` an unsupported P001 mapping.
- Recommendation: **rewrite BZ-C2B-01 and AS-C2B-01; retain P004 only after explicit initiation semantics are supplied.**

### D4 — P002/P006 ownership

BZ-C2B-02, BZ-C2B-07, AS-C2B-02, and AS-C2B-07 conflate stability/predictability preference with structure/organization.

- Options: `rewrite` with preference-versus-method criteria; `split` a fact family only with separate fact conditions; `no-mapping` where neither criterion is defensible.
- Recommendation: **rewrite; do not infer P002 from organization or P006 from stability.**

### D5 — P003 and P005 evidence eligibility

BZ-C2B-04 uses broad Ten-God presence as relationship evidence; BZ-C2B-06 and AS-C2B-06 do not distinguish affect regulation from expression/structure.

- Options: `no-mapping`; `re-scope` to a qualified local expression candidate; `rewrite` with a direct semantic bridge.
- Recommendation: **no-mapping for BZ-C2B-04; re-scope or no-mapping for P005 pending approved evidence semantics.**

### D6 — Astrology aspect role

Every astrology rule accepts conjunction, sextile, square, trine, and opposition for the same Primitive direction. The current expression/tension metadata does not determine direction.

- Options: `split` primary condition from modifier-only aspect role; `rewrite` each rule with aspect-specific semantic criteria; `no-mapping` for aspect families without a defensible direction.
- Recommendation: **split and treat aspect type as modifier/contextualizer unless an approved direction bridge is supplied.**

## Rule disposition sheet

| Rule ID | Recommended disposition | Product Owner decision |
|---|---|---|
| BZ-C2B-01 | rewrite | [ ] keep [ ] rewrite [ ] split [ ] re-scope [ ] remove [ ] needs_product_decision |
| BZ-C2B-02 | rewrite | [ ] keep [ ] rewrite [ ] split [ ] re-scope [ ] remove [ ] needs_product_decision |
| BZ-C2B-03 | rewrite | [ ] keep [ ] rewrite [ ] split [ ] re-scope [ ] remove [ ] needs_product_decision |
| BZ-C2B-04 | no-mapping | [ ] keep [ ] rewrite [ ] split [ ] re-scope [ ] remove [ ] no-mapping [ ] needs_product_decision |
| BZ-C2B-05 | rewrite | [ ] keep [ ] rewrite [ ] split [ ] re-scope [ ] remove [ ] needs_product_decision |
| BZ-C2B-06 | re-scope or no-mapping | [ ] keep [ ] rewrite [ ] split [ ] re-scope [ ] remove [ ] no-mapping [ ] needs_product_decision |
| BZ-C2B-07 | rewrite | [ ] keep [ ] rewrite [ ] split [ ] re-scope [ ] remove [ ] needs_product_decision |
| AS-C2B-01 | rewrite | [ ] keep [ ] rewrite [ ] split [ ] re-scope [ ] remove [ ] needs_product_decision |
| AS-C2B-02 | rewrite | [ ] keep [ ] rewrite [ ] split [ ] re-scope [ ] remove [ ] needs_product_decision |
| AS-C2B-03 | rewrite | [ ] keep [ ] rewrite [ ] split [ ] re-scope [ ] remove [ ] needs_product_decision |
| AS-C2B-04 | re-scope or rewrite | [ ] keep [ ] rewrite [ ] split [ ] re-scope [ ] remove [ ] needs_product_decision |
| AS-C2B-05 | rewrite | [ ] keep [ ] rewrite [ ] split [ ] re-scope [ ] remove [ ] needs_product_decision |
| AS-C2B-06 | re-scope or no-mapping | [ ] keep [ ] rewrite [ ] split [ ] re-scope [ ] remove [ ] no-mapping [ ] needs_product_decision |
| AS-C2B-07 | rewrite | [ ] keep [ ] rewrite [ ] split [ ] re-scope [ ] remove [ ] needs_product_decision |

## Approved policy closure

```text
D1 Evidence identity contract: APPROVED
D2 Local-to-global boundary: APPROVED
D3 P001/P004 ownership: APPROVED
D4 P002/P006 ownership: APPROVED
D5 P003/P005 eligibility: APPROVED
D6 Astrology aspect role: APPROVED
```

## Approval boundary

The next allowed phase is **C2-R Rule-Level Remediation**. Even if all rule dispositions are approved, the subsequent candidate mapping implementation needs separate authorization. It must not activate runtime, modify the v0.3 semantic bundle, or enter C3 without its own gate.
