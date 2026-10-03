# C2-SM P004 Bazi Subject-Ref Contract Review

Date: 2026-10-04

## Contract

`bazi-subject-ref-v1` makes the previously implicit subject vocabulary
machine-readable:

- pillars: `year`, `month`, `day`, `hour`;
- visible stem: `{pillar}.stem`;
- hidden stem: `{pillar}.hidden_stem.{index}`;
- source kinds: `visible_stem` and `hidden_stem`;
- hidden indices are interpreted only under `bazi-hidden-stem-order-v1`.

Thus `month.hidden_stem.0` identifies the first project-canonical hidden stem
of the month branch, not the first tuple element chosen by an external
provider. Stem names were not embedded into references, preserving the
existing codec and Ten-God join contract.

## Boundary behavior

The canonical validator resolves each participant against the actual chart.
Unknown pillars, malformed templates, absent indices, missing hour subjects,
and source-pillar mismatches fail closed. References contain no strength,
operative, primary/strongest, Dao-Shi, personality, or Primitive meaning.

```text
Subject Ref Contract:
READY

Contract Version:
bazi-subject-ref-v1

Provider-independent Identity:
PASS
```
