"""Deterministic, local chart provider used by the v0.7 birth-input entrypoint."""

from datetime import datetime, timedelta, timezone
from decimal import Decimal
from math import atan2, cos, degrees, radians, sin, tan
from zoneinfo import ZoneInfo

from astronomy import Body, Ecliptic, GeoVector, Rotation_EQD_ECL, SiderealTime, Time
from lunar_python import Solar

from .calculation.errors import CalculationError
from .calculation.models import (
    AstrologyAspectFact, AstrologyChartFacts, AstrologyPlacement, BaziChartFacts,
    BaziPillar, BirthInput, DignityFact, FactMode, HiddenStemsFact, HouseCusp,
    NormalizedBirthTime, PillarPosition, TenGodFact, TenGodSourceKind,
)
from .config_models import (
    AstrologyAspectsConfig, AstrologyBodiesConfig, AstrologyCoreConfig,
    AstrologyMethodologyConfig, BaziCalendarConfig, BaziMethodologyConfig,
    BaziRelationsConfig, BaziTimeConfig, DignityConfig, IntegerRange,
    OuterPlanetsConfig, PersonalityScopeConfig, PrimitiveRelationGraphConfig,
    RuntimeConfig, SalienceByOrbConfig, ScoreModelConfig, ScoreRulesConfig,
    SynthesisPriorityConfig,
)

PROVIDER_ID = "local-mit-chart-provider-v1"
PROVIDER_VERSIONS = {"lunar_python": "1.4.8", "astronomy_engine": "2.1.19"}
_STEMS = "甲乙丙丁戊己庚辛壬癸"
_ELEMENT = dict(zip(_STEMS, ("wood", "wood", "fire", "fire", "earth", "earth", "metal", "metal", "water", "water")))
_YANG = frozenset("甲丙戊庚壬")
_HIDDEN = {"子": ("癸",), "丑": ("己", "癸", "辛"), "寅": ("甲", "丙", "戊"), "卯": ("乙",), "辰": ("戊", "乙", "癸"), "巳": ("丙", "戊", "庚"), "午": ("丁", "己"), "未": ("己", "丁", "乙"), "申": ("庚", "壬", "戊"), "酉": ("辛",), "戌": ("戊", "辛", "丁"), "亥": ("壬", "甲")}
_SIGNS = ("Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces")
_BODIES = {"Sun": Body.Sun, "Moon": Body.Moon, "Mercury": Body.Mercury, "Venus": Body.Venus, "Mars": Body.Mars, "Jupiter": Body.Jupiter, "Saturn": Body.Saturn, "Uranus": Body.Uranus, "Neptune": Body.Neptune, "Pluto": Body.Pluto}
_DOMICILE = {"Sun": ("Leo",), "Moon": ("Cancer",), "Mercury": ("Gemini", "Virgo"), "Venus": ("Taurus", "Libra"), "Mars": ("Aries", "Scorpio"), "Jupiter": ("Sagittarius", "Pisces"), "Saturn": ("Capricorn", "Aquarius"), "Uranus": ("Aquarius",), "Neptune": ("Pisces",), "Pluto": ("Scorpio",)}
_EXALT = {"Sun": "Aries", "Moon": "Taurus", "Mercury": "Virgo", "Venus": "Pisces", "Mars": "Capricorn", "Jupiter": "Cancer", "Saturn": "Libra"}
_OPPOSITE = {sign: _SIGNS[(index + 6) % 12] for index, sign in enumerate(_SIGNS)}


def local_runtime_config() -> RuntimeConfig:
    """Runtime contract shipped with the local provider, independent of repo paths."""
    bazi = BaziMethodologyConfig("bazi-core-v1.0", BaziCalendarConfig("gregorian", "solar_terms_jie", "00:00", "true_solar_time"), BaziTimeConfig(True, True, True, True), (("立春", "寅"), ("惊蛰", "卯"), ("清明", "辰"), ("立夏", "巳"), ("芒种", "午"), ("小暑", "未"), ("立秋", "申"), ("白露", "酉"), ("寒露", "戌"), ("立冬", "亥"), ("大雪", "子"), ("小寒", "丑")), BaziRelationsConfig(True, True, True, True, True, True, True, ("辰", "午", "酉", "亥")), PersonalityScopeConfig(False, False))
    astrology = AstrologyMethodologyConfig("western-tropical-whole-sign-v1.0", AstrologyCoreConfig("tropical", "geocentric", "whole_sign", True), AstrologyBodiesConfig(tuple(_BODIES), ("Ascendant", "MC")), AstrologyAspectsConfig(("conjunction", "opposition", "square", "trine", "sextile"), False, (("conjunction", 8), ("opposition", 8), ("square", 7), ("trine", 7), ("sextile", 5)), 1, 4), SalienceByOrbConfig(1, 3, 5), DignityConfig(True, ("domicile", "detriment", "exaltation", "fall"), "modifier_only"), OuterPlanetsConfig(True))
    score = ScoreModelConfig("2.2", IntegerRange(0, 4), ("high", "medium", "low", "unstable"), ("validation", "complement", "contextualization", "tension", "correction", "single_system"), SynthesisPriorityConfig(0, 4, 3), ScoreRulesConfig(False, False, True, True))
    return RuntimeConfig(bazi, astrology, score, PrimitiveRelationGraphConfig("1.0", ()))


class LocalTimeNormalizer:
    def normalize(self, birth_input: BirthInput, config) -> NormalizedBirthTime:
        try:
            zone = ZoneInfo(birth_input.timezone_name)
        except Exception as error:
            raise CalculationError("TIMEZONE_UNAVAILABLE", "IANA timezone is unavailable", system="time", field="timezone_name") from error
        if birth_input.birth_time is None:
            return NormalizedBirthTime(birth_input.birth_date, None, None, None, None, birth_input.timezone_name, None, birth_input.time_basis, birth_input.fact_mode, ("birth_time_unavailable",))
        civil = datetime.combine(birth_input.birth_date, birth_input.birth_time)
        localized = civil.replace(tzinfo=zone)
        utc = localized.astimezone(timezone.utc)
        offset = localized.utcoffset() or timedelta(0)
        standard = civil - (localized.dst() or timedelta(0))
        # Equation of time approximation plus longitude correction. It is recorded
        # separately so the selected Bazi time basis remains auditable.
        day = civil.timetuple().tm_yday
        b = radians((360 / 364) * (day - 81))
        eot_minutes = 9.87 * sin(2 * b) - 7.53 * cos(b) - 1.5 * sin(b)
        meridian = offset.total_seconds() / 3600 * 15
        correction = 4 * (float(birth_input.longitude) - meridian) + eot_minutes
        true_solar = standard + timedelta(minutes=correction)
        return NormalizedBirthTime(birth_input.birth_date, civil, standard, utc, true_solar, birth_input.timezone_name, bool(localized.dst()), birth_input.time_basis, birth_input.fact_mode, ("true_solar_time_approximation",) if birth_input.time_basis.value == "true_solar_time" else ())


class LocalBaziCalculator:
    def calculate(self, birth_input: BirthInput, normalized_time: NormalizedBirthTime, methodology) -> BaziChartFacts:
        basis = normalized_time.true_solar_time if normalized_time.time_basis.value == "true_solar_time" else normalized_time.local_standard_time
        if basis is None:
            raise CalculationError("TIME_REQUIRED", "Bazi local provider requires a birth time", system="bazi")
        try:
            eight = Solar.fromYmdHms(basis.year, basis.month, basis.day, basis.hour, basis.minute, basis.second).getLunar().getEightChar()
            values = (eight.getYear(), eight.getMonth(), eight.getDay(), eight.getTime())
        except Exception as error:
            raise CalculationError("BAZI_PROVIDER_ERROR", "local Bazi provider failed", system="bazi") from error
        pillars = tuple(BaziPillar(value[0], value[1]) for value in values)
        positions = (PillarPosition.YEAR, PillarPosition.MONTH, PillarPosition.DAY, PillarPosition.HOUR)
        hidden = tuple(HiddenStemsFact(position, _HIDDEN[pillar.earthly_branch]) for position, pillar in zip(positions, pillars))
        day_master = pillars[2].heavenly_stem
        ten_gods = []
        for position, pillar in zip(positions, pillars):
            sources = (PillarPosition.DAY,) if position is PillarPosition.DAY else (position, PillarPosition.DAY)
            ten_gods.append(TenGodFact(f"{position.value}.stem", _ten_god(day_master, pillar.heavenly_stem), sources, TenGodSourceKind.VISIBLE_STEM))
        for item in hidden:
            for index, stem in enumerate(item.stems):
                sources = (PillarPosition.DAY,) if item.pillar is PillarPosition.DAY else (item.pillar, PillarPosition.DAY)
                ten_gods.append(TenGodFact(f"{item.pillar.value}.hidden_stem.{index}", _ten_god(day_master, stem), sources, TenGodSourceKind.HIDDEN_STEM))
        return BaziChartFacts(methodology.methodology_version, pillars[0], pillars[1], pillars[2], pillars[3], hidden, tuple(ten_gods), ())


class LocalAstrologyCalculator:
    def calculate(self, birth_input: BirthInput, normalized_time: NormalizedBirthTime, methodology) -> AstrologyChartFacts:
        if normalized_time.utc_time is None:
            raise CalculationError("TIME_REQUIRED", "astrology local provider requires a birth time", system="astrology")
        utc = normalized_time.utc_time
        moment = Time.Make(utc.year, utc.month, utc.day, utc.hour, utc.minute, utc.second + utc.microsecond / 1_000_000)
        longitudes = {name: _longitude(body, moment) for name, body in _BODIES.items()}
        ascendant, mc = _angles(moment, float(birth_input.latitude), float(birth_input.longitude))
        first_sign = int(ascendant // 30)
        placements = tuple(_placement(name, longitude, first_sign) for name, longitude in longitudes.items())
        cusps = tuple(HouseCusp(index + 1, _decimal(((first_sign + index) % 12) * 30)) for index in range(12))
        aspects = _aspects(longitudes, ascendant, mc, methodology)
        dignities = tuple(item for name, longitude in longitudes.items() if (item := _dignity(name, _SIGNS[int(longitude // 30)])) is not None)
        return AstrologyChartFacts(methodology.methodology_version, placements, aspects, _decimal(ascendant), _decimal(mc), cusps, dignities)


def _ten_god(day_master: str, subject: str) -> str:
    element = _ELEMENT[day_master]; target = _ELEMENT[subject]; same = (day_master in _YANG) == (subject in _YANG)
    produced = {"wood": "fire", "fire": "earth", "earth": "metal", "metal": "water", "water": "wood"}
    controls = {"wood": "earth", "fire": "metal", "earth": "water", "metal": "wood", "water": "fire"}
    if target == element: return "比肩" if same else "劫财"
    if produced[element] == target: return "食神" if same else "伤官"
    if controls[element] == target: return "偏财" if same else "正财"
    if controls[target] == element: return "七杀" if same else "正官"
    return "偏印" if same else "正印"


def _longitude(body, moment):
    vector = GeoVector(body, moment, True)
    return Ecliptic(vector).elon % 360


def _angles(moment, latitude, longitude):
    armc = radians((SiderealTime(moment) * 15 + longitude) % 360)
    # Astronomy Engine's date rotation is used for planetary coordinates; this
    # standard mean obliquity is sufficient for the declared whole-sign angles.
    obliquity = radians(23.4392911)
    asc = degrees(atan2(-cos(armc), sin(armc) * cos(obliquity) + tan(radians(latitude)) * sin(obliquity))) % 360
    mc = degrees(atan2(sin(armc) * cos(obliquity), cos(armc))) % 360
    return asc, mc


def _placement(name, longitude, first_sign):
    sign_index = int(longitude // 30)
    return AstrologyPlacement(name, _decimal(longitude), _SIGNS[sign_index], _decimal(longitude % 30), ((sign_index - first_sign) % 12) + 1)


def _aspects(longitudes, ascendant, mc, methodology):
    targets = {"conjunction": 0, "opposition": 180, "square": 90, "trine": 120, "sextile": 60}
    max_orbs = dict(methodology.aspects.max_orbs); values = dict(longitudes); values.update({"Ascendant": ascendant, "MC": mc}); facts = []
    names = list(values)
    for index, first in enumerate(names):
        for second in names[index + 1:]:
            separation = abs(values[first] - values[second]); separation = min(separation, 360 - separation)
            for kind, target in targets.items():
                orb = abs(separation - target); maximum = methodology.aspects.angle_orb if (first in {"Ascendant", "MC"} or second in {"Ascendant", "MC"}) else max_orbs[kind] + (methodology.aspects.luminary_orb_bonus if {first, second} & {"Sun", "Moon"} else 0)
                if orb <= maximum and not ({first, second} & {"Ascendant", "MC"} and kind not in {"conjunction", "opposition", "square"}):
                    facts.append(AstrologyAspectFact(first, second, kind, _decimal(orb)))
    return tuple(facts)


def _dignity(body, sign):
    if sign in _DOMICILE.get(body, ()): return DignityFact(body, "domicile")
    if sign in {_OPPOSITE[item] for item in _DOMICILE.get(body, ())}: return DignityFact(body, "detriment")
    if _EXALT.get(body) == sign: return DignityFact(body, "exaltation")
    if _EXALT.get(body) and _OPPOSITE[_EXALT[body]] == sign: return DignityFact(body, "fall")
    return None


def _decimal(value):
    return Decimal(f"{value:.6f}")
