# 05 Core Dynamic Selection V2.2

## 1. 候选来源

Core Dynamic Candidate 必须来自：

1. Primitive Relation Graph 激活；
2. Dominant Signature 之间的明确张力；
3. Context-Aware Interaction Rule；
4. Cross-System Synthesizer 识别出的高价值 tension / contextualization。

不得由 Narrative Renderer 生成。

---

## 2. 成为 Core Dynamic 的最低条件

候选至少满足以下 5 条中的 2 条：

- 至少一侧有 salience >= 3；
- 两侧都有 salience >= 2；
- 双体系均涉及该主题；
- 可解释至少 2 个 Coverage Dimensions；
- 可派生可区分的 Shadow / Mature Pattern。

若不满足：

进入 secondary observation。

---

## 3. Dynamic 结构

```json
{
  "dynamic_id": "CD01",
  "family": "stability_freedom",
  "type": "tension",
  "priority": 4,
  "pole_a": {
    "label": "稳定",
    "primitive_refs": ["P024", "P026"],
    "signature_refs": ["S04"]
  },
  "pole_b": {
    "label": "自由",
    "primitive_refs": ["P001", "P022"],
    "signature_refs": ["S02"]
  },
  "cross_system_relation": "tension",
  "contextualizers": [],
  "shadow_form": "",
  "mature_form": ""
}
```

---

## 4. Dynamic 去重

同 family 默认只保留一个主 Dynamic。

若两个候选：
- primitive overlap > 70%
或
- source signatures overlap > 70%

则合并。

---

## 5. LLM 的职责

LLM 可以：

- 给 Dynamic 命名；
- 解释两端如何共存；
- 生成 shadow / mature 表述。

LLM 不可以：

- 自行新增 pole；
- 自行提升 priority；
- 绕过 relation graph 和 selection rules。
