# Semantic Candidate Release Checklist

Use this checklist only for semantic assets explicitly supplied or placed in
scope by the user. Do not search unrelated projects or undeclared business
files.

The release states are:

```text
candidate -> validated -> reviewed -> approved -> promoted
```

## Candidate

- Keep candidate assets outside `configs/` while they are being authored.
- Treat examples as structure-only documentation. The agent must not generate
  or infer business semantics, and must not repair missing semantics from
  examples, model knowledge, or public conventions.
- Record the source and project owner for every candidate asset.

## Validated

- Validate the accepted runtime baseline first.
- Validate the candidate bundle in the exact order in
  [stage gates](stage-gates.md): Primitive foundation, Mapping registries,
  Dimension Coverage Policy, Narrative Rules, then relation endpoints.
- Every required asset and cross-reference must pass. A partial set remains a
  candidate and returns `CONFIG_GAP`.
- Record the validation report's `bundle_sha256`. Review and approval must refer
  to the same `bundle_sha256`; any digest change returns the asset set to `candidate`
  and requires validation and review again.
- Only a stable validation report may advance to human review. If the report
  states `configuration files changed during validation`, retry with an immutable candidate snapshot;
  do not review either observed version.
- Validation proves structural and cross-reference consistency only. It does
  not approve domain meaning and does not open `REASONING_ALLOWED`.
- A matching fingerprint proves byte identity only. It does not prove approval,
  domain correctness, reviewer identity, or gate completion.

## Reviewed

- A qualified human reviewer confirms provenance, methodology ownership,
  intended meaning, limitations, thresholds, and absence of placeholders.
- The reviewer confirms that no definition, mapping, score, dimension,
  threshold, interaction, or Narrative rule was invented by the agent.
- Record review evidence outside the production assets; never embed private
  discussion or credentials in the Skill.

## Approved

- Require explicit project-owner approval for the exact validated versions.
- Any content or version change after review returns the bundle to `candidate`.
- Approval of a semantic bundle does not waive any calculation configuration
  requirement and does not open `REASONING_ALLOWED` by itself.

## Promoted

- Promotion is a deliberate release operation outside this checklist. The agent
  must not copy candidate files into `configs/` without a separate, explicit
  project-owner instruction naming the approved versions and destination.
- After authorized promotion, revalidate the production bundle from its final
  location and retain the validation and approval evidence.
- Do not claim Gate 1 complete until every calculation and semantic gate passes
  independently.
