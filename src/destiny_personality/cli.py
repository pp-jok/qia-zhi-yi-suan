import argparse
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
        else:
            return 2
    except ConfigError as error:
        print(str(error), file=sys.stderr)
        return 2
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
