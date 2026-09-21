# 08 Evaluation V2.2

## 1. 不比较文学标题

以下不作为硬指标：

- Signature 名称
- Dynamic 标题
- Archetype 名称

硬比较底层结构。

---

## 2. Primitive Similarity

分两层：

### Exact
按 Primitive ID。

### Ontology-Aware
允许 Relation Graph 的 adjacent/reinforcing 提供部分相似度。

建议：

```text
same = 1.0
adjacent = 0.5
reinforcing = 0.5
unrelated = 0
```

---

## 3. Dynamic Similarity

比较：

- dynamic_family
- pole primitive refs
- pole signature refs
- dynamic type

A/B 顺序允许交换。

---

## 4. Threshold Status

所有阈值必须标记：

```text
provisional
```

首版建议：

```text
Facts = 100%
Primitive exact+ontology >= 0.85
Signature structure >= 0.78
Core Dynamic structure >= 0.72
Dimension structure >= 0.78
Fate source dynamic >= 0.68
Archetype structure >= 0.68
```

这些不得被宣传成统计学准确度。

---

## 5. 阈值校准

流程：

```text
实现
→ 跑 Calibration Cases
→ 同模型重复
→ 跨模型重复
→ 人工审查
→ 再调整阈值
```

---

## 6. 模板坍塌

至少检查：

- Top 10 Primitive 频率；
- Top Dynamic Family 频率；
- Archetype structural pattern 频率。

若明显集中且命盘证据不足：
`FAIL_TEMPLATE_COLLAPSE`
