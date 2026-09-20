# Dynamic Formation Review v1

**Stage:** C3 — Dynamic Formation Review
**Status:** accepted for C4 review on 2026-09-18; no production approval
**Input:** C1 Primitive Catalog and C2's independently accepted mapping review.

## Governing principle

Core Dynamic is an actually activated, evidence-backed tension between two
distinct Primitive poles. It is not a trait label, a relation-graph default, a
cross-system agreement, a report topic, or a requirement to produce a
psychologically dramatic result. A Profile may contain 0–7 Dynamics; 2–5 is a
typical observation range, never a quota.

No named Dynamic family is proposed by this document. Candidate relation
families must be separately reviewed before use. This avoids encoding a Golden
Sample, a report chapter, or a fashionable contrast as a universal pattern.

## Candidate formation pipeline

```text
independent candidates
→ Primitive State Resolution
→ source-local Signatures
→ Cross-System Alignment
→ relation eligibility
→ Core Dynamic selection
→ limitations and audit trail
```

Each step is deterministic after its approved assets and accepted facts are
fixed. An Agent may explain a result but cannot add a Signature, Dynamic,
relation, priority, or limitation.

## Signature proposal

A `DominantSignature` is a source-local, explainable grouping of two or more
resolved Primitive States and their signals. It records source system,
Primitive references, salience, stability, context, counterevidence, and
limitations.

- A Signature cannot merge Bazi and Astrology evidence.
- `unknown` cannot contribute a positive membership.
- A Signature may be absent; absence does not become a low state.
- Later cross-system Alignment can compare source-local Signatures but cannot
  increase a component Primitive's Trait Salience.

## Cross-system Alignment proposal

Alignment compares independently resolved candidates or source-local
Signatures. It has exactly these candidate outcomes:

| Outcome | Meaning | Permitted effect |
| --- | --- | --- |
| `validation` | compatible independent evidence points to a similar scoped tendency | raises confidence in the comparison, not source-local salience |
| `complement` | systems describe different but mutually useful scopes | preserve both scopes; no merged trait |
| `contextualization` | one system specifies where or when another applies | add scoped context and limitation |
| `tension` | independently supported tendencies conflict in a comparable context | may raise Dynamic selection priority; never lower either supported state |
| `correction` | one system limits the semantic range of an earlier interpretation | record qualification only; never correct chart facts |
| `unresolved` | evidence is insufficient to classify the relation | preserve both and the uncertainty |
| `non_comparable` | semantic level or context does not permit comparison | preserve both without synthesis |

Only `tension` is eligible as cross-system support for a Core Dynamic, and it
is insufficient by itself: the relation must still pass the Dynamic gate below.

## Core Dynamic eligibility gate

A proposed Dynamic is valid only when all conditions hold:

1. Two distinct, non-`unknown` Primitive States are activated in a reviewed
   relation family with explicit `pole_a` and `pole_b`.
2. The relation has a semantic rationale distinct from the Primitive labels;
   two strong traits do not automatically form a tension.
3. Both poles have fact and mapping references, a compatible context, and
   retained counterevidence.
4. A documented modifier or contextualizer explains why the poles are
   simultaneously relevant rather than merely unrelated.
5. No exclusion invalidates the relation in the case.

If any condition is missing, omit the Dynamic and record the limitation. A
relation may be supported by one system; cross-system corroboration is useful
but never mandatory. `unresolved` or `non_comparable` cannot be coerced into a
Dynamic.

## Priority and selection proposal

Priority is deterministic and versioned. It may use only approved relation
policy inputs: pole support, evidence stability, contextual recurrence,
documented modifiers, and a valid Alignment outcome. It must not use prose,
user preference for drama, chapter count, or Archetype labels.

Select the highest eligible relations up to seven. When priority ties, use a
stable rule ID order. Output zero or one when the evidence warrants it; record
why omitted candidate relations failed eligibility.

## Required Dynamic audit fields

```text
dynamic_id
relation_family_ref
pole_a
pole_b
source_primitive_refs
source_signature_refs
relation_rule_ref
support
modifiers
contextualizers
true_tension
priority
counterevidence_refs
limitations
```

`shadow_form` and `mature_form` are not inputs to Dynamic selection. They are
downstream derived forms governed by a separate policy.

## C3 decisions required

Product review must approve the eligibility gate, alignment meanings, priority
inputs, deterministic tie-break, and whether the initial relation-family set is
intentionally empty or contains specific reviewed families. No `pending` rule
may be written to a relation graph, Builder, or user-facing report.
