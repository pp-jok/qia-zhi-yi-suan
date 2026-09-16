# Portrait Report Contract

## Root contract

A controlled portrait uses `schema_version: portrait-report-v2` and contains
exactly these root fields in this order:

1. `schema_version`: `portrait-report-v2`
2. `execution_profile`: `controlled_inference`
3. `fact_assurance`: `project_verified` or `capability_reported`
4. `methodology_versions`: explicit Bazi and astrology versions
5. `capability_provenance`: accepted calculation-envelope references
6. `omitted_facts`: explicit fact identifiers or categories not used
7. `configuration_limitations`: every safely bypassed advanced asset and its
   effect on allowed claims
8. `format_profile`: `long-form-personality-book-v2`
9. `input_profile`: `compact-or-structured-birth-input-v1`
10. `content_standard`: `reader-first-depth-v2`
11. `sections`: the ordered report content below

Unknown root fields are invalid. Do not include raw credentials or sensitive
provider payloads.

## Long-form section order

Load the [Long-Form Report Blueprint](../references/long-form-report-blueprint.md)
before drafting. `sections` contains exactly:

1. `front_matter`
2. `prologue`
3. `part_1_chart_voice`
4. `part_2_personality_formation`
5. `part_3_shadow_protection_and_fate`
6. `part_4_integrated_portrait`
7. `finale`
8. `execution_notes`

The four parts contain all fifty-six blueprint chapters in order. A chapter
title is personalized to the accepted facts, while its `chapter_id` and
content dimension remain fixed. Do not substitute a short generic personality
summary for the book structure.

`front_matter` contains the title, subtitle, minimum birth-input summary, Bazi
main chart, Western astrology axes, and important structures. `prologue`
introduces the central cross-system question without completing the later
synthesis. `execution_notes` follows the reader-facing finale and contains
assurance, provenance, omissions, configuration limitations, and inference
disclosure.

Every analytical chapter contains at least one anchored Controlled Inference
claim or one exact `insufficient_basis` marker with a reason. Unsupported
chapters remain visible; they are never filled with generic prose.

A supported chapter normally uses three to five short paragraphs and makes at
least three distinct analytical moves from the blueprint's evidence,
mechanism, lived-expression, and integration layers. This is a semantic depth
requirement, not a mechanical word-count rule. A shorter chapter is valid only
when it marks the missing basis rather than replacing analysis with repetition,
generic advice, or invented biography.

For a completed, fully supported Chinese portrait, `reader-first-depth-v2`
calibrates the reader-facing book at 11,000 to 15,000 non-whitespace content
characters before the audit appendix. Chapters 01 through 55 normally contain
at least 120 CJK content characters each; chapter 56 is a concise five-question
recap. These ranges are regression guards against summary-style output, not
permission to add filler. An `insufficient_basis` chapter is exempt from the
chapter floor, remains visible, and makes the report `partial` when required by
the Execution Report contract.

## User-approved reference interpretation

A user may approve an external report as a supplemental interpretation source.
Such material never becomes a calculated fact. Preserve it on the relevant
claim as `supplemental_interpretation` with:

- `type`: `reference_traditional_interpretation`
- `source_ref`: an execution-local reference to the approved report
- `approval`: `user_approved`
- `basis_refs`: accepted calculated facts that do not conflict with the claim
- `limitations`: the missing methodology, lookup table, or independent check

The underlying controlled claim keeps its normal `claim_type`. A reference
interpretation must not override a conflicting calculated fact, fill a missing
birth input, satisfy a strict configuration gate, or change `fact_assurance`.
If the reference conflicts with accepted facts, omit the interpretation and
record the conflict in `execution_notes`. If it is compatible but lacks strict
configuration, render it as a traditional interpretive view rather than a
project-certified result.

In the rendered book, source qualification belongs in the audit appendix.
Reader-facing chapters may use the accepted traditional interpretation in
natural language, but they must not narrate approval state, source identifiers,
configuration gates, project verification, or assurance mechanics. Moving this
metadata out of the body never permits deleting it from the structured report
or audit appendix.

## Controlled-profile semantics

The blueprint dimensions are reader-facing coverage requirements. They do not satisfy the strict Dimension Coverage Policy, define Primitive membership,
produce Trait Salience or Synthesis Priority scores, activate the strict
Relation Graph, or certify a strict Core Dynamic.

Part I keeps Bazi and astrology independent until the designated first
cross-system synthesis chapter. Later chapters may synthesize both systems
only with anchors from both. Shadow, Mature, Fate, and Archetype language is
interpretive and must retain its supporting claim references:

- Shadow describes a possible strained expression, never a diagnosis.
- Mature describes an integrated possibility, never guaranteed behavior.
- Fate names a recurring tension, never a predicted event or outcome.
- Archetype is a symbolic title, never a scientific type or project taxonomy
  identifier.
- The finale renders only conclusions already established in the chapters.
- A `reference_traditional_interpretation` remains visibly source-qualified
  and cannot certify a strict Bazi strength, favorable element, dignity, or
  predictive conclusion.

## Reader and audit rendering

The main book follows the blueprint's short-paragraph narrative style. Internal
claim IDs, `basis_refs`, confidence, and limitations remain in the structured
report and may be rendered in the audit appendix rather than interrupting the
reader-facing prose. Moving them out of the prose must not delete them.

- Keep chart facts visually distinguishable from interpretation.
- Preserve contradictory signals as tensions instead of smoothing them away.
- Describe cross-system support only when both systems supply cited anchors.
- Do not mention internal `Pxxx` identifiers or absent rule IDs to the reader.
- State that the interpretation is traditional and inferential, not a
  scientific diagnosis, guaranteed behavior, or prediction.
- No required part, chapter dimension, disclosure, or explicit
  `insufficient_basis` marker may be removed for concision.

Failure to satisfy this contract is `INFERENCE_GUARD_ERROR`. The report cannot
reach `REPORT_VALIDATED` until the violation is removed by omitting unsupported
content or marking it `insufficient_basis`; never repair it with invented facts.
