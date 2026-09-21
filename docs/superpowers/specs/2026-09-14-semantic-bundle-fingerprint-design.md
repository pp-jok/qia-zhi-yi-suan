# Semantic Bundle Fingerprint Design

**Date:** 2026-09-14  
**Status:** Approved by standing authorization  
**Scope:** Read-only identity for validated runtime and semantic inputs

## Decision

Add SHA-256 file digests and one deterministic bundle digest to the successful
`validate-semantic-contracts` JSON response. This closes the gap between
"validated" and "approved exact bytes" without creating semantic values,
approval identities, signatures, or a promotion command.

Two broader alternatives were rejected:

- a release-attestation manifest would prematurely define project governance
  and identity verification;
- automatic copy or promotion would cross the explicit human approval boundary.

## Fixed input set

The fingerprint covers the exact ten inputs consumed by bundle validation.
Keys include their scope so files from the accepted baseline cannot be confused
with candidate files.

Runtime scope:

- `bazi_methodology_v1.yaml`;
- `astrology_methodology_v1.yaml`;
- `score_model_v2_2.yaml`;
- `primitive_relation_graph_v1.yaml`.

Candidate scope:

- `primitive_ontology_v1.yaml`;
- `primitive_state_resolution_v1.yaml`;
- `bazi_mapping_registry_v1.yaml`;
- `astrology_mapping_registry_v1.yaml`;
- `dimension_coverage_policy_v1.yaml`;
- `narrative_rules_v1.yaml`.

## Digest contract

Each file digest is the lowercase hexadecimal SHA-256 of its raw bytes. JSON
keys use `runtime/<filename>` or `candidate/<filename>` and contain no absolute
paths.

The bundle digest hashes this UTF-8 canonical stream, with keys sorted in
ascending code-point order and a final newline after every record:

```text
<scoped-key>:<file-sha256>\n
```

The JSON field is:

```json
{
  "fingerprint": {
    "algorithm": "sha256",
    "bundle_sha256": "<64 lowercase hex characters>",
    "files": {
      "candidate/...": "<file sha256>",
      "runtime/...": "<file sha256>"
    }
  }
}
```

Fingerprinting runs only after all loaders accept the bundle. The follow-up
Semantic Snapshot Stability design requires two complete validation and
fingerprint passes before success. If a validated file disappears, becomes
unreadable, or changes between passes, return the corresponding configuration
error through the existing CLI failure channel; never emit a partial success
report.

## Skill boundary

The release checklist requires validation, review, and approval records to
refer to the same bundle digest. A changed digest returns the asset set to
`candidate`. A matching digest proves byte identity only: it does not prove
domain correctness, reviewer identity, approval, Gate 1 completion, or
`REASONING_ALLOWED`.

The distributable Skill remains free of Python and does not invoke the
development validator.
