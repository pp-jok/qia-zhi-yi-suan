"""Load the self-contained audited interpretive-rule bundle."""

from dataclasses import replace
from pathlib import Path
from typing import Any, Callable, Optional, Tuple

import yaml

from .interpretive_models import (
    InterpretiveMatchedValue,
    InterpretiveRuleBundle,
    InterpretiveSignal,
    InterpretiveValuePredicate,
)
from .deterministic_facts_codec import QualifiedFacts, require_qualified_facts
from .calculation.models import DeterministicChartFacts, FactMode


BUNDLE_VERSION = "audited-interpretive-rules-v2"
PREDICATE_VERSION = "audited-interpretive-value-predicates-v2"
RULE_FILE = "interpretive_rules_v1.yaml"
CONFIDENCES = {"high", "moderate", "exploratory", "insufficient"}
SYSTEMS = {"bazi", "astrology"}
ROOT_KEYS = {"bundle_version", "predicate_version", "limitations", "rules"}
RULE_KEYS = {
    "signal_id",
    "family",
    "system",
    "fact_refs",
    "value_predicates",
    "traditional_rule_ref",
    "topic",
    "direction",
    "interpretation",
    "mechanism",
    "likely_expression",
    "contexts",
    "modifiers",
    "confidence",
    "limitations",
}


PredicateResolver = Callable[
    [DeterministicChartFacts, InterpretiveValuePredicate],
    Tuple[InterpretiveMatchedValue, ...],
]
PREDICATE_SELECTOR_KEYS = {
    "bazi.ten_god.day_master_relation": {
        "positions",
        "source_kinds",
        "minimum_occurrences",
    },
    "bazi.elemental_balance": set(),
    "bazi.branch_relation": {"positions", "participants", "minimum_occurrences"},
    "bazi.hidden_stem": {"positions", "minimum_occurrences"},
    "astrology.planet_sign": {"body"},
    "astrology.sign_element": {"body"},
    "astrology.sign_modality": {"body"},
    "astrology.house_placement": {"body"},
    "astrology.aspect": {"body", "other_body", "minimum_occurrences"},
    "astrology.essential_dignity": {"body"},
}
REQUIRED_PREDICATE_SELECTOR_KEYS = {
    "astrology.planet_sign": {"body"},
    "astrology.sign_element": {"body"},
    "astrology.sign_modality": {"body"},
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
    "astrology.sign_element": frozenset({"fire", "earth", "air", "water"}),
    "astrology.sign_modality": frozenset({"cardinal", "fixed", "mutable"}),
    "astrology.house_placement": frozenset(str(house) for house in range(1, 13)),
    "astrology.aspect": frozenset(
        {"conjunction", "opposition", "square", "trine", "sextile"}
    ),
    "astrology.essential_dignity": frozenset(
        {"domicile", "detriment", "exaltation", "fall"}
    ),
}
PILLAR_POSITIONS = frozenset({"year", "month", "day", "hour"})
BRANCH_PARTICIPANTS = frozenset(
    f"{position}.branch" for position in PILLAR_POSITIONS
)
TEN_GOD_SOURCE_KINDS = frozenset({"visible_stem", "hidden_stem", "unknown"})
ASTROLOGY_BODIES = frozenset(
    {"Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto"}
)
READER_VALUE_LABELS = {
    "astrology.sign_element": {
        "fire": "火象",
        "earth": "土象",
        "air": "风象",
        "water": "水象",
    },
    "astrology.sign_modality": {
        "cardinal": "开创",
        "fixed": "固定",
        "mutable": "变动",
    },
    "astrology.aspect": {
        "conjunction": "合相",
        "opposition": "对冲",
        "square": "刑相",
        "trine": "拱相",
        "sextile": "六合相",
    },
    "astrology.essential_dignity": {
        "domicile": "入庙",
        "detriment": "失势",
        "exaltation": "旺相",
        "fall": "落陷",
    },
}
READER_FACT_LABELS = {
    "astrology.sign_element": "元素",
    "astrology.sign_modality": "模式",
    "astrology.house_placement": "宫位",
    "astrology.aspect": "相位",
    "astrology.essential_dignity": "尊贵",
}


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


def _string_list(value: Any, code: str) -> Tuple[str, ...]:
    if not isinstance(value, list):
        raise _invalid(code)
    return tuple(_string(item, code) for item in value)


def _selector_values(
    item: dict[str, Any], key: str, domain: frozenset[str]
) -> Tuple[str, ...]:
    if key not in item:
        return ()
    values = _strings(item[key], "INTERPRETIVE_RULE_INVALID_PREDICATE")
    if not set(values).issubset(domain):
        raise _invalid("INTERPRETIVE_RULE_INVALID_PREDICATE_VALUE")
    return values


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
        allowed_selectors = PREDICATE_SELECTOR_KEYS.get(fact_ref)
        required_selectors = REQUIRED_PREDICATE_SELECTOR_KEYS.get(fact_ref, set())
        selector_keys = set(item) - {"fact_ref", "values"}
        if (
            fact_ref not in fact_refs
            or allowed_selectors is None
            or not required_selectors <= selector_keys <= allowed_selectors
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
        positions = _selector_values(item, "positions", PILLAR_POSITIONS)
        source_kinds = _selector_values(
            item, "source_kinds", TEN_GOD_SOURCE_KINDS
        )
        participants = _selector_values(
            item, "participants", BRANCH_PARTICIPANTS
        )
        minimum_occurrences = item.get("minimum_occurrences", 1)
        if (
            not set(values).issubset(PREDICATE_VALUE_DOMAINS[fact_ref])
            or (body is not None and body not in ASTROLOGY_BODIES)
            or (other_body is not None and other_body not in ASTROLOGY_BODIES)
            or (other_body is not None and body == other_body)
            or isinstance(minimum_occurrences, bool)
            or not isinstance(minimum_occurrences, int)
            or not 1 <= minimum_occurrences <= 10
        ):
            raise _invalid("INTERPRETIVE_RULE_INVALID_PREDICATE_VALUE")
        predicates.append(
            InterpretiveValuePredicate(
                fact_ref=fact_ref,
                values=values,
                body=body,
                other_body=other_body,
                positions=positions,
                source_kinds=source_kinds,
                participants=participants,
                minimum_occurrences=minimum_occurrences,
            )
        )
    if {predicate.fact_ref for predicate in predicates} != set(fact_refs):
        raise _invalid("INTERPRETIVE_RULE_INVALID_PREDICATE")
    if len({predicate.fact_ref for predicate in predicates}) != len(predicates):
        raise _invalid("INTERPRETIVE_RULE_INVALID_PREDICATE")
    return tuple(predicates)


def _rule(value: Any) -> InterpretiveSignal:
    if not isinstance(value, dict) or not RULE_KEYS <= set(value):
        raise _invalid("INTERPRETIVE_RULE_INVALID")
    confidence = _string(value["confidence"], "INTERPRETIVE_RULE_INVALID_CONFIDENCE")
    if confidence not in CONFIDENCES:
        raise _invalid("INTERPRETIVE_RULE_INVALID_CONFIDENCE")
    system = _string(value["system"], "INTERPRETIVE_RULE_INVALID")
    if system not in SYSTEMS:
        raise _invalid("INTERPRETIVE_RULE_INVALID")
    fact_refs = _fact_refs(value["fact_refs"], system)
    predicates = _value_predicates(value["value_predicates"], fact_refs)
    if _requires_exact_demo_chart(predicates):
        raise _invalid("INTERPRETIVE_RULE_DEMO_SPECIFIC")
    if set(value) != RULE_KEYS:
        raise _invalid("INTERPRETIVE_RULE_INVALID")
    return InterpretiveSignal(
        signal_id=_string(value["signal_id"], "INTERPRETIVE_RULE_INVALID"),
        system=system,
        fact_refs=fact_refs,
        value_predicates=predicates,
        traditional_rule_ref=_string(
            value["traditional_rule_ref"], "INTERPRETIVE_RULE_INVALID_PROVENANCE"
        ),
        topic=_string(value["topic"], "INTERPRETIVE_RULE_INVALID"),
        direction=_string(value["direction"], "INTERPRETIVE_RULE_INVALID"),
        interpretation=_string(value["interpretation"], "INTERPRETIVE_RULE_INVALID"),
        confidence=confidence,
        limitations=_strings(value["limitations"], "INTERPRETIVE_RULE_INVALID"),
        family=_string(value["family"], "INTERPRETIVE_RULE_INVALID"),
        mechanism=_string(value["mechanism"], "INTERPRETIVE_RULE_INVALID"),
        likely_expression=_string(
            value["likely_expression"], "INTERPRETIVE_RULE_INVALID"
        ),
        contexts=_strings(value["contexts"], "INTERPRETIVE_RULE_INVALID"),
        modifiers=_string_list(value["modifiers"], "INTERPRETIVE_RULE_INVALID"),
        requires_exact_demo_chart=False,
    )


def _requires_exact_demo_chart(
    predicates: Tuple[InterpretiveValuePredicate, ...],
) -> bool:
    """Reject exact-chart conjunctions from structure, not asset assertions."""

    fact_refs = {predicate.fact_ref for predicate in predicates}
    if len(fact_refs) > 1 and fact_refs != {
        "astrology.sign_element",
        "astrology.sign_modality",
    }:
        return True
    if any(
        predicate.fact_ref == "astrology.planet_sign"
        and len(predicate.values) == 1
        for predicate in predicates
    ):
        return True
    elements = {
        predicate.body: predicate
        for predicate in predicates
        if predicate.fact_ref == "astrology.sign_element"
    }
    modalities = {
        predicate.body: predicate
        for predicate in predicates
        if predicate.fact_ref == "astrology.sign_modality"
    }
    return any(
        len(element.values) == len(modalities[body].values) == 1
        for body, element in elements.items()
        if body in modalities
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
    covered_ten_gods = frozenset(
        value
        for rule in rules
        for predicate in rule.value_predicates
        if predicate.fact_ref == "bazi.ten_god.day_master_relation"
        for value in predicate.values
    )
    covered_planets = frozenset(
        body
        for rule in rules
        for predicate in rule.value_predicates
        for body in (predicate.body, predicate.other_body)
        if predicate.fact_ref.startswith("astrology.") and body is not None
    )
    return InterpretiveRuleBundle(
        BUNDLE_VERSION,
        rules,
        limitations,
        covered_ten_gods,
        covered_planets,
    )


def extract_interpretive_signals(
    qualified_facts: QualifiedFacts,
    bundle: Optional[InterpretiveRuleBundle] = None,
) -> Tuple[InterpretiveSignal, ...]:
    """Extract audited traditional signals from qualification-bound facts only."""

    facts = require_qualified_facts(qualified_facts).facts
    active_bundle = bundle if bundle is not None else load_interpretive_rule_bundle()
    signals = []
    for rule in active_bundle.rules:
        matched_values = _matching_values(rule, facts)
        if matched_values:
            fact_refs = tuple(
                dict.fromkeys(match.fact_path for match in matched_values)
            )
            signals.append(
                replace(
                    rule,
                    fact_refs=fact_refs,
                    matched_values=matched_values,
                    interpretation=_reader_visible_interpretation(
                        rule.interpretation, matched_values
                    ),
                )
            )
    return tuple(signals)


def _matching_values(
    rule: InterpretiveSignal, facts: DeterministicChartFacts
) -> Optional[Tuple[InterpretiveMatchedValue, ...]]:
    matches = []
    for predicate in rule.value_predicates:
        resolver = _PREDICATE_RESOLVERS.get(predicate.fact_ref)
        if resolver is None:
            return None
        predicate_matches = resolver(facts, predicate)
        if not predicate_matches:
            return None
        matches.extend(predicate_matches)
    return tuple(dict.fromkeys(matches))


def _match(
    predicate: InterpretiveValuePredicate,
    fact_path: str,
    value: str,
) -> InterpretiveMatchedValue:
    return InterpretiveMatchedValue(predicate.fact_ref, fact_path, value)


def _reader_visible_interpretation(
    interpretation: str,
    matched_values: Tuple[InterpretiveMatchedValue, ...],
) -> str:
    """Make every matched selector visible in the reader-facing rule text."""

    visible_values = tuple(
        dict.fromkeys(
            _reader_visible_value(match) for match in matched_values
        )
    )
    return f"{interpretation}（命中依据：{'；'.join(visible_values)}）"


def _reader_visible_value(match: InterpretiveMatchedValue) -> str:
    if match.fact_ref == "astrology.house_placement":
        value = f"第{match.value}宫"
    else:
        value = READER_VALUE_LABELS.get(match.fact_ref, {}).get(
            match.value, match.value
        )
    label = READER_FACT_LABELS.get(match.fact_ref)
    return f"{label}：{value}" if label else value


def _ten_god_paths(
    facts: DeterministicChartFacts, predicate: InterpretiveValuePredicate
) -> Tuple[InterpretiveMatchedValue, ...]:
    matches = tuple(
        _match(
            predicate,
            f"bazi.ten_gods[{index}].ten_god",
            fact.ten_god,
        )
        for index, fact in enumerate(facts.bazi.ten_gods)
        if (
            fact.ten_god in predicate.values
            and (
                not predicate.positions
                or set(predicate.positions).intersection(
                    position.value for position in fact.source_pillars
                )
            )
            and (
                not predicate.source_kinds
                or fact.source_kind.value in predicate.source_kinds
            )
        )
    )
    repeated_values = {
        value
        for value in predicate.values
        if sum(match.value == value for match in matches)
        >= predicate.minimum_occurrences
    }
    return tuple(match for match in matches if match.value in repeated_values)


def _elemental_balance_paths(
    facts: DeterministicChartFacts, predicate: InterpretiveValuePredicate
) -> Tuple[InterpretiveMatchedValue, ...]:
    pillars = {
        "year": ("bazi.year_pillar", facts.bazi.year_pillar),
        "month": ("bazi.month_pillar", facts.bazi.month_pillar),
        "day": ("bazi.day_pillar", facts.bazi.day_pillar),
        "hour": ("bazi.hour_pillar", facts.bazi.hour_pillar),
    }
    return tuple(
        _match(predicate, pillars[position][0], position)
        for position in predicate.values
        if position in pillars and pillars[position][1] is not None
    )


def _relation_paths(
    facts: DeterministicChartFacts, predicate: InterpretiveValuePredicate
) -> Tuple[InterpretiveMatchedValue, ...]:
    matches = tuple(
        _match(
            predicate,
            f"bazi.relations[{index}].relation_type",
            fact.relation_type,
        )
        for index, fact in enumerate(facts.bazi.relations)
        if (
            fact.relation_type in predicate.values
            and (
                not predicate.positions
                or set(predicate.positions).intersection(
                    position.value for position in fact.source_pillars
                )
            )
            and (
                not predicate.participants
                or set(predicate.participants).intersection(fact.participant_refs)
            )
        )
    )
    return matches if len(matches) >= predicate.minimum_occurrences else ()


def _hidden_stem_paths(
    facts: DeterministicChartFacts, predicate: InterpretiveValuePredicate
) -> Tuple[InterpretiveMatchedValue, ...]:
    matches = tuple(
        _match(predicate, f"bazi.hidden_stems[{index}].stems", stem)
        for index, fact in enumerate(facts.bazi.hidden_stems)
        for stem in fact.stems
        if stem in predicate.values
        and (not predicate.positions or fact.pillar.value in predicate.positions)
    )
    return matches if len(matches) >= predicate.minimum_occurrences else ()


def _planet_sign_paths(
    facts: DeterministicChartFacts, predicate: InterpretiveValuePredicate
) -> Tuple[InterpretiveMatchedValue, ...]:
    return tuple(
        _match(predicate, f"astrology.placements[{index}].sign", fact.sign)
        for index, fact in enumerate(facts.astrology.placements)
        if fact.body == predicate.body and fact.sign in predicate.values
    )


_SIGN_ELEMENTS = {
    "Aries": "fire", "Leo": "fire", "Sagittarius": "fire",
    "Taurus": "earth", "Virgo": "earth", "Capricorn": "earth",
    "Gemini": "air", "Libra": "air", "Aquarius": "air",
    "Cancer": "water", "Scorpio": "water", "Pisces": "water",
}
_SIGN_MODALITIES = {
    "Aries": "cardinal", "Cancer": "cardinal", "Libra": "cardinal", "Capricorn": "cardinal",
    "Taurus": "fixed", "Leo": "fixed", "Scorpio": "fixed", "Aquarius": "fixed",
    "Gemini": "mutable", "Virgo": "mutable", "Sagittarius": "mutable", "Pisces": "mutable",
}


def _sign_quality_paths(
    facts: DeterministicChartFacts,
    predicate: InterpretiveValuePredicate,
    qualities: dict[str, str],
) -> Tuple[InterpretiveMatchedValue, ...]:
    return tuple(
        _match(
            predicate,
            f"astrology.placements[{index}].sign",
            qualities[fact.sign],
        )
        for index, fact in enumerate(facts.astrology.placements)
        if fact.body == predicate.body and qualities.get(fact.sign) in predicate.values
    )


def _sign_element_paths(
    facts: DeterministicChartFacts, predicate: InterpretiveValuePredicate
) -> Tuple[InterpretiveMatchedValue, ...]:
    return _sign_quality_paths(facts, predicate, _SIGN_ELEMENTS)


def _sign_modality_paths(
    facts: DeterministicChartFacts, predicate: InterpretiveValuePredicate
) -> Tuple[InterpretiveMatchedValue, ...]:
    return _sign_quality_paths(facts, predicate, _SIGN_MODALITIES)


def _house_placement_paths(
    facts: DeterministicChartFacts, predicate: InterpretiveValuePredicate
) -> Tuple[InterpretiveMatchedValue, ...]:
    if facts.normalized_time.fact_mode is FactMode.STABLE_ONLY:
        return ()
    return tuple(
        _match(
            predicate,
            f"astrology.placements[{index}].house",
            str(placement.house),
        )
        for index, placement in enumerate(facts.astrology.placements)
        if (
            placement.body == predicate.body
            and placement.house is not None
            and str(placement.house) in predicate.values
        )
    )


def _aspect_paths(
    facts: DeterministicChartFacts, predicate: InterpretiveValuePredicate
) -> Tuple[InterpretiveMatchedValue, ...]:
    matches = tuple(
        _match(
            predicate,
            f"astrology.aspects[{index}].aspect_type",
            fact.aspect_type,
        )
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
    return matches if len(matches) >= predicate.minimum_occurrences else ()


def _dignity_paths(
    facts: DeterministicChartFacts, predicate: InterpretiveValuePredicate
) -> Tuple[InterpretiveMatchedValue, ...]:
    return tuple(
        _match(
            predicate,
            f"astrology.dignities[{index}].dignity",
            fact.dignity,
        )
        for index, fact in enumerate(facts.astrology.dignities)
        if fact.body == predicate.body and fact.dignity in predicate.values
    )


_PREDICATE_RESOLVERS: dict[str, PredicateResolver] = {
    "bazi.ten_god.day_master_relation": _ten_god_paths,
    "bazi.elemental_balance": _elemental_balance_paths,
    "bazi.branch_relation": _relation_paths,
    "bazi.hidden_stem": _hidden_stem_paths,
    "astrology.planet_sign": _planet_sign_paths,
    "astrology.sign_element": _sign_element_paths,
    "astrology.sign_modality": _sign_modality_paths,
    "astrology.house_placement": _house_placement_paths,
    "astrology.aspect": _aspect_paths,
    "astrology.essential_dignity": _dignity_paths,
}
