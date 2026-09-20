# Core Profile Determinism Policy v1

**Stage:** C4 — Calibration Review
**Status:** C4a accepted for D1 candidate execution on 2026-09-18; no runtime use

## Required invariant

Given the same accepted Fact Packet, same approved Semantic Bundle versions,
and same deterministic execution configuration, repeated construction must
produce normalized-equivalent `core-destiny-profile-v1` IR.

Normalization sorts only contractually unordered collections by stable ID and
removes execution-local identifiers and timestamps. It must not discard facts,
states, relations, priorities, source references, limitations, or unresolved
results. A difference after normalization is a `CORE_DETERMINISM_ERROR` and a
release blocker.

## In-scope comparison

```text
primitive_states
source-local signature membership
cross-system alignment outcomes
core dynamic membership, poles, and priority
shadow and mature forms
fate-theme basis
archetype basis
contradictions, limitations, unresolved questions
semantic_model_versions
```

It does not compare reader-facing prose. Agents may render different language
only from the same validated Profile and Report Plan; neither may alter the Core
IR.

## Prohibited inputs and failure handling

Core construction must not read chapter count, renderer profile, desired result,
model sampling, system clock, random seed, arbitrary map iteration order, or an
Archetype label as upstream inference input.

On failure, retain both normalized artifacts, their exact bundle fingerprints,
and the first differing path. Stop promotion of that Semantic Bundle version;
do not weaken comparison by excluding the changed field.
