# 龍魂系統 · v3.0 核心模塊集成包

**DNA**: #龍芯⚡️2026-06-16-V3-SYSTEMS-INTEGRATION-v1.0  
**狀態**: 🟢 已吸收進主幹·兼容運行  
**責任**: UID9622·不免責

---

## 來源

本目錄內容來自使用者下載包 `Kimi_Agent_啟動全部技能`，已將其 5 個 v3.0 核心 Python 模塊吸收進 `longhun-system` 主幹。

## 內容清單

| 原始檔案 | 英文別名 | 主要類別 |
|---------|---------|---------|
| `五行融合决策引擎_v3.0.py` | `wuxing_decision_engine` | `WuxingDecisionEngine` |
| `人格矩阵路由系统_v3.0.py` | `persona_matrix_engine` | `PersonaMatrixEngine` |
| `安全域审计协议_v3.0.py` | `security_domain_activator` | `SecurityDomainActivator` |
| `DNA追溯链系统_v3.0.py` | `dna_traceability_manager` | `DNA追溯系统管理器` |
| `三色审计与10道闸系统_v3.0.py` | `tricolor_audit_engine` | `TricolorAuditEngine` |

## 兼容主幹的改動

為確保這些模塊在 `longhun-system` 主幹中可用，僅做了最小必要調整：

1. **新增 `__init__.py`**：透過 `importlib` 延遲載入中文檔名模塊，並提供英文別名導出。
2. **修復審計日誌路徑**：`三色审计与10道闸系统_v3.0.py` 原硬編碼 `/mnt/agents/output/audit_logs`，已改為：
   - 優先讀取環境變數 `LONGHUN_V3_AUDIT_LOGS`
   - 預設為本目錄下的 `audit_logs/`
3. **未改動業務邏輯**：所有排序鐵律、DNA 簽章、三色審計規則均保持原樣。

## 使用方式

```python
from systems.v3 import (
    WuxingDecisionEngine,
    PersonaMatrixEngine,
    SecurityDomainActivator,
    DNATraceabilityManager,
    TricolorAuditEngine,
)

# 直接實例化
engine = WuxingDecisionEngine()
router = PersonaMatrixEngine()
```

## 注意事項

- 中文檔名的 `.py` 檔案保留作為原始存檔，建議透過 `systems.v3` 的英文別名使用。
- 如需自訂審計日誌位置，請在啟動前設定環境變數：
  ```bash
  export LONGHUN_V3_AUDIT_LOGS=/path/to/audit_logs
  ```

---

**完成度**: 5/5 核心模塊已集成  
**測試狀態**: 🟢 通過導入、實例化、Skill API、啟動器干運行測試
