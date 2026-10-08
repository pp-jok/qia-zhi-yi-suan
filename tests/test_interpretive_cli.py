from dataclasses import dataclass
import json
from pathlib import Path

import pytest

from destiny_personality.cli import main
from destiny_personality.deterministic_facts_codec import (
    load_qualified_deterministic_facts,
)


FIXTURE_DIRECTORY = Path(__file__).parent / "fixtures" / "interpretive"
DEMO_DIRECTORY = Path(__file__).parents[1] / "docs" / "demos" / "v0.5.0"
SCENARIOS = (
    "contrast_a",
    "contrast_b",
    "relationship_sensitive",
    "tension",
    "missing_time",
)


@dataclass(frozen=True)
class FixturePaths:
    facts: Path
    qualification: Path


def _fixture_paths(scenario: str) -> FixturePaths:
    return FixturePaths(
        facts=FIXTURE_DIRECTORY / f"{scenario}-facts.json",
        qualification=FIXTURE_DIRECTORY / f"{scenario}-qualification.json",
    )


@pytest.fixture
def fixture_paths() -> FixturePaths:
    return _fixture_paths("tension")


def _render(
    scenario: str, tmp_path: Path, *, mode: str = "standard"
) -> dict:
    paths = _fixture_paths(scenario)
    output = tmp_path / f"{scenario}-{mode}.json"
    exit_code = main(
        [
            "build-interpretive-report",
            str(paths.facts),
            "--qualification",
            str(paths.qualification),
            "--mode",
            mode,
            "--output",
            str(output),
        ]
    )
    assert exit_code == 0
    return json.loads(output.read_text(encoding="utf-8"))


def _signal_ids(payload: dict) -> set[str]:
    return {
        signal_id
        for section in payload["sections"]
        for signal_id in section["signal_ids"]
    }


def _reader_visible_signature(payload: dict) -> tuple:
    return tuple(
        (section["title"], section["content"], tuple(section["signal_ids"]))
        for section in payload["sections"]
    )


def test_cli_builds_traceable_standard_report(
    tmp_path: Path, fixture_paths: FixturePaths
) -> None:
    output = tmp_path / "report.json"

    exit_code = main(
        [
            "build-interpretive-report",
            str(fixture_paths.facts),
            "--qualification",
            str(fixture_paths.qualification),
            "--mode",
            "standard",
            "--output",
            str(output),
        ]
    )

    assert exit_code == 0
    payload = json.loads(output.read_text(encoding="utf-8"))
    qualified = load_qualified_deterministic_facts(
        fixture_paths.facts, fixture_paths.qualification
    )
    assert payload["mode"] == "audited_interpretive"
    assert payload["report_mode"] == "standard"
    assert payload["schema_version"] == "interpretive-report-v1"
    assert 8 <= len(payload["sections"]) <= 12
    assert all(section["signal_ids"] for section in payload["sections"])
    assert payload["audit_metadata"]["fact_refs"] == [
        f"deterministic-facts:{qualified.fact_fingerprint}"
    ]
    assert payload["audit_metadata"]["qualification_refs"] == [
        f"fact-qualification:{qualified.qualification_fingerprint}"
    ]


def test_distinct_charts_do_not_collapse_to_identical_reports(
    tmp_path: Path,
) -> None:
    contrast_a = _render("contrast_a", tmp_path)
    contrast_b = _render("contrast_b", tmp_path)

    assert _reader_visible_signature(contrast_a) != _reader_visible_signature(
        contrast_b
    )
    assert _signal_ids(contrast_a) != _signal_ids(contrast_b)


def test_tension_fixture_retains_both_systems_in_growth_tension(
    tmp_path: Path,
) -> None:
    payload = _render("tension", tmp_path)

    assert {
        "BAZI-TEN-GOD-EXPRESSION",
        "BAZI-RELATION-DYNAMICS",
        "ASTROLOGY-PLANET-SIGN-EXPRESSION",
        "ASTROLOGY-ASPECT-DIGNITY-CONTEXT",
    } <= _signal_ids(payload)
    growth_tension = next(
        section for section in payload["sections"] if section["title"] == "成长张力"
    )
    assert "ASTROLOGY-ASPECT-DIGNITY-CONTEXT" in growth_tension["signal_ids"]


def test_missing_time_visibly_degrades_time_sensitive_output(
    tmp_path: Path,
) -> None:
    complete = _render("tension", tmp_path)
    missing_time = _render("missing_time", tmp_path)

    assert "ASTROLOGY-PLANET-SIGN-EXPRESSION" in _signal_ids(complete)
    assert "ASTROLOGY-PLANET-SIGN-EXPRESSION" not in _signal_ids(missing_time)
    assert _signal_ids(missing_time) == _signal_ids(complete) - {
        "ASTROLOGY-PLANET-SIGN-EXPRESSION"
    }
    assert _reader_visible_signature(missing_time) != _reader_visible_signature(
        complete
    )


def test_fixture_directory_contains_five_loadable_qualified_pairs() -> None:
    assert len(SCENARIOS) >= 5
    for scenario in SCENARIOS:
        paths = _fixture_paths(scenario)
        assert paths.facts.is_file()
        assert paths.qualification.is_file()
        qualified = load_qualified_deterministic_facts(
            paths.facts, paths.qualification
        )
        assert qualified.fact_fingerprint
        assert qualified.qualification_fingerprint


@pytest.mark.parametrize(
    ("scenario", "mode", "demo_name"),
    [
        ("contrast_a", "standard", "contrast-a-standard.json"),
        ("tension", "standard", "tension-standard.json"),
        ("missing_time", "concise", "missing-time-concise.json"),
    ],
)
def test_checked_in_demos_are_cli_generated_parseable_and_traceable(
    tmp_path: Path, scenario: str, mode: str, demo_name: str
) -> None:
    expected = _render(scenario, tmp_path, mode=mode)
    checked_in = json.loads(
        (DEMO_DIRECTORY / demo_name).read_text(encoding="utf-8")
    )

    assert checked_in == expected
    assert checked_in["mode"] == "audited_interpretive"
    assert checked_in["report_mode"] == mode
    assert all(section["signal_ids"] for section in checked_in["sections"])
    assert checked_in["audit_metadata"]["rule_bundle_refs"]
    assert checked_in["audit_metadata"]["fact_refs"]
    assert checked_in["audit_metadata"]["qualification_refs"]


def test_cli_requires_independent_qualification(tmp_path: Path, capsys) -> None:
    paths = _fixture_paths("contrast_a")

    assert (
        main(
            [
                "build-interpretive-report",
                str(paths.facts),
                "--qualification",
                str(tmp_path / "missing.json"),
                "--mode",
                "standard",
                "--output",
                str(tmp_path / "report.json"),
            ]
        )
        == 2
    )
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "FACT_QUALIFICATION_REQUIRED" in captured.err
