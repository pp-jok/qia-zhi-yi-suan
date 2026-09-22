"""Deterministic JSON codec for externally calculated chart facts.

The codec deliberately transports facts only. It does not accept birth input or
invoke a chart calculation engine.
"""

from datetime import date, datetime
from decimal import Decimal
import json
from pathlib import Path
from typing import Mapping, Optional, Tuple

from .calculation.models import (
    AstrologyAspectFact,
    AstrologyChartFacts,
    AstrologyPlacement,
    BaziChartFacts,
    BaziPillar,
    BaziRelationFact,
    DeterministicChartFacts,
    DignityFact,
    FactMode,
    HiddenStemsFact,
    HouseCusp,
    NormalizedBirthTime,
    PillarPosition,
    TenGodFact,
    TenGodSourceKind,
    TimeBasis,
)


def deterministic_facts_to_dict(facts: DeterministicChartFacts) -> dict:
    return {
        "schema_version": "deterministic-chart-facts-v1",
        "normalized_time": {
            "birth_date": facts.normalized_time.birth_date.isoformat(),
            "historical_civil_time": _datetime_value(facts.normalized_time.historical_civil_time),
            "local_standard_time": _datetime_value(facts.normalized_time.local_standard_time),
            "utc_time": _datetime_value(facts.normalized_time.utc_time),
            "true_solar_time": _datetime_value(facts.normalized_time.true_solar_time),
            "timezone_name": facts.normalized_time.timezone_name,
            "dst_was_applied": facts.normalized_time.dst_was_applied,
            "time_basis": facts.normalized_time.time_basis.value,
            "fact_mode": facts.normalized_time.fact_mode.value,
            "sensitivity_reasons": list(facts.normalized_time.sensitivity_reasons),
        },
        "bazi": {
            "methodology_version": facts.bazi.methodology_version,
            "year_pillar": _pillar_dict(facts.bazi.year_pillar),
            "month_pillar": _pillar_dict(facts.bazi.month_pillar),
            "day_pillar": _pillar_dict(facts.bazi.day_pillar),
            "hour_pillar": _pillar_dict(facts.bazi.hour_pillar),
            "hidden_stems": [{"pillar": item.pillar.value, "stems": list(item.stems)} for item in facts.bazi.hidden_stems],
            "ten_gods": [{"subject_ref": item.subject_ref, "ten_god": item.ten_god, "source_pillars": [pillar.value for pillar in item.source_pillars], "source_kind": item.source_kind.value} for item in facts.bazi.ten_gods],
            "relations": [{"relation_type": item.relation_type, "participant_refs": list(item.participant_refs), "source_pillars": [pillar.value for pillar in item.source_pillars]} for item in facts.bazi.relations],
        },
        "astrology": {
            "methodology_version": facts.astrology.methodology_version,
            "placements": [{"body": item.body, "longitude": str(item.longitude), "sign": item.sign, "degree_in_sign": str(item.degree_in_sign), "house": item.house} for item in facts.astrology.placements],
            "aspects": [{"body_a": item.body_a, "body_b": item.body_b, "aspect_type": item.aspect_type, "orb": str(item.orb)} for item in facts.astrology.aspects],
            "ascendant": _decimal_value(facts.astrology.ascendant),
            "mc": _decimal_value(facts.astrology.mc),
            "house_cusps": [{"house": item.house, "longitude": str(item.longitude)} for item in facts.astrology.house_cusps],
            "dignities": [{"body": item.body, "dignity": item.dignity} for item in facts.astrology.dignities],
        },
    }


def deterministic_facts_from_dict(payload: Mapping[str, object]) -> DeterministicChartFacts:
    """Decode the internal chart-facts transport used by tests and adapters."""

    if payload.get("schema_version") != "deterministic-chart-facts-v1":
        raise ValueError("DETERMINISTIC_FACTS_SCHEMA_INVALID")
    try:
        normalized = payload["normalized_time"]
        bazi = payload["bazi"]
        astrology = payload["astrology"]
        return DeterministicChartFacts(
            normalized_time=NormalizedBirthTime(
                birth_date=date.fromisoformat(normalized["birth_date"]),
                historical_civil_time=_parse_datetime(normalized["historical_civil_time"]),
                local_standard_time=_parse_datetime(normalized["local_standard_time"]),
                utc_time=_parse_datetime(normalized["utc_time"]),
                true_solar_time=_parse_datetime(normalized["true_solar_time"]),
                timezone_name=normalized["timezone_name"], dst_was_applied=normalized["dst_was_applied"],
                time_basis=TimeBasis(normalized["time_basis"]), fact_mode=FactMode(normalized["fact_mode"]),
                sensitivity_reasons=tuple(normalized["sensitivity_reasons"]),
            ),
            bazi=BaziChartFacts(
                methodology_version=bazi["methodology_version"], year_pillar=_pillar(bazi["year_pillar"]),
                month_pillar=_pillar(bazi["month_pillar"]), day_pillar=_pillar(bazi["day_pillar"]), hour_pillar=_pillar(bazi["hour_pillar"]),
                hidden_stems=tuple(HiddenStemsFact(PillarPosition(item["pillar"]), tuple(item["stems"])) for item in bazi["hidden_stems"]),
                ten_gods=tuple(TenGodFact(item["subject_ref"], item["ten_god"], tuple(PillarPosition(value) for value in item["source_pillars"]), TenGodSourceKind(item["source_kind"])) for item in bazi["ten_gods"]),
                relations=tuple(BaziRelationFact(item["relation_type"], tuple(item["participant_refs"]), tuple(PillarPosition(value) for value in item["source_pillars"])) for item in bazi["relations"]),
            ),
            astrology=AstrologyChartFacts(
                methodology_version=astrology["methodology_version"],
                placements=tuple(AstrologyPlacement(item["body"], Decimal(item["longitude"]), item["sign"], Decimal(item["degree_in_sign"]), item["house"]) for item in astrology["placements"]),
                aspects=tuple(AstrologyAspectFact(item["body_a"], item["body_b"], item["aspect_type"], Decimal(item["orb"])) for item in astrology["aspects"]),
                ascendant=_decimal(astrology["ascendant"]), mc=_decimal(astrology["mc"]),
                house_cusps=tuple(HouseCusp(item["house"], Decimal(item["longitude"])) for item in astrology["house_cusps"]),
                dignities=tuple(DignityFact(item["body"], item["dignity"]) for item in astrology["dignities"]),
            ),
        )
    except (KeyError, TypeError, ValueError) as error:
        raise ValueError("DETERMINISTIC_FACTS_CONTRACT_INVALID") from error


def load_deterministic_facts(path: Path) -> DeterministicChartFacts:
    try:
        return deterministic_facts_from_dict(json.loads(path.read_text(encoding="utf-8")))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError("DETERMINISTIC_FACTS_JSON_INVALID") from error


def load_validated_deterministic_facts(path: Path) -> DeterministicChartFacts:
    """Load the public `deterministic-facts-v1` contract after qualification."""

    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError("DETERMINISTIC_FACTS_JSON_INVALID") from error
    _validate_qualification_envelope(payload)
    internal_payload = dict(payload)
    internal_payload["schema_version"] = "deterministic-chart-facts-v1"
    facts = deterministic_facts_from_dict(internal_payload)
    if payload["fact_mode"] != facts.normalized_time.fact_mode.value:
        raise ValueError("FACT_QUALIFICATION_INVALID")
    versions = payload["methodology_versions"]
    if versions["bazi"] != facts.bazi.methodology_version or versions["astrology"] != facts.astrology.methodology_version:
        raise ValueError("FACT_QUALIFICATION_INVALID")
    return facts


def _validate_qualification_envelope(payload: Mapping[str, object]) -> None:
    if payload.get("schema_version") != "deterministic-facts-v1":
        raise ValueError("DETERMINISTIC_FACTS_SCHEMA_INVALID")
    provenance = payload.get("provenance_refs")
    validation = payload.get("validation_summary")
    if not isinstance(provenance, list) or not provenance or not all(isinstance(ref, str) and ref for ref in provenance):
        raise ValueError("FACT_QUALIFICATION_REQUIRED")
    if not isinstance(validation, Mapping):
        raise ValueError("FACT_QUALIFICATION_REQUIRED")
    required_checks = (
        "structure", "methodology", "provenance", "internal_consistency",
        "time_scope", "independent_comparison",
    )
    if any(validation.get(check) != "passed" for check in required_checks):
        raise ValueError("FACT_QUALIFICATION_INVALID")
    versions = payload.get("methodology_versions")
    if not isinstance(versions, Mapping) or not isinstance(versions.get("bazi"), str) or not isinstance(versions.get("astrology"), str):
        raise ValueError("FACT_QUALIFICATION_INVALID")


def _pillar_dict(value: Optional[BaziPillar]) -> Optional[dict]:
    return None if value is None else {"heavenly_stem": value.heavenly_stem, "earthly_branch": value.earthly_branch}


def _pillar(value: Optional[Mapping[str, object]]) -> Optional[BaziPillar]:
    return None if value is None else BaziPillar(value["heavenly_stem"], value["earthly_branch"])


def _datetime_value(value: Optional[datetime]) -> Optional[str]:
    return None if value is None else value.isoformat()


def _parse_datetime(value: Optional[str]) -> Optional[datetime]:
    return None if value is None else datetime.fromisoformat(value)


def _decimal_value(value: Optional[Decimal]) -> Optional[str]:
    return None if value is None else str(value)


def _decimal(value: Optional[str]) -> Optional[Decimal]:
    return None if value is None else Decimal(value)
