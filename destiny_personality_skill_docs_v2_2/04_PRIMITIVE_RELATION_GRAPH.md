# 04 Primitive Relation Graph

## 1. 目的

Core Dynamic 不应完全依赖 LLM 自由发现“哪些词有张力”。

系统应提供一张可版本化的 Primitive Relation Graph，作为候选动态生成器。

---

## 2. 关系类型

```text
reinforcing
adjacent
complementary
potential_tension
contextualizing
independent
```

---

## 3. 示例

```yaml
relations:
  - left: P024
    right: P022
    relation: potential_tension
    dynamic_family: stability_freedom

  - left: P001
    right: P044
    relation: reinforcing

  - left: P041
    right: P027
    relation: potential_tension
    dynamic_family: ideal_reality

  - left: P013
    right: P019
    relation: potential_tension
    dynamic_family: validation_possibility
```

---

## 4. 激活条件

关系图本身不会自动形成 Core Dynamic。

只有当：

```text
左侧 state != unknown
右侧 state != unknown
且双方至少 moderate
```

才进入 Dynamic Candidate。

---

## 5. Dynamic Candidate Score

建议：

```text
candidate_priority =
max(left_salience, right_salience)
+ relation_importance
+ recurrence
+ explanatory_coverage
- instability
```

---

## 6. 关系图也服务 Evaluation

Ontology-aware similarity：

```text
same primitive = 1.0
adjacent = 0.5
reinforcing = 0.5
independent = 0
potential_tension = 不作为“相似”，而作为关系结构比较
```

这样比纯 ID Jaccard 更合理。
