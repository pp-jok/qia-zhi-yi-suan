from dataclasses import dataclass
import json
from pathlib import Path

import pytest

from destiny_personality.cli import main
from destiny_personality.deterministic_facts_codec import (
    load_qualified_deterministic_facts,
)
from destiny_personality.interpretive_profile import build_interpretive_core_profile


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
    scenario: str,
    tmp_path: Path,
    *,
    mode: str = "standard-interpretive-v1",
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
            "standard-interpretive-v1",
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
    assert payload["report_mode"] == "standard-interpretive-v1"
    assert payload["schema_version"] == "interpretive-report-v1"
    assert 6 <= len(payload["sections"]) <= 12
    assert all(section["kind"] == "analysis" for section in payload["sections"])
    assert all(section["signal_ids"] for section in payload["sections"])
    assert payload["audit_metadata"]["fact_refs"] == [
        f"deterministic-facts:{qualified.fact_fingerprint}"
    ]
    assert payload["audit_metadata"]["qualification_refs"] == [
        f"fact-qualification:{qualified.qualification_fingerprint}"
    ]
    provenance_by_id = {
        provenance["signal_id"]: provenance
        for section in payload["sections"]
        for provenance in section["signal_provenance"]
    }
    assert provenance_by_id
    assert set(provenance_by_id) == _signal_ids(payload)
    assert all(item["fact_refs"] for item in provenance_by_id.values())
    assert all(
        item["traditional_rule_ref"] for item in provenance_by_id.values()
    )
    assert all(
        item["system"] in {"bazi", "astrology"}
        for item in provenance_by_id.values()
    )
    for section in payload["sections"]:
        assert [
            item["signal_id"] for item in section["signal_provenance"]
        ] == section["signal_ids"]


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


def test_tension_fixture_creates_countervailing_profile_conclusions() -> None:
    paths = _fixture_paths("tension")
    qualified = load_qualified_deterministic_facts(
        paths.facts, paths.qualification
    )

    profile = build_interpretive_core_profile(qualified)

    tensions = tuple(
        conclusion
        for conclusion in profile.conclusions
        if conclusion.supporting_signal_ids
        and conclusion.countervailing_signal_ids
    )
    assert tensions
    assert {conclusion.direction for conclusion in tensions} == {
        "reflective",
        "outward",
    }
    assert all(
        {
            "BAZI-TEN-GOD-EXPRESSION",
            "ASTROLOGY-PLANET-SIGN-EXPRESSION",
        }
        == set(
            conclusion.supporting_signal_ids
            + conclusion.countervailing_signal_ids
        )
        for conclusion in tensions
    )


def test_missing_time_visibly_degrades_time_sensitive_output(
    tmp_path: Path,
) -> None:
    complete = _render("tension", tmp_path)
    missing_time = _render("missing_time", tmp_path)

    assert "ASTROLOGY-SUN-HOUSE-CONTEXT" in _signal_ids(complete)
    assert "ASTROLOGY-SUN-HOUSE-CONTEXT" not in _signal_ids(missing_time)
    assert _signal_ids(missing_time) == _signal_ids(complete) - {
        "ASTROLOGY-SUN-HOUSE-CONTEXT"
    }
    assert _reader_visible_signature(missing_time) != _reader_visible_signature(
        complete
    )


@pytest.mark.parametrize(
    "mode", ("standard-interpretive-v1", "concise-interpretive-v1")
)
def test_missing_time_reports_metadata_and_visible_omission_notice(
    tmp_path: Path, mode: str
) -> None:
    payload = _render("missing_time", tmp_path, mode=mode)

    assert payload["audit_metadata"]["fact_mode"] == "stable_only"
    assert payload["audit_metadata"]["birth_time_status"] == (
        "unavailable_or_uncertain"
    )
    assert payload["audit_metadata"]["omitted_time_sensitive_claims"] == [
        "astrology.houses",
        "astrology.angles",
    ]
    visible_text = "".join(
        section["title"] + section["content"] + section["limitation"]
        for section in payload["sections"]
    )
    assert "出生时间不可用或存疑" in visible_text
    assert "宫位与四轴主张已省略" in visible_text


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
        (
            "contrast_a",
            "standard-interpretive-v1",
            "contrast-a-standard.json",
        ),
        ("tension", "standard-interpretive-v1", "tension-standard.json"),
        (
            "missing_time",
            "standard-interpretive-v1",
            "missing-time-standard.json",
        ),
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
                "standard-interpretive-v1",
                "--output",
                str(tmp_path / "report.json"),
            ]
        )
        == 2
    )
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "FACT_QUALIFICATION_REQUIRED" in captured.err


@pytest.mark.parametrize(
    ("mode", "expected_report_mode"),
    [
        ("standard-interpretive-v1", "standard-interpretive-v1"),
        ("concise-interpretive-v1", "concise-interpretive-v1"),
    ],
)
def test_cli_accepts_versioned_public_report_modes(
    tmp_path: Path, mode: str, expected_report_mode: str
) -> None:
    payload = _render("tension", tmp_path, mode=mode)

    assert payload["report_mode"] == expected_report_mode


def test_cli_help_presents_only_versioned_report_modes(capsys) -> None:
    with pytest.raises(SystemExit) as exit_info:
        main(["build-interpretive-report", "--help"])

    assert exit_info.value.code == 0
    help_text = capsys.readouterr().out
    assert (
        "{standard-interpretive-v1,concise-interpretive-v1}" in help_text
    )
    assert "{standard,concise}" not in help_text


@pytest.mark.parametrize(
    ("alias", "canonical_mode"),
    [
        ("standard", "standard-interpretive-v1"),
        ("concise", "concise-interpretive-v1"),
    ],
)
def test_cli_normalizes_compatibility_mode_aliases(
    tmp_path: Path, alias: str, canonical_mode: str
) -> None:
    payload = _render("tension", tmp_path, mode=alias)

    assert payload["report_mode"] == canonical_mode
