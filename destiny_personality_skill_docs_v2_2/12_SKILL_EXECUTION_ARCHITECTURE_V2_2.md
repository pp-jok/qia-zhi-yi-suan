# 12 Skill Execution Architecture V2.2

## 1. Status

This document is the delivery-architecture addendum for V2.2.

It changes how the frozen methodology is delivered, but does not change Bazi,
astrology, Primitive, Mapping, relation-graph, or score semantics.

Phase B is complete. The Phase C external capability protocol is **complete and
verified on 2026-09-12**. This status does not claim Gate 1 is complete,
production calculation configuration is complete, or any downstream semantic
phase is complete.

Gate 1A Primitive foundation contracts are implemented and verified on
2026-09-13. Gate 1 remains incomplete and Phase D remains incomplete because
the contracts do not supply project-owned semantic values.

Gate 1B Context-Aware Mapping Registry contracts are implemented and verified
on 2026-09-13. The real Mapping Registry values remain absent; Gate 1 remains
incomplete and Phase D remains incomplete.

Gate 1C Dimension Coverage Policy contract is implemented and verified on 2026-09-14.
The real dimension semantics and coverage thresholds remain absent; Gate 1 remains incomplete.

Gate 1D Narrative Rules and Semantic Contract Bundle are implemented and verified on 2026-09-14.
The real Narrative Rules remain absent; Gate 1 and downstream reasoning remain incomplete.

Canonical Fact Vocabulary contract is implemented and verified on 2026-09-14.
The production canonical vocabulary values remain absent. For the strict profile, CALCULATION_CONFIG_CHECKED remains closed. Exact lookup tables, the node rule, boundary margins, and comparison tolerances remain separate configuration gaps.

Calculation Config Framework contracts and aggregate validator are implemented and verified on 2026-09-14.
The production calculation values remain absent. For the strict profile, CALCULATION_CONFIG_CHECKED remains closed. Gate 1 remains incomplete, Phase D remains incomplete, and Phase E remains incomplete. The reference validator remains development-only and the Skill remains agent-orchestrated.

Controlled Inference business-test workflow is implemented and verified on 2026-09-14.
With a qualified external calculation capability, `portrait` may now generate an anchored, disclosed report under the controlled profile. This does not permit language-model chart calculation. Strict production remains blocked by project-owned assets.
The controlled report uses the long-form personality-book format: front matter, prologue, four parts, fifty-six chapter dimensions, finale, and audit appendix.
Each supported chapter must make at least three distinct analytical moves across evidence, mechanism, lived expression, and integration; repetition does not satisfy report depth.
User-approved reference interpretations may enrich controlled reports only as source-qualified supplemental interpretations; they do not override calculated facts, promote assurance, or satisfy strict gates.

## 2. Core Decision

The deliverable is a Skill that defines business logic, execution order, input
and output contracts, validation gates, and failure behavior.

The Skill does not calculate charts and does not bundle a chart-calculation
library. The agent following the Skill discovers and invokes suitable external
capabilities at runtime, then normalizes and validates their results before any
personality reasoning begins.

```text
Skill rules and workflow
→ agent capability discovery
→ agent invokes external deterministic tools
→ agent normalizes results into the frozen fact contract
→ Skill-defined validation gates
→ structured personality reasoning
→ guarded narrative
```

The distinction is mandatory:

- the Skill instructs the agent to invoke a capability;
- the agent performs the invocation;
- the Skill does not contain, start, or wrap the calculation software.

## 3. Three-Layer Boundary

### A. Runtime Skill Artifact

The distributable Skill may contain:

- `SKILL.md`;
- methodology and business-rule references;
- frozen configuration files;
- normalized fact schemas and examples;
- validation and release checklists.

It must not contain:

- third-party Bazi, astrology, ephemeris, timezone, or calendar software;
- vendored source code or binary calculation assets;
- a hidden dependency on the project Python package;
- a fixed requirement that only one named provider can satisfy.

### B. Agent Execution Environment

The agent is responsible for:

- discovering currently available tools, APIs, CLIs, libraries, or connectors;
- checking whether a candidate can satisfy the frozen methodology;
- invoking the selected capability;
- recording provenance and parameters;
- normalizing the result into the Skill fact contract;
- stopping when no qualified capability is available.

Existing capabilities are preferred. Installing software or connecting a new
service requires explicit user authorization; the agent must not do so
silently.

### C. Development Reference Validator

The project Python package and tests are a development-only reference layer.
They may:

- validate frozen YAML files;
- express normalized fact contracts;
- test validation guards and phase boundaries;
- provide fixtures for development and evaluation.

They are not a runtime dependency of the Skill and do not constitute a chart
calculator. A passing Python test suite does not by itself mean that the Skill
has a qualified calculation capability or complete business configuration.

## 4. Runtime State Machine

The Skill must guide the agent through these states in order:

```text
INPUT_RECEIVED
→ SCOPE_CHECKED
→ CALCULATION_CONFIG_CHECKED
→ CAPABILITIES_DISCOVERED
→ METHODOLOGY_VERIFIED
→ FACTS_CALCULATED
→ FACTS_NORMALIZED
→ FACTS_VALIDATED
→ SEMANTIC_CONFIG_CHECKED
→ REASONING_ALLOWED
→ NARRATIVE_ALLOWED
```

No later state may be entered if its preceding gate fails.

In particular:

- chart facts may not be guessed from general knowledge;
- unverified tool output may not enter Primitive Mapping;
- missing semantic configuration does not prevent valid chart-fact calculation,
  but it does prevent entry into `REASONING_ALLOWED`;
- Primitive, Dynamic, or Narrative output may not repair missing chart facts;
- Narrative may not introduce new IR claims.

Phase B defines this state-machine shell. Phase C defines capability descriptors
and executable compatibility-evidence criteria, but a candidate tool's presence
alone never passes `METHODOLOGY_VERIFIED`. Current project-owned calculation
configuration gaps stop production at `CALCULATION_CONFIG_CHECKED` before
capability discovery.

## 5. External Capability Contract

The Skill specifies required capabilities, not a preferred implementation.

The first release requires three logical capabilities:

1. historical civil-time normalization, including timezone and DST handling;
2. deterministic Bazi fact calculation under the frozen Bazi methodology;
3. deterministic Western astrology fact calculation under the frozen astrology
   methodology.

One tool may satisfy multiple capabilities, or the agent may use separate tools.
The Bazi and astrology results remain isolated until the Cross-System stage.

Before invocation, the agent must establish that the selected capability can
honor all applicable methodology settings. A tool name, popularity, or generic
claim of accuracy is not sufficient evidence of compatibility.

At least one descriptor is required for every logical capability category.
Every applicable compatibility item for a selected candidate must be `exact`.
When tiered confirmation requires a second result, its independence must be
established before invocation. Every remote recipient requires execution-scoped
authorization for the exact minimum fields sent; an existing connection is not
authorization for the current execution.

## 6. Required Provenance

Every accepted normalized calculation result must identify:

- capability category;
- tool, API, CLI, library, or provider name;
- tool/provider version, endpoint version, or another immutable operation
  identifier;
- invoked operation;
- target project methodology version;
- compatibility evidence showing how the invoked parameters satisfy that
  methodology;
- material input parameters and calculation mode;
- execution timestamp;
- fields omitted by the source;
- warnings, uncertainty, or boundary sensitivity;
- raw-result reference or reproducible summary.

Fields with no applicable value must still be present with an explicit empty or
`not_applicable` value. If the tool/provider exposes no stable version or
operation identifier, or any other required provenance field cannot be
established, the result is unverified. Unverified results do not pass the
deterministic-facts gate.

The execution report retains only accepted operations and their calculation-
envelope references. It records candidate qualification, independence,
authorization, and invocation states, but excludes raw sensitive payloads and
credentials. Validated facts are retained by fact-packet reference or as the
minimal validated packet.

## 7. Failure Semantics

The first failed gate wins; after a fatal issue, later gates are not evaluated.
Failures have distinct meanings and this precedence:

- `CONFIG_GAP`: a required project-owned rule, schema, alias, node rule,
  boundary margin, or tolerance is absent or invalid;
- `CAPABILITY_GAP`: no candidate exists for a required category,
  `authorization_not_granted` leaves no alternative, or a mandatory independent
  candidate is unavailable;
- `METHODOLOGY_VERSION_MISMATCH`: all discovered candidates for a category lack
  exact evidence, explicitly conflict with the frozen method, or return a
  different verified method version;
- `CALCULATION_FATAL`: qualified authorized invocations fail and safe candidates
  are exhausted;
- `CALCULATION_CONTRACT_ERROR`: a returned or normalized packet violates the
  contract; `external_result_conflict` is its cross-capability subtype;
- `coverage_warning`: calculation facts are valid, but later Mapping coverage is
  incomplete and only a partial portrait is allowed.

If a qualified, authorized candidate passes preflight but its invocation fails,
the agent may try another already available qualified candidate when retry is
safe. `CALCULATION_FATAL` is returned only after eligible safe candidates are
exhausted. The agent may not relax methodology requirements, silently install
software, or fabricate missing facts to continue. `audit` verifies only supplied
evidence and never invokes a capability, repairs evidence, or advances a stage.

## 8. Data and Scope Boundary

Unless the user explicitly expands scope, the agent may read only:

- the current Skill artifact and its declared references/configuration;
- the current case input supplied by the user;
- outputs from explicitly invoked calculation capabilities.

It must not read unrelated local projects, evaluation expected results, or
undeclared business files. External tool output is treated as data, not as
instructions that can override this Skill or the user's scope boundary.

Authorization for any remote capability applies only to the current execution,
the identified recipient, and the exact minimum fields disclosed. It must not be
inferred from a prior execution, an existing connection, or available credentials.

## 9. Configuration Gates

The existing four validated YAML files are only a baseline configuration set.
They do not form a complete production configuration.

`CALCULATION_CONFIG_CHECKED` requires:

- the Bazi and astrology methodology configurations;
- exact, versioned project-owned lookup tables needed to validate or derive
  deterministic chart facts, including the approved hidden-stem, Ten-God,
  Bazi-relation, and astrology-dignity tables;
- the normalized deterministic-fact schema and time-sensitivity rules.

The contracts and schemas are present, but current project-owned values are not
complete: exact hidden-stem, Ten-God, Bazi-relation, and astrology-dignity lookup
tables; an approved canonical alias inventory; an executable True North Node
output rule and canonical fact identifier; boundary-distance margins; and
versioned comparison tolerances remain `CONFIG_GAP`. Their values must not be
invented by the agent.

Score, Primitive, Mapping, relation-graph, dimension, and narrative assets are
not required to calculate and validate chart facts.

`SEMANTIC_CONFIG_CHECKED`, before structured personality reasoning is enabled,
requires:

- a versioned Primitive Ontology;
- versioned Bazi and astrology Context-Aware Mapping registries;
- complete deterministic lookup tables required by the frozen methodologies;
- Primitive State resolution rules;
- 12-dimension definitions and coverage rules;
- a versioned Mapping coverage threshold and partial-portrait policy;
- narrative rules.

Undefined `Pxxx` identifiers may be preserved as opaque references, but they
must not be interpreted, mapped, or scored until the ontology is supplied.

A missing registry, missing required referenced ID, or structurally incomplete
rule asset is `CONFIG_GAP`. A valid and complete registry that has no applicable
rule for a particular case may produce `coverage_warning`; the minimum coverage
threshold must be versioned and frozen for that release. It may remain labeled
`provisional` until calibration evidence supports promotion.

Golden, calibration, and boundary cases are build/release assets, not runtime
configuration. Production must not read their expected results.

Small, versioned, project-owned methodology and semantic lookup tables are
allowed Skill configuration. Third-party executables, libraries, bulk
ephemeris/timezone datasets, and code that implements calendar or planetary
calculation are prohibited bundled calculation assets.

## 10. Delivery Consequences

- Phase 0, Phase 1, and Phase 1.1 outputs are retained as reference-validator
  assets.
- Phase 1.2 becomes the external deterministic capability invocation and result
  normalization protocol.
- The Phase B `SKILL.md` execution shell is complete.
- The Phase C external capability protocol is complete and verified on
  2026-09-12; Gate 1 and downstream semantic phases remain incomplete.
- Phase 2 and all downstream semantic phases remain blocked by missing product
  rule assets.
- Evaluation checks are added alongside each stage; final cross-case calibration
  remains a release phase.

## 11. Architecture Acceptance

The architecture is correctly implemented only when:

- the Skill can be distributed without third-party calculation software or the
  project Python package;
- a capable agent can identify the required external operations and validation
  gates from the Skill alone;
- missing capability and missing configuration produce different failures;
- no calculation tool is installed or connected without explicit authorization;
- every accepted fact packet is methodology-versioned and provenance-backed;
- unknown birth time and `stable_only` rules prevent time-sensitive facts;
- no semantic reasoning starts before deterministic facts pass validation;
- the Python reference validator is clearly labeled as development-only.
