# Candidate Profile Summary Contract

`candidate-profile-summary-v1` is the user-readable view of a
`candidate-core-profile-v1`. It remains `primitive_only` and records the
Profile reference, grouped Primitive items, local cross-system alignment,
evidence limits, and birth-time sensitivity.

Each item must retain its Primitive ID, ontology canonical name, state,
contexts, discrete evidence strength, source systems, and limitations. The
allowed evidence strengths are `核心支持`、`明确支持`、`情境支持`、`单体系支持`、
`证据混合`、`证据不足`. They are rule-based labels, not probabilities.

`core_concise` and `core_standard` only render this summary. They cannot add
Signature, Dynamic, Fate Theme, Archetype, diagnosis, prediction, or new
Primitive meaning.
