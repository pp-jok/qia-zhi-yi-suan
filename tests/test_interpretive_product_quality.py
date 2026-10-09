import json
import re
from pathlib import Path

import pytest

from destiny_personality.cli import main
from destiny_personality.deterministic_facts_codec import (
    load_qualified_deterministic_facts,
)
from destiny_personality.interpretive_codec import encode_interpretive_report
from destiny_personality.interpretive_report import build_interpretive_report
from destiny_personality.interpretive_rules import extract_interpretive_signals
from destiny_personality.interpretive_synthesis import (
    build_narrative_synthesis_packet,
)


ROOT = Path(__file__).parents[1]
FIXTURE_DIRECTORY = Path(__file__).parent / "fixtures" / "interpretive" / "v060"
DEMO_DIRECTORY = ROOT / "docs" / "demos" / "v0.6.0"
FIXTURE_NAMES = (
    "bazi-dominated",
    "astrology-dominated",
    "cross-system-agreement",
    "cross-system-tension",
    "missing-time",
    "practical-builder",
    "relational-connector",
    "expressive-creator",
    "structured-steward",
    "reflective-scholar",
    "adaptive-explorer",
    "boundary-mentor",
)
NORMAL_COMPLETE_NAMES = tuple(
    name for name in FIXTURE_NAMES if name != "missing-time"
)
DEMO_CASES = {
    "bazi-dominated": "bazi-dominated-standard.json",
    "astrology-dominated": "astrology-dominated-standard.json",
    "cross-system-agreement": "agreement-standard.json",
    "cross-system-tension": "tension-standard.json",
    "missing-time": "missing-time-standard.json",
}


def _paths(name: str) -> tuple[Path, Path]:
    return (
        FIXTURE_DIRECTORY / f"{name}-facts.json",
        FIXTURE_DIRECTORY / f"{name}-qualification.json",
    )


def _qualified(name: str):
    facts_path, qualification_path = _paths(name)
    return load_qualified_deterministic_facts(facts_path, qualification_path)


def _report_payload(name: str) -> dict:
    return encode_interpretive_report(
        build_interpretive_report(_qualified(name), "standard")
    )


def reader_topics(payload: dict) -> set[str]:
    return {section["title"] for section in payload["sections"]}


def core_reader_text(payload: dict) -> str:
    return "\n".join(
        f'{section["title"]}\n{section["content"]}'
        for section in payload["sections"]
    )


def reader_semantic_signature(payload: dict) -> tuple[tuple[str, str, str, str, str], ...]:
    """Keep the reader-visible semantic frame while ignoring fact interpolation."""
    signatures = []
    for section in payload["sections"]:
        normalized = re.sub(r"（命中依据：.*?）", "（命中依据：已省略）", section["content"])
        fields = re.match(
            r"结论：(.*?)。形成机制：(.*?)。常见表现：(.*?)。情境变化：(.*?)。",
            normalized,
            flags=re.DOTALL,
        )
        assert fields, f"section does not expose the reader semantic frame: {section['title']}"
        signatures.append((section["title"], *fields.groups()))
    return tuple(signatures)


def all_reader_visible_text(payload: dict) -> str:
    section_text = "\n".join(
        f'{section["title"]}\n{section["content"]}\n{section["limitation"]}'
        for section in payload["sections"]
    )
    return f'{payload["title"]}\n{section_text}\n{payload["boundary_statement"]}'


@pytest.fixture(params=NORMAL_COMPLETE_NAMES, ids=NORMAL_COMPLETE_NAMES)
def product_fixture(request):
    return _report_payload(request.param)


@pytest.fixture(scope="module")
def product_fixtures():
    return {name: _report_payload(name) for name in FIXTURE_NAMES}


def test_v060_has_twelve_loadable_qualified_fact_pairs() -> None:
    assert len(FIXTURE_NAMES) >= 12
    for name in FIXTURE_NAMES:
        facts_path, qualification_path = _paths(name)
        assert facts_path.is_file()
        assert qualification_path.is_file()
        qualified = _qualified(name)
        assert qualified.fact_fingerprint
        assert qualified.qualification_fingerprint


def test_normal_chart_has_multiple_real_topics(product_fixture) -> None:
    assert len(reader_topics(product_fixture)) >= 6


def test_normal_chart_has_real_contributions_from_both_systems(
    product_fixture,
) -> None:
    systems = {
        provenance["system"]
        for section in product_fixture["sections"]
        for provenance in section["signal_provenance"]
    }
    assert systems == {"bazi", "astrology"}


def test_reports_are_reader_semantically_distinct(product_fixtures) -> None:
    texts = [core_reader_text(item) for item in product_fixtures.values()]
    assert len(set(texts)) == len(product_fixtures)


def test_reports_have_distinct_reader_semantic_signatures(product_fixtures) -> None:
    signatures = [
        reader_semantic_signature(item) for item in product_fixtures.values()
    ]
    assert len(set(signatures)) == len(product_fixtures)


def test_product_matrix_contains_the_five_required_reader_semantics() -> None:
    bazi = extract_interpretive_signals(_qualified("bazi-dominated"))
    astrology = extract_interpretive_signals(_qualified("astrology-dominated"))
    assert sum(item.system == "bazi" for item in bazi) > sum(
        item.system == "astrology" for item in bazi
    )
    assert sum(item.system == "astrology" for item in astrology) > sum(
        item.system == "bazi" for item in astrology
    )

    agreement = _report_payload("cross-system-agreement")
    expression = next(
        section for section in agreement["sections"]
        if section["title"] == "表达与创造"
    )
    assert {
        "BAZI-TEN-GOD-OUTPUT",
        "ASTROLOGY-PLANET-SIGN-EXPRESSION",
    } <= set(expression["signal_ids"])

    tension = build_narrative_synthesis_packet(
        _qualified("cross-system-tension")
    )
    assert any(item.topic == "style of expression" for item in tension.tensions)

    missing_time = _report_payload("missing-time")
    assert missing_time["audit_metadata"]["birth_time_status"] == (
        "unavailable_or_uncertain"
    )
    assert "astrology.houses" in missing_time["audit_metadata"][
        "omitted_time_sensitive_claims"
    ]
    assert "ASTROLOGY-SUN-HOUSE-CONTEXT" not in {
        signal_id
        for section in missing_time["sections"]
        for signal_id in section["signal_ids"]
    }


def test_reader_body_is_traceable_without_raw_calculation_paths(
    product_fixtures,
) -> None:
    raw_path_markers = (
        "bazi.",
        "astrology.",
        "ten_gods[",
        "placements[",
        "participant_refs",
    )
    for payload in product_fixtures.values():
        assert payload["audit_metadata"]["rule_bundle_refs"]
        assert payload["audit_metadata"]["fact_refs"]
        assert payload["audit_metadata"]["qualification_refs"]
        for section in payload["sections"]:
            assert section["signal_ids"]
            assert section["signal_provenance"]
            assert all(item["fact_refs"] for item in section["signal_provenance"])
        reader_body = all_reader_visible_text(payload)
        assert not any(marker in reader_body for marker in raw_path_markers)


@pytest.mark.parametrize(
    ("fixture_name", "demo_name"), DEMO_CASES.items(), ids=DEMO_CASES
)
def test_checked_in_v060_demos_are_reproducible_through_production_cli(
    tmp_path: Path, fixture_name: str, demo_name: str
) -> None:
    facts_path, qualification_path = _paths(fixture_name)
    generated = tmp_path / demo_name
    assert main(
        [
            "build-interpretive-report",
            str(facts_path),
            "--qualification",
            str(qualification_path),
            "--mode",
            "standard-interpretive-v1",
            "--output",
            str(generated),
        ]
    ) == 0

    checked_in = json.loads(
        (DEMO_DIRECTORY / demo_name).read_text(encoding="utf-8")
    )
    assert checked_in == json.loads(generated.read_text(encoding="utf-8"))


def test_coverage_and_differentiation_docs_cover_every_fixture() -> None:
    coverage = (ROOT / "docs" / "interpretive-rule-coverage.md").read_text(
        encoding="utf-8"
    )
    review = (ROOT / "docs" / "product-differentiation-review.md").read_text(
        encoding="utf-8"
    )
    for name in FIXTURE_NAMES:
        assert name in coverage
        assert name in review
    assert "template collapse" in review.casefold()
