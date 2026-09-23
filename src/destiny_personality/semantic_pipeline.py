"""Pure, policy-driven Semantic Core formation for approved Mapping inputs."""

from hashlib import sha256
import json
from typing import Iterable, Mapping


def build_semantic_core_from_approved_mapping(
    profile_ref: str, approved_mappings: Iterable[Mapping[str, object]], policies: Mapping[str, Mapping[str, object]]
) -> dict:
    mappings = tuple(_freeze(dict(item)) for item in approved_mappings)
    if not mappings:
        return _blocked_core(profile_ref)
    primitives = tuple(
        {
            "primitive_id": item["primitive_id"],
            "state": item["proposed_direction"].get("state", "unknown"),
            "mapping_refs": (item["mapping_candidate_id"],),
            "mechanism_refs": tuple(item.get("semantic_mechanism_refs", ())),
            "evidence_root_refs": tuple(item.get("evidence_root_refs", ())),
            "fact_refs": tuple(item.get("canonical_fact_requirements", ())),
        }
        for item in mappings
    )
    signatures = _form("signature", policies.get("signature", {}), primitives, "required_primitive_ids", "primitive_id", "signature_id")
    dynamics = _form("dynamic", policies.get("dynamic", {}), signatures, "required_signature_ids", "signature_id", "dynamic_id")
    themes = _form("theme", policies.get("theme", {}), dynamics, "required_dynamic_ids", "dynamic_id", "theme_id")
    archetypes = _form("archetype", policies.get("archetype", {}), themes, "required_theme_ids", "theme_id", "archetype_id")
    statuses = {
        "mapping": "available", "primitive_v2": "available",
        "signature": "available" if signatures else "blocked_by_gate",
        "dynamic": "available" if dynamics else "blocked_by_gate",
        "theme": "available" if themes else "blocked_by_gate",
        "archetype": "available" if archetypes else "blocked_by_gate",
    }
    return {
        "profile_ref": profile_ref, "mapping_candidates": mappings, "primitive_states": primitives,
        "signatures": signatures, "dynamics": dynamics, "shadow_mature_forms": tuple(
            {"dynamic_id": item["dynamic_id"], "shadow_form": item.get("shadow_form"), "mature_form": item.get("mature_form")} for item in dynamics
        ), "fate_themes": themes, "archetype": archetypes[0] if archetypes else None,
        "stage_statuses": statuses, "limitations": (), "audit_trail": ("policy_driven",),
    }


def _form(stage: str, policy: Mapping[str, object], sources: tuple, required_key: str, source_id_key: str, output_id_key: str) -> tuple:
    rules = policy.get("rules", ()) if isinstance(policy, Mapping) else ()
    source_ids = {item.get(source_id_key) for item in sources}
    result = []
    for rule in rules if isinstance(rules, list) else ():
        required = rule.get(required_key, ()) if isinstance(rule, Mapping) else ()
        if rule.get(output_id_key) and isinstance(required, list) and set(required).issubset(source_ids):
            result.append({output_id_key: rule[output_id_key], "source_refs": tuple(required), "formation_rule_ref": rule.get("formation_rule_ref", f"{stage}:{rule[output_id_key]}")})
    return tuple(result)


def _blocked_core(profile_ref: str) -> dict:
    return {"profile_ref": profile_ref, "mapping_candidates": (), "primitive_states": (), "signatures": (), "dynamics": (), "shadow_mature_forms": (), "fate_themes": (), "archetype": None, "stage_statuses": {stage: "blocked_by_gate" for stage in ("mapping", "primitive_v2", "signature", "dynamic", "theme", "archetype")}, "limitations": ("APPROVED_MAPPING_REQUIRED",), "audit_trail": ()}


def _freeze(value: object) -> object:
    if isinstance(value, list):
        return tuple(_freeze(item) for item in value)
    if isinstance(value, dict):
        return {key: _freeze(item) for key, item in value.items()}
    return value


def explain_semantic_item(core: Mapping[str, object], item_ref: str) -> dict:
    """Read an existing core item only; explanation never performs inference."""
    item_type, _, item_id = item_ref.partition(":")
    collections = {"signature": core.get("signatures", ()), "dynamic": core.get("dynamics", ()), "theme": core.get("fate_themes", ())}
    id_keys = {"signature": "signature_id", "dynamic": "dynamic_id", "theme": "theme_id"}
    for item in collections.get(item_type, ()):
        if item.get(id_keys[item_type]) == item_id:
            return {"status": "available", "item_id": item_ref, "item_type": item_type, "profile_ref": core["profile_ref"], "source_refs": tuple(item.get("source_refs", ())), "formation_rule_refs": (item.get("formation_rule_ref"),), "limitations": tuple(core.get("limitations", ()))}
    return {"status": "not_found", "item_id": item_ref, "profile_ref": core["profile_ref"], "limitations": tuple(core.get("limitations", ()))}


def diff_semantic_cores(left: Mapping[str, object], right: Mapping[str, object]) -> tuple:
    checks = (("mapping_change", "mapping_candidates"), ("primitive_state_change", "primitive_states"), ("signature_change", "signatures"), ("dynamic_change", "dynamics"), ("theme_change", "fate_themes"), ("archetype_change", "archetype"), ("stage_status_change", "stage_statuses"))
    return tuple(label for label, key in checks if left.get(key) != right.get(key))


def build_semantic_report(core: Mapping[str, object], renderer_profile: str) -> dict:
    """Create a structured report whose sections carry only stored Core refs."""
    if renderer_profile not in {"concise-portrait-v1", "standard-portrait-v1", "dynamic-long-form-v1"}:
        raise ValueError("SEMANTIC_REPORT_PROFILE_INVALID")
    sections = []
    for section_id, collection_key in (("signatures", "signatures"), ("dynamics", "dynamics"), ("fate_themes", "fate_themes")):
        items = tuple(core.get(collection_key, ()))
        if items:
            sections.append({"section_id": section_id, "title": section_id.replace("_", " ").title(), "body": "", "source_refs": tuple(item.get("source_refs", ()) for item in items), "limitations": tuple(core.get("limitations", ()))})
    return {"profile_ref": core["profile_ref"], "renderer_profile": renderer_profile, "sections": tuple(sections), "containment_status": "core_refs_only"}


def semantic_pipeline_fingerprint(formation_policy_versions: Mapping[str, str]) -> str:
    """Fingerprint candidate formation versions independently of active assets."""
    canonical = json.dumps(dict(sorted(formation_policy_versions.items())), separators=(",", ":"), sort_keys=True).encode("utf-8")
    return sha256(canonical).hexdigest()
