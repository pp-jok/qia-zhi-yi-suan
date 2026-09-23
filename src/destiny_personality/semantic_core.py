"""Candidate-only Semantic Core infrastructure with explicit zero-state gates."""

from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import Mapping, Optional, Tuple

import yaml

from .config_errors import ConfigError


ROLE_POLICY_PATH = Path("candidates/semantic-core-v1/semantic_mechanism_role_policy_v1.yaml")


@dataclass(frozen=True)
class SemanticCoreCandidate:
    profile_ref: str
    mapping_candidates: Tuple[object, ...]
    signatures: Tuple[object, ...]
    dynamics: Tuple[object, ...]
    shadow_mature_forms: Tuple[object, ...]
    fate_themes: Tuple[object, ...]
    archetype: Optional[object]
    stage_statuses: Mapping[str, str]
    limitations: Tuple[str, ...]


@dataclass(frozen=True)
class SemanticBundlePromotion:
    status: str
    active_bundle_ref: str
    candidate_bundle_ref: str
    decision_ref: Optional[str]
    rollback_target: Optional[str]
    blockers: Tuple[str, ...]


@dataclass(frozen=True)
class SemanticCoreReportPlan:
    profile_ref: str
    renderer_profile: str
    sections: Tuple[str, ...]
    omitted_sections: Tuple[str, ...]
    containment_status: str


@dataclass(frozen=True)
class SemanticCoreDiff:
    changed_categories: Tuple[str, ...]


@dataclass(frozen=True)
class SemanticCoreRenderedReport:
    profile_ref: str
    sections: Tuple[str, ...]
    claim_refs: Tuple[str, ...]
    containment_status: str


def load_semantic_mechanism_role_policy(project_root: Path) -> Mapping[str, Mapping[str, bool]]:
    path = Path(project_root) / ROLE_POLICY_PATH
    try:
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise ConfigError("CONFIG_PARSE_ERROR", "cannot load role authority policy", file=str(ROLE_POLICY_PATH)) from exc
    if not isinstance(payload, dict) or payload.get("schema_version") != "semantic-mechanism-role-policy-v1":
        raise ConfigError("CONFIG_VERSION_MISMATCH", "invalid role authority policy", file=str(ROLE_POLICY_PATH))
    roles = payload.get("roles")
    if not isinstance(roles, dict):
        raise ConfigError("CONFIG_TYPE_ERROR", "roles must be a mapping", file=str(ROLE_POLICY_PATH), field="roles")
    required = {"evidence_admission", "mapping_origin", "primitive_direction", "primitive_state", "runtime_activation"}
    if any(not isinstance(value, dict) or set(value) != required or any(type(flag) is not bool for flag in value.values()) for value in roles.values()):
        raise ConfigError("CONFIG_VALUE_ERROR", "roles must declare complete boolean authority", file=str(ROLE_POLICY_PATH), field="roles")
    return roles


def mapping_eligibility_for_role(policy: Mapping[str, Mapping[str, bool]], role: str) -> Mapping[str, bool]:
    if role not in policy:
        raise ConfigError("CONFIG_GAP", "role is not governed", file=str(ROLE_POLICY_PATH), field=role)
    return dict(policy[role])


def build_semantic_core_candidate(profile_ref: str, approved_mapping_candidates: Tuple[object, ...]) -> SemanticCoreCandidate:
    if approved_mapping_candidates:
        raise ValueError("semantic formation requires separately approved formation policies")
    statuses = {stage: "blocked_by_gate" for stage in ("mapping", "primitive_v2", "signature", "dynamic", "theme", "archetype")}
    return SemanticCoreCandidate(profile_ref, (), (), (), (), (), None, statuses, ("APPROVED_MAPPING_REQUIRED",))


def promote_semantic_bundle(active_bundle_ref: str, candidate_bundle_ref: str, decision_ref: Optional[str]) -> SemanticBundlePromotion:
    if not isinstance(decision_ref, str) or not decision_ref.strip():
        return SemanticBundlePromotion("blocked_by_gate", active_bundle_ref, candidate_bundle_ref, None, None, ("PROMOTION_AUTHORIZATION_REQUIRED",))
    return SemanticBundlePromotion("shadow", active_bundle_ref, candidate_bundle_ref, decision_ref, active_bundle_ref, ())


def rollback_semantic_bundle(promotion: SemanticBundlePromotion) -> SemanticBundlePromotion:
    if promotion.status != "shadow" or not promotion.rollback_target:
        return SemanticBundlePromotion("blocked_by_gate", promotion.active_bundle_ref, promotion.candidate_bundle_ref, promotion.decision_ref, None, ("ROLLBACK_TARGET_UNAVAILABLE",))
    return SemanticBundlePromotion("rolled_back", promotion.rollback_target, promotion.candidate_bundle_ref, promotion.decision_ref, None, ())


def build_semantic_core_candidate_fingerprint(project_root: Path) -> str:
    root = Path(project_root) / "candidates" / "semantic-core-v1"
    canonical = b"".join(path.name.encode("utf-8") + b":" + sha256(path.read_bytes()).hexdigest().encode("ascii") + b"\n" for path in sorted(root.glob("*.yaml")))
    return sha256(canonical).hexdigest()


def audit_semantic_core_candidate(core: SemanticCoreCandidate) -> Mapping[str, object]:
    return {
        "profile_ref": core.profile_ref,
        "stage_statuses": dict(core.stage_statuses),
        "counts": {"mapping": len(core.mapping_candidates), "signature": len(core.signatures), "dynamic": len(core.dynamics), "theme": len(core.fate_themes)},
        "production_promotion": "blocked_by_gate" if "blocked_by_gate" in core.stage_statuses.values() else "requires_review",
        "limitations": core.limitations,
    }


def explain_semantic_core_item(core: SemanticCoreCandidate, item_id: str) -> Mapping[str, object]:
    collections = {"signature": core.signatures, "dynamic": core.dynamics, "theme": core.fate_themes}
    prefix = item_id.split(":", 1)[0]
    return {"status": "not_found", "item_id": item_id, "profile_ref": core.profile_ref, "limitations": core.limitations} if prefix not in collections or not collections[prefix] else {"status": "available", "item_id": item_id, "profile_ref": core.profile_ref}


def semantic_core_source_view(core: SemanticCoreCandidate, stage: str) -> Mapping[str, object]:
    """Expose stage counts only; source facts never become rendered claims here."""
    collections = {
        "mapping": core.mapping_candidates,
        "signature": core.signatures,
        "dynamic": core.dynamics,
        "theme": core.fate_themes,
        "archetype": (core.archetype,) if core.archetype else (),
    }
    if stage not in collections:
        raise ValueError("SEMANTIC_CORE_SOURCE_STAGE_INVALID")
    return {
        "profile_ref": core.profile_ref,
        "stage": stage,
        "status": core.stage_statuses.get(stage, "blocked_by_gate"),
        "item_count": len(collections[stage]),
        "containment_status": "profile_refs_only",
    }


def build_report_plan(core: SemanticCoreCandidate, renderer_profile: str) -> SemanticCoreReportPlan:
    allowed = {"concise-portrait-v1", "standard-portrait-v1", "dynamic-long-form-v1", "legacy-long-form-v2"}
    if renderer_profile not in allowed:
        raise ValueError("unsupported renderer profile")
    sections = tuple(name for name, values in (("signatures", core.signatures), ("dynamics", core.dynamics), ("fate_themes", core.fate_themes)) if values)
    omitted = tuple(name for name, values in (("signatures", core.signatures), ("dynamics", core.dynamics), ("fate_themes", core.fate_themes), ("archetype", (core.archetype,) if core.archetype else ())) if not values)
    return SemanticCoreReportPlan(core.profile_ref, renderer_profile, sections, omitted, "profile_refs_only")


def render_semantic_core_report(core: SemanticCoreCandidate, plan: SemanticCoreReportPlan) -> SemanticCoreRenderedReport:
    """Render only sections explicitly selected by the immutable ReportPlan."""
    if plan.profile_ref != core.profile_ref or plan.containment_status != "profile_refs_only":
        raise ValueError("REPORT_PLAN_PROFILE_CONTAINMENT_REQUIRED")
    claim_refs = tuple("report_plan." + section for section in plan.sections)
    return SemanticCoreRenderedReport(core.profile_ref, plan.sections, claim_refs, "profile_refs_only")


def diff_semantic_core_candidates(left: SemanticCoreCandidate, right: SemanticCoreCandidate) -> SemanticCoreDiff:
    categories = []
    for name in ("mapping_candidates", "signatures", "dynamics", "fate_themes", "archetype", "stage_statuses"):
        if getattr(left, name) != getattr(right, name):
            categories.append(name)
    return SemanticCoreDiff(tuple(categories))


def form_dominant_signatures(resolved_primitive_states: Tuple[object, ...]) -> Tuple[object, ...]:
    """Formation remains empty until an approved signature policy is supplied."""
    tuple(resolved_primitive_states)
    return ()


def form_core_dynamics(signatures: Tuple[object, ...]) -> Tuple[object, ...]:
    """No relation graph entry creates a Dynamic by default."""
    tuple(signatures)
    return ()


def form_shadow_mature(dynamics: Tuple[object, ...]) -> Tuple[object, ...]:
    tuple(dynamics)
    return ()


def form_fate_themes(dynamics: Tuple[object, ...]) -> Tuple[object, ...]:
    tuple(dynamics)
    return ()


def form_archetype(themes: Tuple[object, ...]) -> Optional[object]:
    tuple(themes)
    return None


def build_promotion_review_packet(candidate_bundle_ref: str, technical_checks: Tuple[str, ...], decision_ref: Optional[str]) -> Mapping[str, object]:
    """Separate reproducible engineering readiness from owner authorization."""
    engineering_status = "ready_for_review" if technical_checks and all(check == "PASS" for check in technical_checks) else "technical_checks_failed"
    blockers = () if isinstance(decision_ref, str) and decision_ref.strip() else ("PROMOTION_AUTHORIZATION_REQUIRED",)
    return {
        "candidate_bundle_ref": candidate_bundle_ref,
        "technical_checks": technical_checks,
        "engineering_status": engineering_status,
        "semantic_status": "approved_for_shadow" if not blockers and engineering_status == "ready_for_review" else "blocked_by_gate",
        "decision_ref": decision_ref,
        "blockers": blockers,
    }


def build_semantic_core_review_packet(
    approved_evidence_root_count: int,
    approved_mechanism_count: int,
    mapping_candidate_count: int,
    technical_checks: Tuple[str, ...],
) -> Mapping[str, object]:
    """Keep engineering completion distinct from semantic authorization."""
    engineering_status = "ready_for_review" if technical_checks and all(check == "PASS" for check in technical_checks) else "technical_checks_failed"
    blockers = () if mapping_candidate_count else ("APPROVED_MAPPING_CANDIDATE_REQUIRED",)
    return {
        "engineering_status": engineering_status,
        "semantic_readiness": "ready_for_review" if not blockers else "blocked_by_gate",
        "approved_evidence_root_count": approved_evidence_root_count,
        "approved_mechanism_count": approved_mechanism_count,
        "mapping_candidate_count": mapping_candidate_count,
        "technical_checks": technical_checks,
        "blockers": blockers,
    }
