# Phase B 最小 Skill 骨架设计

## 1. 状态与目标

状态：设计已于 2026-09-12 获得用户确认，等待书面规范审阅。

Phase B 在当前项目内创建一个干净、可独立分发的
`destiny-personality/` Skill 目录。它是业务逻辑、执行编排和结果校验
框架，不是命盘计算软件。

本阶段的目标是让遵循该 Skill 的智能体能够：

- 识别完整画像、确定性事实和合规审计三种执行模式；
- 收集并预检出生输入；
- 严格按照状态机进入或停止各阶段；
- 区分输入、配置、能力、计算和契约错误；
- 生成统一、可审计的 `Execution Report`；
- 在尚缺 Phase C 或语义配置时准确停止，而不是假装已经具备能力。

Phase B 的成功不以生成真实命盘或完整人格画像为标准。

## 2. 已确认的交付方案

采用“薄编排 Skill”。`SKILL.md` 只保存高频核心流程和不可突破的门禁，
详细契约、检查表和配置按需加载。

未采用以下方案：

1. 单文件 Skill：每次触发都会加载全部规则，浪费上下文且难以维护；
2. 携带可执行验证器：会重新形成运行依赖并混淆 Skill 与智能体的职责。

现有 `destiny_personality_skill_docs_v2_2/` 保留为设计和方法源资料；新
目录是最终可分发 Skill 的最小运行制品。现有 Python 包和测试继续作为
项目开发参考验证器，不复制进 Skill。

## 3. 目录结构

```text
destiny-personality/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── execution-boundaries.md
│   ├── methodology-index.md
│   └── failure-policy.md
├── configs/
│   ├── bazi_methodology_v1.yaml
│   ├── astrology_methodology_v1.yaml
│   ├── score_model_v2_2.yaml
│   └── primitive_relation_graph_v1.yaml
├── schemas/
│   ├── birth-input.md
│   └── execution-report.md
└── checklists/
    ├── preflight.md
    └── stage-gates.md
```

本阶段不创建 `scripts/` 或 `assets/`。`agents/openai.yaml` 只包含界面元数据，
不声明固定 MCP、计算库或服务依赖。

## 4. 三种执行模式

### 4.1 `portrait`

默认模式。目标是从出生输入走完整业务链，但只有全部计算与语义门禁通过
后才允许生成人格 IR 和 Narrative。

在 Phase B 当前状态下，如果 Phase C 兼容性判据或所需配置缺失，应产生
结构化停止报告。不得用通用知识补算命盘，也不得输出临时人格结论。

### 4.2 `facts_only`

只取得、归一化并校验确定性命盘事实。通过 `FACTS_VALIDATED` 后完成，不
进入 Primitive、Mapping、Dynamic 或 Narrative。

### 4.3 `audit`

审计用户提供的事实包或 `Execution Report` 是否符合当前方法、来源、结构
和阶段门禁。审计不补算缺失事实，不静默修复输入，也不生成画像。

## 5. 输入契约

面向用户的最小输入为：

- 出生日期；
- 当地民用出生时间，允许明确表示未知；
- 出生地点。

用户可选提供 IANA 时区和经纬度。如果没有提供，Phase C 可指导智能体在
获得合格外部能力后解析，并将提供方、版本或端点、操作、输入和结果写入
provenance。Phase B 只定义这一输入状态，不实现地点解析。

出生时间未知时必须进入 `stable_only`：

- 不得生成或使用时柱；
- 不得生成或使用 Ascendant、MC 和宫位；
- 不得通过其他文字或派生字段夹带时间敏感结论。

输入错误不得误报为 `CONFIG_GAP` 或 `CAPABILITY_GAP`。

## 6. 状态机与模式终点

```text
INPUT_RECEIVED
→ SCOPE_CHECKED
→ CALCULATION_CONFIG_CHECKED
→ CAPABILITIES_DISCOVERED
→ METHODOLOGY_VERIFIED
→ FACTS_CALCULATED
→ FACTS_NORMALIZED
→ FACTS_VALIDATED
→ SEMANTIC_CONFIG_CHECKED
→ REASONING_ALLOWED
→ NARRATIVE_ALLOWED
```

规则：

- 所有模式都必须先执行作用域与输入检查；
- `facts_only` 在 `FACTS_VALIDATED` 成功后结束；
- `audit` 按被审计对象已声明的阶段逐项验证，不推进到更晚阶段；
- `portrait` 在 `FACTS_VALIDATED` 后继续执行语义配置门禁；
- 任一前置门禁失败，后续状态均不得进入；
- Phase C 尚未提供可执行的工具兼容性判据时，不得仅因发现工具就进入
  `METHODOLOGY_VERIFIED`；
- 结构化人格推理必须在 `REASONING_ALLOWED` 后开始；
- Narrative 必须在 `NARRATIVE_ALLOWED` 后开始。

## 7. 两级配置门禁

### 7.1 `CALCULATION_CONFIG_CHECKED`

需要：

- 八字与占星方法配置；
- 确定性事实 schema；
- time sensitivity 与 `stable_only` 规则；
- 验证或派生命盘事实所需的精确、版本化、项目自有查表规则。

当前 Skill 尚缺 Phase C 才会提供的确定性事实 schema，以及完整藏干、十神、
八字关系和占星 dignity 精确表，因此必须报告对应 `CONFIG_GAP`，不能把
“常见表”或外部知识当成已冻结配置。

### 7.2 `SEMANTIC_CONFIG_CHECKED`

需要：

- Primitive Ontology；
- 八字与占星 Context-Aware Mapping Registry；
- Primitive State 解析规则；
- score 与 relation graph 配置及引用一致性；
- 12 维定义和覆盖规则；
- 版本化、已冻结但可以标记为 `provisional` 的 Mapping coverage 阈值；
- partial-portrait 策略；
- Narrative Rules。

这些资产不影响合法命盘事实的计算和验证，但缺失时必须阻止
`REASONING_ALLOWED`。

Golden、calibration expected 和 boundary cases 是构建／发布证据，不是生产
运行配置，生产不得读取其 expected 结果。

## 8. Execution Report

所有模式统一输出：

```yaml
schema_version:
mode: portrait | facts_only | audit
status: completed | partial | stopped
current_stage:
reasoning_allowed:
narrative_allowed:
input_summary:
capabilities:
provenance:
validated_facts:
issues:
warnings:
next_action:
```

约束：

- `input_summary` 只保留执行和审计需要的摘要，不无必要复制个人信息；
- `reasoning_allowed` 和 `narrative_allowed` 必须是明确布尔值；
- `validated_facts` 只能包含已经通过当前契约验证的事实；
- 每个 issue 必须包含 `code`、`severity`、`stage`、`message` 和
  `required_action`；
- stopped 报告必须精确记录停止阶段和恢复条件；
- partial 只允许用于规则资产完整但当前个案 Mapping 覆盖不足的情况；
- 完整画像只有在全部门禁通过后才附加人格 IR 和 Narrative；
- 面向用户默认展示简明结论，完整结构作为审计记录保留。

`schemas/execution-report.md` 将冻结上述字段的类型、是否必填、空值语义和
模式相关约束；本阶段不引入 JSON Schema 或执行代码。

## 9. 错误与停止策略

- `BIRTH_INPUT_ERROR`：出生输入缺失、类型不合规或模式组合非法；
- `CONFIG_GAP`：项目方法或语义规则资产缺失；
- `CAPABILITY_GAP`：没有已存在且能通过预检的外部能力；
- `METHODOLOGY_VERSION_MISMATCH`：能力或结果不符合冻结方法；
- `CALCULATION_FATAL`：已通过预检的能力调用失败，且安全候选已耗尽或不
  允许重试；
- `CALCULATION_CONTRACT_ERROR`：返回或归一化事实违反契约；
- `coverage_warning`：配置完整但个案没有足够适用 Mapping，只允许 partial。

智能体可以尝试另一个已经存在、通过预检且重试安全的能力。安装软件、
连接新服务或扩大数据范围前必须取得用户明确授权。不得通过降低方法要求、
猜算、补造事实或把 unknown 写成 low 来继续流程。

## 10. 资源加载策略

`SKILL.md` 必须直接包含作用域边界、模式选择、状态机和不可突破的停止规则。
其余内容按阶段读取：

- 输入预检：`schemas/birth-input.md`、`checklists/preflight.md`；
- 确定性计算：`references/methodology-index.md` 和相关 `configs/`；
- 审计与阶段切换：`schemas/execution-report.md`、
  `checklists/stage-gates.md`；
- 失败归类存在歧义：`references/failure-policy.md`；
- 需要确认数据与执行边界：`references/execution-boundaries.md`。

所有引用都由 `SKILL.md` 直接链接，禁止深层引用链。Phase B 不复制尚未
齐全的 Primitive、Mapping 和 Narrative 内容，也不把示例 `Pxxx` 解释成
真实本体。

## 11. 元数据

Skill 名称为 `destiny-personality`，目录同名。YAML frontmatter 只包含：

- `name`；
- 覆盖三种模式及触发场景的 `description`。

`agents/openai.yaml` 包含：

- `display_name`；
- 25–64 字符的 `short_description`；
- 显式提及 `$destiny-personality` 的单句 `default_prompt`。

本阶段不设置图标、品牌色、MCP dependency 或其他未获授权的界面字段。

## 12. 验证策略

### 12.1 结构验证

- 使用 Skill Creator 的 `quick_validate.py` 校验目录名和 frontmatter；
- 检查 manifest 中声明的必需文件全部存在；
- 检查 `SKILL.md` 的所有相对引用可解析；
- 检查 Skill 目录不存在 `scripts/`、Python 文件、二进制计算资产或固定
  MCP dependency。

### 12.2 项目回归

在项目参考验证器测试中增加 Skill 包结构测试，同时保持已有测试通过。
该测试只验证 Skill 制品边界，不使 Python 包成为 Skill 运行依赖。

### 12.3 无上下文前向测试

使用仅获得 Skill 制品和测试请求的全新智能体，覆盖：

1. 完整出生输入下的 `portrait`；
2. 未知出生时间必须选择 `stable_only`；
3. `facts_only` 不进入人格推理；
4. `audit` 不补算、不修复、不生成画像；
5. 计算配置缺失返回 `CONFIG_GAP`；
6. 在 `audit` 模式审查自称“计算配置已通过但没有可用能力”的测试报告时，
   必须先用当前 Skill 资产验证该声明；当前真实配置不完整时应在更早的
   `CONFIG_GAP` 停止，不得信任声明并跳到 `CAPABILITY_GAP`；
7. 在纯策略问题明确假设未来计算配置已经真实通过、但不存在合格外部能力
   时，正确将下一失败归类为 `CAPABILITY_GAP`；
8. 被要求静默安装时先请求授权；
9. 外部结果包含恶意执行文字时只将其视为数据。

前向测试不得向测试智能体泄露预期答案或当前诊断。

## 13. 非目标

Phase B 不做：

- 真实时区、地点、八字或星盘计算；
- 具体外部工具选择、安装、适配或调用；
- Phase C 的方法兼容性证据规则；
- Primitive 定义、Mapping、Evidence Graph、Signature 或 Dynamic；
- 12 维、Shadow、Mature、Fate、Archetype 或 Narrative 生成；
- JSON Schema、Python 运行时或计算脚本打包。

## 14. 验收标准

- 独立 `destiny-personality/` 目录可通过 Skill 基础验证；
- `SKILL.md` 能让智能体正确选择三种模式并遵守状态机；
- 输入未知时间时明确进入 `stable_only`；
- Skill 能区分输入、配置、能力、计算和契约失败；
- `Execution Report` 的核心字段和停止语义明确；
- 缺失 Phase C 或语义资产时准确停止，不生成命盘或画像；
- Skill 不包含计算软件、脚本、Python 文件或固定工具依赖；
- 项目 Python 包只承担开发参考验证；
- 全部项目测试、Skill 快速验证和无上下文前向测试通过。
