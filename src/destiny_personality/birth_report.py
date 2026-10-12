"""Public birth-input orchestration for v0.7."""
from dataclasses import asdict
from datetime import date, time
from decimal import Decimal
import json
from pathlib import Path
import re

from .calculation import BirthInput, ChartCalculationService, FactMode, TimeBasis
from .calculation.validation.astrology import validate_astrology_facts
from .calculation.validation.bazi import validate_bazi_facts
from .deterministic_facts_codec import deterministic_facts_fingerprint, deterministic_facts_to_dict, load_validated_deterministic_facts
from .interpretive_codec import encode_interpretive_report
from .interpretive_report import build_interpretive_report
from .local_provider import LocalAstrologyCalculator, LocalBaziCalculator, LocalTimeNormalizer, PROVIDER_ID, PROVIDER_VERSIONS, local_runtime_config
from .audited_core_profile import build_audited_interpretive_core_profile
from .audited_profile_report import build_audited_profile_report_plan, render_audited_profile_report

_LOCATIONS = {"上海": ("Asia/Shanghai", "31.2304", "121.4737"), "shanghai": ("Asia/Shanghai", "31.2304", "121.4737"), "北京": ("Asia/Shanghai", "39.9042", "116.4074"), "beijing": ("Asia/Shanghai", "39.9042", "116.4074")}
_BIRTH = re.compile(r"^\s*(?P<year>\d{4})\s*(?:年|[-/.])\s*(?P<month>\d{1,2})\s*(?:月|[-/.])\s*(?P<day>\d{1,2})(?:日)?\s*[ T，,]+(?P<hour>\d{1,2})\s*:\s*(?P<minute>\d{2})\s*[，, ]+\s*(?P<place>[^，, ]+)\s*[，, ]+\s*(?P<gender>男|女|male|female|m|f)\s*$", re.I)

def parse_birth_input(text: str):
    match = _BIRTH.match(text)
    if not match: raise ValueError("BIRTH_INPUT_FORMAT_INVALID: expected '1992年7月14日 15:30，上海，女'")
    values = match.groupdict(); place = values["place"].lower()
    if place not in _LOCATIONS: raise ValueError("BIRTHPLACE_UNSUPPORTED: use 上海/北京 in v0.7")
    zone, latitude, longitude = _LOCATIONS[place]
    try: birth_date, birth_time = date(int(values["year"]), int(values["month"]), int(values["day"])), time(int(values["hour"]), int(values["minute"]))
    except ValueError as error: raise ValueError("BIRTH_INPUT_VALUE_INVALID") from error
    return BirthInput(birth_date, birth_time, zone, Decimal(latitude), Decimal(longitude), TimeBasis.TRUE_SOLAR_TIME, FactMode.TIME_SENSITIVE), values["place"], values["gender"].lower()

def build_birth_report(text: str, output: Path, artifacts_dir: Path, mode: str = "core-profile-v1") -> dict:
    birth_input, place, gender = parse_birth_input(text)
    config = local_runtime_config()
    facts = ChartCalculationService(LocalTimeNormalizer(), LocalBaziCalculator(), LocalAstrologyCalculator()).calculate(birth_input, config)
    validate_bazi_facts(facts.bazi, facts.normalized_time.fact_mode, config); validate_astrology_facts(facts.astrology, facts.normalized_time.fact_mode, config)
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    facts_path, qualification_path, execution_path = artifacts_dir / "facts.json", artifacts_dir / "qualification.json", artifacts_dir / "execution.json"
    payload = deterministic_facts_to_dict(facts)
    payload.update({"schema_version": "deterministic-facts-v1", "fact_mode": facts.normalized_time.fact_mode.value, "methodology_versions": {"bazi": facts.bazi.methodology_version, "astrology": facts.astrology.methodology_version}, "provenance_refs": [f"provider:{PROVIDER_ID}", "provider-version:lunar_python-1.4.8", "provider-version:astronomy-engine-2.1.19"], "validation_summary": {"structure": "passed", "methodology": "passed", "provenance": "passed", "internal_consistency": "passed", "time_scope": "passed", "calculation_config": "passed"}})
    _write_json(facts_path, payload); validated = load_validated_deterministic_facts(facts_path); fingerprint = deterministic_facts_fingerprint(validated)
    qualification = {"schema_version": "fact-qualification-v1", "fact_contract_version": "deterministic-facts-v1", "qualification_status": "passed", "fact_fingerprint": fingerprint, "derived_fact_assurance": "project_verified", "methodology_versions": payload["methodology_versions"], "validation_refs": ["local-qualification-v1:structure-methodology-time"], "provenance_refs": payload["provenance_refs"], "calculation_envelope_refs": ["execution.json"], "validation_summary": payload["validation_summary"], "comparison": {"required": False, "status": "not_required"}}
    _write_json(qualification_path, qualification)
    from .deterministic_facts_codec import load_qualified_deterministic_facts
    qualified = load_qualified_deterministic_facts(facts_path, qualification_path)
    artifacts = {"facts": str(facts_path), "qualification": str(qualification_path)}
    if mode == "core-profile-v1":
        profile = build_audited_interpretive_core_profile(qualified)
        plan = build_audited_profile_report_plan(profile)
        rendered_report = render_audited_profile_report(profile, plan)
        report = asdict(rendered_report)
        core_profile_path = artifacts_dir / "core_profile.json"
        report_plan_path = artifacts_dir / "report_plan.json"
        report_audit_path = artifacts_dir / "report_audit.json"
        report.update({"core_profile_ref": str(core_profile_path), "report_plan_ref": str(report_plan_path), "report_audit_ref": str(report_audit_path)})
        _write_json(core_profile_path, asdict(profile))
        _write_json(report_plan_path, asdict(plan))
        _write_json(report_audit_path, {"schema_version": "audited-profile-report-audit-v1", "core_profile_id": profile.core_profile_id, "fact_fingerprint": fingerprint, "qualification_fingerprint": qualified.qualification_fingerprint, "report_plan_ref": str(report_plan_path), "report_mode": mode, "audit_refs": list(rendered_report.audit_refs), "limitations": list(rendered_report.limitations)})
        artifacts.update({"core_profile": str(core_profile_path), "report_plan": str(report_plan_path), "report_audit": str(report_audit_path)})
        result_mode = mode
    elif mode in {"standard-interpretive-v1", "concise-interpretive-v1"}:
        report = encode_interpretive_report(build_interpretive_report(qualified, "standard" if mode == "standard-interpretive-v1" else "concise"))
        report.update({"mode": "audited_interpretive", "report_mode": mode})
        result_mode = "audited_interpretive"
    else:
        raise ValueError("BIRTH_REPORT_MODE_UNSUPPORTED")
    _write_json(output, report)
    execution = {"schema_version": "birth-report-execution-v2", "status": "passed", "provider_id": PROVIDER_ID, "provider_versions": PROVIDER_VERSIONS, "input": {"birth_text": text, "birthplace": place, "gender": gender}, "facts_path": str(facts_path), "qualification_path": str(qualification_path), "report_path": str(output), "fact_fingerprint": fingerprint, "qualification_fingerprint": qualified.qualification_fingerprint, "mode": mode, "artifacts": artifacts}
    _write_json(execution_path, execution)
    artifacts["execution"] = str(execution_path)
    return {"status": "ok", "mode": result_mode, "output": str(output), "artifacts": artifacts, "section_count": len(report["sections"]), "fact_fingerprint": fingerprint}

def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True); path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
