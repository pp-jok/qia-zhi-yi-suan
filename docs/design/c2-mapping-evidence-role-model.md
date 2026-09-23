# C2 Mapping Evidence Role Model

## Status and scope

This is a fresh-mapping design contract. It is not a runtime schema, YAML registry, or authorization to create Mapping v2. It applies after the approved rejection of all legacy rule formulations.

## Evidence roles

| Role | Can create Primitive Evidence? | Required basis | Permitted effect | Forbidden effect |
|---|---|---|---|---|
| `PRIMARY_EVIDENCE` | yes | An explicit Canonical Fact → Semantic Mechanism → target Primitive semantic-question chain | contextual evidence in an approved direction | direction from stereotype, aspect valence, or missing evidence |
| `MODIFIER` | no | Existing eligible Primary Evidence | strength, expression, confidence, tension, condition | creating high/low alone |
| `CONTEXTUALIZER` | no | Existing eligible Primary Evidence | context of expression only | determining high/low or global state |
| `COUNTER_EVIDENCE` | no independent activation | Explicit opposite answer to the same Primitive semantic question | qualified opposing evidence for later state resolution | treating absence as opposition |
| `EXCLUSION` | no | Rule eligibility condition | prevents a rule activation | acting as negative evidence |
| `RULE_GATE` | no | Deterministic fact eligibility check | requires a fact pattern, time scope, or availability condition | supplying Primitive meaning or direction |

`absence != counter evidence` is frozen. An evidence role never changes an evidence root.

## Primary-evidence admission test

A mechanism may be `PRIMARY_EVIDENCE` only if all answers are explicit and project-owned:

1. Which canonical fact(s) are required?
2. What semantic mechanism is asserted by those facts?
3. Why does that mechanism answer one target Primitive semantic question?
4. Why does it not instead belong to P001/P004, P002/P006, or P003/P005 neighbor axes?
5. What direction does the mechanism support, rather than merely fail to oppose?
6. Which contexts can express it, and why is it not global state?
7. What facts exclude or counter the mechanism?

Failure of any answer produces `NO_CURRENT_DEFENSIBLE_MAPPING`, not a partial Primary Evidence rule.

## Evidence identity model

```text
Canonical Fact
  → Evidence Root
    → Semantic Mechanism
      → Evidence Instance
```

Every future candidate rule must declare:

```text
canonical_fact_ref
evidence_root_strategy
semantic_mechanism_id
evidence_role
primitive_id
direction
context_scope
independence_policy
```

### Identity rules

- `canonical_fact_ref` identifies deterministic input facts, never provider prose, model interpretation, or renderer copy.
- `evidence_root_id` is derived exclusively from canonical fact identity. For a compound fact, the strategy must specify the canonical sub-fact set and its canonical ordering.
- `evidence_instance_id` may include mechanism, rule, and context, but it never creates a new independent root.
- If a root is unknown, the instance is audit-visible but aggregation-, promotion-, and validation-ineligible.
- Two mechanisms sharing a root declare `independent = false`; they cannot satisfy Multi-Context Promotion, validation, or independent counting through duplicate projection.

## Context and time contract

- Every admitted future mapping emits contextual Primitive Evidence by default.
- `global_eligible: true` requires explicit global-scope canonical evidence and can create only global candidate evidence; it never resolves Primitive State.
- Bazi hour-pillar-derived facts and astrology house/angle/MC/Ascendant facts require the time-sensitive fact gate.
- Stable-only facts cannot contain hour source, house, angle, MC, Ascendant, or house-cusp data.

## System-specific role constraints

### Bazi

- A single Ten God cannot be a direct Primitive direction shortcut.
- Visible/hidden provenance, pillar position, environment, and deterministic relations can participate only when an approved mechanism explains their combined semantic role.
- Day-master environment is descriptive context only unless a separate approved mechanism says otherwise.

### Astrology

- Planet, sign, and placement are not automatic Primary Evidence.
- Aspect is not Primitive direction. It is eligible only as `RULE_GATE`, `MODIFIER`, or interaction/expression/tension modifier attached to an already eligible mechanism.
- Dignity is `MODIFIER` only.
- House and angle are time-sensitive `CONTEXTUALIZER` or salience modifiers only.
- Conjunction is `merged` or `intensified` expression semantics with tension `context-dependent`; it is not default low tension and not a direction.

## Legacy reintroduction audit rule

A future candidate is marked `LEGACY_RULE_REINTRODUCTION` when its source conditions, target Primitive, and direction are materially the same as a rejected legacy rule. The warning blocks admission unless a new project-owned semantic mechanism is documented and separately Product Owner-approved. No such exception exists in this design stage.
