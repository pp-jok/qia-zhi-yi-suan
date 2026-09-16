# Narrative Rules Template — Non-Production

This document **must not be loaded as runtime configuration**, copied into
`configs/`, or renamed to `narrative_rules_v1.yaml`.

```yaml
schema_version: narrative-rules-v1
narrative_version: <PROJECT_OWNED_VERSION>
ontology_version: <MATCH_APPROVED_ONTOLOGY_VERSION>
dimension_policy_version: <MATCH_APPROVED_DIMENSION_POLICY_VERSION>
sections: [<PROJECT_OWNED_SECTION_ID>]
invariants:
  complete_ir_required: true
  narrative_changes_core_claims: false
  unsupported_claims_allowed: false
  unknown_may_be_rendered_as_certain: false
  secondary_may_be_promoted: false
  chart_anchor_required: true
  traditional_interpretation_claimed_scientific: false
rules:
  - rule_id: <PROJECT_OWNED_RULE_ID>
    priority: <PROJECT_OWNED_PRIORITY>
    target_section: <MATCH_SECTION_ID>
    source_kinds: [<APPROVED_SOURCE_KIND>]
    requires_chart_anchor: true
    rendering_constraints: {<PROJECT_OWNED_KEY>: <PROJECT_OWNED_VALUE>}
    prohibited_inferences: [<PROJECT_OWNED_PROHIBITION>]
    limitations: []
```

The template supplies no approved prose or semantic rule.
