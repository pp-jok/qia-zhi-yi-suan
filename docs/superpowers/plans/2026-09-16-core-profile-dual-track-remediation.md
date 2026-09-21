# Core Profile 双轨渐进式整改实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在不破坏公开 V2 长篇人格书的前提下，建立可审计的 `core-destiny-profile-v1` 推理资产，并让动态报告规划器取代固定章节作为新链路的表达入口。

**Architecture:** 保持 Canonical Chart Facts、外部能力资格、时间敏感性和事实边界不变。先完成可审阅的人格本体、体系映射、Dynamic 形成和校准设计，再将获批设计投影为机器可读资产并实现独立 Semantic Core。两套系统的事实先分别映射为 Primitive Candidates，再解析状态、选择 Signature 与 Dynamic、分层推导 Shadow/Mature/Fate/Archetype，生成 Core Profile；Report Planner 只消费该 Profile。现有固定 56 章迁入明确的 Legacy Renderer 轨道。

**Tech Stack:** Python 3.9+、dataclasses、PyYAML、pytest、Markdown Skill contracts、GitHub CLI。

## Global Constraints

- 公开 V2 冻结为 `legacy-long-form-v2`，GitHub 标签为 `v0.1.0-legacy-long-form`。
- 不打包或替换外部排盘 Provider。
- `fact_assurance` 与 `semantic_model_assurance` 必须分离。
- `fact_assurance = none` 必须终止 Core Profile 推理，只能产生 stopped execution artifact。
- `unknown` 绝不能自动解析为 `supported_low`。
- 八字与西占必须先独立映射；跨系统关系不得增加 Trait Salience。
- Cross-System Alignment 允许 `unresolved` 与 `non_comparable`；二者保留限制，不强制综合。
- Core Dynamic 合法数量为 0–7，通常为 2–5；禁止为了满足数量目标生成次级 Dynamic。
- 新 Renderer 只能表达 Core Profile 已有结论。
- Renderer 的章节规模是体验目标，不是硬验证条件；证据不足时必须允许少于建议下限。
- 生产 Ontology、Mapping、形成规则和校准阈值必须由产品所有者明确批准；D1 只允许
  `candidates/` 中的非默认实现，未获 C4b 批准不得进入 `configs/`。
- 当前业务根目录不是 Git 仓库；只对隔离的公开仓库执行标签、提交和推送。

---

## 阶段 A：冻结并标识旧版

### Task 1: 建立 Legacy V2 发布基线

**Files:**
- Modify: `release/qia-zhi-yi-suan/README.md`
- Modify: `release/qia-zhi-yi-suan/destiny-personality/SKILL.md`
- Test: Git tag、公开仓库元数据和现有 Skill 合同测试

**Interfaces:**
- Consumes: 已发布 `pp-jok/qia-zhi-yi-suan` 的 `main` 与提交 `82baf95`。
- Produces: 可回归的 `v0.1.0-legacy-long-form` 基线与显式 `legacy-long-form-v2` 标识。

- [ ] **Step 1: 写失败合同测试，要求旧版被明确标识**

在 `tests/test_skill_package.py` 添加：

```python
def test_legacy_long_form_v2_is_explicitly_marked() -> None:
    skill = read_skill_file("SKILL.md")
    blueprint = read_skill_file("references/long-form-report-blueprint.md")

    assert "legacy-long-form-v2" in skill
    assert "legacy-long-form-v2" in blueprint
    assert "renderer" in blueprint
```

- [ ] **Step 2: 运行测试并确认失败**

Run: `python3 -m pytest tests/test_skill_package.py::test_legacy_long_form_v2_is_explicitly_marked -q`

Expected: FAIL，因为旧版仍被描述为默认推理骨架。

- [ ] **Step 3: 在文档中加入最小 Legacy 路由说明**

在 `destiny-personality/SKILL.md` 和 `references/long-form-report-blueprint.md` 中写明：

```text
long-form-personality-book-v2 is legacy-long-form-v2.
It remains available for compatibility and regression only.
It must not provide Primitive, Signature, Dynamic, Theme, or Archetype inputs
to the Core Profile pipeline.
```

- [ ] **Step 4: 重新运行失败测试与完整 Skill 包测试**

Run:

```bash
python3 -m pytest tests/test_skill_package.py -q
```

Expected: PASS。

- [ ] **Step 5: 在公开仓库创建不可变基线标签**

Run in `release/qia-zhi-yi-suan`:

```bash
git tag -a v0.1.0-legacy-long-form -m "Freeze legacy 56-chapter renderer"
git push origin v0.1.0-legacy-long-form
```

Expected: `gh api repos/pp-jok/qia-zhi-yi-suan/git/ref/tags/v0.1.0-legacy-long-form` 返回标签引用。

## 阶段 B：建立 Core Profile 合同与审计边界

### Task 2: 定义 Core Profile 与 Report Plan 文档合同

**Files:**
- Create: `destiny-personality/schemas/core-destiny-profile.md`
- Create: `destiny-personality/schemas/report-plan.md`
- Create: `destiny-personality/checklists/core-profile.md`
- Modify: `destiny-personality/schemas/execution-report.md`
- Modify: `destiny-personality/SKILL.md`
- Modify: `tests/test_skill_package.py`

**Interfaces:**
- Consumes: accepted Canonical Fact Packet、现有 Controlled Inference 边界。
- Produces: `core-destiny-profile-v1`、`report-plan-v1` 与执行报告中的 `core_profile_ref`。

- [ ] **Step 1: 写失败测试，锁定 Core Profile 根字段与保障分离**

```python
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
        "dominant_signatures",
        "core_dynamics",
        "audit_trail",
    ):
        assert f"`{field}`" in contract
    assert "`project_semantic_verified`" in contract
    assert "`project_semantic_partial`" in contract
    assert "does not upgrade fact assurance" in contract
```

- [ ] **Step 2: 运行测试并确认失败**

Run: `python3 -m pytest tests/test_skill_package.py::test_core_profile_contract_separates_fact_and_semantic_assurance -q`

Expected: FAIL，因为该合同尚不存在。

- [ ] **Step 3: 编写 `core-destiny-profile-v1` 合同**

合同固定 19 个根字段，使用已确认的字段顺序。每个 Primitive、Signature、Dynamic、
Shadow/Mature、Fate Theme 与 Archetype 条目都要求：

```text
item_id
fact_refs
semantic_rule_refs
source_refs
confidence_or_priority
limitations
context
```

明确 `fact_assurance` 只描述命盘事实，`semantic_model_assurance` 只描述项目内
版本化语义资产。任何 `capability_reported` 事实包不得因 Profile 生成而变成
`project_verified`。`fact_assurance = none` 必须终止正常 Core Profile 推理，只生成
不含人格结论的 stopped execution artifact。

`semantic_model_versions` 必须实际记录 Ontology、State、两套 Mapping、Relation、
Signature Formation、Dynamic Formation、Derived Theme 与 Archetype Policy 的版本。明确
`project_semantic_verified` 仅覆盖该 Profile 实际使用的全部获批资产；缺失某条派生路径的
Policy 时标记 `project_semantic_partial`，关闭该路径而非由模型自由补写。

- [ ] **Step 4: 编写 Report Plan 合同与 Core Profile 审计清单**

`report-plan-v1` 根字段为：

```text
schema_version
core_profile_ref
renderer_profile
selected_topics
omitted_candidate_topics
section_plan
rendering_constraints
audit_trail
```

每个 `selected_topic` 必须具有 `profile_refs`；每个 omitted candidate 必须具有
`reason`。清单要求 Renderer Containment：报告中的核心结论均可回溯到 Profile。

- [ ] **Step 5: 扩展 Execution Report 与 Skill 路由**

在 Execution Report 增加：

```text
core_profile_ref
semantic_model_assurance
semantic_model_versions
report_plan_ref
```

在 `SKILL.md` 明确新链路顺序：`FACT_BASIS_VALIDATED → CORE_PROFILE_VALIDATED →
REPORT_PLAN_VALIDATED → REPORT_VALIDATED`；Legacy 路径不允许向 Core Profile 回流。

- [ ] **Step 6: 运行完整 Skill 包测试**

Run: `python3 -m pytest tests/test_skill_package.py -q`

Expected: PASS。

## 阶段 C：产品语义设计与强制审批门

阶段 C 是人格产品建模，不是先填 YAML 再补解释。每一阶段先交付可读、可质询的设计
文档；`candidates/core-profile-v1/*.yaml` 只能在对应设计通过内部审阅后作为机器可读投影
创建，且始终不是主要审阅对象，也不能作为运行时配置。

### Task 3: C1 — Core Personality Ontology Review

**Files:**
- Create: `docs/domain/core-personality-ontology-review-v1.md`
- Create: `docs/domain/core-primitive-catalog-v1.md`
- Modify: `destiny-personality/checklists/semantic-candidate-release.md`

**Interfaces:**
- Consumes: Core Profile 合同与既有事实边界。
- Produces: 经审阅的 Primitive、State 与非蕴含语义；尚不产生生产 YAML。

- [ ] **Step 1: 编写人格本体审阅稿**

每个候选 Primitive 必须记录：

```text
primitive_id
canonical_name
definition
high_expression
low_expression
non_implications
candidate_evidence_families
counterevidence
sample_bias_risk
review_status
```

明确 `supported_high`、`supported_low`、`mixed`、`unknown` 的证据标准与反例。不得把
Golden Sample 的“判断权”“远行者”“自由与退出”等结论直接上升为通用 Primitive。

- [ ] **Step 2: 记录 C1 审阅结论**

在 `core-personality-ontology-review-v1.md` 为每个 Primitive 记录接受、拒绝或待定，及
原因、反例、风险和需要的后续校准证据。待定项不能进入机器可读候选资产。

### Task 4: C2 — Bazi / Astrology Semantic Mapping Review

**Files:**
- Create: `docs/domain/bazi-semantic-mapping-review-v1.md`
- Create: `docs/domain/astrology-semantic-mapping-review-v1.md`
- Create: `docs/domain/mapping-review-record-v1.md`

**Interfaces:**
- Consumes: C1 已审阅 Primitive 与状态定义。
- Produces: 两套独立体系映射的可审阅规则；不在此阶段综合为人格结论。

- [ ] **Step 1: 写八字与西占独立映射审阅稿**

每条映射规则必须包含：

```text
rule_id
source_system
primary_condition
context
outputs
modifiers
exclusion_conditions
limitations
counterexamples
review_status
```

- [ ] **Step 2: 审阅可比较性边界**

为每条潜在跨系统关系标注 `validation`、`complement`、`contextualization`、`tension`、
`correction`、`unresolved` 或 `non_comparable`。后两者明确不生成综合结论，且保留各自
候选、证据和限制。

### Task 5: C3 — Dynamic Formation Review

**Files:**
- Create: `docs/domain/dynamic-formation-review-v1.md`
- Create: `docs/domain/shadow-mature-fate-archetype-review-v1.md`

**Interfaces:**
- Consumes: C1 Primitive/State 结论、C2 独立 Mapping 审阅结论。
- Produces: 经审阅的 Signature、Dynamic、派生层级与 Archetype 语义；不生成默认答案库。

- [ ] **Step 1: 记录 Dynamic 形成规则**

每个 Dynamic 必须有双方已激活 Primitive、关系规则、上下文、反证和限制。合法数量为
0–7，通常 2–5；0 或 1 是证据不足或关系未激活时的合格结果。

- [ ] **Step 2: 记录分层派生规则**

固定顺序为：

```text
Core Dynamic → Shadow Form → Mature Integration → repeated patterns across dynamics → Fate Theme → Archetype
```

`FateTheme` 和 `Archetype` 都必须记录 `source_dynamic_refs`、`stable_force_refs`、
`movement_force_refs`、`development_theme_refs`、反证和限制；`Archetype` 另记录
`support_level`。Fate Theme 的高置信路径为多个 Dynamic 的重复模式；受控例外仅允许
一个极强 Dynamic 在至少两个独立上下文中有重复证据，并记录
`cross_context_recurrence_refs`。证据不足时二者均可为空。Archetype 只能压缩已有
Profile 结论，禁止反向生成或提高 Primitive、Dynamic、Theme 的支持度。

### Task 6: C4a — Calibration Protocol Review

**Files:**
- Create: `docs/domain/core-profile-calibration-review-v1.md`
- Create: `docs/domain/core-profile-similarity-policy-v1.md`
- Create: `docs/domain/template-collapse-policy-v1.md`
- Create: `docs/domain/core-profile-determinism-policy-v1.md`
- Create: `candidates/core-profile-v1/primitive_ontology_v1.yaml`
- Create: `candidates/core-profile-v1/primitive_state_resolution_v1.yaml`
- Create: `candidates/core-profile-v1/bazi_mapping_registry_v1.yaml`
- Create: `candidates/core-profile-v1/astrology_mapping_registry_v1.yaml`
- Create: `candidates/core-profile-v1/primitive_relation_graph_v2.yaml`
- Test: `tests/test_semantic_candidate_release.py`

**Interfaces:**
- Consumes: C1–C3 可审阅语义设计与匿名化事实夹具定义。
- Produces: 经产品审阅的差异性、模板坍塌、相似度与跨 Agent 校准标准。

- [ ] **Step 1: 定义通用坍塌指标与相似度矩阵**

规定所有 Dynamic Family 统一计算 `dynamic_family_frequency`、
`evidence_supported_frequency`、`unsupported_activation_frequency`。规定
`Pairwise Profile Similarity Matrix` 比较加权 Primitive、Signature Primitive、
Dynamic Family/Pole 和 Fate Theme 重叠；不得使用少数命名 Family 或唯一 ID 数量代替。
同时定义 Machine Core Determinism：同 Fact Packet、同 Semantic Bundle、同确定性执行
配置必须得到规范化后相同的 Core Profile IR；Narrative Variability 仅存在于 Renderer。

- [ ] **Step 2: 形成待批准的校准阈值与例外记录**

将阈值字段、豁免条件、样本覆盖范围和失败处置写入审阅文档。将样本显式分为只可调模型的
`Design / Calibration Set` 与规则冻结后才可读取的 `Holdout Validation Set`；Holdout
必须包含弱信号的 Ambiguous / Middle Cases（中等力量、多个 Primitive 接近、无明显
Dynamic）。Golden Sample 只能属于 calibration/regression。C4a 只批准校准协议和零容忍
安全规则；数值阈值在 D1 可审计输出出现后进入 C4b，避免“Schema correct”被误当成
“人格模型 correct”。

- [ ] **Step 3: 从已审阅设计生成候选 YAML 投影并验证隔离**

每个 YAML 必须写入对应 C1–C4 文档引用和 `review_status: pending`，不得新增设计文档
未定义的 Primitive、Mapping、关系或阈值。添加并运行：

```python
def test_core_profile_candidates_are_not_runtime_configs() -> None:
    candidate_root = PROJECT_ROOT / "candidates" / "core-profile-v1"
    assert (candidate_root / "primitive_ontology_v1.yaml").is_file()
    assert not (SKILL_ROOT / "configs" / "primitive_ontology_v1.yaml").exists()
    assert not (SKILL_ROOT / "configs" / "bazi_mapping_registry_v1.yaml").exists()
```

Run: `python3 -m pytest tests/test_semantic_candidate_release.py -q`

Expected: PASS；候选文件仅用于审阅和追踪，不能使 `SEMANTIC_CONFIG_CHECKED` 通过。

### 强制产品负责人批准门 A

- [ ] **Step 1: 汇总 C1–C4 审阅包**

提交 `core-personality-ontology-review-v1.md`、两份体系 Mapping Review、
`dynamic-formation-review-v1.md`、`shadow-mature-fate-archetype-review-v1.md`、
`core-profile-calibration-review-v1.md` 及其决策记录。

- [ ] **Step 2: 停止等待明确批准**

在产品负责人明确批准 C1–C4a 前，禁止创建候选 Semantic Builder。批准后只允许进入 D1：
`candidates/core-profile-v1/*.yaml` 与候选代码必须带 `review_status: pending` 或
`candidate_mode`，不得进入 `destiny-personality/configs/`、默认 Router、公开仓库或用户
报告。候选实现只能在 Design / Calibration Set 运行，且不能通过 `SEMANTIC_CONFIG_CHECKED`。

## 阶段 D1：非默认候选 Semantic Core 与 Core Profile Builder

### Task 7: 实现隔离的候选 Profile Builder

**Files:**
- Create: `candidates/core-profile-v1/primitive_ontology_v1.yaml`
- Create: `candidates/core-profile-v1/primitive_state_resolution_v1.yaml`
- Create: `candidates/core-profile-v1/bazi_mapping_registry_v1.yaml`
- Create: `candidates/core-profile-v1/astrology_mapping_registry_v1.yaml`
- Create: `candidates/core-profile-v1/primitive_relation_graph_v2.yaml`
- Create: `candidates/core-profile-v1/score_model_v2_3.yaml`
- Create: `candidates/core-profile-v1/core_profile_calibration_policy_v1.yaml`
- Create: `candidates/core-profile-v1/signature_formation_policy_v1.yaml`
- Create: `candidates/core-profile-v1/dynamic_formation_policy_v1.yaml`
- Create: `candidates/core-profile-v1/derived_theme_policy_v1.yaml`
- Create: `src/destiny_personality/core_profile_models.py`
- Create: `src/destiny_personality/core_profile_builder.py`
- Create: `src/destiny_personality/core_profile_validation.py`
- Create: `tests/test_core_profile_builder.py`
- Create: `tests/fixtures/core_profile_calibration/design_set/`
- Create: `tests/test_core_profile_determinism.py`
- Create: `tests/test_profile_differentiation.py`
- Create: `tests/test_template_collapse.py`
- Modify: `src/destiny_personality/__init__.py`
- Modify: `src/destiny_personality/semantic_bundle.py`

**Interfaces:**
- Consumes: accepted fact packet、C1–C4a 已批准设计、从其投影的候选语义资产、existing loaders。
- Produces: candidate-only immutable `CoreDestinyProfile` and
  `build_core_profile(fact_packet, semantic_bundle, candidate_mode=True)`.

- [ ] **Step 1: 写失败测试，验证独立候选、unknown 保护与 Renderer 无关性**

```python
def test_build_core_profile_keeps_system_candidates_independent(profile_fixture):
    profile = build_core_profile(
        profile_fixture.fact_packet,
        profile_fixture.semantic_bundle,
    )
    assert profile.schema_version == "core-destiny-profile-v1"
    assert profile.bazi_primitive_candidates
    assert profile.astrology_primitive_candidates
    assert profile.primitive_states["P001"].state == "unknown"
    assert profile.archetype is None or profile.archetype.source_dynamic_refs
    assert all(theme.source_dynamic_refs for theme in profile.fate_themes)
    assert profile.renderer_profile is None


def test_same_facts_and_semantic_bundle_produce_identical_normalized_profile(profile_fixture):
    first = build_core_profile(profile_fixture.fact_packet, profile_fixture.semantic_bundle)
    second = build_core_profile(profile_fixture.fact_packet, profile_fixture.semantic_bundle)
    assert normalize_core_profile(first) == normalize_core_profile(second)
```

- [ ] **Step 2: 运行测试并确认失败**

Run: `python3 -m pytest tests/test_core_profile_builder.py::test_build_core_profile_keeps_system_candidates_independent -q`

Expected: FAIL，因为 Builder、模型和批准资产尚不存在。

- [ ] **Step 2a: 创建仅供 D1 使用的 Design / Calibration Fixtures**

在 `tests/fixtures/core_profile_calibration/design_set/` 建立八个匿名事实包：
`high_autonomy_high_change`、`high_stability_low_change`、
`high_affiliation_low_autonomy`、`high_action_low_reflection`、
`high_affect_low_structure`、`high_rules_responsibility`、
`cross_system_tension` 和 `unknown_birth_time`。它们仅供候选 Builder 与 C4b 校准，
不得进入公开仓库或用户报告。

- [ ] **Step 3: 实现不可变 Core Profile 模型**

使用 frozen dataclasses 定义：

```python
CoreDestinyProfile
PrimitiveCandidate
PrimitiveState
CrossSystemAlignment
DominantSignature
CoreDynamic
ShadowForm
MatureIntegration
FateTheme
Archetype
ProfileAuditEntry
```

禁止模型包含 Markdown、章节标题、段落、Renderer profile 或用户可见文案字段。

- [ ] **Step 4: 实现 Builder 的固定顺序**

实现以下纯函数管线：

```python
extract_bazi_candidates(...)
extract_astrology_candidates(...)
resolve_primitive_states(...)
align_cross_system(...)
select_dominant_signatures(...)
select_core_dynamics(...)
derive_shadow_forms(...)
derive_mature_integrations(...)
detect_cross_dynamic_patterns(...)
derive_fate_themes(...)
derive_archetype(...)
build_core_profile(...)
```

`select_core_dynamics` 必须只从双方已激活的 Primitive 与已批准 Relation Rule 生成，
按 priority 最多选择 7 个，通常为 2–5 个；无有效 Dynamic 时返回空元组与限制项。
`align_cross_system` 可返回 `unresolved` 或 `non_comparable`，两者均不得进入强制综合
或提升单端 Trait Salience。Fate Theme 默认基于跨 Dynamic 重复模式；受控例外是单一极强
Dynamic 具有独立跨上下文重复证据。Archetype 必须是可选结果并携带 Dynamic、稳定力量、
发展力量和反证引用。`correction` 只能限定既有语义结论的适用范围，不得改写另一个
体系的事实。`fact_assurance = none` 返回 stopped execution artifact，不得进入本管线。
`score_model_v2_3.yaml` 必须独立声明新 Alignment 状态；不得修改冻结的
`score_model_v2_2.yaml`。
三个 Formation Policy 必须写入 `semantic_model_versions`；任何缺失 Policy 必须关闭对应
派生路径并降为 `project_semantic_partial`，不能由 Python 临时分支或 Prompt 补写。

- [ ] **Step 5: 实现 Profile Validator**

Validator 拒绝：unknown 被降为 low、跨系统候选提前合并、无 rule ref 的状态、
无事实引用的 Signature/Dynamic/FateTheme/Archetype、Renderer 字段、超出 7 个 Dynamic、
无跨 Dynamic 或跨上下文重复支持的 Fate Theme、无引用的 Archetype、Archetype 反向支持
底层结论、`fact_assurance = none` 的正常 Profile，和把 `capability_reported` 提升为
`project_verified` 的输出。

- [ ] **Step 6: 运行 Builder、语义 Bundle 与全量测试**

Run:

```bash
python3 -m pytest tests/test_core_profile_builder.py tests/test_semantic_contract_bundle.py -q
python3 -m pytest -q
```

Expected: PASS；候选 Builder 只能读取 `candidates/core-profile-v1/`，并且不得由
默认 Skill Router、公开仓库或用户请求调用。

## 阶段 C4b：经验校准与第二批准门

### Task 8: 用 D1 输出冻结数值校准策略

**Files:**
- Modify: `docs/domain/core-profile-calibration-review-v1.md`
- Modify: `docs/domain/core-profile-similarity-policy-v1.md`
- Modify: `docs/domain/template-collapse-policy-v1.md`
- Modify: `candidates/core-profile-v1/core_profile_calibration_policy_v1.yaml`
- Create: `docs/domain/c4b-calibration-decision-record-v1.md`
- Test: D1 Design / Calibration Set 的确定性、相似度与坍塌评估

**Interfaces:**
- Consumes: D1 候选 Builder 的规范化 Profile 输出与隔离的 Design / Calibration Set。
- Produces: 已冻结的候选 Bundle 指纹、数值阈值、例外和 Holdout 访问规则；仍非生产配置。

- [ ] **Step 1: 运行 D1 的 Design / Calibration Set 并记录原始指标**

记录每一对 Profile 的 Similarity Matrix、每个 Dynamic Family 的四项坍塌指标、
`CORE_DETERMINISM_ERROR` 结果和全部限制。不得读取 `holdout_set/`。

- [ ] **Step 2: 写入候选数值策略与决策记录**

策略必须带 `bundle_fingerprint`、`review_status: pending`、权重、对照对阈值、
例外、`unsupported_activation_frequency: 0` 和引用到全部 C4 审阅文档。任何阈值改变
都改变 Bundle 指纹并重新执行 Calibration Set。

- [ ] **Step 3: 产品负责人批准门 B**

暂停并提交 C4b 决策记录。未获对精确 Bundle 指纹和数值策略的明确批准前，不得将候选
资产复制到 `destiny-personality/configs/`、设置为默认路径或访问 Holdout Set。

## 阶段 D2：生产 Semantic Core 提升

### Task 9: 仅提升经 C4b 批准的候选资产

**Files:**
- Create: `destiny-personality/configs/primitive_ontology_v1.yaml`
- Create: `destiny-personality/configs/primitive_state_resolution_v1.yaml`
- Create: `destiny-personality/configs/bazi_mapping_registry_v1.yaml`
- Create: `destiny-personality/configs/astrology_mapping_registry_v1.yaml`
- Create: `destiny-personality/configs/primitive_relation_graph_v2.yaml`
- Create: `destiny-personality/configs/score_model_v2_3.yaml`
- Create: `destiny-personality/configs/core_profile_calibration_policy_v1.yaml`
- Create: `destiny-personality/configs/signature_formation_policy_v1.yaml`
- Create: `destiny-personality/configs/dynamic_formation_policy_v1.yaml`
- Create: `destiny-personality/configs/derived_theme_policy_v1.yaml`
- Modify: `src/destiny_personality/semantic_bundle.py`
- Test: `tests/test_semantic_contract_bundle.py`

**Interfaces:**
- Consumes: C4b 明确批准的候选 Bundle 指纹和数值策略。
- Produces: 可由受控 Core Profile 路由读取的生产语义 Bundle；仍不自动成为默认输出路径。

- [ ] **Step 1: 校验批准指纹后复制精确候选资产**

复制前验证候选文件的 Bundle 指纹与 C4b 决策记录完全一致。任何差异、待定状态或缺失
批准均返回 `CONFIG_GAP`，不复制任何文件。

- [ ] **Step 2: 以生产位置重跑 Bundle 与确定性测试**

Run:

```bash
python3 -m pytest tests/test_semantic_contract_bundle.py tests/test_core_profile_builder.py -q
```

Expected: PASS；生产 Bundle 与批准候选 Bundle 行为相同，Legacy V2 未受影响。

## 阶段 E：动态报告规划与新 Renderer 合同

### Task 10: 构建只消费 Profile 的 Report Planner

**Files:**
- Create: `src/destiny_personality/report_plan_models.py`
- Create: `src/destiny_personality/report_planner.py`
- Create: `destiny-personality/references/renderer-profiles.md`
- Create: `destiny-personality/checklists/report-plan.md`
- Create: `tests/test_report_planner.py`
- Modify: `destiny-personality/SKILL.md`

**Interfaces:**
- Consumes: validated `CoreDestinyProfile`。
- Produces: immutable `ReportPlan` with `concise-portrait-v1`、`standard-portrait-v1`、
  `dynamic-long-form-v1` 或 `legacy-long-form-v2`。

- [ ] **Step 1: 写失败测试，证明没有激活主题不会进入计划**

```python
def test_standard_plan_selects_only_profile_backed_topics(core_profile):
    plan = build_report_plan(core_profile, renderer_profile="standard-portrait-v1")
    assert all(topic.profile_refs for topic in plan.selected_topics)
    assert "public_authorship" not in plan.selected_topic_ids
    assert plan.section_count_reason in {"within_experience_target", "evidence_limited"}


def test_standard_plan_does_not_pad_sparse_profile(sparse_core_profile):
    plan = build_report_plan(sparse_core_profile, renderer_profile="standard-portrait-v1")
    assert len(plan.section_plan) < 8
    assert plan.section_count_reason == "evidence_limited"
    assert all(topic.profile_refs for topic in plan.selected_topics)
```

- [ ] **Step 2: 运行测试并确认失败**

Run: `python3 -m pytest tests/test_report_planner.py::test_standard_plan_selects_only_profile_backed_topics -q`

Expected: FAIL，因为 Planner 尚不存在。

- [ ] **Step 3: 实现 Renderer Profile 选择规则**

体验规模目标：

```text
concise-portrait-v1: target 4–10 sections
standard-portrait-v1: target 8–16 sections
dynamic-long-form-v1: target 16–32 sections
legacy-long-form-v2: fixed 56 sections, compatibility only
```

Planner 按 Dynamic priority、Signature salience、证据稳定性和用户目标选择主题。每个
Topic 都引用现有 Profile 条目；未选 Candidate Topic 必须记录缺乏激活证据、优先级不足
或与更高优先级主题重复的原因。新 Renderer 的目标区间不构成硬下限或填充要求；证据不足
时必须输出较短计划并记录 `evidence_limited`，不得添加无证据 Topic。

- [ ] **Step 4: 实现 Renderer Containment 校验**

Renderer 输入必须是 `ReportPlan + CoreDestinyProfile`，不接受裸 Fact Packet。验证每个
报告核心断言都含 `profile_refs`，且其引用在 Profile 中存在；违反时抛出
`INFERENCE_GUARD_ERROR`。

- [ ] **Step 5: 运行 Planner 与全量测试**

Run:

```bash
python3 -m pytest tests/test_report_planner.py -q
python3 -m pytest -q
```

Expected: PASS。

## 阶段 F：Holdout、模板坍塌与叙事层业务验证

### Task 11: 建立差异性优先的 Holdout 评估门

**Files:**
- Create: `tests/fixtures/core_profile_calibration/holdout_set/`
- Create: `tests/test_renderer_containment.py`
- Create: `src/destiny_personality/profile_similarity.py`
- Create: `src/destiny_personality/template_collapse.py`
- Modify: `destiny-personality/checklists/business-test.md`
- Modify: `destiny-personality/references/failure-policy.md`

**Interfaces:**
- Consumes: validated Core Profile Builder、Planner 与匿名化事实夹具。
- Produces: Pairwise Profile Similarity Matrix、通用模板坍塌指标、Containment 和跨 Agent 验收记录。

- [ ] **Step 1: 创建隔离的 Holdout Fixture 清单**

Design / Calibration Set 已在 D1 创建。现在只建立 Holdout Fixtures，每个夹具只含可公开
测试的 Canonical Facts 和预期结构差异，不含 Golden Sample 原始报告或文案：

```text
middle_autonomy_middle_stability
near_equal_primitive_signals
no_dominant_signature
no_clear_core_dynamic
unknown_or_limited_context
```

规则冻结前不得依据 Holdout 结果调整 Ontology、Mapping、Formation Policy 或阈值；规则
冻结后读取 Holdout 也不得修改同一 Bundle 的任何已批准资产。

- [ ] **Step 2: 写差异性失败测试**

```python
def test_pairwise_profile_similarity_obeys_approved_policy(
    calibration_profiles, approved_similarity_policy
):
    matrix = build_pairwise_profile_similarity_matrix(calibration_profiles)
    assert matrix["high_autonomy_high_change"]["high_stability_low_change"].overall_similarity <= (
        approved_similarity_policy.maximum_contrasting_case_similarity
    )
    assert set(matrix["high_autonomy_high_change"]["high_stability_low_change"].components) == {
        "weighted_primitive_overlap",
        "signature_primitive_overlap",
        "dynamic_family_pole_overlap",
        "fate_theme_overlap",
    }
```

- [ ] **Step 3: 写 Core Determinism 与 Holdout 测试**

```python
def test_machine_core_is_deterministic_for_same_facts_and_bundle(profile_fixture):
    first = build_core_profile(profile_fixture.fact_packet, profile_fixture.semantic_bundle)
    second = build_core_profile(profile_fixture.fact_packet, profile_fixture.semantic_bundle)
    assert normalize_core_profile(first) == normalize_core_profile(second)


def test_holdout_weak_signal_cases_do_not_force_topics(holdout_profiles):
    for profile in holdout_profiles:
        assert all(dynamic.source_primitive_refs for dynamic in profile.core_dynamics)
        assert all(theme.source_dynamic_refs for theme in profile.fate_themes)
```

- [ ] **Step 4: 写模板坍塌失败测试**

```python
def test_dynamic_families_have_evidence_supported_activation(calibration_profiles, approved_collapse_policy):
    metrics = assess_dynamic_family_activation(calibration_profiles)
    for family_metric in metrics:
        assert family_metric.dynamic_family_frequency >= family_metric.evidence_supported_frequency
        assert family_metric.unsupported_activation_frequency <= (
            approved_collapse_policy.maximum_unsupported_activation_frequency
        )
        assert family_metric.dynamic_family_frequency <= (
            family_metric.evidence_supported_frequency
            + approved_collapse_policy.allowed_contextualized_activations
        )
```

- [ ] **Step 5: 实现夹具、评估器与失败策略**

测试必须基于真实 Builder 输出，不允许手工伪造 Profile 结果。所有阈值从 C4 已批准的
`core_profile_calibration_policy_v1.yaml` 读取，不得硬编码为某两个 Dynamic Family 的出现
次数。若差异性、相似度或坍塌阈值失败，记录 `TEMPLATE_COLLAPSE_ERROR` 并阻止该
Semantic Model 版本成为默认业务路径。

- [ ] **Step 6: 执行 Core Determinism 与叙事层业务测试**

对每个 Calibration Case 使用相同 Semantic Bundle 重复构建 Core Profile，比较：

```text
top primitives
dominant signatures
core dynamics
fate themes
semantic rule references
limitations
```

上述 Core IR 的差异一律为 release blocker；`unresolved` 与 `non_comparable` 是可审计
结果，只有无依据地强行综合时才构成 blocker。再使用至少两个 Agent 对**同一已冻结的
Core Profile**渲染报告：文字相似度不作为通过条件，但 Agent 不得改写 Profile 结构。

- [ ] **Step 7: 全量回归与形成发布建议**

Run:

```bash
python3 -m pytest -q
python3 /Users/lht/.codex/skills/.system/skill-creator/scripts/quick_validate.py destiny-personality
```

所有测试通过后，形成“可提升为默认路径”的发布建议与完整审计记录；不得自动发布。不得
复制 fixtures、个人报告、候选审批记录或任何未批准语义资产。

## 阶段 G：默认路径提升与公开发布

### Task 12: 在阶段 F 通过后发布已批准版本

**Files:**
- Modify: `release/qia-zhi-yi-suan/`
- Test: 全量回归、脱敏审查、公开仓库内容清单

**Interfaces:**
- Consumes: 阶段 F 全部通过记录与产品负责人对默认路径提升的明确同意。
- Produces: `v0.2.0-core-profile` 公开发布；Legacy Renderer 仍可回归。

- [ ] **Step 1: 确认默认路径提升授权**

产品负责人未明确同意时停止于阶段 F；测试通过本身不构成发布授权。

- [ ] **Step 2: 脱敏同步并发布**

仅复制经审查的 Skill、合同、已批准生产配置与源码到 `release/qia-zhi-yi-suan/`，在隔离
公开仓库创建 `v0.2.0-core-profile` 提交与标签并推送 GitHub。不得复制 fixtures、个人报告、
候选审批记录或任何未批准语义资产。

## 执行顺序与停止点

1. 执行阶段 A 与 B。
2. 依序执行 C1（人格本体）、C2（八字/西占映射）、C3（Dynamic 形成）和 C4a（校准
   协议）设计审阅；不得跳过任一层，也不得以 YAML 完整性替代语义审阅。
3. 在 C1–C4a 全部形成完整决策记录后，**停止等待产品负责人明确批准门 A**。
4. 门 A 通过后只执行 D1：候选 Builder 和候选资产仅可在 Design / Calibration Set 运行，
   不得进入默认路径、`configs/`、公开仓库或用户报告。
5. 执行 C4b，以 D1 输出冻结 Bundle 指纹、数值阈值和例外；随后停止等待产品负责人明确
   批准门 B。
6. 门 B 通过后执行 D2，将精确批准的候选资产提升为生产 Bundle；通过 Builder 和
   Validator 后执行阶段 E 的 Planner / Renderer。
7. 使用隔离 Holdout 执行阶段 F 的差异性、模板坍塌、相似度、确定性与 Containment 验收，
   形成默认路径提升建议。
8. 只有产品负责人另行同意默认路径提升与公开发布时，才执行阶段 G。

门 A 允许候选实现而不允许生产提升；门 B 允许生产提升而不允许默认发布；阶段 G 的发布
授权同样不可由测试通过替代。未通过任一授权门时，保持 Legacy V2 可用，但不得把候选或
已实现的语义资产作为新默认推理系统发布。
