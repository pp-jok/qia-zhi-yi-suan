# Semantic Bridge Governance and P006 Pilot Design

## Purpose

Add a narrow, machine-auditable governance layer for translating a
source-backed traditional behavioural process into an approved modern
Primitive direction. Reopen only P006, preserve the v0.4.1 direct-construct
closure as historical truth, and follow the pilot exit rules without lowering
the Evidence Root, PRIMARY_EVIDENCE, Mapping, context, or scientific-boundary
gates.

## Baseline and approved interpretation

The baseline is main `81e4e6389c1196be45baf09734280924b882e27e`, release
v0.4.1, six formal `unknown` Primitive states, zero PRIMARY_EVIDENCE, and zero
active Mapping.

The attached execution specification is treated as the approved product design
and autonomous authorization. Its central correction is valid: a traditional
source need not use a modern Primitive name. A project-owned Semantic Mechanism
may translate an explicit behavioural process, but it may not translate a
symbol, capability, role, temperament adjective, or outcome merely because the
wording feels similar.

## Alternatives considered

### 1. Documentation-only policy

Rejected. A prose policy would not prevent a later agent or candidate asset
from approving capability wording or symbolic analogy as PRIMARY_EVIDENCE.

### 2. Minimal policy asset plus existing-mechanism enforcement

Selected. Add one versioned Semantic Bridge policy and focused validation
functions beside the existing Semantic Mechanism validator. Approved
PRIMARY_EVIDENCE must carry a passing bridge audit. No new runtime stage,
registry family, score, or renderer logic is introduced.

### 3. Full Bridge subsystem

Rejected. A new registry, resolver, persistence model, and runtime layer would
duplicate Claim, Semantic Mechanism, PRIMARY_EVIDENCE, and Mapping ownership.

## Bridge policy

Create `candidates/semantic-core-v1/semantic_bridge_policy_v1.yaml` with six
classes:

- `DIRECT_CONSTRUCT_BRIDGE`: admissible when the source process and Primitive
  process are materially isomorphic.
- `BEHAVIORAL_MECHANISM_BRIDGE`: admissible when the source explicitly describes
  repeated person-level behaviour or process and every admission gate passes.
- `CAPABILITY_OR_ROLE_BRIDGE`: rejected by default.
- `TEMPERAMENT_BRIDGE`: rejected by default.
- `OUTCOME_BRIDGE`: rejected.
- `ANALOGICAL_SYMBOLIC_BRIDGE`: rejected.

The ten mandatory gates are source-behaviour explicitness, subject match,
process match, Primitive ownership, direction entailment, context match,
alternative-interpretation resolution, traditional-method reproducibility,
counterevidence definition, and scientific-boundary declaration.

A Bridge audit record contains:

- `bridge_id`, `bridge_class`, `source_claim_refs`, and `source_behavior`;
- `subject_kind` and `process_meaning`;
- `primitive_id`, `primitive_ownership_rationale`, and `direction_rationale`;
- `direction` and `contexts`;
- `alternative_interpretations` and `excluded_interpretations`;
- `traditional_method_status`;
- `counterevidence`;
- `scientific_boundary`;
- `admission_gates` with all ten gate results.

An admissible semantic bridge may be recorded as semantically valid while its
method is blocked, but an approved PRIMARY_EVIDENCE mechanism requires both an
admissible class and `traditional_method_status: reproducible`. A Bridge never
asserts Primitive state directly.

## Direction and context semantics

High and Low discovery are independent. One admitted High mechanism does not
require a Low mechanism, and the absence of High or Low is never evidence for
the other direction.

This does not relax scope. A Mapping that declares only `work` remains local.
The candidate semantic resolver must expose it as `context_differentiated`
unless the evidence is explicitly global or passes the existing promotion
policy. A single local High mapping therefore preserves a valid work-context
High while not claiming global P006 High.

## P006 pilot result

The exact candidate contexts support Exit C, not activation:

- `处事有方` occurs as a favourable whole-chart character/capability judgement.
  It states effective handling, not a preference for pre-set task structure.
- `治事无规` occurs in `木归蹇地，太柔而治事无规`. It is a negative judgement
  about lacking method/order under unresolved technical conditions, not a
  preference for flexible organization. It cannot establish P006 Low.
- `布置有方` is a later whole-chart case conclusion about competence in handling
  major affairs. It does not isolate a repeated organizational orientation.
- Ptolemy's `able to direct business` is explicitly capability language.
- `systematic workers` occurs inside a mixed Mars-Mercury character list that
  also contains skill, success, trickery, instability, and harmful conduct. It
  does not isolate pre-set task arrangement or exclude competence/occupation.
- `prone to change their minds` is temperament/decision instability, not a
  flexible task-organization preference.

All P006 candidates fail Gate 3, Gate 4, or Gate 7 before method activation.
The result is `P006_BEHAVIORAL_BRIDGE_FAIL_CAPABILITY_OR_TEMPERAMENT_ONLY`, with
zero PE, zero Mapping, and formal `unknown`.

## Ontology compatibility review

Because P006 fails after all five non-P004 Primitives already completed
independent research, the trigger condition is met. The review distinguishes
two facts:

1. the current modern Primitives are useful product questions; and
2. several are not native knowledge objects in the selected traditional
   corpora, causing systematic semantic starvation.

The review will retain `primitive_ontology_v2.yaml` unchanged for v0.4.x
reproducibility and create a non-runtime candidate
`candidates/core-profile-v3/primitive_ontology_v3.yaml`. The version number is
v3 because v2 already exists in the repository.

The v3 pilot Primitive is `TP001 Task Continuity Process`: how an undertaken
matter is sustained, revised, interrupted, or carried through. It is sourced
from already located behaviour-process language such as `作事進退悔懶、有始無終`
and Ptolemy's change-of-mind wording. It excludes achievement, moral diligence,
action-initiation speed, task-organization method, and outcome. This is a
candidate ontology discovery result only; traditional methods and facts remain
blocked, so it creates no PE, Mapping, or runtime output.

## Runtime and packaging boundary

The formal release Mapping bundle stays empty. The release manifest remains the
v2 six-unknown authority. Candidate Bridge and ontology assets cannot enter the
formal resolver. Renderer code remains unchanged.

The candidate resolver receives one correctness fix: local context evidence no
longer becomes a global state by default. Existing synthetic global evidence
must opt in explicitly. Provenance retains declared bridge refs when present.

## Verification and release

Use TDD for policy loading, admission, PRIMARY_EVIDENCE enforcement, independent
single-direction resolution, absence semantics, local scope, symbolic and
capability rejection, scientific boundary, and candidate-ontology isolation.

The final machine summary uses schema
`semantic-bridge-governance-final-v1`. Five autonomous roles review semantics,
traditional method fidelity, ontology ownership, architecture layering, and
product value.

With zero PE, zero active Mapping, and zero formal non-unknown Primitives, the
release classification is:

`SEMANTIC_BRIDGE_GOVERNANCE_COMPLETE__P006_BRIDGE_REJECTED__ONTOLOGY_V3_CANDIDATE_OPENED__NO_FORMAL_ACTIVATION`

The correct release version is v0.4.2, not v0.5.0.
