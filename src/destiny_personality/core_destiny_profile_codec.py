"""Deterministic JSON codec for the formal Core Destiny Profile."""

from dataclasses import asdict
import json
from pathlib import Path
from typing import Mapping

from .core_destiny_profile_validation import validate_core_destiny_profile
from .core_profile_models import CoreDestinyProfile, CrossSystemAlignment, PrimitiveCandidate, PrimitiveState


def core_destiny_profile_to_dict(profile: CoreDestinyProfile) -> dict:
    """Return a JSON-safe representation with no implicit semantic expansion."""

    return asdict(profile)


def core_destiny_profile_from_dict(payload: Mapping[str, object]) -> CoreDestinyProfile:
    if not isinstance(payload, Mapping) or payload.get("schema_version") != "core-destiny-profile-v1":
        raise ValueError("FORMAL_CDP_SCHEMA_INVALID")
    try:
        profile = CoreDestinyProfile(
            schema_version=_string(payload, "schema_version"),
            core_profile_id=_string(payload, "core_profile_id"),
            fact_packet_refs=_tuple_of_strings(payload["fact_packet_refs"]),
            fact_assurance=_string(payload, "fact_assurance"),
            semantic_model_assurance=_string(payload, "semantic_model_assurance"),
            semantic_model_versions=tuple(
                _version_pair(value) for value in _sequence(payload["semantic_model_versions"])
            ),
            bazi_primitive_candidates=tuple(
                _candidate(value) for value in _sequence(payload["bazi_primitive_candidates"])
            ),
            astrology_primitive_candidates=tuple(
                _candidate(value) for value in _sequence(payload["astrology_primitive_candidates"])
            ),
            primitive_states={
                key: _state(value)
                for key, value in _mapping(payload["primitive_states"]).items()
                if isinstance(key, str)
            },
            cross_system_alignment=tuple(
                _alignment(value) for value in _sequence(payload["cross_system_alignment"])
            ),
            dominant_signatures=tuple(_sequence(payload["dominant_signatures"])),
            core_dynamics=tuple(_sequence(payload["core_dynamics"])),
            shadow_mature_forms=tuple(_sequence(payload["shadow_mature_forms"])),
            fate_themes=tuple(_sequence(payload["fate_themes"])),
            archetype=payload["archetype"],
            contradictions=_tuple_of_strings(payload["contradictions"]),
            limitations=_tuple_of_strings(payload["limitations"]),
            unresolved_questions=_tuple_of_strings(payload["unresolved_questions"]),
            audit_trail=_tuple_of_strings(payload["audit_trail"]),
        )
    except (KeyError, TypeError, ValueError, AttributeError) as error:
        raise ValueError("FORMAL_CDP_CONTRACT_INVALID") from error
    errors = validate_core_destiny_profile(profile)
    if errors:
        raise ValueError(errors[0])
    return profile


def load_core_destiny_profile(path: Path) -> CoreDestinyProfile:
    try:
        return core_destiny_profile_from_dict(json.loads(path.read_text(encoding="utf-8")))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError("FORMAL_CDP_JSON_INVALID") from error


def write_core_destiny_profile(profile: CoreDestinyProfile, path: Path) -> None:
    errors = validate_core_destiny_profile(profile)
    if errors:
        raise ValueError(errors[0])
    path.write_text(
        json.dumps(core_destiny_profile_to_dict(profile), ensure_ascii=False, indent=2, sort_keys=True)
        + "\n",
        encoding="utf-8",
    )


def _candidate(value: object) -> PrimitiveCandidate:
    item = _mapping(value)
    return PrimitiveCandidate(
        primitive_id=_string(item, "primitive_id"),
        source_system=_string(item, "source_system"),
        direction=_string(item, "direction"),
        fact_refs=_tuple_of_strings(item["fact_refs"]),
        semantic_rule_refs=_tuple_of_strings(item["semantic_rule_refs"]),
        contexts=_tuple_of_strings(item["contexts"]),
        salience=_string(item, "salience"),
        evidence_stability=_string(item, "evidence_stability"),
        modifier_refs=_tuple_of_strings(item["modifier_refs"]),
        counterevidence_refs=_tuple_of_strings(item["counterevidence_refs"]),
        expression_mode=_string(item, "expression_mode"),
        tension_level=_string(item, "tension_level"),
        counterweight_effect=item["counterweight_effect"],
        limitations=_tuple_of_strings(item["limitations"]),
    )


def _state(value: object) -> PrimitiveState:
    item = _mapping(value)
    context_states = _mapping(item["context_states"])
    if not all(isinstance(key, str) and isinstance(state, str) for key, state in context_states.items()):
        raise ValueError("FORMAL_CDP_CONTRACT_INVALID")
    return PrimitiveState(
        primitive_id=_string(item, "primitive_id"),
        state=_string(item, "state"),
        evidence_refs=_tuple_of_strings(item["evidence_refs"]),
        resolution_rule_ref=_string(item, "resolution_rule_ref"),
        context_states=dict(context_states),
        supporting_candidates=_tuple_of_strings(item["supporting_candidates"]),
        counter_candidates=_tuple_of_strings(item["counter_candidates"]),
        contradictions=_tuple_of_strings(item["contradictions"]),
        unresolved_contexts=_tuple_of_strings(item["unresolved_contexts"]),
        limitations=_tuple_of_strings(item["limitations"]),
    )


def _alignment(value: object) -> CrossSystemAlignment:
    item = _mapping(value)
    salience_delta = item.get("salience_delta", 0)
    if not isinstance(salience_delta, int):
        raise ValueError("FORMAL_CDP_CONTRACT_INVALID")
    return CrossSystemAlignment(
        alignment_id=_string(item, "alignment_id"),
        primitive_id=_string(item, "primitive_id"),
        context_refs=_tuple_of_strings(item["context_refs"]),
        status=_string(item, "status"),
        direction_relation=_string(item, "direction_relation"),
        bazi_rule_refs=_tuple_of_strings(item["bazi_rule_refs"]),
        astrology_rule_refs=_tuple_of_strings(item["astrology_rule_refs"]),
        limitations=_tuple_of_strings(item["limitations"]),
        salience_delta=salience_delta,
    )


def _mapping(value: object) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        raise ValueError("FORMAL_CDP_CONTRACT_INVALID")
    return value


def _sequence(value: object) -> tuple:
    if not isinstance(value, (list, tuple)):
        raise ValueError("FORMAL_CDP_CONTRACT_INVALID")
    return tuple(value)


def _tuple_of_strings(value: object) -> tuple:
    items = _sequence(value)
    if not all(isinstance(item, str) for item in items):
        raise ValueError("FORMAL_CDP_CONTRACT_INVALID")
    return items


def _string(payload: Mapping[str, object], key: str) -> str:
    value = payload[key]
    if not isinstance(value, str):
        raise ValueError("FORMAL_CDP_CONTRACT_INVALID")
    return value


def _version_pair(value: object) -> tuple:
    values = _tuple_of_strings(value)
    if len(values) != 2:
        raise ValueError("FORMAL_CDP_CONTRACT_INVALID")
    return values
