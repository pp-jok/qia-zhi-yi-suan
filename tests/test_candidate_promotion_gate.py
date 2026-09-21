from pathlib import Path
from shutil import copytree

import yaml


def _copy_candidate_bundle(tmp_path: Path) -> Path:
    source = Path(__file__).resolve().parents[1] / "candidates" / "core-profile-v1"
    target = tmp_path / "core-profile-v1"
    copytree(source, target)
    return target


def _write_yaml(path: Path, value: dict) -> None:
    path.write_text(yaml.safe_dump(value, allow_unicode=True), encoding="utf-8")


def test_candidate_bundle_promotion_gate_removes_implemented_fact_blockers() -> None:
    from destiny_personality.core_profile_promotion import validate_candidate_bundle_technical_readiness, validate_candidate_promotion_authorization

    assert validate_candidate_bundle_technical_readiness() == ()
    assert validate_candidate_promotion_authorization() == ("HUMAN_PRODUCTION_APPROVAL_REQUIRED",)


def test_candidate_promotion_gate_rejects_incomplete_environment_table(tmp_path) -> None:
    from destiny_personality.core_profile_promotion import validate_candidate_bundle_for_promotion

    bundle_root = _copy_candidate_bundle(tmp_path)
    environment_path = bundle_root / "bazi_day_master_environment_v1.yaml"
    environment = yaml.safe_load(environment_path.read_text(encoding="utf-8"))
    environment["stem_elements"].pop("甲")
    _write_yaml(environment_path, environment)

    blockers = validate_candidate_bundle_for_promotion(bundle_root)

    assert "BAZI_DAY_MASTER_ENVIRONMENT_UNAVAILABLE" in blockers


def test_candidate_promotion_gate_requires_complete_rule_guards(tmp_path) -> None:
    from destiny_personality.core_profile_promotion import validate_candidate_bundle_for_promotion

    bundle_root = _copy_candidate_bundle(tmp_path)
    bazi_path = bundle_root / "bazi_mapping_registry_v1.yaml"
    bazi = yaml.safe_load(bazi_path.read_text(encoding="utf-8"))
    bazi["rules"][0].pop("allowed_source_kinds")
    _write_yaml(bazi_path, bazi)

    astrology_path = bundle_root / "astrology_mapping_registry_v1.yaml"
    astrology = yaml.safe_load(astrology_path.read_text(encoding="utf-8"))
    astrology["rules"][0].pop("house_context_any")
    _write_yaml(astrology_path, astrology)

    blockers = validate_candidate_bundle_for_promotion(bundle_root)

    assert "BAZI_VISIBLE_HIDDEN_PROVENANCE_UNAVAILABLE" in blockers
    assert "ASTROLOGY_ANGLE_HOUSE_BRANCH_UNIMPLEMENTED" in blockers
