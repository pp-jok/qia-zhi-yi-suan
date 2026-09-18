# Long-Form Personality Book Blueprint

This blueprint is `legacy-long-form-v2`. It fixes the historical report format
and content dimensions while allowing chapter titles and prose to reflect the
current fact basis. It is a legacy renderer and coverage contract, not a source
of chart facts or strict semantic values. It must not provide Primitive,
Signature, Dynamic, Theme, or Archetype inputs to the Core Profile pipeline.

## Chapter depth model

A supported chapter is a developed argument, not a heading plus a trait
summary. Use three to five short paragraphs and cover at least three of these
four layers; cover all four whenever the accepted facts permit:

1. `evidence layer`: identify the chart fact or an already anchored conclusion
   that makes this chapter relevant.
2. `mechanism layer`: explain how the evidence could become the named
   personality dynamic without presenting interpretation as certainty.
3. `lived-expression layer`: show one or more concrete differences between
   ordinary, pressured, relational, or work contexts. Examples illustrate the
   mechanism and must not invent biographical facts.
4. `integration layer`: name the protective value, possible cost, and a mature
   way to use or recalibrate the pattern.

Do not force every chapter into identical labels or sentence templates. The
reader-facing book remains continuous prose. Depth comes from distinct
analytical moves, not restating the same trait, paraphrase padding, generic
advice, invented scenes, or a page-count target. When evidence cannot support
three layers, keep the chapter visible and use `insufficient_basis` with the
missing basis instead of filler.

For `reader-first-depth-v2`, a completed Chinese book uses 11,000 to 15,000
non-whitespace reader-facing content characters before the audit appendix.
Supported chapters 01 through 55 use three to five short paragraphs and at
least 120 CJK content characters; chapter 56 remains a concise five-question
recap. Treat both measurements as a lower-bound regression alarm, then inspect
semantic moves manually. Never pad a chapter to satisfy the count.

Use a reader-first paragraph rhythm. Establish evidence and mechanism before
offering mature integration. At most one paragraph per chapter should read as
calibration or application; the chapter must not become a list of instructions.
Prefer descriptions of mature expression over repeated commands to the reader.

When a user-approved reference report is supplied, compatible traditional
interpretations may enrich the relevant chapter as a
`reference_traditional_interpretation`. Keep the prose readable, but retain
the reference source and missing-verification limitation in the audit appendix.
Never use a reference conclusion to repair a conflicting calculation fact or
to imply that the generic Skill owns the reference's semantic rules.

Use one dominant archetype as the book's memorable closing image. If another
archetype adds value, present it as a subordinate lens, role, or cognitive
method instead of a competing title. Keep source qualification and internal
workflow mechanics in the audit appendix so the main book reads as a coherent
portrait rather than an execution log.

## Front matter and prologue

The first page contains `命格人格书`, the subtitle `八字 × 西方占星完整核心画像`,
minimum birth information, the Bazi main chart, Western astrology axes, and a
short list of important structures. Begin the prologue on the same page when
layout permits. The prologue introduces the central contradiction shared by
the two systems and ends with an inviting thesis rather than a technical
summary.

## Part I: 15 chapters - What the chart itself says

Keep Bazi and astrology independent through `chapter_14`. Cross-system claims
begin only in `chapter_15`.

1. `chapter_01` - `bazi_day_master_environment`: day master, month environment,
   and observed pillar context; omit strength classification when unsupported.
2. `chapter_02` - `bazi_primary_resource_pattern`: the most important Bazi
   input, support, learning, or internalization pattern.
3. `chapter_03` - `bazi_agency_self_pattern`: autonomy, peer, self, or agency
   pattern visible in the supplied Ten-God facts.
4. `chapter_04` - `bazi_reality_resource_pattern`: reality, exchange, resource,
   and result orientation visible in the supplied facts.
5. `chapter_05` - `bazi_rules_expression_tension`: the chart's supported rules,
   authority, expression, or questioning tension.
6. `chapter_06` - `bazi_overall_structure`: evidence-bounded Bazi summary,
   explicit omissions, and the system's leading personality question.
7. `chapter_07` - `astrology_core_axis`: Sun, Moon, Ascendant, and the central
   personality axis.
8. `chapter_08` - `astrology_cognition_pattern`: Mercury and other supported
   cognition indicators.
9. `chapter_09` - `astrology_cognition_tension`: the strongest supported
   cognitive aspect or constraint.
10. `chapter_10` - `astrology_emotional_freedom_pattern`: Moon, emotional
    safety, freedom, and the strongest relevant aspect.
11. `chapter_11` - `astrology_action_execution_pattern`: Mars and supported
    action or execution structure; do not invent dignity status.
12. `chapter_12` - `astrology_relationship_pattern`: Venus and supported
    relationship aspects.
13. `chapter_13` - `astrology_public_expression_pattern`: personal-planet and
    angular house emphasis, social role, expression, or authorship.
14. `chapter_14` - `astrology_depth_pattern`: supported depth, hidden-process,
    psychological, or meaning-seeking indicators.
15. `chapter_15` - `first_cross_system_synthesis`: compare only already stated
    Bazi and astrology claims; identify agreements, tensions, and context.

## Part II: 9 chapters - How those structures become a person

16. `chapter_16` - `core_temperament`
17. `chapter_17` - `verification_and_trust`
18. `chapter_18` - `judgment_right`
19. `chapter_19` - `freedom_within_structure`
20. `chapter_20` - `deepest_fear_or_avoidance`
21. `chapter_21` - `execution_and_convergence`
22. `chapter_22` - `reason_and_value_decisions`
23. `chapter_23` - `expression_right`
24. `chapter_24` - `accurate_understanding_and_recognition`

Each chapter turns supported chart structure into a distinct lived pattern.
Do not repeat the same generic trait under different titles.

## Part III: 16 chapters - Shadow, protection, and fate undercurrents

25. `chapter_25` - `primary_defense`
26. `chapter_26` - `rupture_process`
27. `chapter_27` - `ending_trigger`
28. `chapter_28` - `authority_and_persuasion`
29. `chapter_29` - `choice_and_life_narrative_right`
30. `chapter_30` - `emotional_blind_spot`
31. `chapter_31` - `understanding_versus_relationship_reality`
32. `chapter_32` - `unfinished_meaning`
33. `chapter_33` - `control_and_comprehensibility`
34. `chapter_34` - `risk_preference`
35. `chapter_35` - `standards_and_pressure`
36. `chapter_36` - `problem_prioritization`
37. `chapter_37` - `potential_versus_actuality`
38. `chapter_38` - `understanding_versus_having`
39. `chapter_39` - `imbalance_poles`
40. `chapter_40` - `mature_recalibration`

Every chapter identifies both the protective function and the possible cost.
Do not moralize Shadow language or represent it as pathology.

## Part IV: 16 chapters - Integrated destiny-personality portrait

41. `chapter_41` - `archetype`
42. `chapter_42` - `source_of_stability`
43. `chapter_43` - `interpretation_right`
44. `chapter_44` - `belonging_without_self_loss`
45. `chapter_45` - `freedom_and_exit`
46. `chapter_46` - `commitment_and_closed_possibilities`
47. `chapter_47` - `adaptive_resilience`
48. `chapter_48` - `cognitive_shadow`
49. `chapter_49` - `courage_pattern`
50. `chapter_50` - `relationship_fate_tension`
51. `chapter_51` - `emotional_maturity`
52. `chapter_52` - `creative_essence`
53. `chapter_53` - `public_authorship_right`
54. `chapter_54` - `regret_risk`
55. `chapter_55` - `optimal_operating_cycle`
56. `chapter_56` - `five_fate_questions`

The five fate questions are concise recurring tensions derived from earlier
chapters. They must not predict events or claim unavoidable outcomes.

## Agency-theme separation

Five agency-related chapters have different jobs and must not paraphrase one
generic autonomy trait:

- Chapter 18 is the **judgment right**: having a real seat in consequential
  decisions and preserving independent evaluation inside collaboration.
- Chapter 23 is the **expression right**: forming and speaking a version the
  person understands and can responsibly own.
- Chapter 29 is the **choice and life-narrative right**: ensuring major choices
  retain the person's values and authorship rather than merely satisfying an
  external script.
- Chapter 43 is the **interpretation right**: retaining authority to make
  meaning from one's own experience while acknowledging outside influence.
- Chapter 53 is the **public authorship right**: turning a private method into
  visible, usable, and challengeable social contribution.

Each chapter must use its own evidence, mechanism, context, and cost. Repeated
phrases about freedom, control, or authorship do not satisfy the separation.

## Finale and execution notes

Name one dominant archetype in the prologue, chapter 15, chapter 41, and finale
so the book has a stable narrative spine. The first mention invites, chapter 15
confirms the cross-system synthesis, chapter 41 develops the full image, and
the finale reprises it without adding claims. A secondary label may appear only
as a subordinate cognitive lens, role, or method.

The finale restates the archetype and integrates the established tensions into
one continuous closing image. It introduces no new claim. Follow it with a
compact audit appendix containing fact assurance, capability provenance,
omissions, limitations, claim anchors, and the traditional/inferential
disclosure.

## Narrative rhythm and visual hierarchy

- Use a restrained black-on-white book layout with generous margins and page
  numbers.
- Use large bold headings for parts and chapters and thin separators between
  major transitions.
- Prefer short paragraphs, deliberate line breaks, and one idea per paragraph.
- Use occasional bold thesis lines; do not bold every paragraph.
- Keep reader-facing prose natural and immersive. Place technical claim IDs
  and evidence metadata in the audit appendix.
- Target long-form depth by applying the chapter depth model. Do not hit a
  length target with repetition or generic filler; use `insufficient_basis`
  when evidence cannot support a dimension.
