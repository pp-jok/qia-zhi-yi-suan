"""Candidate-only derivation of school-neutral Bazi element relations.

This module deliberately stops at raw, directed control presence. It is not
called by the calculation service and cannot establish an operative method.
"""

from dataclasses import dataclass, replace
from pathlib import Path
from typing import Mapping, Tuple

import yaml

from .calculation.models import (
    BaziChartFacts,
    BaziRelationFact,
    HiddenStemsFact,
    PillarPosition,
    TenGodSourceKind,
)
from .canonical_bazi_relations import (
    CanonicalBaziRelationPolicy,
    canonical_relation_identity,
)


CONTRACT_FILE = "bazi_neutral_relation_contract_v1.yaml"
SCHEMA_VERSION = "candidate-bazi-neutral-relation-v1"
_ROOT_KEYS = {
    "schema_version",
    "contract_version",
    "review_status",
    "activation_status",
    "implementation_status",
    "relation",
    "subject_ref_templates",
    "stem_elements",
    "controls",
    "prohibited_fields",
    "limitations",
}
_PILLAR_ORDER = {position: index for index, position in enumerate(PillarPosition)}


@dataclass(frozen=True)
class NeutralBaziRelationPolicy:
    contract_version: str
    implementation_status: str
    relation_type: str
    rule_version: str
    participant_roles: Tuple[str, str]
    visible_stem_template: str
    hidden_stem_template: str
    stem_elements: Mapping[str, str]
    controls: Mapping[str, str]
    prohibited_fields: frozenset[str]


@dataclass(frozen=True)
class _StemSubject:
    subject_ref: str
    stem: str
    pillar: PillarPosition
    source_kind: TenGodSourceKind


def load_neutral_bazi_relation_policy(root: Path) -> NeutralBaziRelationPolicy:
    """Load the inactive candidate policy and reject incomplete contracts."""

    path = Path(root) / CONTRACT_FILE
    try:
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as error:
        raise ValueError("NEUTRAL_BAZI_RELATION_CONTRACT_INVALID") from error
    if type(payload) is not dict or set(payload) != _ROOT_KEYS:
        raise ValueError("NEUTRAL_BAZI_RELATION_CONTRACT_INVALID")
    if (
        payload["schema_version"] != SCHEMA_VERSION
        or payload["review_status"] != "candidate_only"
        or payload["activation_status"] != "inactive"
        or payload["implementation_status"]
        != "candidate_provider_available_not_activated"
    ):
        raise ValueError("NEUTRAL_BAZI_RELATION_CONTRACT_INVALID")

    relation = payload["relation"]
    templates = payload["subject_ref_templates"]
    if (
        type(relation) is not dict
        or set(relation)
        != {"relation_type", "rule_version", "participant_roles"}
        or relation["participant_roles"] != ["controller", "controlled"]
        or type(templates) is not dict
        or set(templates) != {"visible_stem", "hidden_stem"}
    ):
        raise ValueError("NEUTRAL_BAZI_RELATION_CONTRACT_INVALID")

    stem_elements = _string_mapping(payload["stem_elements"])
    controls = _string_mapping(payload["controls"])
    prohibited_fields = _string_list(payload["prohibited_fields"])
    if set(stem_elements) != set("甲乙丙丁戊己庚辛壬癸"):
        raise ValueError("NEUTRAL_BAZI_RELATION_CONTRACT_INVALID")
    if set(controls) != {"wood", "fire", "earth", "metal", "water"}:
        raise ValueError("NEUTRAL_BAZI_RELATION_CONTRACT_INVALID")

    return NeutralBaziRelationPolicy(
        contract_version=_string(payload["contract_version"]),
        implementation_status=payload["implementation_status"],
        relation_type=_string(relation["relation_type"]),
        rule_version=_string(relation["rule_version"]),
        participant_roles=("controller", "controlled"),
        visible_stem_template=_string(templates["visible_stem"]),
        hidden_stem_template=_string(templates["hidden_stem"]),
        stem_elements=stem_elements,
        controls=controls,
        prohibited_fields=frozenset(prohibited_fields),
    )


def derive_candidate_neutral_relations(
    facts: BaziChartFacts,
    policy: NeutralBaziRelationPolicy,
) -> Tuple[BaziRelationFact, ...]:
    """Compatibility alias for canonical neutral relation derivation."""

    return derive_canonical_neutral_relations(facts, policy)


def derive_canonical_neutral_relations(
    facts: BaziChartFacts,
    policy: CanonicalBaziRelationPolicy,
) -> Tuple[BaziRelationFact, ...]:
    """Derive deterministic raw control relations without method judgements."""

    if type(facts) is not BaziChartFacts:
        raise TypeError("BAZI_CHART_FACTS_REQUIRED")
    subjects = _stem_subjects(facts, policy)
    relations = {}
    for controller in subjects:
        for controlled in subjects:
            if (
                controller.subject_ref == controlled.subject_ref
                or policy.controls[policy.stem_elements[controller.stem]]
                != policy.stem_elements[controlled.stem]
            ):
                continue
            relation = BaziRelationFact(
                relation_type=policy.relation_type,
                participant_refs=(controller.subject_ref, controlled.subject_ref),
                source_pillars=_source_pillars(
                    controller.pillar, controlled.pillar
                ),
                rule_version=policy.rule_version,
            )
            relations[canonical_relation_identity(relation)] = relation
    return tuple(relations[key] for key in sorted(relations))


def canonicalize_bazi_subjects(
    facts: BaziChartFacts,
    policy: CanonicalBaziRelationPolicy,
) -> BaziChartFacts:
    """Normalize provider-specific hidden-stem order to canonical identity."""

    if type(facts) is not BaziChartFacts:
        raise TypeError("BAZI_CHART_FACTS_REQUIRED")
    pillars = {
        PillarPosition.YEAR: facts.year_pillar,
        PillarPosition.MONTH: facts.month_pillar,
        PillarPosition.DAY: facts.day_pillar,
    }
    if facts.hour_pillar is not None:
        pillars[PillarPosition.HOUR] = facts.hour_pillar

    raw_hidden = {}
    for item in facts.hidden_stems:
        if item.pillar in raw_hidden:
            raise ValueError("DUPLICATE_HIDDEN_STEM_PROVENANCE")
        raw_hidden[item.pillar] = item.stems
    if set(raw_hidden) != set(pillars):
        if set(pillars) - set(raw_hidden):
            raise ValueError("HIDDEN_STEM_PILLAR_MISSING")
        raise ValueError("HIDDEN_STEM_PILLAR_UNAVAILABLE")

    index_maps = {}
    normalized_hidden = []
    for position in PillarPosition:
        pillar = pillars.get(position)
        if pillar is None:
            continue
        expected = policy.hidden_stems.get(pillar.earthly_branch)
        actual = raw_hidden[position]
        if expected is None or len(actual) != len(expected) or set(actual) != set(expected):
            raise ValueError("HIDDEN_STEM_SET_MISMATCH")
        index_maps[position] = {
            old_index: expected.index(stem) for old_index, stem in enumerate(actual)
        }
        normalized_hidden.append(HiddenStemsFact(position, expected))

    def remap_ref(subject_ref: str) -> str:
        parts = subject_ref.split(".")
        if len(parts) != 3 or parts[1] != "hidden_stem" or not parts[2].isdigit():
            return subject_ref
        try:
            position = PillarPosition(parts[0])
            new_index = index_maps[position][int(parts[2])]
        except (ValueError, KeyError, IndexError) as error:
            raise ValueError("TEN_GOD_SUBJECT_REF_INVALID") from error
        return policy.hidden_stem_template.format(
            pillar=position.value, index=new_index
        )

    ten_gods = tuple(
        replace(item, subject_ref=remap_ref(item.subject_ref))
        for item in facts.ten_gods
    )
    relations = []
    for item in facts.relations:
        participant_refs = tuple(remap_ref(ref) for ref in item.participant_refs)
        relations.append(
            item
            if participant_refs == item.participant_refs
            else replace(item, participant_refs=participant_refs)
        )
    return replace(
        facts,
        hidden_stems=tuple(normalized_hidden),
        ten_gods=ten_gods,
        relations=tuple(relations),
    )


def validate_ten_god_subject_refs(
    facts: BaziChartFacts,
    policy: NeutralBaziRelationPolicy,
) -> None:
    """Require Ten-God instances to join to the governed stem catalogue."""

    subjects = {item.subject_ref: item for item in _stem_subjects(facts, policy)}
    for fact in facts.ten_gods:
        if fact.source_kind is TenGodSourceKind.UNKNOWN:
            raise ValueError("TEN_GOD_SUBJECT_KIND_UNRESOLVED")
        subject = subjects.get(fact.subject_ref)
        if subject is None or subject.source_kind is not fact.source_kind:
            raise ValueError("TEN_GOD_SUBJECT_REF_INVALID")
        if subject.pillar not in fact.source_pillars:
            raise ValueError("TEN_GOD_SOURCE_PILLAR_MISMATCH")


def _stem_subjects(
    facts: BaziChartFacts, policy: NeutralBaziRelationPolicy
) -> Tuple[_StemSubject, ...]:
    pillars = (
        (PillarPosition.YEAR, facts.year_pillar),
        (PillarPosition.MONTH, facts.month_pillar),
        (PillarPosition.DAY, facts.day_pillar),
        (PillarPosition.HOUR, facts.hour_pillar),
    )
    subjects = []
    for position, pillar in pillars:
        if pillar is None:
            continue
        _element(pillar.heavenly_stem, policy)
        subjects.append(
            _StemSubject(
                policy.visible_stem_template.format(pillar=position.value),
                pillar.heavenly_stem,
                position,
                TenGodSourceKind.VISIBLE_STEM,
            )
        )

    hidden_by_pillar = {}
    for item in facts.hidden_stems:
        if item.pillar in hidden_by_pillar:
            raise ValueError("DUPLICATE_HIDDEN_STEM_PROVENANCE")
        hidden_by_pillar[item.pillar] = item.stems
    for position in PillarPosition:
        for index, stem in enumerate(hidden_by_pillar.get(position, ())):
            _element(stem, policy)
            subjects.append(
                _StemSubject(
                    policy.hidden_stem_template.format(
                        pillar=position.value, index=index
                    ),
                    stem,
                    position,
                    TenGodSourceKind.HIDDEN_STEM,
                )
            )
    return tuple(subjects)


def _element(stem: str, policy: NeutralBaziRelationPolicy) -> str:
    try:
        return policy.stem_elements[stem]
    except (KeyError, TypeError) as error:
        raise ValueError("UNKNOWN_BAZI_STEM") from error


def _source_pillars(
    controller: PillarPosition, controlled: PillarPosition
) -> Tuple[PillarPosition, ...]:
    return tuple(
        sorted({controller, controlled}, key=lambda position: _PILLAR_ORDER[position])
    )


def _string(value: object) -> str:
    if type(value) is not str or not value.strip():
        raise ValueError("NEUTRAL_BAZI_RELATION_CONTRACT_INVALID")
    return value


def _string_mapping(value: object) -> Mapping[str, str]:
    if type(value) is not dict or not value:
        raise ValueError("NEUTRAL_BAZI_RELATION_CONTRACT_INVALID")
    return {_string(key): _string(item) for key, item in value.items()}


def _string_list(value: object) -> Tuple[str, ...]:
    if type(value) is not list or not value:
        raise ValueError("NEUTRAL_BAZI_RELATION_CONTRACT_INVALID")
    return tuple(_string(item) for item in value)
