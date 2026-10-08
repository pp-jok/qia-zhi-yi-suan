# Execution Report Contract

Produce one report for `portrait`, `facts_only`, and `audit`.

## Required fields

- `schema_version`: use `execution-report-v1`.
- `mode`: `portrait`, `facts_only`, or `audit`.
- `requested_mode`: the user route: `standard-interpretive-v1`,
  `concise-interpretive-v1`, `legacy`, `core`, `core_concise`,
  `core_standard`, `facts_only`, `audit`, or `research`.
- `portrait_route`: `audited_interpretive`, `legacy`, `formal_core`, or
  `candidate_core` when `mode` is `portrait`; otherwise `not_applicable`.
- `renderer_profile`: `standard-interpretive-v1`,
  `concise-interpretive-v1`, `structured`, `concise`, `standard`, or
  `not_applicable`; it is a renderer selection, not an execution lifecycle mode.
- `execution_profile`: `audited_interpretive`, `controlled_inference`, or
  `strict`.
- `status`: `completed`, `partial`, or `stopped`.
- `current_stage`: last successfully reached state, or the failed state when stopped.
- `reasoning_allowed`: explicit boolean.
- `narrative_allowed`: explicit boolean.
- `input_summary`: minimum data needed to identify the audited execution; avoid unnecessary personal-data duplication.
- `capabilities`: list of discovered candidates. Each item requires `candidate_id`, `category`, `qualification_status`, `independence_status`, `authorization_state`, and `invocation_status`.
- `provenance`: list containing only accepted operations and their calculation-envelope references; use an empty list before any accepted operation.
- `validated_facts`: a `fact_packet_ref` to a validated packet or the minimal validated packet itself; use an empty mapping when none passed.
- `fact_assurance`: `project_verified`, `capability_reported`, or `none`.
- `interpretive_rule_bundle_refs`: versioned packaged traditional-rule bundle
  references used by `audited_interpretive`; use an empty list on other routes.
- `interpretive_profile_ref`: validated audited-interpretive profile reference,
  or `not_applicable` when that route did not run.
- `interpretive_report_ref`: validated `interpretive-report-v1` reference, or
  `not_applicable` when that route did not render.
- `audit_target_ref`: immutable reference to the supplied object or evidence
  bundle for `audit`/`research`; otherwise `not_applicable`.
- `strict_stage_result_refs`: ordered strict-gate result records for
  `audit`/`research`. Each record contains `stage`, `status` (`passed` or
  `failed`), and non-empty `evidence_refs`; use an empty list on other routes.
- `audit_result_ref`: immutable reference to the persisted strict
  audit/research result; otherwise `not_applicable`.
- `core_profile_ref`: validated `core-destiny-profile-v1` reference or
  `not_applicable` when the Core Profile route did not run.
- `semantic_model_assurance`: `project_semantic_verified`,
  `project_semantic_partial`, `none`, or `not_applicable` outside the Core
  Profile route.
- `semantic_model_versions`: version references for Semantic Core assets
  actually used; use an empty mapping when no Core Profile was built.
- `report_plan_ref`: validated `report-plan-v1` reference or `not_applicable`
  when no Core Profile renderer plan was built.
- `analysis_basis`: references to the fact items that analytical claims may
  use; empty outside a personality-producing portrait route.
- `configuration_limitations`: safely bypassed advanced assets and the claims omitted because of them; empty in a complete strict execution.
- `inference_disclosure`: the selected interpretive profile's traditional,
  inferential, and non-diagnostic disclosure; `not_applicable` outside an
  interpretive profile.
- `issues`: ordered list of errors and warnings that affect progression.
- `warnings`: non-blocking execution warnings.
- `next_action`: concrete requirement for completion or `none`.

Each `issues` item requires `code`, `severity`, `stage`, `message`, and `required_action`, and may include `subtype`. Use `fatal` or `warning` for `severity`; use `subtype: external_result_conflict` for a cross-capability contract conflict.

Exclude raw sensitive payloads and credentials from the report. Refer to accepted data through envelope and fact-packet references instead of duplicating it. An `authorization_state` records only the execution-scoped decision, never a credential or reusable secret.

## Route result requirements

| execution_profile | portrait_route | requested_mode | Required result fields |
| --- | --- | --- | --- |
| `audited_interpretive` | `audited_interpretive` | `standard-interpretive-v1` or `concise-interpretive-v1` | `interpretive_profile_ref`, `interpretive_report_ref`, `interpretive_rule_bundle_refs` |
| `controlled_inference` | `legacy` | `legacy` (including the literal `portrait` compatibility alias) | `analysis_basis`, `configuration_limitations`, `inference_disclosure` |
| `strict` | `formal_core` or `not_applicable` | `facts_only`, `audit`, `research`, or explicit project-rule certification | for audit/research: `audit_target_ref`, `strict_stage_result_refs`, `audit_result_ref`, and `issues`; interpretive result fields remain `not_applicable` or empty |

## Strict audit/research result contract

Evaluate only stages claimed by the supplied target, in the existing strict
gate order. Record exactly one stage-result entry per evaluated claimed gate;
stop at the first failure and never add entries for an unclaimed or later gate.
An audit/research execution never grants reasoning or Narrative permission.

| Outcome | status | current_stage | Required references | Permission flags |
| --- | --- | --- | --- | --- |
| `all_claimed_stages_pass` | `completed` | highest claimed strict gate that passed; `SCOPE_CHECKED` if no strict branch gate was claimed | `audit_target_ref`, `audit_result_ref`, ordered `strict_stage_result_refs` for every claimed gate | both `false` |
| `first_claimed_stage_fails` | `stopped` | first failed claimed strict gate | `audit_target_ref`, `audit_result_ref`, ordered `strict_stage_result_refs` through the failed gate, and `issues` | both `false` |

## Cross-field rules

- For `stopped`, set both permission flags to `false` unless the stop occurs after a previously completed allowed stage in `audit`; explain that scope in `issues`.
- In `strict`, use `partial` only when semantic rule assets are complete but case-specific Mapping coverage is below the frozen provisional threshold.
- In `audited_interpretive`, require independently qualified facts and the
  packaged versioned rule bundle. A completed report requires non-empty
  `interpretive_profile_ref`, `interpretive_report_ref`, and
  `interpretive_rule_bundle_refs`.
- In `controlled_inference`, use `partial` only when the fact basis is valid but at least one required analytical section is `insufficient_basis`.
- For `facts_only`, complete at `FACTS_VALIDATED`, keep both permission flags `false`, and omit personality IR and Narrative.
- For `audit` or `research`, use `strict`, set `portrait_route` and all
  interpretive/Core result fields to `not_applicable` (or their documented
  empty value), and apply the strict audit/research result contract exactly;
  never calculate, repair, or advance the supplied target.
- For an audited portrait, add the audited profile only after
  `INTERPRETIVE_PROFILE_VALIDATED`; for legacy or strict portraits, retain the
  existing `REASONING_ALLOWED` and `NARRATIVE_ALLOWED` requirements.
- A Core Profile route adds `core_profile_ref` only after
  `CORE_PROFILE_VALIDATED`, and `report_plan_ref` only after
  `REPORT_PLAN_VALIDATED`. Neither reference upgrades `fact_assurance`.
- For a completed audited portrait, set `reasoning_allowed: true`,
  `narrative_allowed: true`, and `current_stage: REPORT_VALIDATED` only after
  every conclusion has signal provenance and the report audit metadata retains
  fact, qualification, rule-bundle, and profile references. These permissions
  are `audited_interpretive`-scoped and do not claim any strict semantic gate.
  Unknown birth time must omit hour/house/angle-dependent claims and add the
  reduced time-scope limitation.
- For a completed controlled portrait, set `reasoning_allowed: true`, `narrative_allowed: true`, and `current_stage: REPORT_VALIDATED` only after both controlled checklists pass. This permission is profile-scoped and does not claim `SEMANTIC_CONFIG_CHECKED` or strict rule approval.
- A user-facing response may summarize the report, but retain the complete structure for audit.
