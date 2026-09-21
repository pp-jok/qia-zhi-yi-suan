# 01 Score Model V2.2

## 1. 四类指标彻底分离

### A. Trait Salience
回答：

> 某个人格倾向在某一体系内部有多强？

范围：
```text
0 none
1 secondary
2 moderate
3 strong
4 dominant
```

分别记录：

```json
{
  "bazi_salience": 3,
  "astrology_salience": 2
}
```

---

### B. Evidence Stability
回答：

> 这个判断受出生时间、边界、弱结构等影响多大？

```text
high
medium
low
unstable
```

---

### C. Cross-System Relation
回答：

> 两套体系之间是什么关系？

```text
validation
complement
contextualization
tension
correction
single_system
```

---

### D. Synthesis Priority
回答：

> 这个主题是否值得进入最终核心画像？

范围：
```text
0 ignore
1 secondary
2 notable
3 core
4 central
```

---

## 2. 禁止旧公式

废弃：

```text
primitive_salience =
max evidence
+ cross-system bonus
- contradiction penalty
```

原因：

- validation 不应该改变 trait 本身强弱；
- tension 不应该把两端同时扣低；
- cross-system relation 与 evidence strength 是不同概念。

---

## 3. Synthesis Priority 推荐规则

```text
priority = base_structural_importance
         + recurrence_bonus
         + cross_system_relevance
         + dynamic_explanatory_value
         - instability_penalty
```

注意：

`cross_system_relevance` 只影响 priority，不改变 bazi_salience / astrology_salience。

---

## 4. tension 的处理

若：

```text
A salience >= 3
B salience >= 3
relation = tension
```

则：

```text
A 保持原分
B 保持原分
Core Dynamic priority 上调
```

而不是互相扣分。

---

## 5. priority 进入 Core Dynamic 的最低要求

建议：

```text
priority >= 3
```

才进入核心动态候选。

`priority = 2` 只进入 secondary observation。
