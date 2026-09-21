from pathlib import Path
from typing import Dict, Optional, Tuple

import yaml

from .candidate_assets import candidate_asset_root


_REQUIRED_STEMS = frozenset("甲乙丙丁戊己庚辛壬癸")
_REQUIRED_MONTH_BRANCHES = frozenset("寅卯辰巳午未申酉戌亥子丑")
_REQUIRED_SOURCE_KINDS = {"visible_stem", "hidden_stem"}


def validate_candidate_bundle_for_promotion(
    candidate_root: Optional[Path] = None,
) -> Tuple[str, ...]:
    """Return explicit blockers before any candidate semantic asset is promoted."""

    assets = _load_candidate_assets(candidate_root or _default_candidate_root())
    bazi = assets.get("bazi_mapping_registry_v1.yaml")
    astrology = assets.get("astrology_mapping_registry_v1.yaml")
    environment = assets.get("bazi_day_master_environment_v1.yaml")
    taxonomy = assets.get("context_taxonomy_v1.yaml")
    weighting = assets.get("candidate_evidence_weighting_policy_v1.yaml")
    blockers = []
    if not assets or any(asset.get("review_status") != "approved" for asset in assets.values()):
        blockers.append("CANDIDATE_REVIEW_PENDING")
    if not _environment_is_complete(environment):
        blockers.append("BAZI_DAY_MASTER_ENVIRONMENT_UNAVAILABLE")
    if not _bazi_provenance_is_complete(bazi):
        blockers.append("BAZI_VISIBLE_HIDDEN_PROVENANCE_UNAVAILABLE")
    if not _astrology_dignity_modifier_is_complete(astrology):
        blockers.append("ASTROLOGY_DIGNITY_MODIFIER_UNIMPLEMENTED")
    if not _astrology_angle_house_modifier_is_complete(astrology):
        blockers.append("ASTROLOGY_ANGLE_HOUSE_BRANCH_UNIMPLEMENTED")
    if not _context_taxonomy_is_complete(taxonomy, bazi, astrology):
        blockers.append("CANDIDATE_CONTEXT_TAXONOMY_UNAVAILABLE")
    if not _weighting_policy_is_complete(weighting):
        blockers.append("CANDIDATE_EVIDENCE_WEIGHTING_POLICY_UNAVAILABLE")
    return tuple(blockers)


def _default_candidate_root() -> Path:
    return candidate_asset_root()


def _load_candidate_assets(candidate_root: Path) -> Dict[str, dict]:
    assets = {}
    for path in candidate_root.glob("*.yaml"):
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
        if isinstance(value, dict):
            assets[path.name] = value
    return assets


def _environment_is_complete(environment: object) -> bool:
    if not isinstance(environment, dict):
        return False
    return _complete_mapping(environment.get("stem_elements"), _REQUIRED_STEMS) and _complete_mapping(
        environment.get("month_branch_seasons"), _REQUIRED_MONTH_BRANCHES
    )


def _complete_mapping(value: object, required_keys: frozenset) -> bool:
    return (
        isinstance(value, dict)
        and required_keys.issubset(value)
        and all(isinstance(value[key], str) and value[key].strip() for key in required_keys)
    )


def _bazi_provenance_is_complete(bazi: object) -> bool:
    if not isinstance(bazi, dict) or not isinstance(bazi.get("rules"), list):
        return False
    rules = bazi["rules"]
    return bool(rules) and all(
        isinstance(rule, dict)
        and isinstance(rule.get("minimum_distinct_pillars"), int)
        and rule["minimum_distinct_pillars"] >= 2
        and isinstance(rule.get("allowed_source_kinds"), list)
        and _REQUIRED_SOURCE_KINDS.issubset(set(rule["allowed_source_kinds"]))
        and rule.get("requires_day_master_environment") is True
        and isinstance(rule.get("contexts"), list)
        and bool(rule["contexts"])
        and isinstance(rule.get("environment_effect"), str)
        for rule in rules
    )


def _astrology_dignity_modifier_is_complete(astrology: object) -> bool:
    return any(
        _nonempty_string_list(rule.get("dignity_modifier_any"))
        for rule in _astrology_rules(astrology)
    )


def _astrology_angle_house_modifier_is_complete(astrology: object) -> bool:
    return any(
        _nonempty_string_list(rule.get("angular_body_any"))
        and _nonempty_list(rule.get("house_context_any"))
        for rule in _astrology_rules(astrology)
    )


def _astrology_rules(astrology: object) -> Tuple[dict, ...]:
    if not isinstance(astrology, dict) or not isinstance(astrology.get("rules"), list):
        return ()
    return tuple(rule for rule in astrology["rules"] if isinstance(rule, dict))


def _nonempty_string_list(value: object) -> bool:
    return isinstance(value, list) and bool(value) and all(
        isinstance(item, str) and item.strip() for item in value
    )


def _nonempty_list(value: object) -> bool:
    return isinstance(value, list) and bool(value)


def _context_taxonomy_is_complete(taxonomy: object, bazi: object, astrology: object) -> bool:
    if not isinstance(taxonomy, dict) or not isinstance(taxonomy.get("contexts"), list):
        return False
    allowed = set(taxonomy["contexts"])
    if not allowed or not isinstance(taxonomy.get("comparison_policy"), dict):
        return False
    bazi_rules = bazi.get("rules", ()) if isinstance(bazi, dict) else ()
    return all(
        isinstance(rule.get("contexts"), list)
        and bool(rule["contexts"])
        and set(rule["contexts"]).issubset(allowed)
        for rule in tuple(bazi_rules) + _astrology_rules(astrology)
    )


def _weighting_policy_is_complete(weighting: object) -> bool:
    if not isinstance(weighting, dict):
        return False
    bands = weighting.get("astrology", {}).get("orb_bands")
    return (
        isinstance(bands, dict)
        and bool(bands)
        and all(isinstance(value, dict) and isinstance(value.get("max_orb"), int) for value in bands.values())
        and isinstance(weighting.get("bazi", {}).get("default_salience"), str)
    )
