# Controlled Portrait Business-Test Checklist

Use this checklist to compare the same approved test case across at least two agents. The goal is consistent evidence use and safety; identical prose is not required.

## Preconditions

- [ ] The case satisfies the Birth Input contract and records whether time is known.
- [ ] Each agent applies `compact-or-structured-birth-input-v1` to the same raw input and produces the same normalized date, local civil time or `unknown`, place text, and supplied sex label.
- [ ] Each agent uses `portrait` with `controlled_inference`.
- [ ] Each agent uses a qualified external calculation capability and records provenance.
- [ ] Required remote authorization is obtained for the current execution.
- [ ] No agent reads another agent's report before producing its own.

## Per-report acceptance

- [ ] **fact fidelity:** zero known hard-fact errors against the accepted capability output.
- [ ] **anchor coverage:** 100% of analytical claims retain valid `basis_refs`.
- [ ] **framework adherence:** claim types, assurance levels, confidence, tensions, and omissions follow the controlled contract.
- [ ] **disclosure completeness:** profile, assurance, provenance, missing facts, configuration limitations, and traditional/inferential boundary are present.
- [ ] **section completeness:** the four-part long-form structure and all fifty-six chapter dimensions are present; evidence gaps use `insufficient_basis` rather than filler.
- [ ] **chapter depth:** every supported chapter makes at least three distinct analytical moves across evidence, mechanism, lived expression, and integration; no generic advice, repeated trait summaries, invented biography, or paraphrase padding is counted as depth.
- [ ] **reader-first depth:** `reader-first-depth-v2` is declared; a completed Chinese report contains 11,000–15,000 non-whitespace reader-facing content characters, supported chapters 01–55 normally contain at least 120 CJK content characters, and failed counts are inspected rather than padded.
- [ ] **theme separation:** the five agency-related chapters separately cover judgment, expression, choice and life narrative, interpretation, and public authorship instead of repeating one autonomy claim.
- [ ] **narrative spine:** one dominant archetype appears with different functions in the prologue, chapter 15, chapter 41, and finale; any secondary label remains subordinate.
- [ ] **harmful overclaiming:** zero prohibited claims of diagnosis, scientific certainty, guaranteed behavior, guaranteed prediction, or strict verification.

## Cross-agent review

- [ ] Compare fact identity and assurance before comparing interpretation.
- [ ] Record unsupported core-claim conflicts; do not resolve them by averaging or majority vote.
- [ ] Treat differences in wording, examples, tone, and emphasis as acceptable when anchors and limitations agree.
- [ ] Fail the case if one agent invents a chart fact, hides a material limitation, or asserts cross-system support without both systems.

Passing this checklist confirms business-test workflow quality only. It does not certify the strict profile, approve missing project-owned assets, or prove statistical or scientific accuracy.
