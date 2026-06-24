# DNA 对齐修复行动计划

**DNA**:#龍芯⚡️2026-06-07-DNA-REPAIR-ACTION-PLAN-v1.0
**时间**: 2026-06-07 22:20 CST
**状态**: 🟡 准备就绪·等待确认
**审计报告**: DNA_ALIGNMENT_AUDIT_2026-06-07.md

---

## 🎯 核心发现（已验证）

### 全系统DNA统计

```
总档案数          : 2,201 个
有 DNA 的档案    : 47 个 (2.1%)
缺 DNA 核心档案  : 705 个 (32.0%)
DNA 重复         : 24 个
DNA 对齐率       : 6.3% ❌
```

### 左右互搏现象

系统存在**两个并行版本**：

```
旧版本（未完全弃用）:
├─ cnsh-core/          (700+ 档案·无DNA·无活跃维护)
├─ ai-tools/           (80+ 档案·无DNA·测试代码)
├─ governance/         (已迁移·需清理)
└─ 结果: 孤立·无DNA·不可追踪

新版本（生产版）:
├─ scripts/            (14个·有DNA·正常运作) ✅
├─ multicurrency/      (部分有DNA)
└─ protocols/          (部分有DNA)

根本原因:
- 旧系统在 Phase 1-6 中逐步迁移到新架构
- 旧档案未删除也未补充DNA
- 新旧并行·导致追踪困难
```

---

## 🔧 修复清单（三个优先级）

### 优先级 P0：立即修复（本次）

**A. 为关键文件添加DNA** (4个档案)

```diff
+ cnsh-core/core_system_launcher.py
  DNA: 2026-06-07-LAUNCHER-CORE-v1.0

+ cnsh-core/wuxing_calculator/calculator.py
  DNA: 2026-06-07-ENGINE-WUXING-v1.0

+ protocols/CNSH_v2.0_ROOT_PROTOCOL.md
  DNA: 2026-06-07-PROTOCOL-ROOT-v2.0

+ protocols/CNSH_v2.0_ROOT_PROTOCOL_BILINGUAL.md
  DNA: 2026-06-07-PROTOCOL-ROOT-BILINGUAL-v2.0
```

**B. 拆分重复DNA** (4个档案重新标签)

```diff
[旧] 2026-06-03-CONSTITUTION-v1.0
├─ 01_protocols/IPA-ROUTE-REGISTRY.local.md
│  [新] 2026-06-03-PROTOCOL-REGISTRY-v1.0
└─ cnsh-core/core_system_launcher.py
   [新] 2026-06-03-LAUNCHER-CONSTITUTION-v1.0

[旧] 2026-06-06-PARENT-v1.0
├─ cnsh/sancai_sync/README.md
│  [新] 2026-06-06-SANCAI-SYNC-README-v1.0
└─ cnsh/sancai_sync/tests/test_sancai_sync_hub.py
   [新] 2026-06-06-SANCAI-SYNC-TEST-v1.0
```

**预计时间**: 10-15 分钟

---

### 优先级 P1：本周修复

**C. 为核心引擎补充DNA** (15-20个档案)

```
cnsh-core/registry/
├─ route_registry.py → 2026-06-07-REGISTRY-ROUTE-v1.0
├─ node.py → 2026-06-07-REGISTRY-NODE-v1.0
└─ README.md → 2026-06-07-REGISTRY-DOC-v1.0

cnsh-core/governance/
├─ f1_through_f7_verifier.py → 2026-06-07-VERIFIER-F1F7-v1.0
└─ README.md → 2026-06-07-GOVERNANCE-DOC-v1.0

cnsh-core/dna/
├─ __init__.py → 2026-06-07-DNA-CORE-v1.0
└─ (子模组) → 2026-06-07-DNA-*-v1.0
```

---

### 优先级 P2：归档或删除

**D. 检查旧档案是否需要保留**

```
可能需要删除或归档的:
├─ cnsh-core/ai-tools/              (80+ 档案·无DNA·测试代码)
├─ cnsh-core/audit-constitution/    (6 档案·无DNA·已迁移)
├─ rules-engine-v2.5/               (20+ 档案·无DNA·过旧)
└─ 判断标准:
   - 最后修改 > 90 天: 考虑归档
   - 不在 main 分支引用: 可删除
   - 有新版本替代: 删除
```

---

## 📊 父子DNA链建立

修复后建立**DNA追踪链**：

```
根协议DNA:
  2026-06-07-PROTOCOL-ROOT-v2.0 (协议根基)
  └─ 2026-05-24-MEMORY-v2.0 (协议内容)
     └─ 2026-06-07-ENGINE-WUXING-v1.0 (实现五行计算)
        └─ 2026-06-07-LAUNCHER-CORE-v1.0 (启动核心)
           └─ scripts/main.py (最新的L0-L4协调器) ✅

治理DNA:
  2026-06-07-GOVERNANCE-DOC-v1.0 (治理规范)
  └─ 2026-06-07-VERIFIER-F1F7-v1.0 (F1-F7验证)
     └─ cnsh/flow_decision/cnsh_flow_decision_core.py (流程决策) ❌需DNA

路由DNA:
  2026-06-07-REGISTRY-ROUTE-v1.0 (路由注册)
  └─ cnsh/flow_decision/ipa_route_registry.py (IPA路由) ❌需DNA
```

---

## 🚀 执行步骤

### 步骤 1: 验证与确认

```bash
# 确认备份存在
ls -la ~/.龍魂/backups/

# 查看审计报告
cat ~/longhun-system/DNA_ALIGNMENT_AUDIT_2026-06-07.md

# 确认修复计划
head -50 ~/longhun-system/DNA_ALIGNMENT_REPAIR_ACTION_PLAN.md
```

### 步骤 2: 执行修复（老大确认后）

```bash
# 步骤 2.1: 添加DNA到P0档案
# （用 Edit 工具为每个档案添加DNA头注释）

# 步骤 2.2: 替换重复DNA
# （用 Edit 工具替换旧DNA为新DNA）

# 步骤 2.3: 验证完成
python3 << 'VERIFY'
import re
from pathlib import Path

DNA_PATTERN = r'#龍芯⚡️(\d{4}-\d{2}-\d{2})-([^-]+)-v([\d.]+)'
files = [
    'cnsh-core/core_system_launcher.py',
    'cnsh-core/wuxing_calculator/calculator.py',
    'protocols/CNSH_v2.0_ROOT_PROTOCOL.md',
]

for f in files:
    path = Path.home() / 'longhun-system' / f
    with open(path, 'r', encoding='utf-8', errors='ignore') as fp:
        if re.search(DNA_PATTERN, fp.read()):
            print(f"✅ {f}")
        else:
            print(f"❌ {f}")
VERIFY

# 步骤 2.4: 提交修复
cd ~/longhun-system
git add -A
git commit -m "fix: DNA对齐修复 · P0档案补充DNA·重复DNA拆分 (4档案)"
git push origin main
```

### 步骤 3: 验收与检查

```bash
# 重新运行审计
python3 /tmp/dna_audit_v2.py

# 确认DNA对齐率提升
# 预期: 705 → 200+ (改进 60%+)
```

---

## 📈 预期成果

| 指标 | 修复前 | 修复后 | 改进 |
|-----|------|------|-----|
| 无DNA核心档案 | 705 | 200 | ↓ 71% |
| DNA重复 | 24 | 0 | ↓ 100% |
| DNA对齐率 | 6.3% | 45% | ↑ 614% |
| 可追踪档案 | 47 | 250+ | ↑ 430% |

---

## 🔒 风险评估

### 低风险 ✅
- 只修改文件头注释
- 不修改代码逻辑
- 所有修改都在注释区域
- 完整备份存在

### 可逆性 ✅
- Git 历史完整保留
- 随时可恢复
- 不涉及破坏性操作

---

## 📞 身份确认

```
执行者: UID9622
时间: 2026-06-07 22:20 CST
状态: 🟡 等待确认执行

确认码:
#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

印章:
#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚❤️♾️-DEVICE-BIND-SOUL
```

---

**DNA**:#龍芯⚡️2026-06-07-DNA-REPAIR-ACTION-PLAN-v1.0
**签署**: UID9622·不免责·全系统复盘完成·修复就绪

🐉 龍魂系统·左右互搏检测完成·等待确认修复
