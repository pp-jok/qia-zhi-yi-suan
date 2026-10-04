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


@dataclass(frozen=True)
class ReleaseReportTopic:
    """A primitive claim explicitly admitted from one validated formal profile."""

    topic_id: str
    primitive_id: str
    state: str
    profile_refs: Tuple[str, ...]


@dataclass(frozen=True)
class ReleaseReportPlan:
    """Immutable, profile-bound plan for the limited-coverage release renderer."""

    schema_version: str
    core_profile_id: str
    profile_fingerprint: str
    renderer_profile: str
    section_ids: Tuple[str, ...]
    primitive_topics: Tuple[ReleaseReportTopic, ...]
    omitted_section_ids: Tuple[str, ...]
    containment_status: str
    audit_trail: Tuple[str, ...]
