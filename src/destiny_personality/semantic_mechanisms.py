"""Candidate-only governance for C2-SM semantic mechanism review."""

from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import Collection, Mapping, Optional, Tuple

import yaml

from .config_errors import ConfigError


MECHANISM_CONTRACT_FILE = "semantic_mechanism_contract_v1.yaml"
EVIDENCE_ROOT_CONTRACT_FILE = "semantic_evidence_root_contract_v1.yaml"
EVIDENCE_ROOT_REGISTRY_FILE = "semantic_evidence_root_registry_v1.yaml"
MECHANISM_SCHEMA_VERSION = "semantic-mechanism-v1"
EVIDENCE_ROOT_SCHEMA_VERSION = "semantic-evidence-root-v1"
EVIDENCE_ROOT_REGISTRY_SCHEMA_VERSION = "semantic-evidence-root-registry-v1"
DEFAULT_CONTRACT_ROOT = Path(__file__).resolve().parents[2] / "candidates" / "semantic-mechanisms-v1"


@dataclass(frozen=True)
class SemanticMechanismContracts:
    mechanism_schema_version: str
    evidence_root_schema_version: str
    allowed_roles: Tuple[str, ...]


@dataclass(frozen=True)
class SemanticMechanismFinding:
    code: str
    severity: str
    message: str


class _LoadedSemanticMechanismCandidate(dict):
    """Mapping payload that retains the contract root used for its admission."""

    def __init__(self, payload: Mapping[str, object], contract_root: Path) -> None:
        super().__init__(payload)
        self.contract_root = Path(contract_root)


def load_semantic_mechanism_contracts(root: Path) -> SemanticMechanismContracts:
    """Load the candidate-only contracts without registering runtime assets."""

    directory = Path(root)
    mechanism = _load_mapping(directory, MECHANISM_CONTRACT_FILE)
    evidence_root = _load_mapping(directory, EVIDENCE_ROOT_CONTRACT_FILE)
    _require_equal(
        mechanism, "schema_version", MECHANISM_SCHEMA_VERSION, MECHANISM_CONTRACT_FILE
    )
    _require_equal(
        evidence_root,
        "schema_version",
        EVIDENCE_ROOT_SCHEMA_VERSION,
        EVIDENCE_ROOT_CONTRACT_FILE,
    )
    roles = mechanism.get("allowed_roles")
    if type(roles) is not list or not roles or any(
        type(role) is not str or not role.strip() for role in roles
    ):
        raise ConfigError(
            "CONFIG_VALUE_ERROR",
            "allowed_roles must be a non-empty string list",
            file=MECHANISM_CONTRACT_FILE,
            field="allowed_roles",
        )
    return SemanticMechanismContracts(
        mechanism_schema_version=MECHANISM_SCHEMA_VERSION,
        evidence_root_schema_version=EVIDENCE_ROOT_SCHEMA_VERSION,
        allowed_roles=tuple(roles),
    )


def load_semantic_mechanism_candidates(root: Path) -> Tuple[Mapping[str, object], ...]:
    """Load zero or more review candidates; an empty registry is valid."""

    directory = Path(root) / "mechanism_candidates"
    if not directory.is_dir():
        return ()
    candidates = []
    for path in sorted(directory.glob("*.yaml")):
        candidates.append(
            _LoadedSemanticMechanismCandidate(
                _load_mapping(path.parent, path.name), Path(root)
            )
        )
    return tuple(candidates)


def load_approved_evidence_root_ids(root: Path) -> frozenset[str]:
    """Load Product Owner-approved root identifiers from the candidate registry.

    Only entries whose individual review state is explicitly ``approved`` are
    eligible for Semantic Mechanism candidate validation.
    """

    return frozenset(
        entry["evidence_root_id"]
        for entry in load_evidence_root_registry(root)
        if entry["review_status"] == "approved"
    )


def load_evidence_root_registry(root: Path) -> Tuple[Mapping[str, object], ...]:
    """Load a fail-closed candidate-only Evidence Root Registry."""

    directory = Path(root)
    registry = _load_mapping(directory, EVIDENCE_ROOT_REGISTRY_FILE)
    _require_equal(
        registry,
        "schema_version",
        EVIDENCE_ROOT_REGISTRY_SCHEMA_VERSION,
        EVIDENCE_ROOT_REGISTRY_FILE,
    )
    contract = _load_mapping(directory, EVIDENCE_ROOT_CONTRACT_FILE)
    _require_equal(
        contract,
        "schema_version",
        EVIDENCE_ROOT_SCHEMA_VERSION,
        EVIDENCE_ROOT_CONTRACT_FILE,
    )
    roots = _require_list(registry, "roots", EVIDENCE_ROOT_REGISTRY_FILE)
    required_fields = _require_string_list(
        contract, "required_root_fields", EVIDENCE_ROOT_CONTRACT_FILE
    )
    allowed_statuses = set(
        _require_string_list(
            contract, "allowed_review_statuses", EVIDENCE_ROOT_CONTRACT_FILE
        )
    )
    prohibited_origins = set(
        _require_string_list(
            contract, "prohibited_origins", EVIDENCE_ROOT_CONTRACT_FILE
        )
    )

    seen_ids = set()
    for index, root_entry in enumerate(roots):
        _validate_evidence_root(
            root_entry,
            index,
            seen_ids,
            required_fields,
            allowed_statuses,
            prohibited_origins,
        )
    return tuple(roots)


def build_evidence_root_audit_report(
    roots: Collection[Mapping[str, object]],
) -> Mapping[str, int]:
    """Summarize validated Evidence Root review states."""

    approved_count = sum(root["review_status"] == "approved" for root in roots)
    return {
        "root_count": len(roots),
        "approved_count": approved_count,
        "non_approved_count": len(roots) - approved_count,
    }


def validate_semantic_mechanism_candidate(
    candidate: Mapping[str, object],
    approved_root_ids: Collection[str],
    contract_root: Optional[Path] = None,
) -> Tuple[SemanticMechanismFinding, ...]:
    """Return audit findings; errors block admission and warnings require review."""

    findings = []
    (
        required_fields,
        allowed_roles,
        allowed_review_statuses,
        prohibited_origins,
    ) = _candidate_contract_rules(
        contract_root
        or _loaded_candidate_contract_root(candidate)
        or DEFAULT_CONTRACT_ROOT
    )
    fields_with_specific_findings = {
        "evidence_root_refs",
        "target_primitive_questions",
    }
    for field in required_fields:
        if (
            field not in fields_with_specific_findings
            and not _has_non_empty_value(candidate, field)
        ):
            findings.append(
                _finding("SEMANTIC_MECHANISM_CONTRACT_FIELD_REQUIRED", "error")
            )

    if not _is_non_empty_string(candidate.get("candidate_id")):
        findings.append(
            _finding("SEMANTIC_MECHANISM_INVALID_CANDIDATE_ID", "error")
        )

    if not _is_non_empty_string(candidate.get("source_system")):
        findings.append(
            _finding("SEMANTIC_MECHANISM_INVALID_SOURCE_SYSTEM", "error")
        )

    if not _is_non_empty_string_list(candidate.get("source_fact_classes")):
        findings.append(
            _finding("SEMANTIC_MECHANISM_INVALID_SOURCE_FACT_CLASSES", "error")
        )

    if not _is_non_empty_string(candidate.get("proposed_mechanism")):
        findings.append(
            _finding("SEMANTIC_MECHANISM_INVALID_PROPOSED_MECHANISM", "error")
        )

    evidence_role = candidate.get("evidence_role")
    if (
        _has_non_empty_value(candidate, "evidence_role")
        and evidence_role not in allowed_roles
    ):
        findings.append(_finding("SEMANTIC_MECHANISM_INVALID_ROLE", "error"))

    review_status = candidate.get("review_status")
    if (
        _has_non_empty_value(candidate, "review_status")
        and review_status not in allowed_review_statuses
    ):
        findings.append(
            _finding("SEMANTIC_MECHANISM_INVALID_REVIEW_STATUS", "error")
        )

    origin = candidate.get("origin")
    if not _is_non_empty_string(origin):
        findings.append(_finding("SEMANTIC_MECHANISM_INVALID_ORIGIN", "error"))
    elif origin == "golden_sample":
        findings.append(_finding("GOLDEN_SAMPLE_SEMANTIC_LEAK", "error"))
    elif origin in prohibited_origins:
        findings.append(_finding("SEMANTIC_MECHANISM_PROHIBITED_ORIGIN", "error"))

    if review_status == "approved" and not _is_non_empty_string(
        candidate.get("product_owner_decision_ref")
    ):
        findings.append(
            _finding("SEMANTIC_MECHANISM_APPROVAL_REFERENCE_REQUIRED", "error")
        )

    roots = candidate.get("evidence_root_refs")
    if type(roots) is not list or not roots or any(
        type(root) is not str or not root.strip() for root in roots
    ):
        findings.append(_finding("SEMANTIC_MECHANISM_EVIDENCE_ROOT_REQUIRED", "error"))
    elif not set(roots).issubset(set(approved_root_ids)):
        findings.append(_finding("SEMANTIC_MECHANISM_UNAPPROVED_ROOT", "error"))

    questions = candidate.get("target_primitive_questions")
    if type(questions) is not list or not questions or any(
        type(question) is not str or not question.strip() for question in questions
    ):
        findings.append(
            _finding("SEMANTIC_MECHANISM_PRIMITIVE_QUESTION_REQUIRED", "error")
        )

    state_assertion = candidate.get("asserts_primitive_state")
    if type(state_assertion) is not bool:
        findings.append(
            _finding("SEMANTIC_MECHANISM_INVALID_STATE_ASSERTION", "error")
        )
    elif state_assertion is True:
        findings.append(
            _finding("SEMANTIC_MECHANISM_DIRECT_STATE_ASSERTION", "error")
        )

    similarity = candidate.get("legacy_similarity")
    similarity_keys = {
        "same_source_conditions",
        "same_target_primitive",
        "same_direction",
    }
    if (
        type(similarity) is not dict
        or set(similarity) != similarity_keys
        or any(type(similarity[key]) is not bool for key in similarity_keys)
    ):
        findings.append(
            _finding("SEMANTIC_MECHANISM_INVALID_LEGACY_SIMILARITY", "error")
        )
    elif all(
        similarity.get(key) is True
        for key in similarity_keys
    ):
        findings.append(_finding("LEGACY_REINTRODUCTION_WARNING", "warning"))
    return tuple(findings)


def load_approved_semantic_mechanism_ids(root: Path) -> frozenset[str]:
    """Derive approved mechanism IDs from validated candidate assets only."""

    directory = Path(root)
    approved_root_ids = load_approved_evidence_root_ids(directory)
    approved_ids = set()
    for candidate in load_semantic_mechanism_candidates(directory):
        if candidate.get("review_status") != "approved":
            continue
        findings = validate_semantic_mechanism_candidate(
            candidate, approved_root_ids, directory
        )
        if any(finding.severity == "error" for finding in findings):
            continue
        approved_ids.add(candidate["candidate_id"])
    return frozenset(approved_ids)


def mapping_candidate_eligibility(
    candidate: Mapping[str, object], contract_root: Optional[Path] = None
) -> Tuple[SemanticMechanismFinding, ...]:
    """Use authoritative assets, never caller-supplied IDs, for eligibility."""

    mechanism_ref = candidate.get("mechanism_ref")
    root = (
        Path(contract_root)
        if isinstance(contract_root, (str, Path))
        else DEFAULT_CONTRACT_ROOT
    )
    from .semantic_authority import load_mapping_eligible_semantic_mechanisms
    from .semantic_core import load_semantic_mechanism_role_policy

    project_root = root.parents[1] if root.name == "semantic-mechanisms-v1" else root
    try:
        policy = load_semantic_mechanism_role_policy(project_root)
        eligible_ids = {
            item["candidate_id"]
            for item in load_mapping_eligible_semantic_mechanisms(root, policy)
        }
    except ConfigError:
        eligible_ids = set()
    if type(mechanism_ref) is not str or mechanism_ref not in eligible_ids:
        return (_finding("MAPPING_CANDIDATE_UNAPPROVED_MECHANISM", "error"),)
    return (_finding("MAPPING_CANDIDATE_ELIGIBLE_FOR_DESIGN_ONLY", "info"),)


def build_semantic_mechanism_audit_report(
    candidates: Collection[Mapping[str, object]],
    approved_root_ids: Collection[str],
    contract_root: Optional[Path] = None,
) -> Mapping[str, int]:
    """Summarize candidate review findings; an empty registry is valid."""

    findings = tuple(
        finding
        for candidate in candidates
        for finding in validate_semantic_mechanism_candidate(
            candidate, approved_root_ids, contract_root
        )
    )
    return {
        "candidate_count": len(candidates),
        "error_count": sum(finding.severity == "error" for finding in findings),
        "warning_count": sum(finding.severity == "warning" for finding in findings),
        "admission_eligible_count": sum(
            not validate_semantic_mechanism_candidate(
                candidate, approved_root_ids, contract_root
            )
            for candidate in candidates
        ),
    }


def _candidate_contract_rules(
    root: Path,
) -> Tuple[Tuple[str, ...], Tuple[str, ...], Tuple[str, ...], Tuple[str, ...]]:
    """Load the contract fields used to admit a candidate for review."""

    contract = _load_mapping(Path(root), MECHANISM_CONTRACT_FILE)
    _require_equal(
        contract,
        "schema_version",
        MECHANISM_SCHEMA_VERSION,
        MECHANISM_CONTRACT_FILE,
    )
    return (
        _require_string_list(
            contract, "required_candidate_fields", MECHANISM_CONTRACT_FILE
        ),
        _require_string_list(contract, "allowed_roles", MECHANISM_CONTRACT_FILE),
        _require_string_list(
            contract, "allowed_review_statuses", MECHANISM_CONTRACT_FILE
        ),
        _require_string_list(
            contract, "prohibited_origins", MECHANISM_CONTRACT_FILE
        ),
    )


def _has_non_empty_value(candidate: Mapping[str, object], field: str) -> bool:
    """Treat false as a valid required value while rejecting missing containers."""

    value = candidate.get(field)
    if value is None:
        return False
    if type(value) is str:
        return bool(value.strip())
    if type(value) in (list, dict, tuple, set):
        return bool(value)
    return True


def _is_non_empty_string(value: object) -> bool:
    return type(value) is str and bool(value.strip())


def _is_non_empty_string_list(value: object) -> bool:
    return type(value) is list and bool(value) and all(
        _is_non_empty_string(item) for item in value
    )


def _loaded_candidate_contract_root(candidate: Mapping[str, object]) -> Optional[Path]:
    if isinstance(candidate, _LoadedSemanticMechanismCandidate):
        return candidate.contract_root
    return None


def build_semantic_mechanism_candidate_fingerprint(root: Path) -> str:
    """Fingerprint only C2-SM candidate files, never active semantic assets."""

    directory = Path(root)
    files = sorted(path for path in directory.rglob("*.yaml") if path.is_file())
    canonical = b"".join(
        f"{path.relative_to(directory).as_posix()}:".encode("utf-8")
        + sha256(path.read_bytes()).hexdigest().encode("ascii")
        + b"\n"
        for path in files
    )
    return sha256(canonical).hexdigest()


def _load_mapping(directory: Path, filename: str) -> Mapping[str, object]:
    path = directory / filename
    if not path.is_file():
        raise ConfigError(
            "CONFIG_GAP",
            "required semantic mechanism contract is missing",
            file=filename,
        )
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise ConfigError(
            "CONFIG_PARSE_ERROR",
            "semantic mechanism contract cannot be parsed",
            file=filename,
        ) from exc
    if type(value) is not dict:
        raise ConfigError(
            "CONFIG_TYPE_ERROR",
            "semantic mechanism contract root must be a mapping",
            file=filename,
        )
    return value


def _require_equal(
    payload: Mapping[str, object], field: str, expected: str, filename: str
) -> None:
    if payload.get(field) != expected:
        raise ConfigError(
            "CONFIG_VERSION_MISMATCH",
            f"expected {field} {expected!r}",
            file=filename,
            field=field,
        )


def _require_list(
    payload: Mapping[str, object], field: str, filename: str
) -> list:
    value = payload.get(field)
    if type(value) is not list:
        raise ConfigError(
            "CONFIG_TYPE_ERROR",
            f"{field} must be a list",
            file=filename,
            field=field,
        )
    return value


def _require_string_list(
    payload: Mapping[str, object], field: str, filename: str
) -> Tuple[str, ...]:
    value = _require_list(payload, field, filename)
    if not value or any(type(item) is not str or not item.strip() for item in value):
        raise ConfigError(
            "CONFIG_VALUE_ERROR",
            f"{field} must be a non-empty string list",
            file=filename,
            field=field,
        )
    return tuple(value)


def _validate_evidence_root(
    root_entry: object,
    index: int,
    seen_ids: set,
    required_fields: Collection[str],
    allowed_statuses: Collection[str],
    prohibited_origins: Collection[str],
) -> None:
    field_prefix = f"roots[{index}]"
    if type(root_entry) is not dict:
        raise ConfigError(
            "CONFIG_TYPE_ERROR",
            "each evidence root must be a mapping",
            file=EVIDENCE_ROOT_REGISTRY_FILE,
            field=field_prefix,
        )
    for field in required_fields:
        if field not in root_entry:
            raise ConfigError(
                "CONFIG_GAP",
                f"each evidence root requires {field}",
                file=EVIDENCE_ROOT_REGISTRY_FILE,
                field=f"{field_prefix}.{field}",
            )

    for field in (
        "evidence_root_id",
        "system",
        "source_type",
        "source_ref",
        "version",
        "product_owner_decision_ref",
    ):
        value = root_entry[field]
        if type(value) is not str or not value.strip():
            raise ConfigError(
                "CONFIG_VALUE_ERROR",
                f"{field} must be a non-empty string",
                file=EVIDENCE_ROOT_REGISTRY_FILE,
                field=f"{field_prefix}.{field}",
            )

    root_id = root_entry["evidence_root_id"]
    if root_id in seen_ids:
        raise ConfigError(
            "CONFIG_VALUE_ERROR",
            "evidence_root_id must be unique",
            file=EVIDENCE_ROOT_REGISTRY_FILE,
            field=f"{field_prefix}.evidence_root_id",
        )
    seen_ids.add(root_id)

    review_status = root_entry["review_status"]
    if type(review_status) is not str or review_status not in allowed_statuses:
        raise ConfigError(
            "CONFIG_VALUE_ERROR",
            "review_status is not allowed by the root contract",
            file=EVIDENCE_ROOT_REGISTRY_FILE,
            field=f"{field_prefix}.review_status",
        )
    for field in ("scope", "provenance"):
        if type(root_entry[field]) is not dict or not root_entry[field]:
            raise ConfigError(
                "CONFIG_TYPE_ERROR",
                f"{field} must be a non-empty mapping",
                file=EVIDENCE_ROOT_REGISTRY_FILE,
                field=f"{field_prefix}.{field}",
            )
    for field in ("approved_use", "prohibited_use"):
        value = root_entry[field]
        if type(value) is not list or not value or any(
            type(item) is not str or not item.strip() for item in value
        ):
            raise ConfigError(
                "CONFIG_VALUE_ERROR",
                f"{field} must be a non-empty string list",
                file=EVIDENCE_ROOT_REGISTRY_FILE,
                field=f"{field_prefix}.{field}",
            )

    origin = root_entry["provenance"].get("origin")
    if type(origin) is not str or not origin.strip():
        raise ConfigError(
            "CONFIG_VALUE_ERROR",
            "provenance.origin must be a non-empty string",
            file=EVIDENCE_ROOT_REGISTRY_FILE,
            field=f"{field_prefix}.provenance.origin",
        )
    if origin in prohibited_origins:
        raise ConfigError(
            "CONFIG_VALUE_ERROR",
            "provenance.origin is prohibited by the root contract",
            file=EVIDENCE_ROOT_REGISTRY_FILE,
            field=f"{field_prefix}.provenance.origin",
        )


def _finding(code: str, severity: str) -> SemanticMechanismFinding:
    return SemanticMechanismFinding(code=code, severity=severity, message=code)
