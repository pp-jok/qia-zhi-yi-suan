# C2 Semantic Evidence Root Review v1

## Registry state

```text
Registry: candidate-semantic-evidence-root-registry-v1
Review status: candidate_only
Root count: 2
Approved root count: 2
```

An empty registry was the valid initial Phase 1 state. Phase 2A admits exactly
two project-owned fact-identity roots; the registry does not treat any other
canonical facts, legacy rules, or Golden Samples as roots by default.

| Root ID | Scope | Approved use |
|---|---|---|
| `ER-BZ-TEN-GOD-INSTANCE-V1` | Ten-God instance identity: subject, Ten God, source pillars, source kind | Identification and candidate-mechanism evidence reference only. |
| `ER-AS-ASPECT-INSTANCE-V1` | Aspect instance identity: bodies, aspect type, orb | Identification and candidate-mechanism evidence reference only. |

Both entries prohibit direct Primitive-state assertions and Mapping-rule
creation. They are descriptors of deterministic fact identity, not semantic
mechanisms or personality conclusions.

## Admission requirements

A future root entry must have a stable `evidence_root_id`, source scope,
provenance, review record, exclusions, and an explicit Product Owner review
state. The loader rejects malformed registry entries. Only entries marked
`approved` are returned as usable root identifiers; all other states remain
unusable and fail closed for mechanism validation.

## Review questions

Before approval, review must establish:

1. The source condition is project-owned and independently identifiable.
2. Its semantic scope and exclusions are recorded without relying on an output
   outcome.
3. Its provenance is not Golden Sample-derived and cannot reintroduce a legacy
   rule under a new name.
4. It is suitable only as evidence for stated Primitive questions, not as a
   direct claim about a user's Primitive state.

## Authority boundary

Adding a root record does not approve it. Product Owner approval is required
before any Semantic Mechanism can reference it. Root approval alone does not
approve a mechanism or a mapping.
