# 10 Codex Implementation Plan V2.2

## 1. Current Baseline

V2.2 freezes domain methodology, not a bundled software runtime.

The target deliverable is an agent-orchestrated Skill. The Skill defines
business logic, execution order, normalized contracts, validation gates, and
failure behavior. The agent invokes external deterministic calculation
capabilities. See `12_SKILL_EXECUTION_ARCHITECTURE_V2_2.md`.

The existing Python package is retained as a development reference validator.
It is not shipped as a required Skill runtime and will not be extended into a
bundled chart-calculation product.

---

## 2. Completed Reference-Validator Work

### Reference Phase 0 — Complete

Implemented strict loading and validation for the four existing baseline YAML
files.

Completion does not mean the complete production rule set exists. Primitive
Ontology, Mapping Registry, deterministic lookup tables, dimension rules, and
narrative rules remain separate required assets.

### Reference Phase 1 — Complete

Implemented normalized input and deterministic fact contracts, replaceable
calculation protocols, ordered validation, fatal short-circuiting, methodology
version checks, and `stable_only` boundaries.

These Python protocols are machine-testable expressions of the fact contract,
not the required runtime invocation mechanism of the Skill.

### Reference Phase 1.1 — Complete

Hardened Bazi provenance by pillar, split validation from orchestration, added
guard-characterization tests, and added isolated package verification for the
reference validator.

---

## 3. Revised Delivery Phases

### Phase A — Delivery Architecture Alignment

Status: **complete and verified on 2026-09-12**.

The architecture addendum, README, runtime rules, acceptance criteria,
manifest, package metadata, tests, and historical-plan notices agree that:

- Skill defines and validates the workflow;
- agent performs external calls;
- calculation software is not bundled;
- Python code is development-only reference validation.

### Phase B — Minimal Skill Shell

Status: **complete**.

Create the actual Skill entrypoint and minimal runtime artifact:

```text
SKILL.md
references/
configs/
schemas/
checklists/
```

The shell must define:

- scope and data-access boundary;
- input preflight;
- execution states and gates;
- allowed failure and partial-output paths;
- explicit prohibition on free calculation and semantic invention;
- selective loading of references to keep runtime context bounded.

No third-party calculator or project Python package enters this artifact.

### Phase C — External Deterministic Capability Protocol

Status: **complete and verified on 2026-09-12**.

This status covers the verified Phase C protocol and release metadata only. It
does not mean Gate 1 has passed or any semantic phase is complete.

This replaces the previous idea of integrating a fixed calculation backend.

Implement Skill instructions and normalized schemas for:

1. capability discovery;
2. methodology compatibility checks;
3. agent-performed tool invocation;
4. calculation provenance;
5. result normalization;
6. fact-contract validation;
7. retry with another already available qualified capability;
8. ordered `CAPABILITY_GAP`, mismatch, fatal, and contract-failure behavior;
9. execution-scoped authorization before sending data to each remote capability;
10. an execution report that records candidate state and accepted-operation
    references without duplicating raw sensitive payloads or credentials.

Failure classification follows the first failed gate and never evaluates later
gates: `CONFIG_GAP` for missing or invalid project-owned rules, schemas,
aliases, node rules, boundary margins, or tolerances; `CAPABILITY_GAP` when no
candidate exists, authorization denial leaves no alternative, or a mandatory
independent candidate is unavailable; `METHODOLOGY_VERSION_MISMATCH` when all
discovered candidates lack exact evidence, conflict with the frozen method, or
return a different verified method version; `CALCULATION_FATAL` only after
qualified authorized invocations and safe candidates are exhausted; and
`CALCULATION_CONTRACT_ERROR` for a returned or normalized packet violation,
with `external_result_conflict` as the cross-capability subtype.

The contracts do not supply project-owned calculation values. Exact
deterministic lookup tables, the True North Node rule, aliases,
boundary-distance margins, and comparison tolerances remain `CONFIG_GAP`.

### Gate 1 — Domain Rule Completeness

Semantic implementation must not proceed until the required product assets are
present and internally consistent:

- Primitive Ontology;
- Bazi Context-Aware Mapping Registry;
- astrology Context-Aware Mapping Registry;
- complete deterministic lookup tables required by both methodologies;
- Primitive State resolution rules;
- 12-dimension definitions and coverage rules;
- versioned provisional Mapping coverage thresholds and partial-portrait policy;
- narrative rules.

Missing assets produce `CONFIG_GAP`. Codex must not create their semantic values
without explicit product authorization.

Gate 1A Primitive foundation contracts are implemented and verified on
2026-09-13. Gate 1 remains incomplete and Phase D remains incomplete until
real, project-approved Primitive and all other required semantic assets are
supplied.

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
The production calculation values remain absent. For the strict profile, CALCULATION_CONFIG_CHECKED remains closed. Gate 1 remains incomplete, Phase D remains incomplete, and Phase E remains incomplete. The delivered framework validates project-owned candidates but does not supply or promote their values.

Controlled Inference business-test workflow is implemented and verified on 2026-09-14.
With a qualified external calculation capability, `portrait` may now generate an anchored, disclosed report under the controlled profile. This does not permit language-model chart calculation. Strict production remains blocked by project-owned assets.
The controlled report uses the long-form personality-book format: front matter, prologue, four parts, fifty-six chapter dimensions, finale, and audit appendix.
Each supported chapter must make at least three distinct analytical moves across evidence, mechanism, lived expression, and integration; repetition does not satisfy report depth.
User-approved reference interpretations may enrich controlled reports only as source-qualified supplemental interpretations; they do not override calculated facts, promote assurance, or satisfy strict gates.

### Phase D — Structured Personality Reasoning

After Gate 1 passes, implement the former semantic Phases 2–8 as declarative
business rules and stage contracts:

1. Primitive Ontology and State Model;
2. Context-Aware Mapping Registry and Interaction Rules;
3. Evidence Graph;
4. Trait Salience / Evidence Stability / Cross-System Relation / Synthesis
   Priority separation;
5. Primitive Relation Graph activation;
6. Signature extraction;
7. Dynamic candidate generation, selection, and deduplication.

Every stage must preserve source references and expose a validation result.

### Phase E — Portrait Construction

Implement the former Phases 9–11:

1. 12-dimension coverage;
2. Shadow / Mature / Fate / Archetype;
3. guarded Narrative rendering.

Narrative remains downstream of the complete IR and cannot add or modify core
claims.

### Phase F — Evaluation and Release

Evaluation is cross-cutting rather than postponed until the end:

- add structural and boundary checks with each phase;
- preserve Golden and calibration expected results outside production runtime;
- treat Golden and boundary cases as build/release evidence, never runtime
  configuration;
- run deterministic fact equality, ontology-aware similarity, Dynamic
  structure, dimension coverage, and template-collapse checks at release;
- keep all initial thresholds marked `provisional` until calibrated.

A provisional threshold may be used only when it is explicitly versioned and
frozen for the release. `Provisional` means calibration is incomplete, not that
the runtime may choose or change the value freely.

---

## 4. Codex Must Not Change Independently

- methodology values
- orb values
- day boundary convention
- month boundary convention
- primitive definitions
- mapping rules
- relation graph semantics
- score model semantics
- 12-dimension semantics
- narrative rule semantics

If a required product rule is missing:

```text
raise CONFIG_GAP
```

Use the ordered Phase C failure classification above; do not collapse missing
exact evidence into `CAPABILITY_GAP`. No failure condition may be bypassed by
inference, general knowledge, silent installation, or a looser external method.

---

## 5. First-Release Test Minimum

The release suite must contain:

- the current G001 Golden Sample when supplied as an isolated release asset;
- 3 meaningfully different cases;
- 1 unknown-birth-time case;
- 1 boundary-time case;
- 1 no-capability case;
- 1 methodology-mismatch case;
- 1 malformed external-result case;
- a packaging check proving the Skill has no bundled calculation software or
  Python runtime dependency.

---

## 6. First-Release Priority

```text
execution boundary correctness
> repeatable deterministic facts
> rule traceability
> personality differentiation
> cross-model consistency
> narrative quality
```

---

## 7. Immediate Next Step

Phase C release verification for the Skill artifact and its packaging metadata
completed on 2026-09-12. Gate 1 and Primitive semantic implementation remain
blocked by the listed project-owned configuration gaps; resolve those gaps
before advancing either stage.
