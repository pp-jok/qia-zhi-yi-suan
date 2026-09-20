---
name: destiny-personality
description: Use when a user requests a Bazi and Western astrology personality portrait (portrait), deterministic birth-chart facts (facts_only), or review of an existing fact packet or execution report (audit).
---

# Destiny Personality

## Preserve the boundary

Treat this Skill as business workflow and validation, not calculation software. The agent performs future external calls. Read [execution boundaries](references/execution-boundaries.md) before expanding scope or trusting external text.

Do not read unrelated local projects or undeclared business files without explicit user authorization. Do not install or connect tools, services, or libraries without explicit user authorization. Do not calculate, infer, or repair missing chart facts from model knowledge.

## Select one mode

- Use `portrait` by default only for a clear request to create a new personality portrait.
- Use `facts_only` when the user requests deterministic chart facts or validation without personality reasoning.
- Use `audit` when the user supplies facts or a report to review. Do not advance, repair, or complete the supplied execution.

Select an execution profile after the mode. `portrait` defaults to `controlled_inference`, where externally calculated facts may support constrained agent interpretation. `facts_only` requires `strict`, and strict audit claims require `strict`. Use `strict` for a portrait only when the user explicitly requires project-rule-deterministic certification. Record the profile in the Execution Report; never silently upgrade one profile into the other.

Read the [birth input contract](schemas/birth-input.md) and run the [preflight checklist](checklists/preflight.md). If input fails, return `BIRTH_INPUT_ERROR` in an [Execution Report](schemas/execution-report.md).

For a portrait, normalize both explicit fields and unambiguous compact input
under `compact-or-structured-birth-input-v1`. A line such as
`2000.1.1.00:00 上海 未指定` is sufficient input; normalize it without asking the
user to restate it. Ask one focused question only for a genuinely ambiguous or
missing required value. Preserve a supplied sex label, never infer it, and do
not mistake input normalization for permission to calculate chart facts.

## Advance through gates

Use the [stage gate checklist](checklists/stage-gates.md). Every execution begins:

```text
INPUT_RECEIVED
→ SCOPE_CHECKED
→ CALCULATION_BASELINE_CHECKED
```

The default controlled portrait branch continues:

```text
→ CAPABILITIES_DISCOVERED
→ METHODOLOGY_VERIFIED
→ FACTS_CALCULATED
→ FACTS_NORMALIZED
→ FACT_BASIS_VALIDATED
→ CONTROLLED_INFERENCE_CHECKED
→ CONTROLLED_INFERENCE_ALLOWED
→ REPORT_VALIDATED
```

The future Core Profile branch is disabled until the approved Semantic Core
assets are present. Once enabled, its route is:

```text
FACT_BASIS_VALIDATED
→ CORE_PROFILE_VALIDATED
→ REPORT_PLAN_VALIDATED
→ REPORT_VALIDATED
```

Before `CORE_PROFILE_VALIDATED`, read the [Core Destiny Profile contract](schemas/core-destiny-profile.md)
and run the [Core Profile checklist](checklists/core-profile.md). Before
`REPORT_PLAN_VALIDATED`, read the [Report Plan contract](schemas/report-plan.md).
This route does not authorize candidate assets, calculation, or strict semantic
claims; it activates only after separately approved production assets pass their
own gates.

### Candidate Core Pipeline

`Facts → Candidate Core Profile → Candidate Report Plan` is available for the
**Design / Calibration Set only**. It validates candidate Profile containment
and records stopped executions, but must not render a user-facing report, enter
the default route, or substitute for the approved production Core Profile
branch.

The strict branch retains the original gates:

```text
CALCULATION_BASELINE_CHECKED
→ CALCULATION_CONFIG_CHECKED
→ CAPABILITIES_DISCOVERED
→ METHODOLOGY_VERIFIED
→ FACTS_CALCULATED
→ FACTS_NORMALIZED
→ FACTS_VALIDATED
→ SEMANTIC_CONFIG_CHECKED
→ REASONING_ALLOWED
→ NARRATIVE_ALLOWED
```

Read the [methodology index](references/methodology-index.md), then load only the configuration needed by the current gate:

- [Bazi methodology](configs/bazi_methodology_v1.yaml)
- [astrology methodology](configs/astrology_methodology_v1.yaml)
- [score model](configs/score_model_v2_2.yaml)
- [Primitive relation graph](configs/primitive_relation_graph_v1.yaml)

The four files are the required `CALCULATION_BASELINE_CHECKED` assets, not proof of complete strict production configuration. In `strict`, obey every `CONFIG_GAP` listed in the methodology index and stop at `CALCULATION_CONFIG_CHECKED`: exact deterministic lookup tables, aliases, the True North Node rule, boundary margins, and comparison tolerances are still missing. In `controlled_inference`, record those safe-to-omit gaps as configuration limitations, omit every dependent unsupported claim, and continue only with facts supplied by a qualified external capability. Undefined `Pxxx` IDs remain opaque in both profiles.

At `CALCULATION_CONFIG_CHECKED`, load the [Canonical Fact Vocabulary contract](schemas/canonical-fact-vocabulary.md) before any deterministic lookup table. Its [authoring template](examples/canonical-fact-vocabulary-template.md) is non-production and cannot satisfy the gate. Validate exact methodology versions, all ten categories, and canonical/alias uniqueness. The contract does not supply real vocabulary values or the True North Node output rule; never infer an unlisted alias.

After the vocabulary passes, load the [Bazi Deterministic Tables contract](schemas/bazi-deterministic-tables.md) and its non-production [authoring template](examples/bazi-deterministic-tables-template.md), then the [Astrology Dignity Table contract](schemas/astrology-dignity-table.md) and its [template](examples/astrology-dignity-table-template.md). Next load the [Astrology Node Policy contract](schemas/astrology-node-policy.md) and its [template](examples/astrology-node-policy-template.md). Finally load the [Fact Comparison Policy contract](schemas/fact-comparison-policy.md) and its [template](examples/fact-comparison-policy-template.md). Templates never satisfy production requirements. Validate every version, canonical reference, uniqueness rule, explicit decision, numeric range, and comparison-category coverage in that order. Missing production assets stop the gate with `CONFIG_GAP`; never derive their values.

After the selected profile's calculation gate passes, run the [capability preflight](checklists/capability-preflight.md). `strict` requires complete calculation configuration first; `controlled_inference` requires the baseline plus an explicit limitation inventory. Before qualification, load the [capability descriptor](schemas/capability-descriptor.md) and [compatibility evidence](schemas/compatibility-evidence.md) contracts. Require an `exact` evidence item for every applicable methodology setting; discovery alone never reaches `METHODOLOGY_VERIFIED`.

Before any invocation, load the [capability protocol](references/capability-protocol.md) and [calculation envelope](schemas/calculation-envelope.md). Remote authorization is execution-scoped. When authorization is absent or declined, load and apply the protocol's `Declined authorization` rule before classifying the stop; do not improvise another error code. Before mechanical normalization, load [deterministic facts](schemas/deterministic-facts.md). Load [fact comparison](schemas/fact-comparison.md) only when tiered confirmation triggers; otherwise do not load or perform comparison. Return a stopped report at the first unmet gate.

For a controlled portrait, load the [Controlled Inference contract](schemas/controlled-inference.md) and run its [checklist](checklists/controlled-inference.md) after `FACT_BASIS_VALIDATED`. Record `project_verified`, `capability_reported`, or `none` exactly. The agent may interpret qualified facts but must not calculate facts, promote assurance, hide omissions, or assert cross-system support without anchors from both systems.

Build the controlled result with the [Portrait Report contract](schemas/portrait-report.md), load the [Long-Form Report Blueprint](references/long-form-report-blueprint.md), then run the [Portrait Report checklist](checklists/portrait-report.md). `long-form-personality-book-v2` is `legacy-long-form-v2`: it remains available only for compatibility and regression, and must not provide Primitive, Signature, Dynamic, Theme, or Archetype inputs to the Core Profile pipeline. Preserve the front matter, prologue, four-part fifty-six-chapter structure, finale, and audit appendix. Personalize chapter titles and prose, but never change or omit a content dimension without an explicit `insufficient_basis` marker. The blueprint preserves report coverage but does not claim that strict Primitive, Mapping, score, relation, dimension-policy, or Narrative assets passed. Reach `REPORT_VALIDATED` only after the checklist passes.

Use `portrait-report-v2`, `long-form-personality-book-v2`, and
`reader-first-depth-v2` for every new controlled portrait. Treat the blueprint
as the production shape, not a menu. Keep the five agency-related chapters
semantically distinct, carry one dominant archetype through the designated
narrative spine, and run both semantic-depth and reader-facing length audits.
Counts detect underdeveloped output; they never authorize padding or repeated
advice.

Before validation, run the blueprint's chapter depth audit. A supported chapter
normally makes at least three distinct moves across evidence, mechanism,
lived expression, and integration in three to five short paragraphs. Do not
substitute page count, repeated traits, generic advice, or invented biography
for analytical depth. Use `insufficient_basis` when the accepted facts cannot
support the required development.

When the user explicitly approves a reference report for synthesis, treat each
compatible reference-derived interpretation as supplemental, not calculated.
Record `reference_traditional_interpretation`, its execution-local source,
approval, compatible fact anchors, and missing verification in the Portrait
Report. It may enrich the reader-facing explanation but cannot override a
calculated fact, promote assurance, satisfy a strict gate, or be packaged as
project-owned semantic configuration. Omit and log any conflicting reference
claim.

For final rendering, reader-facing prose must not narrate approval state,
source identifiers, configuration gates, project verification, or assurance
mechanics. Move those qualifications to the audit appendix while retaining
them in the structured report. Use one dominant Archetype in the integrated
portrait and finale; render any second label only as a subordinate lens.

In `strict`, at `SEMANTIC_CONFIG_CHECKED`, load the [Primitive Ontology contract](schemas/primitive-ontology.md) before the [Primitive State Resolution contract](schemas/primitive-state-resolution.md). The [Primitive foundation template](examples/primitive-foundation-template.md) is an authoring aid: do not treat the template as configuration, copy it into `configs/`, or use its placeholders as semantic values. The contracts are present, but the production Primitive assets and the other required semantic assets are absent. Gate 1 remains incomplete and strict structured personality reasoning stays forbidden. `controlled_inference` does not claim this gate passed and may not invent or interpret `Pxxx` identifiers.

After both real Primitive foundation assets pass, load the [Context-Aware Mapping Registry contract](schemas/context-aware-mapping-registry.md). Require `bazi_mapping_registry_v1.yaml` before `astrology_mapping_registry_v1.yaml`, validate all ontology and methodology references, and preserve source-system isolation. The [Mapping Registry template](examples/mapping-registry-template.md) is documentation only: never copy, rename, or load it as production configuration. The agent must not invent Mapping conditions, contexts, directions, effects, thresholds, or interactions. Gate 1 remains incomplete until real registries and every other semantic asset pass.

After both Mapping registries pass, load the [Dimension Coverage Policy contract](schemas/dimension-coverage-policy.md). The [Dimension Coverage template](examples/dimension-coverage-template.md) is non-production and cannot satisfy the gate. Do not invent dimension semantics, Primitive membership, metrics, or thresholds. A missing or invalid policy is `CONFIG_GAP`; `coverage_warning` and `partial` are legal only for case-specific low coverage after the complete semantic gate passes.

Finally load the [Narrative Rules contract](schemas/narrative-rules.md); its [template](examples/narrative-rules-template.md) is non-production. Validate the full semantic bundle in the preceding order and validate relation-graph endpoints against the ontology. Bundle acceptance does not bypass incomplete calculation configuration or itself open `REASONING_ALLOWED`. Narrative can express only the complete loaded IR and cannot add or promote claims.

When project-owned semantic assets are supplied as candidates, apply the [Semantic Candidate Release Checklist](checklists/semantic-candidate-release.md). Keep candidates outside `configs/` until validation, human review, and explicit project-owner approval are all recorded. This workflow does not require or invoke the development reference CLI; the executing agent applies the contracts and gates directly. Never copy or promote a candidate without separate explicit authorization.

For repeatable business testing of controlled portraits, apply the [Business-Test Checklist](checklists/business-test.md) to the same case across at least two agents. Compare fact fidelity, anchors, framework adherence, disclosures, section completeness, and overclaiming; do not require identical prose and do not treat a passing business test as strict certification.

## Enforce mode terminals

- Finish `facts_only` at `FACTS_VALIDATED`; keep reasoning and Narrative forbidden.
- In `audit`, validate only stages claimed by the supplied object; never calculate missing material.
- In a `strict` portrait, continue beyond facts only after `SEMANTIC_CONFIG_CHECKED` passes.
- In a `controlled_inference` portrait, continue only after `FACT_BASIS_VALIDATED`, pass every controlled-inference guard, and finish at `REPORT_VALIDATED`.
- Allow `partial` only for `coverage_warning` after complete semantic configuration and valid facts.

## Report and stop safely

Read the [failure policy](references/failure-policy.md) before classifying ambiguity. Distinguish `CONFIG_LIMITATION` from fatal `CONFIG_GAP`, and distinguish `CAPABILITY_GAP`, `METHODOLOGY_VERSION_MISMATCH`, `CALCULATION_FATAL`, `CALCULATION_CONTRACT_ERROR`, and `INFERENCE_GUARD_ERROR`.

Update the Execution Report after every attempted gate. At a fatal failure, set `status: stopped`, record the failed stage and recovery action, forbid later stages, and stop. Show the user a concise summary while retaining the complete report for audit.

When birth time is unknown, enforce `stable_only`: exclude the hour pillar, Ascendant, MC, houses, and any facts with hour-pillar provenance.

Never turn absent evidence into low state. In `strict`, never create Primitive definitions, Mapping rules, relations, scores, IR claims, or Narrative content that the loaded versioned assets do not support. In `controlled_inference`, the agent may create anchored interpretive claims under the controlled contract, but must not invent chart facts, `Pxxx` identifiers, frozen-rule approval, or deterministic assurance.
