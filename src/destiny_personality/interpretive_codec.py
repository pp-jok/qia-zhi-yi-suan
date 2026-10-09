"""Plain-data codec for audited interpretive reports."""

from typing import Dict, Optional

from .interpretive_models import (
    InterpretiveSignalProvenance,
    InterpretiveSystemProfile,
    InterpretiveSystemTopic,
    NarrativeSynthesisPacket,
)
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
                "kind": section.kind,
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


def encode_narrative_synthesis_packet(
    packet: NarrativeSynthesisPacket,
) -> Dict[str, object]:
    """Encode the bounded synthesis packet as deterministic plain data."""

    if not isinstance(packet, NarrativeSynthesisPacket):
        raise TypeError("NARRATIVE_SYNTHESIS_PACKET_REQUIRED")
    return {
        "bazi_profile": _encode_system_profile(packet.bazi_profile),
        "astrology_profile": _encode_system_profile(
            packet.astrology_profile
        ),
        "alignments": [
            {
                "topic": item.topic,
                "kind": item.kind,
                "bazi_signal_ids": list(item.bazi_signal_ids),
                "astrology_signal_ids": list(item.astrology_signal_ids),
                "interpretation": item.interpretation,
                "confidence": item.confidence,
                "limitations": list(item.limitations),
                "signal_provenance": _encode_provenance(
                    item.signal_provenance
                ),
                "bazi_source": _encode_system_topic(item.bazi_source),
                "astrology_source": _encode_system_topic(
                    item.astrology_source
                ),
            }
            for item in packet.alignments
        ],
        "tensions": [
            {
                "topic": item.topic,
                "left_pole": item.left_pole,
                "right_pole": item.right_pole,
                "contexts": list(item.contexts),
                "left_contexts": list(item.left_contexts),
                "right_contexts": list(item.right_contexts),
                "why_coexist": item.why_coexist,
                "integration": item.integration,
                "bazi_signal_ids": list(item.bazi_signal_ids),
                "astrology_signal_ids": list(item.astrology_signal_ids),
                "limitations": list(item.limitations),
                "signal_provenance": _encode_provenance(
                    item.signal_provenance
                ),
            }
            for item in packet.tensions
        ],
        "limitations": list(packet.limitations),
        "audit_refs": list(packet.audit_refs),
    }


def _encode_system_profile(
    profile: InterpretiveSystemProfile,
) -> Dict[str, object]:
    return {
        "system": profile.system,
        "signal_ids": list(profile.signal_ids),
        "topics": [
            _encode_system_topic(topic)
            for topic in profile.topics
        ],
        "limitations": list(profile.limitations),
        "audit_refs": list(profile.audit_refs),
    }


def _encode_system_topic(
    topic: Optional[InterpretiveSystemTopic],
) -> Optional[Dict[str, object]]:
    if topic is None:
        return None
    return {
        "topic": topic.topic,
        "directions": list(topic.directions),
        "signal_ids": list(topic.signal_ids),
        "interpretations": list(topic.interpretations),
        "mechanisms": list(topic.mechanisms),
        "likely_expressions": list(topic.likely_expressions),
        "contexts": list(topic.contexts),
        "limitations": list(topic.limitations),
        "signal_provenance": _encode_provenance(topic.signal_provenance),
    }


def _encode_provenance(
    items: tuple[InterpretiveSignalProvenance, ...],
) -> list[Dict[str, object]]:
    return [
        {
            "signal_id": item.signal_id,
            "system": item.system,
            "fact_refs": list(item.fact_refs),
            "traditional_rule_ref": item.traditional_rule_ref,
            "limitations": list(item.limitations),
            "mechanism": item.mechanism,
            "likely_expression": item.likely_expression,
            "contexts": list(item.contexts),
        }
        for item in items
    ]
