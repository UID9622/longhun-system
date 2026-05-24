---
name: longhun-on-flow
description: 龍魂流程调度回调族。触发词：闭环/冲突/调度/回滚/上下文/优先级抢占。命中抽屉 24·49·50·52·53·54，走 FLOW 主路由。含 multisync。
version: v1.0
dna: "#龍芯⚡️2026-05-23-ON-FLOW-SKILL-v1.0"
---

# on_flow · 流程调度回调族

> **触发词**: 闭环/冲突/调度/回滚/上下文/优先级抢占
> **命中抽屉**: 24·49·50·52·53·54
> **路由**: S3·S7 · LOG
> **含旧 Skill**: multisync 多源同步

---

## 参数签名

```python
def on_flow(state_from: str, state_to: str, ctx: dict, retry: int) -> dict:
    """
    流程调度主入口
    state_from: 起始状态
    state_to: 目标状态
    ctx: 上下文
    retry: 重试次数
    """
    pass
```

---

## 流程状态机

```
INIT → RUNNING → PENDING → COMPLETE
         ↓          ↓
      FAILED ← ← ROLLBACK
```

---

## 输出格式

```yaml
flow_result:
  state_from: <起始>
  state_to: <目标>
  success: true | false
  retry_count: <重试次数>
  rollback: true | false
  dna_trace: <DNA>
  log: AUDIT_LOG log
```

---

## 联动

- 上游: 抽屉词典 Router
- 下游: AUDIT_LOG 唯一账本
- Notion 草日志: 唯一同步轴

---

☰ 龍🇨🇳魂 ☷
