# C2-SK P004 Astrology Methodology Product Owner Packet

## D1 — Aspect RULE_GATE

**What:** proposed non-directional aspect admission gate. **Why:** preserves identified aspect facts for later review. **Evidence:** approved aspect Root and aspect-method claims. **Enables:** review admission. **Does not enable:** direction, Mapping, state, runtime. **Risk:** over-reading gate approval.

```text
D1: [ ] approve as RULE_GATE  [ ] defer  [ ] reject
```

## D2 — Planet Placement Root

**What:** proposed placement fact identity. **Why:** method candidate needs auditable body/sign/degree. **Evidence:** deterministic placement facts. **Enables:** fact reference. **Does not enable:** Mars meaning, direction, mechanism, Mapping or runtime. **Risk:** confusing identity with interpretation.

```text
D2: [ ] approve  [ ] defer  [ ] reject  [ ] request revision
```

## D3 — P004 Hellenistic Natal Methodology Candidate

**Readiness:** `D3_READY_FOR_PRODUCT_OWNER_DECISION`. Candidate Validation is `READY_FOR_PO_REVIEW`; Product Owner Selection is still `PENDING`.

**What:** `AMC-AS-P004-HELLENISTIC-NATAL-V1`, a P004-specific natal method candidate. **Why:** prevents school mixing and defines the methodology boundary for later research. **Evidence:** Demetra George is the machine-declared Method Authority; cross-school and project boundaries remain separate. Evidence symmetry, authority purity, materiality semantics, materiality completeness, and approval provenance all pass. **Enables if approved:** future P004 materiality and semantic-mechanism research within this method. **Does not enable:** scientific-truth claims, Mars→P004 high/low, PRIMARY_EVIDENCE, Mapping, Primitive state, production behavior, D1, or D2. **Risk:** treating unresolved materiality as either exclusion or approval.

The hardened audit finds sect, dignity, reception, speed, visibility, aspects, bonification, maltreatment, and related techniques to have known method roles but unresolved P004 materiality. This uncertainty is explicit and does not make them P004-required. Application/perfection is `NOT_P004` only for automatic transfer of horary event logic into natal personality direction. Mars relevance also remains unresolved inside the selected authority.

```text
D3: [ ] approve for continued semantic design  [ ] defer  [ ] reject  [ ] request revision
```

If approved, the approval record must provide a non-empty, traceable `product_owner_decision_ref`. The Loader rejects an approved status without it. This packet does not populate or simulate that decision.
