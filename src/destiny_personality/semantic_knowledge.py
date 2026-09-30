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
SOURCE_QUALITY_POLICY = "semantic_knowledge_source_quality_policy_v1.yaml"
METHODOLOGY_CONTRACT = "astrology_methodology_candidate_contract_v1.yaml"
METHODOLOGY_REGISTRY = "astrology_methodology_candidate_registry_v1.yaml"


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
    quality_policy = _mapping(directory / SOURCE_QUALITY_POLICY)
    _equal(quality_policy, "schema_version", "semantic-knowledge-source-quality-policy-v1", SOURCE_QUALITY_POLICY)
    quality_natures = quality_policy.get("evidence_nature_by_source_type")
    if type(quality_natures) is not dict:
        raise _error("evidence_nature_by_source_type must be a mapping", SOURCE_QUALITY_POLICY, None)
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
        expected_nature = quality_natures.get(source["source_type"])
        if source.get("evidence_nature") != expected_nature:
            raise _error("source type cannot masquerade as another evidence nature", SOURCE_REGISTRY, f"sources.{index}.evidence_nature")
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
        _validate_citations(claim, index, source_ids, set(_string_list(contract, "allowed_citation_support_roles", CLAIM_CONTRACT)))
        if claim.get("support_class") not in allowed_support:
            raise _error("invalid support_class", CLAIM_REGISTRY, f"claims.{index}.support_class")
        if claim.get("p004_relevance") not in allowed_relevance:
            raise _error("invalid p004_relevance", CLAIM_REGISTRY, f"claims.{index}.p004_relevance")
        if claim.get("review_status") not in allowed_status:
            raise _error("invalid review_status", CLAIM_REGISTRY, f"claims.{index}.review_status")
    _validate_relations(claims, set(_string_list(contract, "allowed_relation_types", CLAIM_CONTRACT)))
    return tuple(claims)


def build_semantic_knowledge_audit(
    sources: Tuple[Mapping[str, object], ...], claims: Tuple[Mapping[str, object], ...]
) -> Mapping[str, object]:
    """Produce a machine-readable candidate-governance audit, never a truth score."""

    def distribution(items: Tuple[Mapping[str, object], ...], field: str) -> Mapping[str, int]:
        values = sorted({str(item[field]) for item in items})
        return {value: sum(item[field] == value for item in items) for value in values}

    return {
        "source_count": len(sources),
        "claim_count": len(claims),
        "source_quality_distribution": distribution(sources, "source_quality_class"),
        "claim_support_distribution": distribution(claims, "support_class"),
        "unknown_source_refs": 0,
        "invalid_citations": 0,
        "invalid_claim_relations": 0,
        "self_relations": 0,
        "dangling_relations": 0,
        "direct_p004_claim_count": sum(item["p004_relevance"] == "DIRECT_ACTION_INITIATION" for item in claims),
        "school_specific_direct_claim_count": sum(item["support_class"] == "DIRECT_BUT_SCHOOL_SPECIFIC" for item in claims),
        "ambiguous_claim_count": sum(item["support_class"] == "AMBIGUOUS" for item in claims),
        "empirical_source_count": sum(item["evidence_nature"] == "empirical" for item in sources),
        "traditional_methodology_source_count": sum(item["evidence_nature"] == "traditional_methodology" for item in sources),
    }


def load_astrology_methodology_candidates(
    root: Path,
    sources: Tuple[Mapping[str, object], ...],
    claims: Tuple[Mapping[str, object], ...],
) -> Tuple[Mapping[str, object], ...]:
    """Load inactive P004-specific methodology candidates with fail-closed refs."""

    directory = Path(root)
    contract = _mapping(directory / METHODOLOGY_CONTRACT)
    registry = _mapping(directory / METHODOLOGY_REGISTRY)
    _equal(contract, "schema_version", "astrology-methodology-candidate-v1", METHODOLOGY_CONTRACT)
    _equal(registry, "schema_version", "astrology-methodology-candidate-registry-v1", METHODOLOGY_REGISTRY)
    _candidate_only(registry, METHODOLOGY_REGISTRY)
    required = _string_list(contract, "required_candidate_fields", METHODOLOGY_CONTRACT)
    required_nullable = _string_list(contract, "required_nullable_candidate_fields", METHODOLOGY_CONTRACT)
    allowed_status = set(_string_list(contract, "allowed_review_statuses", METHODOLOGY_CONTRACT))
    allowed_validation = set(
        _string_list(contract, "allowed_candidate_validation_statuses", METHODOLOGY_CONTRACT)
    )
    allowed_selection = set(
        _string_list(contract, "allowed_product_owner_selection_statuses", METHODOLOGY_CONTRACT)
    )
    allowed_materiality = set(
        _string_list(contract, "allowed_p004_materiality_roles", METHODOLOGY_CONTRACT)
    )
    material_roles = set(
        _string_list(contract, "material_p004_roles_requiring_evidence", METHODOLOGY_CONTRACT)
    )
    audit_fields = set(_string_list(contract, "required_condition_audit_fields", METHODOLOGY_CONTRACT))
    source_ids = {item["source_id"] for item in sources}
    claim_ids = {item["claim_id"] for item in claims}
    sources_by_id = {item["source_id"]: item for item in sources}
    claims_by_id = {item["claim_id"]: item for item in claims}
    candidates = _list(registry, "candidates", METHODOLOGY_REGISTRY)
    seen = set()
    for index, candidate in enumerate(candidates):
        _required(candidate, required, METHODOLOGY_REGISTRY, index)
        for field in required_nullable:
            if field not in candidate:
                raise _error("required nullable field missing", METHODOLOGY_REGISTRY, f"candidates.{index}.{field}")
        candidate_id = candidate.get("methodology_candidate_id")
        if not _nonempty(candidate_id) or candidate_id in seen:
            raise _error("duplicate or invalid methodology candidate id", METHODOLOGY_REGISTRY, f"candidates.{index}.methodology_candidate_id")
        seen.add(candidate_id)
        if candidate.get("review_status") not in allowed_status:
            raise _error("invalid methodology review_status", METHODOLOGY_REGISTRY, f"candidates.{index}.review_status")
        if candidate.get("candidate_validation_status") not in allowed_validation:
            raise _error("invalid candidate validation status", METHODOLOGY_REGISTRY, f"candidates.{index}.candidate_validation_status")
        if candidate.get("product_owner_selection_status") not in allowed_selection:
            raise _error("invalid product owner selection status", METHODOLOGY_REGISTRY, f"candidates.{index}.product_owner_selection_status")

        authority_sources = _known_refs(
            candidate, "method_authority_source_refs", source_ids, "unknown methodology authority source", index
        )
        authority_claims = _known_refs(
            candidate, "method_authority_claim_refs", claim_ids, "unknown methodology authority claim", index
        )
        boundary_sources = _known_refs(
            candidate, "boundary_source_refs", source_ids, "unknown methodology boundary source", index
        )
        boundary_claims = _known_refs(
            candidate, "boundary_claim_refs", claim_ids, "unknown methodology boundary claim", index
        )
        project_sources = _known_refs(
            candidate, "project_boundary_source_refs", source_ids, "unknown project boundary source", index
        )
        project_claims = _known_refs(
            candidate, "project_boundary_claim_refs", claim_ids, "unknown project boundary claim", index
        )
        if set(authority_sources) & (set(boundary_sources) | set(project_sources)):
            raise _error(
                "method authority and boundary source roles must be disjoint",
                METHODOLOGY_REGISTRY,
                f"candidates.{index}",
            )
        if set(authority_claims) & (set(boundary_claims) | set(project_claims)):
            raise _error(
                "method authority and boundary claim roles must be disjoint",
                METHODOLOGY_REGISTRY,
                f"candidates.{index}",
            )
        tradition = candidate["tradition_or_school"]
        for source_ref in authority_sources:
            if sources_by_id[source_ref].get("tradition_or_school") != tradition:
                raise _error(
                    "method authority source must match candidate tradition",
                    METHODOLOGY_REGISTRY,
                    f"candidates.{index}.method_authority_source_refs",
                )
        for claim_ref in authority_claims:
            if claims_by_id[claim_ref].get("tradition_or_school") != tradition:
                raise _error(
                    "method authority claim must match candidate tradition",
                    METHODOLOGY_REGISTRY,
                    f"candidates.{index}.method_authority_claim_refs",
                )

        _validate_methodology_approval(candidate, index)
        _validate_condition_technique_audit(
            candidate,
            index,
            audit_fields,
            allowed_materiality,
            material_roles,
            source_ids,
            claim_ids,
        )
    return tuple(candidates)


def _validate_methodology_approval(candidate: Mapping[str, object], index: int) -> None:
    status = candidate["review_status"]
    selection = candidate["product_owner_selection_status"]
    decision_ref = candidate["product_owner_decision_ref"]
    if status == "approved_for_semantic_design":
        if not _nonempty(decision_ref):
            raise _error(
                "approved methodology requires product_owner_decision_ref",
                METHODOLOGY_REGISTRY,
                f"candidates.{index}.product_owner_decision_ref",
            )
        if selection != "SELECTED_FOR_SEMANTIC_DESIGN":
            raise _error(
                "approved methodology must record product owner selection",
                METHODOLOGY_REGISTRY,
                f"candidates.{index}.product_owner_selection_status",
            )
    elif status == "proposed":
        if selection != "PENDING" or decision_ref is not None:
            raise _error(
                "proposed methodology must remain pending without a decision reference",
                METHODOLOGY_REGISTRY,
                f"candidates.{index}.product_owner_selection_status",
            )


def _validate_condition_technique_audit(
    candidate: Mapping[str, object],
    candidate_index: int,
    required_fields: set[str],
    allowed_materiality: set[str],
    material_roles: set[str],
    source_ids: set[str],
    claim_ids: set[str],
) -> None:
    audit = candidate.get("condition_technique_audit")
    if type(audit) is not list or not audit or any(type(item) is not dict for item in audit):
        raise _error(
            "condition_technique_audit must be a non-empty list of mappings",
            METHODOLOGY_REGISTRY,
            f"candidates.{candidate_index}.condition_technique_audit",
        )
    seen = set()
    for audit_index, item in enumerate(audit):
        field = f"candidates.{candidate_index}.condition_technique_audit.{audit_index}"
        if not required_fields.issubset(item):
            raise _error("condition audit field missing", METHODOLOGY_REGISTRY, field)
        technique = item.get("technique")
        if not _nonempty(technique) or technique in seen:
            raise _error("duplicate or invalid condition technique", METHODOLOGY_REGISTRY, field + ".technique")
        seen.add(technique)
        for text_field in ("method_role", "direction", "result"):
            if not _nonempty(item.get(text_field)):
                raise _error("condition audit text must be non-empty", METHODOLOGY_REGISTRY, field + "." + text_field)
        if type(item.get("required_by_method")) is not bool or type(item.get("required_by_p004")) is not bool:
            raise _error("condition audit requirement flags must be booleans", METHODOLOGY_REGISTRY, field)
        role = item.get("p004_role")
        if role not in allowed_materiality:
            raise _error("invalid P004 materiality role", METHODOLOGY_REGISTRY, field + ".p004_role")
        source_refs = item.get("source_refs")
        claim_refs = item.get("claim_refs")
        if type(source_refs) is not list or any(not _nonempty(ref) for ref in source_refs):
            raise _error("condition source_refs must be a string list", METHODOLOGY_REGISTRY, field + ".source_refs")
        if type(claim_refs) is not list or any(not _nonempty(ref) for ref in claim_refs):
            raise _error("condition claim_refs must be a string list", METHODOLOGY_REGISTRY, field + ".claim_refs")
        if not set(source_refs).issubset(source_ids):
            raise _error("unknown condition source reference", METHODOLOGY_REGISTRY, field + ".source_refs")
        if not set(claim_refs).issubset(claim_ids):
            raise _error("unknown condition claim reference", METHODOLOGY_REGISTRY, field + ".claim_refs")
        if role in material_roles and (not source_refs or not claim_refs):
            raise _error("P004 material role requires source and claim evidence", METHODOLOGY_REGISTRY, field)
        if item["required_by_p004"] and role not in material_roles:
            raise _error("required_by_p004 needs a material P004 role", METHODOLOGY_REGISTRY, field)


def _known_refs(
    candidate: Mapping[str, object],
    field: str,
    known: set[str],
    message: str,
    candidate_index: int,
) -> Tuple[str, ...]:
    refs = candidate.get(field)
    if not _nonempty_strings(refs) or not set(refs).issubset(known):
        raise _error(message, METHODOLOGY_REGISTRY, f"candidates.{candidate_index}.{field}")
    return tuple(refs)


def _mapping(path: Path) -> Mapping[str, object]:
    try:
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise _error("cannot read registry", path.name, None) from exc
    if type(payload) is not dict:
        raise _error("document must be a mapping", path.name, None)
    return payload


def _validate_citations(claim: Mapping[str, object], index: int, source_ids: set[str], roles: set[str]) -> None:
    citations = claim.get("citations")
    if type(citations) is not list or not citations:
        raise _error("citations must be a non-empty list", CLAIM_REGISTRY, f"claims.{index}.citations")
    for citation_index, citation in enumerate(citations):
        field = f"claims.{index}.citations.{citation_index}"
        if type(citation) is not dict or set(citation) != {"source_ref", "locator", "support_role"}:
            raise _error("citation must bind source_ref, locator, and support_role", CLAIM_REGISTRY, field)
        if citation["source_ref"] not in source_ids:
            raise _error("unknown source reference", CLAIM_REGISTRY, field + ".source_ref")
        if not _nonempty(citation["locator"]):
            raise _error("citation locator must be non-empty", CLAIM_REGISTRY, field + ".locator")
        if citation["support_role"] not in roles:
            raise _error("invalid citation support_role", CLAIM_REGISTRY, field + ".support_role")


def _validate_relations(claims: list[Mapping[str, object]], allowed: set[str]) -> None:
    ids = {item["claim_id"] for item in claims}
    for index, claim in enumerate(claims):
        relations = claim.get("related_claims")
        if type(relations) is not list:
            raise _error("related_claims must be a list", CLAIM_REGISTRY, f"claims.{index}.related_claims")
        seen = set()
        for relation_index, relation in enumerate(relations):
            field = f"claims.{index}.related_claims.{relation_index}"
            if type(relation) is not dict or set(relation) != {"claim_ref", "relation"}:
                raise _error("relation must contain claim_ref and relation", CLAIM_REGISTRY, field)
            ref, kind = relation["claim_ref"], relation["relation"]
            if ref == claim["claim_id"]:
                raise _error("self relation is not allowed", CLAIM_REGISTRY, field + ".claim_ref")
            if ref not in ids:
                raise _error("unknown related claim", CLAIM_REGISTRY, field + ".claim_ref")
            if kind not in allowed:
                raise _error("invalid claim relation", CLAIM_REGISTRY, field + ".relation")
            if (ref, kind) in seen:
                raise _error("duplicate claim relation", CLAIM_REGISTRY, field)
            seen.add((ref, kind))


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
