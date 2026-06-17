# CNSH · 龍魂中文原生指令系統

**DNA**: #龍芯⚡️2026-06-17-CNSH-MAIN-v1.0

CNSH（Chinese Native Shell）是龍魂系統的中文原生指令與決策執行層。
本目錄為 `/Users/zuimeidedeyihan/CNSH` 的實體主幹，包含：

- `flow_decision/`：CNSH 流程決策引擎（IPA 路由、人格協同、數字根追溯）
- `sancai_sync/`：三才同步中樞
- `task_executor_v9_integrated.py`：整合版任務執行引擎
- `v9_system_integration_bridge.py`：v9 系統整合橋接器
- `v9_task_executor_adapter.py`：v9 任務執行適配器

## 快速啟動

```bash
cd ~/longhun-system/CNSH
python3 task_executor_v9_integrated.py --help
```

或直接運行：

```bash
bash launch.sh
```

## 核心入口

| 文件 | 作用 |
|------|------|
| `task_executor_v9_integrated.py` | 整合版任務執行引擎主入口 |
| `flow_decision/cnsh_flow_decision_core.py` | CNSH 決策核心 |
| `flow_decision/ipa_route_registry.py` | IPA 路由註冊表 |
| `sancai_sync/sancai_sync_hub.py` | 三才同步中樞 |

## 說明

- 原 `cnsh.integrated/` 已遷移為本目錄，並保留 `cnsh.integrated` 符號鏈接指向 `CNSH/`，確保舊路徑兼容。
- 所有模塊均可在 Python 中以 `import cnsh.xxx` 調用。

---

**DNA**: #龍芯⚡️2026-06-17-CNSH-MAIN-v1.0
