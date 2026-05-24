# CNSH 龍魂流场决策总核 v4.1 · 工程包

**DNA:** `#龍芯⚡️2026-05-03-CNSH-FLOW-DECISION-CORE-v4.1-人格协作×IPA×DNA重铸增量`  
**CONFIRM:** `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`  
**SEAL:** `#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL`

## 包内结构

| 模块 | 职责 |
|------|------|
| `cnsh_flow_decision_core.py` | 主入口 `run_flow_decision(raw_input, tags)` |
| `schemas.py` | `FlowDecisionNode` **38** 字段 |
| `digital_root.py` | 四源数字根（explicit → dna 数字 → content hash → 原文数字 → 0 土） |
| `dna_tag_policy.py` | DNA 尾标签解析 + burn/seal 证明串 |
| `ipa_route_registry.py` | **11** 个 IPA 节点 + 统一回执 |
| `persona_collaboration.py` | 10 道闸主驻/辅驻静态表 + 铁律自检 |
| 其余 | 五行 / 三才 / 生克 / 九宫 / 沙盒桶 / 三色 |

## 运行测试

```bash
cd /Users/zuimeidedeyihan/longhun-system
python3 -m unittest discover -s cnsh/flow_decision/tests -p 'test_*.py' -v
```

## 调用示例

```python
from cnsh.flow_decision import run_flow_decision
from cnsh.flow_decision.cnsh_flow_decision_core import CONFIRM_REQUIRED, GPG_REQUIRED

r = run_flow_decision("你好", {"title": "t", "confirm_code": CONFIRM_REQUIRED, "gpg": GPG_REQUIRED})
print(r.node.field_count(), r.node.result_status, len(r.ipa_receipts))
```

## 与 IPA 路由镜像

本地登记见：`01_protocols/IPA-ROUTE-REGISTRY.local.md` 中 `[IPA-FLOW-DECISION-CORE-v4.1]` 行。

## 未完成 / 边界

- Notion / SQLite / JSONL **真实落盘**未接（仅字段与 `gate_trace` 就绪）。
- 500ms 节点超时（§2.2）未实现（同步单机版）。
- `known_parent_roots` 需由上层 DNA 登记处传入方可硬验父链存在性。
