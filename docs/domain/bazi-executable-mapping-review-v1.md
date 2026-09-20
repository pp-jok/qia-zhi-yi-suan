# Bazi Executable Mapping Review v1

**Stage:** C2b — candidate condition review
**Status:** accepted for D1 candidate use on 2026-09-18; no production approval

## Candidate condition vocabulary

The proposed DSL reads normalized Bazi facts only:

```text
ten_god_any: [canonical Ten-God names]
ten_god_all: [canonical Ten-God names]
relation_any: [canonical relation types]
context: [decision, relationship, work, pressure]
```

Every rule requires `ten_god_all` or two independent `ten_god_any` families;
one visible token never qualifies. Exact canonical spellings must be supplied by
the candidate Canonical Fact Vocabulary before YAML projection.

The current D1 projection additionally requires evidence across at least two
distinct source pillars, an explicit `visible_stem` or `hidden_stem` origin,
and a mechanically derived day-master/month-branch environment reference from
the versioned candidate table. The environment is descriptive only; it does
not encode strength, favorable elements, patterns, transits, or outcomes.

## Candidate mappings

| Rule ID | Output | Candidate condition | Context / exclusions |
| --- | --- | --- | --- |
| `BZ-C2B-01` | `P001` high | peer (`比肩`/`劫财`) plus output (`食神`/`伤官`) evidence | decision/work; exclude when either family is only a hidden or uncorroborated token |
| `BZ-C2B-02` | `P002` high | resource (`正印`/`偏印`) plus authority (`正官`/`七杀`) evidence | pressure/work; exclude treating authority evidence as personal preference without corroboration |
| `BZ-C2B-03` | `P002` low | output plus wealth (`正财`/`偏财`) evidence, without accepted resource/authority counterweight | change/work; never infer novelty from output alone |
| `BZ-C2B-04` | `P003` high | wealth or authority evidence plus peer or resource corroboration | relationship; exclude treating exchange, duty, or role sensitivity as reciprocal attunement |
| `BZ-C2B-05` | `P004` high | output plus wealth evidence | work/action; exclude completion, achievement, or moral-worth claims |
| `BZ-C2B-06` | `P005` high | resource plus authority evidence | pressure; describes containment/processing only, never diagnosis or intensity |
| `BZ-C2B-07` | `P006` high | resource plus authority evidence | work/decision; exclude equating authority symbolism with obedience or intelligence |

## Required modifiers

- Each activated rule records visible/hidden provenance, source pillars, and
  a day-master environment reference from the candidate table.
- A conflicting accepted rule for the same Primitive produces `mixed` unless a
  separately approved State Policy resolves the scoped contexts.
- Relations may only modify an already activated rule; none may create a
  Primitive or reverse direction by itself.

## Review decision

For every row, decide accept, revise, or reject; accepted rows also need exact
Canonical Fact Vocabulary tokens and a machine-readable context enumeration.
Unaccepted rows remain absent from candidate YAML.
