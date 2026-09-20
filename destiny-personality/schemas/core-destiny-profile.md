# Core Destiny Profile Contract

`core-destiny-profile-v1` is the versioned intermediate representation (IR)
for a personality model. It is not a chart fact packet, diagnosis, prediction,
reader-facing report, or renderer input prompt.

## Preconditions and terminal behavior

Create this object only after an accepted fact packet passes the selected
profile's fact-basis gate. `fact_assurance: none` forbids Core Profile
reasoning. In that case return a stopped execution artifact explaining the
missing fact basis; do not create a normal `core-destiny-profile-v1` or attach
Primitive, Signature, Dynamic, Fate Theme, or Archetype conclusions.

## Root fields

Use exactly these root fields in this order:

1. `schema_version`: fixed to `core-destiny-profile-v1`.
2. `core_profile_id`: execution-local ID; never a cross-execution identity.
3. `fact_packet_refs`: accepted fact-packet references.
4. `fact_assurance`: `project_verified` or `capability_reported` for a normal
   Profile.
5. `semantic_model_assurance`: `project_semantic_verified`,
   `project_semantic_partial`, or `none`.
6. `semantic_model_versions`: actual versions of Ontology, State Policy, Bazi
   Mapping, Astrology Mapping, Relation, Signature Formation, Dynamic
   Formation, Derived Theme, and Archetype Policy assets used by this Profile.
7. `bazi_primitive_candidates`.
8. `astrology_primitive_candidates`.
9. `primitive_states`.
10. `cross_system_alignment`.
11. `dominant_signatures`.
12. `core_dynamics`.
13. `shadow_mature_forms`.
14. `fate_themes`.
15. `archetype`.
16. `contradictions`.
17. `limitations`.
18. `unresolved_questions`.
19. `audit_trail`.

Every conclusion item requires `item_id`, `fact_refs`, `semantic_rule_refs`,
`source_refs`, `confidence_or_priority`, `limitations`, and `context`.

## Assurance resolution

`fact_assurance` describes chart facts only. `semantic_model_assurance`
describes only the versioned Semantic Core assets used for this Profile. A
Semantic Core result does not upgrade fact assurance: a
`capability_reported` fact packet remains `capability_reported`.

Use `project_semantic_verified` only when every semantic asset actually used
by this Profile exists, is approved, has a matching version, and validates.
Use `project_semantic_partial` when a complete subset can safely run but a
missing asset closes a dependent path. For example, a missing Derived Theme
Policy requires `fate_themes: []` and a recorded limitation; it never permits
free-form theme generation.

## Independence and containment

Generate Bazi and Astrology candidates independently. Alignment may relate
them but may not replace their source evidence or raise an individual Trait
Salience merely because the systems agree. `unresolved` and `non_comparable`
are valid alignment results and must preserve their limitations.

Core Profile contains no Markdown, chapter titles, paragraphs, renderer
profile, or other user-visible prose. A renderer may read a validated Profile
but cannot modify it or create Profile conclusions.

## Determinism

The same accepted Fact Packet, Semantic Bundle versions, and deterministic
execution configuration must produce a normalized-equivalent Core Profile IR.
Agent variation is allowed only after this contract, in reader-facing language,
examples, and section composition; it must not alter Profile structure.
