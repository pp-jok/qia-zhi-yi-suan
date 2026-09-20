from dataclasses import dataclass
from typing import Optional, Tuple, Union

from .calculation.models import DeterministicChartFacts
from .core_profile_builder import build_candidate_core_profile
from .core_profile_models import CoreDestinyProfile, StoppedCoreProfileExecution
from .core_profile_validation import validate_candidate_profile
from .report_plan_models import CandidateReportPlan
from .report_plan_validation import validate_candidate_report_plan
from .report_planner import build_candidate_report_plan


@dataclass(frozen=True)
class CandidatePipelineExecution:
    status: str
    profile: Union[CoreDestinyProfile, StoppedCoreProfileExecution]
    report_plan: Optional[CandidateReportPlan]
    profile_validation_errors: Tuple[str, ...]
    report_plan_validation_errors: Tuple[str, ...]


def execute_candidate_pipeline(
    facts: DeterministicChartFacts,
    *,
    fact_assurance: str,
) -> CandidatePipelineExecution:
    """Execute the isolated candidate chain without invoking a renderer."""

    profile = build_candidate_core_profile(facts, fact_assurance=fact_assurance)
    if isinstance(profile, StoppedCoreProfileExecution):
        return CandidatePipelineExecution(
            status="stopped",
            profile=profile,
            report_plan=None,
            profile_validation_errors=(profile.failure_code,),
            report_plan_validation_errors=(),
        )
    profile_errors = validate_candidate_profile(profile)
    if profile_errors:
        return CandidatePipelineExecution(
            status="candidate_invalid",
            profile=profile,
            report_plan=None,
            profile_validation_errors=profile_errors,
            report_plan_validation_errors=(),
        )
    report_plan = build_candidate_report_plan(profile)
    report_plan_errors = validate_candidate_report_plan(report_plan, profile)
    return CandidatePipelineExecution(
        status="candidate_complete" if not report_plan_errors else "candidate_invalid",
        profile=profile,
        report_plan=report_plan,
        profile_validation_errors=(),
        report_plan_validation_errors=report_plan_errors,
    )
