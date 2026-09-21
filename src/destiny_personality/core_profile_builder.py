from dataclasses import asdict
from hashlib import sha256
from pathlib import Path
from typing import Dict, Iterable, Optional, Union

import yaml

from .calculation.models import DeterministicChartFacts
from .candidate_assets import candidate_asset_root
from .context_taxonomy import load_candidate_context_taxonomy
from .core_profile_models import (
    CandidateCoreProfile,
    CandidateFactScope,
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
    ("state_policy", "candidate-state-policy-v2"),
    ("state_resolver", "candidate-state-resolver-v3"),
    ("bazi_mapping", "candidate-c2-bazi-v2"),
    ("astrology_mapping", "candidate-c2-astrology-v2"),
    ("alignment", "candidate-alignment-v2"),
    ("alignment_policy", "candidate-context-v1"),
    ("alignment_resolver", "candidate-alignment-resolver-v3"),
    ("candidate_builder", "candidate-builder-semantic-v3"),
    ("context_taxonomy", "candidate-context-v1"),
    ("evidence_weighting", "candidate-evidence-weighting-v1"),
    ("dynamic_formation", "c3-review-v1"),
    ("calibration_protocol", "c4a-review-v1"),
)

_SEMANTIC_ALGORITHM_VERSIONS = (
    "candidate-builder-semantic-v3",
    "candidate-state-resolver-v3",
    "candidate-alignment-resolver-v3",
    "candidate-similarity-resolver-v2",
)


def candidate_semantic_bundle_fingerprint(candidate_root: Optional[Path] = None) -> str:
    """Fingerprint D1 semantic assets without creating a circular calibration hash."""

    digest = sha256()
    for path in sorted((candidate_root or _candidate_asset_root()).glob("*.yaml")):
        if path.name.startswith(("core_profile_calibration_policy_", "holdout_validation_")):
            continue
        digest.update(path.name.encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    for version in _SEMANTIC_ALGORITHM_VERSIONS:
        digest.update(version.encode("utf-8"))
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
            resolution_rule_ref="candidate-state-policy-v2:no-mapped-evidence",
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
        state = _resolve_global_state(context_states, directions, primitive_candidates)
        refs = tuple(ref for candidate in primitive_candidates for ref in candidate.fact_refs)
        rules = tuple(rule for candidate in primitive_candidates for rule in candidate.semantic_rule_refs)
        supporting = tuple(
            rule
            for candidate in primitive_candidates
            if candidate.direction == "high"
            for rule in candidate.semantic_rule_refs
        )
        counter = tuple(
            rule
            for candidate in primitive_candidates
            if candidate.direction == "low"
            for rule in candidate.semantic_rule_refs
        )
        states[primitive_id] = PrimitiveState(
            primitive_id=primitive_id,
            state=state,
            evidence_refs=refs,
            resolution_rule_ref="|".join(rules),
            context_states=context_states,
            supporting_candidates=supporting,
            counter_candidates=counter,
            contradictions=_state_contradictions(state, primitive_candidates),
            unresolved_contexts=(
                tuple(sorted(context_states)) if state == "context_differentiated" else ()
            ),
            limitations=("candidate rules; not production approved",) + (
                ("global state preserves separate context directions",)
                if state == "context_differentiated"
                else ()
            ) + (("counterweight contextualization retained",) if any(candidate.counterweight_effect for candidate in primitive_candidates) else ()),
        )
    return CandidateCoreProfile(
        schema_version="candidate-core-profile-v1",
        candidate_profile_id=f"candidate-{sha256(f'{fingerprint}:{candidate_semantic_bundle_fingerprint()}'.encode('utf-8')).hexdigest()[:16]}",
        fact_fingerprint=fingerprint,
        fact_scope=CandidateFactScope(
            birth_time_known=facts.astrology.ascendant is not None,
            astrology_time_mode="known_time" if facts.astrology.ascendant is not None else "stable_only",
            bazi_hour_available=facts.bazi.hour_pillar is not None,
        ),
        fact_assurance=fact_assurance,
        semantic_model_assurance="project_semantic_partial",
        semantic_capability_level="primitive_only",
        semantic_bundle_fingerprint=candidate_semantic_bundle_fingerprint(),
        semantic_model_versions=_CANDIDATE_VERSIONS,
        bazi_primitive_candidates=bazi_candidates,
        astrology_primitive_candidates=astrology_candidates,
        cross_system_alignments=alignments,
        primitive_states=states,
        limitations=(
            "candidate mappings are pending production approval; "
            "relation and derived-dynamic rules remain disabled",
        ),
    )


def normalize_candidate_profile(profile: CandidateCoreProfile) -> tuple:
    return (
        profile.schema_version,
        profile.fact_fingerprint,
        profile.fact_assurance,
        profile.semantic_model_assurance,
        profile.semantic_model_versions,
        tuple(
            (
                item.primitive_id,
                item.source_system,
                item.direction,
                item.contexts,
                item.salience,
                item.evidence_stability,
                item.fact_refs,
                item.semantic_rule_refs,
                item.modifier_refs,
                item.counterevidence_refs,
                item.expression_mode,
                item.tension_level,
                item.counterweight_effect,
                item.limitations,
            )
            for item in profile.bazi_primitive_candidates + profile.astrology_primitive_candidates
        ),
        tuple(
            (
                item.alignment_id,
                item.primitive_id,
                item.context_refs,
                item.status,
                item.direction_relation,
                item.bazi_rule_refs,
                item.astrology_rule_refs,
                item.limitations,
            )
            for item in profile.cross_system_alignments
        ),
        tuple(
            (
                primitive_id,
                state.state,
                tuple(sorted(state.context_states.items())),
                state.evidence_refs,
                state.resolution_rule_ref,
                state.supporting_candidates,
                state.counter_candidates,
                state.contradictions,
                state.unresolved_contexts,
                state.limitations,
            )
            for primitive_id, state in sorted(profile.primitive_states.items())
        ),
        profile.semantic_capability_level,
        profile.semantic_bundle_fingerprint,
        profile.limitations,
    )


# Kept as an import-compatible name during the candidate pre-release series.
normalize_core_profile = normalize_candidate_profile


def _fact_fingerprint(facts: DeterministicChartFacts) -> str:
    return sha256(repr(asdict(facts)).encode("utf-8")).hexdigest()


def _extract_bazi_candidates(
    facts: DeterministicChartFacts,
) -> tuple[PrimitiveCandidate, ...]:
    rules_path = _candidate_asset_root() / "bazi_mapping_registry_v1.yaml"
    rules = yaml.safe_load(rules_path.read_text(encoding="utf-8"))["rules"]
    weighting = _load_evidence_weighting_policy()["bazi"]
    taxonomy = load_candidate_context_taxonomy()
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
        counterevidence_refs, counterweight_effect = _counterweight_evidence(rule, ten_gods)
        if (
            all(ten_gods.intersection(group) for group in rule["requires_any_groups"])
            and len(source_pillars) >= rule["minimum_distinct_pillars"]
            and source_kinds_are_allowed
            and (
                not rule.get("requires_visible_evidence_per_group")
                or _has_visible_evidence_for_each_group(ten_god_facts, rule["requires_any_groups"])
            )
            and (not rule["requires_day_master_environment"] or environment is not None)
        ):
            contexts = _validated_contexts(rule["contexts"], taxonomy.contexts)
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
                    contexts=contexts,
                    salience=weighting["default_salience"],
                    evidence_stability="environment_contextualized",
                    modifier_refs=environment_ref + (
                        (f"bazi.environment_effect:{rule['environment_effect']}:{environment.season}",)
                        if environment is not None
                        else ()
                    ),
                    counterevidence_refs=counterevidence_refs,
                    expression_mode="contextualized" if environment is not None else "direct",
                    tension_level="medium" if counterweight_effect else "low",
                    counterweight_effect=counterweight_effect,
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
    aspect_semantics = registry["aspect_semantics"]
    weighting = _load_evidence_weighting_policy()["astrology"]
    taxonomy = load_candidate_context_taxonomy()
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
            aspect_semantic = _combined_aspect_semantics(matching_aspects, aspect_semantics)
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
                    contexts=_validated_contexts(rule["contexts"], taxonomy.contexts),
                    salience=_aspect_salience(matching_aspects, weighting["orb_bands"]),
                    evidence_stability="stable" if not known_time else "time_augmented",
                    modifier_refs=modifier_refs + _aspect_role_refs(matching_aspects, aspect_semantics),
                    counterevidence_refs=(),
                    expression_mode=aspect_semantic["expression_mode"],
                    tension_level=aspect_semantic["tension_level"],
                    counterweight_effect=None,
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


def _aspect_role_refs(aspects: Iterable[object], semantics: dict[str, dict]) -> tuple[str, ...]:
    return tuple(
        f"astrology.aspect_expression:{semantics[aspect.aspect_type]['expression_mode']}:"
        f"{semantics[aspect.aspect_type]['tension_level']}"
        for aspect in aspects
    )


def _aspect_salience(aspects: Iterable[object], orb_bands: dict[str, dict]) -> str:
    minimum_orb = min(aspect.orb for aspect in aspects)
    for label, policy in sorted(orb_bands.items(), key=lambda item: item[1]["max_orb"]):
        if minimum_orb <= policy["max_orb"]:
            return label
    raise ValueError("aspect exceeds approved orb bands")


def _combined_aspect_semantics(aspects: Iterable[object], semantics: dict[str, dict]) -> dict[str, str]:
    values = [semantics[aspect.aspect_type] for aspect in aspects]
    return max(values, key=lambda item: {"low": 0, "medium": 1, "high": 2}[item["tension_level"]])


def _load_evidence_weighting_policy() -> dict:
    path = _candidate_asset_root() / "candidate_evidence_weighting_policy_v1.yaml"
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _validated_contexts(contexts: Iterable[str], allowed_contexts: set[str]) -> tuple[str, ...]:
    result = tuple(sorted(set(contexts)))
    if not result or not set(result).issubset(allowed_contexts):
        raise ValueError("candidate mapping contains an unapproved context tag")
    return result


def _context_scope(contexts: tuple[str, ...]) -> str:
    return "+".join(contexts)


def _counterweight_evidence(rule: dict, ten_gods: set[str]) -> tuple[tuple[str, ...], Optional[str]]:
    for policy in rule.get("counterweight_rules", ()):
        matched = tuple(value for value in policy["evidence_any"] if value in ten_gods)
        if matched:
            return tuple(f"bazi.ten_gods:{value}" for value in matched), policy["effect"]
    return (), None


def _has_visible_evidence_for_each_group(ten_god_facts: tuple, groups: list[list[str]]) -> bool:
    return all(
        any(
            fact.ten_god in group and fact.source_kind.value == "visible_stem"
            for fact in ten_god_facts
        )
        for group in groups
    )


def _resolve_context_states(candidates: tuple[PrimitiveCandidate, ...]) -> Dict[str, str]:
    by_context: Dict[str, set[str]] = {}
    for candidate in candidates:
        by_context.setdefault(_context_scope(candidate.contexts), set()).add(candidate.direction)
    return {
        context: "mixed" if len(directions) > 1 else f"supported_{next(iter(directions))}"
        for context, directions in sorted(by_context.items())
    }


def _resolve_global_state(
    context_states: Dict[str, str],
    directions: set[str],
    candidates: tuple[PrimitiveCandidate, ...],
) -> str:
    if len(directions) == 1:
        return f"supported_{next(iter(directions))}"
    if any(state == "mixed" for state in context_states.values()):
        return "mixed"
    if any(
        left.direction != right.direction and set(left.contexts) & set(right.contexts)
        for index, left in enumerate(candidates)
        for right in candidates[index + 1 :]
    ):
        return "mixed"
    return "context_differentiated"


def _state_contradictions(state: str, candidates: tuple[PrimitiveCandidate, ...]) -> tuple[str, ...]:
    if state != "mixed":
        return ()
    if any(
        left.direction != right.direction and set(left.contexts) & set(right.contexts)
        and set(left.contexts) != set(right.contexts)
        for index, left in enumerate(candidates)
        for right in candidates[index + 1 :]
    ):
        return ("opposite directions in overlapping context scopes",)
    return ("opposite directions in the same context",)


def _candidate_asset_root() -> Path:
    return candidate_asset_root()


def _align_cross_system(
    bazi_candidates: tuple[PrimitiveCandidate, ...],
    astrology_candidates: tuple[PrimitiveCandidate, ...],
) -> tuple[CrossSystemAlignment, ...]:
    alignments = []
    comparison_policy = load_candidate_context_taxonomy().comparison_policy
    for primitive_id in _CANDIDATE_PRIMITIVES:
        bazi_for_primitive = tuple(
            item for item in bazi_candidates if item.primitive_id == primitive_id
        )
        astrology_for_primitive = tuple(
            item for item in astrology_candidates if item.primitive_id == primitive_id
        )
        if not bazi_for_primitive and not astrology_for_primitive:
            continue
        if not bazi_for_primitive or not astrology_for_primitive:
            alignments.extend(_single_system_alignments(primitive_id, bazi_for_primitive, astrology_for_primitive))
            continue
        for bazi_candidate in bazi_for_primitive:
            for astrology_candidate in astrology_for_primitive:
                shared = tuple(sorted(set(bazi_candidate.contexts) & set(astrology_candidate.contexts)))
                exact = set(bazi_candidate.contexts) == set(astrology_candidate.contexts)
                relation = "same" if bazi_candidate.direction == astrology_candidate.direction else "opposed"
                status = _alignment_status(comparison_policy, exact, bool(shared), relation)
                scope = shared or tuple(sorted(set(bazi_candidate.contexts) | set(astrology_candidate.contexts)))
                alignments.append(_alignment(primitive_id, scope, status, relation, bazi_candidate, astrology_candidate))
    return tuple(alignments)


def _alignment_status(policy: dict[str, str], exact: bool, has_overlap: bool, relation: str) -> str:
    if relation == "opposed" and has_overlap:
        return "unresolved"
    key = "exact_overlap" if exact else "partial_overlap" if has_overlap else "no_overlap"
    result = policy[key]
    return "validation" if result == "comparable" else result


def _single_system_alignments(
    primitive_id: str,
    bazi_candidates: tuple[PrimitiveCandidate, ...],
    astrology_candidates: tuple[PrimitiveCandidate, ...],
) -> tuple[CrossSystemAlignment, ...]:
    result = []
    for candidate in bazi_candidates + astrology_candidates:
        result.append(
            _alignment(
                primitive_id,
                candidate.contexts,
                "non_comparable",
                "single_system",
                candidate if candidate.source_system == "bazi" else None,
                candidate if candidate.source_system == "astrology" else None,
            )
        )
    return tuple(result)


def _alignment(
    primitive_id: str,
    contexts: tuple[str, ...],
    status: str,
    direction_relation: str,
    bazi_candidate: Optional[PrimitiveCandidate],
    astrology_candidate: Optional[PrimitiveCandidate],
) -> CrossSystemAlignment:
    bazi_refs = bazi_candidate.semantic_rule_refs if bazi_candidate else ()
    astrology_refs = astrology_candidate.semantic_rule_refs if astrology_candidate else ()
    scope = _context_scope(contexts)
    return CrossSystemAlignment(
        alignment_id=f"{primitive_id}:{scope}:{'|'.join(bazi_refs)}:{'|'.join(astrology_refs)}",
        primitive_id=primitive_id,
        context_refs=contexts,
        status=status,
        direction_relation=direction_relation,
        bazi_rule_refs=bazi_refs,
        astrology_rule_refs=astrology_refs,
        limitations=("candidate alignment is descriptive and does not alter primitive salience",),
    )
