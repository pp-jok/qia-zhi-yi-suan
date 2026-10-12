# v0.8.0 审计型核心画像设计

## 目标

让出生输入的默认产品路径生成可复核、因人而异的核心画像和动态报告，同时不改变 formal primitive 发布资产的治理含义。

## 方案选择

1. 直接提升 candidate mapping：覆盖面高，但会将未批准资产伪装成发布事实，拒绝。
2. 继续固定解释报告：风险低，但不能解决产品链路断裂，拒绝。
3. 从已审计解释信号构建独立产品 IR：证据来源明确、可用既有双体系关系、不会污染 formal CDP，采用。

## 架构

`build_audited_interpretive_core_profile(qualified_facts)` 只接受 loader 产出的 `QualifiedFacts`。它提取已有规则信号，重用 narrative synthesis，并创建带 provenance 的候选、cross-system alignment、signature、dynamic、shadow/mature、theme 与 archetype。

`build_audited_profile_report_plan(profile)` 按稳定显著度选择不同的画像项目，过滤同一主题/证据集合的重复项。`render_audited_profile_report(profile, plan)` 不重新读取事实或规则，只将计划中已有的文本片段和证据渲染为 JSON 报告。

默认出生模式调用此链路并输出 `core_profile.json`、`report_plan.json`、`report_audit.json`。`standard-interpretive-v1` 与 `concise-interpretive-v1` 保持原行为。

## 错误与边界

- 非 `QualifiedFacts` 输入拒绝。
- 没有 traceable signals 时拒绝，不产生空壳“完整画像”。
- 单体系主题只能形成 contextual/non-comparable 条目，不宣称 cross-system validation。
- shadow/mature 仅是同一受支持方向在压力/整合条件下的反思性表达，非诊断、非预测。
- 正式 primitive `CoreDestinyProfile`、release manifest 与 candidate assets 不修改语义。

## 验收

三组完整出生输入均生成 facts、qualification、CDP、plan、report、audit；报告章节数及主题集合可变；每个展示条目可回溯至画像和信号；旧测试保持通过。

