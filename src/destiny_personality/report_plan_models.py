from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class CandidateReportTopic:
    topic_id: str
    profile_refs: Tuple[str, ...]
    reason: str


@dataclass(frozen=True)
class CandidateReportPlan:
    schema_version: str
    core_profile_ref: str
    selected_topics: Tuple[CandidateReportTopic, ...]
    omitted_candidate_topics: Tuple[CandidateReportTopic, ...]
    section_plan: Tuple[str, ...]
    rendering_constraints: Tuple[str, ...]
    audit_trail: Tuple[str, ...]
