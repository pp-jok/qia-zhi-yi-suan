"""Lossless JSON codec for policy-driven candidate Semantic Core records."""

import json
from pathlib import Path
from typing import Mapping


def write_pipeline_core(core: Mapping[str, object], formation_policies: Mapping[str, object], path: Path) -> None:
    from .semantic_pipeline import semantic_pipeline_fingerprint
    versions = {stage: str(policy.get("policy_version", "unversioned")) if isinstance(policy, Mapping) else str(policy) for stage, policy in sorted(formation_policies.items())}
    payload = {"schema_version": "semantic-pipeline-core-v1", "core": core, "formation_policy_versions": versions, "formation_policy_fingerprint": semantic_pipeline_fingerprint(formation_policies)}
    Path(path).write_text(json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")


def load_pipeline_core(path: Path) -> dict:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if payload.get("schema_version") != "semantic-pipeline-core-v1" or not isinstance(payload.get("core"), dict) or not isinstance(payload.get("formation_policy_versions"), dict) or not isinstance(payload.get("formation_policy_fingerprint"), str):
        raise ValueError("SEMANTIC_PIPELINE_CORE_CODEC_INVALID")
    return {"core": _restore_tuples(payload["core"]), "formation_policy_versions": payload["formation_policy_versions"], "formation_policy_fingerprint": payload["formation_policy_fingerprint"]}


def _restore_tuples(value: object) -> object:
    if isinstance(value, list):
        return tuple(_restore_tuples(item) for item in value)
    if isinstance(value, dict):
        return {key: _restore_tuples(item) for key, item in value.items()}
    return value
