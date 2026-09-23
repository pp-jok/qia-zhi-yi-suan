# C2-SM Phase 2B Astrology Aspect Gate Design

## Objective

Create the first candidate-only Semantic Mechanism using the approved astrology
aspect identity Root. The candidate establishes an evidence-review gate for the
C1 P004 Action Initiation question. It answers only whether a deterministic
aspect instance is sufficiently identified to be reviewed as non-primary,
contextual evidence; it does not answer whether action initiation is high, low,
or mixed.

## Alternatives considered

1. **Recommended — P004 aspect eligibility gate.** Use the approved astrology
   Root in `RULE_GATE` role. This proves the Root-to-Mechanism audit chain with
   no direction claim and accords with the C2 feasibility matrix, which limits
   aspects to `RULE_GATE` or `MODIFIER`.
2. Bazi Ten-God provenance gate. This is technically viable but closer to the
   rejected legacy source conditions, so it has more reintroduction risk.
3. Directional Primary mechanism. This remains unsupported because there is no
   project-owned direction bridge from aspect facts to P004.

## Candidate asset

The new file is
`candidates/semantic-mechanisms-v1/mechanism_candidates/SMC-AS-ASPECT-ELIGIBILITY-GATE-P004-V1.yaml`.
It has these governing values:

| Field | Value |
|---|---|
| `candidate_id` | `SMC-AS-ASPECT-ELIGIBILITY-GATE-P004-V1` |
| `source_system` | `astrology` |
| `source_fact_classes` | `deterministic_facts.astrology.aspects` |
| `evidence_root_refs` | `ER-AS-ASPECT-INSTANCE-V1` |
| `evidence_role` | `RULE_GATE` |
| `target_primitive_questions` | P004's canonical Action Initiation question |
| `review_status` | `proposed` |
| `asserts_primitive_state` | `false` |
| `origin` | `approved_evidence_root` |

The mechanism statement is constrained to: an aspect instance may be admitted
for later P004 evidence review only after its bodies, aspect type, and orb are
identified; it cannot establish P004 direction, magnitude, or a Primitive
state. Its legacy comparison marks all three material-equivalence dimensions
false because it is neither a Mars/Sun condition nor a directional mapping.

## Contract hardening

The candidate validator will validate every `required_candidate_fields` field
from the contract before semantic checks. It will reject non-empty violations in
candidate ID, source system, fact classes, mechanism statement, review status,
role, and origin. Review status and role must be allowed by the contract;
prohibited origins must fail with the existing Golden-Sample error for that
specific origin and a generic prohibited-origin error for other forbidden
origins.

The loader remains candidate-only: it loads YAML documents for review but does
not mark a candidate approved or connect it to Mapping v2. The audit report
will show one validation-eligible proposed candidate, not an approved mapping
mechanism.

## Boundaries

- Create exactly one proposed `RULE_GATE` candidate; do not create a Bazi
  mechanism, a Primary mechanism, or a Mapping v2 candidate.
- Do not modify active runtime, active fingerprints, calibration, Signature,
  or C3.
- Preserve all guards against missing Root, missing Primitive question, direct
  state assertion, legacy equivalence, and Golden-Sample leakage.
- Product approval of this design does not itself mark the candidate `approved`.
  A subsequent review record is required before it can be considered by any
  Mapping Candidate design.

## Verification

Tests must first prove the candidate is loaded, valid against the two approved
Root IDs, and represented in the audit report. They must also prove that an
unknown role, unknown review status, missing required contract field, and a
non-Golden prohibited origin are rejected. Full tests, package verification,
and fingerprint isolation must remain green.

Completion leaves the project at: two approved Evidence Roots, one proposed
non-directional Semantic Mechanism, zero approved mechanisms, zero Mapping v2
candidates, and no runtime activation.
