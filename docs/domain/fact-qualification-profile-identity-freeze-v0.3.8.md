# Fact Qualification and Profile Identity Freeze v0.3.8

## Qualification integrity

The public Candidate Core Profile route now consumes `deterministic-facts-v1`
plus a separate `fact-qualification-v1`. Qualification binds its fact
fingerprint to decoded facts, records methodology and audit references, and
uses an explicit comparison requirement/status. The facts packet's validation
summary is not authority by itself.

Assurance is derived, never caller-selected. The current project does not ship
complete strict deterministic calculation assets, so even a qualification that
records external strict success remains `capability_reported`; it cannot claim
`project_verified` until the project-owned gate is actually available.

## Three-layer identity

- Semantic bundle fingerprint changes only when interpretation assets change.
- `candidate-profile-runtime-v2` changes Profile identity and normalized IR
  when facts are organized differently.
- Presentation fingerprint changes Portrait wording identity without changing
  the Candidate Profile semantic result.

The Candidate Profile ID now binds fact fingerprint, semantic bundle
fingerprint, and profile runtime version. Codec, validator, normalized profile,
and version diff retain that separation.

## Baseline freeze

P001–P006, mappings, state resolution, context taxonomy, alignment,
presentation meanings, calibration, and holdout are frozen at this baseline.
Signature Formation is a future, separate product-design phase; no Signature,
Dynamic, Fate Theme, Archetype, or production route is enabled here.
