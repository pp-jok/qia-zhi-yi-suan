"""Load the self-contained audited interpretive-rule bundle."""

from dataclasses import replace
from pathlib import Path
from typing import Any, Callable, Optional, Tuple

import yaml

from .interpretive_models import (
    InterpretiveRuleBundle,
    InterpretiveSignal,
    InterpretiveValuePredicate,
)
from .deterministic_facts_codec import QualifiedFacts, require_qualified_facts
from .calculation.models import DeterministicChartFacts, FactMode


BUNDLE_VERSION = "audited-interpretive-rules-v1"
PREDICATE_VERSION = "audited-interpretive-value-predicates-v1"
RULE_FILE = "interpretive_rules_v1.yaml"
CONFIDENCES = {"high", "moderate", "exploratory", "insufficient"}
SYSTEMS = {"bazi", "astrology"}
ROOT_KEYS = {"bundle_version", "predicate_version", "limitations", "rules"}
RULE_KEYS = {
    "signal_id",
    "system",
    "fact_refs",
    "value_predicates",
    "traditional_rule_ref",
    "topic",
    "direction",
    "interpretation",
    "confidence",
    "limitations",
}


FactPathResolver = Callable[
    [DeterministicChartFacts, InterpretiveValuePredicate], Tuple[str, ...]
]
PREDICATE_KEYS = {"fact_ref", "values", "body", "other_body"}
PREDICATE_SELECTOR_KEYS = {
    "bazi.ten_god.day_master_relation": set(),
    "bazi.elemental_balance": set(),
    "bazi.branch_relation": set(),
    "bazi.hidden_stem": set(),
    "astrology.planet_sign": {"body"},
    "astrology.house_placement": {"body"},
    "astrology.aspect": {"body", "other_body"},
    "astrology.essential_dignity": {"body"},
}
PREDICATE_VALUE_DOMAINS = {
    "bazi.ten_god.day_master_relation": frozenset(
        {"比肩", "劫财", "食神", "伤官", "正财", "偏财", "正官", "七杀", "正印", "偏印"}
    ),
    "bazi.elemental_balance": frozenset({"year", "month", "day", "hour"}),
    "bazi.branch_relation": frozenset(
        {"combination", "clash", "harm", "punishment", "five_element_controls"}
    ),
    "bazi.hidden_stem": frozenset("甲乙丙丁戊己庚辛壬癸"),
    "astrology.planet_sign": frozenset(
        {
            "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
            "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
        }
    ),
    "astrology.house_placement": frozenset(str(house) for house in range(1, 13)),
    "astrology.aspect": frozenset(
        {"conjunction", "opposition", "square", "trine", "sextile"}
    ),
    "astrology.essential_dignity": frozenset(
        {"domicile", "detriment", "exaltation", "fall"}
    ),
}
ASTROLOGY_BODIES = frozenset(
    {"Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto"}
)


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


def _value_predicates(
    value: Any, fact_refs: Tuple[str, ...]
) -> Tuple[InterpretiveValuePredicate, ...]:
    if not isinstance(value, list) or not value:
        raise _invalid("INTERPRETIVE_RULE_INVALID_PREDICATE")
    predicates = []
    for item in value:
        if not isinstance(item, dict) or not {"fact_ref", "values"} <= set(item):
            raise _invalid("INTERPRETIVE_RULE_INVALID_PREDICATE")
        fact_ref = _string(item["fact_ref"], "INTERPRETIVE_RULE_INVALID_PREDICATE")
        expected_selectors = PREDICATE_SELECTOR_KEYS.get(fact_ref)
        selector_keys = set(item) - {"fact_ref", "values"}
        if (
            fact_ref not in fact_refs
            or expected_selectors is None
            or selector_keys != expected_selectors
            or set(item) - {"fact_ref", "values", "body", "other_body"}
        ):
            raise _invalid("INTERPRETIVE_RULE_INVALID_PREDICATE")
        values = _strings(item["values"], "INTERPRETIVE_RULE_INVALID_PREDICATE")
        body = (
            _string(item["body"], "INTERPRETIVE_RULE_INVALID_PREDICATE")
            if "body" in item
            else None
        )
        other_body = (
            _string(item["other_body"], "INTERPRETIVE_RULE_INVALID_PREDICATE")
            if "other_body" in item
            else None
        )
        if (
            not set(values).issubset(PREDICATE_VALUE_DOMAINS[fact_ref])
            or (body is not None and body not in ASTROLOGY_BODIES)
            or (other_body is not None and other_body not in ASTROLOGY_BODIES)
            or (other_body is not None and body == other_body)
        ):
            raise _invalid("INTERPRETIVE_RULE_INVALID_PREDICATE_VALUE")
        predicates.append(InterpretiveValuePredicate(fact_ref, values, body, other_body))
    if {predicate.fact_ref for predicate in predicates} != set(fact_refs):
        raise _invalid("INTERPRETIVE_RULE_INVALID_PREDICATE")
    if len({predicate.fact_ref for predicate in predicates}) != len(predicates):
        raise _invalid("INTERPRETIVE_RULE_INVALID_PREDICATE")
    return tuple(predicates)


def _rule(value: Any) -> InterpretiveSignal:
    if not isinstance(value, dict) or set(value) != RULE_KEYS:
        raise _invalid("INTERPRETIVE_RULE_INVALID")
    confidence = _string(value["confidence"], "INTERPRETIVE_RULE_INVALID_CONFIDENCE")
    if confidence not in CONFIDENCES:
        raise _invalid("INTERPRETIVE_RULE_INVALID_CONFIDENCE")
    system = _string(value["system"], "INTERPRETIVE_RULE_INVALID")
    if system not in SYSTEMS:
        raise _invalid("INTERPRETIVE_RULE_INVALID")
    fact_refs = _fact_refs(value["fact_refs"], system)
    return InterpretiveSignal(
        signal_id=_string(value["signal_id"], "INTERPRETIVE_RULE_INVALID"),
        system=system,
        fact_refs=fact_refs,
        value_predicates=_value_predicates(value["value_predicates"], fact_refs),
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
    if payload["predicate_version"] != PREDICATE_VERSION:
        raise _invalid("INTERPRETIVE_RULE_INVALID_PREDICATE_VERSION")
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
    for predicate in rule.value_predicates:
        resolver = _FACT_PATH_RESOLVERS.get(predicate.fact_ref)
        if resolver is None:
            return None
        matched_paths = resolver(facts, predicate)
        if not matched_paths:
            return None
        fact_paths.extend(matched_paths)
    return tuple(fact_paths)


def _ten_god_paths(
    facts: DeterministicChartFacts, predicate: InterpretiveValuePredicate
) -> Tuple[str, ...]:
    return tuple(
        f"bazi.ten_gods[{index}].ten_god"
        for index, fact in enumerate(facts.bazi.ten_gods)
        if fact.ten_god in predicate.values
    )


def _elemental_balance_paths(
    facts: DeterministicChartFacts, predicate: InterpretiveValuePredicate
) -> Tuple[str, ...]:
    pillars = {
        "year": ("bazi.year_pillar", facts.bazi.year_pillar),
        "month": ("bazi.month_pillar", facts.bazi.month_pillar),
        "day": ("bazi.day_pillar", facts.bazi.day_pillar),
        "hour": ("bazi.hour_pillar", facts.bazi.hour_pillar),
    }
    return tuple(
        pillars[position][0]
        for position in predicate.values
        if position in pillars and pillars[position][1] is not None
    )


def _relation_paths(
    facts: DeterministicChartFacts, predicate: InterpretiveValuePredicate
) -> Tuple[str, ...]:
    return tuple(
        f"bazi.relations[{index}].relation_type"
        for index, fact in enumerate(facts.bazi.relations)
        if fact.relation_type in predicate.values
    )


def _hidden_stem_paths(
    facts: DeterministicChartFacts, predicate: InterpretiveValuePredicate
) -> Tuple[str, ...]:
    return tuple(
        f"bazi.hidden_stems[{index}].stems"
        for index, fact in enumerate(facts.bazi.hidden_stems)
        if set(fact.stems).intersection(predicate.values)
    )


def _planet_sign_paths(
    facts: DeterministicChartFacts, predicate: InterpretiveValuePredicate
) -> Tuple[str, ...]:
    return tuple(
        f"astrology.placements[{index}].sign"
        for index, fact in enumerate(facts.astrology.placements)
        if fact.body == predicate.body and fact.sign in predicate.values
    )


def _house_placement_paths(
    facts: DeterministicChartFacts, predicate: InterpretiveValuePredicate
) -> Tuple[str, ...]:
    if facts.normalized_time.fact_mode is FactMode.STABLE_ONLY:
        return ()
    return tuple(
        f"astrology.placements[{index}].house"
        for index, placement in enumerate(facts.astrology.placements)
        if (
            placement.body == predicate.body
            and placement.house is not None
            and str(placement.house) in predicate.values
        )
    )


def _aspect_paths(
    facts: DeterministicChartFacts, predicate: InterpretiveValuePredicate
) -> Tuple[str, ...]:
    return tuple(
        f"astrology.aspects[{index}].aspect_type"
        for index, fact in enumerate(facts.astrology.aspects)
        if (
            (
                fact.body_a == predicate.body and fact.body_b == predicate.other_body
            )
            or (
                fact.body_a == predicate.other_body and fact.body_b == predicate.body
            )
        )
        and fact.aspect_type in predicate.values
    )


def _dignity_paths(
    facts: DeterministicChartFacts, predicate: InterpretiveValuePredicate
) -> Tuple[str, ...]:
    return tuple(
        f"astrology.dignities[{index}].dignity"
        for index, fact in enumerate(facts.astrology.dignities)
        if fact.body == predicate.body and fact.dignity in predicate.values
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
