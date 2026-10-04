from dataclasses import asdict
from hashlib import sha256
from typing import Tuple, Union

from .core_profile_models import CandidateCoreProfile, CoreDestinyProfile, StoppedCoreProfileExecution
from .core_destiny_profile_validation import validate_core_destiny_profile
from .report_plan_models import (
    CandidateReportPlan,
    CandidateReportTopic,
    ReleaseReportPlan,
    ReleaseReportTopic,
)


_RELEASE_RENDERER_PROFILES = frozenset(
    {
        "concise-portrait-v1",
        "standard-portrait-v1",
        "dynamic-long-form-v1",
        "legacy-long-form-v2",
    }
)
_RELEASE_BASE_SECTIONS = (
    "facts_summary",
    "core_profile",
    "report",
    "assurance",
    "limitations",
    "audit_refs",
)


def build_candidate_report_plan(
    profile: Union[CandidateCoreProfile, StoppedCoreProfileExecution],
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
        core_profile_ref=profile.candidate_profile_id,
        selected_topics=tuple(selected_topics),
        omitted_candidate_topics=tuple(omitted_topics),
        section_plan=tuple(topic.topic_id for topic in selected_topics),
        rendering_constraints=("no_new_semantic_conclusions",),
        audit_trail=("candidate-only", "profile-containment-required"),
    )


def build_release_report_plan(
    profile: CoreDestinyProfile, renderer_profile: str
) -> ReleaseReportPlan:
    """Select release sections solely from a validated formal Core Destiny Profile.

    Candidate and legacy profile planners intentionally remain separate.  A
    primitive topic is admitted only when the formal resolver has already
    resolved it to an evidence-backed non-unknown state.
    """

    if renderer_profile not in _RELEASE_RENDERER_PROFILES:
        raise ValueError("RELEASE_RENDERER_PROFILE_INVALID")
    errors = validate_core_destiny_profile(profile)
    if errors:
        raise ValueError("FORMAL_CDP_INVALID:" + errors[0])

    if renderer_profile == "legacy-long-form-v2":
        return ReleaseReportPlan(
            schema_version="release-report-plan-v1",
            core_profile_id=profile.core_profile_id,
            profile_fingerprint=release_profile_fingerprint(profile),
            renderer_profile=renderer_profile,
            section_ids=_RELEASE_BASE_SECTIONS,
            primitive_topics=(),
            omitted_section_ids=("legacy_semantic_reinterpretation",),
            containment_status="validated_cdp_only",
            audit_trail=("release-plan-v1", "legacy-frozen-handoff"),
        )

    topics = tuple(
        ReleaseReportTopic(
            topic_id="primitive:" + primitive_id,
            primitive_id=primitive_id,
            state=state.state,
            profile_refs=("primitive_states." + primitive_id,),
        )
        for primitive_id, state in sorted(profile.primitive_states.items())
        if state.state != "unknown"
    )
    omitted = tuple(
        "primitive:" + primitive_id
        for primitive_id, state in sorted(profile.primitive_states.items())
        if state.state == "unknown"
    )
    section_ids = _RELEASE_BASE_SECTIONS + tuple(topic.topic_id for topic in topics)
    if renderer_profile == "dynamic-long-form-v1" and profile.core_dynamics:
        section_ids += ("core_dynamics",)
    return ReleaseReportPlan(
        schema_version="release-report-plan-v1",
        core_profile_id=profile.core_profile_id,
        profile_fingerprint=release_profile_fingerprint(profile),
        renderer_profile=renderer_profile,
        section_ids=section_ids,
        primitive_topics=topics,
        omitted_section_ids=omitted,
        containment_status="validated_cdp_only",
        audit_trail=("release-plan-v1", "formal-cdp-contained"),
    )


def release_profile_fingerprint(profile: CoreDestinyProfile) -> str:
    """Bind a plan to the exact formal profile without consulting source facts."""

    return sha256(repr(asdict(profile)).encode("utf-8")).hexdigest()


def validate_release_report_plan(
    plan: ReleaseReportPlan, profile: CoreDestinyProfile
) -> Tuple[str, ...]:
    """Return deterministic containment failures for a release report plan."""

    if not isinstance(plan, ReleaseReportPlan):
        return ("REPORT_CONTAINMENT_VIOLATION",)
    if plan.core_profile_id != profile.core_profile_id:
        return ("REPORT_CONTAINMENT_VIOLATION",)
    if plan.profile_fingerprint != release_profile_fingerprint(profile):
        return ("REPORT_CONTAINMENT_VIOLATION",)
    if plan.containment_status != "validated_cdp_only":
        return ("REPORT_CONTAINMENT_VIOLATION",)
    try:
        expected = build_release_report_plan(profile, plan.renderer_profile)
    except ValueError:
        return ("REPORT_CONTAINMENT_VIOLATION",)
    return () if plan == expected else ("REPORT_CONTAINMENT_VIOLATION",)
