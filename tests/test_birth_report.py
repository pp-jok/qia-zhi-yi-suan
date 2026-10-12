import json

import pytest

from destiny_personality.birth_report import build_birth_report, parse_birth_input


def test_real_birth_input_runs_calculation_qualification_and_report(tmp_path):
    result = build_birth_report(
        "1992年7月14日 15:30，上海，女",
        tmp_path / "report.json",
        tmp_path / "artifacts",
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


@pytest.mark.parametrize("value", ("bad input", "1992年7月14日 15:30，杭州，女"))
def test_birth_input_rejects_invalid_or_unsupported_locations(value):
    with pytest.raises(ValueError):
        parse_birth_input(value)
