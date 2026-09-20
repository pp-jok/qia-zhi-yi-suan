from typing import Optional, Tuple

from .core_profile_models import CoreDestinyProfile
from .report_plan_models import CandidateReportPlan


def validate_candidate_report_plan(
    plan: CandidateReportPlan,
    profile: CoreDestinyProfile,
) -> Tuple[str, ...]:
    """Validate Profile containment for a candidate-only report plan."""

    errors = []
    if plan.core_profile_ref != profile.core_profile_id:
        errors.append("REPORT_PLAN_PROFILE_MISMATCH")
    if "no_new_semantic_conclusions" not in plan.rendering_constraints:
        errors.append("REPORT_PLAN_CONTAINMENT_CONSTRAINT_MISSING")
    for topic in plan.selected_topics:
        if not topic.topic_id.startswith("primitive:"):
            errors.append("REPORT_PLAN_TOPIC_NOT_PRIMITIVE")
        if not topic.profile_refs:
            errors.append("REPORT_PLAN_PROFILE_REF_MISSING")
            continue
        for profile_ref in topic.profile_refs:
            primitive_id = _primitive_id_from_ref(profile_ref)
            if primitive_id is None or primitive_id not in profile.primitive_states:
                errors.append("REPORT_PLAN_PROFILE_REF_INVALID")
            elif profile.primitive_states[primitive_id].state == "unknown":
                errors.append("REPORT_PLAN_UNKNOWN_TOPIC_SELECTED")
    return tuple(errors)


def _primitive_id_from_ref(profile_ref: str) -> Optional[str]:
    prefix = "primitive_states."
    if not profile_ref.startswith(prefix):
        return None
    return profile_ref[len(prefix):]
