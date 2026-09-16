# Execution Report Contract

Produce one report for `portrait`, `facts_only`, and `audit`.

## Required fields

- `schema_version`: use `execution-report-v1`.
- `mode`: `portrait`, `facts_only`, or `audit`.
- `execution_profile`: `controlled_inference` or `strict`.
- `status`: `completed`, `partial`, or `stopped`.
- `current_stage`: last successfully reached state, or the failed state when stopped.
- `reasoning_allowed`: explicit boolean.
- `narrative_allowed`: explicit boolean.
- `input_summary`: minimum data needed to identify the audited execution; avoid unnecessary personal-data duplication.
- `capabilities`: list of discovered candidates. Each item requires `candidate_id`, `category`, `qualification_status`, `independence_status`, `authorization_state`, and `invocation_status`.
- `provenance`: list containing only accepted operations and their calculation-envelope references; use an empty list before any accepted operation.
- `validated_facts`: a `fact_packet_ref` to a validated packet or the minimal validated packet itself; use an empty mapping when none passed.
- `fact_assurance`: `project_verified`, `capability_reported`, or `none`.
- `analysis_basis`: references to the fact items that analytical claims may use; empty outside a controlled portrait.
- `configuration_limitations`: safely bypassed advanced assets and the claims omitted because of them; empty in a complete strict execution.
- `inference_disclosure`: the controlled profile's traditional, inferential, and non-diagnostic disclosure; `not_applicable` outside that profile.
- `issues`: ordered list of errors and warnings that affect progression.
- `warnings`: non-blocking execution warnings.
- `next_action`: concrete requirement for completion or `none`.

Each `issues` item requires `code`, `severity`, `stage`, `message`, and `required_action`, and may include `subtype`. Use `fatal` or `warning` for `severity`; use `subtype: external_result_conflict` for a cross-capability contract conflict.

Exclude raw sensitive payloads and credentials from the report. Refer to accepted data through envelope and fact-packet references instead of duplicating it. An `authorization_state` records only the execution-scoped decision, never a credential or reusable secret.

## Cross-field rules

- For `stopped`, set both permission flags to `false` unless the stop occurs after a previously completed allowed stage in `audit`; explain that scope in `issues`.
- In `strict`, use `partial` only when semantic rule assets are complete but case-specific Mapping coverage is below the frozen provisional threshold.
- In `controlled_inference`, use `partial` only when the fact basis is valid but at least one required analytical section is `insufficient_basis`.
- For `facts_only`, complete at `FACTS_VALIDATED`, keep both permission flags `false`, and omit personality IR and Narrative.
- For `audit`, validate only the supplied object's claimed stages; never calculate, repair, or advance it.
- For `portrait`, add personality IR only after `REASONING_ALLOWED` and Narrative only after `NARRATIVE_ALLOWED`.
- For a completed controlled portrait, set `reasoning_allowed: true`, `narrative_allowed: true`, and `current_stage: REPORT_VALIDATED` only after both controlled checklists pass. This permission is profile-scoped and does not claim `SEMANTIC_CONFIG_CHECKED` or strict rule approval.
- A user-facing response may summarize the report, but retain the complete structure for audit.
