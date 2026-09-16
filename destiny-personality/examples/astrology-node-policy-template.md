# Astrology Node Policy Template — Non-Production

This authoring aid **must not be loaded as runtime configuration**, copied into
`configs/`, or renamed to `astrology_node_policy_v1.yaml`.

```yaml
schema_version: astrology-node-policy-v1
policy_version: <PROJECT_OWNED_POLICY_VERSION>
methodology_version: <ACCEPTED_ASTROLOGY_METHODOLOGY_VERSION>
vocabulary_version: <ACCEPTED_VOCABULARY_VERSION>
node_id: <CANONICAL_ASTROLOGY_NODE_ID>
output:
  included: <BOOLEAN_DECISION>
  phase: <PROJECT_OWNED_PHASE>
  aspect_participation: <BOOLEAN_DECISION>
  dignity_participation: <BOOLEAN_DECISION>
  weight_role: <PROJECT_OWNED_WEIGHT_ROLE>
  time_sensitive: <BOOLEAN_DECISION>
```

Angle-bracket tokens are deliberately invalid; the template makes no node
decision.
