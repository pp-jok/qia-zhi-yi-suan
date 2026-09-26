# Semantic Core Verification Lifecycle Closure Report

## Baseline and scope

This closure starts from `65f6529` and changes candidate-only engineering. It
does not approve, enable, or promote a semantic asset.

## Initial gaps and engineering decisions

- Caller-supplied decision and evaluation files were removed from the
  authoritative promotion CLI path. Repository governance registries are now
  the trust root.
- Mapping Proposal is explicit and distinct from reviewed Mapping candidates;
  an empty proposal registry remains a valid zero result.
- Primitive resolution retains exclusion, local context, and conflict state
  rather than collapsing all disagreement to `mixed`.
- Pipeline provenance is persisted once and consumed by Pipeline Explain and
  Source View without semantic recomputation.
- Formation fingerprints are content-bound canonical hashes of loaded policy
  payloads, with a separate readable version table.

## Authority and lifecycle model

`governance/semantic-promotion-v1/` owns decision, calibration, and holdout
registries. A promotion resolves a decision ID, rejects superseded or unknown
records, requires matching passing machine-artifact metadata, writes only a
Shadow record, and rejects a duplicate Shadow record. Rollback persists its
terminal state. The older non-authoritative promotion command is documented as
a simulation and cannot write an Authority Store record.

## Mapping, evaluation, and provenance

Proposals require explicit authoring and review before candidate compilation.
Proposal validation distinguishes required non-empty fields from qualifier
collections: `modifiers`, `contextualizers`, `counterevidence`, and
`exclusions` must exist as lists but may be empty. Calibration uses the
repository design fixture set and Holdout uses its disjoint holdout fixture
set. Each runner emits a fingerprint-bound artifact; only an explicit
`--register` request can append a passing artifact to the authority registry.
Blocked or failed evaluations cannot be registered.

The stored provenance graph links formed output through Primitive and Mapping
to Semantic Mechanism, Evidence Root, and canonical Fact where those records
exist. Cross-asset links are read only from an authored Mapping
`provenance_links` collection; the runtime never fabricates a Cartesian product
from independent reference lists. Shadow/Mature forms and Archetypes are also
stored as lineage nodes.

## Qualifier resolution boundary

The current runtime is formally **stored-but-not-resolved** for Mapping
qualifiers. It preserves `modifier_refs`, `contextualizer_refs`, and
`counterevidence_refs`, and marks such Primitive output with
`qualifier_resolution_mode: stored_but_not_resolved`. Qualifiers do not create,
reverse, or weight a Primitive direction until a separately approved,
policy-driven qualifier resolution model exists. Exclusions remain an explicit
hard gate when `exclusion_matched` is true.

## Current real semantic asset state

```text
Approved Evidence Roots: 2
Proposed Semantic Mechanisms: 1
Approved Semantic Mechanisms: 0
Mapping Proposals: 0
Approved Mappings: 0
Primitive/Formation Runtime: disabled
Production Activation: not authorized
```

The proposed `SMC-AS-ASPECT-ELIGIBILITY-GATE-P004-V1` remains proposed with
role `RULE_GATE`; it was not changed.

## Historical verification evidence

- Before this closure, all 61 test files were run in bounded groups to avoid
  the local execution cutoff: historical baseline `551 passed`.
- Isolated wheel build, install, import, and runtime validation completed:
  `package verification passed`.

## Readiness statement

```text
Semantic Verification Lifecycle: COMPLETE
Semantic Core Foundation Engineering: COMPLETE / FROZEN
Calibration Pipeline: COMPLETE
Holdout Pipeline: COMPLETE
Semantic Asset Readiness: blocked at Product Owner mechanism and Mapping gates
Production Activation: not authorized
```

No Evidence Root, Semantic Mechanism, Mapping, Primitive runtime, formation
policy, or production semantic bundle was activated by this work.
