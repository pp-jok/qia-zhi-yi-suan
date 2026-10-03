# C2-SM P004 Bazi Hidden-Stem Identity Audit

Date: 2026-10-04

## Finding

Before this review, `HiddenStemsFact.stems` ordering was supplied by a provider
or fixture. The project described a common hidden-stem table but did not own a
versioned machine contract for index identity. Consequently,
`month.hidden_stem.0` was structurally valid yet not provider-independent.

## Adopted policy

`bazi-hidden-stem-order-v1` is now a packaged, project-owned identity table for
all twelve branches. It defines branch plus ordered hidden stems only. It does
not encode main/middle/residual qi, weights, season strength, flourishing,
pattern, Dao-Shi, personality, or any semantic conclusion.

The explicit reference provider uses normalization: it verifies exact stem
membership, reorders to the governed tuple, and remaps Ten-God and relation
references to canonical indices. The formal calculation and qualified-facts
boundaries use fail-closed validation and reject noncanonical stored order.
Missing, duplicate, extra, or mismatched pillar records are rejected.

## Cross-provider result

Providers returning the same hidden stems in different raw tuple orders now
produce the same canonical subjects and relation identity. A provider cannot
freely assign an index. Tests cover reversed provider order, membership
mismatch, missing pillar coverage, and formal-boundary order rejection.

```text
Hidden Stem Identity:
READY

Ordering Policy:
bazi-hidden-stem-order-v1

Policy Semantics:
IDENTITY_ONLY
```
