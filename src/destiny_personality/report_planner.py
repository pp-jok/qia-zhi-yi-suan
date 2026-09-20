from typing import Union

from .core_profile_models import CoreDestinyProfile, StoppedCoreProfileExecution
from .report_plan_models import CandidateReportPlan, CandidateReportTopic


def build_candidate_report_plan(
    profile: Union[CoreDestinyProfile, StoppedCoreProfileExecution],
) -> CandidateReportPlan:
    """Plan candidate output from Profile evidence without adding semantics."""

    if isinstance(profile, StoppedCoreProfileExecution):
        raise ValueError("cannot plan a stopped execution artifact")
    selected_topics = []
    omitted_topics = []
    for primitive_id, state in sorted(profile.primitive_states.items()):
        topic = CandidateReportTopic(
            topic_id=f"primitive:{primitive_id}",
            profile_refs=(f"primitive_states.{primitive_id}",),
            reason=f"state:{state.state}",
        )
        if state.state == "unknown":
            omitted_topics.append(topic)
        else:
            selected_topics.append(topic)
    return CandidateReportPlan(
        schema_version="candidate-report-plan-v1",
        core_profile_ref=profile.core_profile_id,
        selected_topics=tuple(selected_topics),
        omitted_candidate_topics=tuple(omitted_topics),
        section_plan=tuple(topic.topic_id for topic in selected_topics),
        rendering_constraints=("no_new_semantic_conclusions",),
        audit_trail=("candidate-only", "profile-containment-required"),
    )
