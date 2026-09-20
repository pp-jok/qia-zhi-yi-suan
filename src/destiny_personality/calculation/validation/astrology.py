from decimal import Decimal

from destiny_personality.config_models import RuntimeConfig

from ..errors import CalculationError
from ..models import (
    AstrologyAspectFact,
    AstrologyChartFacts,
    AstrologyPlacement,
    DignityFact,
    FactMode,
    HouseCusp,
)
from .common import (
    contract_error,
    validate_decimal_range,
    validate_nonempty_string,
)


def validate_astrology_facts(
    facts: AstrologyChartFacts, fact_mode: FactMode, config: RuntimeConfig
) -> None:
    if type(facts) is not AstrologyChartFacts:
        raise contract_error(
            "astrology", "backend must return AstrologyChartFacts"
        )
    methodology = config.astrology
    if facts.methodology_version != methodology.methodology_version:
        raise CalculationError(
            "METHODOLOGY_VERSION_MISMATCH",
            "astrology methodology version does not match runtime config",
            system="astrology",
            field="methodology_version",
        )

    _validate_collection(facts.placements, AstrologyPlacement, "placements")
    expected_planets = set(methodology.bodies.planets)
    seen_planets = set()
    for index, placement in enumerate(facts.placements):
        prefix = f"placements.{index}"
        if placement.body not in expected_planets:
            raise contract_error(
                "astrology", "unknown configured planet", f"{prefix}.body"
            )
        if placement.body in seen_planets:
            raise contract_error(
                "astrology", "duplicate planet placement", f"{prefix}.body"
            )
        seen_planets.add(placement.body)
        validate_decimal_range(
            placement.longitude,
            Decimal("0"),
            Decimal("360"),
            "astrology",
            f"{prefix}.longitude",
        )
        validate_nonempty_string(
            placement.sign, "astrology", f"{prefix}.sign"
        )
        validate_decimal_range(
            placement.degree_in_sign,
            Decimal("0"),
            Decimal("30"),
            "astrology",
            f"{prefix}.degree_in_sign",
        )
        if fact_mode is FactMode.STABLE_ONLY:
            if placement.house is not None:
                raise contract_error(
                    "astrology",
                    "stable-only placement cannot include a house",
                    f"{prefix}.house",
                )
        elif type(placement.house) is not int or not 1 <= placement.house <= 12:
            raise contract_error(
                "astrology",
                "house must be an integer from 1 to 12",
                f"{prefix}.house",
            )
    if seen_planets != expected_planets:
        raise contract_error(
            "astrology",
            "placements must contain every configured planet",
            "placements",
        )

    _validate_angles_and_cusps(facts, fact_mode)
    _validate_aspects(facts, fact_mode, config)
    _validate_dignities(facts, config)


def _validate_collection(value: object, item_type: type, field: str) -> None:
    if type(value) is not tuple:
        raise contract_error("astrology", "collection must be a tuple", field)
    for index, item in enumerate(value):
        if type(item) is not item_type:
            raise contract_error(
                "astrology", f"invalid {item_type.__name__}", f"{field}.{index}"
            )


def _validate_optional_longitude(value: object, field: str) -> None:
    validate_decimal_range(
        value, Decimal("0"), Decimal("360"), "astrology", field
    )


def _validate_angles_and_cusps(
    facts: AstrologyChartFacts, fact_mode: FactMode
) -> None:
    _validate_collection(facts.house_cusps, HouseCusp, "house_cusps")
    if fact_mode is FactMode.STABLE_ONLY:
        if facts.ascendant is not None:
            raise contract_error(
                "astrology",
                "stable-only facts cannot include Ascendant",
                "ascendant",
            )
        if facts.mc is not None:
            raise contract_error(
                "astrology", "stable-only facts cannot include MC", "mc"
            )
        if facts.house_cusps:
            raise contract_error(
                "astrology",
                "stable-only facts cannot include house cusps",
                "house_cusps",
            )
        return

    _validate_optional_longitude(facts.ascendant, "ascendant")
    _validate_optional_longitude(facts.mc, "mc")
    seen_houses = set()
    for index, cusp in enumerate(facts.house_cusps):
        if type(cusp.house) is not int or not 1 <= cusp.house <= 12:
            raise contract_error(
                "astrology",
                "cusp house must be an integer from 1 to 12",
                f"house_cusps.{index}.house",
            )
        if cusp.house in seen_houses:
            raise contract_error(
                "astrology",
                "duplicate house cusp",
                f"house_cusps.{index}.house",
            )
        seen_houses.add(cusp.house)
        validate_decimal_range(
            cusp.longitude,
            Decimal("0"),
            Decimal("360"),
            "astrology",
            f"house_cusps.{index}.longitude",
        )
    if seen_houses != set(range(1, 13)):
        raise contract_error(
            "astrology",
            "time-sensitive facts require all 12 house cusps",
            "house_cusps",
        )


def _validate_aspects(
    facts: AstrologyChartFacts, fact_mode: FactMode, config: RuntimeConfig
) -> None:
    _validate_collection(facts.aspects, AstrologyAspectFact, "aspects")
    methodology = config.astrology
    planets = set(methodology.bodies.planets)
    angles = set(methodology.bodies.angles)
    allowed_bodies = planets | angles
    enabled_aspects = set(methodology.aspects.enabled)
    max_orbs = dict(methodology.aspects.max_orbs)
    seen = set()
    for index, aspect in enumerate(facts.aspects):
        prefix = f"aspects.{index}"
        for field, body in (
            ("body_a", aspect.body_a),
            ("body_b", aspect.body_b),
        ):
            if body not in allowed_bodies:
                raise contract_error(
                    "astrology", "unknown aspect body", f"{prefix}.{field}"
                )
        if aspect.body_a == aspect.body_b:
            raise contract_error(
                "astrology",
                "aspect cannot reference one body twice",
                f"{prefix}.body_b",
            )
        if aspect.aspect_type not in enabled_aspects:
            raise contract_error(
                "astrology",
                "aspect type is not enabled",
                f"{prefix}.aspect_type",
            )
        key = (tuple(sorted((aspect.body_a, aspect.body_b))), aspect.aspect_type)
        if key in seen:
            raise contract_error("astrology", "duplicate aspect", prefix)
        seen.add(key)

        angle_count = int(aspect.body_a in angles) + int(aspect.body_b in angles)
        if angle_count:
            if fact_mode is FactMode.STABLE_ONLY:
                raise contract_error(
                    "astrology",
                    "stable-only facts cannot include angle aspects",
                    prefix,
                )
            if angle_count != 1 or not (
                aspect.body_a in planets or aspect.body_b in planets
            ):
                raise contract_error(
                    "astrology",
                    "angle aspect must pair one planet and one angle",
                    prefix,
                )
            if aspect.aspect_type not in {
                "conjunction",
                "opposition",
                "square",
            }:
                raise contract_error(
                    "astrology",
                    "angle aspect type is not allowed",
                    f"{prefix}.aspect_type",
                )
            maximum = Decimal(methodology.aspects.angle_orb)
        else:
            maximum = Decimal(max_orbs[aspect.aspect_type])
            if (
                aspect.body_a in {"Sun", "Moon"}
                or aspect.body_b in {"Sun", "Moon"}
            ):
                maximum += Decimal(methodology.aspects.luminary_orb_bonus)
        _validate_orb(aspect.orb, maximum, f"{prefix}.orb")


def _validate_orb(value: object, maximum: Decimal, field: str) -> None:
    if type(value) is not Decimal or not value.is_finite():
        raise contract_error(
            "astrology", "orb must be a finite Decimal", field
        )
    if not Decimal("0") <= value <= maximum:
        raise contract_error(
            "astrology", f"orb must be between 0 and {maximum}", field
        )


def _validate_dignities(
    facts: AstrologyChartFacts, config: RuntimeConfig
) -> None:
    _validate_collection(facts.dignities, DignityFact, "dignities")
    planets = set(config.astrology.bodies.planets)
    dignity_types = set(config.astrology.dignity.dignity_types)
    seen = set()
    for index, dignity in enumerate(facts.dignities):
        prefix = f"dignities.{index}"
        if dignity.body not in planets:
            raise contract_error(
                "astrology", "unknown dignity body", f"{prefix}.body"
            )
        if dignity.dignity not in dignity_types:
            raise contract_error(
                "astrology", "unknown dignity type", f"{prefix}.dignity"
            )
        key = (dignity.body, dignity.dignity)
        if key in seen:
            raise contract_error("astrology", "duplicate dignity", prefix)
        seen.add(key)
