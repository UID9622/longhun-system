# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂系统 · v3.0 核心模块集成包

**DNA**:#龍芯⚡️2026-06-16-V3-SYSTEMS-INTEGRATION-FILE1-v1.0  
**状态**: 🟢 已吸收进主干·兼容运行  
**责任**: UID9622·不免责

---

## 来源

本目录内容来自使用者下载包 `Kimi_Agent_启动全部技能`，已将其 5 个 v3.0 核心 Python 模块吸收进 `longhun-system` 主干。

## 内容清单

| 原始档案 | 英文别名 | 主要类别 |
|---------|---------|---------|
| `五行融合决策引擎_v3.0.py` | `wuxing_decision_engine` | `WuxingDecisionEngine` |
| `人格矩阵路由系统_v3.0.py` | `persona_matrix_engine` | `PersonaMatrixEngine` |
| `安全域审计协议_v3.0.py` | `security_domain_activator` | `SecurityDomainActivator` |
| `DNA追溯链系统_v3.0.py` | `dna_traceability_manager` | `DNA追溯系统管理器` |
| `三色审计与10道闸系统_v3.0.py` | `tricolor_audit_engine` | `TricolorAuditEngine` |

## 兼容主干的改动

为确保这些模块在 `longhun-system` 主干中可用，仅做了最小必要调整：

1. **新增 `__init__.py`**：透过 `importlib` 延迟载入中文档名模块，并提供英文别名导出。
2. **修复审计日志路径**：`三色审计与10道闸系统_v3.0.py` 原硬编码 `/mnt/agents/output/audit_logs`，已改为：
   - 优先读取环境变数 `LONGHUN_V3_AUDIT_LOGS`
   - 预设为本目录下的 `audit_logs/`
3. **未改动业务逻辑**：所有排序铁律、DNA 签章、三色审计规则均保持原样。

## 使用方式

```python
from systems.v3 import (
    WuxingDecisionEngine,
    PersonaMatrixEngine,
    SecurityDomainActivator,
    DNATraceabilityManager,
    TricolorAuditEngine,
)

# 直接实例化
engine = WuxingDecisionEngine()
router = PersonaMatrixEngine()
```

## 注意事项

- 中文档名的 `.py` 档案保留作为原始存档，建议透过 `systems.v3` 的英文别名使用。
- 如需自订审计日志位置，请在启动前设定环境变数：
  ```bash
  export LONGHUN_V3_AUDIT_LOGS=/path/to/audit_logs
  ```

---

**完成度**: 5/5 核心模块已集成  
**测试状态**: 🟢 通过导入、实例化、Skill API、启动器干运行测试
