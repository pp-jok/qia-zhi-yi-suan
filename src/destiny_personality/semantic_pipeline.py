"""Pure, policy-driven Semantic Core formation for approved Mapping inputs."""

from hashlib import sha256
import json
from pathlib import Path
from typing import Iterable, Mapping

import yaml


def build_semantic_core_from_approved_mapping(
    profile_ref: str, approved_mappings: Iterable[Mapping[str, object]], policies: Mapping[str, Mapping[str, object]]
) -> dict:
    mappings = tuple(_freeze(dict(item)) for item in approved_mappings)
    if not mappings:
        return _blocked_core(profile_ref)
    primitives = resolve_primitive_states(mappings, policies.get("primitive_v2", {}))
    signatures = _form("signature", policies.get("signature", {}), primitives, "required_primitive_ids", "primitive_id", "signature_id")
    dynamics = _form("dynamic", policies.get("dynamic", {}), signatures, "required_signature_ids", "signature_id", "dynamic_id")
    themes = _form("theme", policies.get("theme", {}), dynamics, "required_dynamic_ids", "dynamic_id", "theme_id")
    archetypes = _form("archetype", policies.get("archetype", {}), themes, "required_theme_ids", "theme_id", "archetype_id")
    statuses = {
        "mapping": "available", "primitive_v2": "available",
        "signature": _stage_status("signature" in policies, signatures),
        "dynamic": _stage_status("dynamic" in policies, dynamics),
        "theme": _stage_status("theme" in policies, themes),
        "archetype": _stage_status("archetype" in policies, archetypes),
    }
    core = {
        "profile_ref": profile_ref, "mapping_candidates": mappings, "primitive_states": primitives,
        "signatures": signatures, "dynamics": dynamics, "shadow_mature_forms": tuple(
            {"dynamic_id": item["dynamic_id"], "shadow_form": item.get("shadow_form"), "mature_form": item.get("mature_form")} for item in dynamics
        ), "fate_themes": themes, "archetype": archetypes[0] if archetypes else None,
        "stage_statuses": statuses, "limitations": (), "audit_trail": ("policy_driven",),
    }
    core["provenance"] = build_semantic_provenance(core)
    return core


def load_enabled_formation_policies(project_root: Path) -> tuple[dict, dict]:
    """Load only explicitly enabled reviewed formation policies from this repository."""
    root = Path(project_root) / "candidates" / "core-profile-v1"
    specs = {
        "signature": "signature_formation_policy_v1.yaml",
        "dynamic": "dynamic_formation_policy_v1.yaml",
        "theme": "derived_theme_policy_v1.yaml",
    }
    policies = {}
    versions = {}
    for stage, filename in specs.items():
        path = root / filename
        if not path.is_file():
            continue
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            continue
        if payload.get("review_status") == "approved" and payload.get("mode") == "enabled":
            policies[stage] = payload
            versions[stage] = str(payload.get("policy_version", "unversioned"))
    return policies, versions


def _form(stage: str, policy: Mapping[str, object], sources: tuple, required_key: str, source_id_key: str, output_id_key: str) -> tuple:
    rules = policy.get("rules", ()) if isinstance(policy, Mapping) else ()
    source_ids = {item.get(source_id_key) for item in sources}
    result = []
    for rule in rules if isinstance(rules, list) else ():
        required = rule.get(required_key, ()) if isinstance(rule, Mapping) else ()
        if rule.get(output_id_key) and isinstance(required, list) and set(required).issubset(source_ids):
            formed = {output_id_key: rule[output_id_key], "source_refs": tuple(required), "formation_rule_ref": rule.get("formation_rule_ref", f"{stage}:{rule[output_id_key]}")}
            for field in ("shadow_form", "mature_form", "contexts", "limitations"):
                if field in rule:
                    formed[field] = _freeze(rule[field])
            result.append(formed)
    return tuple(result)


def _stage_status(policy_present: bool, output: tuple) -> str:
    if not policy_present:
        return "blocked_by_gate"
    return "available" if output else "available_zero"


def _blocked_core(profile_ref: str) -> dict:
    return {"profile_ref": profile_ref, "mapping_candidates": (), "primitive_states": (), "signatures": (), "dynamics": (), "shadow_mature_forms": (), "fate_themes": (), "archetype": None, "stage_statuses": {stage: "blocked_by_gate" for stage in ("mapping", "primitive_v2", "signature", "dynamic", "theme", "archetype")}, "limitations": ("APPROVED_MAPPING_REQUIRED",), "audit_trail": ()}


def build_semantic_provenance(core: Mapping[str, object]) -> dict:
    """Build immutable stored lineage; consumers read this rather than infer anew."""
    nodes, edges = set(), set()
    for mapping in core.get("mapping_candidates", ()):
        mapping_ref = "mapping:" + str(mapping["mapping_candidate_id"])
        primitive_ref = "primitive:" + str(mapping["primitive_id"])
        nodes.update((mapping_ref, primitive_ref)); edges.add((primitive_ref, "derived_from", mapping_ref))
        for field, kind in (("semantic_mechanism_refs", "semantic_mechanism"), ("evidence_root_refs", "evidence_root"), ("canonical_fact_requirements", "fact")):
            for ref in mapping.get(field, ()):
                child = kind + ":" + str(ref); nodes.add(child); edges.add((mapping_ref, "supported_by", child))
        for link in mapping.get("provenance_links", ()):
            if not isinstance(link, Mapping):
                continue
            left, relation, right = link.get("from"), link.get("relation"), link.get("to")
            if all(isinstance(value, str) and value for value in (left, relation, right)):
                nodes.update((left, right)); edges.add((left, relation, right))
    for collection, prefix, source_prefix in (("signatures", "signature", "primitive"), ("dynamics", "dynamic", "signature"), ("fate_themes", "theme", "dynamic")):
        for item in core.get(collection, ()):
            identifier = item.get(prefix + "_id") or item.get("theme_id")
            if identifier:
                node = prefix + ":" + str(identifier); nodes.add(node)
                for ref in item.get("source_refs", ()):
                    edges.add((node, "formed_from", source_prefix + ":" + str(ref)))
    for item in core.get("shadow_mature_forms", ()):
        if not isinstance(item, Mapping) or not item.get("dynamic_id"):
            continue
        dynamic_ref = "dynamic:" + str(item["dynamic_id"])
        for form_kind in ("shadow", "mature"):
            if item.get(form_kind + "_form"):
                node = "shadow_mature:" + str(item["dynamic_id"]) + ":" + form_kind
                nodes.update((node, dynamic_ref)); edges.add((node, "formed_from", dynamic_ref))
    archetype = core.get("archetype")
    if isinstance(archetype, Mapping) and archetype.get("archetype_id"):
        node = "archetype:" + str(archetype["archetype_id"]); nodes.add(node)
        for ref in archetype.get("source_refs", ()):
            edges.add((node, "formed_from", "theme:" + str(ref)))
    return {"nodes": tuple(sorted(nodes)), "edges": tuple(sorted(edges))}


def explain_semantic_pipeline_item(core: Mapping[str, object], item_ref: str) -> dict:
    """Return persisted lineage for one item without invoking semantic formation."""
    graph = core.get("provenance", {})
    if not isinstance(graph, Mapping):
        return {"status": "not_found", "item_id": item_ref, "provenance_nodes": (), "provenance_edges": ()}
    edges = tuple(graph.get("edges", ()))
    if item_ref not in set(graph.get("nodes", ())):
        return {"status": "not_found", "item_id": item_ref, "provenance_nodes": (), "provenance_edges": ()}
    seen, frontier = {item_ref}, [item_ref]
    selected = []
    while frontier:
        current = frontier.pop()
        for left, relation, right in edges:
            if left == current and right not in seen:
                seen.add(right); frontier.append(right); selected.append((left, relation, right))
    return {"status": "available", "item_id": item_ref, "provenance_nodes": tuple(sorted(seen)), "provenance_edges": tuple(sorted(selected)), "limitations": tuple(core.get("limitations", ()))}


def semantic_pipeline_source_view(core: Mapping[str, object], stage: str) -> dict:
    prefixes = {"mapping": "mapping", "primitive": "primitive", "signature": "signature", "dynamic": "dynamic", "shadow_mature": "shadow_mature", "theme": "theme", "archetype": "archetype"}
    if stage not in prefixes:
        raise ValueError("SEMANTIC_CORE_SOURCE_STAGE_INVALID")
    prefix = prefixes[stage] + ":"
    graph = core.get("provenance", {})
    nodes = tuple(node for node in graph.get("nodes", ()) if node.startswith(prefix)) if isinstance(graph, Mapping) else ()
    status_key = "primitive_v2" if stage == "primitive" else ("dynamic" if stage == "shadow_mature" else stage)
    return {"profile_ref": core["profile_ref"], "stage": stage, "status": core.get("stage_statuses", {}).get(status_key, "blocked_by_gate"), "item_count": len(nodes), "provenance_nodes": nodes, "containment_status": "persisted_provenance_only"}


def resolve_primitive_states(mappings: Iterable[Mapping[str, object]], policy: Mapping[str, object]) -> tuple:
    """Aggregate multiple Mapping records into one explicit state per Primitive."""
    grouped = {}
    for mapping in mappings:
        if mapping.get("exclusion_matched") is True:
            continue
        grouped.setdefault(mapping["primitive_id"], []).append(mapping)
    results = []
    for primitive_id, items in sorted(grouped.items()):
        states = {item.get("proposed_direction", {}).get("state", "unknown") for item in items}
        context_states = _context_states(items)
        state = "context_differentiated" if len(set(context_states.values())) > 1 else _resolve_state(states, policy)
        result = {"primitive_id": primitive_id, "state": state, "mapping_refs": tuple(item["mapping_candidate_id"] for item in items)}
        if context_states:
            result["context_states"] = context_states
        if any("semantic_mechanism_refs" in item for item in items):
            result["mechanism_refs"] = tuple(ref for item in items for ref in item.get("semantic_mechanism_refs", ()))
            result["evidence_root_refs"] = tuple(ref for item in items for ref in item.get("evidence_root_refs", ()))
            result["fact_refs"] = tuple(ref for item in items for ref in item.get("canonical_fact_requirements", ()))
        for field, output_field in (("modifiers", "modifier_refs"), ("contextualizers", "contextualizer_refs"), ("counterevidence", "counterevidence_refs")):
            refs = tuple(ref for item in items for ref in item.get(field, ()) if isinstance(ref, str) and ref)
            if refs:
                result[output_field] = refs
        if any(field in item for item in items for field in ("modifiers", "contextualizers", "counterevidence", "exclusions")):
            result["qualifier_resolution_mode"] = "stored_but_not_resolved"
        results.append(result)
    return tuple(results)


def _context_states(items: list[Mapping[str, object]]) -> dict:
    grouped = {}
    for item in items:
        state = item.get("proposed_direction", {}).get("state", "unknown")
        contexts = item.get("contexts", ())
        for context in contexts if isinstance(contexts, (list, tuple)) else ():
            if isinstance(context, str) and context:
                grouped.setdefault(context, set()).add(state)
    return {context: _resolve_state(states, {}) for context, states in sorted(grouped.items())}


def _resolve_state(states: set, policy: Mapping[str, object]) -> str:
    conflict_state = policy.get("conflict_state", "mixed") if isinstance(policy, Mapping) else "mixed"
    known = {state for state in states if state != "unknown"}
    if not known:
        return "unknown"
    if len(known) > 1:
        return conflict_state
    return next(iter(known))


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


def diff_semantic_pipeline_cores(left: Mapping[str, object], right: Mapping[str, object]) -> tuple:
    checks = (
        ("mapping_change", "mapping_candidates"), ("primitive_state_change", "primitive_states"),
        ("signature_change", "signatures"), ("dynamic_change", "dynamics"),
        ("shadow_mature_change", "shadow_mature_forms"), ("theme_change", "fate_themes"),
        ("archetype_change", "archetype"), ("formation_policy_change", "formation_policy_fingerprint"),
        ("provenance_change", "provenance"), ("authority_change", "authority"),
        ("stage_status_change", "stage_statuses"),
    )
    context_changed = any(item.get("context_states") != other.get("context_states") for item, other in zip(left.get("primitive_states", ()), right.get("primitive_states", ())))
    labels = [label for label, key in checks if left.get(key) != right.get(key)]
    if context_changed and "context_state_change" not in labels:
        labels.insert(2, "context_state_change")
    return tuple(labels)


def build_semantic_report(core: Mapping[str, object], renderer_profile: str) -> dict:
    """Create a structured report whose sections carry only stored Core refs."""
    if renderer_profile not in {"concise-portrait-v1", "standard-portrait-v1", "dynamic-long-form-v1"}:
        raise ValueError("SEMANTIC_REPORT_PROFILE_INVALID")
    sections = []
    for section_id, collection_key in (("signatures", "signatures"), ("dynamics", "dynamics"), ("fate_themes", "fate_themes")):
        items = tuple(core.get(collection_key, ()))
        if items:
            rule_refs = tuple(str(item.get("formation_rule_ref", "unreferenced")) for item in items)
            sections.append({"section_id": section_id, "title": section_id.replace("_", " ").title(), "body": f"已形成 {len(items)} 项受控语义条目；来源规则：" + ", ".join(rule_refs), "source_refs": tuple(item.get("source_refs", ()) for item in items), "limitations": tuple(core.get("limitations", ()))})
    return {"profile_ref": core["profile_ref"], "renderer_profile": renderer_profile, "sections": tuple(sections), "containment_status": "core_refs_only"}


def semantic_pipeline_fingerprint(formation_policy_versions: Mapping[str, str]) -> str:
    """Fingerprint candidate formation versions independently of active assets."""
    canonical = json.dumps(dict(sorted(formation_policy_versions.items())), separators=(",", ":"), sort_keys=True).encode("utf-8")
    return sha256(canonical).hexdigest()
