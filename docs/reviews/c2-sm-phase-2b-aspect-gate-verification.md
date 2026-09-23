# C2-SM Phase 2B Aspect Gate Verification

## Scope

This record verifies the candidate-only Phase 2B submission
`SMC-AS-ASPECT-ELIGIBILITY-GATE-P004-V1`. It does not approve that mechanism,
create a Mapping v2 candidate, or activate any runtime behavior.

## Candidate review state

```text
Candidate: SMC-AS-ASPECT-ELIGIBILITY-GATE-P004-V1
Review status: proposed
Evidence Root reference: ER-AS-ASPECT-INSTANCE-V1
Role: RULE_GATE
Target review question: P004 — When and how is concrete action started and advanced?
Approved Semantic Mechanisms: 0
Mapping v2 candidates: 0
Runtime activation: none
```

The candidate admits an identified astrology aspect instance only to later P004
evidence review. It does not establish a Primitive state, direction, magnitude,
or score.

## Fresh verification evidence

Commands executed from the project root on 2026-09-23:

```sh
PYTHONPATH=src python3 - <<'PY'
from pathlib import Path
from destiny_personality.core_profile_builder import (
    candidate_presentation_bundle_fingerprint,
    candidate_semantic_bundle_fingerprint,
)
from destiny_personality.semantic_mechanisms import (
    build_evidence_root_audit_report,
    build_semantic_mechanism_audit_report,
    build_semantic_mechanism_candidate_fingerprint,
    load_approved_evidence_root_ids,
    load_evidence_root_registry,
    load_semantic_mechanism_candidates,
)

root = Path("candidates/semantic-mechanisms-v1")
roots = load_evidence_root_registry(root)
approved_root_ids = load_approved_evidence_root_ids(root)
candidates = load_semantic_mechanism_candidates(root)
print("Evidence Root audit:", dict(build_evidence_root_audit_report(roots)))
print(
    "Semantic Mechanism audit:",
    dict(build_semantic_mechanism_audit_report(candidates, approved_root_ids)),
)
print("Approved Root IDs:", ", ".join(sorted(approved_root_ids)))
print("Candidate Mechanism IDs:", ", ".join(item["candidate_id"] for item in candidates))
print("C2-SM candidate fingerprint:", build_semantic_mechanism_candidate_fingerprint(root))
print("Active semantic fingerprint:", candidate_semantic_bundle_fingerprint())
print("Active presentation fingerprint:", candidate_presentation_bundle_fingerprint())
PY
python3 -m pytest -q --disable-warnings
python3 scripts/verify_package.py
```

Audit output:

```text
Evidence Root audit: {root_count: 2, approved_count: 2, non_approved_count: 0}
Semantic Mechanism audit: {candidate_count: 1, error_count: 0, warning_count: 0, admission_eligible_count: 1}
Approved Root IDs: ER-AS-ASPECT-INSTANCE-V1, ER-BZ-TEN-GOD-INSTANCE-V1
Candidate Mechanism IDs: SMC-AS-ASPECT-ELIGIBILITY-GATE-P004-V1
```

Verification result:

```text
Full test suite: 501 passed in 25.87s
Package verification: passed
```

Fingerprint output:

```text
C2-SM candidate fingerprint: 355d2561fb142138d4f007588c2338a8479264acef2558d3006bcf03cb35d829
Active semantic fingerprint: 256ba053b174a054226301f1b493e0e0c8f9f50e9f2976a72b8045dbf6ed6131
Active presentation fingerprint: 2f1d3866638074485351ada0c6a9aaa9bd1acd916f65973ca2b319a75b99b91d
```

The candidate fingerprint is intentionally isolated from active semantic and
presentation fingerprints. Candidate-only change therefore does not alter the
active runtime contract.

## Gate

The next required gate is a separate Product Owner decision for
`SMC-AS-ASPECT-ELIGIBILITY-GATE-P004-V1`. Until explicitly approved, it cannot
be consumed by Mapping Candidate design. Mapping v2 remains unauthorized.
