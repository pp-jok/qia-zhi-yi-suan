import argparse
from dataclasses import asdict
import json
from pathlib import Path
import sys
from typing import Optional, Sequence

from .calculation_bundle import load_calculation_contract_bundle
from .calculation_fingerprint import build_calculation_bundle_fingerprint
from .config_errors import ConfigError
from .config_loader import load_runtime_config
from .semantic_bundle import load_semantic_contract_bundle
from .semantic_fingerprint import build_semantic_bundle_fingerprint


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="destiny-personality-reference-validate")
    subparsers = parser.add_subparsers(dest="command", required=True)
    validate = subparsers.add_parser(
        "validate-config", help="validate a V2.2 runtime configuration directory"
    )
    validate.add_argument("path", type=Path)
    validate_semantic = subparsers.add_parser(
        "validate-semantic-contracts",
        help="validate candidate semantic contracts against a runtime baseline",
    )
    validate_semantic.add_argument("candidate_dir", type=Path)
    validate_semantic.add_argument(
        "--runtime-config-dir",
        required=True,
        type=Path,
        help="directory containing the accepted runtime baseline",
    )
    validate_calculation = subparsers.add_parser(
        "validate-calculation-contracts",
        help="validate candidate calculation contracts against a runtime baseline",
    )
    validate_calculation.add_argument("candidate_dir", type=Path)
    validate_calculation.add_argument(
        "--runtime-config-dir",
        required=True,
        type=Path,
        help="directory containing the accepted runtime baseline",
    )
    render = subparsers.add_parser("render-core-portrait")
    render.add_argument("profile", type=Path)
    render.add_argument("--mode", choices=("core", "core_concise", "core_standard"), required=True)
    explain = subparsers.add_parser("explain-profile-item")
    explain.add_argument("profile", type=Path); explain.add_argument("item_id")
    view = subparsers.add_parser("profile-source-view")
    view.add_argument("profile", type=Path); view.add_argument("--view", choices=("combined", "bazi", "astrology", "comparison"), required=True)
    diff = subparsers.add_parser("profile-diff")
    diff.add_argument("left", type=Path); diff.add_argument("right", type=Path)
    build = subparsers.add_parser("build-core-profile")
    build.add_argument("facts", type=Path)
    build.add_argument("--qualification", type=Path)
    build.add_argument("--output", type=Path, required=True)
    semantic_build = subparsers.add_parser("build-semantic-core")
    semantic_build.add_argument("project_root", type=Path)
    semantic_build.add_argument("profile_ref")
    semantic_build.add_argument("output", type=Path)
    audit_core = subparsers.add_parser("audit-semantic-core")
    audit_core.add_argument("project_root", type=Path)
    mechanisms = subparsers.add_parser("validate-semantic-mechanisms")
    mechanisms.add_argument("project_root", type=Path)
    mapping = subparsers.add_parser("build-mapping-candidates")
    mapping.add_argument("project_root", type=Path)
    mapping_validate = subparsers.add_parser("validate-mapping-v2")
    mapping_validate.add_argument("project_root", type=Path)
    signatures = subparsers.add_parser("build-signatures")
    signatures.add_argument("project_root", type=Path)
    dynamics = subparsers.add_parser("build-dynamics")
    dynamics.add_argument("project_root", type=Path)
    mapping_calibration = subparsers.add_parser("run-mapping-calibration")
    mapping_calibration.add_argument("project_root", type=Path)
    mapping_calibration.add_argument("--register", action="store_true", help="append a passing artifact to the authoritative registry")
    mapping_holdout = subparsers.add_parser("run-mapping-holdout")
    mapping_holdout.add_argument("project_root", type=Path)
    mapping_holdout.add_argument("--register", action="store_true", help="append a passing artifact to the authoritative registry")
    promote = subparsers.add_parser("promote-semantic-bundle", help="deprecated simulation; never writes an authority record")
    promote.add_argument("active_bundle_ref")
    promote.add_argument("candidate_bundle_ref")
    promote.add_argument("--decision-ref")
    authorized_promote = subparsers.add_parser("promote-semantic-bundle-authorized")
    authorized_promote.add_argument("project_root", type=Path)
    authorized_promote.add_argument("active_bundle_ref")
    authorized_promote.add_argument("candidate_bundle_ref")
    authorized_promote.add_argument("candidate_fingerprint")
    authorized_promote.add_argument("decision_id")
    rollback = subparsers.add_parser("rollback-semantic-bundle")
    rollback.add_argument("active_bundle_ref")
    rollback.add_argument("candidate_bundle_ref")
    rollback.add_argument("decision_ref")
    authorized_rollback = subparsers.add_parser("rollback-semantic-bundle-authorized")
    authorized_rollback.add_argument("project_root", type=Path)
    authorized_rollback.add_argument("decision_id")
    authorized_rollback.add_argument("candidate_fingerprint")
    packet = subparsers.add_parser("promotion-review-packet")
    packet.add_argument("candidate_bundle_ref")
    packet.add_argument("--decision-ref")
    report_plan = subparsers.add_parser("build-report-plan")
    report_plan.add_argument("core", type=Path)
    report_plan.add_argument("renderer_profile")
    render_report = subparsers.add_parser("render-report")
    render_report.add_argument("core", type=Path)
    render_report.add_argument("renderer_profile")
    semantic_source = subparsers.add_parser("semantic-core-source-view")
    semantic_source.add_argument("core", type=Path)
    semantic_source.add_argument("stage", choices=("mapping", "primitive", "signature", "dynamic", "shadow_mature", "theme", "archetype"))
    semantic_explain = subparsers.add_parser("semantic-core-explain")
    semantic_explain.add_argument("core", type=Path)
    semantic_explain.add_argument("item_id")
    semantic_diff = subparsers.add_parser("semantic-core-diff")
    semantic_diff.add_argument("left", type=Path)
    semantic_diff.add_argument("right", type=Path)
    semantic_packet = subparsers.add_parser("semantic-core-review-packet")
    semantic_packet.add_argument("project_root", type=Path)
    return parser


def _runtime_config_summary(config) -> dict:
    return {
        "status": "ok",
        "bazi_methodology_version": config.bazi.methodology_version,
        "astrology_methodology_version": config.astrology.methodology_version,
        "score_model_version": config.score_model.score_model_version,
        "relation_graph_version": config.relation_graph.relation_graph_version,
        "relation_count": len(config.relation_graph.relations),
    }


def _semantic_contract_summary(bundle, runtime_config, fingerprint) -> dict:
    foundation = bundle.primitive_foundation
    mappings = bundle.mapping_registries
    dimensions = bundle.dimension_coverage_policy
    narrative = bundle.narrative_rules
    return {
        "status": "ok",
        "command": "validate-semantic-contracts",
        "fingerprint": fingerprint,
        "versions": {
            "ontology": foundation.ontology.ontology_version,
            "primitive_resolution": foundation.resolution.resolution_version,
            "bazi_registry": mappings.bazi.registry_version,
            "astrology_registry": mappings.astrology.registry_version,
            "dimension_policy": dimensions.policy_version,
            "narrative": narrative.narrative_version,
        },
        "counts": {
            "primitives": len(foundation.ontology.primitives),
            "state_rules": len(foundation.resolution.rules),
            "bazi_mapping_rules": len(mappings.bazi.rules),
            "astrology_mapping_rules": len(mappings.astrology.rules),
            "dimensions": len(dimensions.dimensions),
            "narrative_rules": len(narrative.rules),
            "relation_graph_relations": len(
                runtime_config.relation_graph.relations
            ),
        },
    }


def _calculation_contract_summary(bundle, fingerprint) -> dict:
    return {
        "status": "ok",
        "command": "validate-calculation-contracts",
        "fingerprint": fingerprint,
        "versions": {
            "vocabulary": bundle.vocabulary.vocabulary_version,
            "bazi_tables": bundle.bazi_tables.table_version,
            "astrology_dignity_table": (
                bundle.astrology_dignity_table.table_version
            ),
            "astrology_node_policy": (
                bundle.astrology_node_policy.policy_version
            ),
            "comparison_policy": bundle.comparison_policy.policy_version,
        },
        "counts": {
            "vocabulary_categories": len(bundle.vocabulary.categories),
            "vocabulary_entries": sum(
                len(category.entries)
                for category in bundle.vocabulary.categories
            ),
            "bazi_rules": sum(
                len(section.rules) for section in bundle.bazi_tables.tables
            ),
            "astrology_dignity_rows": len(
                bundle.astrology_dignity_table.rows
            ),
            "comparison_categories": len(
                bundle.comparison_policy.logical_categories
            ),
            "canonical_precision": len(
                bundle.comparison_policy.canonical_precision
            ),
            "boundary_margins": len(
                bundle.comparison_policy.boundary_margins
            ),
            "tolerances": len(bundle.comparison_policy.tolerances),
            "representation_equivalences": len(
                bundle.comparison_policy.representation_equivalences
            ),
        },
    }


def _load_semantic_snapshot(candidate_dir: Path, runtime_config_dir: Path):
    runtime_config = load_runtime_config(runtime_config_dir)
    bundle = load_semantic_contract_bundle(candidate_dir, runtime_config)
    fingerprint = build_semantic_bundle_fingerprint(
        candidate_dir, runtime_config_dir
    )
    return runtime_config, bundle, fingerprint


def _load_stable_semantic_snapshot(
    candidate_dir: Path, runtime_config_dir: Path
):
    _, _, first_fingerprint = _load_semantic_snapshot(
        candidate_dir, runtime_config_dir
    )
    runtime_config, bundle, second_fingerprint = _load_semantic_snapshot(
        candidate_dir, runtime_config_dir
    )
    if first_fingerprint != second_fingerprint:
        raise ConfigError(
            "CONFIG_VALUE_ERROR",
            "configuration files changed during validation; retry with an "
            "immutable candidate snapshot",
        )
    return runtime_config, bundle, second_fingerprint


def _load_calculation_snapshot(candidate_dir: Path, runtime_config_dir: Path):
    runtime_config = load_runtime_config(runtime_config_dir)
    bundle = load_calculation_contract_bundle(candidate_dir, runtime_config)
    fingerprint = build_calculation_bundle_fingerprint(
        candidate_dir, runtime_config_dir
    )
    return bundle, fingerprint


def _load_stable_calculation_snapshot(
    candidate_dir: Path, runtime_config_dir: Path
):
    _, first_fingerprint = _load_calculation_snapshot(
        candidate_dir, runtime_config_dir
    )
    bundle, second_fingerprint = _load_calculation_snapshot(
        candidate_dir, runtime_config_dir
    )
    if first_fingerprint != second_fingerprint:
        raise ConfigError(
            "CONFIG_VALUE_ERROR",
            "configuration files changed during validation; retry with an "
            "immutable candidate snapshot",
        )
    return bundle, second_fingerprint


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = _build_parser().parse_args(argv)
    try:
        if args.command == "validate-config":
            summary = _runtime_config_summary(load_runtime_config(args.path))
        elif args.command == "validate-semantic-contracts":
            runtime_config, bundle, fingerprint = _load_stable_semantic_snapshot(
                args.candidate_dir, args.runtime_config_dir
            )
            summary = _semantic_contract_summary(
                bundle, runtime_config, fingerprint
            )
        elif args.command == "validate-calculation-contracts":
            bundle, fingerprint = _load_stable_calculation_snapshot(
                args.candidate_dir, args.runtime_config_dir
            )
            summary = _calculation_contract_summary(bundle, fingerprint)
        elif args.command == "build-core-profile":
            from .core_profile_builder import build_candidate_core_profile
            from .core_profile_codec import write_candidate_profile
            from .deterministic_facts_codec import load_qualified_deterministic_facts

            qualified = load_qualified_deterministic_facts(args.facts, args.qualification)
            profile = build_candidate_core_profile(qualified.facts, fact_assurance=qualified.fact_assurance)
            write_candidate_profile(profile, args.output)
            summary = {"status": "ok", "profile": str(args.output), "profile_id": profile.candidate_profile_id}
        elif args.command == "build-semantic-core":
            from .mapping_v2 import compile_mapping_v2_from_repository
            from .semantic_pipeline import build_semantic_core_from_approved_mapping, load_enabled_formation_policies
            from .semantic_pipeline_codec import write_pipeline_core

            mapping_bundle = compile_mapping_v2_from_repository(args.project_root)
            mappings = (*mapping_bundle.bazi_rules, *mapping_bundle.astrology_rules)
            policies, policy_versions = load_enabled_formation_policies(args.project_root)
            core = build_semantic_core_from_approved_mapping(args.profile_ref, mappings, policies)
            core["audit_trail"] = (*core["audit_trail"], "repository_mapping_v2", mapping_bundle.status)
            if mapping_bundle.blockers:
                core["limitations"] = tuple(sorted(set((*core["limitations"], *mapping_bundle.blockers))))
            write_pipeline_core(core, policies or policy_versions, args.output)
            summary = {"status": core["stage_statuses"]["mapping"], "output": str(args.output), "stage_statuses": core["stage_statuses"]}
        elif args.command in {"audit-semantic-core", "validate-semantic-mechanisms", "build-mapping-candidates", "validate-mapping-v2", "build-signatures", "build-dynamics", "run-mapping-calibration", "run-mapping-holdout", "promote-semantic-bundle", "promote-semantic-bundle-authorized", "rollback-semantic-bundle", "rollback-semantic-bundle-authorized", "promotion-review-packet", "build-report-plan", "render-report", "semantic-core-source-view", "semantic-core-explain", "semantic-core-diff", "semantic-core-review-packet"}:
            from .semantic_core import audit_semantic_core_candidate, build_promotion_review_packet, build_report_plan, build_semantic_core_candidate, build_semantic_core_review_packet, diff_semantic_core_candidates, explain_semantic_core_item, form_core_dynamics, form_dominant_signatures, load_semantic_mechanism_role_policy, promote_semantic_bundle, render_semantic_core_report, rollback_semantic_bundle, semantic_core_source_view
            from .semantic_core_codec import load_semantic_core_candidate
            from .semantic_mechanisms import build_semantic_mechanism_audit_report, load_approved_evidence_root_ids, load_approved_semantic_mechanism_ids, load_semantic_mechanism_candidates
            from .mapping_v2 import audit_mapping_v2_candidates, build_fresh_mapping_candidates, build_mapping_evaluation_artifact, compile_mapping_v2_candidate_bundle, compile_mapping_v2_from_repository, load_mapping_proposal_registry, load_mapping_v2_candidate_registry, mapping_evaluation_dataset_refs, mapping_v2_candidate_fingerprint, run_mapping_v2_calibration, run_mapping_v2_holdout
            from .semantic_authority import load_mapping_eligible_semantic_mechanisms
            root = args.project_root if hasattr(args, "project_root") else Path(".")
            mechanism_root = root / "candidates" / "semantic-mechanisms-v1"
            if args.command == "promote-semantic-bundle":
                simulation = asdict(promote_semantic_bundle(args.active_bundle_ref, args.candidate_bundle_ref, args.decision_ref))
                simulation["status"] = "simulated_" + simulation["status"]
                simulation["authority"] = "none"
                simulation["persistence"] = "none"
                summary = simulation
            elif args.command == "promote-semantic-bundle-authorized":
                from .promotion_authority import load_promotion_authority
                from .semantic_promotion import promote_from_authority
                authority = load_promotion_authority(args.project_root, args.candidate_bundle_ref, args.candidate_fingerprint, args.decision_id)
                record = args.project_root / "governance" / "semantic-promotion-v1" / "promotion-records" / (args.decision_id + "-" + args.candidate_fingerprint + ".json")
                summary = asdict(promote_from_authority(args.active_bundle_ref, authority, record))
            elif args.command == "rollback-semantic-bundle-authorized":
                from .semantic_promotion import rollback_from_record
                record = args.project_root / "governance" / "semantic-promotion-v1" / "promotion-records" / (args.decision_id + "-" + args.candidate_fingerprint + ".json")
                summary = asdict(rollback_from_record(record))
            elif args.command == "rollback-semantic-bundle":
                summary = asdict(rollback_semantic_bundle(promote_semantic_bundle(args.active_bundle_ref, args.candidate_bundle_ref, args.decision_ref)))
            elif args.command == "promotion-review-packet":
                summary = build_promotion_review_packet(args.candidate_bundle_ref, ("PASS",), args.decision_ref)
            elif args.command == "build-report-plan":
                summary = asdict(build_report_plan(load_semantic_core_candidate(args.core), args.renderer_profile))
            elif args.command == "render-report":
                core = load_semantic_core_candidate(args.core)
                summary = asdict(render_semantic_core_report(core, build_report_plan(core, args.renderer_profile)))
            elif args.command == "semantic-core-source-view":
                from .semantic_pipeline_codec import load_pipeline_core
                try:
                    pipeline_core = load_pipeline_core(args.core)["core"]
                except ValueError:
                    summary = semantic_core_source_view(load_semantic_core_candidate(args.core), args.stage)
                else:
                    from .semantic_pipeline import semantic_pipeline_source_view
                    summary = semantic_pipeline_source_view(pipeline_core, args.stage)
            elif args.command == "semantic-core-explain":
                from .semantic_pipeline_codec import load_pipeline_core
                try:
                    pipeline_core = load_pipeline_core(args.core)["core"]
                except ValueError:
                    summary = explain_semantic_core_item(load_semantic_core_candidate(args.core), args.item_id)
                else:
                    from .semantic_pipeline import explain_semantic_pipeline_item
                    summary = explain_semantic_pipeline_item(pipeline_core, args.item_id)
            elif args.command == "semantic-core-diff":
                from .semantic_pipeline_codec import load_pipeline_core
                try:
                    left_pipeline, right_pipeline = load_pipeline_core(args.left), load_pipeline_core(args.right)
                except ValueError:
                    summary = asdict(diff_semantic_core_candidates(load_semantic_core_candidate(args.left), load_semantic_core_candidate(args.right)))
                else:
                    from .semantic_pipeline import diff_semantic_pipeline_cores
                    left_core = {**left_pipeline["core"], "formation_policy_fingerprint": left_pipeline["formation_policy_fingerprint"]}
                    right_core = {**right_pipeline["core"], "formation_policy_fingerprint": right_pipeline["formation_policy_fingerprint"]}
                    summary = {"changed_categories": diff_semantic_pipeline_cores(left_core, right_core)}
            elif args.command == "semantic-core-review-packet":
                candidates = load_semantic_mechanism_candidates(mechanism_root)
                approved_roots = load_approved_evidence_root_ids(mechanism_root)
                approved_mechanisms = load_approved_semantic_mechanism_ids(mechanism_root)
                summary = build_semantic_core_review_packet(len(approved_roots), len(approved_mechanisms), 0, ("PASS",))
            elif args.command == "audit-semantic-core":
                policy = load_semantic_mechanism_role_policy(root)
                eligible = load_mapping_eligible_semantic_mechanisms(mechanism_root, policy)
                mapping_bundle = compile_mapping_v2_candidate_bundle(
                    load_mapping_v2_candidate_registry(root).candidates,
                    eligible.mechanism_ids,
                )
                summary = dict(audit_semantic_core_candidate(build_semantic_core_candidate("cli-audit", ())))
                summary.update({
                    "mapping_eligible_mechanism_count": len(eligible.mechanism_ids),
                    "mapping_proposal_count": len(load_mapping_proposal_registry(root)),
                    "approved_mapping_count": len(mapping_bundle.bazi_rules) + len(mapping_bundle.astrology_rules),
                    "mapping_v2_candidate_fingerprint": mapping_v2_candidate_fingerprint(root),
                    "mapping_v2_runtime_status": mapping_bundle.status,
                    "mapping_v2_runtime_blockers": mapping_bundle.blockers,
                    "semantic_readiness": "blocked_by_gate" if mapping_bundle.status == "blocked_by_gate" else "candidate_only",
                })
            elif args.command == "validate-semantic-mechanisms":
                candidates = load_semantic_mechanism_candidates(mechanism_root)
                summary = dict(build_semantic_mechanism_audit_report(candidates, load_approved_evidence_root_ids(mechanism_root), contract_root=mechanism_root))
            elif args.command in {"build-mapping-candidates", "validate-mapping-v2"}:
                policy = load_semantic_mechanism_role_policy(root)
                eligible = load_mapping_eligible_semantic_mechanisms(mechanism_root, policy)
                candidates = build_fresh_mapping_candidates(load_mapping_proposal_registry(root), eligible.mechanism_ids)
                if args.command == "validate-mapping-v2":
                    registry = load_mapping_v2_candidate_registry(root)
                    candidates = registry.candidates
                bundle = compile_mapping_v2_candidate_bundle(candidates, eligible.mechanism_ids)
                summary = asdict(bundle)
                if args.command == "validate-mapping-v2":
                    summary["audit"] = audit_mapping_v2_candidates(candidates, eligible.mechanism_ids)
            elif args.command == "build-signatures":
                summary = {"status": "blocked_by_gate", "signatures": list(form_dominant_signatures(())), "blockers": ["APPROVED_PRIMITIVE_V2_REQUIRED"]}
            elif args.command == "run-mapping-calibration":
                mapping_bundle = compile_mapping_v2_from_repository(root)
                summary = dict(build_mapping_evaluation_artifact("calibration", (*mapping_bundle.bazi_rules, *mapping_bundle.astrology_rules), "mapping-v2:repository", mapping_v2_candidate_fingerprint(root), mapping_evaluation_dataset_refs(root, "calibration"), "mapping-v2-evaluation-v1"))
                if args.register:
                    from .promotion_authority import register_evaluation_artifact
                    register_evaluation_artifact(root, "calibration", summary)
                    summary["authority_registry"] = "registered"
                summary["mapping_bundle_status"] = mapping_bundle.status
                summary["mapping_bundle_blockers"] = mapping_bundle.blockers
            elif args.command == "run-mapping-holdout":
                mapping_bundle = compile_mapping_v2_from_repository(root)
                summary = dict(build_mapping_evaluation_artifact("holdout", (*mapping_bundle.bazi_rules, *mapping_bundle.astrology_rules), "mapping-v2:repository", mapping_v2_candidate_fingerprint(root), mapping_evaluation_dataset_refs(root, "holdout"), "mapping-v2-evaluation-v1"))
                if args.register:
                    from .promotion_authority import register_evaluation_artifact
                    register_evaluation_artifact(root, "holdout", summary)
                    summary["authority_registry"] = "registered"
                summary["mapping_bundle_status"] = mapping_bundle.status
                summary["mapping_bundle_blockers"] = mapping_bundle.blockers
            else:
                summary = {"status": "blocked_by_gate", "dynamics": list(form_core_dynamics(())), "blockers": ["APPROVED_SIGNATURE_REQUIRED"]}
        elif args.command in {"render-core-portrait", "explain-profile-item", "profile-source-view", "profile-diff"}:
            from .core_profile_codec import load_candidate_profile
            from .core_portrait import build_candidate_profile_summary, compare_candidate_profiles_versions, explain_profile_item, render_core_concise, render_core_standard, source_view
            if args.command == "profile-diff":
                summary = asdict(compare_candidate_profiles_versions(load_candidate_profile(args.left), load_candidate_profile(args.right)))
            else:
                profile = load_candidate_profile(args.profile)
                if args.command == "render-core-portrait":
                    view = build_candidate_profile_summary(profile)
                    summary = asdict(view if args.mode == "core" else render_core_concise(view) if args.mode == "core_concise" else render_core_standard(view))
                elif args.command == "explain-profile-item":
                    summary = asdict(explain_profile_item(profile, args.item_id))
                else:
                    summary = [asdict(item) for item in source_view(profile, args.view)]
        else:
            return 2
    except (ConfigError, ValueError) as error:
        print(str(error), file=sys.stderr)
        return 2
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
