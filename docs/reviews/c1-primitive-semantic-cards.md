# C1 Primitive Semantic Cards

## Shared negative rules

Absence is not opposition; unknown is not low; conflicting local evidence is not automatically mixed; local evidence is not global evidence; a modifier is not a Primitive; behavior is not a trait; and presentation wording is not semantic state.

| ID | Canonical axis and question | High / low | Mixed / unknown | Excluded meanings and neighbors |
|---|---|---|---|---|
| P001 | Self-directed judgement: how strongly is judgement organized from one's own internal criteria? | High: self-directed judgement. Low: reliance on explicit external roles, guidance, or frameworks. | Mixed requires valid opposite evidence on the same scope; unknown is insufficient permitted judgement evidence. | Excludes action speed, rebellion, change preference, social distance. Neighbors: P004 action, P003 affiliation. |
| P002 | Preference for predictability: how much is stability and explicit expectation preferred? | High: stable, clear, predictable structure. Low: openness to change and lower certainty. | Mixed requires same-scope support for both; unknown is no valid stability-direction evidence. | Excludes responsibility, organizational skill, risk morality. Neighbors: P006 structure, P004 action. |
| P003 | Relational responsiveness: how much are relational feeling, response and coordination prioritized? | High: responsive coordination. Low: independent relational handling. | Mixed requires opposing relational evidence; unknown is not absence of relationships. | Excludes autonomy, sociability, attachment diagnosis. Neighbor: P001. |
| P004 | Action initiation: how readily is concrete action started and advanced? | High: initiates and advances action. Low: preserves observation, preparation, or waiting. | Mixed requires same-scope activation and restraint; unknown is no action evidence. | Excludes judgement ownership, impulsivity, achievement. Neighbor: P001. |
| P005 | Affect regulation orientation: how is affect preferentially held or processed? | High: uses boundary, structure, regulation. Low: permits open, flowing affect. | Mixed requires opposite regulation evidence; unknown is not emotional absence. | Excludes intensity, pathology, relationship need. Neighbor: P006. |
| P006 | Organizational orientation: how strongly are activity and tasks organized through order and structure? | High: order, organization, structure. Low: flexibility and fewer presets. | Mixed requires same-scope structured and flexible organization evidence; unknown is no organization evidence. | Excludes stability need, responsibility, control morality. Neighbors: P002, P005. |

## Context and promotion

Valid current contexts are decision, work, pressure, relationship, change, and action. Local evidence is `LOCAL_ONLY` by default. `MULTI_CONTEXT_SUPPORT` needs consistent evidence in at least two independent contexts. `GLOBAL_ELIGIBLE` additionally needs a mapping rule explicitly marked global-capable. `GLOBAL_BLOCKED` applies to relationship-only, pressure-only, or modifier-only evidence. Different local directions remain contextual variation unless same-scope evidence supports both directions; they must not become global mixed automatically.

## Counter evidence

Counter evidence is valid permitted evidence for the opposite direction in the same Primitive/scope. Non-evidence includes missing facts, unavailable time-sensitive facts, excluded facts, and evidence owned by a neighbor. Source-system identity is provenance only and never changes Primitive meaning.
