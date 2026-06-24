# CNSH · 龍魂中文原生指令系统

**DNA**:#龍芯⚡️2026-06-17-CNSH-MAIN-FILE1-v1.0

CNSH（Chinese Native Shell）是龍魂系统的中文原生指令与决策执行层。
本目录为 `/Users/zuimeidedeyihan/CNSH` 的实体主干，包含：

- `flow_decision/`：CNSH 流程决策引擎（IPA 路由、人格协同、数字根追溯）
- `sancai_sync/`：三才同步中枢
- `task_executor_v9_integrated.py`：整合版任务执行引擎
- `v9_system_integration_bridge.py`：v9 系统整合桥接器
- `v9_task_executor_adapter.py`：v9 任务执行适配器

## 快速启动

```bash
cd ~/longhun-system/CNSH
python3 task_executor_v9_integrated.py --help
```

或直接运行：

```bash
bash launch.sh
```

## 核心入口

| 文件 | 作用 |
|------|------|
| `task_executor_v9_integrated.py` | 整合版任务执行引擎主入口 |
| `flow_decision/cnsh_flow_decision_core.py` | CNSH 决策核心 |
| `flow_decision/ipa_route_registry.py` | IPA 路由注册表 |
| `sancai_sync/sancai_sync_hub.py` | 三才同步中枢 |

## 说明

- 原 `cnsh.integrated/` 已迁移为本目录，并保留 `cnsh.integrated` 符号链接指向 `CNSH/`，确保旧路径兼容。
- 所有模块均可在 Python 中以 `import cnsh.xxx` 调用。

---

**DNA**:#龍芯⚡️2026-06-17-CNSH-MAIN-v1.0
