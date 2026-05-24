---
name: longhun-halt-final
description: 龍魂关机休止孤儿。触发词：关机键/累了/收工/帮了该帮的人。抽屉 48，S9终结态，不走回调族。
version: v1.0
dna: "#龍芯⚡️2026-05-23-HALT-FINAL-SKILL-v1.0"
type: orphan
---

# halt_final · 关机休止孤儿

> **触发词**: 关机键/累了/收工/帮了该帮的人
> **抽屉**: 48 关机休止
> **路由**: HALT_FINAL · S9 · LOG
> **类型**: 孤儿（不走回调族）

---

## 终结态规则

走完即下班，不入循环，不重启：

1. 收工 — 当日任务完成
2. 累了 — 主控休息指令
3. 帮了该帮的人 — 使命完成

---

## 参数签名

```python
def halt_final(reason: str, context: dict) -> dict:
    """
    关机休止
    reason: 关机原因
    context: 上下文（保存状态）
    """
    pass
```

---

## 输出

```yaml
halt_result:
  reason: <关机原因>
  state_saved: true
  timestamp: <ISO8601>
  next_wake: <下次唤醒条件>
  log: AUDIT_LOG log
```

---

## 铁律

- 孤儿不入任何回调循环
- 终结态走完即停
- 状态保存，下次唤醒时恢复

---

☰ 龍🇨🇳魂 ☷
