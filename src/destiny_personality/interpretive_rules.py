"""Load the self-contained audited interpretive-rule bundle."""

from pathlib import Path
from typing import Any, Optional, Tuple

import yaml

from .interpretive_models import InterpretiveRuleBundle, InterpretiveSignal


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
        fact_refs=_strings(value["fact_refs"], "INTERPRETIVE_RULE_INVALID_PROVENANCE"),
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
