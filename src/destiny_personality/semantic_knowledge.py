"""Candidate-only registry for methodology sources and semantic claims.

These assets preserve why a proposed semantic mechanism may be reviewed.  They
are deliberately not part of fact resolution, activation, or Mapping authority.
"""

from pathlib import Path
from typing import Mapping, Tuple

import yaml

from .config_errors import ConfigError


SOURCE_CONTRACT = "semantic_knowledge_source_contract_v1.yaml"
SOURCE_REGISTRY = "semantic_knowledge_source_registry_v1.yaml"
CLAIM_CONTRACT = "semantic_knowledge_claim_contract_v1.yaml"
CLAIM_REGISTRY = "semantic_knowledge_claim_registry_v1.yaml"


def load_semantic_knowledge_source_registry(root: Path) -> Tuple[Mapping[str, object], ...]:
    """Load candidate-only methodology sources with explicit bibliographic identity."""

    directory = Path(root)
    contract = _mapping(directory / SOURCE_CONTRACT)
    registry = _mapping(directory / SOURCE_REGISTRY)
    _equal(contract, "schema_version", "semantic-knowledge-source-v1", SOURCE_CONTRACT)
    _equal(registry, "schema_version", "semantic-knowledge-source-registry-v1", SOURCE_REGISTRY)
    _candidate_only(registry, SOURCE_REGISTRY)
    required = _string_list(contract, "required_source_fields", SOURCE_CONTRACT)
    allowed_types = set(_string_list(contract, "allowed_source_types", SOURCE_CONTRACT))
    allowed_quality = set(_string_list(contract, "allowed_quality_classes", SOURCE_CONTRACT))
    allowed_status = set(_string_list(contract, "allowed_review_statuses", SOURCE_CONTRACT))
    sources = _list(registry, "sources", SOURCE_REGISTRY)
    seen = set()
    for index, source in enumerate(sources):
        _required(source, required, SOURCE_REGISTRY, index)
        source_id = source.get("source_id")
        if not _nonempty(source_id) or source_id in seen:
            raise _error("duplicate or invalid source_id", SOURCE_REGISTRY, f"sources.{index}.source_id")
        seen.add(source_id)
        if source.get("source_type") not in allowed_types:
            raise _error("invalid source_type", SOURCE_REGISTRY, f"sources.{index}.source_type")
        if source.get("source_quality_class") not in allowed_quality:
            raise _error("invalid source_quality_class", SOURCE_REGISTRY, f"sources.{index}.source_quality_class")
        if source.get("review_status") not in allowed_status:
            raise _error("invalid review_status", SOURCE_REGISTRY, f"sources.{index}.review_status")
    return tuple(sources)


def load_semantic_knowledge_claim_registry(
    root: Path, sources: Tuple[Mapping[str, object], ...]
) -> Tuple[Mapping[str, object], ...]:
    """Load auditable claims and reject any chain with an unknown methodology source."""

    directory = Path(root)
    contract = _mapping(directory / CLAIM_CONTRACT)
    registry = _mapping(directory / CLAIM_REGISTRY)
    _equal(contract, "schema_version", "semantic-knowledge-claim-v1", CLAIM_CONTRACT)
    _equal(registry, "schema_version", "semantic-knowledge-claim-registry-v1", CLAIM_REGISTRY)
    _candidate_only(registry, CLAIM_REGISTRY)
    required = _string_list(contract, "required_claim_fields", CLAIM_CONTRACT)
    allowed_status = set(_string_list(contract, "allowed_review_statuses", CLAIM_CONTRACT))
    allowed_support = set(_string_list(contract, "allowed_support_classes", CLAIM_CONTRACT))
    allowed_relevance = set(_string_list(contract, "allowed_p004_relevance", CLAIM_CONTRACT))
    source_ids = {item["source_id"] for item in sources}
    claims = _list(registry, "claims", CLAIM_REGISTRY)
    seen = set()
    for index, claim in enumerate(claims):
        _required(claim, required, CLAIM_REGISTRY, index)
        claim_id = claim.get("claim_id")
        if not _nonempty(claim_id) or claim_id in seen:
            raise _error("duplicate or invalid claim_id", CLAIM_REGISTRY, f"claims.{index}.claim_id")
        seen.add(claim_id)
        refs = claim.get("source_refs")
        if not _nonempty_strings(refs):
            raise _error("source_refs must be a non-empty string list", CLAIM_REGISTRY, f"claims.{index}.source_refs")
        if not set(refs).issubset(source_ids):
            raise _error("unknown source reference", CLAIM_REGISTRY, f"claims.{index}.source_refs")
        if not _nonempty_strings(claim.get("source_locators")):
            raise _error("source_locators must be a non-empty string list", CLAIM_REGISTRY, f"claims.{index}.source_locators")
        if claim.get("support_class") not in allowed_support:
            raise _error("invalid support_class", CLAIM_REGISTRY, f"claims.{index}.support_class")
        if claim.get("p004_relevance") not in allowed_relevance:
            raise _error("invalid p004_relevance", CLAIM_REGISTRY, f"claims.{index}.p004_relevance")
        if claim.get("review_status") not in allowed_status:
            raise _error("invalid review_status", CLAIM_REGISTRY, f"claims.{index}.review_status")
    return tuple(claims)


def _mapping(path: Path) -> Mapping[str, object]:
    try:
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise _error("cannot read registry", path.name, None) from exc
    if type(payload) is not dict:
        raise _error("document must be a mapping", path.name, None)
    return payload


def _equal(payload: Mapping[str, object], field: str, expected: str, file: str) -> None:
    if payload.get(field) != expected:
        raise _error(f"{field} must equal {expected}", file, field)


def _candidate_only(payload: Mapping[str, object], file: str) -> None:
    if payload.get("review_status") != "candidate_only" or payload.get("activation_status") != "inactive":
        raise _error("registry must remain candidate_only and inactive", file, None)


def _required(payload: object, fields: Tuple[str, ...], file: str, index: int) -> None:
    if type(payload) is not dict:
        raise _error("registry entry must be a mapping", file, f"entries.{index}")
    for field in fields:
        if field not in payload or payload[field] in (None, ""):
            raise _error("required field missing", file, f"entries.{index}.{field}")


def _list(payload: Mapping[str, object], field: str, file: str) -> list[Mapping[str, object]]:
    value = payload.get(field)
    if type(value) is not list or any(type(item) is not dict for item in value):
        raise _error(f"{field} must be a list of mappings", file, field)
    return value


def _string_list(payload: Mapping[str, object], field: str, file: str) -> Tuple[str, ...]:
    value = payload.get(field)
    if not _nonempty_strings(value):
        raise _error(f"{field} must be a non-empty string list", file, field)
    return tuple(value)


def _nonempty_strings(value: object) -> bool:
    return type(value) is list and bool(value) and all(_nonempty(item) for item in value)


def _nonempty(value: object) -> bool:
    return type(value) is str and bool(value.strip())


def _error(message: str, file: str, field: object) -> ConfigError:
    return ConfigError("CONFIG_VALUE_ERROR", message, file=file, field=field)
