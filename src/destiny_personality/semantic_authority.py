"""Authoritative admission helpers for candidate-only semantic assets."""

from pathlib import Path
from typing import Mapping, Tuple

from .config_errors import ConfigError
from .semantic_mechanisms import (
    load_approved_evidence_root_ids,
    load_semantic_mechanism_candidates,
    validate_semantic_mechanism_candidate,
)


def load_mapping_eligible_semantic_mechanisms(
    mechanism_root: Path, role_policy: Mapping[str, Mapping[str, bool]]
) -> Tuple[Mapping[str, object], ...]:
    """Derive eligibility from repository assets; callers cannot inject IDs."""
    try:
        approved_roots = load_approved_evidence_root_ids(mechanism_root)
        candidates = load_semantic_mechanism_candidates(mechanism_root)
    except ConfigError:
        return ()
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
    return tuple(eligible)
