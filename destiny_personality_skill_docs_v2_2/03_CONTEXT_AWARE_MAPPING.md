# 03 Context-Aware Mapping

## 1. 目的

八字与占星都不是“单结构单含义”的简单词典。

V2.2 规定：

> Mapping Rule 可以有 Primary Signal，但人格解释必须允许 Context / Modifier 改写表现形式。

---

## 2. 八字规则结构

```yaml
- rule_id: BZ_R100
  source_system: bazi
  primary_condition:
    feature: resource_star_strength
    operator: ">="
    value: strong

  context:
    all:
      - day_master_strength: strong
      - season_support: true

  outputs:
    - primitive_id: P009
      direction: increase
      salience: 3
    - primitive_id: P007
      direction: increase
      salience: 2

  modifiers:
    - when:
        output_star_strength: strong
      effects:
        - expression_mode: externalized

  limitations:
    - "不得单独推出高智力"
    - "不得忽略身强弱和月令"
```

---

## 3. 占星规则结构

```yaml
- rule_id: AST_R120
  source_system: astrology
  primary_condition:
    feature: mercury_sign
    operator: "=="
    value: Gemini

  outputs:
    - primitive_id: P008
      direction: increase
      salience: 3
    - primitive_id: P019
      direction: increase
      salience: 2

  contextualizers:
    - when:
        aspect:
          body_a: Mercury
          body_b: Saturn
          type: opposition
          max_orb: 3.0
      effects:
        - primitive_id: P013
          direction: increase
        - interpretation_mode: "fast_generation_with_internal_audit"
```

---

## 4. 规则优先级

```text
Methodology Rule
> Context-Aware Mapping
> Interaction Rule
> Primitive Relation Graph
> LLM synthesis
```

LLM 不得覆盖上层规则。

---

## 5. Interaction Rule

允许显式定义组合结构：

```yaml
- interaction_id: AST_I001
  requires:
    - AST_R120
    - AST_R144
  produces:
    signature_hint: "fast_generation_with_internal_audit"
```

八字同样允许 interaction rule。

---

## 6. 映射输出必须保留两套体系隔离

```json
{
  "bazi_primitive_candidates": [],
  "astrology_primitive_candidates": []
}
```

Cross-System Synthesizer 之后才允许对齐。
