"""Lossless JSON codec for the candidate-only Core Profile IR."""

from dataclasses import asdict
import json
from pathlib import Path
from typing import Mapping

from .core_profile_models import CandidateCoreProfile, CandidateFactScope, CrossSystemAlignment, PrimitiveCandidate, PrimitiveState
from .core_profile_validation import validate_candidate_profile


def candidate_profile_to_dict(profile: CandidateCoreProfile) -> dict:
    return asdict(profile)


def candidate_profile_from_dict(payload: Mapping[str, object]) -> CandidateCoreProfile:
    if payload.get("schema_version") != "candidate-core-profile-v1":
        raise ValueError("CANDIDATE_PROFILE_SCHEMA_INVALID")
    try:
        scope = CandidateFactScope(**payload["fact_scope"])
        profile = CandidateCoreProfile(
            schema_version=payload["schema_version"], candidate_profile_id=payload["candidate_profile_id"],
            fact_fingerprint=payload["fact_fingerprint"], fact_scope=scope, fact_assurance=payload["fact_assurance"],
            semantic_model_assurance=payload["semantic_model_assurance"], semantic_capability_level=payload["semantic_capability_level"],
            semantic_bundle_fingerprint=payload["semantic_bundle_fingerprint"],
            semantic_model_versions=tuple(tuple(item) for item in payload["semantic_model_versions"]),
            bazi_primitive_candidates=tuple(_candidate(item) for item in payload["bazi_primitive_candidates"]),
            astrology_primitive_candidates=tuple(_candidate(item) for item in payload["astrology_primitive_candidates"]),
            cross_system_alignments=tuple(_alignment(item) for item in payload["cross_system_alignments"]),
            primitive_states={key: _state(value) for key, value in payload["primitive_states"].items()},
            limitations=tuple(payload["limitations"]),
        )
    except (KeyError, TypeError, AttributeError) as error:
        raise ValueError("CANDIDATE_PROFILE_CONTRACT_INVALID") from error
    errors = validate_candidate_profile(profile)
    if errors:
        raise ValueError(errors[0])
    return profile


def load_candidate_profile(path: Path) -> CandidateCoreProfile:
    try:
        return candidate_profile_from_dict(json.loads(path.read_text(encoding="utf-8")))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError("CANDIDATE_PROFILE_JSON_INVALID") from error


def write_candidate_profile(profile: CandidateCoreProfile, path: Path) -> None:
    path.write_text(json.dumps(candidate_profile_to_dict(profile), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _candidate(value: Mapping[str, object]) -> PrimitiveCandidate:
    return PrimitiveCandidate(**{**value, **{key: tuple(value[key]) for key in ("fact_refs", "semantic_rule_refs", "contexts", "modifier_refs", "counterevidence_refs", "limitations")}})


def _alignment(value: Mapping[str, object]) -> CrossSystemAlignment:
    return CrossSystemAlignment(**{**value, **{key: tuple(value[key]) for key in ("context_refs", "bazi_rule_refs", "astrology_rule_refs", "limitations")}})


def _state(value: Mapping[str, object]) -> PrimitiveState:
    return PrimitiveState(**{**value, **{key: tuple(value[key]) for key in ("evidence_refs", "supporting_candidates", "counter_candidates", "contradictions", "unresolved_contexts", "limitations")}})
