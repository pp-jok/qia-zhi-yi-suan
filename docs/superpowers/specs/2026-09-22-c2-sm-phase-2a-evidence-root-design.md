# C2-SM Phase 2A Evidence Root Design

## Decision and objective

The delegated Product Owner authorization of 2026-09-22 opens C2-SM Phase 2A.
This phase admits a minimal set of project-owned Evidence Root definitions that
identify deterministic fact instances without assigning personality meaning.

It must make the two fact families needed for future Bazi and astrology
mechanism review auditable:

1. Bazi Ten-God observations, including source pillar and visible/hidden origin.
2. Astrology aspect observations, including the two bodies, aspect type, and
   orb.

The result is still candidate-only and has no Mapping v2 or runtime effect.

## Alternatives considered

1. **Recommended — two fact-identity roots.** Admit one Bazi and one astrology
   root definition, each describing the stable identity fields of a canonical
   fact instance. This establishes cross-system review parity while remaining
   entirely non-directional.
2. Admit every available fact family now. This broadens coverage without a
   demonstrated review need and makes root governance harder to validate.
3. Admit Semantic Mechanisms directly. This would skip the fact-identity layer
   required by C2-D1 and risks reintroducing legacy target/direction claims.

## Asset model

The Registry gains two approved entries:

| Root ID | Canonical source reference | Stable instance identity | Permitted use |
|---|---|---|---|
| `ER-BZ-TEN-GOD-INSTANCE-V1` | `deterministic_facts.bazi.ten_gods` | `subject_ref`, `ten_god`, `source_pillars`, `source_kind` | Identify and audit a Ten-God fact instance. |
| `ER-AS-ASPECT-INSTANCE-V1` | `deterministic_facts.astrology.aspects` | `body_a`, `body_b`, `aspect_type`, `orb` | Identify and audit an aspect fact instance. |

Both roots explicitly prohibit direct Primitive-state assertions, mapping-rule
creation, Golden-Sample derivation, and use of renderer wording or a legacy
output as provenance. A root is a fact-identity descriptor; it is not a rule,
mechanism, personality conclusion, or scoring input.

## Validation and audit design

`load_evidence_root_registry(root)` will validate each root against the root
contract before returning it. Every entry must contain the contract's required
fields, a non-empty stable ID, a declared system, canonical source reference,
scope, permitted/prohibited use, provenance, review state, and Product Owner
decision reference. Duplicate IDs, unknown review statuses, and prohibited
origins fail closed.

`load_approved_evidence_root_ids(root)` continues to expose only explicitly
approved roots. Existing mechanism validation consumes only those IDs. A new
audit report records root count by review status and validation findings.

## Boundaries

- No Semantic Mechanism candidates are added in Phase 2A.
- No Mapping v2 candidate, active mapping registry, calibration, Signature, C3,
  or runtime code changes.
- Existing active semantic and presentation fingerprints must remain unchanged.
- The C2-SM candidate fingerprint is expected to change because the Registry
  gains approved candidate-only root definitions.

## Tests and completion criteria

Tests must first demonstrate that an approved, complete root is loaded and
available to a mechanism candidate; missing required fields, duplicate IDs,
unknown review statuses, and Golden-Sample provenance are rejected. Existing
tests must continue to prove zero Semantic Mechanisms, no runtime activation,
and fingerprint isolation.

Phase 2A is complete only when the focused root tests, full test suite, package
verification, audit report, and updated governance review all pass. Its next
gate is a separate review of the first Semantic Mechanism candidate; it does
not authorize Mapping v2.
