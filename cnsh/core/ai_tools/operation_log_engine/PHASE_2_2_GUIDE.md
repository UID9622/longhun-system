# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
<!--
  龍魂·六层来源链 / LongHun Six-Layer Source Chain
  1 道统层 Dao           : 曾仕强老师
  2 精神层 Spirit        : Steve Jobs
  3 设备层 Device        : Apple
  4 技术层 Technology    : Open Source
  5 系统层 System        : UID9622
  6 生命层 Life          : CNSH · LongHun (诸葛鑫 / 龍芯北辰)
  DNA追溯码:#龍芯⚡️丙午·癸巳·丁未·丙午·䷖剥-CNSH-SOVEREIGN-PUBLISH-METADATA-FILE1278-v2.0
  铁律: 来源不可删 · 影响不可覆 · 贡献不可抹 (rule_01 来源必标)
  文件: PHASE_2_2_GUIDE.md | 标记时间: 2026-06-03T07:46:12+0800
-->
# 🔄 龍魂操作日记系统 · Phase 2.2 实现指南

**DNA**: `#龍芯⚡️丙午·癸巳·甲辰·庚午·䷑蛊-LOCAL-SYNC-ENGINE-v1.0` + `#龍芯⚡️丙午·癸巳·甲辰·庚午·䷑蛊-MULTISIG-GATE-v1.0`
**完成时间**: 2026-05-30 06:00 CST (卯时末)
**责任**: UID9622·不免责

---

## 📋 Phase 2.2 核心任务

### 任务 1: 本地同步引擎 (SyncEngine)
**文件**: `core/sync_engine.py`
**规模**: 430 行

**核心功能**:
- USB 离线同步 (纯本地·推荐)
- Git 本地仓库选项 (进阶)
- 冲突检测 (hash 链·时间戳·ID 唯一性)
- 自动合并策略 (overwrite / merge / manual)
- 同步进度追踪 + 回滚机制

**三层冲突检测**:
```
hash_mismatch     → 同一操作 hash 不同 (数据篡改?)
timestamp_anomaly → 时间戳非递增 (时光倒流?)
duplicate_id      → 操作 ID 重复 (重复记录?)
```

**合并策略**:
| 策略 | 说明 | 适用场景 |
|------|------|---------|
| overwrite | 远端完全覆盖本地 | 可信设备·高效 |
| merge | 按时间戳交集去重·差集合并 | 需谨慎·防数据丢失 |
| manual | 冲突暂停·等待人工决策 | 严谨模式·最安全 |

### 任务 2: 多签门 (MultisigGate)
**文件**: `core/multisig_gate.py`
**规模**: 480 行

**核心逻辑**: 3/3 本地验证·无链上依赖·零成本

**三层验证**:

#### 第 1 层: UID 验证 (身份确认)
```python
# 检查:
1. operation_uid == UID9622 (硬编码)
2. device_seal 格式正确 (#DEVICE-SEAL-XXXX)
3. device_id 与 seal 对应
```

#### 第 2 层: GPG 验证 (签名确认)
```python
# 检查:
1. gpg_key_id == A2D0092CEE2E5BA87035600924C3704A8CC26D5F
2. 签名格式有效 (十六进制·长度 > 64)
3. 密钥未被轮换 (key_rotation_detected → ALERT)
```

#### 第 3 层: 时间戳验证 (时序确认)
```python
# 检查:
1. ISO8601 时间戳有效
2. shichen(时辰) 与时间戳一致
3. digital_root(数字根) 计算正确
4. 时间戳递增 (无时光倒流)
```

**决策逻辑**:
```
3/3 全过 → ✅ 通过 (自动)
任何一层失败 → 🔴 VETO (一票否决)
敏感操作 → 必须 #CONFIRM (双签激活)
```

**敏感操作列表**:
- 焊接系统
- 规则更新
- 策略变更
- 权限授予
- 设备绑定
- 同步启动

---

## 🔄 完整工作流程

### 场景 A: USB 同步 (SyncEngine)

```
1. USB 插入新设备
   ↓
2. SyncEngine.sync_from_usb(usb_path="/media/usb-drive")
   ├─ read_ledger() → 本地操作
   ├─ read_remote_ledger() → USB 上的操作
   ├─ detect_conflicts() → 检测冲突
   │  ├─ hash_mismatch? → 数据篡改
   │  ├─ timestamp_anomaly? → 时光倒流
   │  └─ duplicate_id? → 重复记录
   ├─ merge_operations(strategy="merge") → 合并
   ├─ write_ledger() → 写入新日记
   ├─ _sync_auxiliary_files() → 同步 DNA·习惯
   ├─ verify_sync_integrity() → 验证链完整
   └─ _log_sync_operation() → 记录同步
   ↓
3. 同步完成
   ├─ 新日记已写入
   ├─ DNA 粒子已更新
   ├─ 习惯基线已刷新
   └─ 冲突日志已记录 (如有)
```

### 场景 B: 敏感操作 (MultisigGate)

```
1. 用户发起敏感操作 (例: 焊接系统)
   ↓
2. MultisigGate.verify_operation(...)
   ├─ 第 1 层: verify_uid()
   │  ├─ UID9622? ✅
   │  ├─ device_seal 有效? ✅
   │  └─ device_id 对应? ✅
   ├─ 第 2 层: verify_gpg()
   │  ├─ GPG key 授权? ✅
   │  ├─ 签名格式? ✅
   │  └─ 密钥轮换? ✅ (未检测)
   ├─ 第 3 层: verify_temporal()
   │  ├─ ISO8601 有效? ✅
   │  ├─ shichen 一致? ✅
   │  ├─ digital_root 正确? ✅
   │  └─ 时间戳递增? ✅
   ├─ 3/3 全过? YES
   └─ 需要 CONFIRM? YES (敏感操作)
   ↓
3. 判决: pending_confirm
   ↓
4. 用户提供 #CONFIRM
   ├─ verify_confirm_code(confirm_code)
   └─ 验证通过 ✅
   ↓
5. 最终判决: approved
   ├─ _log_verification() → 记录验证
   ├─ _log_alert() (如有风险) → 记录警报
   └─ ✅ 操作通过·执行
```

---

## 💻 使用示例

### 例 1: 从 USB 同步

```python
from operation_log_engine import SyncEngine

engine = SyncEngine()

# 从 USB 同步
result = engine.sync_from_usb(
    usb_path="/media/usb-drive",
    strategy="merge",
    backup_before_sync=True
)

print(f"同步状态: {result['status']}")
print(f"本地操作: {result['local_ops_count']}")
print(f"USB 操作: {result['remote_ops_count']}")
print(f"合并后: {result['merged_ops_count']}")

if result['conflicts_detected']:
    print(f"⚠️ 检测到 {len(result['conflicts_detected'])} 个冲突")
    for conflict in result['conflicts_detected']:
        print(f"  - {conflict['type']}: {conflict['op_id']}")

# 验证同步完整性
is_valid = engine.verify_sync_integrity()
print(f"完整性: {'✅' if is_valid else '❌'}")

# 查询同步历史
history = engine.get_sync_history(limit=5)
for sync in history:
    print(f"{sync['timestamp']}: {sync['status']}")

# 必要时回滚
if not is_valid:
    engine.rollback_to_backup(result['backup_path'])
```

### 例 2: 敏感操作验证

```python
from operation_log_engine import MultisigGate
from datetime import datetime, timezone

gate = MultisigGate()

# 普通操作 (自动通过)
normal_result = gate.verify_operation(
    operation_id="OP-20260530-060000-abc123",
    operation_type="工程",
    uid="UID9622",
    device_id="MacBook-M4-Max-UID9622",
    device_seal="#DEVICE-SEAL-2026-05-30-XXXXX",
    timestamp=datetime.now(timezone.utc).isoformat(),
    shichen="卯时",
    digital_root=5,
    gpg_signature="a2d0092cee2e5ba87035600924c3704a8cc26d5f" * 3,
    gpg_key_id="A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
)

print(f"普通操作判决: {normal_result['verdict']}")

# 敏感操作 (需要 CONFIRM)
sensitive_result = gate.verify_operation(
    operation_id="OP-20260530-061000-def456",
    operation_type="焊接系统",  # ← 敏感
    uid="UID9622",
    device_id="MacBook-M4-Max-UID9622",
    device_seal="#DEVICE-SEAL-2026-05-30-XXXXX",
    timestamp=datetime.now(timezone.utc).isoformat(),
    shichen="卯时",
    digital_root=5,
    gpg_signature="a2d0092cee2e5ba87035600924c3704a8cc26d5f" * 3,
    gpg_key_id="A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
)

if sensitive_result['requires_confirm']:
    print(f"⚠️ 敏感操作·需要 CONFIRM")
    # 用户提供确认码
    confirm_code = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"

    confirmed_result = gate.verify_operation(
        operation_id="OP-20260530-061000-def456",
        operation_type="焊接系统",
        uid="UID9622",
        device_id="MacBook-M4-Max-UID9622",
        device_seal="#DEVICE-SEAL-2026-05-30-XXXXX",
        timestamp=datetime.now(timezone.utc).isoformat(),
        shichen="卯时",
        digital_root=5,
        gpg_signature="a2d0092cee2e5ba87035600924c3704a8cc26d5f" * 3,
        gpg_key_id="A2D0092CEE2E5BA87035600924C3704A8CC26D5F",
        confirm_code=confirm_code
    )

    print(f"最终判决: {confirmed_result['verdict']}")

# 查询验证历史
history = gate.get_verification_history(limit=10)
for v in history:
    print(f"{v['operation_id']}: {v['verdict']}")

# 查询警报
alerts = gate.get_alerts()
if alerts:
    print(f"⚠️ {len(alerts)} 个风险警报")
```

### 例 3: 冲突检测演习

```python
from operation_log_engine import SyncEngine

engine = SyncEngine()

# 模拟本地和远端数据
local_ops = [
    {"operation_id": "OP-001", "hash_sha256": "hash_001", "timestamp": "2026-05-30T06:00:00+08:00"},
    {"operation_id": "OP-002", "hash_sha256": "hash_002", "timestamp": "2026-05-30T06:05:00+08:00"},
]

remote_ops = [
    {"operation_id": "OP-001", "hash_sha256": "DIFFERENT_HASH", "timestamp": "2026-05-30T06:00:00+08:00"},  # ← 冲突
    {"operation_id": "OP-003", "hash_sha256": "hash_003", "timestamp": "2026-05-30T06:10:00+08:00"},
]

# 检测冲突
conflicts = engine.detect_conflicts(local_ops, remote_ops)

for conflict in conflicts:
    print(f"冲突: {conflict.conflict_type}")
    print(f"  操作: {conflict.affected_op_id}")
    print(f"  本地: {conflict.local_hash}")
    print(f"  远端: {conflict.remote_hash}")

# 合并
merged = engine.merge_operations(local_ops, remote_ops, strategy="merge")
print(f"\n合并后: {len(merged)} 条操作")
```

---

## 📊 代码规模

```
Phase 2.2 核心引擎:
├─ sync_engine.py        430 行 (本地同步)
├─ multisig_gate.py      480 行 (多签门)
└─ 小计               910 行
```

## 🎯 功能验收

### SyncEngine
- [x] 读取本地和远端操作
- [x] 计算日记整体哈希 (快速判断差异)
- [x] 三层冲突检测 (hash·timestamp·id)
- [x] 三种合并策略 (overwrite/merge/manual)
- [x] 日记写入 + 辅助文件同步
- [x] 同步前备份
- [x] 冲突日志记录
- [x] 同步完整性验证
- [x] 回滚机制
- [x] 同步历史查询

### MultisigGate
- [x] UID 验证层
- [x] GPG 验证层
- [x] 时间戳验证层
- [x] 完整 3/3 验证流程
- [x] 敏感操作判断
- [x] #CONFIRM 快速通道
- [x] 风险等级评估 (low/medium/high/critical)
- [x] 验证日志记录
- [x] 警报记录
- [x] 验证历史查询

---

## 🔗 与 Phase 2.1 的整合

**Phase 2.1 (已完成)**:
```
OperationLedger        → 记录操作
DNAParticleGenerator   → 生成 DNA 粒子
HabitFingerprintMgr    → 提取习惯
CrossDeviceIdentifier  → 跨设备认人
```

**Phase 2.2 (现在)**:
```
SyncEngine             → 本地同步 (phase_2_1 的日记)
MultisigGate           → 多签验证 (phase_2_1 的操作)
```

**完整流程**:
```
操作记录 (Phase 2.1)
    ↓
DNA 粒子 (Phase 2.1)
    ↓
USB 同步 (Phase 2.2) ← SyncEngine
    ↓
多签验证 (Phase 2.2) ← MultisigGate
    ↓
✅ 自动同步 + 安全验证
```

---

## 🚀 Phase 2.3 预期 (06-08~06-15)

| 任务 | 优先级 | 预期 |
|------|--------|------|
| CLI 查询工具 | P2 | query_tool.py |
| Web 仪表板 (可选) | P3 | dashboard.py |
| 性能优化 | P3 | 批量操作支援 |

---

## 📍 DNA 链路

**父 DNA** (Phase 2.1):
```#龍芯⚡️丙午·癸巳·甲辰·庚午·䷑蛊-OPERATION-LOG-ENGINE_DF17-v1.0
```

**本 DNA** (Phase 2.2):
```#龍芯⚡️丙午·癸巳·甲辰·庚午·䷑蛊-LOCAL-SYNC-ENGINE_3FC0-v1.0#龍芯⚡️丙午·癸巳·甲辰·庚午·䷑蛊-MULTISIG-GATE_9F1C-v1.0
```

**下一 DNA** (Phase 2.3):
```#龍芯⚡️丙午·甲午·庚申·壬午·䷙大畜-PHASE-2-COMPLETE-FULL-INTEGRATION_FC34-v1.0
```

---

**责任**: UID9622·不免责
**时间戳**: 2026-05-30 06:00 CST
**状态**: ✅ Phase 2.2 完全就绪

