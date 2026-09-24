"""Authoritative admission helpers for candidate-only semantic assets."""

from pathlib import Path
from dataclasses import dataclass
from typing import FrozenSet, Mapping, Tuple

from .config_errors import ConfigError
from .semantic_mechanisms import (
    load_approved_evidence_root_ids,
    load_semantic_mechanism_candidates,
    validate_semantic_mechanism_candidate,
)


@dataclass(frozen=True)
class MappingEligibilitySnapshot:
    """Repository-derived mapping authority, separated from candidate payloads."""

    mechanisms: Tuple[Mapping[str, object], ...]
    policy_version: str

    @property
    def mechanism_ids(self) -> FrozenSet[str]:
        return frozenset(
            str(item["candidate_id"])
            for item in self.mechanisms
            if isinstance(item.get("candidate_id"), str)
        )


def load_mapping_eligible_semantic_mechanisms(
    mechanism_root: Path, role_policy: Mapping[str, Mapping[str, bool]]
) -> MappingEligibilitySnapshot:
    """Derive mapping authority from repository assets; callers cannot inject IDs."""
    try:
        approved_roots = load_approved_evidence_root_ids(mechanism_root)
        candidates = load_semantic_mechanism_candidates(mechanism_root)
    except ConfigError:
        return MappingEligibilitySnapshot((), "unavailable")
    eligible = []
    for candidate in candidates:
        authority = role_policy.get(str(candidate.get("evidence_role")), {})
        findings = validate_semantic_mechanism_candidate(candidate, approved_roots, mechanism_root)
        if (
            candidate.get("review_status") == "approved"
            and authority.get("mapping_origin") is True
            and not any(finding.severity == "error" for finding in findings)
        ):
            eligible.append(dict(candidate))
    return MappingEligibilitySnapshot(tuple(eligible), "semantic-mechanism-role-policy-v1")
