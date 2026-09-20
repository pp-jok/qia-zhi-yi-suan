# Astrology Semantic Mapping Review v1

**Stage:** C2 — Astrology Semantic Mapping Review
**Status:** accepted for C3 review on 2026-09-18; no production approval
**Input:** C1 catalog entries `CP-CORE-01` through `CP-CORE-06`.

## Boundary and evidence standard

These are review hypotheses, not rules in `astrology_mapping_registry_v1.yaml`.
They use only project-methodology fact families: personal planets, Ascendant/MC,
major aspects, house context when birth time is known, and dignity as a modifier.
Outer planets require personal-planet or angle contact for high weight. No
single sign, planet, aspect, house, dignity label, or birth-time-dependent fact
can determine a Primitive alone.

Future rules require a contextual qualifier, aspect/house or comparable
corroboration, a stated exclusion, and a limitation. Unknown birth time removes
Ascendant, MC, houses, and other time-dependent facts; it cannot be repaired by
an interpretive substitute.

## Candidate evidence propositions

| ID | Candidate Primitive | Astrology evidence proposition | Mandatory context and exclusion | Counterevidence / limitation |
| --- | --- | --- | --- | --- |
| `AS-01` | Agentic Self-Direction | A coherent Sun, Mars, Mercury, or Ascendant pattern may support self-definition, decision ownership, or initiative. | Require a personal-planet/aspect or angle context; exclude treating Sun sign alone as agency. | Relationship, Saturn, or house context may qualify where ownership is expressed. |
| `AS-02` | Predictability Orientation | A coherent Saturn, fixed-pattern, or stabilizing personal-planet pattern may support continuity; a corroborated Uranian/change pattern may support lower orientation. | Require personal-planet or angle contact for outer-planet weight; exclude equating one aspect with risk preference. | Structure in one domain may coexist with novelty in another. |
| `AS-03` | Relational Attunement | A coherent Moon, Venus, descendant/relationship-axis, or personal-planet relational pattern may support reciprocity and feedback salience. | Require corroborating aspect or known-time relational context; exclude treating Venus or Moon alone as dependency. | Care, attachment, public charm, and relational attunement are distinct. |
| `AS-04` | Action Mobilization | A coherent Mars/Sun/Mercury activation pattern may support initiation, pacing, or externalization. | Require aspect, angle, or house corroboration when available; exclude converting high activation into completion or achievement. | Pressure action and voluntary action may differ. |
| `AS-05` | Affective Regulation Orientation | A coherent Moon, Mercury, Saturn, and relevant aspect pattern may qualify processing, containment, and expression timing of affect. | Require non-diagnostic language and an approved semantic bridge; exclude emotional intensity or mental-health claims. | Private regulation and public expression can diverge. |
| `AS-06` | Structuring Orientation | A coherent Mercury/Saturn or relevant personal-planet/angle pattern may support explicit framing, standards, sequencing, or model use. | Require corroboration beyond a single placement; dignity is modifier-only; exclude intelligence or compliance conclusions. | Occupational role or learned method may explain structure without a global tendency. |

## Cross-cutting modifiers proposed for C2 review

- **Time sensitivity:** any house/angle inference includes birth-time provenance
  and is excluded under `stable_only`.
- **Aspect salience:** only enabled major aspects and approved orb bands may
  qualify a proposition; exact thresholds remain an asset decision.
- **Dignity:** may modify an otherwise supported proposition, never create one.
- **Outer planets:** cannot carry high weight without personal-planet or angle
  contact, as required by the existing methodology.
- **Conflict handling:** Astrology-internal conflict yields `mixed` or a
  limitation; it is not reconciled by Bazi evidence at this stage.

## C2 review decisions required

For each proposition, product review must accept, revise, or reject the
semantic bridge and specify eligible fact families, mandatory corroboration,
prohibited shortcuts, exclusions, and retained counterevidence.
