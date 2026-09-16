# Failure Policy

The first failed applicable gate wins. Classify it once, stop progression, and
do not evaluate later gates after a fatal issue. Apply this fatal precedence:

1. `BIRTH_INPUT_ERROR`: required input is missing, malformed, contradictory, or wrong for the requested mode.
2. `CONFIG_GAP`: an asset required by the selected profile or required by an emitted claim is absent or invalid.
3. `CAPABILITY_GAP`: no candidate exists for a required category, `authorization_not_granted` leaves no alternative, or a mandatory independent candidate is unavailable.
4. `METHODOLOGY_VERSION_MISMATCH`: all discovered candidates for a category lack exact evidence, conflict with the frozen method, or return another verified method version.
5. `CALCULATION_FATAL`: qualified authorized invocations fail and safe candidates are exhausted.
6. `CALCULATION_CONTRACT_ERROR`: a returned or normalized packet violates the contract; `external_result_conflict` is its cross-capability subtype.
7. `INFERENCE_GUARD_ERROR`: a controlled portrait contains an unanchored claim, promotes reported facts, hides a material limitation, violates the report schema, or makes a prohibited diagnosis, certainty, guarantee, or prediction.
8. `coverage_warning`: strict semantic assets are complete and facts are valid, but case-specific Mapping coverage is below the frozen provisional threshold.

`CONFIG_LIMITATION` is a non-fatal warning available only in
`controlled_inference`. Use it when an advanced calculation or semantic asset
is absent, every dependent claim is safely omitted, and the limitation is
disclosed. It does not satisfy `CALCULATION_CONFIG_CHECKED`,
`SEMANTIC_CONFIG_CHECKED`, or any strict certification. If an absent asset is
required by an emitted claim or cannot be safely omitted, it remains `CONFIG_GAP`.

Every fatal code produces `stopped`. A strict `coverage_warning` may produce
`partial`. A controlled report may also be `partial` when its fact basis is
valid but a required section is explicitly `insufficient_basis`. No partial
path authorizes invented content.

After a qualified, authorized invocation failure, retry only with another
already available, preflight-qualified candidate and only when repeating the
operation is safe. Exhaust safe candidates before returning
`CALCULATION_FATAL`. Remote authorization is execution-scoped and does not
carry into another execution. Never install, connect, loosen methodology, or
fabricate facts as a retry.

For every stopped report, identify the failed stage and one concrete recovery
action. An `audit` verifies only supplied evidence and never advances it. Keep
permission flags false unless the applicable strict or controlled profile has
already reached its explicit permission gate.
