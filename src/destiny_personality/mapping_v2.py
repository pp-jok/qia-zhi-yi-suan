"""Candidate-only Fresh Mapping v2 infrastructure."""

from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import Iterable, Mapping, Tuple

import yaml


@dataclass(frozen=True)
class MappingV2CandidateBundle:
    status: str
    bazi_rules: Tuple[object, ...]
    astrology_rules: Tuple[object, ...]
    blockers: Tuple[str, ...]


@dataclass(frozen=True)
class MappingV2CandidateRegistry:
    review_status: str
    candidates: Tuple[object, ...]


@dataclass(frozen=True)
class MappingV2Evaluation:
    status: str
    blockers: Tuple[str, ...]


def load_mapping_v2_candidate_registry(project_root: Path) -> MappingV2CandidateRegistry:
    path = Path(project_root) / "candidates" / "mapping-v2" / "mapping_v2_candidate_registry_v1.yaml"
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or payload.get("schema_version") != "mapping-v2-candidate-registry-v1":
        raise ValueError("MAPPING_V2_REGISTRY_VERSION_MISMATCH")
    candidates = payload.get("candidates")
    if payload.get("review_status") != "candidate_only" or not isinstance(candidates, list):
        raise ValueError("MAPPING_V2_REGISTRY_CONTRACT_ERROR")
    return MappingV2CandidateRegistry(payload["review_status"], tuple(candidates))


def build_fresh_mapping_candidates(mapping_eligible_mechanisms: Iterable[object]) -> Tuple[object, ...]:
    """No mechanism may become a Mapping without a separately authored candidate."""
    tuple(mapping_eligible_mechanisms)
    return ()


def compile_mapping_v2_candidate_bundle(
    candidates: Iterable[object], approved_mapping_eligible_ids: Iterable[str] = ()
) -> MappingV2CandidateBundle:
    """Compile only independently approved, mechanism-backed mapping records."""
    items = tuple(candidates)
    if not items:
        return MappingV2CandidateBundle("blocked_by_gate", (), (), ("APPROVED_MAPPING_CANDIDATE_REQUIRED",))
    eligible_ids = tuple(approved_mapping_eligible_ids)
    findings = tuple(
        finding
        for item in items
        for finding in validate_mapping_candidate(item, eligible_ids)
    )
    if findings:
        return MappingV2CandidateBundle("blocked_by_gate", (), (), tuple(sorted(set(findings))))
    bazi_rules = tuple(item for item in items if item["source_system"] == "bazi")
    astrology_rules = tuple(item for item in items if item["source_system"] == "astrology")
    return MappingV2CandidateBundle("candidate_compiled", bazi_rules, astrology_rules, ())


def validate_mapping_candidate(candidate: object, approved_mapping_eligible_ids: Iterable[str]) -> Tuple[str, ...]:
    """Reject direct Fact-to-Primitive mappings and unapproved mechanisms."""
    if not isinstance(candidate, dict):
        return ("MAPPING_CANDIDATE_TYPE_ERROR",)
    minimum_required = ("mapping_candidate_id", "semantic_mechanism_refs", "primitive_id", "primitive_question")
    if any(not candidate.get(field) for field in minimum_required):
        return ("MAPPING_CANDIDATE_CONTRACT_FIELD_REQUIRED",)
    refs = candidate["semantic_mechanism_refs"]
    if not isinstance(refs, list) or not all(isinstance(ref, str) and ref for ref in refs):
        return ("MAPPING_CANDIDATE_CONTRACT_FIELD_REQUIRED",)
    if not set(refs).issubset(set(approved_mapping_eligible_ids)):
        return ("APPROVED_MAPPING_ELIGIBLE_MECHANISM_REQUIRED",)
    required = (
        "mapping_candidate_id", "source_system", "canonical_fact_requirements",
        "semantic_mechanism_refs", "primitive_id", "primitive_question",
        "proposed_direction", "contexts", "evidence_root_refs", "limitations",
        "legacy_similarity", "audit_trail", "review_status",
    )
    findings = []
    if any(not candidate.get(field) for field in required):
        findings.append("MAPPING_CANDIDATE_CONTRACT_FIELD_REQUIRED")
    if candidate.get("source_system") not in {"bazi", "astrology"}:
        findings.append("MAPPING_CANDIDATE_SOURCE_SYSTEM_INVALID")
    for field in ("canonical_fact_requirements", "contexts", "evidence_root_refs", "limitations", "audit_trail"):
        if not isinstance(candidate.get(field), list) or not all(isinstance(value, str) and value for value in candidate.get(field, ())):
            findings.append("MAPPING_CANDIDATE_CONTRACT_FIELD_REQUIRED")
    if not isinstance(candidate.get("proposed_direction"), Mapping) or not candidate.get("proposed_direction"):
        findings.append("MAPPING_CANDIDATE_DIRECTION_REQUIRED")
    if not isinstance(candidate.get("legacy_similarity"), Mapping):
        findings.append("MAPPING_CANDIDATE_LEGACY_SIMILARITY_REQUIRED")
    if candidate.get("origin") in {"legacy_output", "golden_sample", "runtime_output"}:
        findings.append("MAPPING_CANDIDATE_PROHIBITED_ORIGIN")
    if candidate.get("direct_fact_to_primitive") is True:
        findings.append("MAPPING_CANDIDATE_DIRECT_FACT_TO_PRIMITIVE_PROHIBITED")
    if candidate.get("review_status") != "approved":
        findings.append("MAPPING_CANDIDATE_APPROVAL_REQUIRED")
    return tuple(sorted(set(findings)))


def audit_mapping_v2_candidates(
    candidates: Iterable[object], approved_mapping_eligible_ids: Iterable[str]
) -> Mapping[str, object]:
    """Return a machine-readable candidate audit without activating any record."""
    items = tuple(candidates)
    findings = tuple(
        finding
        for item in items
        for finding in validate_mapping_candidate(item, approved_mapping_eligible_ids)
    )
    return {
        "candidate_count": len(items),
        "status": "blocked_by_gate" if findings or not items else "candidate_compiled",
        "findings": tuple(sorted(set(findings))) if findings else (("APPROVED_MAPPING_CANDIDATE_REQUIRED",) if not items else ()),
    }


def mapping_v2_candidate_fingerprint(project_root: Path) -> str:
    root = Path(project_root) / "candidates" / "mapping-v2"
    canonical = b"".join(path.name.encode("utf-8") + b":" + sha256(path.read_bytes()).hexdigest().encode("ascii") + b"\n" for path in sorted(root.glob("*.yaml")))
    return sha256(canonical).hexdigest()


def run_mapping_v2_calibration(approved_bundle: Iterable[object]) -> MappingV2Evaluation:
    return MappingV2Evaluation("blocked_by_gate", ("APPROVED_MAPPING_V2_BUNDLE_REQUIRED",)) if not tuple(approved_bundle) else MappingV2Evaluation("ready_for_review", ())


def run_mapping_v2_holdout(approved_bundle: Iterable[object]) -> MappingV2Evaluation:
    return MappingV2Evaluation("blocked_by_gate", ("APPROVED_MAPPING_V2_BUNDLE_REQUIRED",)) if not tuple(approved_bundle) else MappingV2Evaluation("ready_for_review", ())
