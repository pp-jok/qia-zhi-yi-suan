# C2-SK Semantic Knowledge Governance Hardening

## Problem and migration

The first-pass registry used parallel `source_refs` / `source_locators` and `conflicting_claim_refs`. That made source-to-locator pairing ambiguous and misclassified a qualifier as a contradiction. The candidate-only v1 registry now uses:

- `citations`: each object binds `source_ref`, claim-specific `locator`, and `support_role`.
- `related_claims`: each object binds `claim_ref` and a directed relation of `supports`, `qualifies`, `contradicts`, `contextualizes`, or `limits`.

The loader fail-closes unknown citation sources, blank locators, unsupported support roles, unknown related claims, self-references, duplicate relations, and unsupported relation types.

## Quality policy

`semantic_knowledge_source_quality_policy_v1.yaml` defines Tier A/B/C/Rejected by authority, traceability, stability, methodological clarity, and school clarity. It separately encodes `evidence_nature`: traditional methodology, project normative, or empirical. This prevents a traditional technical source from being represented as empirical research; source quality remains distinct from claim support and scientific validity.

## P004 result

The aspect-methodology claim now `qualifies` and `limits` the Mars action/initiative claim. It does not contradict it. Joey Yap remains Tier B, Houlding sources Tier B, the project ontology Tier A normative-only, and Alsayed is recalibrated to Tier C because its self-published provenance is limited. No source or claim status creates a Mechanism.

## Guarantees

All registries remain `candidate_only` / inactive. Root count is 3 (2 approved, 1 proposed); approved mechanisms and Mapping Proposals remain zero. No Foundation component or active runtime asset changed.
