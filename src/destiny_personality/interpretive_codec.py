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
        },
    }
