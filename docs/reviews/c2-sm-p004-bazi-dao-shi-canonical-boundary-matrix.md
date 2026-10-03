# C2-SM P004 Bazi Dao-Shi Canonical Boundary Matrix

Date: 2026-10-03
Baseline: `c3fb59333b5ac7701d9145f94123550ab880768a`

This audit separates chart identity, neutral derivation, methodology judgement, and semantic interpretation. “Canonical eligible” means eligible in principle; it does not mean the project currently computes or governs the item.

| Item | Current location | Correct layer | Deterministic? | School-dependent? | Canonical eligible? | Root eligible? |
|---|---|---|---|---|---|---|
| Eating God identity | `BaziChartFacts.ten_gods[].ten_god` | A — raw/deterministic chart fact | Yes, when supplied by an accepted calculation envelope | No within frozen `bazi-core-v1.0` | Yes; implemented | Yes; already covered by `ER-BZ-TEN-GOD-INSTANCE-V1` |
| Indirect Resource identity | Same Ten-God collection | A | Yes on the same basis | No within the frozen methodology | Yes; implemented | Yes; same existing Root |
| Position | `TenGodFact.source_pillars` and `subject_ref` | A | Yes | No | Yes; implemented | Yes as identity provenance, not as importance |
| Visibility | `TenGodFact.source_kind` | A | Yes | No | Yes; implemented | Yes as identity provenance |
| Hidden/visible provenance | `source_kind`, `source_pillars`, hidden-stem facts | A | Yes | No | Yes; implemented | Yes within the existing identity Root |
| Month branch | `BaziChartFacts.month_pillar.earthly_branch` | A | Yes | No | Yes; implemented | Potentially, but no new Root is needed now |
| Season label | Candidate `DayMasterEnvironmentFact.season` derived from an approved lookup table | B — derived, school-neutral descriptor | Yes for the frozen month-branch table | No for the four-season label; it says nothing about strength | Yes; implemented only in candidate semantic support, not in the deterministic packet | Not for the withdrawn interaction Root |
| Element relation | No project-owned emitted relation family; only a generic `BaziRelationFact` shape and non-production table template exist | B | Deterministic in principle | No for raw five-phase control identity | Yes after vocabulary, rules, provider output, and validation are implemented | Not yet |
| Control relation between chart subjects | Generic `BaziRelationFact` can represent it, but no governed participant-reference rule or production table exists | B | Deterministic in principle | No if limited to raw element control | Yes after implementation | Not yet |
| Stem combination present | Generic relation shape/config mentions combinations; no project-owned deterministic table is present | B | Deterministic in principle | Presence: no; effect/transformation: yes | Presence only, after implementation | Not yet |
| Branch relation present | Same generic relation boundary | B | Deterministic in principle | Presence: no; interpretive effect: yes | Presence only, after implementation | Not yet |
| Strength | No canonical fact | C — methodology judgement | No under current assets | Yes | No under current boundary | No |
| Operative Eating God status | Only appeared in the withdrawn proposed Root | C | No | Yes | No | No |
| Wealth rescue | Only appeared as `wealth_rescue_status` in the withdrawn proposed Root | C | No | Yes | No | No |
| Exception state | Only appeared as `combination_exception_status` in the withdrawn proposed Root | C | No | Yes | No | No |
| `倒食`成立 | Previously implied by `qualification_status` | C | No | Yes | No | No; this is a method result |
| `conditional_limits_supported_high` | Accepted source-bounded Claim | D — semantic interpretation | No | Source/school bounded | No | Never; it belongs to a future Semantic Mechanism |

## Boundary decision

The neutral fact layer may identify Ten-God instances, locations, visibility, season context, and mechanically present relations. It must not say whether an instance is operative, whether a rescue is effective, whether an exception cancels the pattern, or whether 倒食 is established.

The existing `ER-BZ-TEN-GOD-INSTANCE-V1` remains valid and unchanged. The proposed interaction Root crossed the C-to-A boundary and is withdrawn.
