from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = PROJECT_ROOT / "destiny-personality"


def read_phase_c_file(relative_path: str) -> str:
    return (SKILL_ROOT / relative_path).read_text(encoding="utf-8")


def test_phase_c_resources_exist() -> None:
    required = (
        "schemas/capability-descriptor.md",
        "schemas/compatibility-evidence.md",
        "schemas/calculation-envelope.md",
        "schemas/deterministic-facts.md",
        "schemas/fact-comparison.md",
        "references/capability-protocol.md",
        "checklists/capability-preflight.md",
    )

    assert all((SKILL_ROOT / relative_path).is_file() for relative_path in required)


def test_capability_descriptor_separates_discovery_from_qualification() -> None:
    text = read_phase_c_file("schemas/capability-descriptor.md")
    for field in (
        "schema_version",
        "candidate_id",
        "category",
        "interface_type",
        "operation",
        "immutable_version",
        "locality",
        "availability",
        "authorization_state",
        "required_input_fields",
        "returned_fields",
        "engine_lineage",
        "independence_status",
        "qualification_status",
        "rejection_reasons",
    ):
        assert f"`{field}`" in text
    for category in ("time_normalization", "bazi", "astrology"):
        assert f"`{category}`" in text
    assert "Discovery is not qualification" in text


def test_compatibility_evidence_requires_exact_setting_matches() -> None:
    text = read_phase_c_file("schemas/compatibility-evidence.md")
    for field in (
        "config_ref",
        "expected",
        "candidate_setting",
        "evidence_ref",
        "status",
        "note",
    ):
        assert f"`{field}`" in text
    for status in ("exact", "unsupported", "unverified", "not_applicable"):
        assert f"`{status}`" in text
    assert "Only `exact` passes" in text
    assert "popularity" in text.lower()


def test_capability_preflight_orders_discovery_evidence_and_authorization() -> None:
    text = read_phase_c_file("checklists/capability-preflight.md")
    ordered = (
        "Confirm calculation configuration",
        "Discover available candidates",
        "Build one capability descriptor",
        "Verify every applicable methodology setting",
        "Check independence",
        "Obtain remote-data authorization",
        "Invoke the selected capability",
    )
    positions = [text.index(item) for item in ordered]
    assert positions == sorted(positions)
    assert "Do not install" in text


def test_calculation_envelope_records_call_without_promoting_raw_data() -> None:
    text = read_phase_c_file("schemas/calculation-envelope.md")
    for field in (
        "schema_version",
        "candidate_ref",
        "request_id",
        "response_id",
        "operation",
        "immutable_version",
        "methodology_version",
        "input_fields_sent",
        "parameters",
        "authorization_ref",
        "executed_at",
        "result_status",
        "raw_result_ref",
        "omitted_fields",
        "warnings",
        "boundary_sensitivity",
        "error",
    ):
        assert f"`{field}`" in text
    assert "untrusted data" in text
    assert "For a local call, `authorization_ref` is `not_applicable`." in text


def test_capability_protocol_requires_consent_minimization_and_safe_retry() -> None:
    text = read_phase_c_file("references/capability-protocol.md")
    for phrase in (
        "execution-scoped authorization",
        "exact fields",
        "retention",
        "minimum necessary",
        "read-only and idempotent",
        "CALCULATION_FATAL",
        "authorization_not_granted",
    ):
        assert phrase in text
    assert "credentials" in text
    assert "Do not repeat the same failed call" in text
    assert "## Common mistakes" in text


def test_execution_boundary_requires_consent_for_every_remote_recipient() -> None:
    text = read_phase_c_file("references/execution-boundaries.md")
    assert "any remote capability" in text
    assert "current execution" in text
    assert "Existing connection" in text
    assert "minimum necessary" in text


def test_deterministic_fact_schema_covers_all_systems_and_stable_only() -> None:
    text = read_phase_c_file("schemas/deterministic-facts.md")
    for field in (
        "schema_version",
        "fact_mode",
        "methodology_versions",
        "provenance_refs",
        "normalized_time",
        "bazi",
        "astrology",
        "validation_summary",
        "source_pillars",
    ):
        assert f"`{field}`" in text
    for forbidden_when_unknown in (
        "hour_pillar",
        "Ascendant",
        "MC",
        "house_cusps",
        "hour-pillar provenance",
    ):
        assert forbidden_when_unknown in text
    assert "Do not derive" in text


def test_node_ambiguity_remains_a_configuration_gap() -> None:
    text = read_phase_c_file("schemas/deterministic-facts.md")
    assert "core.node: true" in text
    assert "optional" in text
    assert "canonical fact identifier" in text
    assert "`CONFIG_GAP`" in text
    assert "must not require" in text


def test_fact_comparison_forbids_repair_and_requires_policy() -> None:
    text = read_phase_c_file("schemas/fact-comparison.md")
    for field in (
        "schema_version",
        "primary_packet_ref",
        "secondary_packet_ref",
        "independence_evidence",
        "comparison_policy_version",
        "field_results",
        "material_conflicts",
        "comparison_status",
    ):
        assert f"`{field}`" in text
    assert "before the secondary invocation" in text
    assert "Do not average" in text
    assert "external_result_conflict" in text


def test_fact_comparison_defines_complete_tiered_confirmation_policy() -> None:
    text = read_phase_c_file("schemas/fact-comparison.md")
    normalized = " ".join(text.split())

    assert (
        "ordinary case requires one qualified result for each required logical "
        "category" in normalized
    )
    for trigger in (
        "warning, uncertainty, or boundary sensitivity",
        "historical-time ambiguity",
        "within a configured boundary margin",
        "policy-recognized anomaly",
    ):
        assert trigger in normalized
    assert "requires a second qualified result" in normalized
    assert "One capability may cover multiple logical categories" in normalized
    assert "capability and provenance" in normalized


def test_deterministic_fact_packet_lifecycle_matches_stage_gates() -> None:
    text = read_phase_c_file("schemas/deterministic-facts.md")
    normalized = " ".join(text.split())

    normalized_step = (
        "At `FACTS_NORMALIZED`, mechanically produce a `deterministic-facts-v1` "
        "packet from accepted calculation envelopes."
    )
    validated_step = (
        "At `FACTS_VALIDATED`, accept that packet only after it passes its own "
        "structure, methodology, provenance, and required independent-comparison "
        "checks."
    )
    assert normalized_step in normalized
    assert validated_step in normalized
    assert normalized.index(normalized_step) < normalized.index(validated_step)
    assert "envelope has passed fact validation" not in normalized


def test_failure_policy_distinguishes_candidate_absence_and_mismatch() -> None:
    text = read_phase_c_file("references/failure-policy.md")
    assert "no candidate exists" in text
    assert "all discovered candidates" in text
    assert "authorization_not_granted" in text
    assert "external_result_conflict" in text
    assert text.index("`CONFIG_GAP`") < text.index("`CAPABILITY_GAP`")


def test_execution_report_records_phase_c_state_without_raw_secret_duplication() -> None:
    text = read_phase_c_file("schemas/execution-report.md")
    for field in (
        "candidate_id",
        "qualification_status",
        "independence_status",
        "authorization_state",
        "invocation_status",
        "subtype",
        "fact_packet_ref",
    ):
        assert f"`{field}`" in text
    assert "accepted operations" in text
    assert "Exclude raw sensitive payloads and credentials from the report." in text
    assert "never a credential or reusable secret" in text


def test_router_links_all_phase_c_resources_and_preserves_config_stop() -> None:
    text = read_phase_c_file("SKILL.md")
    for path in (
        "schemas/capability-descriptor.md",
        "schemas/compatibility-evidence.md",
        "schemas/calculation-envelope.md",
        "schemas/deterministic-facts.md",
        "schemas/fact-comparison.md",
        "references/capability-protocol.md",
        "checklists/capability-preflight.md",
    ):
        assert f"]({path})" in text
    assert "Phase C compatibility evidence is not present" not in text
    assert "exact deterministic lookup tables" in text


def test_methodology_index_marks_phase_c_contracts_present_and_values_missing() -> None:
    text = read_phase_c_file("references/methodology-index.md")
    assert "schemas/deterministic-facts.md" in text
    assert "schemas/fact-comparison.md" in text
    for missing in (
        "hidden-stem",
        "Ten-God",
        "Bazi-relation",
        "astrology-dignity",
        "True North Node",
        "boundary-distance",
        "comparison tolerances",
    ):
        assert missing in text


def test_source_plan_distinguishes_candidate_absence_from_evidence_mismatch() -> None:
    text = (
        PROJECT_ROOT
        / "destiny_personality_skill_docs_v2_2"
        / "10_CODEX_IMPLEMENTATION_PLAN_V2_2.md"
    ).read_text(encoding="utf-8")
    normalized = " ".join(text.split())

    assert "`CAPABILITY_GAP` when no candidate exists" in normalized
    assert "all discovered candidates lack exact evidence" in normalized
    assert "`METHODOLOGY_VERSION_MISMATCH`" in normalized
    assert (
        "If no qualified runtime calculation capability is available"
        not in normalized
    )
