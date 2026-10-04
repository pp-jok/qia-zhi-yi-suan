"""Builder for the formal, limited-coverage Core Destiny Profile."""

from hashlib import sha256
from typing import Iterable, Optional

from .core_profile_models import CoreDestinyProfile, PrimitiveCandidate
from .deterministic_facts_codec import deterministic_facts_fingerprint
from .release_manifest import ReleaseManifest, load_release_manifest
from .release_semantics import align_release_states, release_mapping_candidates, resolve_release_primitive_states


_SEMANTIC_ASSURANCE_UNKNOWN_ONLY = "limited_coverage_unknown_only"
_SEMANTIC_ASSURANCE_MAPPED = "limited_coverage_approved_mapping"


def build_core_destiny_profile(
    facts: object,
    *,
    fact_assurance: str,
    approved_mappings: Iterable[object] = (),
    manifest: Optional[ReleaseManifest] = None,
) -> CoreDestinyProfile:
    """Build a formal profile from facts and explicitly approved active mappings only.

    The default release asset has no approved mappings.  That is a valid result:
    the profile remains complete, carries six ``unknown`` primitive states, and
    records its semantic limitation instead of inventing a conclusion.
    """

    if fact_assurance not in {"none", "capability_reported", "project_verified"}:
        raise ValueError("FACT_ASSURANCE_INVALID")
    release_manifest = manifest or load_release_manifest()
    mapping_items = tuple(approved_mappings)
    candidates = release_mapping_candidates(mapping_items, release_manifest)
    primitive_states = resolve_release_primitive_states(mapping_items, release_manifest)
    bazi_candidates = tuple(
        candidate for candidate in candidates if candidate.source_system == "bazi"
    )
    astrology_candidates = tuple(
        candidate for candidate in candidates if candidate.source_system == "astrology"
    )
    alignments = tuple(
        align_release_states(
            _first_for_primitive(bazi_candidates, primitive_id),
            _first_for_primitive(astrology_candidates, primitive_id),
            primitive_id=primitive_id,
        )
        for primitive_id in sorted(release_manifest.core_primitives)
    )
    fact_fingerprint = deterministic_facts_fingerprint(facts)
    semantic_assurance = (
        _SEMANTIC_ASSURANCE_MAPPED if candidates else _SEMANTIC_ASSURANCE_UNKNOWN_ONLY
    )
    profile_id_input = "{}:{}:{}".format(
        fact_fingerprint,
        release_manifest.release_id,
        "|".join(_candidate_identifier(candidate) for candidate in candidates),
    )
    limitations = [
        "formal semantic coverage is limited to approved active mappings",
        "candidate and legacy mapping registries are excluded from this profile",
        "unknown primitive states are not interpreted as low",
    ]
    if not candidates:
        limitations.append("no approved active mappings are available in this release")
    if fact_assurance == "none":
        limitations.append("fact assurance is none; semantic conclusions remain unavailable")
    unresolved_questions = tuple(
        "{}: no approved active mapping resolves this primitive".format(primitive_id)
        for primitive_id, state in sorted(primitive_states.items())
        if state.state == "unknown"
    )
    return CoreDestinyProfile(
        schema_version="core-destiny-profile-v1",
        core_profile_id="cdp-" + sha256(profile_id_input.encode("utf-8")).hexdigest()[:16],
        fact_packet_refs=("deterministic-facts:" + fact_fingerprint,),
        fact_assurance=fact_assurance,
        semantic_model_assurance=semantic_assurance,
        semantic_model_versions=(
            ("release_manifest", release_manifest.schema_version),
            ("release_semantics", "release-semantics-v1"),
        ),
        bazi_primitive_candidates=bazi_candidates,
        astrology_primitive_candidates=astrology_candidates,
        primitive_states=primitive_states,
        cross_system_alignment=alignments,
        dominant_signatures=(),
        core_dynamics=(),
        shadow_mature_forms=(),
        fate_themes=(),
        archetype=None,
        contradictions=tuple(
            sorted(
                {
                    contradiction
                    for state in primitive_states.values()
                    for contradiction in state.contradictions
                }
            )
        ),
        limitations=tuple(limitations),
        unresolved_questions=unresolved_questions,
        audit_trail=(
            "release_manifest:" + release_manifest.release_id,
            "release_manifest_schema:" + release_manifest.schema_version,
            "fact_fingerprint:" + fact_fingerprint,
            "approved_active_mapping_count:" + str(len(candidates)),
            "formal_resolver:release-semantics-v1",
        ),
    )


def _first_for_primitive(
    candidates: Iterable[PrimitiveCandidate], primitive_id: str
) -> Optional[PrimitiveCandidate]:
    return next(
        (candidate for candidate in candidates if candidate.primitive_id == primitive_id),
        None,
    )


def _candidate_identifier(candidate: PrimitiveCandidate) -> str:
    return "|".join(candidate.semantic_rule_refs)
