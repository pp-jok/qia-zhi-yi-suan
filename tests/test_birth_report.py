import json

import pytest

from destiny_personality.birth_report import build_birth_report, parse_birth_input


def test_real_birth_input_runs_calculation_qualification_and_report(tmp_path):
    result = build_birth_report(
        "1992年7月14日 15:30，上海，女",
        tmp_path / "report.json",
        tmp_path / "artifacts",
        mode="standard-interpretive-v1",
    )
    assert result["status"] == "ok"
    assert result["section_count"] >= 7
    facts = json.loads((tmp_path / "artifacts" / "facts.json").read_text())
    qualification = json.loads((tmp_path / "artifacts" / "qualification.json").read_text())
    report = json.loads((tmp_path / "report.json").read_text())
    assert facts["bazi"]["day_pillar"] == {"heavenly_stem": "辛", "earthly_branch": "卯"}
    assert len(facts["astrology"]["placements"]) == 10
    assert len(facts["astrology"]["house_cusps"]) == 12
    assert qualification["qualification_status"] == "passed"
    assert report["mode"] == "audited_interpretive"


def test_default_birth_report_persists_audited_core_profile_artifacts(tmp_path):
    result = build_birth_report(
        "2000年1月1日 00:30，上海，女",
        tmp_path / "report.json",
        tmp_path / "artifacts",
    )

    report = json.loads((tmp_path / "report.json").read_text())
    profile = json.loads((tmp_path / "artifacts" / "core_profile.json").read_text())
    plan = json.loads((tmp_path / "artifacts" / "report_plan.json").read_text())
    audit = json.loads((tmp_path / "artifacts" / "report_audit.json").read_text())
    assert result["mode"] == "core-profile-v1"
    assert report["mode"] == "core-profile-v1"
    assert report["report_plan_ref"] == str(tmp_path / "artifacts" / "report_plan.json")
    assert profile["schema_version"] == "audited-interpretive-cdp-v1"
    assert plan["schema_version"] == "audited-profile-report-plan-v1"
    assert audit["core_profile_id"] == profile["core_profile_id"]
    assert 4 <= result["section_count"] <= 8


@pytest.mark.parametrize("value", ("bad input", "1992年7月14日 15:30，杭州，女"))
def test_birth_input_rejects_invalid_or_unsupported_locations(value):
    with pytest.raises(ValueError):
        parse_birth_input(value)
