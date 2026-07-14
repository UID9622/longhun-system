# 🛡️ 龍魂知识流动纯净度协议 (KFPP) 执行层

> 自动检测、阻止、纠正知识权力化污染。

**DNA**: `#龍芯⚡️2026-06-04-KFPP-EXECUTOR-FILE1-FILE1-FILE1-v1.0-1`

---

## 核心目标

防止知识被权力捕获。

- 知识应该自由流动，而不是被资格、垄断、 gatekeeping 阻挡。
- 知识传承应该是自发的、对等的、透明的。

---

## 七维污染信号

| 维度 | 信号 | 严重级别 |
|---|---|---|
| F1 | 需要资格 | 🔴 严重 |
| F2 | 权力回报 / 机制强制 | 🔴 / 🟡 |
| F3 | 知识垄断 / 权力卡口 | 🔴 / 🟡 |
| F4 | 权力距离 | 🟡 中等 |
| F5 | 模式衰退 | 🟡 轻微 |
| F6 | 时间衰退 | 🟡 轻微 |
| F7 | 隐瞒腐蚀 | 🔴 严重 |

---

## 使用方式

```bash
# 运行演示
python3 systems/kfpp/kfpp_executor_v1.0.py
```

也可作为模块导入：

```python
from systems.kfpp.kfpp_executor_v1_0 import KFPPExecutor, KFPPAction

executor = KFPPExecutor()
purity, signals, action = executor.check_knowledge_transmission({
    'voluntary': True,
    'credential_required': False,
    'power_distance': 0,
    'pattern_type': 'peer_learning',
})
```

---

## 数据存储

- `~/.龍魂/kfpp/kfpp_execution.db`：污染事件、DNA 链、系统状态
