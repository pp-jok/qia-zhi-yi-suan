# Core Profile Calibration Review v1

**Stage:** C4 — Calibration Review  
**Status:** C4b candidate policy frozen for the named D1 Bundle on 2026-09-18; no production approval

## Dataset separation

The project uses three non-interchangeable sets:

| Set | Purpose | Permitted use |
| --- | --- | --- |
| Design Set | exposes semantic gaps while C1–C3 proposals are revised | ontology, mapping, formation, and draft policy work |
| Calibration Set | selects versioned weights, thresholds, and exceptions | finalizes candidate policy after C1–C3 freeze for that iteration |
| Holdout Validation Set | tests generalization after Semantic Bundle and policy freeze | release evaluation only; no rule or threshold tuning |

Golden Sample material may appear only in Design/Calibration regression with
its original report excluded from runtime assets. It cannot appear in Holdout
or prove final generalization.

## Design / Calibration coverage proposal

Eight anonymous contrast cases exercise:

```text
high_autonomy_high_change
high_stability_low_change
high_affiliation_low_autonomy
high_action_low_reflection
high_affect_low_structure
high_rules_responsibility
cross_system_tension
unknown_birth_time
```

They are stress cases, not a user-distribution claim. Each case stores only
approved Canonical Facts, provenance class, and expected structural distinction;
no reader-facing report text.

## Holdout coverage proposal

After the candidate Semantic Bundle and C4 policy freeze, use a separate Holdout
set containing:

```text
middle_autonomy_middle_stability
near_equal_primitive_signals
no_dominant_signature
no_clear_core_dynamic
unknown_or_limited_context
```

These weak-signal cases verify that the system retains `unknown`, `mixed`,
limitations, and zero Dynamics rather than manufacturing themes. Do not inspect
Holdout results to revise C1–C4 assets for the same release candidate.

## Required C4 decisions

Before the approval gate, product review must set or reject:

1. Semantic Bundle fingerprint and frozen candidate version set.
2. Similarity weights, contrast-pair threshold categories, and exceptions.
3. Any eligible-case frequency guard beyond the zero-unsupported invariant.
4. Determinism normalization contract and exact failure code.
5. Holdout access procedure and exception documentation.

The initial review intentionally does **not** choose numeric similarity or
frequency thresholds without Core Profile runs. Missing values keep policy
pending and block stage D promotion.

## D1 Design Set run — 2026-09-18

The eight isolated Design Set fixtures were executed by the candidate-only
Builder. The run is a calibration input, not evidence for production release.

| Check | Result |
| --- | --- |
| Anonymous fixture coverage | 8 / 8 planned cases loaded |
| Normalized candidate Profile distinction | 8 / 8 unique; therefore all 28 pairs remain structurally distinguishable |
| Cross-system tension case | `P002 = mixed`; neither source was overwritten |
| Unknown-birth-time case | no astrology candidate was activated |
| Dynamic / Archetype output | zero for every case, as the D1 policies are disabled |
| Numeric similarity / collapse scores | emitted under the C4b candidate policy; Design Set maximum is `0.75` and does not exceed the threshold |

## C4b candidate decision — 2026-09-18

Following owner approval to proceed, the candidate-only policy freezes:

- semantic Bundle fingerprint:
  `a77958e1f4453828b44fd1c2573f58f4e51e63b1c25c581d0293da0166276bd9`;
- equal Primitive salience and evidence-stability weights of `1.0`;
- a `1.0` weight for `weighted_primitive_overlap` and `0.0` for unavailable
  Signature, Dynamic, and Fate components;
- a Design Set contrast-pair maximum similarity of `0.75` with no D1
  exceptions;
- `unsupported_activation_frequency: 0`.

The named policy is candidate-only. Any semantic asset change changes the
fingerprint and invalidates the policy until calibration is repeated.

## Holdout validation — 2026-09-20

The frozen approved Bundle was evaluated against five anonymous Holdout cases:
`middle_autonomy_middle_stability`, `near_equal_primitive_signals`,
`no_dominant_signature`, `no_clear_core_dynamic`, and
`unknown_or_limited_context`.

| Check | Result |
| --- | --- |
| Holdout fixture coverage | 5 / 5 named cases loaded |
| Dynamic / Archetype output | zero for every case, as the approved policies remain disabled |
| Limited-context handling | unknown-time case activates no astrology candidate and retains only `unknown` states |
| Candidate auditability | every activated candidate contains both fact and semantic-rule references |

The Holdout run did not change any candidate semantic asset, mapping condition,
or calibration threshold. It is validation evidence for the approved candidate
Bundle only and does not open strict production or a default route.
