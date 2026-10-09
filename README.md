# 掐指一算

> **An Auditable Destiny & Personality Oracle**

**观星轨，察五行，循证据之线，照见性格深处的命纹。**

`掐指一算` 是一个面向智能体的八字 × 西方占星人格画像 Skill。它以八字为骨、星盘为镜，把外部能力计算出的命盘事实织成一部可追溯、可审计、有边界的性格秘典。

它不是排盘软件，也不把计算程序封装进 Skill。使用它的智能体会在运行时寻找并调用合格的外部计算能力；Skill 负责输入规范、方法校验、事实边界、推演许可、报告结构与最终审计。

## 发布通道：v0.6.0 Internal Test Product

v0.6.0 将 `audited_interpretive` 完整化为可内测的用户产品流程。普通用户只需提供出生信息；Skill 会发现并调用可用的计算/资格校验供应方。若没有合格供应方，流程会显式返回 `CAPABILITY_GAP`，不要求用户补交 facts JSON，也不让模型自由排盘。

供应方产生的 `deterministic-facts-v1` 与 `fact-qualification-v1` 是内部运行时接口。通过指纹绑定后，版本化的八字/占星传统解释规则才能产生可追溯信号和用户可读报告。

新路径不计算命盘，不从原始出生信息自行补齐事实，也不创建 PRIMARY_EVIDENCE、Mapping 或 Primitive 状态。结论必须回指信号 ID；信号又必须回指通过资格校验的事实和传统规则。

v0.5.0 的所有严格路径保持原样。`strict` 只在用户明确要求审计、研究或项目内规则确定性认证时使用，仍然在任一未满足的严格门停止。正式 Core 有限覆盖、Candidate Preview 和显式 56 章兼容长书继续互相隔离。

## 它能做什么

- 接受结构化出生资料或紧凑输入，例如：`2000.1.1.00:00 上海 未指定`
- 校验外部八字与西方占星计算能力的方法、版本与来源
- 严格区分命盘事实、传统解释和智能体推演
- 默认从合格事实生成 `standard-interpretive-v1` 审计式解释报告
- 在结论、信号、事实、规则、资格与指纹之间保留审计链
- 在出生时间缺失时移除时柱、宫位、上升点与角度结论，并显式降级
- 对无匹配规则的主题使用 `insufficient`，不用套话填补空白
- 在明确请求 `controlled_inference` 兼容路径时生成四部、56 章长书
- 在严格配置不完整时主动停止，不伪造确定性结论

## 一次占示如何发生

```text
出生输入
  ↓
范围与模式确认
  ↓
外部能力发现与方法校验
  ↓
八字 / 星盘事实归一化
  ↓
独立事实资格校验
  ↓
版本化传统解释规则与信号综合
  ↓
用户报告与审计元数据
```

默认画像使用 `audited_interpretive`：允许版本化传统规则解释经过资格校验的事实，但不允许运行时计算或补齐命盘事实、伪造规则或抬高保障等级。

如果运行环境没有合格的计算/资格校验供应方，流程在能力发现阶段返回 `CAPABILITY_GAP` 并停止。不用通用模型知识计算、修补或猜测命盘事实。

`strict` 是更严苛的确定性路径。只有完整的项目内查表、词表、边界规则、Primitive、Mapping 与叙事资产全部通过时，它才会开放；当前 Skill 会在缺失处如实停止。

## 安装

```bash
git clone https://github.com/pp-jok/qia-zhi-yi-suan.git
cp -R qia-zhi-yi-suan/destiny-personality ~/.codex/skills/
pip install ./qia-zhi-yi-suan
```

重新启动或刷新支持 Agent Skills 的运行环境后，即可通过 `$destiny-personality` 调用。

## 使用示例

```text
使用 $destiny-personality，根据以下资料生成完整命格人格书：
2000.1.1.00:00 上海 未指定
```

```text
使用 $destiny-personality，根据以下资料生成核心人格，不要长篇：
2000.1.1.00:00 上海 未指定
```

也可以请求其他模式：

```text
使用 $destiny-personality，只校验这份命盘事实，不进行人格推演。
```

```text
使用 $destiny-personality，审计这份已有的事实包和执行报告。
```

以下 CLI 是供应方/运行时的内部集成接口，不是普通用户输入：

```bash
destiny-personality-reference-validate build-interpretive-report FACTS.json \
  --qualification FACT_QUALIFICATION.json \
  --mode standard-interpretive-v1 \
  --output REPORT.json
```

## 审计式解释报告

发布契约：normal complete qualified charts: 7–12 meaningful sections; sparse evidence or missing birth time may produce fewer sections and must visibly state its scope。

`standard-interpretive-v1` 是默认模式，符合条件的普通完整命盘生成 7–12 个有意义的用户可读章节；证据稀疏或出生时间缺失时可以更短，但必须明确展示其适用范围与限制。当受支持主题超过 12 个时，第 12 节合并展示其余结论，并保留每条信号的 provenance 与局限，不静默截断。`concise-interpretive-v1` 是同一受控结论集的短版视图。公开报告入口只接受指纹绑定的 `QualifiedFacts`；调用方自行构造的 profile 或原始事实不能进入审计报告路径。CLI 仍接受 `standard` 和 `concise` 作为兼容别名，但持久化的 `report_mode` 始终使用带版本的正式名称。

置信标签不是科学准确率，而是对当前规则与证据范围的受控表达：

- `high`：来自多个体系或独立规则的支持，且没有反向信号。
- `moderate`：只有单个稳定体系/规则支持，结论必须保持有限语气。
- `exploratory`：存在反向证据或探索性信号，只作为反思线索。
- `insufficient`：请求的主题没有匹配规则，不形成人格结论。

追溯链为“报告结论/章节 → 信号 ID → 具体合格事实路径/传统规则”。每个章节的结构化 `signal_provenance` 保留信号所属体系、事实路径、规则引用与局限；报告审计元数据另保存事实指纹、资格指纹、规则包版本、`fact_mode` 与出生时间状态。内部 ID 不进入用户正文。

出生时间缺失时，运行时进入 `stable_only`：保留与时间无关的信号，省略时柱、上升点、MC、宫位、角度及其依赖结论，并在报告中增加限制说明。不得根据其他落点推测缺失的宫位或角度。

所有解释都来自版本化的传统八字/占星规则，不是实证心理学结论、人格诊断或行为预测，也不能代替专业意见或重大决策。

## 命书结构

长篇画像使用 `portrait-report-v2`、`long-form-personality-book-v2` 与 `reader-first-depth-v2`：

1. 封面与出生资料
2. 序章：提出贯穿全书的核心矛盾
3. 第一部：命盘本身在说什么（15 章）
4. 第二部：这些结构如何成为一个人（9 章）
5. 第三部：阴影、保护与命运底流（16 章）
6. 第四部：整合后的命格人格画像（16 章）
7. 终章：回收主原型与核心张力
8. 执行与审计附录

中文完整版以 11,000–15,000 个非空白正文字符作为深度校准。章节必须包含证据、形成机制、现实表现与整合意义中的至少三层；字数只是防止摘要化输出的警铃，不是制造填充文字的咒语。

## 五道门

相近的“自主性”主题被拆成五种不同的权利：

- **判断权**：在重要决定中拥有真实席位
- **表达权**：形成并说出自己能够负责的版本
- **选择与人生叙事权**：人生不完全由外部标准书写
- **解释权**：对自己的经历保有意义解释能力
- **社会署名权**：把私人方法转化为公开贡献

这五道门使用不同的事实、机制、场景与代价，避免整本命书反复讲述同一句“做自己”。

## 仓库结构

```text
destiny-personality/
├── SKILL.md            # 主流程与模式路由
├── agents/             # Skill 界面元数据
├── checklists/         # 阶段门、推演与报告验收
├── configs/            # 基础方法配置
├── examples/           # 非生产配置模板
├── references/         # 能力协议、失败策略与长篇蓝图
└── schemas/            # 输入、事实、推演与报告合同
candidates/core-profile-v1/
                        # 已批准的候选语义资产与校准策略
src/destiny_personality/
                        # 审计式解释、正式 Core、候选预览与校验器
src/destiny_personality/interpretive_assets/v1/
                        # wheel 内置的版本化传统解释规则
governance/             # 自治决策记录与审计绑定
docs/domain/             # 候选资产批准、校准与 Holdout 审计记录
pyproject.toml           # 最小 Python 安装元数据
```

发布包不包含二进制文件、固定外部供应商或用户命盘资料。公开的 synthetic 测试覆盖审计式解释、候选 IR 与映射边界；Python 模块不计算出生盘。

## 守夜人的规则

- 没有合格事实，不开启推演。
- 不把未知事实解释成负面状态。
- 不把传统解释伪装成科学结论。
- 不把两个体系的相似措辞自动视为相互证明。
- 不在正文讲述内部审批、来源编号和配置门；这些信息进入审计附录。
- 不用神秘语言掩盖方法缺口。

## 边界声明

本项目使用传统命理与占星符号进行受控、可审计的解释。输出不是科学诊断、心理诊断、医疗意见、法律意见、财务意见，也不保证行为、关系或未来事件必然发生。

所谓“阴影”指压力下可能出现的保护策略；所谓“命题”指可能反复面对的张力；所谓“原型”是整合文本的象征名称。它们不是病理标签，也不是不可逃离的宿命判决。

## License

[MIT](LICENSE) © 2026 pp-jok
