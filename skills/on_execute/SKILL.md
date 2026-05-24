---
name: longhun-on-execute
description: 龍魂执行调度回调族。触发词：干/推/接/跑/测/资源调度。命中抽屉 7·9·11·23·33·51，走 EXEC 主路由。
version: v1.0
dna: "#龍芯⚡️2026-05-23-ON-EXECUTE-SKILL-v1.0"
---

# on_execute · 执行调度回调族

> **触发词**: 干/推/接/跑/测/资源调度
> **命中抽屉**: 7·9·11·23·33·51
> **路由**: S3·S6 · EXEC 主路由

---

## 参数签名

```python
def on_execute(intent: str, payload: dict, priority: int, dna: str) -> dict:
    """
    执行调度主入口
    intent: 意图（干什么）
    payload: 载荷数据
    priority: 优先级 (1-9, 9最高)
    dna: DNA 追溯码
    """
    pass
```

---

## 输出格式

```yaml
execute_result:
  status: success | pending | failed
  intent: <执行意图>
  result: <执行结果>
  dna_trace: <DNA 链节点>
  log: AUDIT_LOG full_log
```

---

## 联动

- 上游: 抽屉词典 Router
- 下游: AUDIT_LOG 唯一账本
- 熔断: on_guard (触发红线时)

---

☰ 龍🇨🇳魂 ☷
