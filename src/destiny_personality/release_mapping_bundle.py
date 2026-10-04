"""Strict loader for the governed active release Mapping bundle."""

from dataclasses import dataclass
from hashlib import sha256
import json
from pathlib import Path
from typing import Mapping, Optional, Tuple

import yaml


SCHEMA_VERSION = "active-release-mapping-bundle-v1"
BUNDLE_ID = "ACTIVE-RELEASE-MAPPING-BUNDLE-V1"
DECISION_REF = "docs/governance/decisions/auto-release-mapping-bundle-v1.md"


@dataclass(frozen=True)
class ActiveReleaseMappingBundle:
    schema_version: str
    bundle_id: str
    activation_status: str
    mappings: Tuple[Mapping[str, object], ...]
    asset_fingerprint: str
    decision_ref: str
    limitations: Tuple[str, ...]


def active_release_mapping_bundle_path() -> Path:
    return (
        Path(__file__).resolve().parent
        / "release_assets"
        / "v1"
        / "active_mapping_bundle_v1.yaml"
    )


def mapping_payload_fingerprint(mappings: object) -> str:
    canonical = json.dumps(
        mappings, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return sha256(canonical).hexdigest()


def load_active_release_mapping_bundle(
    path: Optional[Path] = None,
) -> ActiveReleaseMappingBundle:
    bundle_path = Path(path) if path is not None else active_release_mapping_bundle_path()
    try:
        payload = yaml.safe_load(bundle_path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as error:
        raise ValueError("RELEASE_MAPPING_BUNDLE_INVALID") from error
    if not isinstance(payload, dict) or set(payload) != {
        "schema_version",
        "bundle_id",
        "activation_status",
        "mapping_count",
        "mappings",
        "asset_fingerprint",
        "decision",
        "limitations",
    }:
        raise ValueError("RELEASE_MAPPING_BUNDLE_INVALID")
    mappings = payload["mappings"]
    decision = payload["decision"]
    limitations = payload["limitations"]
    if (
        payload["schema_version"] != SCHEMA_VERSION
        or payload["bundle_id"] != BUNDLE_ID
        or payload["activation_status"] != "active"
        or not isinstance(mappings, list)
        or mappings
        or payload["mapping_count"] != 0
        or payload["asset_fingerprint"] != mapping_payload_fingerprint(mappings)
        or decision
        != {
            "authority": "delegated_autonomous_executor",
            "mode": "AUTONOMOUS_COMPLETION",
            "outcome": "CLOSE_ZERO",
            "ref": DECISION_REF,
        }
        or not isinstance(limitations, list)
        or not limitations
        or not all(isinstance(item, str) and item for item in limitations)
    ):
        raise ValueError("RELEASE_MAPPING_BUNDLE_INVALID")
    return ActiveReleaseMappingBundle(
        schema_version=SCHEMA_VERSION,
        bundle_id=BUNDLE_ID,
        activation_status="active",
        mappings=(),
        asset_fingerprint=payload["asset_fingerprint"],
        decision_ref=DECISION_REF,
        limitations=tuple(limitations),
    )


def require_active_release_mapping_bundle(
    value: object,
) -> ActiveReleaseMappingBundle:
    expected = load_active_release_mapping_bundle()
    if not isinstance(value, ActiveReleaseMappingBundle) or value != expected:
        raise ValueError("RELEASE_MAPPING_BUNDLE_INVALID")
    return value
