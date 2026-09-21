# Controlled Inference Business Testing Design

**Date:** 2026-09-14  
**Status:** Approved by explicit no-confirmation implementation authorization; report structure corrected after live-test review  
**Scope:** Skill workflow, contracts, status model, tests, and documentation

## 1. Product decision

The product no longer treats every missing semantic asset as a universal block
on personality reports. It separates two execution profiles beneath the
existing modes:

- `controlled_inference`: the default profile for `portrait`. A qualified
  external capability supplies chart facts; the agent interprets them under a
  fixed analysis and report contract. Results are useful for business testing
  but are not represented as fully project-rule-deterministic.
- `strict`: required for `facts_only`, deterministic certification, and strict
  audit claims. It retains the complete calculation and semantic configuration
  gates.

The user-facing modes remain `portrait`, `facts_only`, and `audit`. No fourth
mode is introduced.

## 2. Trust boundary

The relaxation applies only to interpretation. The agent must not calculate or
repair pillars, planetary positions, houses, aspects, dignities, historical
time, or other chart facts from language-model knowledge.

Every fact basis receives one assurance level:

- `project_verified`: all applicable project configuration and deterministic
  validation gates passed;
- `capability_reported`: a qualified external capability supplied the value and
  the agent validated method compatibility, provenance, structure, range,
  internal consistency, and time sensitivity, but could not independently
  re-derive it under complete project-owned lookup and comparison assets;
- `none`: no usable fact basis; personality inference is forbidden.

`capability_reported` permits only `controlled_inference`. It never satisfies a
strict deterministic-fact claim. Missing aliases are retained with their source
labels rather than guessed. A node fact is omitted unless the applicable node
policy is available. Missing comparison policy forbids claims that a secondary
result confirms, corrects, or resolves the primary result.

## 3. Gate model

All executions begin with:

```text
INPUT_RECEIVED
-> SCOPE_CHECKED
-> CALCULATION_BASELINE_CHECKED
```

The controlled portrait branch continues:

```text
-> CAPABILITIES_DISCOVERED
-> METHODOLOGY_VERIFIED
-> FACTS_CALCULATED
-> FACTS_NORMALIZED
-> FACT_BASIS_VALIDATED
-> CONTROLLED_INFERENCE_CHECKED
-> CONTROLLED_INFERENCE_ALLOWED
-> REPORT_VALIDATED
```

`CALCULATION_BASELINE_CHECKED` requires the four frozen baseline YAML files,
input/time rules, capability contracts, and output schemas. The five advanced
calculation assets remain mandatory for `strict`; their absence is recorded as
a configuration limitation rather than a fatal `CONFIG_GAP` for
`controlled_inference`, provided every affected unsupported claim is omitted.

The strict branch retains the existing order:

```text
-> CALCULATION_CONFIG_CHECKED
-> CAPABILITIES_DISCOVERED
-> METHODOLOGY_VERIFIED
-> FACTS_CALCULATED
-> FACTS_NORMALIZED
-> FACTS_VALIDATED
-> SEMANTIC_CONFIG_CHECKED
-> REASONING_ALLOWED
-> NARRATIVE_ALLOWED
```

Strict gates are not weakened or relabeled as complete.

## 4. Controlled analysis contract

Every analytical claim is a record with:

- `claim_id`
- `claim`
- `claim_type`: `observation`, `inference`, or `synthesis`
- `systems`: one or both of `bazi` and `astrology`
- `basis_refs`: references to fact-basis items
- `confidence`: `high`, `medium`, or `low`
- `limitations`: explicit list, possibly empty

Rules:

1. An inference has at least one fact-basis reference.
2. A synthesis has at least two references and may claim cross-system support
   only when both systems are represented.
3. `capability_reported` facts may support interpretation but never a claim of
   deterministic project verification.
4. Contradictory signals are described as context or tension, not silently
   averaged or deleted.
5. Unknown or omitted facts do not become negative evidence.
6. The agent may vary wording and emphasis but may not add unanchored chart
   facts, diagnoses, scientific certainty, or guaranteed predictions.

Primitive, Mapping, Dimension, and Narrative assets remain optional refinement
inputs for this profile. When absent, the agent works directly from the
validated fact basis and must not invent `Pxxx` identifiers, rule IDs, scores,
or claims that those frozen assets approved its reasoning.

## 5. Portrait report contract

The user-facing report uses `long-form-personality-book-v1`, derived from the
approved reference report's format and content dimensions without copying its
case-specific conclusions into the generic Skill. It contains:

Every supported chapter develops at least three distinct analytical moves
across evidence, mechanism, lived expression, and integration. Three to five
short paragraphs are the normal rendering; repetition, generic advice,
invented biography, and paraphrase padding do not count as depth.

1. front matter with birth data, Bazi main chart, Western axes, and important
   structures;
2. an unnumbered prologue;
3. Part I with 15 chapters covering separate Bazi analysis, separate astrology
   analysis, and the first cross-system synthesis only in chapter 15;
4. Part II with 9 chapters turning supported structures into lived personality
   patterns;
5. Part III with 16 chapters covering Shadow, defense, blind spots, risk,
   boundaries, and mature recalibration;
6. Part IV with 16 chapters covering Archetype, stability, authorship,
   commitment, resilience, relationship Fate, emotional maturity, creativity,
   social position, regret risk, the operating cycle, and five Fate questions;
7. an unnumbered finale;
8. a compact audit appendix for assurance, provenance, anchors, omissions,
   limitations, and disclosure.

The 56 chapter dimensions and their order are fixed. Chapter titles and prose
are personalized to the accepted fact basis. A missing dimension uses
`insufficient_basis`; it is never replaced with filler. The blueprint is a
controlled rendering contract and does not claim strict Dimension Coverage
Policy acceptance, Primitive membership, scoring, or threshold evaluation.

The internal Execution Report adds profile, assurance, analysis-basis,
configuration-limitation, and controlled-inference fields. A completed
controlled report sets `reasoning_allowed: true`, `narrative_allowed: true`,
and `current_stage: REPORT_VALIDATED`; those flags describe this execution
profile only and do not assert that strict semantic gates passed.

## 6. Failure and partial behavior

- Missing or invalid required input remains `BIRTH_INPUT_ERROR`.
- Missing the four baseline configs or an asset required for a claim that the
  agent cannot safely omit remains `CONFIG_GAP`.
- Missing advanced assets that can be safely bypassed become
  `CONFIG_LIMITATION` warnings in `controlled_inference`.
- Missing or incompatible calculation capability retains
  `CAPABILITY_GAP` or `METHODOLOGY_VERSION_MISMATCH`.
- Invocation and contract failures retain `CALCULATION_FATAL` and
  `CALCULATION_CONTRACT_ERROR`.
- `INFERENCE_GUARD_ERROR` stops a portrait when a claim lacks anchors, promotes
  reported facts to verified facts, hides a material limitation, or violates
  the fixed report contract.
- `partial` is permitted when the fact basis is valid but one or more report
  sections use `insufficient_basis`; it is not permission to fabricate content.

## 7. Compatibility and implementation boundary

Existing Python configuration loaders, strict bundles, fingerprints, and CLIs
remain unchanged because they continue to serve the `strict` profile. The main
implementation is a Skill contract and gate change, not a new inference engine.
The Skill still contains no calculator or executable dependency; the agent
performs external capability calls.

Existing strict tests remain as regression coverage. New tests verify the
profile branch, assurance rules, fixed long-form report structure, all 56
chapter dimensions, failure classification, status metadata, and absence of
production semantic assets or executable code.

## 8. Business-test readiness

The workflow is business-test ready when the Skill package validates, all tests
pass, and an executing environment has at least one qualified calculation
capability plus any required execution-scoped authorization. Readiness does not
mean the strict production profile is complete. Cross-agent business testing
measures fact fidelity, anchor coverage, framework adherence, disclosure,
section completeness, and harmful overclaiming; it does not require identical
prose.
