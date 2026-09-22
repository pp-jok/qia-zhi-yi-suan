# Fact Qualification Contract

`fact-qualification-v1` is the audit object that authorizes a specific
`deterministic-facts-v1` packet for Candidate Core Profile runtime use. It is
separate from the facts packet: a facts packet's `validation_summary` is a
human-readable summary, not qualification authority.

## Required fields

```text
schema_version
fact_fingerprint
qualification_status
derived_fact_assurance
fact_contract_version
methodology_versions
validation_refs
provenance_refs
calculation_envelope_refs
comparison
validation_summary
```

`schema_version` is `fact-qualification-v1`; `fact_contract_version` is
`deterministic-facts-v1`; and `qualification_status` is `passed` before a
profile may be built. `fact_fingerprint` must equal the deterministic runtime
fingerprint of the decoded current facts. A mismatch is
`FACT_QUALIFICATION_MISMATCH`.

`validation_refs`, `provenance_refs`, and `calculation_envelope_refs` are
non-empty audit references. `methodology_versions` must equal the decoded Bazi
and astrology methodology versions. `validation_summary` records passed
`structure`, `methodology`, `provenance`, `internal_consistency`, and
`time_scope` checks, plus `calculation_config`.

`comparison.required: false` requires `status: not_required`.
`comparison.required: true` requires `status: passed` and a non-empty
`comparison_ref`. Missing, failed, or conflicting required comparison evidence
is not qualified.

## Assurance derivation

The runtime derives assurance; a caller cannot set it. A qualified external
packet normally yields `capability_reported`. `project_verified` additionally
requires complete project-owned strict deterministic configuration and its
validation evidence. The current candidate runtime does not ship that complete
strict configuration, so it must not promote a self-attested strict result
beyond `capability_reported`.
