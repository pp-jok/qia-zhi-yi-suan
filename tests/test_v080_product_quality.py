import json

from destiny_personality.birth_report import build_birth_report


CASES = (
    ("case-a", "2000年1月1日 00:30，上海，女"),
    ("case-b", "1992年7月14日 15:30，上海，女"),
    ("case-c", "1986年5月25日 11:55，北京，男"),
)


def test_three_birth_cases_produce_distinct_traceable_dynamic_plans(tmp_path):
    planned_section_sets = []
    reader_title_sets = []
    for case_id, birth_text in CASES:
        case_dir = tmp_path / case_id
        result = build_birth_report(
            birth_text, case_dir / "report.json", case_dir / "artifacts"
        )
        report = json.loads((case_dir / "report.json").read_text())
        profile = json.loads((case_dir / "artifacts" / "core_profile.json").read_text())
        plan = json.loads((case_dir / "artifacts" / "report_plan.json").read_text())
        audit = json.loads((case_dir / "artifacts" / "report_audit.json").read_text())
        assert result["mode"] == "core-profile-v1"
        assert profile["semantic_model_assurance"] == "audited_interpretive_rule_derived"
        assert audit["core_profile_id"] == profile["core_profile_id"]
        assert report["core_profile_id"] == profile["core_profile_id"]
        assert len(plan["sections"]) == len(report["sections"])
        assert 4 <= len(report["sections"]) <= 8
        assert all(section["signal_ids"] and section["rule_refs"] and section["fact_refs"] for section in report["sections"])
        planned_section_sets.append(
            tuple(
                (section["section_id"], section["evidence_fingerprint"])
                for section in plan["sections"]
            )
        )
        reader_title_sets.append(tuple(section["title"] for section in report["sections"]))

    assert len(set(planned_section_sets)) == len(CASES)
    assert len(set(reader_title_sets)) == len(CASES)
