# 龍魂·第一道闸门 (longhun_gate)

> 数字根熔断 × DNA格式校验 × 三重检测 × 抽屉五行路由 × 五桶分拣

| 项 | 值 |
|----|----|
| 模块路径 | `03_engine/python/longhun_gate/` |
| 入口 | `gate_engine.decide(text, metadata=None, evidence="")` |
| DNA | `#龍芯⚡️2026-04-26-GATE-ENGINE-INTEGRATED-v1.0` |
| 主权 | UID9622 · 诸葛鑫 |

---

## 来源（一次复盘整合的产物·不是凭空写的）

| 资料 | 位置 |
|------|------|
| 整合方案·三大决策·七层架构 | [`01_protocols/cnsh/PROTOCOL__20260426__GATE-INTEGRATION-PLAN__v1.md`](../../../01_protocols/cnsh/PROTOCOL__20260426__GATE-INTEGRATION-PLAN__v1.md) |
| 55 抽屉 + 8 语义区登记表 | [`04_knowledge_base/wuxing/DRAWER_REGISTRY__v1.yaml`](../../../04_knowledge_base/wuxing/DRAWER_REGISTRY__v1.yaml) |
| Notion 主表 schema | [`05_notion_mirror/SCHEMA__GATE_SANDBOX_CORE__v1.md`](../../../05_notion_mirror/SCHEMA__GATE_SANDBOX_CORE__v1.md) |
| 5 份原始投喂存档 | [`05_archive/imports/feeds_2026-04-26/`](../../../05_archive/imports/feeds_2026-04-26/) |

---

## 用法

```python
from longhun_gate import decide

result = decide(
    "宝宝，帮我把这个Notion自动跑起来，带DNA追溯",
    metadata={"source": "cnsh-chrome-plugin", "operator": "UID9622"},
)
# {
#   "digital_root": 0,
#   "gate_color": "🟢",
#   "audit_color": "🟢",
#   "drawers": ["7-Hook触发", "11-落地执行", "2-DNA追溯", "55-人格调度"],
#   "elements": ["木", "木", "水", "火"],
#   "state": "S6_EXECUTE",
#   "route": "EXEC",
#   "engine": "Execution Engine",
#   "bucket": "📦 入库/封装",
#   "decision": "通过第一道闸门，进入沙盒分拣与后续流程。"
# }
```

跑一遍 demo（5 个测试用例）：

```bash
python3 03_engine/python/longhun_gate/gate_engine.py
```

---

## 与本地现有引擎的边界

| 现有 | 位置 | 与本模块关系 |
|------|------|-------------|
| `circuit_breaker.py` v3.0 | `bin/` | **复用**：红线/黄线/owner_vent 沿用现有 |
| `dna_append_log.py` v1.0 | `bin/` | **复用**：DNA 链 append-only 写入 |
| 本模块新增 | 本目录 | 数字根熔断 + DNA 格式校验 + 虚伪编译器 + 数据守护 + 抽屉五行路由 |

**不重复造轮子**：本引擎只补 Feed⑤ 独有的 4 项能力，红线检测 / DNA 链写入两条命脉继续走 `bin/` 现有实现。

---

## 不直接接主系统

按 Feed⑤ 原话："**应先在沙盒跑一周观察**"。

---

`DNA: #龍芯⚡️2026-04-26-LONGHUN-GATE-README-v1.0`
`确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
