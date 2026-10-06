"""Load the self-contained audited interpretive-rule bundle."""

from dataclasses import replace
from pathlib import Path
from typing import Any, Callable, Optional, Tuple

import yaml

from .interpretive_models import InterpretiveRuleBundle, InterpretiveSignal
from .deterministic_facts_codec import QualifiedFacts, require_qualified_facts
from .calculation.models import DeterministicChartFacts, FactMode


BUNDLE_VERSION = "audited-interpretive-rules-v1"
RULE_FILE = "interpretive_rules_v1.yaml"
CONFIDENCES = {"high", "moderate", "exploratory", "insufficient"}
SYSTEMS = {"bazi", "astrology"}
ROOT_KEYS = {"bundle_version", "limitations", "rules"}
RULE_KEYS = {
    "signal_id",
    "system",
    "fact_refs",
    "traditional_rule_ref",
    "topic",
    "direction",
    "interpretation",
    "confidence",
    "limitations",
}


FactPathResolver = Callable[[DeterministicChartFacts], Tuple[str, ...]]


def interpretive_rule_asset_root() -> Path:
    return Path(__file__).resolve().parent / "interpretive_assets" / "v1"


def _invalid(code: str) -> ValueError:
    return ValueError(code)


def _string(value: Any, code: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise _invalid(code)
    return value


def _strings(value: Any, code: str) -> Tuple[str, ...]:
    if not isinstance(value, list) or not value:
        raise _invalid(code)
    return tuple(_string(item, code) for item in value)


def _fact_refs(value: Any, system: str) -> Tuple[str, ...]:
    references = _strings(value, "INTERPRETIVE_RULE_INVALID_PROVENANCE")
    prefix = f"{system}."
    if any(not reference.startswith(prefix) or reference == prefix for reference in references):
        raise _invalid("INTERPRETIVE_RULE_INVALID_FACT_REF")
    return references


def _rule(value: Any) -> InterpretiveSignal:
    if not isinstance(value, dict) or set(value) != RULE_KEYS:
        raise _invalid("INTERPRETIVE_RULE_INVALID")
    confidence = _string(value["confidence"], "INTERPRETIVE_RULE_INVALID_CONFIDENCE")
    if confidence not in CONFIDENCES:
        raise _invalid("INTERPRETIVE_RULE_INVALID_CONFIDENCE")
    system = _string(value["system"], "INTERPRETIVE_RULE_INVALID")
    if system not in SYSTEMS:
        raise _invalid("INTERPRETIVE_RULE_INVALID")
    return InterpretiveSignal(
        signal_id=_string(value["signal_id"], "INTERPRETIVE_RULE_INVALID"),
        system=system,
        fact_refs=_fact_refs(value["fact_refs"], system),
        traditional_rule_ref=_string(
            value["traditional_rule_ref"], "INTERPRETIVE_RULE_INVALID_PROVENANCE"
        ),
        topic=_string(value["topic"], "INTERPRETIVE_RULE_INVALID"),
        direction=_string(value["direction"], "INTERPRETIVE_RULE_INVALID"),
        interpretation=_string(value["interpretation"], "INTERPRETIVE_RULE_INVALID"),
        confidence=confidence,
        limitations=_strings(value["limitations"], "INTERPRETIVE_RULE_INVALID"),
    )


def load_interpretive_rule_bundle(
    directory: Optional[Path] = None,
) -> InterpretiveRuleBundle:
    """Return the validated, versioned traditional interpretation contract."""

    root = Path(directory) if directory is not None else interpretive_rule_asset_root()
    path = root if root.suffix == ".yaml" else root / RULE_FILE
    try:
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as error:
        raise _invalid("INTERPRETIVE_RULE_INVALID") from error
    if not isinstance(payload, dict) or set(payload) != ROOT_KEYS:
        raise _invalid("INTERPRETIVE_RULE_INVALID")
    if payload["bundle_version"] != BUNDLE_VERSION:
        raise _invalid("INTERPRETIVE_RULE_INVALID_VERSION")
    limitations = _strings(payload["limitations"], "INTERPRETIVE_RULE_INVALID")
    raw_rules = payload["rules"]
    if not isinstance(raw_rules, list) or not raw_rules:
        raise _invalid("INTERPRETIVE_RULE_INVALID")
    rules = tuple(_rule(item) for item in raw_rules)
    if len({rule.signal_id for rule in rules}) != len(rules):
        raise _invalid("INTERPRETIVE_RULE_INVALID")
    if {rule.system for rule in rules} != SYSTEMS:
        raise _invalid("INTERPRETIVE_RULE_INVALID")
    return InterpretiveRuleBundle(BUNDLE_VERSION, rules, limitations)


def extract_interpretive_signals(
    qualified_facts: QualifiedFacts,
    bundle: Optional[InterpretiveRuleBundle] = None,
) -> Tuple[InterpretiveSignal, ...]:
    """Extract audited traditional signals from qualification-bound facts only."""

    facts = require_qualified_facts(qualified_facts).facts
    active_bundle = bundle if bundle is not None else load_interpretive_rule_bundle()
    signals = []
    for rule in active_bundle.rules:
        fact_refs = _matching_fact_paths(rule, facts)
        if fact_refs:
            signals.append(replace(rule, fact_refs=fact_refs))
    return tuple(signals)


def _matching_fact_paths(
    rule: InterpretiveSignal, facts: DeterministicChartFacts
) -> Optional[Tuple[str, ...]]:
    fact_paths = []
    for declared_ref in rule.fact_refs:
        resolver = _FACT_PATH_RESOLVERS.get(declared_ref)
        if resolver is None:
            return None
        matched_paths = resolver(facts)
        if not matched_paths:
            return None
        fact_paths.extend(matched_paths)
    return tuple(fact_paths)


def _ten_god_paths(facts: DeterministicChartFacts) -> Tuple[str, ...]:
    return tuple(
        f"bazi.ten_gods[{index}].ten_god"
        for index, _ in enumerate(facts.bazi.ten_gods)
    )


def _elemental_balance_paths(facts: DeterministicChartFacts) -> Tuple[str, ...]:
    paths = [
        "bazi.year_pillar",
        "bazi.month_pillar",
        "bazi.day_pillar",
    ]
    if facts.bazi.hour_pillar is not None:
        paths.append("bazi.hour_pillar")
    return tuple(paths)


def _relation_paths(facts: DeterministicChartFacts) -> Tuple[str, ...]:
    return tuple(
        f"bazi.relations[{index}].relation_type"
        for index, _ in enumerate(facts.bazi.relations)
    )


def _hidden_stem_paths(facts: DeterministicChartFacts) -> Tuple[str, ...]:
    return tuple(
        f"bazi.hidden_stems[{index}].stems"
        for index, _ in enumerate(facts.bazi.hidden_stems)
    )


def _planet_sign_paths(facts: DeterministicChartFacts) -> Tuple[str, ...]:
    return tuple(
        f"astrology.placements[{index}].sign"
        for index, _ in enumerate(facts.astrology.placements)
    )


def _house_placement_paths(facts: DeterministicChartFacts) -> Tuple[str, ...]:
    if facts.normalized_time.fact_mode is FactMode.STABLE_ONLY:
        return ()
    return tuple(
        f"astrology.placements[{index}].house"
        for index, placement in enumerate(facts.astrology.placements)
        if placement.house is not None
    )


def _aspect_paths(facts: DeterministicChartFacts) -> Tuple[str, ...]:
    return tuple(
        f"astrology.aspects[{index}].aspect_type"
        for index, _ in enumerate(facts.astrology.aspects)
    )


def _dignity_paths(facts: DeterministicChartFacts) -> Tuple[str, ...]:
    return tuple(
        f"astrology.dignities[{index}].dignity"
        for index, _ in enumerate(facts.astrology.dignities)
    )


_FACT_PATH_RESOLVERS: dict[str, FactPathResolver] = {
    "bazi.ten_god.day_master_relation": _ten_god_paths,
    "bazi.elemental_balance": _elemental_balance_paths,
    "bazi.branch_relation": _relation_paths,
    "bazi.hidden_stem": _hidden_stem_paths,
    "astrology.planet_sign": _planet_sign_paths,
    "astrology.house_placement": _house_placement_paths,
    "astrology.aspect": _aspect_paths,
    "astrology.essential_dignity": _dignity_paths,
}
