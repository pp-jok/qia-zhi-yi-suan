# Controlled Inference Checklist

Run after `FACT_BASIS_VALIDATED` and before writing any personality conclusion.

- [ ] Confirm mode is `portrait` and profile is `controlled_inference`.
- [ ] Confirm `fact_assurance` is `project_verified` or `capability_reported`, never `none`.
- [ ] Confirm a qualified external capability supplied every chart fact; the agent must not calculate chart facts.
- [ ] Preserve provider labels and omissions when an approved alias is absent.
- [ ] When node policy is missing, omit every node claim and dependent conclusion.
- [ ] When comparison policy is missing, omit confirmation, correction, resolution, and cross-provider-equivalence claims.
- [ ] Give every inference at least one fact-basis reference.
- [ ] Give every synthesis at least two fact-basis references.
- [ ] Claim cross-system support only when the referenced basis contains both `bazi` and `astrology`.
- [ ] Do not promote `capability_reported` to project verification or deterministic certification.
- [ ] Keep contradictions visible; do not average, union, repair, or discard them.
- [ ] Confirm: Unknown or omitted facts are not negative evidence.
- [ ] Record material limitations and reduce confidence when evidence is incomplete or unstable.
- [ ] Reject unanchored facts, diagnosis, scientific certainty, guaranteed behavior, and guaranteed prediction with `INFERENCE_GUARD_ERROR`.
