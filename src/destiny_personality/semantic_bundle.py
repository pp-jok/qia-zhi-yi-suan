from dataclasses import dataclass
from pathlib import Path

from .config_errors import ConfigError
from .config_models import RuntimeConfig
from .dimension_loader import load_dimension_coverage_policy
from .dimension_models import DimensionCoveragePolicyConfig
from .mapping_loader import load_mapping_registries
from .mapping_models import MappingRegistryBundle
from .narrative_loader import load_narrative_rules
from .narrative_models import NarrativeRulesConfig
from .primitive_loader import load_primitive_foundation
from .primitive_models import PrimitiveFoundationConfig


@dataclass(frozen=True)
class SemanticContractBundle:
    primitive_foundation: PrimitiveFoundationConfig
    mapping_registries: MappingRegistryBundle
    dimension_coverage_policy: DimensionCoveragePolicyConfig
    narrative_rules: NarrativeRulesConfig


def load_semantic_contract_bundle(
    config_dir: Path,
    runtime_config: RuntimeConfig,
) -> SemanticContractBundle:
    directory = Path(config_dir)
    foundation = load_primitive_foundation(directory)
    mappings = load_mapping_registries(directory, foundation, runtime_config)
    dimensions = load_dimension_coverage_policy(directory, foundation, runtime_config)
    narrative = load_narrative_rules(directory, foundation, dimensions)

    ontology_ids = {item.primitive_id for item in foundation.ontology.primitives}
    for index, relation in enumerate(runtime_config.relation_graph.relations):
        for side in ("left", "right"):
            if getattr(relation, side) not in ontology_ids:
                raise ConfigError(
                    "CONFIG_VALUE_ERROR",
                    "relation endpoint is not defined by the accepted ontology",
                    file="primitive_relation_graph_v1.yaml",
                    field=f"relations.{index}.{side}",
                )
    return SemanticContractBundle(foundation, mappings, dimensions, narrative)
