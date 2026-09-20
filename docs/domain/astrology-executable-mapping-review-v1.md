# Astrology Executable Mapping Review v1

**Stage:** C2b — candidate condition review
**Status:** accepted for D1 candidate use on 2026-09-18; no production approval

## Candidate condition vocabulary

The proposed DSL reads normalized astrology facts only:

```text
placement_any: [body names]
aspect_any: [{body_a, body_b, aspect_type}]
angle_or_house_context: [known-time context]
dignity_modifier: [body, dignity]
```

Every rule requires a personal-planet placement plus a major-aspect or
known-time angle/house corroborator. Dignity only modifies an activated rule.
Outer planets cannot carry high weight without a personal-planet or angle
contact. Unknown birth time removes every angle/house condition.

The current D1 projection accepts only conjunction, sextile, square, trine, or
opposition with an orb no greater than `8`. For the `P001` candidate rule only,
an already activated major aspect may additionally retain qualifying dignity
and known-time angular/house references. Those references cannot activate or
reverse a Primitive. The remaining rules have no dignity or angle/house
modifier; all conditions remain candidate-only and have no production approval.

## Candidate mappings

| Rule ID | Output | Candidate condition | Context / exclusions |
| --- | --- | --- | --- |
| `AS-C2B-01` | `P001` high | Sun or Mars with a Mercury/Sun/Mars major aspect or known-time angle context | decision/work; exclude Sun sign alone and leadership claims |
| `AS-C2B-02` | `P002` high | Saturn aspecting Sun, Moon, Mercury, Venus, or Mars; optional known-time corroboration | pressure/work; exclude treating Saturn alone as fear or rigidity |
| `AS-C2B-03` | `P002` low | Uranus major aspect to a personal planet or angle, plus personal-planet activation | change/work; exclude one outer-planet placement without contact |
| `AS-C2B-04` | `P003` high | Moon or Venus with a major aspect, plus known-time relationship-axis context when available | relationship; exclude dependency, charm, or relationship success claims |
| `AS-C2B-05` | `P004` high | Mars with Sun/Mercury major aspect or angle/house corroboration | action/work; exclude completion and achievement claims |
| `AS-C2B-06` | `P005` high | Moon with Mercury or Saturn major aspect, optionally modified by dignity | pressure/relationship; exclude diagnosis, intensity, or pathology claims |
| `AS-C2B-07` | `P006` high | Mercury-Saturn major aspect or Mercury plus known-time angular/house corroboration | work/decision; exclude intelligence, compliance, or education claims |

## Required modifiers

- Record aspect type, orb, enabled-orb-band result, and body provenance.
- When house/angle context is unavailable, use only the non-time-sensitive
  branch and add a limitation; do not infer an equivalent context.
- Conflicting accepted rules for one Primitive yield `mixed` unless an approved
  State Policy resolves their scoped contexts.

## Review decision

For every row, decide accept, revise, or reject; accepted rows also need exact
canonical body, aspect, dignity, and context tokens. Unaccepted rows remain
absent from candidate YAML.
