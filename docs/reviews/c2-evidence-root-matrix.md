# C2-R Evidence Root Matrix

## Approved identity contract

```text
Canonical Fact → Evidence Root → Evidence Instance(s)
```

`evidence_root_id` is determined only by canonical fact identity. Neither a mapping rule, a context label, an aspect expression label, nor renderer wording may create an independent root.

## Current-state matrix

| Rule | Canonical Fact Root | Evidence Root ID Strategy | Other Rules Sharing Root | Independent? | Aggregation Eligible? |
|---|---|---|---|---|---|
| BZ-C2B-01 | deterministic `bazi.ten_gods` match plus environment derivative | UNKNOWN_ROOT; no canonical fact identity field | BZ-C2B-03, BZ-C2B-05 partially share 食伤 family | no proof | no |
| BZ-C2B-02 | deterministic 印/官 Ten-God match plus environment derivative | UNKNOWN_ROOT | BZ-C2B-06, BZ-C2B-07 same complete fact pattern | no proof | no |
| BZ-C2B-03 | deterministic 食伤/财 match plus environment derivative | UNKNOWN_ROOT | BZ-C2B-05 exact; BZ-C2B-01 partial | no proof | no |
| BZ-C2B-04 | deterministic broad Ten-God match plus environment derivative | UNKNOWN_ROOT | none established | no proof | no |
| BZ-C2B-05 | deterministic 食伤/财 match plus environment derivative | UNKNOWN_ROOT | BZ-C2B-03 exact; BZ-C2B-01 partial | no proof | no |
| BZ-C2B-06 | deterministic 印/官 Ten-God match plus environment derivative | UNKNOWN_ROOT | BZ-C2B-02, BZ-C2B-07 same complete fact pattern | no proof | no |
| BZ-C2B-07 | deterministic 印/官 Ten-God match plus environment derivative | UNKNOWN_ROOT | BZ-C2B-02, BZ-C2B-06 same complete fact pattern | no proof | no |
| AS-C2B-01 | deterministic Sun–Mars aspect/placement facts | UNKNOWN_ROOT | AS-C2B-05 exact aspect family | no proof | no |
| AS-C2B-02 | deterministic Saturn–Sun aspect/placement facts | UNKNOWN_ROOT | none established | no proof | no |
| AS-C2B-03 | deterministic Uranus–Sun aspect/placement facts | UNKNOWN_ROOT | none established | no proof | no |
| AS-C2B-04 | deterministic Moon–Venus aspect/placement facts | UNKNOWN_ROOT | none established | no proof | no |
| AS-C2B-05 | deterministic Mars–Sun aspect/placement facts | UNKNOWN_ROOT | AS-C2B-01 exact aspect family | no proof | no |
| AS-C2B-06 | deterministic Moon–Mercury aspect/placement facts | UNKNOWN_ROOT | none established | no proof | no |
| AS-C2B-07 | deterministic Mercury–Saturn aspect/placement facts | UNKNOWN_ROOT | none established | no proof | no |

## Fail-closed consequence

Every current evidence item remains audit-visible. Until a future approved implementation supplies the D1 identity fields, every item is aggregation-ineligible, promotion-ineligible, and validation-ineligible. This is a design conclusion only; current runtime remains unchanged until separately authorized implementation.
