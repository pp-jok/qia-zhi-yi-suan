# Formal Core Profile Runtime

## Boundary

This Skill orchestrates business logic, validation, and reporting. It discovers
and invokes an external calculation capability when authorization and the
capability protocol allow that call; it does not bundle a calculator. Birth
input is never converted into chart facts by the Skill, its Python package, or
model memory.

The formal production chain is:

```text
external qualified Facts -> Core Destiny Profile -> Report Plan -> Report
```

The accepted machine path is:

```text
deterministic-facts-v1 + fact-qualification-v1
-> build-release-report
-> release-rendered-report-v1
```

Example:

```text
destiny-personality-reference-validate build-release-report FACTS.json \
  --qualification FACT_QUALIFICATION.json \
  --mode standard-portrait-v1 \
  --output REPORT.json
```

## Route contract

| Route | Preconditions | Behavior |
| --- | --- | --- |
| Formal limited coverage | Fingerprint-bound qualified facts | Build the release CDP from the packaged release manifest and active approved mappings only. |
| Candidate Preview | Explicit experimental request | Keep candidate profile identifiers, rules, and output separate from the formal CDP. |
| Controlled-inference legacy | Explicit 56-chapter compatibility request | Use the frozen legacy blueprint; never use it as Core semantic evidence. |
| Strict failure/degradation | A required gate is absent or invalid | Stop for fact-basis failures; omit unsupported semantic sections for semantic gaps. |

The current zero-Mapping release is valid and reports
`limited_coverage_unknown_only`. All P001-P006 states remain `unknown`; unknown
is not low. It forms no Signature, Dynamic, Shadow/Mature form, Theme, or
Archetype. The report still includes fact references, separate fact and semantic
assurance, limitations, unresolved questions, and audit references.

In the formal route, semantic gaps degrade through omitted sections and
explicit limitations; fact qualification failures stop before CDP
construction. A missing or mismatched
qualification must never be converted into `capability_reported` by the agent.

## Renderer modes

- `concise-portrait-v1`: compact contained formal result.
- `standard-portrait-v1`: standard contained formal result.
- `dynamic-long-form-v1`: may include only already formed, traceable Dynamics.
- `legacy-long-form-v2`: frozen compatibility handoff; it does not reinterpret
  the formal CDP with legacy semantics.

The renderer consumes only a validated Core Destiny Profile and its exact bound
Report Plan. It never reads birth input, raw facts, candidate registries, or
legacy rules, and it cannot add an unplanned claim.
