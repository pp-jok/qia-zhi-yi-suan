# Portrait Report Checklist

Run after controlled claims are complete and before returning the report.

- [ ] Confirm `schema_version` is `portrait-report-v2`, `format_profile` is `long-form-personality-book-v2`, `input_profile` is `compact-or-structured-birth-input-v1`, `content_standard` is `reader-first-depth-v2`, and profile is `controlled_inference`.
- [ ] Confirm fact assurance, methodology versions, provenance, omitted facts, and configuration limitations are explicit.
- [ ] Confirm the front matter contains birth summary, Bazi main chart, Western axes, and important structures without unsupported facts.
- [ ] Confirm the prologue introduces the central question without adding an unanchored conclusion.
- [ ] Confirm the four-part long-form structure is present and ordered.
- [ ] Confirm all fifty-six chapter dimensions appear once and in blueprint order.
- [ ] Run a chapter-level depth audit: each supported chapter uses three to five short paragraphs and covers at least three distinct evidence, mechanism, lived-expression, or integration layers.
- [ ] Run the reader-facing length calibration before the audit appendix: a completed Chinese book has 11,000–15,000 non-whitespace content characters, chapters 01–55 normally have at least 120 CJK content characters, and chapter 56 remains a concise five-question recap; inspect rather than pad any failed count.
- [ ] Confirm short chapters use `insufficient_basis` for the missing layer instead of repetition, generic advice, invented biography, or paraphrase padding.
- [ ] When a user-approved reference is used, confirm every `reference_traditional_interpretation` retains `source_ref`, `user_approved`, compatible `basis_refs`, and limitations.
- [ ] Confirm reference-derived content does not conflict with accepted calculation facts or satisfy a strict gate, and must not promote fact assurance.
- [ ] Confirm any reference conflict is omitted from prose and recorded in `execution_notes`.
- [ ] Confirm reader-facing chapters contain no internal workflow language about approval state, source IDs, configuration gates, project verification, or assurance mechanics; preserve all such metadata in the audit appendix.
- [ ] Confirm the finale and integrated portrait use one dominant archetype; any secondary archetype is clearly subordinate.
- [ ] Confirm the dominant archetype forms one spine across the prologue, chapter 15, chapter 41, and finale without becoming four copied paragraphs.
- [ ] Confirm Part I keeps Bazi and astrology independent until `chapter_15`.
- [ ] Confirm every Part II chapter describes a distinct lived pattern rather than repeating a generic trait.
- [ ] Confirm the five agency-related chapters remain distinct: chapter 18 judgment right, chapter 23 expression right, chapter 29 choice and life-narrative right, chapter 43 interpretation right, and chapter 53 public authorship right.
- [ ] Confirm every Part III chapter includes a protective function and possible cost without diagnostic language.
- [ ] Confirm Part IV includes Archetype, stability, protected value, belonging, freedom, commitment, resilience, cognitive Shadow, courage, relationship Fate, emotional maturity, creativity, social authorship, regret risk, operating cycle, and five Fate questions.
- [ ] Every analytical section and chapter contains an anchored claim or one `insufficient_basis` marker with a reason.
- [ ] Confirm every structured claim preserves its `basis_refs`, confidence, and material limitations in the audit appendix.
- [ ] Confirm cross-system language has cited Bazi and astrology anchors.
- [ ] Confirm the finale introduces no new fact or core conclusion.
- [ ] Confirm contradictions and uncertainty remain visible.
- [ ] Confirm the blueprint dimensions are not represented as the strict Dimension Coverage Policy, Primitive coverage, a frozen score, or strict Core Dynamics.
- [ ] Confirm no unsupported node, alias-normalized, diagnostic, scientific-certainty, guaranteed-behavior, or predictive claim appears.
- [ ] Confirm the traditional and inferential interpretation disclosure is present.
- [ ] Confirm reader-facing prose uses short paragraphs and keeps technical metadata in the audit appendix.
- [ ] Confirm reader-facing prose establishes evidence and mechanism before calibration, uses no more than one application-oriented paragraph per chapter, and does not read like a repetitive self-help checklist.
- [ ] Set `current_stage: REPORT_VALIDATED` only after every item passes; otherwise stop with `INFERENCE_GUARD_ERROR`.
