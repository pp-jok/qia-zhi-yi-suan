# Stage Gate Checklist

Advance only after every condition for the selected execution profile passes.

## Shared entry

1. `INPUT_RECEIVED`: required mode input is present.
2. `SCOPE_CHECKED`: preflight scope, profile, and authorization rules pass.
3. `CALCULATION_BASELINE_CHECKED`: the four frozen baseline YAML files, birth/time rules, capability contracts, deterministic-fact contract, controlled-inference contract, and report contracts are present and internally consistent.

## Controlled portrait branch

4. `CAPABILITIES_DISCOVERED`: at least one capability descriptor exists for every required calculation category, without silent installation or connection.
5. `METHODOLOGY_VERIFIED`: every applicable compatibility-evidence item for the selected capability is `exact`.
6. `FACTS_CALCULATED`: qualified and authorized invocations completed and each accepted operation has a calculation envelope.
7. `FACTS_NORMALIZED`: source output was converted mechanically without deriving, repairing, translating an unknown alias, or inventing a fact.
8. `FACT_BASIS_VALIDATED`: method versions, provenance, structure, ranges, internal consistency, and `stable_only` exclusions pass; assurance is explicitly `project_verified`, `capability_reported`, or `none`.
9. `CONTROLLED_INFERENCE_CHECKED`: assurance is not `none`, every intended analytical claim can satisfy the controlled-inference contract, and all missing advanced assets are either required and fatal or safely omitted and recorded as limitations.
10. `CONTROLLED_INFERENCE_ALLOWED`: anchored interpretation may begin; this does not assert `SEMANTIC_CONFIG_CHECKED` or strict rule approval.
11. `REPORT_VALIDATED`: the fixed portrait report is complete, every analytical section is anchored or marked `insufficient_basis`, and all disclosures are present.

The five advanced calculation assets remain absent and mandatory for the strict profile. In the controlled profile, their absence is non-fatal only when every dependent claim is omitted. The agent must never create substitute tables, aliases, node rules, margins, or tolerances.

## Strict branch

4. `CALCULATION_CONFIG_CHECKED`: require the exact project-owned assets in this order: `canonical_fact_vocabulary_v1.yaml`, then the deterministic lookup tables in `bazi_deterministic_tables_v1.yaml` and `astrology_dignity_table_v1.yaml`, followed by `astrology_node_policy_v1.yaml` and `fact_comparison_policy_v1.yaml`.
5. `CAPABILITIES_DISCOVERED`: at least one capability descriptor exists for every required category, without silent installation or connection.
6. `METHODOLOGY_VERIFIED`: every applicable compatibility-evidence item is `exact`.
7. `FACTS_CALCULATED`: all necessary qualified and authorized invocations completed.
8. `FACTS_NORMALIZED`: accepted results were converted mechanically into the deterministic-facts contract.
9. `FACTS_VALIDATED`: each normalized packet independently passes completeness, ranges, sources, methodology version, provenance, `stable_only`, and mandatory comparison checks.
10. `SEMANTIC_CONFIG_CHECKED`: Ontology, Mapping, Primitive State, score, relation, dimensions, coverage policy, and Narrative assets are complete and cross-reference valid.
11. `REASONING_ALLOWED`: strict structured reasoning may begin; Narrative remains forbidden.
12. `NARRATIVE_ALLOWED`: complete strict IR exists and Narrative may render it without adding claims.

## Mode terminals

- `facts_only`: use `strict`, finish after `FACTS_VALIDATED`, and keep both permission flags false.
- `audit`: verify only the supplied evidence and the profile it claims; never calculate, repair, invoke, or advance it.
- `portrait` with `controlled_inference`: finish at `REPORT_VALIDATED`.
- `portrait` with `strict`: continue through `NARRATIVE_ALLOWED` only when every strict gate passes.

On fatal failure, record the failed gate and do not evaluate later gates. In the controlled branch, `partial` is allowed only for valid fact basis plus an `insufficient_basis` report section. In the strict branch, `partial` retains its existing `coverage_warning` meaning.

For the Primitive foundation portion of `SEMANTIC_CONFIG_CHECKED`, require the
real `primitive_ontology_v1.yaml` first, then
`primitive_state_resolution_v1.yaml`. Validate both contracts and their version
references before validating remaining semantic assets. Documentation examples
never satisfy an asset requirement; if any production asset is absent, return
`CONFIG_GAP` and keep Gate 1 closed.

After the real Primitive foundation passes, require
`bazi_mapping_registry_v1.yaml` and then
`astrology_mapping_registry_v1.yaml`. Validate the shared Context-Aware Mapping
contract, ontology and methodology versions, Primitive output references,
source-system isolation, and same-registry Interaction references. Documentation
templates never satisfy either asset. Missing or invalid production registries
return `CONFIG_GAP` under the ordered failure policy and keep Gate 1 closed.

After both registries pass, require `dimension_coverage_policy_v1.yaml` and
validate exactly twelve dimensions, ontology and score versions, Primitive
references, provisional frozen thresholds, and one bounded requirement per
dimension. A configuration failure is never `coverage_warning`; return
`CONFIG_GAP` and keep Gate 1 closed. Only case-specific low coverage after all
semantic configuration passes may produce `coverage_warning` and `partial`.

Then require `narrative_rules_v1.yaml`, validate its ontology and dimension
versions, fixed no-new-claims invariants, section coverage, source kinds, and
chart anchors. Validate relation-graph endpoints against the accepted ontology
last. Because earlier calculation assets remain independently required,
semantic bundle acceptance never opens `REASONING_ALLOWED` by itself.
