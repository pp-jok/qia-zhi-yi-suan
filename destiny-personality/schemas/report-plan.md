# Report Plan Contract

`report-plan-v1` is an immutable rendering plan derived from one validated
`core-destiny-profile-v1`. Candidate planning instead uses
`candidate-report-plan-v1` derived from `candidate-core-profile-v1`; neither
is a source of new personality inference.

## Root fields

Use these root fields:

```text
schema_version
core_profile_ref
renderer_profile
selected_topics
omitted_candidate_topics
section_plan
rendering_constraints
audit_trail
```

Every `selected_topic` requires non-empty `profile_refs`. Every omitted
candidate requires a `reason`: no activation evidence, lower priority than a
selected topic, duplicate scope, or profile limitation.

## Renderer containment

The production planner accepts `CoreDestinyProfile` plus `renderer_profile`; it never
accepts a bare Fact Packet. The renderer accepts `ReportPlan +
CoreDestinyProfile` and must reject a core assertion that lacks a valid
`profile_refs` reference.

`concise-portrait-v1`, `standard-portrait-v1`, and `dynamic-long-form-v1` use
section-count targets only. Sparse evidence may produce fewer sections and
records `evidence_limited`; no renderer may add a Topic, Primitive, Signature,
Dynamic, Fate Theme, or Archetype merely to meet a count target.

`legacy-long-form-v2` remains a compatibility renderer. It is not a source of
Core Profile inputs.
