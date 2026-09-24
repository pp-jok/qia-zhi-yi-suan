"""Deterministic persistence for candidate-only Semantic Core records."""

import json
from pathlib import Path

from .semantic_core import SemanticCoreCandidate


def write_semantic_core_candidate(core: SemanticCoreCandidate, path: Path) -> None:
    payload = {
        "schema_version": "semantic-core-candidate-v1",
        "profile_ref": core.profile_ref,
        "mapping_candidates": list(core.mapping_candidates),
        "signatures": list(core.signatures),
        "dynamics": list(core.dynamics),
        "shadow_mature_forms": list(core.shadow_mature_forms),
        "fate_themes": list(core.fate_themes),
        "archetype": core.archetype,
        "stage_statuses": dict(core.stage_statuses),
        "limitations": list(core.limitations),
    }
    Path(path).write_text(json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")


def load_semantic_core_candidate(path: Path) -> SemanticCoreCandidate:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if payload.get("schema_version") == "semantic-pipeline-core-v1":
        return _pipeline_payload_to_candidate(payload)
    if payload.get("schema_version") != "semantic-core-candidate-v1":
        raise ValueError("SEMANTIC_CORE_CODEC_VERSION_MISMATCH")
    return SemanticCoreCandidate(
        payload["profile_ref"], tuple(payload["mapping_candidates"]), tuple(payload["signatures"]),
        tuple(payload["dynamics"]), tuple(payload["shadow_mature_forms"]), tuple(payload["fate_themes"]),
        payload["archetype"], dict(payload["stage_statuses"]), tuple(payload["limitations"]),
    )


def _pipeline_payload_to_candidate(payload: object) -> SemanticCoreCandidate:
    if not isinstance(payload, dict) or not isinstance(payload.get("core"), dict):
        raise ValueError("SEMANTIC_CORE_CODEC_VERSION_MISMATCH")
    core = payload["core"]
    required = ("profile_ref", "mapping_candidates", "signatures", "dynamics", "shadow_mature_forms", "fate_themes", "stage_statuses", "limitations")
    if any(field not in core for field in required) or not isinstance(core["stage_statuses"], dict):
        raise ValueError("SEMANTIC_CORE_CODEC_VERSION_MISMATCH")
    return SemanticCoreCandidate(
        core["profile_ref"], tuple(core["mapping_candidates"]), tuple(core["signatures"]),
        tuple(core["dynamics"]), tuple(core["shadow_mature_forms"]), tuple(core["fate_themes"]),
        core.get("archetype"), dict(core["stage_statuses"]), tuple(core["limitations"]),
    )
