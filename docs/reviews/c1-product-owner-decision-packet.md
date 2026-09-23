# C1 Product Owner Decision Packet

Status: **C1 APPROVED** on 2026-09-22. This packet preserves the pre-approval rationale; the Product Owner selected D1 Option A, D2 Option A, D3 Option A, and D4 Multi-Context Promotion. Approval is limited to Primitive Ontology v2 Candidate Implementation and does not authorize C2 mapping work or runtime activation.

## D1 — P001 / P004

P001 — 自主判断与自我主导。定义：判断依据主要来自自身标准还是外部框架。问题：如何形成判断？包括自主判断/外部指导；排除行动速度、反叛、变化偏好。P004 — 行动启动与推进方式。定义：如何启动并推进具体行动。问题：何时开始行动？包括启动/观察准备；排除判断所有权、冲动和成就。

冲突：主动做决定可能被同时读成自主判断与行动启动，导致 Mapping duplication、double counting、状态夸大，并在未来 Signature/Dynamic/Renderer 中塌缩。

| Semantic unit | P001 | P004 | Conflict |
|---|---|---|---|
| 判断标准归属 | primary | exclude | 当前易被“主动”混淆 |
| 行动开始时机 | exclude | primary | 当前易被“自主”混淆 |
| 执行推进 | exclude | primary | 需要 Mapping 明确事实条件 |

Option A：P001 只拥有判断标准，P004 只拥有启动/推进；共享“主动”证据只能按事实指向一个 owner。迁移低，最利于 Signature 正交。Option B：P001 拥有自主决策，P004 拥有执行节律，但允许同一事实双映射并标注 modifier；迁移中，double counting 风险高。

正交检验：P001 高/P004 低（自主但审慎等待）成立；P001 低/P004 高（按外部目标迅速执行）成立。

Engineering recommendation：Option A。理由：可机械分离“为什么/依据谁判断”与“何时行动”。风险：需 C2 精确审计现有事实条件。置信度：high。

## D2 — P002 / P006

P002 — 稳定感与可预期需求。定义：对稳定、明确和可预期的偏好。问题：需要多少确定性？包括稳定/开放变化；排除组织能力、责任。P006 — 结构化与组织取向。定义：以多少预设结构组织任务。问题：如何安排活动？包括秩序/弹性；排除安全感和价值判断。

冲突：规则、计划和秩序可同时被读为“需要稳定”及“善于组织”。

| Semantic unit | P002 | P006 | Conflict |
|---|---|---|---|
| 对不确定性的偏好 | primary | exclude | 稳定需求与计划表象混同 |
| 任务组织方法 | exclude | primary | 结构方法与安全感混同 |

Option A：P002 拥有可预期需求，P006 拥有组织方法；工作结构证据不得自动证明全局稳定需求。Option B：P002 包含稳定规则偏好，P006 只保留工作流程结构；迁移中且上下文泄漏风险高。

正交检验：P002 高/P006 低（需要确定性但组织松散）成立；P002 低/P006 高（愿意变化但工作有序）成立。

Engineering recommendation：Option A。理由：偏好与方法是可独立变化的轴。风险：需定义边缘事实的 evidence ownership。置信度：high。

## D3 — P003 / P001

P003 — 关系互动中的感受与回应。定义：关系中对感受、回应和协调的优先度。问题：如何处理关系互动？包括回应协调/独立处理；排除自主判断、社交量。P001 如 D1。

冲突：独立处理关系可能被误读为低关系回应和高自主判断。

| Semantic unit | P003 | P001 | Conflict |
|---|---|---|---|
| 关系回应优先度 | primary | exclude | 独立不等于自主判断 |
| 判断标准归属 | exclude | primary | 关系协调不等于放弃判断 |

Option A：P003 只拥有关系回应，P001 只拥有判断归属；关系事实默认不提升全局自主。Option B：关系独立同时作为 P003 low 与 P001 high；迁移低但会重复拥有“独立”。

正交检验：P003 高/P001 高（重视回应且自主判断）成立；P003 低/P001 低（低回应且借外部框架判断）成立。

Engineering recommendation：Option A。理由：保护关系语义不吞没全局判断。风险：需明确何种跨情境证据才可支持 P001。置信度：high。

## D4 — Local → Global Promotion

Option A — Strict Global Evidence：只有明确 global evidence 可形成 global state；安全但大量结论停留局部。Option B — Multi-Context Promotion：明确 global evidence，或两个独立代表 context 同方向、达到资格且无 material counter-context，才形成 global candidate。Option C — Weighted Aggregation：按代表性、覆盖与权重阈值聚合；表达力高但需未经批准的数值模型。

Material counter-context：独立来源的有效反方向证据，位于代表性 context，具有重复性或足以改变该轴解释的事实 assurance；不是单次弱修饰、缺失或不可用时敏感事实。禁止多数投票。work high / relationship low 默认是 contextual variation，不是 global mixed；只有真正 global scope 的相反有效证据才可 global mixed。

Engineering recommendation：Option B。理由：保留局部性又允许经跨情境证明的全局候选，且无需提前定义权重。风险：代表性与最低资格仍须 C2/C1 后续批准。置信度：medium.

## Impact Matrix

| Decision | Recommended | Ontology | Mapping | Signature/Dynamic | Migration risk |
|---|---|---|---|---|---|
| D1 | A | clarify ownership | split decision/action facts | improves orthogonality | low |
| D2 | A | clarify preference/method | block structural-to-stability lift | reduces collapse | low |
| D3 | A | isolate relational response | block relationship-to-global autonomy lift | preserves contextuality | low |
| D4 | B | add promotion protocol | mark scope/qualification | prevents false global dynamics | medium |

## Product Owner Decision Sheet

```text
D1 P001/P004: [x] Option A  [ ] Option B
Decision: APPROVED — Option A. Reason: judgement ownership and action initiation have distinct primary semantic ownership.

D2 P002/P006: [x] Option A  [ ] Option B
Decision: APPROVED — Option A. Reason: predictability preference and organizational method must remain independently resolvable.

D3 P003/P001: [x] Option A  [ ] Option B
Decision: APPROVED — Option A. Reason: relational responsiveness and judgement ownership must not infer one another.

D4 Local → Global: [ ] Strict Global Evidence  [x] Multi-Context Promotion  [ ] Weighted Aggregation
Decision: APPROVED — Multi-Context Promotion. Reason: explicit global evidence or independently rooted, same-direction evidence in representative contexts may create a global candidate only.
```
