from dataclasses import replace
from pathlib import Path
import shutil

import pytest
import yaml

from destiny_personality.calculation import BaziRelationFact, PillarPosition
from destiny_personality.canonical_bazi_relations import (
    canonical_bazi_relation_asset_root,
    canonical_relation_identity,
    canonical_relation_policy_fingerprint,
    load_canonical_bazi_relation_policy,
)


EXPECTED_HIDDEN_STEMS = {
    "子": ("癸",),
    "丑": ("己", "癸", "辛"),
    "寅": ("甲", "丙", "戊"),
    "卯": ("乙",),
    "辰": ("戊", "乙", "癸"),
    "巳": ("丙", "戊", "庚"),
    "午": ("丁", "己"),
    "未": ("己", "丁", "乙"),
    "申": ("庚", "壬", "戊"),
    "酉": ("辛",),
    "戌": ("戊", "辛", "丁"),
    "亥": ("壬", "甲"),
}


def test_canonical_policy_governs_hidden_order_subject_refs_and_relation_identity() -> None:
    policy = load_canonical_bazi_relation_policy()

    assert policy.hidden_stem_order_version == "bazi-hidden-stem-order-v1"
    assert policy.subject_ref_contract_version == "bazi-subject-ref-v1"
    assert policy.relation_contract_version == "bazi-relation-canonical-v1"
    assert policy.family_id == "deterministic_facts.bazi.relations"
    assert policy.hidden_stems == EXPECTED_HIDDEN_STEMS
    assert policy.pillars == ("year", "month", "day", "hour")
    assert policy.visible_stem_template == "{pillar}.stem"
    assert policy.hidden_stem_template == "{pillar}.hidden_stem.{index}"
    assert policy.source_kinds == {
        "visible_stem": "visible_stem",
        "hidden_stem": "hidden_stem",
    }
    assert policy.approved_rule_versions == {
        "five_element_controls": "wuxing-control-v1"
    }
    assert policy.identity_fields == (
        "relation_type",
        "participant_refs",
        "rule_version",
    )
    assert policy.provenance_fields == ("source_pillars",)
    assert policy.ordering_fields == policy.identity_fields
    assert policy.provider_authority == "conformance_reference_only"
    assert policy.default_provider_activation is False


def test_canonical_contract_excludes_methodology_and_semantic_fields() -> None:
    policy = load_canonical_bazi_relation_policy()

    assert {
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
    }.issubset(policy.prohibited_fields)


def test_relation_identity_excludes_source_pillar_provenance() -> None:
    first = BaziRelationFact(
        "five_element_controls",
        ("year.stem", "month.stem"),
        (PillarPosition.YEAR, PillarPosition.MONTH),
        "wuxing-control-v1",
    )
    different_provenance = replace(
        first, source_pillars=(PillarPosition.MONTH, PillarPosition.YEAR)
    )

    assert canonical_relation_identity(first) == canonical_relation_identity(
        different_provenance
    )
    assert canonical_relation_identity(first) == (
        "five_element_controls",
        ("year.stem", "month.stem"),
        "wuxing-control-v1",
    )


def test_canonical_policy_fingerprint_covers_all_three_assets(tmp_path: Path) -> None:
    source = canonical_bazi_relation_asset_root()
    copied = tmp_path / "calculation-v1"
    shutil.copytree(source, copied)

    original = canonical_relation_policy_fingerprint(copied)
    relation_path = copied / "bazi_relation_canonical_contract_v1.yaml"
    payload = yaml.safe_load(relation_path.read_text(encoding="utf-8"))
    payload["contract_version"] = "changed"
    relation_path.write_text(
        yaml.safe_dump(payload, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )

    assert len(original) == 64
    assert canonical_relation_policy_fingerprint(copied) != original


def test_canonical_policy_rejects_incomplete_hidden_stem_table(tmp_path: Path) -> None:
    source = canonical_bazi_relation_asset_root()
    copied = tmp_path / "calculation-v1"
    shutil.copytree(source, copied)
    path = copied / "bazi_hidden_stem_order_v1.yaml"
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    payload["branches"].pop("亥")
    path.write_text(
        yaml.safe_dump(payload, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="CANONICAL_BAZI_RELATION_POLICY_INVALID"):
        load_canonical_bazi_relation_policy(copied)


def test_candidate_contract_is_retained_as_historical_transition_record() -> None:
    path = (
        Path(__file__).resolve().parents[1]
        / "candidates"
        / "calculation-v1"
        / "bazi_neutral_relation_contract_v1.yaml"
    )
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))

    assert payload["review_status"] == "historical_superseded"
    assert payload["activation_status"] == "inactive"
    assert payload["implementation_status"] == (
        "superseded_by_bazi_relation_canonical_v1"
    )
