"""Natural-language presentation for an already validated, limited-coverage CDP.

This module deliberately receives no raw chart facts, mapping registry, or
candidate asset.  The report can only restate information explicitly selected
by the release report plan.
"""

from dataclasses import dataclass
from typing import Mapping, Tuple

from .core_destiny_profile_validation import validate_core_destiny_profile
from .core_profile_models import CoreDestinyProfile
from .report_plan_models import ReleaseReportPlan, ReleaseReportTopic
from .report_planner import validate_release_report_plan


@dataclass(frozen=True)
class ReleaseRenderedReport:
    schema_version: str
    core_profile_id: str
    renderer_profile: str
    facts_summary: Mapping[str, object]
    core_profile: Mapping[str, object]
    report: Mapping[str, object]
    assurance: Mapping[str, object]
    limitations: Tuple[str, ...]
    audit_refs: Tuple[str, ...]


def render_release_report(
    profile: CoreDestinyProfile, plan: ReleaseReportPlan
) -> ReleaseRenderedReport:
    """Render a plan-verified report without adding claims or reading registries."""

    if validate_core_destiny_profile(profile) or validate_release_report_plan(plan, profile):
        raise ValueError("REPORT_CONTAINMENT_VIOLATION")
    if plan.renderer_profile == "legacy-long-form-v2":
        report = _legacy_handoff(profile)
    else:
        report = _planned_report(profile, plan.primitive_topics)
    counts = _state_counts(profile)
    return ReleaseRenderedReport(
        schema_version="release-rendered-report-v1",
        core_profile_id=profile.core_profile_id,
        renderer_profile=plan.renderer_profile,
        facts_summary={
            "fact_packet_refs": profile.fact_packet_refs,
            "fact_assurance": profile.fact_assurance,
        },
        core_profile={
            "semantic_model_versions": profile.semantic_model_versions,
            "primitive_state_counts": counts,
            "resolved_primitive_ids": tuple(
                topic.primitive_id for topic in plan.primitive_topics
            ),
        },
        report=report,
        assurance={
            "fact_assurance": profile.fact_assurance,
            "semantic_model_assurance": profile.semantic_model_assurance,
            "coverage_status": "limited",
        },
        limitations=profile.limitations + profile.unresolved_questions,
        audit_refs=profile.audit_trail + plan.audit_trail,
    )


def _state_counts(profile: CoreDestinyProfile) -> Mapping[str, int]:
    counts = {}
    for state in profile.primitive_states.values():
        counts[state.state] = counts.get(state.state, 0) + 1
    return {state: counts[state] for state in sorted(counts)}


def _planned_report(
    profile: CoreDestinyProfile, topics: Tuple[ReleaseReportTopic, ...]
) -> Mapping[str, object]:
    interpretations = tuple(_primitive_interpretation(profile, topic) for topic in topics)
    if interpretations:
        summary = "Only primitive states supported by active approved mappings are included."
    else:
        summary = (
            "No primitive-level interpretation is included because this release "
            "has no approved active mapping coverage."
        )
    return {
        "kind": "contained_release_report",
        "summary": summary,
        "primitive_interpretations": interpretations,
    }


def _primitive_interpretation(
    profile: CoreDestinyProfile, topic: ReleaseReportTopic
) -> Mapping[str, object]:
    state = profile.primitive_states[topic.primitive_id]
    return {
        "primitive_id": topic.primitive_id,
        "state": topic.state,
        "statement": "{} is reported as {} from approved active mapping evidence.".format(
            topic.primitive_id, topic.state
        ),
        "evidence_refs": state.evidence_refs,
        "semantic_rule_refs": state.supporting_candidates + state.counter_candidates,
        "limitations": state.limitations,
    }


def _legacy_handoff(profile: CoreDestinyProfile) -> Mapping[str, object]:
    return {
        "kind": "legacy_compatibility_handoff",
        "status": "frozen",
        "message": (
            "legacy-long-form-v2 remains a separate frozen compatibility path; "
            "the formal release profile is not reinterpreted with legacy semantics."
        ),
        "formal_profile_ref": profile.core_profile_id,
    }
