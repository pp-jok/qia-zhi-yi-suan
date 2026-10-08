"""Plain-data codec for audited interpretive reports."""

from typing import Dict

from .interpretive_report import InterpretiveReport


def encode_interpretive_report(report: InterpretiveReport) -> Dict[str, object]:
    """Encode an interpretive report as deterministic JSON-compatible data."""

    if not isinstance(report, InterpretiveReport):
        raise TypeError("INTERPRETIVE_REPORT_REQUIRED")
    return {
        "schema_version": report.schema_version,
        "mode": report.mode,
        "title": report.title,
        "sections": [
            {
                "section_id": section.section_id,
                "title": section.title,
                "content": section.content,
                "signal_ids": list(section.signal_ids),
                "limitation": section.limitation,
                "signal_provenance": [
                    {
                        "signal_id": item.signal_id,
                        "system": item.system,
                        "fact_refs": list(item.fact_refs),
                        "traditional_rule_ref": item.traditional_rule_ref,
                        "limitations": list(item.limitations),
                    }
                    for item in section.signal_provenance
                ],
            }
            for section in report.sections
        ],
        "boundary_statement": report.boundary_statement,
        "audit_metadata": {
            "rule_bundle_refs": list(report.audit_metadata.rule_bundle_refs),
            "fact_refs": list(report.audit_metadata.fact_refs),
            "qualification_refs": list(report.audit_metadata.qualification_refs),
            "profile_audit_refs": list(
                report.audit_metadata.profile_audit_refs
            ),
            "fact_mode": report.audit_metadata.fact_mode,
            "birth_time_status": report.audit_metadata.birth_time_status,
            "time_sensitivity_reasons": list(
                report.audit_metadata.time_sensitivity_reasons
            ),
            "omitted_time_sensitive_claims": list(
                report.audit_metadata.omitted_time_sensitive_claims
            ),
        },
    }
