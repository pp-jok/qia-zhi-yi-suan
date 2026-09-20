# Core Profile Checklist

Run this checklist before marking a Core Profile validated.

- [ ] The fact packet was accepted and `fact_assurance` is not `none`.
- [ ] `fact_assurance` and `semantic_model_assurance` are recorded separately.
- [ ] Every used semantic asset has an approved, matching version reference.
- [ ] Missing semantic assets close their dependent path and add a limitation.
- [ ] Bazi and Astrology candidates remain independently traceable.
- [ ] Every Primitive, Signature, Dynamic, Fate Theme, and Archetype item has
      its required audit references.
- [ ] `unknown` was not changed to `supported_low` without explicit reverse
      evidence.
- [ ] `unresolved` and `non_comparable` alignment results retain limitations
      and were not force-synthesized.
- [ ] No renderer, Markdown, section, paragraph, or user-visible prose field
      appears in the Profile.
- [ ] Repeated deterministic construction with the same facts and Semantic
      Bundle produces a normalized-equivalent Profile.
