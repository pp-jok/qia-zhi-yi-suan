"""Candidate-only derivation of school-neutral Bazi element relations.

This module deliberately stops at raw, directed control presence. It is not
called by the calculation service and cannot establish an operative method.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Mapping, Tuple

import yaml

from .calculation.models import (
    BaziChartFacts,
    BaziRelationFact,
    PillarPosition,
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
        != "candidate_implementation_not_emitted"
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
    """Derive deterministic raw control relations without method judgements."""

    if type(facts) is not BaziChartFacts:
        raise TypeError("BAZI_CHART_FACTS_REQUIRED")
    subjects = _stem_subjects(facts, policy)
    relations = {
        BaziRelationFact(
            relation_type=policy.relation_type,
            participant_refs=(controller.subject_ref, controlled.subject_ref),
            source_pillars=_source_pillars(controller.pillar, controlled.pillar),
        )
        for controller in subjects
        for controlled in subjects
        if controller.subject_ref != controlled.subject_ref
        and policy.controls[policy.stem_elements[controller.stem]]
        == policy.stem_elements[controlled.stem]
    }
    return tuple(
        sorted(
            relations,
            key=lambda item: (
                item.relation_type,
                item.participant_refs,
                tuple(position.value for position in item.source_pillars),
            ),
        )
    )


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
