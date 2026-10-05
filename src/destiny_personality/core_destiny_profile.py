"""Builder for the formal, limited-coverage Core Destiny Profile."""

from hashlib import sha256
from .core_profile_models import CoreDestinyProfile, PrimitiveCandidate
from .deterministic_facts_codec import QualifiedFacts, require_qualified_facts
from .release_manifest import load_release_manifest
from .release_mapping_bundle import load_active_release_mapping_bundle
from .release_semantics import align_release_candidate_sets, release_mapping_candidates, resolve_release_primitive_states


_SEMANTIC_ASSURANCE_UNKNOWN_ONLY = "limited_coverage_unknown_only"


def build_core_destiny_profile(
    qualified_facts: QualifiedFacts,
) -> CoreDestinyProfile:
    """Build from loader-produced qualified facts and the governed release bundle.

    The v0.4.x release asset has no approved mappings.  That is a valid result:
    the profile remains complete, carries six ``unknown`` primitive states, and
    records its semantic limitation instead of inventing a conclusion.
    """

    qualified = require_qualified_facts(qualified_facts)
    facts = qualified.facts
    fact_assurance = qualified.fact_assurance
    release_manifest = load_release_manifest()
    mapping_bundle = load_active_release_mapping_bundle()
    candidates = release_mapping_candidates(mapping_bundle, release_manifest)
    primitive_states = resolve_release_primitive_states(mapping_bundle, release_manifest)
    bazi_candidates = tuple(
        candidate for candidate in candidates if candidate.source_system == "bazi"
    )
    astrology_candidates = tuple(
        candidate for candidate in candidates if candidate.source_system == "astrology"
    )
    alignments = tuple(
        align_release_candidate_sets(
            tuple(item for item in bazi_candidates if item.primitive_id == primitive_id),
            tuple(item for item in astrology_candidates if item.primitive_id == primitive_id),
            primitive_id=primitive_id,
        )
        for primitive_id in sorted(release_manifest.core_primitives)
    )
    fact_fingerprint = qualified.fact_fingerprint
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
        semantic_model_assurance=_SEMANTIC_ASSURANCE_UNKNOWN_ONLY,
        semantic_model_versions=(
            ("release_manifest", release_manifest.schema_version),
            ("active_mapping_bundle", mapping_bundle.asset_fingerprint),
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
            "active_mapping_bundle:" + mapping_bundle.bundle_id,
            "active_mapping_bundle_fingerprint:" + mapping_bundle.asset_fingerprint,
            "fact_fingerprint:" + fact_fingerprint,
            "qualification_fingerprint:" + qualified.qualification_fingerprint,
            "approved_active_mapping_count:" + str(len(candidates)),
            "formal_resolver:release-semantics-v1",
        ),
    )


def _candidate_identifier(candidate: PrimitiveCandidate) -> str:
    return "|".join(candidate.semantic_rule_refs)
