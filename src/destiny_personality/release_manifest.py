"""Strict loader for the limited-coverage release primitive closure."""

from dataclasses import dataclass
from pathlib import Path
from typing import Mapping, Optional, Tuple

import yaml


CORE_PRIMITIVE_IDS = frozenset({"P001", "P002", "P003", "P004", "P005", "P006"})
MANIFEST_SCHEMA_VERSION = "release-primitive-coverage-v1"
_TERMINAL_STATUSES = frozenset(
    {
        "CLOSED_NO_DEFENSIBLE_CONSTRUCT_UNDER_REVIEWED_ASSETS",
        "CLOSED_SYSTEM_SPECIFIC_RESEARCH",
    }
)
_CLOSED_UNDER_REVIEWED_ASSETS = "CLOSED_NO_DEFENSIBLE_CONSTRUCT_UNDER_REVIEWED_ASSETS"
_P004_CLOSURE = "CLOSED_SYSTEM_SPECIFIC_RESEARCH"
_NO_CURRENT_DEFENSIBLE_MAPPING = "NO_CURRENT_DEFENSIBLE_MAPPING"
_EXPECTED_FINAL_STATUS = {
    primitive_id: _CLOSED_UNDER_REVIEWED_ASSETS
    for primitive_id in CORE_PRIMITIVE_IDS - {"P004"}
}
_EXPECTED_FINAL_STATUS["P004"] = _P004_CLOSURE
_EXPECTED_SYSTEM_CLOSURES = {
    primitive_id: {
        "bazi": _NO_CURRENT_DEFENSIBLE_MAPPING,
        "astrology": _NO_CURRENT_DEFENSIBLE_MAPPING,
    }
    for primitive_id in CORE_PRIMITIVE_IDS - {"P004"}
}
_EXPECTED_SYSTEM_CLOSURES["P004"] = {
    "astrology": "CLOSED_UNDER_CURRENT_HELLENISTIC_METHODOLOGY",
    "bazi": "DEFERRED_WITH_REASON:METHOD_RESEARCH_SATURATED",
}


@dataclass(frozen=True)
class PrimitiveClosure:
    primitive_id: str
    final_status: str
    resolver_capability: str
    primary_evidence_refs: Tuple[str, ...]
    mapping_refs: Tuple[str, ...]
    evidence_root_refs: Tuple[str, ...]
    system_closures: Mapping[str, str]
    research_report_ref: str


@dataclass(frozen=True)
class ExtendedInventory:
    status: str
    primitive_ids: Tuple[str, ...]
    reason: str


@dataclass(frozen=True)
class ReleaseManifest:
    schema_version: str
    release_id: str
    core_primitives: Mapping[str, PrimitiveClosure]
    extended_inventory: ExtendedInventory


def release_manifest_path() -> Path:
    """Return the package-owned release asset without consulting candidate assets."""
    return Path(__file__).resolve().parent / "release_assets" / "v1" / "primitive_coverage_v1.yaml"


def load_release_manifest(path: Optional[Path] = None) -> ReleaseManifest:
    """Load the release closure and reject malformed or non-zero coverage states."""
    manifest_path = Path(path) if path is not None else release_manifest_path()
    try:
        payload = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as error:
        raise ValueError("RELEASE_MANIFEST_INVALID") from error
    return _parse_release_manifest(payload)


def _parse_release_manifest(payload: object) -> ReleaseManifest:
    if not isinstance(payload, dict):
        raise ValueError("RELEASE_MANIFEST_INVALID")
    if payload.get("schema_version") != MANIFEST_SCHEMA_VERSION:
        raise ValueError("RELEASE_MANIFEST_INVALID")
    release_id = payload.get("release_id")
    if not isinstance(release_id, str) or not release_id:
        raise ValueError("RELEASE_MANIFEST_INVALID")

    raw_closures = payload.get("core_primitives")
    if not isinstance(raw_closures, dict) or set(raw_closures) != CORE_PRIMITIVE_IDS:
        raise ValueError("RELEASE_MANIFEST_INVALID")
    closures = {
        primitive_id: _parse_primitive_closure(primitive_id, raw_closures[primitive_id])
        for primitive_id in sorted(CORE_PRIMITIVE_IDS)
    }
    return ReleaseManifest(
        schema_version=MANIFEST_SCHEMA_VERSION,
        release_id=release_id,
        core_primitives=closures,
        extended_inventory=_parse_extended_inventory(payload.get("extended_inventory")),
    )


def _parse_primitive_closure(primitive_id: str, payload: object) -> PrimitiveClosure:
    if not isinstance(payload, dict):
        raise ValueError("RELEASE_MANIFEST_INVALID")
    final_status = payload.get("final_status")
    if (
        final_status not in _TERMINAL_STATUSES
        or final_status != _EXPECTED_FINAL_STATUS[primitive_id]
        or payload.get("resolver_capability") != "unknown"
    ):
        raise ValueError("RELEASE_MANIFEST_INVALID")
    primary_evidence_refs = _string_tuple(payload.get("primary_evidence_refs"))
    mapping_refs = _string_tuple(payload.get("mapping_refs"))
    evidence_root_refs = _string_tuple(payload.get("evidence_root_refs"))
    if primary_evidence_refs or mapping_refs:
        raise ValueError("RELEASE_MANIFEST_INVALID")
    system_closures = payload.get("system_closures")
    if system_closures != _EXPECTED_SYSTEM_CLOSURES[primitive_id]:
        raise ValueError("RELEASE_MANIFEST_INVALID")
    report_ref = payload.get("research_report_ref")
    if not isinstance(report_ref, str) or not report_ref:
        raise ValueError("RELEASE_MANIFEST_INVALID")
    return PrimitiveClosure(
        primitive_id=primitive_id,
        final_status=final_status,
        resolver_capability="unknown",
        primary_evidence_refs=primary_evidence_refs,
        mapping_refs=mapping_refs,
        evidence_root_refs=evidence_root_refs,
        system_closures=dict(system_closures),
        research_report_ref=report_ref,
    )


def _parse_extended_inventory(payload: object) -> ExtendedInventory:
    if not isinstance(payload, dict) or payload.get("status") != "EMPTY_DEFERRED":
        raise ValueError("RELEASE_MANIFEST_INVALID")
    primitive_ids = _string_tuple(payload.get("primitive_ids"))
    reason = payload.get("reason")
    if primitive_ids or not isinstance(reason, str) or not reason:
        raise ValueError("RELEASE_MANIFEST_INVALID")
    return ExtendedInventory("EMPTY_DEFERRED", (), reason)


def _string_tuple(value: object) -> Tuple[str, ...]:
    if not isinstance(value, list) or not all(isinstance(item, str) and item for item in value):
        raise ValueError("RELEASE_MANIFEST_INVALID")
    return tuple(value)
