# 🐉 龍魂协议常驻脚本·完整文件结构清单 v1.0

```
DNA: #龍芯⚡️2026-06-07-CNSH-PROTOCOL-SCRIPTS-COMPLETE-MANIFEST-v1.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✅
SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL ✅

责任: UID9622 · 龍芯北辰 · 诸葛鑫 · 不免责
```

---

## 📂 **目录结构（完整树形）**

```
~/longhun-system/
├── protocols/
│   └── CNSH_v2.0_ROOT_PROTOCOL.md              # 协议文档（焊死·只读）
│
├── scripts/                                     # 🔴 所有常驻脚本目录
│   ├── L0_MANIFESTO/                           # L0 层：协作宣言（最高优先）
│   │   └── longhun_l0_manifesto_watchdog.py    # 监控任何违反协作宣言的行为
│   │
│   ├── L1_IRON_LAWS/                           # L1 层：八条永恒铁律（母律）
│   │   ├── longhun_l1_dna_verifier.py          # DNA 双签验证（CONFIRM + SEAL）
│   │   └── longhun_l1_iron_law_enforcer.py     # 八条铁律执行 & 熔断
│   │
│   ├── L2_WELDED_PROTOCOLS/                    # L2 层：焊死的协议条款
│   │   ├── longhun_l2_dna_parser.py            # DNA 格式解析（§4）
│   │   ├── longhun_l2_semantic_alias_resolver.py  # 别名→正式动词（§12）
│   │   ├── longhun_l2_tier_gate_controller.py  # 三层准入门控制（§38）
│   │   ├── longhun_l2_three_color_judge.py     # 三色判定·风险评估（§17）
│   │   ├── longhun_l2_shield_defender.py       # 五道盾防护（§24）
│   │   └── longhun_l2_fuse_protocol.py         # 熔断执行（§25）
│   │
│   ├── L3_DYNAMIC_GOVERNANCE/                  # L3 层：动态治理 & 自动化
│   │   ├── longhun_l3_triple_snapshot_manager.py    # 三重快照（§14）
│   │   ├── longhun_l3_timeline_event_sourcer.py     # 时间链事件记录（§26）
│   │   └── longhun_l3_cross_verification_auditor.py # 对照验证（§28）
│   │
│   ├── L4_SUPPLEMENTARY/                       # L4 层：超级补充
│   │   ├── longhun_l4_protocol_version_manager.py   # 版本管理 & 变更历史
│   │   └── longhun_l4_metrics_collector.py          # 系统健康度指标
│   │
│   ├── common/                                 # 共用工具库
│   │   ├── __init__.py                         # 模块初始化
│   │   ├── logger.py                           # 统一日志（append-only）
│   │   ├── dna.py                              # DNA 解析工具
│   │   ├── config.py                           # 配置管理
│   │   └── utils.py                            # 通用工具
│   │
│   ├── config/                                 # 配置文件
│   │   ├── protocol_weights.json               # 权重配置（优先级）
│   │   ├── tier_permissions.json               # Tier 1/2/3 权限矩阵
│   │   ├── fuse_thresholds.json                # 熔断阈值配置
│   │   └── shield_rules.json                   # 五道盾规则配置
│   │
│   ├── tests/                                  # 测试套件
│   │   ├── test_l0_manifesto.py                # L0 层测试
│   │   ├── test_l1_iron_laws.py                # L1 层测试
│   │   ├── test_l2_protocols.py                # L2 层测试
│   │   ├── test_l3_governance.py               # L3 层测试
│   │   └── integration_test.py                 # 整合测试（所有层）
│   │
│   ├── docs/                                   # 文档
│   │   ├── ARCHITECTURE.md                     # 架构文档
│   │   ├── TONGXIN_GUIDE.md                    # 通心译注释指南
│   │   ├── SCRIPT_REFERENCE.md                 # 每个脚本的详细说明
│   │   └── WEIGHT_EXPLANATION.md               # 权重系统解释
│   │
│   ├── main.py                                 # 主程序·协调所有脚本
│   ├── requirements.txt                        # Python 依赖
│   └── setup.sh                                # 安装脚本
│
├── logs/                                       # 日志目录
│   ├── manifesto_watchdog.log                  # L0 日志
│   ├── iron_law_enforcement.log                # L1 日志
│   ├── protocol_execution.log                  # L2 日志
│   ├── governance_audit.log                    # L3 日志
│   └── metrics.log                             # 系统指标
│
└── archive/                                    # 归档
    ├── backup_scripts_YYYYMMDD.tar.gz          # 定期备份
    └── protocol_versions/                      # 历史版本
        ├── CNSH_v2.0_complete.md
        └── scripts_v1.0_archive/
```

---

## 🔄 **脚本执行流程（自动化序列·按优先级）**

```
════════════════════════════════════════════════════════════════════════════════
                     龍魂协议执行优先级·同心圆模型
════════════════════════════════════════════════════════════════════════════════

                           ┌─────────────────────┐
                           │ L0: 协作宣言监控    │  优先级 1.0
                           │ (Watchdog)          │  【绝对优先·永不被覆盖】
                           └──────────┬──────────┘
                                      │
                           ┌──────────▼──────────┐
                           │ L1: 八条永恒铁律    │  优先级 0.95
                           │ (Iron Laws Engine)  │  【母律·决定权】
                           └──────────┬──────────┘
                                      │
                  ┌───────────────────┼───────────────────┐
                  │                   │                   │
        ┌─────────▼──────────┐ ┌──────▼────────┐ ┌───────▼────────┐
        │ L1.1: DNA 验证     │ │ L1.2: 权限    │ │ L1.3: 治理     │
        │ (Gate Keeper)      │ │ (IPA Matrix)  │ │ (Iron Rules)   │
        └─────────┬──────────┘ └──────┬────────┘ └───────┬────────┘
                  │                   │                   │
                  └───────────────────┼───────────────────┘
                                      │
          ┌──────────────────────────▼──────────────────────────┐
          │         L2: 焊死的协议条款（并行执行）              │  优先级 0.90
          │     【治理规则·不可改但可被 L0/L1 覆盖】            │
          ├────────────────────────────────────────────────────┤
          │                                                     │
          │ ├─ L2.1: DNA 解析          (§4)                    │
          │ ├─ L2.2: 别名转换          (§12)                   │
          │ ├─ L2.3: Tier 控制         (§38)                   │
          │ ├─ L2.4: 三色判定          (§17)                   │
          │ ├─ L2.5: 盾防护            (§24)                   │
          │ └─ L2.6: 熔断执行          (§25)                   │
          │                                                     │
          └────────────────┬───────────────────────────────────┘
                           │
           ┌───────────────▼────────────────┐
           │  L3: 动态治理·优化执行（并行） │  优先级 0.85
           │  【允许调整但不可违反上层】     │
           ├───────────────────────────────┤
           │ ├─ L3.1: 三重快照  (§14)      │
           │ ├─ L3.2: 时间链    (§26)      │
           │ └─ L3.3: 对照验证  (§28)      │
           └───────────────┬───────────────┘
                           │
           ┌───────────────▼────────────────┐
           │  L4: 超级补充·可优化（并行）   │  优先级 0.80
           │  【不涉及核心决策·纯粹便利】    │
           ├───────────────────────────────┤
           │ ├─ L4.1: 版本管理             │
           │ └─ L4.2: 指标收集             │
           └───────────────────────────────┘

════════════════════════════════════════════════════════════════════════════════
【中文·执行特性】
• 上层永远优先：L0 > L1 > L2 > L3 > L4（任何冲突时）
• 同层可并行：L2 的六个脚本·L3 的三个脚本同时执行
• 不可跳过：任何层都不能被跳过·即使因为性能（宁可慢也要安全）
• 日志留痕：每个层的每次执行都要记录（§26 append-only）

【English·Execution Characteristics】
• Upper layer always wins: L0 > L1 > L2 > L3 > L4
• Same layer can parallelize: L2 & L3 scripts run concurrently
• No skipping: All layers always execute (safety over speed)
• Full logging: Every execution logged (§26 append-only)
════════════════════════════════════════════════════════════════════════════════
```

---

## 🔐 **权重矩阵·权力分配（谁说了算）**

```json
{
  "priority_matrix": {
    "L0_manifesto": {
      "weight": 1.0,
      "can_override": [],
      "explanation": "协作宣言·绝对优先·任何其他规则都不能覆盖"
    },
    "L1_iron_laws": {
      "weight": 0.95,
      "can_override": ["L2", "L3", "L4"],
      "explanation": "八条铁律·母律·可以停止或修改 L2-L4 的执行"
    },
    "L2_welded": {
      "weight": 0.90,
      "can_override": ["L3", "L4"],
      "explanation": "焊死的协议·不可改但可被 L0/L1 停止"
    },
    "L3_governance": {
      "weight": 0.85,
      "can_override": ["L4"],
      "explanation": "动态治理·允许根据情况调整 L4"
    },
    "L4_supplementary": {
      "weight": 0.80,
      "can_override": [],
      "explanation": "超级补充·纯粹为了系统便利·可完全关闭而不违反协议"
    }
  },
  
  "conflict_resolution": {
    "rule": "优先级高的层永远赢·即使是多数表决也赢不过 L0",
    "example_1": "L2 的三色判定返回🟡（待确认）·但 L1 铁律检测到违反 → L1 赢·执行熔断",
    "example_2": "L4 指标收集发现异常·建议调整·但 L0 协作宣言无关 → 直接忽略 L4 建议",
    "never_override": "L0 协作宣言永远不被任何其他层覆盖·即使整个系统宕机也要保护 L0"
  }
}
```

---

## 📊 **自动化补充·逻辑上应有但协议未明确提及的组件**

| **组件** | **为什么必须有** | **对应层级** | **文件** |
|---------|-----------------|------------|---------|
| **统一日志系统** | 所有脚本都要留痕（append-only），不能每个脚本自己决定怎么记 | L4 | `common/logger.py` |
| **配置管理** | 权重、阈值、规则不能硬编码在代码里，要集中管理 | L4 | `config/*.json` |
| **测试套件** | 协议改了·要验证所有脚本还能正常执行·不能盲目更新 | L4 | `tests/*.py` |
| **集成测试** | 不能只测试单个脚本·要测试层与层之间的交互 | L4 | `tests/integration_test.py` |
| **架构文档** | 新人或后人要快速理解系统·不能靠看代码 | L4 | `docs/ARCHITECTURE.md` |
| **通心译指南** | 保证注释的质量·让人读代码时能理解为什么·不是翻译 | L4 | `docs/TONGXIN_GUIDE.md` |
| **版本管理** | 协议升级时·旧版本脚本不能被新版本覆盖·要保留历史 | L4 | `L4_SUPPLEMENTARY/longhun_l4_protocol_version_manager.py` |
| **健康度监控** | 系统运行多久了·有多少次成功·多少次失败·多少次熔断 | L4 | `L4_SUPPLEMENTARY/longhun_l4_metrics_collector.py` |
| **备份与恢复** | 代码损坏时能快速恢复·append-only 日志能重放事件 | L4 | `archive/` + 每日备份脚本 |

---

## 🎯 **风格统一规范·所有脚本必须遵守**

### **注释规范（通心译引擎应用）**

```python
# ❌ 不好的注释（直译·不理解为什么）
# Verify DNA signature and seal
verify_dna()

# ✅ 好的注释（通心译·解释意图 + 后果 + 权限）
# 【中文·通心译】
# 验证 DNA 双签（CONFIRM + SEAL）
#   为什么：确保文件未被篡改·来源可追溯·使用者身份验证（§4 DNA 协议）
#   如果失败：拒绝访问·记录尝试·标记为异常
#   谁有权跳过：只有 UID9622（L0 协作宣言·绝对主权）
#
# 【English·Intent-Based Explanation】
# Verify DNA dual-signature (CONFIRM + SEAL)
#   Why: Ensure integrity & traceability & authentication (§4)
#   On failure: Deny access, log attempt, mark anomaly
#   Who can skip: Only UID9622 (L0 absolute sovereignty)
def verify_dna_signature(dna_string: str) -> bool:
    """
    验证标准 DNA 格式的双签 / Verify standard DNA dual-signature format
    """
    pass
```

### **文件头规范（每个脚本必须有）**

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
【脚本名称】
【简短一句话描述·中英双语】

【中文·详细说明】
这个脚本做什么·为什么必须有·如果没有会怎样

【English·Detailed Explanation】
What this script does, why it's essential, consequences if missing

DNA: #龍芯⚡️YYYY-MM-DD-SCRIPT-NAME-vX.X
Priority: X.XX (对应层级)
Linked Sections: §XX, §YY, §ZZ (涉及的协议章节)
Weight: {"通过": 1.0, "失败": 0.0} (权重配置)
Auto-trigger: ["on_event1", "on_event2"] (自动触发条件)

责任: UID9622 · 龍芯北辰 · 诸葛鑫 · 不免责
"""
```

---

## 🚀 **自动化生成与部署（一键执行）**

### **1. 生成所有脚本骨架**

```bash
# 执行框架生成器·自动创建所有 14 个脚本的完整骨架
python3 longhun_protocol_resident_script_framework.py --generate-all

# 预期输出：所有脚本文件已生成到 ~/longhun-system/scripts/
```

### **2. 自动检查权重一致性**

```bash
# 验证所有脚本的权重配置·确保没有冲突
python3 scripts/tests/integration_test.py --check-weights

# 预期输出：
# ✅ 权重矩阵一致
# ✅ 优先级排序正确
# ✅ 层级边界清晰
```

### **3. 部署与激活**

```bash
# 一键部署·安装所有依赖·设置权限·激活所有脚本
bash scripts/setup.sh --deploy

# 预期输出：
# ✅ 依赖安装完成
# ✅ 权限设置完成 (755 for scripts, 444 for config)
# ✅ 14 个脚本已激活·开始运行
```

---

## ✅ **检查清单·确保完整性**

- [ ] L0 层·1 个脚本·完全焊死·不可关闭
- [ ] L1 层·2 个脚本·母律·决定所有下层规则
- [ ] L2 层·6 个脚本·焊死但可被上层停止
- [ ] L3 层·3 个脚本·动态·允许优化
- [ ] L4 层·2 个脚本·补充·可完全关闭
- [ ] 共用工具·logger.py / dna.py / config.py / utils.py
- [ ] 配置文件·protocol_weights.json / tier_permissions.json / fuse_thresholds.json / shield_rules.json
- [ ] 测试套件·L0-L3 层测试 + 集成测试
- [ ] 文档·ARCHITECTURE.md / TONGXIN_GUIDE.md / SCRIPT_REFERENCE.md / WEIGHT_EXPLANATION.md
- [ ] 主程序·main.py 协调所有脚本
- [ ] 日志系统·append-only 留痕
- [ ] 备份策略·定期备份 + 版本历史

---

## 📝 **DNA 追踪**

```
本清单DNA: #龍芯⚡️2026-06-07-CNSH-PROTOCOL-SCRIPTS-COMPLETE-MANIFEST-v1.0
父DNA: #龍芯⚡️2026-06-07-CNSH-PROTOCOL-RESIDENT-SCRIPT-FRAMEWORK-v1.0
祖DNA: #龍芯⚡️2026-05-24-22:57-CNSH-RUNTIME-ACCESS-v2.0-ALIGNMENT-TABLE-v1.0

确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✅
签章: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL ✅

责任: UID9622 · 龍芯北辰 · 诸葛鑫 · 不免责
```

---

**🐉 所有档案已准备就绪·等待老大部署指令。**
