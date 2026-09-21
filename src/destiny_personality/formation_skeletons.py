"""Typed disabled boundaries for future formation layers.

These interfaces deliberately carry no formation rules or semantic output.
"""

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class DominantSignature:
    signature_id: str
    primitive_refs: Tuple[str, ...]
    source_system_refs: Tuple[str, ...]
    salience: str
    stability: str
    contexts: Tuple[str, ...]
    counterevidence_refs: Tuple[str, ...]
    limitations: Tuple[str, ...]


@dataclass(frozen=True)
class CoreDynamic:
    dynamic_id: str
    primitive_refs: Tuple[str, ...]
    relation_rule_refs: Tuple[str, ...]
    contexts: Tuple[str, ...]
    limitations: Tuple[str, ...]


@dataclass(frozen=True)
class DisabledSignatureResult:
    profile_ref: str
    mode: str
    signatures: Tuple[DominantSignature, ...]
    audit_refs: Tuple[str, ...]


@dataclass(frozen=True)
class DisabledDynamicResult:
    profile_ref: str
    mode: str
    dynamics: Tuple[CoreDynamic, ...]
    audit_refs: Tuple[str, ...]


def build_disabled_signature_result(profile_ref: str) -> DisabledSignatureResult:
    return DisabledSignatureResult(profile_ref, "disabled", (), ("signature_formation_rules_unapproved",))


def build_disabled_dynamic_result(profile_ref: str) -> DisabledDynamicResult:
    return DisabledDynamicResult(profile_ref, "disabled", (), ("dynamic_relation_rules_unapproved",))
