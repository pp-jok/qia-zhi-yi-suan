import re
from pathlib import Path

import yaml


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = PROJECT_ROOT / "destiny-personality"


def read_skill_file(relative_path: str) -> str:
    return (SKILL_ROOT / relative_path).read_text(encoding="utf-8")


def test_skill_scaffold_and_ui_metadata_exist() -> None:
    required = (
        "SKILL.md",
        "agents/openai.yaml",
        "references",
        "configs",
        "schemas",
        "checklists",
    )
    assert all((SKILL_ROOT / path).exists() for path in required)

    skill_text = read_skill_file("SKILL.md")
    frontmatter = yaml.safe_load(skill_text.split("---", 2)[1])
    assert frontmatter["name"] == "destiny-personality"
    assert "portrait" in frontmatter["description"]
    assert "facts_only" in frontmatter["description"]
    assert "audit" in frontmatter["description"]

    metadata = yaml.safe_load(read_skill_file("agents/openai.yaml"))
    assert set(metadata) == {"interface"}
    assert "$destiny-personality" in metadata["interface"]["default_prompt"]


def test_skill_contains_no_executable_or_fixed_tool_dependency() -> None:
    assert not (SKILL_ROOT / "scripts").exists()
    assert not (SKILL_ROOT / "assets").exists()
    assert not list(SKILL_ROOT.rglob("*.py"))
    assert not list(SKILL_ROOT.rglob("*.pyc"))
    assert not list(SKILL_ROOT.rglob("*.so"))
    assert not list(SKILL_ROOT.rglob("*.dylib"))
    assert not list(SKILL_ROOT.rglob("*.dll"))

    metadata = yaml.safe_load(read_skill_file("agents/openai.yaml"))
    assert "dependencies" not in metadata


def test_birth_input_contract_covers_minimum_input_and_unknown_time() -> None:
    text = read_skill_file("schemas/birth-input.md")
    for field in (
        "birth_date",
        "birth_time",
        "birth_place",
        "timezone_name",
        "latitude",
        "longitude",
    ):
        assert f"`{field}`" in text
    assert "unknown" in text
    assert "stable_only" in text
    assert "BIRTH_INPUT_ERROR" in text
    assert "compact-or-structured-birth-input-v1" in text
    assert "1986.5.25.11:55 北京 男" in text
    assert "unambiguous compact input" in text
    assert "do not ask for confirmation" in text
    assert "sex" in text
    assert "must not infer" in text


def test_execution_report_contract_covers_all_modes_and_fields() -> None:
    text = read_skill_file("schemas/execution-report.md")
    for mode in ("portrait", "facts_only", "audit"):
        assert f"`{mode}`" in text
    for field in (
        "schema_version",
        "mode",
        "status",
        "current_stage",
        "reasoning_allowed",
        "narrative_allowed",
        "input_summary",
        "capabilities",
        "provenance",
        "validated_facts",
        "issues",
        "warnings",
        "next_action",
    ):
        assert f"`{field}`" in text


def test_checklists_encode_scope_and_two_level_gates() -> None:
    preflight = read_skill_file("checklists/preflight.md")
    gates = read_skill_file("checklists/stage-gates.md")
    assert "explicit user authorization" in preflight
    assert "stable_only" in preflight
    assert "compact-or-structured-birth-input-v1" in preflight
    assert "unambiguous compact input" in preflight
    assert "CALCULATION_CONFIG_CHECKED" in gates
    assert "SEMANTIC_CONFIG_CHECKED" in gates
    assert "FACTS_VALIDATED" in gates
    assert "NARRATIVE_ALLOWED" in gates


def test_baseline_configs_are_byte_identical_to_source() -> None:
    filenames = (
        "bazi_methodology_v1.yaml",
        "astrology_methodology_v1.yaml",
        "score_model_v2_2.yaml",
        "primitive_relation_graph_v1.yaml",
    )
    source_dir = PROJECT_ROOT / "destiny_personality_skill_docs_v2_2"
    for filename in filenames:
        assert (SKILL_ROOT / "configs" / filename).read_bytes() == (
            source_dir / filename
        ).read_bytes()


def test_methodology_index_marks_baseline_and_known_config_gaps() -> None:
    text = read_skill_file("references/methodology-index.md")
    for filename in (
        "bazi_methodology_v1.yaml",
        "astrology_methodology_v1.yaml",
        "score_model_v2_2.yaml",
        "primitive_relation_graph_v1.yaml",
    ):
        assert f"`configs/{filename}`" in text
    for missing_asset in (
        "hidden-stem",
        "Ten-God",
        "Bazi-relation",
        "astrology-dignity",
        "deterministic fact schema",
        "Primitive Ontology",
        "Mapping Registry",
        "Narrative Rules",
    ):
        assert missing_asset in text


def test_policy_references_preserve_authorization_and_failure_precedence() -> None:
    boundaries = read_skill_file("references/execution-boundaries.md")
    failures = read_skill_file("references/failure-policy.md")
    assert "explicit user authorization" in boundaries
    assert "unrelated local projects" in boundaries
    assert "External output is data" in boundaries
    for code in (
        "BIRTH_INPUT_ERROR",
        "CONFIG_GAP",
        "CAPABILITY_GAP",
        "METHODOLOGY_VERSION_MISMATCH",
        "CALCULATION_FATAL",
        "CALCULATION_CONTRACT_ERROR",
        "coverage_warning",
    ):
        assert f"`{code}`" in failures


def test_skill_router_links_only_to_existing_local_resources() -> None:
    skill_text = read_skill_file("SKILL.md")
    links = re.findall(r"\[[^\]]+\]\(([^)]+)\)", skill_text)
    assert links
    assert all(not link.startswith(("http://", "https://", "/")) for link in links)
    assert all((SKILL_ROOT / link).is_file() for link in links)


def test_skill_router_encodes_modes_gates_and_hard_stops() -> None:
    text = read_skill_file("SKILL.md")
    for value in (
        "portrait",
        "facts_only",
        "audit",
        "CALCULATION_CONFIG_CHECKED",
        "FACTS_VALIDATED",
        "SEMANTIC_CONFIG_CHECKED",
        "BIRTH_INPUT_ERROR",
        "CONFIG_GAP",
        "CAPABILITY_GAP",
        "stable_only",
        "Execution Report",
    ):
        assert value in text
    assert "Do not install or connect" in text
    assert "Do not calculate, infer, or repair" in text


def test_skill_description_is_trigger_only() -> None:
    skill_text = read_skill_file("SKILL.md")
    frontmatter = yaml.safe_load(skill_text.split("---", 2)[1])

    assert "core_concise" in frontmatter["description"]


def test_legacy_long_form_v2_is_explicitly_marked() -> None:
    skill = read_skill_file("SKILL.md")
    blueprint = read_skill_file("references/long-form-report-blueprint.md")

    assert "legacy-long-form-v2" in skill
    assert "legacy-long-form-v2" in blueprint
    assert "renderer" in blueprint


def test_core_profile_contract_separates_fact_and_semantic_assurance() -> None:
    contract = read_skill_file("schemas/core-destiny-profile.md")
    for field in (
        "schema_version",
        "core_profile_id",
        "fact_packet_refs",
        "fact_assurance",
        "semantic_model_assurance",
        "semantic_model_versions",
        "bazi_primitive_candidates",
        "astrology_primitive_candidates",
        "primitive_states",
        "cross_system_alignment",
        "dominant_signatures",
        "core_dynamics",
        "shadow_mature_forms",
        "fate_themes",
        "archetype",
        "contradictions",
        "limitations",
        "unresolved_questions",
        "audit_trail",
    ):
        assert f"`{field}`" in contract
    assert "`project_semantic_verified`" in contract
    assert "`project_semantic_partial`" in contract
    assert "does not upgrade fact assurance" in contract
    assert "stopped execution artifact" in contract


def test_core_profile_route_and_report_plan_are_auditable() -> None:
    skill = read_skill_file("SKILL.md")
    execution_report = read_skill_file("schemas/execution-report.md")
    report_plan = read_skill_file("schemas/report-plan.md")
    checklist = read_skill_file("checklists/core-profile.md")

    assert "CORE_PROFILE_VALIDATED" in skill
    assert "REPORT_PLAN_VALIDATED" in skill
    for field in (
        "core_profile_ref",
        "semantic_model_assurance",
        "semantic_model_versions",
        "report_plan_ref",
    ):
        assert f"`{field}`" in execution_report
    assert "`profile_refs`" in report_plan
    assert "bare Fact Packet" in report_plan
    assert "normalized-equivalent Profile" in checklist


def test_primitive_foundation_contracts_are_distributable() -> None:
    ontology = read_skill_file("schemas/primitive-ontology.md")
    resolution = read_skill_file("schemas/primitive-state-resolution.md")
    template = read_skill_file("examples/primitive-foundation-template.md")

    for field in (
        "schema_version",
        "ontology_version",
        "primitives",
        "primitive_id",
        "canonical_name",
        "definition",
        "high_expression",
        "low_expression",
        "aliases",
        "limitations",
    ):
        assert f"`{field}`" in ontology
    assert "globally unambiguous" in ontology
    assert "P###" in ontology

    for field in (
        "resolution_version",
        "score_model_version",
        "states",
        "invariants",
        "rules",
        "rule_id",
        "target_state",
        "priority",
        "requires_explicit_reverse_evidence",
        "evidence_requirements",
        "thresholds",
    ):
        assert f"`{field}`" in resolution
    for state in ("supported_high", "supported_low", "mixed", "unknown"):
        assert f"`{state}`" in resolution
    for invariant in (
        "no_evidence_state",
        "low_requires_explicit_reverse_evidence",
        "unknown_is_not_low",
        "preserve_system_salience",
        "cross_system_validation_changes_trait_salience",
        "tension_reduces_trait_salience",
    ):
        assert f"`{invariant}`" in resolution
    for result_field in (
        "bazi_salience",
        "astrology_salience",
        "evidence_stability",
        "evidence_refs",
        "resolution_rule_ref",
    ):
        assert f"`{result_field}`" in resolution

    assert "must not be loaded as runtime configuration" in template
    assert "<PROJECT_OWNED_NAME>" in template


def test_no_primitive_placeholder_is_a_production_config() -> None:
    for filename in (
        "primitive_ontology_v1.yaml",
        "primitive_state_resolution_v1.yaml",
    ):
        assert not (SKILL_ROOT / "configs" / filename).exists()


def test_skill_routes_gate_1a_without_claiming_semantic_completion() -> None:
    skill = read_skill_file("SKILL.md")
    gates = read_skill_file("checklists/stage-gates.md")
    methodology = read_skill_file("references/methodology-index.md")

    for path in (
        "schemas/primitive-ontology.md",
        "schemas/primitive-state-resolution.md",
        "examples/primitive-foundation-template.md",
    ):
        assert f"]({path})" in skill
    assert "do not treat the template as configuration" in skill.lower()
    assert "Gate 1 remains incomplete" in skill

    assert gates.index("primitive_ontology_v1.yaml") < gates.index(
        "primitive_state_resolution_v1.yaml"
    )
    assert "remaining semantic assets" in gates
    assert "Gate 1A contracts are present" in methodology
    assert "production Primitive assets are absent" in methodology
    assert "`CONFIG_GAP`" in methodology


def test_primitive_contracts_define_exact_configuration_error_mapping() -> None:
    for relative_path in (
        "schemas/primitive-ontology.md",
        "schemas/primitive-state-resolution.md",
    ):
        text = read_skill_file(relative_path)
        for phrase in (
            "Missing asset or required field",
            "`CONFIG_GAP`",
            "Malformed YAML",
            "`CONFIG_PARSE_ERROR`",
            "Wrong container or scalar type",
            "`CONFIG_TYPE_ERROR`",
            "Unsupported schema or cross-file version",
            "`CONFIG_VERSION_MISMATCH`",
            "Invalid, ambiguous, duplicate, or unknown value",
            "`CONFIG_VALUE_ERROR`",
            "dot-separated field path",
        ):
            assert phrase in text


def test_mapping_registry_contract_is_distributable() -> None:
    contract = read_skill_file("schemas/context-aware-mapping-registry.md")
    template = read_skill_file("examples/mapping-registry-template.md")

    for filename in (
        "bazi_mapping_registry_v1.yaml",
        "astrology_mapping_registry_v1.yaml",
    ):
        assert f"`{filename}`" in contract
        assert f"`{filename}`" in template
    for field in (
        "schema_version",
        "registry_version",
        "source_system",
        "methodology_version",
        "fact_schema_version",
        "score_model_version",
        "ontology_version",
        "rules",
        "interactions",
        "rule_id",
        "priority",
        "primary_condition",
        "context",
        "outputs",
        "modifiers",
        "limitations",
        "primitive_id",
        "direction",
        "salience",
        "interaction_id",
        "requires",
        "produces",
    ):
        assert f"`{field}`" in contract
    for phrase in (
        "non-empty `context`",
        "same registry",
        "source-system isolation",
        "Missing asset or required field",
        "`CONFIG_GAP`",
        "Malformed YAML",
        "`CONFIG_PARSE_ERROR`",
        "Wrong container, scalar, mapping-key, or nested declarative type",
        "`CONFIG_TYPE_ERROR`",
        "Unsupported schema, ontology, methodology, fact-schema, or score-model reference",
        "`CONFIG_VERSION_MISMATCH`",
        "Invalid, duplicate, unresolved, or unknown value",
        "`CONFIG_VALUE_ERROR`",
        "dot-separated field path",
    ):
        assert phrase in contract

    assert "must not be loaded as runtime configuration" in template
    assert "must not be copied" in template
    assert "<PROJECT_OWNED_DIRECTION>" in template


def test_no_mapping_placeholder_is_a_production_config() -> None:
    for filename in (
        "bazi_mapping_registry_v1.yaml",
        "astrology_mapping_registry_v1.yaml",
    ):
        assert not (SKILL_ROOT / "configs" / filename).exists()


def test_skill_routes_gate_1b_without_claiming_semantic_completion() -> None:
    skill = read_skill_file("SKILL.md")
    gates = read_skill_file("checklists/stage-gates.md")
    methodology = read_skill_file("references/methodology-index.md")

    for path in (
        "schemas/context-aware-mapping-registry.md",
        "examples/mapping-registry-template.md",
    ):
        assert f"]({path})" in skill
    assert "must not invent mapping" in skill.lower()
    assert "source-system isolation" in skill
    assert "Gate 1 remains incomplete" in skill

    assert gates.index("primitive_state_resolution_v1.yaml") < gates.index(
        "bazi_mapping_registry_v1.yaml"
    )
    assert gates.index("bazi_mapping_registry_v1.yaml") < gates.index(
        "astrology_mapping_registry_v1.yaml"
    )
    assert "same-registry" in gates
    assert "Gate 1B contracts are present" in methodology
    assert "production Mapping Registry assets are absent" in methodology
    assert "`CONFIG_GAP`" in methodology


def test_dimension_coverage_contract_and_route_are_distributable() -> None:
    skill = read_skill_file("SKILL.md")
    gates = read_skill_file("checklists/stage-gates.md")
    contract = read_skill_file("schemas/dimension-coverage-policy.md")
    template = read_skill_file("examples/dimension-coverage-template.md")
    for path in ("schemas/dimension-coverage-policy.md", "examples/dimension-coverage-template.md"):
        assert f"]({path})" in skill
    for field in ("dimension_count", "dimensions", "dimension_id", "canonical_name", "primitive_refs", "coverage_policy", "threshold_status", "coverage_metric", "complete_threshold", "partial_threshold", "partial_portrait_allowed", "partial_status", "warning_code", "missing_config_code", "dimension_requirements", "minimum_supported_primitives"):
        assert f"`{field}`" in contract
    for value in ("`12`", "`provisional`", "`coverage_warning`", "`CONFIG_GAP`", "`partial`"):
        assert value in contract
    for code in ("CONFIG_GAP", "CONFIG_PARSE_ERROR", "CONFIG_TYPE_ERROR", "CONFIG_VERSION_MISMATCH", "CONFIG_VALUE_ERROR"):
        assert f"`{code}`" in contract
    assert "only after `SEMANTIC_CONFIG_CHECKED`" in contract
    assert "must not be loaded as runtime configuration" in template
    assert "<PROJECT_OWNED_COMPLETE_THRESHOLD>" in template
    assert gates.index("astrology_mapping_registry_v1.yaml") < gates.index("dimension_coverage_policy_v1.yaml")
    assert "configuration failure is never `coverage_warning`" in gates
    assert not (SKILL_ROOT / "configs" / "dimension_coverage_policy_v1.yaml").exists()


def test_narrative_contract_and_semantic_bundle_route_are_distributable() -> None:
    skill = read_skill_file("SKILL.md")
    gates = read_skill_file("checklists/stage-gates.md")
    contract = read_skill_file("schemas/narrative-rules.md")
    template = read_skill_file("examples/narrative-rules-template.md")
    for path in ("schemas/narrative-rules.md", "examples/narrative-rules-template.md"):
        assert f"]({path})" in skill
    for invariant in ("complete_ir_required", "narrative_changes_core_claims", "unsupported_claims_allowed", "unknown_may_be_rendered_as_certain", "secondary_may_be_promoted", "chart_anchor_required", "traditional_interpretation_claimed_scientific"):
        assert f"`{invariant}`" in contract
    assert "does not contain prose templates" in contract
    assert "must not be loaded as runtime configuration" in template
    assert gates.index("dimension_coverage_policy_v1.yaml") < gates.index("narrative_rules_v1.yaml")
    assert "semantic bundle acceptance never opens `REASONING_ALLOWED`" in gates
    assert not (SKILL_ROOT / "configs" / "narrative_rules_v1.yaml").exists()


def test_semantic_candidate_release_workflow_is_human_controlled() -> None:
    skill = read_skill_file("SKILL.md")
    checklist = read_skill_file("checklists/semantic-candidate-release.md")

    assert "](checklists/semantic-candidate-release.md)" in skill
    assert "does not require or invoke the development reference CLI" in skill
    assert "candidate -> validated -> reviewed -> approved -> promoted" in checklist
    for phrase in (
        "explicit project-owner approval",
        "must not generate",
        "must not copy",
        "must not repair",
        "does not open `REASONING_ALLOWED`",
    ):
        assert phrase in checklist

    for phrase in (
        "same `bundle_sha256`",
        "returns the asset set to `candidate`",
        "proves byte identity only",
        "does not prove approval",
        "Only a stable validation report may advance to human review",
        "configuration files changed during validation",
        "retry with an immutable candidate snapshot",
    ):
        assert phrase in checklist


def test_semantic_candidate_workflow_does_not_add_production_assets() -> None:
    assert {path.name for path in (SKILL_ROOT / "configs").iterdir()} == {
        "astrology_methodology_v1.yaml",
        "bazi_methodology_v1.yaml",
        "primitive_relation_graph_v1.yaml",
        "score_model_v2_2.yaml",
    }


def test_candidate_core_pipeline_is_not_a_default_user_report_route() -> None:
    skill = read_skill_file("SKILL.md")

    assert "Candidate Core Portrait Preview" in skill
    assert "explicitly selected" in skill
    assert "does not enter the default legacy route" in skill


def test_canonical_fact_vocabulary_contract_is_distributable() -> None:
    skill = read_skill_file("SKILL.md")
    gates = read_skill_file("checklists/stage-gates.md")
    methodology = read_skill_file("references/methodology-index.md")
    contract = read_skill_file("schemas/canonical-fact-vocabulary.md")
    template = read_skill_file("examples/canonical-fact-vocabulary-template.md")

    for path in (
        "schemas/canonical-fact-vocabulary.md",
        "examples/canonical-fact-vocabulary-template.md",
    ):
        assert f"]({path})" in skill
    for field in (
        "schema_version",
        "vocabulary_version",
        "methodology_versions",
        "categories",
        "entries",
        "canonical_id",
        "aliases",
    ):
        assert f"`{field}`" in contract
    for category in (
        "bazi_stem",
        "bazi_branch",
        "bazi_ten_god",
        "bazi_relation",
        "astrology_body",
        "astrology_sign",
        "astrology_aspect",
        "astrology_angle",
        "astrology_dignity",
        "astrology_node",
    ):
        assert f"`{category}`" in contract
    for code in (
        "CONFIG_GAP",
        "CONFIG_PARSE_ERROR",
        "CONFIG_TYPE_ERROR",
        "CONFIG_VERSION_MISMATCH",
        "CONFIG_VALUE_ERROR",
    ):
        assert f"`{code}`" in contract
    assert "trimming and Unicode-preserving case folding" in contract
    assert "does not define the True North Node output rule" in contract
    assert "must not be loaded as runtime configuration" in template
    assert "<PROJECT_OWNED_CANONICAL_ID>" in template
    assert gates.index("canonical_fact_vocabulary_v1.yaml") < gates.index(
        "deterministic lookup tables"
    )
    assert "Canonical Fact Vocabulary contract is present" in methodology
    assert not (SKILL_ROOT / "configs" / "canonical_fact_vocabulary_v1.yaml").exists()


def test_calculation_contract_framework_is_distributable_and_ordered() -> None:
    skill = read_skill_file("SKILL.md")
    gates = read_skill_file("checklists/stage-gates.md")
    resources = (
        ("bazi-deterministic-tables", "bazi_deterministic_tables_v1.yaml"),
        ("astrology-dignity-table", "astrology_dignity_table_v1.yaml"),
        ("astrology-node-policy", "astrology_node_policy_v1.yaml"),
        ("fact-comparison-policy", "fact_comparison_policy_v1.yaml"),
    )
    positions = []
    for stem, production_name in resources:
        contract_path = f"schemas/{stem}.md"
        template_path = f"examples/{stem}-template.md"
        contract = read_skill_file(contract_path)
        template = read_skill_file(template_path)
        assert f"]({contract_path})" in skill
        assert f"]({template_path})" in skill
        assert production_name in contract
        assert "CONFIG_GAP" in contract
        assert "must not be loaded as runtime configuration" in template
        assert not (SKILL_ROOT / "configs" / production_name).exists()
        positions.append(gates.index(production_name))
    assert positions == sorted(positions)
    assert gates.index("canonical_fact_vocabulary_v1.yaml") < positions[0]

    node_contract = read_skill_file("schemas/astrology-node-policy.md")
    for field in (
        "included", "phase", "aspect_participation",
        "dignity_participation", "weight_role", "time_sensitive",
    ):
        assert f"`{field}`" in node_contract

    comparison_contract = read_skill_file("schemas/fact-comparison-policy.md")
    for field in (
        "triggers", "logical_categories", "boundary_margins",
        "canonical_precision", "tolerances", "representation_equivalences",
    ):
        assert f"`{field}`" in comparison_contract


def test_methodology_index_routes_every_calculation_contract_without_values() -> None:
    text = read_skill_file("references/methodology-index.md")
    for path in (
        "schemas/bazi-deterministic-tables.md",
        "schemas/astrology-dignity-table.md",
        "schemas/astrology-node-policy.md",
        "schemas/fact-comparison-policy.md",
    ):
        assert f"`{path}`" in text
    assert "All calculation configuration contracts are present" in text
    assert "production values remain absent" in text
    assert "CALCULATION_CONFIG_CHECKED" in text


def test_skill_routes_controlled_portrait_and_preserves_strict_modes() -> None:
    skill = read_skill_file("SKILL.md")
    preflight = read_skill_file("checklists/preflight.md")
    gates = read_skill_file("checklists/stage-gates.md")
    capability = read_skill_file("checklists/capability-preflight.md")

    for profile in ("controlled_inference", "strict"):
        assert f"`{profile}`" in skill
        assert f"`{profile}`" in preflight
    assert "`portrait` defaults to `controlled_inference`" in skill
    assert "`facts_only` requires `strict`" in skill
    assert "strict audit claims require `strict`" in skill

    for stage in (
        "CALCULATION_BASELINE_CHECKED",
        "FACT_BASIS_VALIDATED",
        "CONTROLLED_INFERENCE_CHECKED",
        "CONTROLLED_INFERENCE_ALLOWED",
        "REPORT_VALIDATED",
    ):
        assert f"`{stage}`" in gates
    assert gates.index("## Controlled portrait branch") < gates.index(
        "## Strict branch"
    )
    assert "four frozen baseline YAML files" in gates
    assert "five advanced calculation assets" in gates
    assert "Confirm the selected execution profile" in capability
    assert "controlled profile" in capability
    assert "strict profile" in capability

    for legacy_stage in (
        "CALCULATION_CONFIG_CHECKED",
        "FACTS_VALIDATED",
        "SEMANTIC_CONFIG_CHECKED",
        "REASONING_ALLOWED",
        "NARRATIVE_ALLOWED",
    ):
        assert f"`{legacy_stage}`" in gates


def test_controlled_inference_contract_preserves_fact_boundary() -> None:
    skill = read_skill_file("SKILL.md")
    contract = read_skill_file("schemas/controlled-inference.md")
    checklist = read_skill_file("checklists/controlled-inference.md")
    facts = read_skill_file("schemas/deterministic-facts.md")
    boundaries = read_skill_file("references/execution-boundaries.md")

    for path in (
        "schemas/controlled-inference.md",
        "checklists/controlled-inference.md",
    ):
        assert f"]({path})" in skill
    for assurance in ("project_verified", "capability_reported", "none"):
        assert f"`{assurance}`" in contract
    for field in (
        "claim_id",
        "claim",
        "claim_type",
        "systems",
        "basis_refs",
        "confidence",
        "limitations",
    ):
        assert f"`{field}`" in contract
    for claim_type in ("observation", "inference", "synthesis"):
        assert f"`{claim_type}`" in contract
    for rule in (
        "must not calculate chart facts",
        "at least one fact-basis reference",
        "at least two fact-basis references",
        "both `bazi` and `astrology`",
        "must not promote `capability_reported`",
        "omit every node claim",
        "Unknown or omitted facts are not negative evidence",
    ):
        assert rule in contract or rule in checklist
    assert "not a `deterministic-facts-v1` packet" in facts
    assert "Interpretation may vary; chart facts may not." in boundaries


def test_portrait_report_contract_has_fixed_sections_and_disclosures() -> None:
    skill = read_skill_file("SKILL.md")
    contract = read_skill_file("schemas/portrait-report.md")
    blueprint = read_skill_file("references/long-form-report-blueprint.md")
    checklist = read_skill_file("checklists/portrait-report.md")
    execution = read_skill_file("schemas/execution-report.md")
    paths = (
        "schemas/portrait-report.md",
        "references/long-form-report-blueprint.md",
        "checklists/portrait-report.md",
    )
    for path in paths:
        assert f"]({path})" in skill

    sections = (
        "front_matter",
        "prologue",
        "part_1_chart_voice",
        "part_2_personality_formation",
        "part_3_shadow_protection_and_fate",
        "part_4_integrated_portrait",
        "finale",
        "execution_notes",
    )
    positions = [contract.index(f"`{section}`") for section in sections]
    assert positions == sorted(positions)
    for field in (
        "schema_version",
        "execution_profile",
        "fact_assurance",
        "methodology_versions",
        "capability_provenance",
        "omitted_facts",
        "configuration_limitations",
        "format_profile",
        "input_profile",
        "content_standard",
        "sections",
    ):
        assert f"`{field}`" in contract
    assert "`portrait-report-v2`" in contract
    assert "`long-form-personality-book-v2`" in contract
    assert "`compact-or-structured-birth-input-v1`" in contract
    assert "`reader-first-depth-v2`" in contract
    assert "`insufficient_basis`" in contract
    assert "traditional and inferential" in contract
    assert "scientific diagnosis" in contract
    assert "Every analytical section" in checklist
    assert "basis_refs" in checklist

    chapter_positions = [
        blueprint.index(f"`chapter_{index:02d}` -") for index in range(1, 57)
    ]
    assert chapter_positions == sorted(chapter_positions)
    for part_count in (
        "Part I: 15 chapters",
        "Part II: 9 chapters",
        "Part III: 16 chapters",
        "Part IV: 16 chapters",
    ):
        assert part_count in blueprint
    for dimension in (
        "first_cross_system_synthesis",
        "judgment_right",
        "expression_right",
        "choice_and_life_narrative_right",
        "interpretation_right",
        "public_authorship_right",
        "primary_defense",
        "relationship_fate_tension",
        "five_fate_questions",
    ):
        assert f"`{dimension}`" in blueprint
    assert "short paragraphs" in blueprint
    assert "reader-facing prose" in blueprint
    assert "audit appendix" in blueprint
    for layer in (
        "evidence layer",
        "mechanism layer",
        "lived-expression layer",
        "integration layer",
    ):
        assert layer in blueprint
    assert "three to five short paragraphs" in contract
    assert "chapter-level depth audit" in checklist
    assert "paraphrase padding" in checklist
    assert "depth audit" in skill
    assert "`reference_traditional_interpretation`" in contract
    assert "user-approved reference" in blueprint
    assert "must not override a conflicting calculated fact" in contract
    assert "must not promote fact assurance" in checklist
    assert "reference-derived interpretation" in skill
    assert "source qualification belongs in the audit appendix" in contract
    assert "one dominant archetype" in blueprint
    assert "11,000 to 15,000" in blueprint
    assert "120 CJK content characters" in blueprint
    assert "judgment right" in blueprint
    assert "expression right" in blueprint
    assert "choice and life-narrative right" in blueprint
    assert "interpretation right" in blueprint
    assert "public authorship right" in blueprint
    assert "prologue, chapter 15, chapter 41, and finale" in blueprint
    assert "internal workflow language" in checklist
    assert "reader-facing length calibration" in checklist
    assert "five agency-related chapters" in checklist
    assert "reader-facing prose must not narrate" in skill
    assert "reader-first-depth-v2" in skill
    assert "do not satisfy the strict Dimension Coverage Policy" in contract

    for field in (
        "execution_profile",
        "fact_assurance",
        "analysis_basis",
        "configuration_limitations",
        "inference_disclosure",
    ):
        assert f"`{field}`" in execution
    assert "`current_stage: REPORT_VALIDATED`" in execution
    assert "profile-scoped" in execution
    assert "does not claim `SEMANTIC_CONFIG_CHECKED`" in execution


def test_failure_policy_distinguishes_controlled_limitations_from_fatal_gaps() -> None:
    failures = read_skill_file("references/failure-policy.md")
    methodology = read_skill_file("references/methodology-index.md")
    runtime = (
        PROJECT_ROOT
        / "destiny_personality_skill_docs_v2_2"
        / "09_PRODUCTION_RUNTIME_RULES.md"
    ).read_text(encoding="utf-8")

    for code in ("CONFIG_LIMITATION", "INFERENCE_GUARD_ERROR"):
        assert f"`{code}`" in failures
        assert f"`{code}`" in runtime
    assert "non-fatal warning" in failures
    assert "safely omitted" in failures
    assert "required by an emitted claim" in failures
    assert "remains `CONFIG_GAP`" in failures
    assert "does not satisfy `CALCULATION_CONFIG_CHECKED`" in failures
    assert "Strict production remains closed" in methodology
    assert "controlled business testing may proceed" in methodology
    assert "qualified external calculation capability" in methodology
    assert "safe omission" in runtime
    assert "strict profile" in runtime
    assert "controlled profile" in runtime


def test_business_test_checklist_defines_cross_agent_quality_gate() -> None:
    skill = read_skill_file("SKILL.md")
    checklist = read_skill_file("checklists/business-test.md")
    assert "](checklists/business-test.md)" in skill
    for criterion in (
        "fact fidelity",
        "anchor coverage",
        "framework adherence",
        "disclosure completeness",
        "section completeness",
        "harmful overclaiming",
    ):
        assert criterion in checklist
    assert "identical prose is not required" in checklist
    assert "at least two agents" in checklist
    assert "zero known hard-fact errors" in checklist
    assert "100% of analytical claims" in checklist
    assert "all fifty-six chapter dimensions" in checklist
    assert "four-part long-form structure" in checklist
    assert "chapter depth" in checklist
    assert "at least three distinct analytical moves" in checklist
    assert "paraphrase padding" in checklist
    assert "reader-first-depth-v2" in checklist
    assert "11,000–15,000" in checklist
    assert "five agency-related chapters" in checklist
    assert "one dominant archetype" in checklist
    assert "zero prohibited claims" in checklist
    assert "does not certify the strict profile" in checklist
