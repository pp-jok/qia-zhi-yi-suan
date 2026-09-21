# Core Profile 双轨渐进式整改设计

## 目标

将当前以固定长篇人格书为中心的运行路径，整改为先建立可复用、可审计、
差异化的 `Core Destiny Profile`，再由独立 Report Planner 决定写什么、写多深和
采用何种 Renderer。现有 V2 长篇报告保留为兼容性输出，不再参与核心人格结构发现。

整改遵循两条原则：

1. 固化方法，不固化结论。
2. 先建立人，再决定写什么。

## 非目标

- 不替换或打包外部排盘软件。
- 不移除现有 Calculation Methodology、Capability Protocol、Evidence Anchor、
  Failure Policy、Time Sensitivity 或 Controlled Inference 的安全边界。
- 不在本次整改中实现事业、关系、财富、时运或合盘等下游产品。
- 不删除当前 V2 长篇报告能力。

## 版本策略

当前公开能力被冻结为 `legacy-long-form-v2`，并在公开仓库中标记为
`v0.1.0-legacy-long-form`。后续核心整改在 `v0.2-core-profile` 线上进行。

旧版继续接受原有输入与执行配置，用于历史回归、用户兼容和新旧结果对照；
不再向旧版新增固定章节、固定人格主题或长度要求。新链路不得依赖旧版
`long-form-personality-book-v2`、`reader-first-depth-v2`、固定五道权利或任何
个案原型名称。

## 总体架构

```text
Birth Input
  ↓
Calculation Provider
  ↓
Canonical Chart Facts
  ├── legacy-long-form-v2
  └── Core Reasoning Engine
        ├── Bazi Signal Extractor
        ├── Astrology Signal Extractor
        ├── Bazi Primitive Candidates
        ├── Astrology Primitive Candidates
        ├── Primitive State Resolution
        ├── Cross-System Alignment
        ├── Dominant Signature Extraction
        ├── Core Dynamic Selection
        ├── Shadow Form Derivation
        ├── Mature Integration Derivation
        ├── Cross-Dynamic Pattern Detection
        ├── Fate Theme Derivation
        ├── Archetype Derivation
        └── Core Destiny Profile
              ↓
           Report Planner
              ├── concise-portrait-v1
              ├── standard-portrait-v1
              └── dynamic-long-form-v1
```

Renderer 只能读取 `Core Destiny Profile`；它不能读取原始命盘事实后自行补充
人格结构，也不能修改 Profile。

## Core Destiny Profile 合同

新增 `core-destiny-profile-v1`，作为人格产品和未来下游领域产品的正式 IR。
Root fields 固定为：

1. `schema_version`: `core-destiny-profile-v1`
2. `core_profile_id`: execution-local、不可作为跨执行身份标识的 ID
3. `fact_packet_refs`: 已接受事实包引用
4. `fact_assurance`: `project_verified`、`capability_reported` 或 `none`
5. `semantic_model_assurance`: `project_semantic_verified`、
   `project_semantic_partial` 或 `none`
6. `semantic_model_versions`: Ontology、State Policy、两套独立 Mapping、Relation、
   Signature Formation、Dynamic Formation、Derived Theme 与 Archetype Policy 的实际
   版本引用
7. `bazi_primitive_candidates`
8. `astrology_primitive_candidates`
9. `primitive_states`
10. `cross_system_alignment`
11. `dominant_signatures`
12. `core_dynamics`
13. `shadow_mature_forms`
14. `fate_themes`
15. `archetype`
16. `contradictions`
17. `limitations`
18. `unresolved_questions`
19. `audit_trail`

`fact_assurance` 与 `semantic_model_assurance` 必须分离。外部事实可为
`capability_reported`，但只要项目内 Semantic Core 的版本化资产完整并通过校验，
Profile 可标记 `project_semantic_verified`。这不升级事实本身，也不等于严格生产认证。

`fact_assurance = none` 时禁止执行 Core Profile 推理，也不得产生正常的
`core-destiny-profile-v1`。系统只能生成说明缺少有效事实基础的 stopped execution artifact；
它不得带有 Primitive、Signature、Dynamic、Fate Theme 或 Archetype 结论。

任何 Core Profile 结论必须包含事实引用、映射规则引用、状态/签名/动态来源、
置信度或优先级、限制和适用上下文。Profile 是版本化推断模型，不是确定性人格事实。

## Semantic Core

### Primitive Ontology 与状态

建立生产级 `primitive_ontology_v1.yaml`，分为 `core` 与 `extended` 两组。
Primitive 只描述基础人格倾向，不预埋 Shadow、Fate Theme、Archetype 或某个 Golden
Sample 的特定主题。

Primitive State 只能为：

```text
supported_high
supported_low
mixed
unknown
```

缺失、未计算、未映射或相互冲突的证据不得自动成为 `supported_low`。每个状态必须
保留正向、反向、修正和缺失证据。

### 独立映射

八字与西占分别生成 Primitive Candidates：

```text
bazi_primitive_candidates
astrology_primitive_candidates
```

两个 Mapping Registry 必须独立版本化。规则必须包含事实条件、上下文条件、方向、
强度、修正条件、排除条件和规则引用。Agent 不得临场创建 Mapping。

Cross-System Alignment 仅可把独立候选关系标记为 `validation`、`complement`、
`contextualization`、`tension`、`correction`、`unresolved` 或 `non_comparable`。
`unresolved` 表示现有证据不足以判断关系；`non_comparable` 表示两个候选不在可比较的
语义粒度或上下文中。后二者必须保留各自候选和限制，**不得强行综合出统一人格结论**。
跨系统一致性不得直接增加单一 Primitive 的 Trait Salience；张力不得降低任一端已被支持
的强度。

`correction` 只允许表示**对既有语义推断适用范围的限定**，例如一个系统提供的上下文使
另一系统所支持的倾向不能被概括到所有关系或生活场景。它不得表示一个体系纠正、否定或
改写另一个体系的命盘事实；无法满足该定义时必须使用 `contextualization`、`unresolved`
或 `non_comparable`。

现有 `score_model_v2_2.yaml` 作为 Legacy V2 基线冻结。Core Profile 链路须使用新增且
独立版本化的 `score_model_v2_3.yaml`（或后续批准版本）声明上述 Alignment 状态；不得
悄然改变旧模型的可接受值或其回归行为。

### Signature 与 Dynamic

`Dominant Signature` 是多个已解决 Primitive State 和其来源信号的可解释组合。
每个 Signature 必须记录：来源系统、Primitive、显著度、稳定度、适用上下文、反证和
限制。

`Core Dynamic` 是被实际激活的两极关系，而不是 Relation Graph 的默认结果。每个
Dynamic 必须记录：

```text
dynamic_id
pole_a
pole_b
source_primitive_refs
source_signature_refs
relation_rule_ref
support
modifiers
contextualizers
true_tension
shadow_form
mature_form
priority
limitations
```

每份 Profile 可选择 **0–7** 个 Core Dynamics，通常为 **2–5** 个。数量是观察到的
结构结果而非完成指标：证据不足、关系未激活或不可比较时，少于两个乃至零个均为合法结果。
没有双方激活 Primitive、已批准的关系规则和充分上下文时，不得生成 Dynamic，也不得为
满足数量目标补造次级 Dynamic。

Relation Graph 仅为候选关系库，不能成为人格答案库。

### Shadow、Mature、Fate 与 Archetype 的分层

派生不得合并为单一“形式与主题”步骤，固定顺序为：

```text
Core Dynamic
  → Shadow Form
  → Mature Integration
  → repeated patterns across dynamics
  → Fate Theme
  → Archetype
```

- `ShadowForm` 必须指向一个已激活 `CoreDynamic`，描述该张力在压力、资源不足或防御性
  情境下的失衡表达；不能由单一 Primitive 直接生成。
- `MatureIntegration` 必须指向同一 `CoreDynamic`，描述两极在具备条件时可被同时持有的
  整合方式；它不是 Shadow 的反义标签。
- `FateTheme` 默认从多个 Dynamic 的重复模式、稳定力量与发展方向中归纳；也可以来自
  一个极强 Dynamic 在至少两个独立上下文中的重复证据。后者必须额外记录
  `cross_context_recurrence_refs`，且不得由单一 Dynamic 自动升级。两条路径都必须记录
  `source_dynamic_refs`、`stable_force_refs`、`movement_force_refs`、
  `development_theme_refs` 与限制。
- `Archetype` 是 Profile 的可选高层概括，而非固定标签。它必须包含 `archetype_id`、
  `source_dynamic_refs`、`stable_force_refs`、`movement_force_refs`、
  `development_theme_refs`、`support_level`、`counterevidence_refs`、`limitations` 和
  `context`。证据不足时 `archetype` 可为空，不能用模板名称填充。
  Archetype 只能压缩既有 Profile 结论，不能反向生成或提高 Primitive、Dynamic、Theme 的
  支持度；Validator 必须拒绝这种反向推理。

### Core Determinism 与 Narrative Variability

Semantic Core 是版本化推理资产，而非由 Agent 临场裁量的提示词效果。相同的已接受
Fact Packet、相同的 Semantic Bundle 版本与相同的确定性执行配置，必须产生字节级等价
或在合同中明确规范化后等价的 Core Profile IR。至少以下结构不得因 Agent 而改变：

```text
primitive_states
dominant_signature membership
core_dynamic membership and poles
fate_theme basis
archetype basis
limitations and unresolved states
```

不同 Agent 可在 Renderer 层产生不同的解释语言、例子、章节组合和写作风格；这些属于
`Narrative Variability`，不得回流或改写 Core Profile。

每个形成阶段必须有可审计的版本引用。最小生产资产为：

```text
signature_formation_policy_v1
dynamic_formation_policy_v1
derived_theme_policy_v1
```

它们可以是独立配置或版本化代码资产，但必须写入 `semantic_model_versions`，并可由
Profile 的审计记录定位；不得把关键形成规则隐藏为未版本化的 Python 分支或 LLM Prompt。

`project_semantic_verified` 仅表示**当前 Profile 实际使用的全部语义资产**均存在、获批、
版本匹配并通过验证；不要求无关路径的资产齐备。`project_semantic_partial` 表示 Profile
可在已完备路径上生成，但缺失资产关闭相应派生路径。例如缺少 `derived_theme_policy_v1`
时，`fate_themes` 必须为空并记录限制，而不是自由补写主题。

## Profile 推理边界

新的 Semantic Core 可以在 `controlled_inference` 中运行，但前提是：

- 事实包已通过既有资格与方法校验；
- 所有被使用的 Semantic Asset 均为项目内版本化生产资产；
- 每个 Profile 输出保留事实与语义规则审计；
- 任一缺失资产降低 `semantic_model_assurance` 或阻止相关结论；
- Agent 不得将 Core Profile 解释为严格事实、诊断或预测。

`strict` 仍维持原有严格计算与语义配置门。Core Profile 的引入不绕过任何 strict
Gate。

## Report Planner 与 Renderer

新增 Report Planner，输入为 Core Profile 和用户选择的 `renderer_profile`。它负责：

- 选择值得呈现的 Signatures、Dynamics、Shadow/Mature Forms、Fate Themes 和
  Archetype；
- 根据优先级、证据充分度和用户请求确定章节数量与深度；
- 记录每个输出主题对应的 Profile 引用；
- 排除没有被激活的 Candidate Topic。

支持四类输出：

| Renderer profile | 默认规模 | 用途 |
| --- | --- | --- |
| `concise-portrait-v1` | 建议 4–10 节 | 快速核心画像 |
| `standard-portrait-v1` | 建议 8–16 节 | 默认完整业务报告 |
| `dynamic-long-form-v1` | 建议 16–32 节 | 深度阅读版 |
| `legacy-long-form-v2` | 固定 56 章 | 历史兼容与对照 |

前三类规模是阅读体验目标，不是 Validator 的硬性上下限。证据稀疏时，Planner 可以输出
少于建议下限的报告，并记录 `evidence_limited`；证据丰富时也只能在 Profile 支持范围内
扩展。章节数不得成为补造 Topic、Dynamic 或 Theme 的理由。

新 Renderer 只能表达已存在于 Core Profile 中的内容，不能为了章节完整性创建新的
Primitive、Signature、Dynamic、Theme 或 Archetype。没有证据的 Candidate Topic
不进入 Report Plan；新链路不使用空的 `insufficient_basis` 章节维持模板。

## 测试与验收

保留事实准确率、能力资格、来源、锚点、限制、出生时间不确定性与越界防护测试。
新增以下验证：

1. **Profile Contract Tests**：字段顺序、引用完整性、状态合法性、版本一致性和
   Profile 不可由 Renderer 修改。
2. **Mapping Tests**：八字与西占独立映射；上下文条件、修正和排除规则按预期工作；
   unknown 不变 low。
3. **Machine Core Determinism**：相同 Fact Packet、Semantic Bundle 和执行配置重复运行
   必须得到规范化后相同的 Core Profile IR；这一测试独立于 Agent 文案。
4. **Narrative Variability**：不同 Agent 可产生不同表达，但 Renderer 输入 Profile、
   核心结构引用与事实边界必须保持不变。
5. **Differentiation Calibration**：Design / Calibration Set 至少覆盖高自主高变化、
   高稳定低变化、高关系依赖低自主、高行动低反思、高情绪低结构、强规则责任导向、
   跨系统不一致、出生时间未知；该集合只能用于调规则，不能作为最终泛化证明。
6. **Holdout Validation**：规则冻结后，在与 Calibration Set 隔离的 Holdout Validation
   Set 上验证差异性、坍塌和 Containment；Golden Sample 仅能属于 calibration/regression，
   不得同时承担最终有效性证明。
7. **Ambiguous / Middle Cases**：Holdout 必须包含中等自主、中等稳定、多个 Primitive
   接近、无突出力量及无明显 Core Dynamic 的弱信号样本，检验系统不会硬找主题。
8. **Template Collapse Tests**：对所有 Dynamic Family 通用统计
   `dynamic_family_frequency`、`evidence_supported_frequency` 和
   `unsupported_activation_frequency`。异常高频或无证据激活由经审批的校准策略判定，
   不得只为少数命名 Family 设置阈值。
9. **Differentiation Matrix**：生成 `Pairwise Profile Similarity Matrix`，比较加权
   Primitive 重叠、Signature Primitive 重叠、Dynamic Family/Pole 重叠和 Fate Theme
   重叠。相似度阈值及例外由校准审批记录提供，不能以“不同 ID 数量”替代。
10. **Renderer Containment Tests**：每个报告核心结论必须回链到 Profile；Renderer
   不得生成 Profile 外的核心结论。
11. **Legacy Regression Tests**：冻结 V2 的输入、合同和输出能力继续可用。

Golden Sample 仅用于校准事实、Top Primitive、Signature、Dynamic 和 Profile
差异；不得进入生产 Mapping、默认章节、默认 Archetype 或预期文案。

## 交付阶段

1. **阶段 A**：冻结 Legacy V2 并建立版本标签。
2. **阶段 B**：创建 Core Profile Schema、Profile Audit Checklist 与 Execution Report 扩展。
3. **阶段 C1 — Core Personality Ontology Review**：先审阅人格 Primitive、状态与
   非蕴含边界，产出语义设计文档；候选 YAML 只能是该文档的机器可读投影。
4. **阶段 C2 — Bazi / Astrology Semantic Mapping Review**：独立审阅两套体系到
   Primitive 的映射语义、上下文、反例与不可比较边界。
5. **阶段 C3 — Dynamic Formation Review**：审阅 Alignment、Signature、Dynamic、
   Shadow、Mature、Fate 与 Archetype 的形成规则，禁止将 Relation Graph 当作答案库。
6. **阶段 C4a — Calibration Protocol Review**：审阅差异性、坍塌、相似度矩阵、
   确定性和 Holdout 隔离的方法；在没有 Profile 样本前不得凭空设定数值阈值。
7. **强制产品负责人批准门 A**：C1–C4a 的设计记录获批前，不得创建候选 Semantic
   Builder。该批准只允许 D1 非默认候选实现，不允许生产配置、默认路径或公开发布。
8. **阶段 D1 — Candidate Semantic Core**：用候选资产实现隔离、不可发布的 Builder 与
   Validator，只运行 Design / Calibration Set。
9. **阶段 C4b — Empirical Calibration Review**：基于 D1 的可审计输出设定相似度权重、
   数值阈值和例外；冻结候选 Bundle 后才可读取 Holdout。
10. **强制产品负责人批准门 B**：C4b 的数值策略和候选 Bundle 获批前，不得提升为生产
    Semantic Core 或默认路径。
11. **阶段 D2 — Production Semantic Core**：将获批资产提升为生产 Semantic Core、
    Builder 与 Validator。
12. **阶段 E**：实现只消费 Core Profile 的 Planner 与 Renderer；保留 Legacy Renderer。
13. **阶段 F**：执行 Holdout、模板坍塌、相似度矩阵、确定性和叙事层业务验证。
14. **阶段 G**：仅在阶段 F 通过且产品负责人同意后，提升为默认路径并发布公开版本。

任何阶段若只改善固定长篇报告的文字表现，却没有提高人格差异性、核心结构可追溯性或
下游复用能力，不属于本次整改范围。
