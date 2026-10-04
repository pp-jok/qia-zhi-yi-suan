"""Formal, release-bounded primitive resolution.

This module intentionally has no dependency on candidate assets or candidate
mapping registries.  It accepts an already-approved active mapping bundle and
otherwise resolves the release manifest to explicit ``unknown`` states.
"""

from collections import defaultdict
from typing import Dict, Iterable, Mapping, Optional, Tuple, Union

from .core_profile_models import CrossSystemAlignment, PrimitiveCandidate, PrimitiveState
from .release_manifest import CORE_PRIMITIVE_IDS, ReleaseManifest


_RESOLVER_REF = "release-state-resolver-v1"
_DIRECTIONS = {
    "high": "supported_high",
    "low": "supported_low",
    "supported_high": "supported_high",
    "supported_low": "supported_low",
}


def resolve_release_primitive_states(
    mappings: Iterable[object], manifest: ReleaseManifest
) -> Dict[str, PrimitiveState]:
    """Resolve exactly the manifest's six primitives without coercing unknown to low."""

    candidates = release_mapping_candidates(mappings, manifest)
    by_primitive = defaultdict(list)
    for candidate in candidates:
        by_primitive[candidate.primitive_id].append(candidate)
    return {
        primitive_id: _resolve_primitive_state(
            primitive_id, tuple(by_primitive.get(primitive_id, ())), manifest
        )
        for primitive_id in sorted(CORE_PRIMITIVE_IDS)
    }


def release_mapping_candidates(
    mappings: Iterable[object], manifest: ReleaseManifest
) -> Tuple[PrimitiveCandidate, ...]:
    """Convert only approved active mapping records to formal candidates.

    Passing an empty iterable is the normal limited-coverage release path.
    Candidate/legacy identifiers are rejected here rather than being allowed to
    become a formal conclusion by accident.
    """

    result = []
    for item in mappings:
        candidate = _mapping_to_candidate(item)
        if candidate is None or candidate.primitive_id not in manifest.core_primitives:
            continue
        if _has_candidate_only_ref(candidate):
            continue
        result.append(candidate)
    return tuple(sorted(result, key=_candidate_key))


def align_release_states(
    bazi_state: Optional[Union[PrimitiveCandidate, PrimitiveState]],
    astrology_state: Optional[Union[PrimitiveCandidate, PrimitiveState]],
    *,
    primitive_id: Optional[str] = None,
) -> CrossSystemAlignment:
    """Describe cross-system evidence without adding any salience.

    An alignment is validation metadata, not a second vote.  It is therefore
    non-comparable whenever either system has no approved evidence and always
    carries a zero ``salience_delta``.
    """

    bazi = _as_candidate(bazi_state, "bazi")
    astrology = _as_candidate(astrology_state, "astrology")
    resolved_primitive_id = primitive_id or _primitive_id_of(bazi, astrology)
    bazi_has_evidence = _has_approved_evidence(bazi)
    astrology_has_evidence = _has_approved_evidence(astrology)
    if not bazi_has_evidence or not astrology_has_evidence:
        status, relation = "non_comparable", "insufficient_approved_evidence"
    elif bazi.direction == astrology.direction:
        status, relation = "validation", "agreement"
    else:
        status, relation = "unresolved", "opposed"
    contexts = tuple(sorted(set((bazi.contexts if bazi else ()) + (astrology.contexts if astrology else ()))))
    bazi_refs = bazi.semantic_rule_refs if bazi_has_evidence and bazi else ()
    astrology_refs = astrology.semantic_rule_refs if astrology_has_evidence and astrology else ()
    return CrossSystemAlignment(
        alignment_id="{}:{}:{}:{}".format(
            resolved_primitive_id, relation, "|".join(bazi_refs), "|".join(astrology_refs)
        ),
        primitive_id=resolved_primitive_id,
        context_refs=contexts,
        status=status,
        direction_relation=relation,
        bazi_rule_refs=bazi_refs,
        astrology_rule_refs=astrology_refs,
        limitations=(
            "cross-system alignment is validation metadata and does not increase salience",
        ),
        salience_delta=0,
    )


def _resolve_primitive_state(
    primitive_id: str, candidates: Tuple[PrimitiveCandidate, ...], manifest: ReleaseManifest
) -> PrimitiveState:
    closure = manifest.core_primitives[primitive_id]
    if not candidates:
        return PrimitiveState(
            primitive_id=primitive_id,
            state="unknown",
            evidence_refs=(),
            resolution_rule_ref=_RESOLVER_REF + ":no-active-approved-mapping",
            context_states={},
            supporting_candidates=(),
            counter_candidates=(),
            contradictions=(),
            unresolved_contexts=(),
            limitations=(
                "NO_ACTIVE_APPROVED_MAPPING",
                "manifest closure: " + closure.final_status,
                "unknown is not interpreted as low",
            ),
        )

    directions = {_direction(candidate.direction) for candidate in candidates}
    context_states = _context_states(candidates)
    global_candidates = tuple(candidate for candidate in candidates if _has_global_authority(candidate))
    global_directions = {_direction(candidate.direction) for candidate in global_candidates}
    promoted_direction = _promoted_context_direction(candidates, context_states)
    if len(global_directions) > 1:
        state = "mixed"
    elif len(global_directions) == 1:
        state = next(iter(global_directions))
    elif promoted_direction is not None:
        state = promoted_direction
    elif len(directions) > 1:
        state = "context_differentiated"
    else:
        state = "unknown"
    supporting = tuple(
        _candidate_ref(candidate)
        for candidate in candidates
        if _direction(candidate.direction) == "supported_high"
    )
    counter = tuple(
        _candidate_ref(candidate)
        for candidate in candidates
        if _direction(candidate.direction) == "supported_low"
    )
    contradictions = (
        ("approved directions conflict",) if len(directions) > 1 else ()
    )
    limitations = ["approved mapping evidence remains bounded by declared contexts"]
    if state == "unknown" and context_states:
        limitations.append("CONTEXT_EVIDENCE_NOT_PROMOTED")
    if state == "unknown":
        limitations.append("unknown is not interpreted as low")
    return PrimitiveState(
        primitive_id=primitive_id,
        state=state,
        evidence_refs=tuple(sorted({ref for candidate in candidates for ref in candidate.fact_refs})),
        resolution_rule_ref=_RESOLVER_REF + ":approved-active-mapping",
        context_states=context_states,
        supporting_candidates=supporting,
        counter_candidates=counter,
        contradictions=contradictions,
        unresolved_contexts=tuple(sorted(context_states)) if state in {"unknown", "context_differentiated"} else (),
        limitations=tuple(limitations),
    )


def _mapping_to_candidate(item: object) -> Optional[PrimitiveCandidate]:
    if isinstance(item, PrimitiveCandidate):
        return item
    if not isinstance(item, Mapping) or item.get("review_status") != "approved":
        return None
    primitive_id = item.get("primitive_id")
    source_system = item.get("source_system")
    direction = _mapping_direction(item.get("proposed_direction"))
    rule_refs = _strings(item.get("semantic_mechanism_refs"))
    fact_refs = _strings(item.get("canonical_fact_requirements"))
    roots = _strings(item.get("evidence_root_refs"))
    if (
        not isinstance(primitive_id, str)
        or source_system not in {"bazi", "astrology"}
        or direction is None
        or not rule_refs
        or not fact_refs
        or not roots
    ):
        return None
    modifiers = _strings(item.get("modifiers")) + tuple(
        "evidence_root:" + root for root in roots
    )
    if item.get("global_authority") is True or item.get("resolution_scope") == "global":
        modifiers += ("global_authority",)
    return PrimitiveCandidate(
        primitive_id=primitive_id,
        source_system=source_system,
        direction=direction,
        fact_refs=fact_refs,
        semantic_rule_refs=rule_refs,
        contexts=_strings(item.get("contexts")),
        salience=str(item.get("salience", "declared")),
        evidence_stability=str(item.get("evidence_stability", "approved_mapping")),
        modifier_refs=modifiers,
        counterevidence_refs=_strings(item.get("counterevidence")),
        expression_mode=str(item.get("expression_mode", "direct")),
        tension_level=str(item.get("tension_level", "low")),
        counterweight_effect=None,
        limitations=_strings(item.get("limitations")),
    )


def _mapping_direction(value: object) -> Optional[str]:
    if not isinstance(value, Mapping):
        return None
    raw = value.get("state", value.get("direction"))
    return _DIRECTIONS.get(raw) if isinstance(raw, str) else None


def _context_states(candidates: Tuple[PrimitiveCandidate, ...]) -> Dict[str, str]:
    result = {}
    for candidate in candidates:
        for context in candidate.contexts:
            prior = result.get(context)
            direction = _direction(candidate.direction)
            result[context] = direction if prior in {None, direction} else "mixed"
    return {key: result[key] for key in sorted(result)}


def _promoted_context_direction(
    candidates: Tuple[PrimitiveCandidate, ...], context_states: Mapping[str, str]
) -> Optional[str]:
    directions = set(context_states.values())
    if len(context_states) < 2 or len(directions) != 1 or "mixed" in directions:
        return None
    if any(candidate.counterevidence_refs for candidate in candidates):
        return None
    roots_by_context = {
        context: {
            root.removeprefix("evidence_root:")
            for candidate in candidates
            if context in candidate.contexts
            for root in candidate.modifier_refs
            if root.startswith("evidence_root:")
        }
        for context in context_states
    }
    root_sets = list(roots_by_context.values())
    if any(not refs for refs in root_sets) or any(
        left.intersection(right)
        for index, left in enumerate(root_sets)
        for right in root_sets[index + 1 :]
    ):
        return None
    return next(iter(directions))


def _has_global_authority(candidate: PrimitiveCandidate) -> bool:
    return "global_authority" in candidate.modifier_refs or "scope:global" in candidate.modifier_refs


def _as_candidate(
    value: Optional[Union[PrimitiveCandidate, PrimitiveState]], source_system: str
) -> Optional[PrimitiveCandidate]:
    if value is None or isinstance(value, PrimitiveCandidate):
        return value
    if not isinstance(value, PrimitiveState) or value.state not in {"supported_high", "supported_low"}:
        return None
    return PrimitiveCandidate(
        primitive_id=value.primitive_id,
        source_system=source_system,
        direction="high" if value.state == "supported_high" else "low",
        fact_refs=value.evidence_refs,
        semantic_rule_refs=value.supporting_candidates + value.counter_candidates,
        contexts=tuple(value.context_states),
        salience="declared",
        evidence_stability="resolved",
        modifier_refs=(),
        counterevidence_refs=(),
        expression_mode="direct",
        tension_level="low",
        counterweight_effect=None,
        limitations=value.limitations,
    )


def _has_approved_evidence(candidate: Optional[PrimitiveCandidate]) -> bool:
    return bool(
        candidate
        and candidate.source_system in {"bazi", "astrology"}
        and _direction(candidate.direction) in {"supported_high", "supported_low"}
        and candidate.fact_refs
        and candidate.semantic_rule_refs
        and not _has_candidate_only_ref(candidate)
    )


def _has_candidate_only_ref(candidate: PrimitiveCandidate) -> bool:
    return any(
        marker in ref.lower()
        for ref in candidate.semantic_rule_refs
        for marker in ("candidate", "legacy", "core-profile-v1")
    )


def _candidate_key(candidate: PrimitiveCandidate) -> Tuple[str, str, str, Tuple[str, ...]]:
    return (candidate.primitive_id, candidate.source_system, candidate.direction, candidate.semantic_rule_refs)


def _candidate_ref(candidate: PrimitiveCandidate) -> str:
    return "|".join(candidate.semantic_rule_refs)


def _direction(value: str) -> str:
    return _DIRECTIONS.get(value, value)


def _primitive_id_of(
    bazi: Optional[PrimitiveCandidate], astrology: Optional[PrimitiveCandidate]
) -> str:
    return bazi.primitive_id if bazi is not None else astrology.primitive_id if astrology is not None else "unknown"


def _strings(value: object) -> Tuple[str, ...]:
    if not isinstance(value, (list, tuple)):
        return ()
    return tuple(item for item in value if isinstance(item, str) and item)
