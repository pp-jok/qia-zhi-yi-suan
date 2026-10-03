"""Canonical, semantic-free identity policy for neutral Bazi relations."""

from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import Mapping, Optional, Tuple

import yaml

from .calculation.models import BaziChartFacts, BaziRelationFact, PillarPosition


ASSET_FILES = (
    "bazi_hidden_stem_order_v1.yaml",
    "bazi_subject_ref_contract_v1.yaml",
    "bazi_relation_canonical_contract_v1.yaml",
)
_BRANCHES = set("子丑寅卯辰巳午未申酉戌亥")
_STEMS = set("甲乙丙丁戊己庚辛壬癸")
_PILLARS = ("year", "month", "day", "hour")
_PROHIBITED = {
    "operative",
    "qualification",
    "rescue",
    "effective",
    "strength",
    "strength_score",
    "dao_shi",
    "personality",
    "primitive",
    "primitive_direction",
    "supported_high",
    "supported_low",
}


@dataclass(frozen=True)
class CanonicalBaziRelationPolicy:
    hidden_stem_order_version: str
    subject_ref_contract_version: str
    relation_contract_version: str
    family_id: str
    hidden_stems: Mapping[str, Tuple[str, ...]]
    pillars: Tuple[str, ...]
    visible_stem_template: str
    hidden_stem_template: str
    source_kinds: Mapping[str, str]
    stem_elements: Mapping[str, str]
    controls: Mapping[str, str]
    approved_rule_versions: Mapping[str, str]
    relation_type: str
    rule_version: str
    participant_roles: Tuple[str, str]
    identity_fields: Tuple[str, ...]
    provenance_fields: Tuple[str, ...]
    ordering_fields: Tuple[str, ...]
    prohibited_fields: frozenset[str]
    provider_authority: str
    default_provider_activation: bool


class CanonicalBaziRelationError(ValueError):
    """Stable fail-closed error at the canonical relation boundary."""

    def __init__(self, detail: str, field: str) -> None:
        super().__init__(f"{detail} | {field}")
        self.detail = detail
        self.field = field


def canonical_bazi_relation_asset_root() -> Path:
    return Path(__file__).resolve().parent / "canonical_assets" / "calculation-v1"


def load_canonical_bazi_relation_policy(
    root: Optional[Path] = None,
) -> CanonicalBaziRelationPolicy:
    directory = Path(root) if root is not None else canonical_bazi_relation_asset_root()
    try:
        hidden = _mapping(_load(directory / ASSET_FILES[0]))
        subjects = _mapping(_load(directory / ASSET_FILES[1]))
        relations = _mapping(_load(directory / ASSET_FILES[2]))
        _exact_keys(
            hidden,
            {
                "schema_version",
                "policy_version",
                "review_status",
                "ordering_semantics",
                "branches",
                "prohibited_semantics",
            },
        )
        _exact_keys(
            subjects,
            {
                "schema_version",
                "contract_version",
                "review_status",
                "hidden_stem_order_policy_ref",
                "pillars",
                "templates",
                "source_kind_mapping",
                "valid_examples",
                "invalid_examples",
            },
        )
        _exact_keys(
            relations,
            {
                "schema_version",
                "contract_version",
                "review_status",
                "family_id",
                "fact_type",
                "allowed_relations",
                "identity_fields",
                "provenance_fields",
                "ordering_fields",
                "deduplication_fields",
                "stem_elements",
                "controls",
                "provider_authority",
                "default_provider_activation",
                "validation",
                "prohibited_fields",
            },
        )

        branches = _mapping(hidden["branches"])
        if set(branches) != _BRANCHES:
            raise ValueError
        hidden_stems = {
            _string(branch): _string_tuple(stems)
            for branch, stems in branches.items()
        }
        if any(not stems or len(stems) != len(set(stems)) for stems in hidden_stems.values()):
            raise ValueError
        if {stem for stems in hidden_stems.values() for stem in stems} != _STEMS:
            raise ValueError

        templates = _mapping(subjects["templates"])
        source_kinds = _string_mapping(subjects["source_kind_mapping"])
        allowed = _list(relations["allowed_relations"])
        if len(allowed) != 1:
            raise ValueError
        relation = _mapping(allowed[0])
        _exact_keys(
            relation, {"relation_type", "rule_version", "direction", "arity"}
        )
        identity = _string_tuple(relations["identity_fields"])
        provenance = _string_tuple(relations["provenance_fields"])
        ordering = _string_tuple(relations["ordering_fields"])
        if (
            hidden["schema_version"] != "bazi-hidden-stem-order-v1"
            or hidden["policy_version"] != "bazi-hidden-stem-order-v1"
            or hidden["review_status"] != "canonical"
            or hidden["ordering_semantics"] != "identity_only"
            or subjects["schema_version"] != "bazi-subject-ref-contract-v1"
            or subjects["contract_version"] != "bazi-subject-ref-v1"
            or subjects["review_status"] != "canonical"
            or subjects["hidden_stem_order_policy_ref"] != hidden["policy_version"]
            or _string_tuple(subjects["pillars"]) != _PILLARS
            or set(templates) != {"visible_stem", "hidden_stem"}
            or templates["visible_stem"] != "{pillar}.stem"
            or templates["hidden_stem"] != "{pillar}.hidden_stem.{index}"
            or source_kinds
            != {"visible_stem": "visible_stem", "hidden_stem": "hidden_stem"}
            or relations["schema_version"]
            != "bazi-relation-canonical-contract-v1"
            or relations["contract_version"] != "bazi-relation-canonical-v1"
            or relations["review_status"] != "canonical"
            or relations["family_id"] != "deterministic_facts.bazi.relations"
            or relations["fact_type"] != "BaziRelationFact"
            or relation["relation_type"] != "five_element_controls"
            or relation["rule_version"] != "wuxing-control-v1"
            or _string_tuple(relation["direction"])
            != ("controller", "controlled")
            or relation["arity"] != 2
            or identity
            != ("relation_type", "participant_refs", "rule_version")
            or provenance != ("source_pillars",)
            or ordering != identity
            or _string_tuple(relations["deduplication_fields"]) != identity
            or relations["provider_authority"] != "conformance_reference_only"
            or relations["default_provider_activation"] is not False
        ):
            raise ValueError
        stem_elements = _string_mapping(relations["stem_elements"])
        controls = _string_mapping(relations["controls"])
        prohibited = frozenset(_string_tuple(relations["prohibited_fields"]))
        if set(stem_elements) != _STEMS or set(controls) != {
            "wood",
            "fire",
            "earth",
            "metal",
            "water",
        } or not _PROHIBITED.issubset(prohibited):
            raise ValueError

        return CanonicalBaziRelationPolicy(
            hidden_stem_order_version=hidden["policy_version"],
            subject_ref_contract_version=subjects["contract_version"],
            relation_contract_version=relations["contract_version"],
            family_id=relations["family_id"],
            hidden_stems=hidden_stems,
            pillars=_PILLARS,
            visible_stem_template=templates["visible_stem"],
            hidden_stem_template=templates["hidden_stem"],
            source_kinds=source_kinds,
            stem_elements=stem_elements,
            controls=controls,
            approved_rule_versions={relation["relation_type"]: relation["rule_version"]},
            relation_type=relation["relation_type"],
            rule_version=relation["rule_version"],
            participant_roles=("controller", "controlled"),
            identity_fields=identity,
            provenance_fields=provenance,
            ordering_fields=ordering,
            prohibited_fields=prohibited,
            provider_authority=relations["provider_authority"],
            default_provider_activation=False,
        )
    except (OSError, UnicodeError, yaml.YAMLError, KeyError, TypeError, ValueError) as error:
        raise ValueError("CANONICAL_BAZI_RELATION_POLICY_INVALID") from error


def canonical_relation_identity(
    relation: BaziRelationFact,
) -> Tuple[str, Tuple[str, ...], str]:
    return relation.relation_type, relation.participant_refs, relation.rule_version


def validate_canonical_bazi_relations(
    facts: BaziChartFacts,
    policy: CanonicalBaziRelationPolicy,
) -> None:
    """Validate governed relations against actual chart subjects and rules.

    Empty collections and unrelated legacy relation families are intentionally
    outside this contract and remain backward compatible.
    """

    governed = [
        (index, relation)
        for index, relation in enumerate(facts.relations)
        if relation.relation_type == policy.relation_type
    ]
    if not governed:
        return

    subjects = _canonical_subject_catalog(facts, policy)
    identities = [canonical_relation_identity(item) for _, item in governed]
    if len(identities) != len(set(identities)):
        raise CanonicalBaziRelationError(
            "DUPLICATE_IDENTITY", "relations"
        )
    if identities != sorted(identities):
        raise CanonicalBaziRelationError("ORDER_INVALID", "relations")

    for index, relation in governed:
        field = f"relations.{index}"
        approved = policy.approved_rule_versions.get(relation.relation_type)
        if relation.rule_version != approved:
            raise CanonicalBaziRelationError(
                "RULE_VERSION_UNAPPROVED", f"{field}.rule_version"
            )
        if (
            len(relation.participant_refs) != 2
            or len(set(relation.participant_refs)) != 2
        ):
            raise CanonicalBaziRelationError(
                "PARTICIPANT_ARITY_INVALID", f"{field}.participant_refs"
            )
        try:
            controller = subjects[relation.participant_refs[0]]
            controlled = subjects[relation.participant_refs[1]]
        except KeyError as error:
            raise CanonicalBaziRelationError(
                "SUBJECT_REF_UNRESOLVED", f"{field}.participant_refs"
            ) from error
        expected_pillars = _ordered_pillars(
            controller[1], controlled[1]
        )
        if relation.source_pillars != expected_pillars:
            raise CanonicalBaziRelationError(
                "SOURCE_PILLARS_MISMATCH", f"{field}.source_pillars"
            )
        controller_element = policy.stem_elements[controller[0]]
        controlled_element = policy.stem_elements[controlled[0]]
        if policy.controls[controller_element] != controlled_element:
            raise CanonicalBaziRelationError(
                "CONTROL_TRUTH_MISMATCH", f"{field}.participant_refs"
            )


def _canonical_subject_catalog(
    facts: BaziChartFacts,
    policy: CanonicalBaziRelationPolicy,
) -> Mapping[str, Tuple[str, PillarPosition]]:
    pillars = {
        PillarPosition.YEAR: facts.year_pillar,
        PillarPosition.MONTH: facts.month_pillar,
        PillarPosition.DAY: facts.day_pillar,
    }
    if facts.hour_pillar is not None:
        pillars[PillarPosition.HOUR] = facts.hour_pillar

    hidden_by_pillar = {}
    for index, item in enumerate(facts.hidden_stems):
        if item.pillar in hidden_by_pillar:
            raise CanonicalBaziRelationError(
                "HIDDEN_STEM_PILLAR_DUPLICATE", f"hidden_stems.{index}.pillar"
            )
        hidden_by_pillar[item.pillar] = item.stems
    if set(hidden_by_pillar) != set(pillars):
        raise CanonicalBaziRelationError(
            "HIDDEN_STEM_COVERAGE_INVALID", "hidden_stems"
        )

    catalog = {}
    for position in PillarPosition:
        pillar = pillars.get(position)
        if pillar is None:
            continue
        if pillar.heavenly_stem not in policy.stem_elements:
            raise CanonicalBaziRelationError(
                "VISIBLE_STEM_UNRECOGNIZED",
                f"{position.value}_pillar.heavenly_stem",
            )
        expected = policy.hidden_stems.get(pillar.earthly_branch)
        actual = hidden_by_pillar[position]
        if expected is None or actual != expected:
            raise CanonicalBaziRelationError(
                "HIDDEN_STEM_ORDER_MISMATCH",
                f"hidden_stems.{position.value}",
            )
        catalog[
            policy.visible_stem_template.format(pillar=position.value)
        ] = (pillar.heavenly_stem, position)
        for hidden_index, stem in enumerate(actual):
            catalog[
                policy.hidden_stem_template.format(
                    pillar=position.value, index=hidden_index
                )
            ] = (stem, position)
    return catalog


def _ordered_pillars(
    first: PillarPosition, second: PillarPosition
) -> Tuple[PillarPosition, ...]:
    return tuple(
        position
        for position in PillarPosition
        if position == first or position == second
    )


def canonical_relation_policy_fingerprint(root: Optional[Path] = None) -> str:
    directory = Path(root) if root is not None else canonical_bazi_relation_asset_root()
    digest = sha256()
    for filename in ASSET_FILES:
        content = (directory / filename).read_bytes()
        digest.update(f"{filename}:".encode("utf-8"))
        digest.update(sha256(content).hexdigest().encode("ascii"))
        digest.update(b"\n")
    return digest.hexdigest()


def _load(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _mapping(value: object) -> dict:
    if type(value) is not dict:
        raise ValueError
    return value


def _list(value: object) -> list:
    if type(value) is not list:
        raise ValueError
    return value


def _exact_keys(value: Mapping[object, object], expected: set[str]) -> None:
    if set(value) != expected or any(type(key) is not str for key in value):
        raise ValueError


def _string(value: object) -> str:
    if type(value) is not str or not value.strip():
        raise ValueError
    return value


def _string_tuple(value: object) -> Tuple[str, ...]:
    values = _list(value)
    return tuple(_string(item) for item in values)


def _string_mapping(value: object) -> Mapping[str, str]:
    data = _mapping(value)
    return {_string(key): _string(item) for key, item in data.items()}
