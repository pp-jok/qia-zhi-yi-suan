# Candidate Core Profile Contract

`candidate-core-profile-v1` is an isolated, pre-production intermediate
representation. It is not `core-destiny-profile-v1`, a reader-facing report,
or an authorization to open a production route.

## Root fields

Use these root fields:

```text
schema_version
candidate_profile_id
fact_fingerprint
fact_assurance
semantic_model_assurance
semantic_capability_level
semantic_bundle_fingerprint
semantic_model_versions
bazi_primitive_candidates
astrology_primitive_candidates
cross_system_alignments
primitive_states
limitations
```

`schema_version` is fixed to `candidate-core-profile-v1` and
`semantic_capability_level` is currently fixed to `primitive_only`.
`candidate_profile_id` is derived from both `fact_fingerprint` and the semantic
bundle fingerprint, so identical facts evaluated under a changed bundle cannot
share an identity. `semantic_model_versions` must include versioned mapping,
state resolver, alignment resolver, context taxonomy, evidence weighting, and
builder semantics. The version list also records the state and alignment
resolver versions explicitly. The bundle fingerprint covers semantic YAML assets and those
algorithm versions; calibration and holdout evidence records are excluded to
avoid circular self-fingerprinting.

## Evidence and context

Every Primitive Candidate records its source system, direction, fact and rule
references, `contexts`, salience, evidence stability, modifiers,
counterevidence, expression mode, tension level, and counterweight effect.
Contexts are non-empty tags from `candidate-context-v1`, never free-form
compound strings. A Primitive State records `context_states`; opposing evidence
with disjoint scopes resolves to `context_differentiated`, while exact, subset,
superset, or partial-overlap scopes resolve to `mixed` and retain a scope-
conflict audit note. Counterweight evidence remains visible in State Audit
limitations; it does not silently alter candidate direction or salience.

Each Cross-System Alignment has an ID, Primitive ID, local context references,
source rule references, status, and direction relation. Allowed statuses are
`validation`, `contextualization`, `unresolved`, and `non_comparable`.

Unknown birth time removes only time-sensitive angular and house modifiers.
Stable planetary aspects remain eligible evidence when their mapping rule does
not require time.

## Containment

The Candidate Report Planner may select existing non-unknown Primitive topics.
It cannot derive Signature, Dynamic, Fate Theme, Archetype, or new prose-level
semantic conclusions. A future production route must use the separate
`core-destiny-profile-v1` contract and explicit human approval.

An empty candidate list yields `unknown` for that Primitive. Candidate IR has
no Dynamic or Archetype fields; those belong only to a future production
contract after independent approval.
