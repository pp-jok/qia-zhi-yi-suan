from dataclasses import asdict
from hashlib import sha256
from pathlib import Path
from typing import Dict, Iterable, Union

import yaml

from .calculation.models import DeterministicChartFacts
from .candidate_assets import candidate_asset_root
from .core_profile_models import (
    CandidateCoreProfile,
    CrossSystemAlignment,
    PrimitiveCandidate,
    PrimitiveState,
    StoppedCoreProfileExecution,
)
from .day_master_environment import derive_candidate_day_master_environment


_CANDIDATE_PRIMITIVES = (
    "P001",
    "P002",
    "P003",
    "P004",
    "P005",
    "P006",
)

_CANDIDATE_VERSIONS = (
    ("ontology", "c1-review-v1"),
    ("state_policy", "candidate-state-policy-v1"),
    ("bazi_mapping", "c2-review-v1"),
    ("astrology_mapping", "c2-review-v1"),
    ("alignment", "candidate-v2.3"),
    ("dynamic_formation", "c3-review-v1"),
    ("calibration_protocol", "c4a-review-v1"),
)


def candidate_semantic_bundle_fingerprint() -> str:
    """Fingerprint D1 semantic assets without creating a circular calibration hash."""

    digest = sha256()
    for path in sorted(_candidate_asset_root().glob("*.yaml")):
        if path.name == "core_profile_calibration_policy_v1.yaml":
            continue
        digest.update(path.name.encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def build_candidate_core_profile(
    facts: DeterministicChartFacts,
    *,
    fact_assurance: str,
) -> Union[CandidateCoreProfile, StoppedCoreProfileExecution]:
    fingerprint = _fact_fingerprint(facts)
    if fact_assurance == "none":
        return StoppedCoreProfileExecution(
            schema_version="core-profile-stopped-execution-v1",
            core_profile_id=f"candidate-stopped-{fingerprint[:16]}",
            fact_assurance=fact_assurance,
            failure_code="FACT_ASSURANCE_NONE",
            semantic_conclusions=(),
            limitations=(
                "fact_assurance=none stops candidate semantic inference",
            ),
        )
    if fact_assurance not in {"project_verified", "capability_reported"}:
        raise ValueError("unsupported fact_assurance")

    bazi_candidates = _extract_bazi_candidates(facts)
    astrology_candidates = _extract_astrology_candidates(facts)
    alignments = _align_cross_system(bazi_candidates, astrology_candidates)
    states: Dict[str, PrimitiveState] = {
        primitive_id: PrimitiveState(
            primitive_id=primitive_id,
            state="unknown",
            evidence_refs=(),
            resolution_rule_ref="candidate-state-policy-v1:no-mapped-evidence",
            context_states={},
            supporting_candidates=(),
            counter_candidates=(),
            contradictions=(),
            unresolved_contexts=(),
            limitations=("no candidate evidence matched",),
        )
        for primitive_id in _CANDIDATE_PRIMITIVES
    }
    for primitive_id in _CANDIDATE_PRIMITIVES:
        primitive_candidates = tuple(
            candidate
            for candidate in bazi_candidates + astrology_candidates
            if candidate.primitive_id == primitive_id
        )
        if not primitive_candidates:
            continue
        context_states = _resolve_context_states(primitive_candidates)
        directions = {candidate.direction for candidate in primitive_candidates}
        state = _resolve_global_state(context_states, directions)
        refs = tuple(ref for candidate in primitive_candidates for ref in candidate.fact_refs)
        rules = tuple(rule for candidate in primitive_candidates for rule in candidate.semantic_rule_refs)
        supporting = tuple(rule for candidate in primitive_candidates if candidate.direction == "high" for rule in candidate.semantic_rule_refs)
        counter = tuple(rule for candidate in primitive_candidates if candidate.direction == "low" for rule in candidate.semantic_rule_refs)
        states[primitive_id] = PrimitiveState(
            primitive_id=primitive_id,
            state=state,
            evidence_refs=refs,
            resolution_rule_ref="|".join(rules),
            context_states=context_states,
            supporting_candidates=supporting,
            counter_candidates=counter,
            contradictions=("opposite directions in the same context" if state == "mixed" else ()),
            unresolved_contexts=(tuple(sorted(context_states)) if state == "context_differentiated" else ()),
            limitations=("candidate rules; not production approved",) + (("global state preserves separate context directions",) if state == "context_differentiated" else ()),
        )
    return CandidateCoreProfile(
        schema_version="candidate-core-profile-v1",
        candidate_profile_id=f"candidate-{fingerprint[:16]}",
        fact_assurance=fact_assurance,
        semantic_model_assurance="project_semantic_partial",
        semantic_capability_level="primitive_only",
        semantic_bundle_fingerprint=candidate_semantic_bundle_fingerprint(),
        semantic_model_versions=_CANDIDATE_VERSIONS,
        bazi_primitive_candidates=bazi_candidates,
        astrology_primitive_candidates=astrology_candidates,
        cross_system_alignments=alignments,
        primitive_states=states,
        core_dynamics=(),
        archetype=None,
        limitations=(
            "candidate mappings are pending production approval; "
            "relation and derived-dynamic rules remain disabled",
        ),
    )


def normalize_candidate_profile(profile: CandidateCoreProfile) -> tuple:
    return (
        profile.schema_version,
        profile.fact_assurance,
        profile.semantic_model_assurance,
        profile.semantic_model_versions,
        tuple((item.primitive_id, item.source_system, item.direction, item.context, item.salience, item.evidence_stability, item.fact_refs, item.semantic_rule_refs, item.modifier_refs, item.counterevidence_refs, item.limitations) for item in profile.bazi_primitive_candidates + profile.astrology_primitive_candidates),
        tuple(
            (
                item.primitive_id,
                item.status,
                item.bazi_rule_refs,
                item.astrology_rule_refs,
                item.shared_contexts,
                item.limitations,
            )
            for item in profile.cross_system_alignments
        ),
        tuple(
            (primitive_id, state.state, tuple(sorted(state.context_states.items())), state.evidence_refs, state.resolution_rule_ref, state.supporting_candidates, state.counter_candidates, state.contradictions, state.unresolved_contexts, state.limitations)
            for primitive_id, state in sorted(profile.primitive_states.items())
        ),
        profile.semantic_capability_level,
        profile.semantic_bundle_fingerprint,
        profile.limitations,
    )


normalize_core_profile = normalize_candidate_profile


def _fact_fingerprint(facts: DeterministicChartFacts) -> str:
    return sha256(repr(asdict(facts)).encode("utf-8")).hexdigest()


def _extract_bazi_candidates(
    facts: DeterministicChartFacts,
) -> tuple[PrimitiveCandidate, ...]:
    rules_path = _candidate_asset_root() / "bazi_mapping_registry_v1.yaml"
    rules = yaml.safe_load(rules_path.read_text(encoding="utf-8"))["rules"]
    ten_god_facts = facts.bazi.ten_gods
    ten_gods = {fact.ten_god for fact in ten_god_facts}
    environment = derive_candidate_day_master_environment(facts.bazi)
    candidates = []
    for rule in rules:
        matching_facts = tuple(
            fact
            for fact in ten_god_facts
            if any(fact.ten_god in group for group in rule["requires_any_groups"])
        )
        source_pillars = {
            pillar for fact in matching_facts for pillar in fact.source_pillars
        }
        source_kinds_are_allowed = all(
            fact.source_kind.value in rule["allowed_source_kinds"]
            for fact in matching_facts
        )
        environment_ref = (
            (
                "bazi.day_master_environment:"
                f"{environment.day_master_stem}:{environment.day_master_element}:"
                f"{environment.month_branch}:{environment.season}:{environment.table_ref}",
            )
            if environment is not None
            else ()
        )
        if (
            all(ten_gods.intersection(group) for group in rule["requires_any_groups"])
            and len(source_pillars) >= rule["minimum_distinct_pillars"]
            and source_kinds_are_allowed
            and (not rule.get("requires_visible_evidence_per_group") or _has_visible_evidence_for_each_group(ten_god_facts, rule["requires_any_groups"]))
            and not ten_gods.intersection(rule.get("counterweight_any", ()))
            and (not rule["requires_day_master_environment"] or environment is not None)
        ):
            candidates.append(
                PrimitiveCandidate(
                    primitive_id=rule["primitive_id"],
                    source_system="bazi",
                    direction=rule["direction"],
                    fact_refs=tuple(
                        f"bazi.ten_gods:{value}"
                        for group in rule["requires_any_groups"]
                        for value in group
                        if value in ten_gods
                    ) + tuple(
                        f"bazi.ten_god_source:{fact.source_kind.value}"
                        for fact in matching_facts
                    ) + environment_ref,
                    semantic_rule_refs=(rule["rule_id"],),
                    context=rule["context"],
                    salience="moderate",
                    evidence_stability="deterministic",
                    modifier_refs=environment_ref,
                    counterevidence_refs=(),
                    limitations=("candidate rule; not production approved",),
                )
            )
    return tuple(candidates)


def _extract_astrology_candidates(
    facts: DeterministicChartFacts,
) -> tuple[PrimitiveCandidate, ...]:
    rules_path = _candidate_asset_root() / "astrology_mapping_registry_v1.yaml"
    registry = yaml.safe_load(rules_path.read_text(encoding="utf-8"))
    rules = registry["rules"]
    aspect_roles = registry["aspect_roles"]
    bodies = {placement.body for placement in facts.astrology.placements}
    known_time = facts.astrology.ascendant is not None
    candidates = []
    for rule in rules:
        required_pair = rule.get("requires_aspect_pair")
        matching_aspects = tuple(
            aspect
            for aspect in facts.astrology.aspects
            if required_pair
            and frozenset((aspect.body_a, aspect.body_b)) == frozenset(required_pair)
            and aspect.aspect_type in rule["allowed_aspect_types"]
            and aspect.orb <= rule["max_orb"]
        )
        has_required_aspect = not required_pair or bool(matching_aspects)
        if bodies.intersection(rule["requires_any_bodies"]) and has_required_aspect and (
            not rule.get("requires_known_time") or known_time
        ):
            modifier_refs = _astrology_modifier_refs(rule, facts)
            candidates.append(
                PrimitiveCandidate(
                    primitive_id=rule["primitive_id"],
                    source_system="astrology",
                    direction=rule["direction"],
                    fact_refs=tuple(
                        f"astrology.placements:{body}"
                        for body in rule["requires_any_bodies"]
                        if body in bodies
                    ) + tuple(
                        f"astrology.aspects:{aspect.body_a}:{aspect.aspect_type}:"
                        f"{aspect.body_b}:{aspect.orb}"
                        for aspect in matching_aspects
                    ) + modifier_refs,
                    semantic_rule_refs=(rule["rule_id"],),
                    context=rule["context"],
                    salience=_aspect_salience(matching_aspects),
                    evidence_stability="stable" if not known_time else "time_augmented",
                    modifier_refs=modifier_refs + _aspect_role_refs(matching_aspects, aspect_roles),
                    counterevidence_refs=(),
                    limitations=("candidate rule; not production approved",),
                )
            )
    return tuple(candidates)


def _astrology_modifier_refs(rule: dict, facts: DeterministicChartFacts) -> tuple[str, ...]:
    refs = []
    dignity_modifier_any = set(rule.get("dignity_modifier_any", ()))
    eligible_bodies = set(rule["requires_any_bodies"])
    for dignity in facts.astrology.dignities:
        if dignity.body in eligible_bodies and dignity.dignity in dignity_modifier_any:
            refs.append(f"astrology.dignities:{dignity.body}:{dignity.dignity}")
    if facts.astrology.ascendant is not None:
        angular_bodies = set(rule.get("angular_body_any", ()))
        allowed_houses = set(rule.get("house_context_any", ()))
        for placement in facts.astrology.placements:
            if placement.body in angular_bodies and placement.house in allowed_houses:
                refs.append(f"astrology.angular:{placement.body}:{placement.house}")
    return tuple(refs)


def _aspect_role_refs(aspects: Iterable[object], roles: dict[str, str]) -> tuple[str, ...]:
    return tuple(f"astrology.aspect_role:{roles[aspect.aspect_type]}" for aspect in aspects)


def _aspect_salience(aspects: Iterable[object]) -> str:
    return "strong" if any(aspect.orb <= 3 for aspect in aspects) else "moderate"


def _has_visible_evidence_for_each_group(ten_god_facts: tuple, groups: list[list[str]]) -> bool:
    return all(any(fact.ten_god in group and fact.source_kind.value == "visible_stem" for fact in ten_god_facts) for group in groups)


def _resolve_context_states(candidates: tuple[PrimitiveCandidate, ...]) -> Dict[str, str]:
    by_context: Dict[str, set[str]] = {}
    for candidate in candidates:
        by_context.setdefault(candidate.context, set()).add(candidate.direction)
    return {context: "mixed" if len(directions) > 1 else f"supported_{next(iter(directions))}" for context, directions in sorted(by_context.items())}


def _resolve_global_state(context_states: Dict[str, str], directions: set[str]) -> str:
    if len(directions) == 1:
        return f"supported_{next(iter(directions))}"
    return "mixed" if any(state == "mixed" for state in context_states.values()) else "context_differentiated"


def _candidate_asset_root() -> Path:
    return candidate_asset_root()


def _align_cross_system(
    bazi_candidates: tuple[PrimitiveCandidate, ...],
    astrology_candidates: tuple[PrimitiveCandidate, ...],
) -> tuple[CrossSystemAlignment, ...]:
    alignments = []
    for primitive_id in _CANDIDATE_PRIMITIVES:
        bazi_for_primitive = tuple(
            item for item in bazi_candidates if item.primitive_id == primitive_id
        )
        astrology_for_primitive = tuple(
            item for item in astrology_candidates if item.primitive_id == primitive_id
        )
        if not bazi_for_primitive and not astrology_for_primitive:
            continue
        bazi_directions = {item.direction for item in bazi_for_primitive}
        astrology_directions = {item.direction for item in astrology_for_primitive}
        shared_contexts = tuple(sorted({item.context for item in bazi_for_primitive} & {item.context for item in astrology_for_primitive}))
        if not bazi_for_primitive or not astrology_for_primitive:
            status = "non_comparable"
        elif not shared_contexts:
            status = "non_comparable"
        elif bazi_directions == astrology_directions and len(bazi_directions) == 1:
            status = "validation"
        else:
            status = "unresolved"
        alignments.append(
            CrossSystemAlignment(
                primitive_id=primitive_id,
                status=status,
                bazi_rule_refs=tuple(
                    rule for item in bazi_for_primitive for rule in item.semantic_rule_refs
                ),
                astrology_rule_refs=tuple(
                    rule for item in astrology_for_primitive for rule in item.semantic_rule_refs
                ),
                shared_contexts=shared_contexts,
                limitations=(
                    "candidate alignment is descriptive and does not alter primitive salience",
                ),
            )
        )
    return tuple(alignments)
