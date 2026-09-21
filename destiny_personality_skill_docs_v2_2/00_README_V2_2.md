# 八字 × 西方占星核心画像 Skill V2.2
## Rule Freeze / 可编码规则冻结版

V2.2 是正式进入 Skill 开发前的方法决策收口版本。这表示已写明的方法
不得由智能体临场更改，不表示生产所需的所有规则资产已经齐全。

本项目的交付物是业务逻辑、执行编排与结果校验 Skill，不是内置排盘
软件。Skill 指导智能体在运行时调用合格的外部确定性计算能力，再将结果
归一化、校验后进入人格推理。第三方计算软件和项目 Python 参考验证器均
不是 Skill 运行依赖。完整边界见
`12_SKILL_EXECUTION_ARCHITECTURE_V2_2.md`。

交付状态：Phase B 的最小 Skill shell 已完成。Phase C 的能力描述、方法兼容
证据、调用信封、确定性事实、事实比对、预检、失败策略、执行报告和路由已于
2026-09-12 **complete and verified**。此状态只覆盖 Phase C 协议交付；本文不
声明 Gate 1 已通过或后续语义阶段已完成。

Gate 1A Primitive foundation contracts are implemented and verified on
2026-09-13. Gate 1 remains incomplete and Phase D remains incomplete because
real project-approved Primitive and other semantic assets are still absent.

Gate 1B Context-Aware Mapping Registry contracts are implemented and verified
on 2026-09-13. The real Mapping Registry values remain absent; Gate 1 remains
incomplete and Phase D remains incomplete.

Gate 1C Dimension Coverage Policy contract is implemented and verified on 2026-09-14.
The real dimension semantics and coverage thresholds remain absent; Gate 1 remains incomplete.

Gate 1D Narrative Rules and Semantic Contract Bundle are implemented and verified on 2026-09-14.
The real Narrative Rules remain absent; Gate 1 and downstream reasoning remain incomplete.

Canonical Fact Vocabulary contract is implemented and verified on 2026-09-14.
The production canonical vocabulary values remain absent. For the strict profile, CALCULATION_CONFIG_CHECKED remains closed. Exact lookup tables, the node rule, boundary margins, and comparison tolerances remain separate configuration gaps.

Calculation Config Framework contracts and aggregate validator are implemented and verified on 2026-09-14.
The production calculation values remain absent. For the strict profile, CALCULATION_CONFIG_CHECKED remains closed. Gate 1 remains incomplete, Phase D remains incomplete, and Phase E remains incomplete. The Skill still instructs the agent to invoke external deterministic capabilities; it does not bundle or start calculation software.

Controlled Inference business-test workflow is implemented and verified on 2026-09-14.
With a qualified external calculation capability, `portrait` may now generate an anchored, disclosed report under the controlled profile. This does not permit language-model chart calculation. Strict production remains blocked by project-owned assets.
The controlled report uses the long-form personality-book format: front matter, prologue, four parts, fifty-six chapter dimensions, finale, and audit appendix.
Each supported chapter must make at least three distinct analytical moves across evidence, mechanism, lived expression, and integration; repetition does not satisfy report depth.
User-approved reference interpretations may enrich controlled reports only as source-qualified supplemental interpretations; they do not override calculated facts, promote assurance, or satisfy strict gates.

本版本不再增加新的大模块，只完成五件事：

1. 将 Trait Salience、Evidence Stability、Cross-System Relation、Synthesis Priority 四者彻底拆开；
2. 将 Mapping Registry 升级为 Context-Aware Mapping；
3. 引入 Primitive Relation Graph；
4. 将 Primitive 的正式 wire state 定义为 supported_high / supported_low / mixed / unknown；
5. 冻结八字与西方占星方法配置，避免 Codex 临场替产品做方法选择。

完成 V2.2 后，领域方法停止自由扩展。交付架构以
`12_SKILL_EXECUTION_ARCHITECTURE_V2_2.md` 为准；发现产品规则缺口时仍应
停止并报告，不得由智能体自行补造。

---

## 核心推理链

```text
Birth Input
→ Time Normalization
→ Deterministic Chart Facts
→ Independent System Analysis
→ Context-Aware Primitive Mapping
→ Primitive State Resolution
→ Dominant Signatures
→ Primitive Relation Graph Activation
→ Core Dynamic Candidates
→ Core Dynamic Selection
→ 12-Dimension Coverage
→ Shadow / Mature Integration
→ Fate Tensions
→ Archetype
→ Narrative
```

其中 Time Normalization 与 Deterministic Chart Facts 由智能体调用外部能力
取得。Skill 负责规定调用条件、结果契约、校验门禁和后续推理流程。

---

## V2.2 的核心原则

### 1. 跨体系一致不能直接增强人格倾向本身
两套体系都指向某一人格倾向，只能提高该主题进入综合画像的优先级，不能把 Trait Salience 本身虚增。

### 2. 反向结构不能简单扣分
如果两股力量都强，应生成 tension，而不是互相抵消。

### 3. 八字与占星映射必须考虑上下文
禁止单纯使用：
`单一结构 → 固定人格结论`

### 4. 无证据不等于低
`unknown` 必须是合法状态。

### 5. Narrative 不参与核心评分
文学层只负责表达，不得影响 IR。

### 6. Skill 不内置确定性计算软件
Skill 只声明需要什么能力以及怎样验证结果。智能体负责实际调用；能力
缺失时停止并报告，不得猜算盘、静默安装软件或放宽方法规则。

### 7. 首个失败门决定结果
执行按 `CONFIG_GAP`、`CAPABILITY_GAP`、
`METHODOLOGY_VERSION_MISMATCH`、`CALCULATION_FATAL`、
`CALCULATION_CONTRACT_ERROR` 的阶段顺序分类；首个失败门一旦确定，就不再
评估后续门。无候选、授权被拒且无替代、或缺少强制独立候选属于能力缺口；
全部已发现候选均无 exact 证据或与冻结方法冲突属于方法版本不匹配；合格且
已授权的安全候选调用耗尽后才是计算失败；返回包违约属于契约错误，跨能力
冲突使用 `external_result_conflict` 子类型。远程授权只对本次执行有效。

当前精确查表、True North Node 规则、alias、boundary-distance margins 与
comparison tolerances 仍是 `CONFIG_GAP`，不得补造业务值。
