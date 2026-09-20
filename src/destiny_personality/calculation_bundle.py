from dataclasses import dataclass
from pathlib import Path

from .astrology_table_loader import load_astrology_dignity_table
from .astrology_table_models import AstrologyDignityTableConfig
from .bazi_table_loader import load_bazi_deterministic_tables
from .bazi_table_models import BaziDeterministicTablesConfig
from .comparison_policy_loader import load_fact_comparison_policy
from .comparison_policy_models import FactComparisonPolicyConfig
from .config_models import RuntimeConfig
from .node_policy_loader import load_astrology_node_policy
from .node_policy_models import AstrologyNodePolicyConfig
from .vocabulary_loader import load_canonical_fact_vocabulary
from .vocabulary_models import CanonicalFactVocabularyConfig


@dataclass(frozen=True)
class CalculationContractBundle:
    vocabulary: CanonicalFactVocabularyConfig
    bazi_tables: BaziDeterministicTablesConfig
    astrology_dignity_table: AstrologyDignityTableConfig
    astrology_node_policy: AstrologyNodePolicyConfig
    comparison_policy: FactComparisonPolicyConfig


def load_calculation_contract_bundle(
    config_dir: Path,
    runtime_config: RuntimeConfig,
) -> CalculationContractBundle:
    directory = Path(config_dir)
    vocabulary = load_canonical_fact_vocabulary(directory, runtime_config)
    bazi_tables = load_bazi_deterministic_tables(
        directory, runtime_config, vocabulary
    )
    dignity_table = load_astrology_dignity_table(
        directory, runtime_config, vocabulary
    )
    node_policy = load_astrology_node_policy(
        directory, runtime_config, vocabulary
    )
    comparison_policy = load_fact_comparison_policy(
        directory, runtime_config, vocabulary
    )
    return CalculationContractBundle(
        vocabulary,
        bazi_tables,
        dignity_table,
        node_policy,
        comparison_policy,
    )
