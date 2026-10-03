# C2-SM P004 Bazi Neutral Relation Canonical Adoption Final Report

Date: 2026-10-04

## Baseline and implementation

The execution baseline was `main` at `84c7238fcec057be701ee412311adf7f5527fd64`
with open PR #2 at `1a41b3cbbd913b42442a6726cd16af52399d7f3c`.
PR #2 already provided the candidate policy, deterministic generator,
explicitly injected provider, Ten-God joins, rule-version provenance, codec
round-trip, and default isolation. This change did not duplicate them; it
hardened and reviewed them for canonical adoption.

The hidden-stem audit found accidental provider-order identity. A packaged,
versioned ordering table now governs all twelve branches. The explicit
reference provider normalizes equivalent input orders and remaps dependent
references; formal boundaries reject noncanonical stored facts. The subject
contract fixes visible and hidden templates, pillar vocabulary, source kinds,
and the ordering-policy dependency.

## Canonical relation boundary

`five_element_controls` has controller-first direction, arity two, and the
sole approved `wuxing-control-v1` version. Identity, deduplication, and ordering
are explicitly `(relation_type, participant_refs, rule_version)`;
`source_pillars` is provenance validated from resolved subjects. The validator
recomputes actual stem elements and rejects false control claims, unresolved
refs, unknown versions, duplicate identity, wrong provenance, and unstable
ordering.

The existing codec preserves identity, order, rule version, and source
provenance. The public qualified-facts loader now enforces the canonical
relation boundary. Fact assurance remains governed by the independent
qualification record and is not promoted by relation presence. Empty relation
collections, old providers producing no canonical relation, and unrelated
legacy relations remain compatible. Default provider/output and current
methodology versions are unchanged.

## Authority and semantic separation

The fact is school-neutral raw control presence. It cannot express effective
control, strength, rescue, exception, operative Dao-Shi, personality meaning,
P004 direction, or Primitive state. The canonical contract is authoritative;
the existing provider is only a conformance reference and is not wired into
production.

The canonical fact family is ready for a separate generic Evidence Root
proposal, but no Root is created here. The future Root must remain generic and
must not be named or scoped as a Dao-Shi conclusion.

## Fingerprints and verification

```text
Semantic Fingerprint:
256ba053b174a054226301f1b493e0e0c8f9f50e9f2976a72b8045dbf6ed6131

Presentation Fingerprint:
2f1d3866638074485351ada0c6a9aaa9bd1acd916f65973ca2b319a75b99b91d

Canonical Relation Policy Fingerprint:
b1fa64f2ed4b1255ddd245d4fbdf5b33c660939bf43a5934b638256e5a0295c9
```

The semantic and presentation fingerprints are unchanged. Focused tests cover
policy completeness, cross-provider normalization, Ten-God joins, canonical
identity/deduplication/order, actual control truth, governed rule versions,
codec and qualified import, default isolation, semantic separation, and legacy
compatibility. Full suite and installed-wheel verification are the release
gate.

## Machine-readable summary

```text
Semantic Core Foundation:
FROZEN

P004 Astrology:
CLOSED_UNDER_CURRENT_HELLENISTIC_METHODOLOGY

P004 Bazi Initiation:
SATURATED

P004 Bazi Pre-action Low:
SATURATED

P004 Bazi Advancement Construct:
DIRECT_LIMITATION_FOUND

Dao-Shi Semantic Claim:
READY / ACCEPTED_FOR_REVIEW

Dao-Shi Method:
NOT_READY

BMC-BZ-P004-DAO-SHI-V1:
NOT_READY

Neutral Relation Candidate:
HISTORICAL_SUPERSEDED

Hidden Stem Identity:
READY

Subject Ref Contract:
READY

five_element_controls:
CANONICAL

deterministic_facts.bazi.relations:
CANONICAL

Canonical Provider Authority:
CONFORMANCE_REFERENCE_ONLY

Default Production Provider:
UNCHANGED

Fully Resolved Method Questions:
0

Partially Resolved Method Questions:
8

Unresolved Method Questions:
2

Not Fully Resolved Method Questions:
10

Evidence Root Proposal Readiness:
READY

Evidence Root:
0

Proposed PRIMARY_EVIDENCE:
0

Approved PRIMARY_EVIDENCE:
0

PRIMARY_EVIDENCE:
0

Mapping Proposals:
0

Approved Mappings:
0

Mapping:
0

Production Activation:
NOT AUTHORIZED

Next Gate:
GENERIC_BAZI_RELATION_EVIDENCE_ROOT_PROPOSAL
```
