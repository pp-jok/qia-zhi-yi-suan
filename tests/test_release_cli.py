import json

from destiny_personality.calculation import DeterministicChartFacts


def _facts_payload(normalized_time, bazi_facts, astrology_facts):
    from destiny_personality.deterministic_facts_codec import deterministic_facts_to_dict

    facts = DeterministicChartFacts(normalized_time, bazi_facts, astrology_facts)
    payload = deterministic_facts_to_dict(facts)
    payload.update(
        {
            "schema_version": "deterministic-facts-v1",
            "fact_mode": facts.normalized_time.fact_mode.value,
            "methodology_versions": {
                "bazi": facts.bazi.methodology_version,
                "astrology": facts.astrology.methodology_version,
            },
            "provenance_refs": ["accepted-envelope:test"],
            "validation_summary": {"structure": "passed"},
        }
    )
    return facts, payload


def _qualification(facts):
    from destiny_personality.deterministic_facts_codec import deterministic_facts_fingerprint

    return {
        "schema_version": "fact-qualification-v1",
        "fact_fingerprint": deterministic_facts_fingerprint(facts),
        "qualification_status": "passed",
        "derived_fact_assurance": "capability_reported",
        "fact_contract_version": "deterministic-facts-v1",
        "methodology_versions": {
            "bazi": facts.bazi.methodology_version,
            "astrology": facts.astrology.methodology_version,
        },
        "validation_refs": ["validation:test"],
        "provenance_refs": ["provenance:test"],
        "calculation_envelope_refs": ["envelope:test"],
        "comparison": {"required": False, "status": "not_required"},
        "validation_summary": {
            "structure": "passed",
            "methodology": "passed",
            "provenance": "passed",
            "internal_consistency": "passed",
            "time_scope": "passed",
            "calculation_config": "not_available",
        },
    }


def test_cli_builds_degraded_release_report_from_qualified_facts(
    tmp_path, normalized_time, bazi_facts, astrology_facts, capsys
):
    from destiny_personality.cli import main

    facts, payload = _facts_payload(normalized_time, bazi_facts, astrology_facts)
    facts_path = tmp_path / "facts.json"
    qualification_path = tmp_path / "qualification.json"
    output_path = tmp_path / "release-report.json"
    facts_path.write_text(json.dumps(payload), encoding="utf-8")
    qualification_path.write_text(json.dumps(_qualification(facts)), encoding="utf-8")

    assert main([
        "build-release-report", str(facts_path), "--qualification", str(qualification_path),
        "--mode", "standard-portrait-v1", "--output", str(output_path),
    ]) == 0
    assert json.loads(capsys.readouterr().out)["status"] == "ok"
    report = json.loads(output_path.read_text(encoding="utf-8"))
    assert report["report"]["primitive_interpretations"] == []
    assert report["assurance"]["semantic_model_assurance"] == "limited_coverage_unknown_only"


def test_cli_rejects_unqualified_facts(tmp_path, capsys):
    from destiny_personality.cli import main

    facts_path = tmp_path / "facts.json"
    facts_path.write_text("{}", encoding="utf-8")
    assert main([
        "build-release-report", str(facts_path), "--qualification", str(tmp_path / "missing.json"),
        "--mode", "concise-portrait-v1", "--output", str(tmp_path / "output.json"),
    ]) == 2
    assert "DETERMINISTIC_FACTS_SCHEMA_INVALID" in capsys.readouterr().err
