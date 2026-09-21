# Shadow, Mature, Fate, and Archetype Review v1

**Stage:** C3 — Derived-form review  
**Status:** accepted for C4 review on 2026-09-18; no production approval  
**Input:** only validated Core Dynamics; never raw chart facts or Archetype labels.

## Fixed derivation order

```text
Core Dynamic
→ Shadow Form
→ Mature Integration
→ repeated pattern analysis
→ Fate Theme
→ Archetype
```

No later layer can become evidence for an earlier layer. In particular,
Archetype is a compression of Profile evidence and cannot create or raise a
Primitive, Signature, Dynamic, or Fate Theme.

## Shadow Form proposal

A `ShadowForm` describes how one validated Dynamic may become imbalanced under
pressure, resource scarcity, threat, or defensive narrowing. It must reference
one Dynamic, the activating context, protective function, possible cost,
counterevidence, and limitation. It is neither a diagnosis nor a moral flaw.

Do not derive a Shadow Form from a Primitive alone. No Shadow is generated when
the Dynamic lacks a reviewed pressure-context bridge.

## Mature Integration proposal

A `MatureIntegration` describes how the same Dynamic's two poles can be held
without suppressing either. It must reference the same Dynamic as its Shadow
Form, relevant enabling conditions, context, limitations, and audit references.
It is not a positive opposite label and cannot be rendered as advice detached
from the Dynamic's evidence.

## Fate Theme proposal

A `FateTheme` is an optional, durable pattern hypothesis. It is permitted only
through one of these auditable paths:

1. **Repeated-dynamic path:** at least two Core Dynamics share a reviewed
   repeated pattern, with stable-force and movement-force references.
2. **Exceptional-dynamic path:** one exceptionally dominant Dynamic has
   independently supported recurrence in at least two distinct contexts; retain
   `cross_context_recurrence_refs`.

Both paths require `source_dynamic_refs`, `stable_force_refs`,
`movement_force_refs`, `development_theme_refs`, counterevidence, limitations,
and a versioned Derived Theme Policy reference. A single Dynamic alone never
creates a Fate Theme.

## Archetype proposal

An `Archetype` is an optional concise expression of a sufficiently supported
Profile. It requires `archetype_id`, `source_dynamic_refs`,
`stable_force_refs`, `movement_force_refs`, `development_theme_refs`,
`support_level`, `counterevidence_refs`, `limitations`, and `context`.

It must be absent when its compression would conceal material contradictions,
weak evidence, unresolved comparisons, or context locality. It cannot be used
as a default label, a report-title generator, or an upstream inference source.

## C3 decisions required

Product review must approve the Shadow pressure-context boundary, Mature
Integration conditions, exceptional-dynamic qualification, Archetype support
level, and all required audit fields. Missing approved policy closes the
dependent path and yields `project_semantic_partial`; it never permits
free-form generation.
