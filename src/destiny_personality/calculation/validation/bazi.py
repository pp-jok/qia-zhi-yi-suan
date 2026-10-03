from typing import Optional

from destiny_personality.config_models import RuntimeConfig

from ..errors import CalculationError
from ..models import (
    BaziChartFacts,
    BaziPillar,
    BaziRelationFact,
    FactMode,
    HiddenStemsFact,
    PillarPosition,
    TenGodFact,
    TenGodSourceKind,
)
from .common import contract_error, validate_nonempty_string


def validate_bazi_facts(
    facts: BaziChartFacts, fact_mode: FactMode, config: RuntimeConfig
) -> None:
    if type(facts) is not BaziChartFacts:
        raise contract_error("bazi", "backend must return BaziChartFacts")
    if facts.methodology_version != config.bazi.methodology_version:
        raise CalculationError(
            "METHODOLOGY_VERSION_MISMATCH",
            "Bazi methodology version does not match runtime config",
            system="bazi",
            field="methodology_version",
        )
    for field in ("year_pillar", "month_pillar", "day_pillar"):
        _validate_pillar(getattr(facts, field), field)
    if fact_mode is FactMode.STABLE_ONLY:
        if facts.hour_pillar is not None:
            raise contract_error(
                "bazi",
                "stable-only facts cannot include an hour pillar",
                "hour_pillar",
            )
    else:
        _validate_pillar(facts.hour_pillar, "hour_pillar")

    _validate_collection(facts.hidden_stems, HiddenStemsFact, "hidden_stems")
    for index, item in enumerate(facts.hidden_stems):
        pillar_field = f"hidden_stems.{index}.pillar"
        if type(item.pillar) is not PillarPosition:
            raise contract_error(
                "bazi", "pillar must be a PillarPosition", pillar_field
            )
        if (
            fact_mode is FactMode.STABLE_ONLY
            and item.pillar is PillarPosition.HOUR
        ):
            raise contract_error(
                "bazi",
                "stable-only facts cannot use an hour source",
                pillar_field,
            )
        if type(item.stems) is not tuple or any(
            type(stem) is not str or not stem.strip() for stem in item.stems
        ):
            raise contract_error(
                "bazi",
                "stems must be a tuple of non-empty strings",
                f"hidden_stems.{index}.stems",
            )

    _validate_collection(facts.ten_gods, TenGodFact, "ten_gods")
    for index, item in enumerate(facts.ten_gods):
        validate_nonempty_string(
            item.subject_ref, "bazi", f"ten_gods.{index}.subject_ref"
        )
        validate_nonempty_string(
            item.ten_god, "bazi", f"ten_gods.{index}.ten_god"
        )
        if type(item.source_kind) is not TenGodSourceKind:
            raise contract_error(
                "bazi", "source kind must be a TenGodSourceKind", f"ten_gods.{index}.source_kind"
            )
        _validate_source_pillars(
            item.source_pillars,
            f"ten_gods.{index}.source_pillars",
            fact_mode,
        )

    _validate_collection(facts.relations, BaziRelationFact, "relations")
    for index, item in enumerate(facts.relations):
        validate_nonempty_string(
            item.relation_type, "bazi", f"relations.{index}.relation_type"
        )
        validate_nonempty_string(
            item.rule_version, "bazi", f"relations.{index}.rule_version"
        )
        if type(item.participant_refs) is not tuple or any(
            type(ref) is not str or not ref.strip()
            for ref in item.participant_refs
        ):
            raise contract_error(
                "bazi",
                "participant refs must be a tuple of non-empty strings",
                f"relations.{index}.participant_refs",
            )
        _validate_source_pillars(
            item.source_pillars,
            f"relations.{index}.source_pillars",
            fact_mode,
        )
        if item.relation_type == "five_element_controls":
            _validate_five_element_control_relation(item, index)

    # Import locally to avoid coupling package initialization to the optional
    # canonical asset loader.
    from destiny_personality.canonical_bazi_relations import (
        CanonicalBaziRelationError,
        load_canonical_bazi_relation_policy,
        validate_canonical_bazi_relations,
    )

    try:
        validate_canonical_bazi_relations(
            facts, load_canonical_bazi_relation_policy()
        )
    except CanonicalBaziRelationError as error:
        raise contract_error("bazi", error.detail, error.field) from error


def _validate_pillar(value: object, field: str) -> None:
    if type(value) is not BaziPillar:
        raise contract_error("bazi", "value must be a BaziPillar", field)
    validate_nonempty_string(
        value.heavenly_stem, "bazi", f"{field}.heavenly_stem"
    )
    validate_nonempty_string(
        value.earthly_branch, "bazi", f"{field}.earthly_branch"
    )


def _validate_collection(value: object, item_type: type, field: str) -> None:
    if type(value) is not tuple:
        raise contract_error("bazi", "collection must be a tuple", field)
    for index, item in enumerate(value):
        if type(item) is not item_type:
            raise contract_error(
                "bazi", f"invalid {item_type.__name__}", f"{field}.{index}"
            )


def _validate_five_element_control_relation(
    relation: BaziRelationFact, index: int
) -> None:
    refs_field = f"relations.{index}.participant_refs"
    if len(relation.participant_refs) != 2 or len(set(relation.participant_refs)) != 2:
        raise contract_error(
            "bazi", "element control requires two distinct participants", refs_field
        )
    participant_pillars = set()
    for ref_index, subject_ref in enumerate(relation.participant_refs):
        pillar = _subject_ref_pillar(subject_ref)
        if pillar is None:
            raise contract_error(
                "bazi",
                "element control participant reference is invalid",
                f"{refs_field}.{ref_index}",
            )
        participant_pillars.add(pillar)
    if set(relation.source_pillars) != participant_pillars:
        raise contract_error(
            "bazi",
            "element control source pillars must match participant references",
            f"relations.{index}.source_pillars",
        )
    if relation.rule_version == "unversioned":
        raise contract_error(
            "bazi",
            "element control rule version must be governed",
            f"relations.{index}.rule_version",
        )


def _subject_ref_pillar(subject_ref: str) -> Optional[PillarPosition]:
    parts = subject_ref.split(".")
    if len(parts) == 2 and parts[1] == "stem":
        pass
    elif (
        len(parts) == 3
        and parts[1] == "hidden_stem"
        and parts[2].isdigit()
    ):
        pass
    else:
        return None
    try:
        return PillarPosition(parts[0])
    except ValueError:
        return None


def _validate_source_pillars(
    value: object, field: str, fact_mode: FactMode
) -> None:
    if type(value) is not tuple or not value:
        raise contract_error(
            "bazi", "source pillars must be a non-empty tuple", field
        )
    seen = set()
    for index, position in enumerate(value):
        item_field = f"{field}.{index}"
        if type(position) is not PillarPosition:
            raise contract_error(
                "bazi", "source pillar must be a PillarPosition", item_field
            )
        if position in seen:
            raise contract_error("bazi", "duplicate source pillar", item_field)
        if (
            fact_mode is FactMode.STABLE_ONLY
            and position is PillarPosition.HOUR
        ):
            raise contract_error(
                "bazi", "stable-only facts cannot use an hour source", item_field
            )
        seen.add(position)
