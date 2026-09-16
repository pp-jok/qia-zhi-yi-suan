# Controlled Inference Contract

Use this contract only for a `portrait` execution whose `execution_profile` is
`controlled_inference`. It permits constrained interpretation, not language-
model chart calculation.

## Fact assurance

Assign exactly one `fact_assurance` value before interpretation:

- `project_verified`: every applicable strict calculation configuration and
  deterministic validation rule passed;
- `capability_reported`: a qualified external capability supplied the facts,
  and methodology, provenance, structure, ranges, internal consistency, and
  time sensitivity passed, but missing project assets prevented independent
  re-derivation;
- `none`: there is no usable fact basis and inference is forbidden.

The agent must not promote `capability_reported` to `project_verified`, describe
it as independently verified, or emit a `deterministic-facts-v1` certification.
Retain unknown provider labels with their provenance instead of guessing an
alias. If the node policy is absent, omit every node claim and every conclusion
that depends on one. If comparison policy is absent, do not claim that another
source confirms, corrects, or resolves the primary source.

## Analytical claim record

Every claim contains exactly:

- `claim_id`: execution-unique non-empty identifier;
- `claim`: the human-readable conclusion;
- `claim_type`: `observation`, `inference`, or `synthesis`;
- `systems`: a non-empty unique list containing `bazi`, `astrology`, or both;
- `basis_refs`: a non-empty unique list of fact-basis identifiers;
- `confidence`: `high`, `medium`, or `low`;
- `limitations`: an explicit list of material qualifications, possibly empty.

An `observation` restates or groups supplied facts without inventing a new chart
fact. An `inference` requires at least one fact-basis reference. A `synthesis`
requires at least two fact-basis references and may claim cross-system support
only when `systems` contains both `bazi` and `astrology` and the references
actually include each system.

## Interpretation rules

- The agent must not calculate chart facts, repair them, fill omitted fields,
  translate unknown aliases, or turn narrative plausibility into fact evidence.
- Unknown or omitted facts are not negative evidence.
- Contradictory signals remain visible as tension, context, or uncertainty; do
  not average, union, or silently discard them.
- Wording and emphasis may vary across agents. Fact identity, assurance,
  anchors, and disclosed limitations may not.
- Do not invent `Pxxx` identifiers, Mapping rules, frozen scores, rule IDs, or
  claims that absent semantic assets approved the result.
- Do not make a medical or psychological diagnosis, claim scientific certainty,
  guarantee behavior, or guarantee a future event.

## Gate result

Pass `CONTROLLED_INFERENCE_CHECKED` only when assurance is not `none`, every
planned claim can satisfy this contract, and all material configuration
limitations are recorded. A violation is `INFERENCE_GUARD_ERROR` and prevents
`CONTROLLED_INFERENCE_ALLOWED`.
