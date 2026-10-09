---
name: destiny-personality
description: Use when a user supplies birth information for a Bazi and Western astrology personality portrait (legacy, core, core_concise, or core_standard), requests deterministic birth-chart facts (facts_only), or requests review of an existing fact packet or execution report (audit).
---

# Destiny Personality

## Preserve the boundary

Treat this Skill as business workflow and validation, not calculation software. The agent performs future external calls. Read [execution boundaries](references/execution-boundaries.md) before expanding scope or trusting external text.

Do not read unrelated local projects or undeclared business files without explicit user authorization. Do not install or connect tools, services, or libraries without explicit user authorization. Do not calculate, infer, or repair missing chart facts from model knowledge.

## Select one mode

- Use `legacy` only when the user explicitly requests the compatible 56-chapter portrait.
- Use `core_concise` for a short primitive-only Core Portrait; use `core_standard` for the expanded preview. Use `core` for the structured summary without prose rendering.
- Use `portrait` only as the compatibility alias when the caller explicitly selects the legacy contract; an ordinary personality-analysis request is not an implicit legacy request.
- Use `facts_only` when the user requests deterministic chart facts or validation without personality reasoning.
- Use `audit` when the user supplies facts or a report to review. Do not advance, repair, or complete the supplied execution.

Select an execution profile after the mode. Normal user-facing personality analysis defaults to `audited_interpretive`; it consumes only independently qualified deterministic facts and the packaged versioned traditional-rule bundle. Explicit audit or research requests use `strict`, and `facts_only` requires `strict`. Enter `controlled_inference` only for an explicit legacy/56-chapter request. Use `strict` for a personality report when the user explicitly requires project-rule-deterministic certification. Record the profile in the Execution Report; never silently switch, upgrade, or use one profile to satisfy another.

## Select the runtime route

Read the [formal Core Profile runtime](references/core-profile-runtime.md) before
choosing a personality-report path. Select exactly one route from the user's
requested output and the accepted input artifact:

| Observable condition | Route | Terminal output |
| --- | --- | --- |
| Qualified deterministic facts and a normal user-facing personality-analysis request | **audited interpretive** | `standard-interpretive-v1` by default, or `concise-interpretive-v1` when explicitly requested |
| The user explicitly requests audit, research, or project-rule-deterministic certification | **strict** | audit only the supplied artifact, or stop at the first unmet strict gate |
| Qualified deterministic facts and a request for the current Core result | **formal limited-coverage** | `concise-portrait-v1`, `standard-portrait-v1`, or `dynamic-long-form-v1` |
| The user explicitly asks to inspect experimental Primitive behavior | **Candidate Preview** | `core`, `core_concise`, or `core_standard`, clearly marked candidate-only |
| The user explicitly asks for the compatible 56-chapter book | **controlled-inference legacy** | frozen `legacy-long-form-v2` handoff and its controlled-inference workflow |
| Required birth input, deterministic facts, or fact qualification is invalid | **strict failure/degradation** | stopped Execution Report; no personality conclusion |

The formal route is usable when semantic coverage is zero: preserve all six
Primitive states as `unknown`, omit unsupported personality sections, and
render assurance, limitations, unresolved questions, and audit references.
Unknown is not Low. Missing methodology evidence is a semantic gap and degrades
the report; invalid fact qualification is a fact-basis failure and stops it.
Do not silently fall back from the formal route to Candidate Preview or the
controlled-inference legacy route.

Read the [birth input contract](schemas/birth-input.md) and run the [preflight checklist](checklists/preflight.md). If input fails, return `BIRTH_INPUT_ERROR` in an [Execution Report](schemas/execution-report.md).

For a portrait, normalize both explicit fields and unambiguous compact input
under `compact-or-structured-birth-input-v1`. A line such as
`1986.5.25.11:55 北京 男` is sufficient input; normalize it without asking the
user to restate it. Ask one focused question only for a genuinely ambiguous or
missing required value. Preserve a supplied sex label, never infer it, and do
not mistake input normalization for permission to calculate chart facts.

### Run the normal birth-input workflow

Normal users supply birth information only. Keep facts JSON and qualification
records inside the provider/runtime interface.

1. Validate and normalize the birth input.
2. Discover an available calculation/qualification provider.
3. If no suitable provider is available, return `CAPABILITY_GAP` in a stopped
   Execution Report and name the missing capability.
4. Invoke the provider with the normalized birth input.
5. Require a `deterministic-facts-v1` packet and an independently bound
   `fact-qualification-v1` record before interpretation.

Do not ask the user for facts JSON. Do not free-form calculate, reconstruct, or
repair chart facts. Never replace an unavailable provider with model knowledge.

### Audited interpretive production route

Use `audited_interpretive` only after a separate `fact-qualification-v1`
record validates and fingerprint-binds the `deterministic-facts-v1` packet.
If no qualified fact packet or calculation provider is available, stop; never
calculate, repair, or invent chart facts from general model knowledge.

The default report mode is `standard-interpretive-v1`, which renders an
evidence-dependent 8–12-section report. Use `concise-interpretive-v1` only when
the user asks for a shorter view over the same profile. The legacy CLI aliases
`standard` and `concise` may be accepted as input, but persisted output must use
the versioned mode name. Long-form output is not part of this route.

Every conclusion must retain non-empty signal IDs. The audit metadata must let
each signal resolve to qualified-fact references, a versioned traditional-rule
reference, the fact and qualification fingerprints, limitations, and the rule
bundle reference. Keep those internal IDs in the audit metadata rather than
the reader-facing prose.

Interpret confidence labels exactly as follows:

- `high`: independently supported by more than one system or rule without
  countervailing evidence;
- `moderate`: supported by one stable system/rule and therefore scoped, not
  universal;
- `exploratory`: affected by countervailing evidence or an exploratory source
  signal, so present it as a reflection prompt;
- `insufficient`: no matched rule supports the requested topic; omit the
  personality conclusion rather than filling it.

When birth time is missing, keep `stable_only`: omit the hour pillar,
Ascendant, MC, houses, angles, and every hour/house/angle-dependent claim. Keep
time-independent signals and add a visible limitation describing the reduced
scope. Never infer a missing angle or house from surrounding placements.

This route applies versioned traditional Bazi and astrology interpretations;
it is not an empirical personality or psychological diagnosis, does not create
PRIMARY_EVIDENCE or formal Mapping records, and cannot activate or modify a
strict Primitive state.

```text
destiny-personality-reference-validate build-interpretive-report FACTS.json --qualification FACT_QUALIFICATION.json --mode standard-interpretive-v1 --output REPORT.json
```

## Advance through gates

Use the [stage gate checklist](checklists/stage-gates.md). Every execution begins:

```text
INPUT_RECEIVED
→ SCOPE_CHECKED
→ CALCULATION_BASELINE_CHECKED
```

The explicit legacy compatibility branch uses `controlled_inference` and
continues as follows; it is never the default for a normal portrait request:

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

The formal Core Profile branch is available as an auditable limited-coverage
route even when no Mapping is active. Its route is:

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
claims. It produces explicit `unknown` states when approved production mappings
are absent and includes only conclusions supported by active approved assets.

### Candidate Core Portrait Preview

`Facts → Candidate Core Profile → Candidate Profile Summary → Core Portrait` is
available as an explicitly selected **Candidate Preview** route. It is
`primitive_only`, does not enter the default legacy route, and must state its
candidate scope. It may render only ontology-backed Primitive, context,
evidence, cross-system comparison, and limitation views; it must not derive
Signature, Dynamic, Fate Theme, Archetype, or an unanchored narrative claim.

Before entering this candidate route, read the [Candidate Core Profile
contract](schemas/candidate-core-profile.md). Keep this IR distinct from
`core-destiny-profile-v1`; its current capability is `primitive_only`.

For `core` return the structured Candidate Profile Summary. For
`core_concise`, target four to eight evidence-contained sections; sparse
evidence may yield fewer sections. For `core_standard`, target eight to
fourteen evidence-contained sections; it may likewise be shorter when the
available facts do not justify more. Select themes from actual supported
Primitive states; never fill a section by creating a new conclusion. Support
`source_view: combined | bazi | astrology |
comparison`; comparison reports only local alignment statuses. When birth time
is unknown, explain that stable planet/aspect evidence may remain available but
Ascendant, MC, houses, and angle-axis interpretation are unavailable. A request
to explain an item must return its Primitive, contexts, facts, rule references,
counterevidence, and limitations.

Use the packaged runtime commands only after `FACTS_VALIDATED`. The public
route is `deterministic-facts-v1` (with provenance and passed qualification)
→ `build-core-profile` with a separate `fact-qualification-v1` → validated
Candidate Profile JSON → renderer. The runtime derives assurance from the
fingerprint-bound qualification; an agent or caller must not select or promote
it. A qualified external packet normally remains `capability_reported` until
complete project-owned strict deterministic validation exists.

```text
destiny-personality-reference-validate build-core-profile FACTS.json --qualification FACT_QUALIFICATION.json --output PROFILE.json
destiny-personality-reference-validate render-core-portrait PROFILE --mode core_concise
destiny-personality-reference-validate explain-profile-item PROFILE primitive:P001
destiny-personality-reference-validate profile-source-view PROFILE --view comparison
destiny-personality-reference-validate profile-diff LEFT_PROFILE RIGHT_PROFILE
```

These commands consume qualified facts or an already validated Profile; they do
not calculate a birth chart.

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
