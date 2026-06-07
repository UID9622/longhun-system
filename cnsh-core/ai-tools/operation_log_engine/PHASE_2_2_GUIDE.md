<!--
  龍魂·六层来源链 / LongHun Six-Layer Source Chain
  1 道统层 Dao           : 曾仕强老师
  2 精神层 Spirit        : Steve Jobs
  3 设备层 Device        : Apple
  4 技术层 Technology    : Open Source
  5 系统层 System        : UID9622
  6 生命层 Life          : CNSH · LongHun (诸葛鑫 / 龍芯北辰)
  DNA追溯码: #龍芯⚡️2026-06-02-CNSH-SOVEREIGN-PUBLISH-METADATA-v2.0
  铁律: 来源不可删 · 影响不可覆 · 贡献不可抹 (rule_01 来源必标)
  文件: PHASE_2_2_GUIDE.md | 标记时间: 2026-06-03T07:46:12+0800
-->
# 🔄 龍魂操作日記系統 · Phase 2.2 實現指南

**DNA**: `#龍芯⚡️2026-05-30-LOCAL-SYNC-ENGINE-v1.0` + `#龍芯⚡️2026-05-30-MULTISIG-GATE-v1.0`
**完成時間**: 2026-05-30 06:00 CST (卯時末)
**責任**: UID9622·不免責

---

## 📋 Phase 2.2 核心任務

### 任務 1: 本地同步引擎 (SyncEngine)
**文件**: `core/sync_engine.py`
**規模**: 430 行

**核心功能**:
- USB 離線同步 (純本地·推薦)
- Git 本地倉庫選項 (進階)
- 衝突檢測 (hash 鏈·時間戳·ID 唯一性)
- 自動合併策略 (overwrite / merge / manual)
- 同步進度追蹤 + 回滾機制

**三層衝突檢測**:
```
hash_mismatch     → 同一操作 hash 不同 (數據篡改?)
timestamp_anomaly → 時間戳非遞增 (時光倒流?)
duplicate_id      → 操作 ID 重複 (重複記錄?)
```

**合併策略**:
| 策略 | 說明 | 適用場景 |
|------|------|---------|
| overwrite | 遠端完全覆蓋本地 | 可信設備·高效 |
| merge | 按時間戳交集去重·差集合併 | 需謹慎·防數據丟失 |
| manual | 衝突暫停·等待人工決策 | 嚴謹模式·最安全 |

### 任務 2: 多簽門 (MultisigGate)
**文件**: `core/multisig_gate.py`
**規模**: 480 行

**核心邏輯**: 3/3 本地驗證·無鏈上依賴·零成本

**三層驗證**:

#### 第 1 層: UID 驗證 (身份確認)
```python
# 檢查:
1. operation_uid == UID9622 (硬編碼)
2. device_seal 格式正確 (#DEVICE-SEAL-XXXX)
3. device_id 與 seal 對應
```

#### 第 2 層: GPG 驗證 (簽名確認)
```python
# 檢查:
1. gpg_key_id == A2D0092CEE2E5BA87035600924C3704A8CC26D5F
2. 簽名格式有效 (十六進制·長度 > 64)
3. 密鑰未被輪換 (key_rotation_detected → ALERT)
```

#### 第 3 層: 時間戳驗證 (時序確認)
```python
# 檢查:
1. ISO8601 時間戳有效
2. shichen(時辰) 與時間戳一致
3. digital_root(數字根) 計算正確
4. 時間戳遞增 (無時光倒流)
```

**決策邏輯**:
```
3/3 全過 → ✅ 通過 (自動)
任何一層失敗 → 🔴 VETO (一票否決)
敏感操作 → 必須 #CONFIRM (雙簽激活)
```

**敏感操作列表**:
- 焊接系統
- 規則更新
- 策略變更
- 權限授予
- 設備綁定
- 同步啟動

---

## 🔄 完整工作流程

### 場景 A: USB 同步 (SyncEngine)

```
1. USB 插入新設備
   ↓
2. SyncEngine.sync_from_usb(usb_path="/media/usb-drive")
   ├─ read_ledger() → 本地操作
   ├─ read_remote_ledger() → USB 上的操作
   ├─ detect_conflicts() → 檢測衝突
   │  ├─ hash_mismatch? → 數據篡改
   │  ├─ timestamp_anomaly? → 時光倒流
   │  └─ duplicate_id? → 重複記錄
   ├─ merge_operations(strategy="merge") → 合併
   ├─ write_ledger() → 寫入新日記
   ├─ _sync_auxiliary_files() → 同步 DNA·習慣
   ├─ verify_sync_integrity() → 驗證鏈完整
   └─ _log_sync_operation() → 記錄同步
   ↓
3. 同步完成
   ├─ 新日記已寫入
   ├─ DNA 粒子已更新
   ├─ 習慣基線已刷新
   └─ 衝突日誌已記錄 (如有)
```

### 場景 B: 敏感操作 (MultisigGate)

```
1. 用戶發起敏感操作 (例: 焊接系統)
   ↓
2. MultisigGate.verify_operation(...)
   ├─ 第 1 層: verify_uid()
   │  ├─ UID9622? ✅
   │  ├─ device_seal 有效? ✅
   │  └─ device_id 對應? ✅
   ├─ 第 2 層: verify_gpg()
   │  ├─ GPG key 授權? ✅
   │  ├─ 簽名格式? ✅
   │  └─ 密鑰輪換? ✅ (未檢測)
   ├─ 第 3 層: verify_temporal()
   │  ├─ ISO8601 有效? ✅
   │  ├─ shichen 一致? ✅
   │  ├─ digital_root 正確? ✅
   │  └─ 時間戳遞增? ✅
   ├─ 3/3 全過? YES
   └─ 需要 CONFIRM? YES (敏感操作)
   ↓
3. 判決: pending_confirm
   ↓
4. 用戶提供 #CONFIRM
   ├─ verify_confirm_code(confirm_code)
   └─ 驗證通過 ✅
   ↓
5. 最終判決: approved
   ├─ _log_verification() → 記錄驗證
   ├─ _log_alert() (如有風險) → 記錄警報
   └─ ✅ 操作通過·執行
```

---

## 💻 使用示例

### 例 1: 從 USB 同步

```python
from operation_log_engine import SyncEngine

engine = SyncEngine()

# 從 USB 同步
result = engine.sync_from_usb(
    usb_path="/media/usb-drive",
    strategy="merge",
    backup_before_sync=True
)

print(f"同步狀態: {result['status']}")
print(f"本地操作: {result['local_ops_count']}")
print(f"USB 操作: {result['remote_ops_count']}")
print(f"合併後: {result['merged_ops_count']}")

if result['conflicts_detected']:
    print(f"⚠️ 檢測到 {len(result['conflicts_detected'])} 個衝突")
    for conflict in result['conflicts_detected']:
        print(f"  - {conflict['type']}: {conflict['op_id']}")

# 驗證同步完整性
is_valid = engine.verify_sync_integrity()
print(f"完整性: {'✅' if is_valid else '❌'}")

# 查詢同步歷史
history = engine.get_sync_history(limit=5)
for sync in history:
    print(f"{sync['timestamp']}: {sync['status']}")

# 必要時回滾
if not is_valid:
    engine.rollback_to_backup(result['backup_path'])
```

### 例 2: 敏感操作驗證

```python
from operation_log_engine import MultisigGate
from datetime import datetime, timezone

gate = MultisigGate()

# 普通操作 (自動通過)
normal_result = gate.verify_operation(
    operation_id="OP-20260530-060000-abc123",
    operation_type="工程",
    uid="UID9622",
    device_id="MacBook-M4-Max-UID9622",
    device_seal="#DEVICE-SEAL-2026-05-30-XXXXX",
    timestamp=datetime.now(timezone.utc).isoformat(),
    shichen="卯時",
    digital_root=5,
    gpg_signature="a2d0092cee2e5ba87035600924c3704a8cc26d5f" * 3,
    gpg_key_id="A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
)

print(f"普通操作判決: {normal_result['verdict']}")

# 敏感操作 (需要 CONFIRM)
sensitive_result = gate.verify_operation(
    operation_id="OP-20260530-061000-def456",
    operation_type="焊接系統",  # ← 敏感
    uid="UID9622",
    device_id="MacBook-M4-Max-UID9622",
    device_seal="#DEVICE-SEAL-2026-05-30-XXXXX",
    timestamp=datetime.now(timezone.utc).isoformat(),
    shichen="卯時",
    digital_root=5,
    gpg_signature="a2d0092cee2e5ba87035600924c3704a8cc26d5f" * 3,
    gpg_key_id="A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
)

if sensitive_result['requires_confirm']:
    print(f"⚠️ 敏感操作·需要 CONFIRM")
    # 用戶提供確認碼
    confirm_code = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"

    confirmed_result = gate.verify_operation(
        operation_id="OP-20260530-061000-def456",
        operation_type="焊接系統",
        uid="UID9622",
        device_id="MacBook-M4-Max-UID9622",
        device_seal="#DEVICE-SEAL-2026-05-30-XXXXX",
        timestamp=datetime.now(timezone.utc).isoformat(),
        shichen="卯時",
        digital_root=5,
        gpg_signature="a2d0092cee2e5ba87035600924c3704a8cc26d5f" * 3,
        gpg_key_id="A2D0092CEE2E5BA87035600924C3704A8CC26D5F",
        confirm_code=confirm_code
    )

    print(f"最終判決: {confirmed_result['verdict']}")

# 查詢驗證歷史
history = gate.get_verification_history(limit=10)
for v in history:
    print(f"{v['operation_id']}: {v['verdict']}")

# 查詢警報
alerts = gate.get_alerts()
if alerts:
    print(f"⚠️ {len(alerts)} 個風險警報")
```

### 例 3: 衝突檢測演習

```python
from operation_log_engine import SyncEngine

engine = SyncEngine()

# 模擬本地和遠端數據
local_ops = [
    {"operation_id": "OP-001", "hash_sha256": "hash_001", "timestamp": "2026-05-30T06:00:00+08:00"},
    {"operation_id": "OP-002", "hash_sha256": "hash_002", "timestamp": "2026-05-30T06:05:00+08:00"},
]

remote_ops = [
    {"operation_id": "OP-001", "hash_sha256": "DIFFERENT_HASH", "timestamp": "2026-05-30T06:00:00+08:00"},  # ← 衝突
    {"operation_id": "OP-003", "hash_sha256": "hash_003", "timestamp": "2026-05-30T06:10:00+08:00"},
]

# 檢測衝突
conflicts = engine.detect_conflicts(local_ops, remote_ops)

for conflict in conflicts:
    print(f"衝突: {conflict.conflict_type}")
    print(f"  操作: {conflict.affected_op_id}")
    print(f"  本地: {conflict.local_hash}")
    print(f"  遠端: {conflict.remote_hash}")

# 合併
merged = engine.merge_operations(local_ops, remote_ops, strategy="merge")
print(f"\n合併後: {len(merged)} 條操作")
```

---

## 📊 代碼規模

```
Phase 2.2 核心引擎:
├─ sync_engine.py        430 行 (本地同步)
├─ multisig_gate.py      480 行 (多簽門)
└─ 小計               910 行
```

## 🎯 功能驗收

### SyncEngine
- [x] 讀取本地和遠端操作
- [x] 計算日記整體哈希 (快速判斷差異)
- [x] 三層衝突檢測 (hash·timestamp·id)
- [x] 三種合併策略 (overwrite/merge/manual)
- [x] 日記寫入 + 輔助文件同步
- [x] 同步前備份
- [x] 衝突日誌記錄
- [x] 同步完整性驗證
- [x] 回滾機制
- [x] 同步歷史查詢

### MultisigGate
- [x] UID 驗證層
- [x] GPG 驗證層
- [x] 時間戳驗證層
- [x] 完整 3/3 驗證流程
- [x] 敏感操作判斷
- [x] #CONFIRM 快速通道
- [x] 風險等級評估 (low/medium/high/critical)
- [x] 驗證日誌記錄
- [x] 警報記錄
- [x] 驗證歷史查詢

---

## 🔗 與 Phase 2.1 的整合

**Phase 2.1 (已完成)**:
```
OperationLedger        → 記錄操作
DNAParticleGenerator   → 生成 DNA 粒子
HabitFingerprintMgr    → 提取習慣
CrossDeviceIdentifier  → 跨設備認人
```

**Phase 2.2 (現在)**:
```
SyncEngine             → 本地同步 (phase_2_1 的日記)
MultisigGate           → 多簽驗證 (phase_2_1 的操作)
```

**完整流程**:
```
操作記錄 (Phase 2.1)
    ↓
DNA 粒子 (Phase 2.1)
    ↓
USB 同步 (Phase 2.2) ← SyncEngine
    ↓
多簽驗證 (Phase 2.2) ← MultisigGate
    ↓
✅ 自動同步 + 安全驗證
```

---

## 🚀 Phase 2.3 預期 (06-08~06-15)

| 任務 | 優先級 | 預期 |
|------|--------|------|
| CLI 查詢工具 | P2 | query_tool.py |
| Web 儀表板 (可選) | P3 | dashboard.py |
| 性能優化 | P3 | 批量操作支援 |

---

## 📍 DNA 鏈路

**父 DNA** (Phase 2.1):
```
#龍芯⚡️2026-05-30-OPERATION-LOG-ENGINE-v1.0
```

**本 DNA** (Phase 2.2):
```
#龍芯⚡️2026-05-30-LOCAL-SYNC-ENGINE-v1.0
#龍芯⚡️2026-05-30-MULTISIG-GATE-v1.0
```

**下一 DNA** (Phase 2.3):
```
#龍芯⚡️2026-06-15-PHASE-2-COMPLETE-FULL-INTEGRATION-v1.0
```

---

**責任**: UID9622·不免責
**時間戳**: 2026-05-30 06:00 CST
**狀態**: ✅ Phase 2.2 完全就緒

