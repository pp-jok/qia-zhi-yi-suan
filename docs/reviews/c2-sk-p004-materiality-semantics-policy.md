# C2-SK P004 Materiality Semantics Policy

## Governing rule

`absence of P004 evidence != evidence of non-P004 materiality`.

Every technique receives two independent descriptions: its role inside the selected methodology and its evidence-calibrated P004 materiality. Method membership never supplies Primitive ownership.

## Taxonomy

| Role | Meaning | Minimum evidence |
|---|---|---|
| `P004_REQUIRED` | Necessary to form governed P004 evidence | `DIRECT_P004_MATERIALITY`, Source+Claim directly owning the P004 construct |
| `P004_MODIFIER` | Changes strength, applicability, or expression of already-established P004 evidence without independently setting direction | `DIRECT_P004_MATERIALITY`, Source+Claim naming that modifying relation |
| `P004_CONTEXTUALIZER` | Determines the context in which established P004 evidence applies | `DIRECT_P004_MATERIALITY`, Source+Claim naming the context boundary |
| `P004_COUNTEREVIDENCE` | Weakens or limits established direction evidence; it is not automatically opposite evidence | `DIRECT_P004_MATERIALITY`, Source+Claim naming the limiting relation |
| `QUALITY_ONLY` | Evidence affirmatively limits the technique to planetary quality, condition, capability, or effectiveness for the audited scope | `DIRECT_NON_P004_BOUNDARY`, Source+boundary Claim |
| `PROMINENCE_ONLY` | Evidence affirmatively limits the technique to visibility, salience, prominence, or accidental strength for the audited scope | `DIRECT_NON_P004_BOUNDARY`, Source+boundary Claim |
| `NOT_P004` | A scoped use is directly excluded by another use case, the project ontology, or methodology evidence | `DIRECT_NON_P004_BOUNDARY`, Source+boundary Claim and explicit scope |
| `UNRESOLVED` | The method role is known or a relevance hypothesis exists, but P004 materiality has not been established or excluded | `METHOD_ROLE_ONLY` or `INSUFFICIENT` |

## Evidence classes

| Evidence class | Permitted roles | Interpretation |
|---|---|---|
| `DIRECT_P004_MATERIALITY` | Required, modifier, contextualizer, counterevidence | Direct governed P004 materiality support |
| `DIRECT_NON_P004_BOUNDARY` | Quality-only, prominence-only, not-P004 | Direct and scoped exclusion support |
| `METHOD_ROLE_ONLY` | Unresolved | Establishes method membership or role, not P004 materiality |
| `INSUFFICIENT` | Unresolved | Relevance may exist, but evidence is not sufficient for a materiality conclusion |

The Loader enforces this mapping. A classification cannot be made stronger merely by supplying more references of the wrong evidence class.

## Default unresolved policy

When a methodology includes a technique but no direct P004 materiality or direct non-P004 boundary Claim exists, the only legal classification is `UNRESOLVED`. This applies even when the technique is traditionally important, required by the method, called “strong,” “fast,” “visible,” “beneficial,” or “difficult.”

`required_by_method = true` never implies `required_by_p004 = true`.

## Direct, modifier, and exclusion semantics

- “Not direct direction” does not mean “can never modify direction evidence.”
- “Good condition” does not mean P004 high; “difficult condition” does not mean P004 low.
- Planetary speed or motion direction does not directly equal semantic Action Initiation, but that shortcut boundary alone does not prove permanent non-materiality.
- Missing evidence is not P004 low and cannot be converted into counterevidence.
- `NOT_P004` must state its exclusion scope. Application/perfection is excluded only from automatic transfer of horary event logic into natal P004 personality direction.

## Examples

| Observation | Legal result | Reason |
|---|---|---|
| George lists sect as planetary condition; no P004 bridge exists | `UNRESOLVED / METHOD_ROLE_ONLY` | Method role is known; materiality is not |
| Dignity does not directly establish initiation, but future modifier use is untested | `UNRESOLVED / METHOD_ROLE_ONLY` | Direct shortcut is blocked, exclusive status is not proven |
| Horary application describes developing events and perfection describes fulfilment | scoped `NOT_P004 / DIRECT_NON_P004_BOUNDARY` | Automatic natal-personality transfer is a different use case |
| A future Claim directly states that a technique changes an established P004 signal | `P004_MODIFIER / DIRECT_P004_MATERIALITY` | Direct materiality evidence exists |

Materiality completeness means every identified technique has an evidence-calibrated status, including honest unresolved states. It does not mean uncertainty has been eliminated.
