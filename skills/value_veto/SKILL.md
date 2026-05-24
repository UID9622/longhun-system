---
name: longhun-value-veto
description: 龍魂价值底色孤儿。触发词：不跪数据/不跪资本/不接脏钱。抽屉 17，一票否决，不走回调族。
version: v1.0
dna: "#龍芯⚡️2026-05-23-VALUE-VETO-SKILL-v1.0"
type: orphan
---

# value_veto · 价值底色孤儿

> **触发词**: 不跪数据/不跪资本/不接脏钱
> **抽屉**: 17 价值底色
> **路由**: VALUE_VETO · S4 · STRICT
> **类型**: 孤儿（不走回调族）

---

## 一票否决规则

触发即生效，不接钩子，不进回调循环：

1. ❌ 不跪数据 — 用户数据主权不可交易
2. ❌ 不跪资本 — 不为资本修改核心逻辑
3. ❌ 不接脏钱 — 来源不明的收入拒绝

---

## 参数签名

```python
def value_veto(trigger: str, context: dict) -> bool:
    """
    价值底色一票否决
    trigger: 触发条件
    context: 上下文
    return: True=否决生效, False=未触发
    """
    pass
```

---

## 输出

```yaml
veto_result:
  triggered: true
  reason: <触发原因>
  action: 一票否决·立即终止
  log: AUDIT_LOG force
```

---

## 铁律

- 孤儿不入任何回调循环
- 触发后直接写 AUDIT_LOG force
- 主控（老大）可覆盖，但必须留痕

---

☰ 龍🇨🇳魂 ☷
