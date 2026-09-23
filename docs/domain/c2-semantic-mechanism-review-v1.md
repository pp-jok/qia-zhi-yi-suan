# C2 Semantic Mechanism Review v1

## Candidate review procedure

1. Register and review an Evidence Root under the separate root process.
2. Draft a candidate-only mechanism with root references and target Primitive
   questions.
3. Run contract validation and record every error or warning in the audit
   report.
4. Resolve or reject blocking errors; evaluate legacy-equivalence warnings.
5. Obtain an explicit Product Owner decision for the mechanism.
6. Only then may a future, separately authorized Mapping Candidate design cite
   the approved mechanism.

## Automated blocking conditions

| Finding | Effect |
|---|---|
| `SEMANTIC_MECHANISM_EVIDENCE_ROOT_REQUIRED` | Reject candidate. |
| `SEMANTIC_MECHANISM_UNAPPROVED_ROOT` | Reject candidate. |
| `SEMANTIC_MECHANISM_PRIMITIVE_QUESTION_REQUIRED` | Reject candidate. |
| `SEMANTIC_MECHANISM_DIRECT_STATE_ASSERTION` | Reject candidate. |
| `GOLDEN_SAMPLE_SEMANTIC_LEAK` | Reject candidate. |
| `SEMANTIC_MECHANISM_CONTRACT_FIELD_REQUIRED` | Reject candidate. |
| `SEMANTIC_MECHANISM_INVALID_ROLE` | Reject candidate. |
| `SEMANTIC_MECHANISM_INVALID_REVIEW_STATUS` | Reject candidate. |
| `SEMANTIC_MECHANISM_PROHIBITED_ORIGIN` | Reject candidate. |
| `MAPPING_CANDIDATE_UNAPPROVED_MECHANISM` | Reject Mapping Candidate use. |

`LEGACY_REINTRODUCTION_WARNING` requires explicit review; it cannot be ignored
by a loader or converted into runtime behavior.

## Current review result

```text
Evidence Root candidates: 2
Semantic Mechanism candidates: 1
Approved Semantic Mechanisms: 0
Mapping Candidate references: 0
```

The proposed candidate is `SMC-AS-ASPECT-ELIGIBILITY-GATE-P004-V1`. It cites
`ER-AS-ASPECT-INSTANCE-V1` and asks only whether an identified aspect instance
may enter later P004 evidence review as a non-primary `RULE_GATE`. It does not
assert a P004 state or direction, and it does not create a mapping.

No Product Owner mechanism decision has been made. The next gate is a separate
decision on this mechanism: approve, reject, or request revision. Root approval
and C2-SM authorization do not imply mechanism approval. Even an approved
mechanism would only become eligible for separately authorized Mapping Candidate
design; Mapping v2 is not authorized by this review.
