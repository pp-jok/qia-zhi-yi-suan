# Independent Fact Comparison Contract

## Packet

`fact-comparison-v1` records the result of comparing two independently valid
deterministic fact packets. Required top-level fields are `schema_version`,
`primary_packet_ref`, `secondary_packet_ref`, `independence_evidence`,
`comparison_policy_version`, `field_results`, `material_conflicts`, and
`comparison_status`.

`schema_version` is `fact-comparison-v1`. Packet references identify the two
accepted `deterministic-facts-v1` packets. `independence_evidence` qualifies
the secondary result for the affected logical category. `field_results` records
policy-authorized field comparisons, and `material_conflicts` records only
differences declared material by the versioned policy.

## Preconditions and policy

The ordinary case requires one qualified result for each required logical
category. A second result is mandatory when the primary result reports a
warning, uncertainty, or boundary sensitivity; when there is historical-time
ambiguity; when a result falls within a configured boundary margin; or when a
versioned policy identifies a policy-recognized anomaly. Each trigger requires
a second qualified result for every affected logical category.

One capability may cover multiple logical categories. That does not make two
results independent: independence is established separately for the affected
category from capability and provenance evidence before the secondary
invocation.

Check the versioned comparison policy before the secondary invocation. The
complete comparison strategy, including applicable fields and category-specific
qualification requirements, must be fixed before the secondary invocation.
Missing applicable boundary margins, alias rules, canonical precision, or
numerical tolerances are `CONFIG_GAP` and prevent the call.

The secondary result must be qualified and independent for the affected logical
category. Compare two packets only after each independently passes its own fact
contract. A primary packet that fails its fact contract is a
`CALCULATION_CONTRACT_ERROR`; a secondary result must not be invoked to repair
or replace it.

## Comparison rules

Representation-only equivalence is allowed solely by the versioned comparison
policy. Do not average positions, union categorical facts, choose a preferred
result by intuition, or use comparison to repair an invalid primary packet.
No implementation may invent lookup tables, aliases, boundary margins,
precision, thresholds, or tolerances.

A material difference sets `comparison_status` to `conflict` and returns
`CALCULATION_CONTRACT_ERROR` with subtype `external_result_conflict`.
Otherwise, `comparison_status` is determined only by the versioned policy and
the recorded `field_results`.
