"""Fixture loading and deterministic Mapping-to-Primitive evaluation."""

from dataclasses import dataclass
from hashlib import sha256
import json
from pathlib import Path
from typing import Iterable, Mapping, Optional, Tuple

import yaml

from .semantic_pipeline import resolve_primitive_states


_SCHEMA_VERSION = "candidate-core-profile-calibration-facts-v1"


@dataclass(frozen=True)
class MappingEvaluationFixture:
    fixture_id: str
    schema_version: str
    input_tokens: Tuple[str, ...]
    expected_states: Mapping[str, Tuple[str, ...]]
    expected_contexts: Mapping[str, Tuple[str, ...]]
    evaluation_tags: Tuple[str, ...]
    limitations: Tuple[str, ...]
    content_fingerprint: str
    path_ref: str


@dataclass(frozen=True)
class MappingEvaluationDataset:
    kind: str
    fixtures: Tuple[MappingEvaluationFixture, ...]
    refs: Tuple[str, ...]
    fingerprint: str


@dataclass(frozen=True)
class MappingEvaluationRun:
    status: str
    metrics: Mapping[str, object]
    findings: Tuple[str, ...]
    case_outcomes: Tuple[Mapping[str, object], ...]


def load_mapping_evaluation_fixture(path: Path, project_root: Optional[Path] = None) -> MappingEvaluationFixture:
    """Load one versioned fixture and reject incomplete or ambiguous payloads."""
    try:
        payload = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise ValueError("MAPPING_EVALUATION_FIXTURE_INVALID") from exc
    if not isinstance(payload, dict) or payload.get("fixture_schema_version") != _SCHEMA_VERSION:
        raise ValueError("MAPPING_EVALUATION_FIXTURE_INVALID")
    case_id = payload.get("case_id")
    astrology = payload.get("astrology")
    gods = payload.get("bazi_ten_gods")
    if not isinstance(case_id, str) or not case_id or not isinstance(gods, list) or not all(isinstance(item, str) and item for item in gods):
        raise ValueError("MAPPING_EVALUATION_FIXTURE_INVALID")
    if not isinstance(astrology, dict) or not isinstance(astrology.get("known_birth_time"), bool) or not isinstance(astrology.get("aspect_pairs"), list):
        raise ValueError("MAPPING_EVALUATION_FIXTURE_INVALID")
    pairs = []
    for pair in astrology["aspect_pairs"]:
        if not isinstance(pair, list) or len(pair) != 2 or not all(isinstance(item, str) and item for item in pair):
            raise ValueError("MAPPING_EVALUATION_FIXTURE_INVALID")
        pairs.append(tuple(sorted(pair)))
    expected_states = _normalize_expectations(payload.get("expected_states", {}))
    expected_contexts = _normalize_expectations(payload.get("expected_contexts", {}))
    tokens = {"fact_assurance:" + str(payload.get("fact_assurance", "unknown")), "birth_time:" + ("known" if astrology["known_birth_time"] else "unknown")}
    tokens.update("bazi.ten_god:" + item for item in gods)
    tokens.update("astrology.aspect:" + left + ":" + right for left, right in pairs)
    canonical_payload = _canonical(payload)
    root = Path(project_root) if project_root is not None else None
    path_ref = Path(path).relative_to(root).as_posix() if root is not None else Path(path).as_posix()
    return MappingEvaluationFixture(
        case_id, _SCHEMA_VERSION, tuple(sorted(tokens)), expected_states, expected_contexts,
        _string_tuple(payload.get("evaluation_tags", ())), _string_tuple(payload.get("limitations", ())),
        sha256(canonical_payload.encode("utf-8")).hexdigest(), path_ref,
    )


def load_mapping_evaluation_datasets(project_root: Path) -> Mapping[str, MappingEvaluationDataset]:
    """Load both disjoint repository fixture sets and validate their independence."""
    root = Path(project_root)
    base = root / "tests" / "fixtures" / "core_profile_calibration"
    datasets = {}
    for kind, name in (("calibration", "design_set"), ("holdout", "holdout_set")):
        directory = base / name
        paths = tuple(sorted(directory.glob("*.yaml")))
        if not paths:
            raise ValueError("MAPPING_EVALUATION_DATASET_EMPTY")
        fixtures = tuple(load_mapping_evaluation_fixture(path, root) for path in paths)
        ids = tuple(item.fixture_id for item in fixtures)
        if len(set(ids)) != len(ids):
            raise ValueError("MAPPING_EVALUATION_FIXTURE_ID_DUPLICATE")
        refs = tuple(item.path_ref for item in fixtures)
        fingerprint = sha256(_canonical([(item.fixture_id, item.content_fingerprint) for item in fixtures]).encode("utf-8")).hexdigest()
        datasets[kind] = MappingEvaluationDataset(kind, fixtures, refs, fingerprint)
    calibration, holdout = datasets["calibration"], datasets["holdout"]
    if set(calibration.refs) & set(holdout.refs):
        raise ValueError("MAPPING_EVALUATION_DATASET_PATH_OVERLAP")
    if {item.content_fingerprint for item in calibration.fixtures} & {item.content_fingerprint for item in holdout.fixtures}:
        raise ValueError("MAPPING_EVALUATION_DATASET_CONTENT_OVERLAP")
    if {item.fixture_id for item in calibration.fixtures} & {item.fixture_id for item in holdout.fixtures}:
        raise ValueError("MAPPING_EVALUATION_DATASET_ID_OVERLAP")
    return datasets


def execute_mapping_evaluation(kind: str, bundle: Iterable[Mapping[str, object]], dataset: MappingEvaluationDataset) -> MappingEvaluationRun:
    """Execute each fixture through the existing Primitive Resolver without mutation."""
    if kind not in {"calibration", "holdout"} or dataset.kind != kind:
        raise ValueError("MAPPING_EVALUATION_KIND_INVALID")
    mappings = tuple(item for item in bundle if isinstance(item, Mapping))
    outcomes = tuple(_execute_case(fixture, mappings) for fixture in dataset.fixtures)
    deterministic = tuple(_execute_case(fixture, mappings) for fixture in dataset.fixtures)
    determinism_failures = sum(left != right for left, right in zip(outcomes, deterministic))
    unexpected = sum(not item["passed"] for item in outcomes)
    states = tuple(state["state"] for item in outcomes for state in item["primitive_states"])
    output_shapes = {_canonical(item["primitive_states"]) for item in outcomes}
    collapse = int(len(outcomes) > 1 and len(output_shapes) == 1)
    metrics = {
        "fixture_count": len(dataset.fixtures), "executed_case_count": len(outcomes),
        "passed_case_count": len(outcomes) - unexpected, "failed_case_count": unexpected,
        "blocked_case_count": 0, "determinism_failure_count": determinism_failures,
        "unknown_count": states.count("unknown"), "unknown_rate": _rate(states.count("unknown"), len(states)),
        "mixed_count": states.count("mixed"), "mixed_rate": _rate(states.count("mixed"), len(states)),
        "context_differentiated_count": states.count("context_differentiated"),
        "context_differentiated_rate": _rate(states.count("context_differentiated"), len(states)),
        "differentiation_score": _rate(len(output_shapes), len(outcomes)),
        "template_collapse_count": collapse, "unexpected_state_count": unexpected,
    }
    findings = tuple(sorted(set(
        (["MAPPING_EVALUATION_UNEXPECTED_STATE"] if unexpected else [])
        + (["MAPPING_EVALUATION_NONDETERMINISTIC"] if determinism_failures else [])
        + (["MAPPING_EVALUATION_OBSERVED_TEMPLATE_COLLAPSE"] if collapse else [])
    )))
    return MappingEvaluationRun("pass" if not findings else "fail", metrics, findings, outcomes)


def _execute_case(fixture: MappingEvaluationFixture, mappings: Tuple[Mapping[str, object], ...]) -> Mapping[str, object]:
    applicable = tuple(item for item in mappings if set(_string_tuple(item.get("canonical_fact_requirements", ()))) <= set(fixture.input_tokens))
    states = tuple(resolve_primitive_states(applicable, {}))
    by_id = {str(item["primitive_id"]): item for item in states}
    passed = all(by_id.get(identifier, {}).get("state") in allowed for identifier, allowed in fixture.expected_states.items())
    passed = passed and all(set(by_id.get(identifier, {}).get("context_states", ())) >= set(contexts) for identifier, contexts in fixture.expected_contexts.items())
    return {"fixture_id": fixture.fixture_id, "fixture_fingerprint": fixture.content_fingerprint, "primitive_states": states, "passed": passed}


def _normalize_expectations(value: object) -> Mapping[str, Tuple[str, ...]]:
    if value is None:
        return {}
    if not isinstance(value, Mapping):
        raise ValueError("MAPPING_EVALUATION_FIXTURE_INVALID")
    result = {}
    for key, expected in value.items():
        values = (expected,) if isinstance(expected, str) else tuple(expected) if isinstance(expected, list) else ()
        if not isinstance(key, str) or not key or not values or not all(isinstance(item, str) and item for item in values):
            raise ValueError("MAPPING_EVALUATION_FIXTURE_INVALID")
        result[key] = tuple(sorted(values))
    return result


def _string_tuple(value: object) -> Tuple[str, ...]:
    if not isinstance(value, (list, tuple)) or not all(isinstance(item, str) and item for item in value):
        return ()
    return tuple(value)


def _canonical(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), default=list)


def _rate(value: int, total: int) -> float:
    return value / total if total else 0.0
