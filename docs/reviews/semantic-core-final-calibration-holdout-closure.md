# Semantic Core Final Calibration and Holdout Execution Closure

## Baseline and scope

Baseline: `3d255b5b900c93ff65e68d4216405c1196be1728`.

This closure adds execution and trust verification to the existing candidate-only Calibration/Holdout path. It does not approve an Evidence Root, Semantic Mechanism, Mapping, Primitive, formation policy, or production bundle.

## Fixture contract and execution

`candidate-core-profile-calibration-facts-v1` fixtures are loaded rather than merely named. The loader validates the schema and required input fields, normalizes Ten-God, aspect, birth-time, and assurance input into stable facts, and records an individual content fingerprint. Optional expected state/context assertions are supported for synthetic evaluation fixtures without changing the meaning of the existing repository fixtures.

Calibration uses the eight Design Set fixtures and Holdout uses the five Holdout Set fixtures. The loader rejects empty datasets, invalid fixtures, duplicate IDs, overlapping paths, overlapping IDs, and identical fixture content across the two sets.

For a non-empty approved Mapping bundle, every fixture is matched against the Mapping's canonical fact requirements and passed to the existing Primitive Resolver. It executes each case twice to test determinism, preserves valid `unknown`, `mixed`, and `context_differentiated` outcomes, evaluates optional expected states, and reports observed output collapse independently of the existing structural template-collapse guard. Holdout uses the same read-only execution mechanism; it cannot alter Mapping, policy, proposals, or runtime.

## Artifact and registry trust model

Each artifact contains `mapping_bundle_fingerprint`, `dataset_fingerprint`, `evaluation_input_fingerprint`, and `artifact_fingerprint`. Input fingerprints exclude the timestamp and bind the evaluation kind, candidate bundle binding, Mapping content, dataset content, runner, policy, and fixed evaluation config. Artifact fingerprints cover the normalized artifact payload excluding the timestamp and the fingerprint itself.

`register_evaluation_artifact` and `load_promotion_authority` independently validate this contract. A passing status alone is insufficient: missing, tampered, or unrecognized artifact fields fail closed. The official CLI runner is the `run-mapping-calibration` or `run-mapping-holdout` command; `--register` only writes a fully validated passing artifact to the authority registry.

## Zero-state behavior

The repository fixtures are loaded and fingerprinted in the current zero state, but the runners correctly return `blocked_by_gate` with zero executed cases because Approved Mappings remain zero. `--register` rejects that blocked artifact. Synthetic tests cover the independent PASS lifecycle.

## Final readiness

```text
Semantic Core Foundation Engineering: COMPLETE / FROZEN
Semantic Verification Infrastructure: COMPLETE
Calibration Pipeline: COMPLETE
Holdout Pipeline: COMPLETE

Approved Evidence Roots: 2
Proposed Semantic Mechanisms: 1
Approved Semantic Mechanisms: 0
Mapping Proposals: 0
Approved Mappings: 0

Primitive Runtime: disabled
Signature Runtime: disabled
Dynamic Runtime: disabled
Fate Theme Runtime: disabled
Archetype Runtime: disabled
Production Activation: NOT AUTHORIZED
```

Future work starts with real semantic asset authoring and the Product Owner review flow; it must not expand Semantic Core Foundation engineering merely for additional abstraction.

## Final verification

The current suite was collected as 572 tests and completed in bounded groups:
167 + 113 + 181 + 111 = `572 passed`. Isolated package verification completed
against a freshly built wheel. No active semantic or presentation fingerprint
was modified by this closure. GitHub Actions for published commit `aac3e4a`
also completed successfully on Python 3.9, 3.11, and 3.12, with the separate
package-verification job successful.
