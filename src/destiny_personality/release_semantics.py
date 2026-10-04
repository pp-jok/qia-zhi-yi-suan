"""Formal release resolution bound to governed package-owned assets."""

from typing import Dict, Iterable, Optional, Tuple, Union

from .core_profile_models import CrossSystemAlignment, PrimitiveCandidate, PrimitiveState
from .release_manifest import CORE_PRIMITIVE_IDS, ReleaseManifest
from .release_mapping_bundle import (
    ActiveReleaseMappingBundle,
    require_active_release_mapping_bundle,
)


_RESOLVER_REF = "release-state-resolver-v1"
_DIRECTIONS = {
    "high": "supported_high",
    "low": "supported_low",
    "supported_high": "supported_high",
    "supported_low": "supported_low",
}


def resolve_release_primitive_states(
    bundle: ActiveReleaseMappingBundle, manifest: ReleaseManifest
) -> Dict[str, PrimitiveState]:
    """Resolve the exact v0.4.0 bundle; caller-supplied mappings are forbidden."""

    admitted = release_mapping_candidates(bundle, manifest)
    if admitted:
        raise ValueError("RELEASE_MAPPING_BUNDLE_INVALID")
    return {
        primitive_id: _unknown_state(primitive_id, manifest)
        for primitive_id in sorted(CORE_PRIMITIVE_IDS)
    }


def release_mapping_candidates(
    bundle: ActiveReleaseMappingBundle, manifest: ReleaseManifest
) -> Tuple[PrimitiveCandidate, ...]:
    """Return the governed active candidates; v0.4.0 deliberately has none."""

    governed = require_active_release_mapping_bundle(bundle)
    if set(manifest.core_primitives) != set(CORE_PRIMITIVE_IDS):
        raise ValueError("RELEASE_MANIFEST_INVALID")
    if governed.mappings:
        raise ValueError("RELEASE_MAPPING_BUNDLE_INVALID")
    return ()


def align_release_states(
    bazi_state: Optional[Union[PrimitiveCandidate, PrimitiveState]],
    astrology_state: Optional[Union[PrimitiveCandidate, PrimitiveState]],
    *,
    primitive_id: Optional[str] = None,
) -> CrossSystemAlignment:
    """Compatibility wrapper for one candidate per system."""

    bazi = _as_candidate(bazi_state, "bazi")
    astrology = _as_candidate(astrology_state, "astrology")
    resolved = primitive_id or _primitive_id_of(bazi, astrology)
    return align_release_candidate_sets(
        () if bazi is None else (bazi,),
        () if astrology is None else (astrology,),
        primitive_id=resolved,
    )


def align_release_candidate_sets(
    bazi_candidates: Iterable[PrimitiveCandidate],
    astrology_candidates: Iterable[PrimitiveCandidate],
    *,
    primitive_id: str,
) -> CrossSystemAlignment:
    """Aggregate both systems so an internal contradiction cannot be hidden."""

    bazi = tuple(item for item in bazi_candidates if _has_approved_evidence(item))
    astrology = tuple(
        item for item in astrology_candidates if _has_approved_evidence(item)
    )
    bazi_directions = {_direction(item.direction) for item in bazi}
    astrology_directions = {_direction(item.direction) for item in astrology}
    bazi_refs = tuple(sorted({ref for item in bazi for ref in item.semantic_rule_refs}))
    astrology_refs = tuple(
        sorted({ref for item in astrology for ref in item.semantic_rule_refs})
    )
    if not bazi or not astrology:
        status, relation = "non_comparable", "insufficient_approved_evidence"
        bazi_refs, astrology_refs = (), ()
    elif len(bazi_directions) != 1 or len(astrology_directions) != 1:
        status, relation = "unresolved", "internal_contradiction"
    elif bazi_directions == astrology_directions:
        status, relation = "validation", "agreement"
    else:
        status, relation = "unresolved", "opposed"
    contexts = tuple(
        sorted(
            {
                context
                for item in bazi + astrology
                for context in item.contexts
            }
        )
    )
    return CrossSystemAlignment(
        alignment_id="{}:{}:{}:{}".format(
            primitive_id, relation, "|".join(bazi_refs), "|".join(astrology_refs)
        ),
        primitive_id=primitive_id,
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


def _unknown_state(primitive_id: str, manifest: ReleaseManifest) -> PrimitiveState:
    closure = manifest.core_primitives[primitive_id]
    return PrimitiveState(
        primitive_id=primitive_id,
        state="unknown",
        evidence_refs=(),
        resolution_rule_ref=_RESOLVER_REF + ":governed-empty-bundle",
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


def _as_candidate(
    value: Optional[Union[PrimitiveCandidate, PrimitiveState]], source_system: str
) -> Optional[PrimitiveCandidate]:
    if value is None or isinstance(value, PrimitiveCandidate):
        return value
    if not isinstance(value, PrimitiveState) or value.state not in {
        "supported_high",
        "supported_low",
    }:
        return None
    return PrimitiveCandidate(
        primitive_id=value.primitive_id,
        source_system=source_system,
        direction=value.state,
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


def _has_approved_evidence(candidate: PrimitiveCandidate) -> bool:
    return bool(
        candidate.source_system in {"bazi", "astrology"}
        and _direction(candidate.direction) in {"supported_high", "supported_low"}
        and candidate.fact_refs
        and candidate.semantic_rule_refs
        and not any(
            marker in ref.lower()
            for ref in candidate.semantic_rule_refs
            for marker in ("candidate", "legacy", "core-profile-v1")
        )
    )


def _direction(value: str) -> str:
    return _DIRECTIONS.get(value, value)


def _primitive_id_of(
    bazi: Optional[PrimitiveCandidate], astrology: Optional[PrimitiveCandidate]
) -> str:
    if bazi is not None:
        return bazi.primitive_id
    if astrology is not None:
        return astrology.primitive_id
    return "unknown"
