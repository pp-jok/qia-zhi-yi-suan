# Candidate Profile Summary Contract

`candidate-profile-summary-v1` is the user-readable view of a
`candidate-core-profile-v1`. It remains `primitive_only` and records the
Profile reference, grouped Primitive items, local cross-system alignment,
evidence limits, and birth-time sensitivity.

Each item records `item_id`, `primitive_id`, `canonical_name`, `state`,
`contexts`, `resolved_direction`, `context_directions`, `evidence_strength`,
`source_systems`, and `limitations`. The allowed evidence strengths are
`核心支持`、`明确支持`、`情境支持`、`单体系支持`、`证据混合`、`证据不足`. They are
rule-based labels, not probabilities.

`resolved_direction` is one of `high`, `low`, `contextual`, `mixed`, or
`unknown`. It is presentation routing only: it cannot change a Primitive
State or create semantic evidence. `context_directions` contains ordered
`(context_scope, direction)` pairs, where direction is `high`, `low`,
`mixed`, or `unknown`; every pair is derived only from
`PrimitiveState.context_states`. A compound scope retains its internal tags
until the renderer localizes them for the user.

`core_concise` and `core_standard` only render this summary. They cannot add
Signature, Dynamic, Fate Theme, Archetype, diagnosis, prediction, or new
Primitive meaning.
