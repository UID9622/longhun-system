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
  文件: IMPLEMENTATION_GUIDE.md | 标记时间: 2026-06-03T07:46:12+0800
-->
# 🧬 龍魂操作日記系統 · Phase 2.1 實現指南

**DNA**: `#龍芯⚡️2026-05-30-OPERATION-LOG-ENGINE-v1.0`
**責任**: UID9622·不免責
**日期**: 2026-05-30 (卯時末·火時)

---

## 📋 核心架構 (四引擎系統)

### 1️⃣ OperationLedger (操作日記)
**文件**: `core/operation_ledger.py`

**功能**:
- append-only JSONL 日記 (每次操作一條·不可修改)
- SHA-256 parent-hash 鏈式驗證 (無斷裂)
- 自動習慣提取 (拼音錯別字、口頭禪、逗號習慣)
- 時辰 + 數字根計算

**核心方法**:
```python
ledger = OperationLedger()

# 追加操作到日記
record = ledger.append_operation(
    operation_type="工程",
    operation_name="L5-F8-implementation",
    device_id="MacBook-M4-Max-UID9622",
    agent_type="Claude Haiku 4.5",
    input_text="嘿嘿,,,帮我设计操作日记",
    output_text="收到! 這是跨設備身份識別系統...",
    rules_triggered=["§9.27", "§11.2"],
    persona_active="P02",
    persona_weight=0.50,
    notes="核心操作·F8引擎啟動"
)

# 驗證鏈完整性
ledger.verify_chain_integrity()  # True if no breaks

# 獲取統計
stats = ledger.get_stats()  # {total_operations, average_habit_match, device_count}
```

**存儲結構**:
```
~/.龍魂/操作日記/
├── operation_ledger.jsonl
│   └── {operation_id}: timestamp, shichen, digital_root, habits, DNA, hash, parent_hash
├── dna_particles/
│   └── OP-*.dna.json
└── habit_fingerprints/
    ├── baseline_snapshot.json
    ├── pinyin_typos.json
    ├── catchphrases.json
    ├── polyphonic_prefs.json
    └── wuxing_profile.json
```

---

### 2️⃣ DNAParticleGenerator (DNA粒子)
**文件**: `core/dna_particle_generator.py`

**功能**:
- 從操作記錄生成 DNA 粒子 (身份証)
- 10 字段決策收據格式
- 三色評判 (🟢🟡🔴)
- 粒子驗證 + 證明導出

**核心方法**:
```python
gen = DNAParticleGenerator()

# 從操作記錄生成 DNA 粒子
dna_particle = gen.generate_from_record(operation_record)

# 保存粒子
file_path = gen.save_particle(dna_particle)
# 結果: ~/.龍魂/operattion_日記/dna_particles/OP-*.dna.json

# 加載粒子
particle = gen.load_particle("OP-20260530-053000-abc123")

# 驗證粒子哈希
is_valid = gen.verify_particle_hash("OP-20260530-053000-abc123")

# 導出粒子作為證明 (含十字段摘要)
proof = gen.export_particle_proof("OP-20260530-053000-abc123")
```

**DNA粒子結構** (10字段):
```json
{
  "identity": {
    "uid": "UID9622",
    "gpg_prefix": "A2D0092CEE2E5BA87035600924C3704A8CC26D5F",
    "device_id": "MacBook-M4-Max-UID9622"
  },
  "temporal_anchor": {
    "iso8601": "2026-05-30T05:30:00+08:00",
    "shichen": "卯時末",
    "digital_root": 5
  },
  "habit_fingerprint": {
    "typo_match": 0.98,
    "catchphrase_match": 0.95,
    "polyphonic_match": 0.92
  },
  "operation": {
    "type": "工程",
    "name": "L5-F8-implementation",
    "input_size": 2048,
    "output_size": 5120
  },
  "dna": "#龍芯⚡️2026-05-30-05:30-OP-工程-L5-F8-v1.0",
  "hash": "sha256_hash_value",
  "parent_hash": "previous_operation_hash",
  "ten_fields": {
    "summary": "工程-L5-F8-implementation",
    "path": "OP-20260530-053000-abc123",
    "route": "P02",
    "weight": 0.50,
    "risk_color": "🟢",
    "rules": "§9.27,§11.2",
    "three_color": "🟢 通過",
    "bias_source": "龍魂文化向量(道德經)",
    "vendor_policy": "Notion AI default security",
    "dna_trace": "#龍芯⚡️2026-05-30-05:30-OP-工程-L5-F8-v1.0"
  }
}
```

---

### 3️⃣ HabitFingerprintManager (習慣指紋)
**文件**: `core/habit_fingerprint_manager.py`

**功能**:
- F8 習慣不動點提取 (拼音錯別字、口頭禪、多音字偏好)
- 基線建立 (baseline_snapshot)
- 習慣匹配度計算 (SI 信心度)
- 跨設備身份驗證

**核心方法**:
```python
manager = HabitFingerprintManager()

# 從操作記錄建立習慣基線
baseline = manager.establish_baseline(operation_records)
manager.save_baseline(baseline)

# 提取新文本的習慣特徵
habits = manager.extract_habit_features("嘿嘿,,,幫我做個新功能")

# 計算新文本與基線的匹配度
overall_si, match_scores = manager.compute_habit_match("嘿嘿,,,帮我设计...")

# 驗證身份 (自動判決: 通過/待審/失敗)
is_verified, message, si = manager.verify_identity(new_text, threshold=0.85)
# 返回: (True, "✅ Confirmed (SI=95%)", 0.95)
```

**習慣基線結構**:
```json
{
  "typos": {
    "得/的": 0.35,
    "哪/那": 0.15
  },
  "catchphrases": {
    "嘿嘿": 0.92,
    "焊死": 0.78,
    "寶寶": 0.65,
    ",,,": 0.98
  },
  "polyphonic": {
    "中": {"usage_frequency": 0.25, "probable_reading": "zhōng"},
    "行": {"usage_frequency": 0.15, "probable_reading": "xíng"}
  },
  "confidence_metrics": {
    "typo_confidence": 0.95,
    "catchphrase_confidence": 0.92,
    "polyphonic_confidence": 0.89,
    "overall_si": 0.92
  }
}
```

**SI 信心度判決**:
- `SI >= 0.85` → ✅ 確認身份 (自動通過)
- `SI 0.70-0.85` → 🟡 身份待審 (需人工確認)
- `SI < 0.70` → 🔴 身份驗證失敗 (拒絕訪問)

---

### 4️⃣ CrossDeviceIdentifier (跨設備識別)
**文件**: `core/cross_device_identifier.py`

**功能**:
- F8 習慣引擎整合
- 設備信任管理 + 設備封印
- 自動同步決策
- 完整的跨設備認人流程

**核心方法**:
```python
identifier = CrossDeviceIdentifier()

# 從USB加載習慣基線
baseline = identifier.load_baseline_from_usb("/media/usb-drive")

# 掃描本地操作記錄
local_ops = identifier.scan_local_operations(limit=100)

# 獲取當前設備ID
device_id = identifier.get_device_id()  # MacBook-M4-Max-UID9622

# 完整識別流程 (一個方法搞定)
result = identifier.identify_user(baseline, local_ops, device_id)
# 返回:
# {
#   'identification': {
#     'si_score': 0.95,
#     'verified': True,
#     'message': '✅ Confirmed: SI=95%'
#   },
#   'trust': {
#     'trust_level': 'trusted',
#     'is_trusted': True
#   },
#   'sync_decision': {
#     'should_sync': True,
#     'sync_direction': 'bidirectional',
#     'post_sync_actions': ['refresh_dna_particles', 'update_habit_baseline', ...]
#   }
# }

# 根據結果授予設備訪問權限
if result['identification']['verified']:
    device_record = identifier.grant_device_access(device_id, "full")

# 記錄同步操作
identifier.log_sync_operation(result)

# 查詢所有可信設備
trusted_devices = identifier.get_trusted_devices()
```

**設備註冊結構**:
```json
{
  "MacBook-M4-Max-UID9622": {
    "device_id": "MacBook-M4-Max-UID9622",
    "device_seal": "#DEVICE-SEAL-2026-05-30-XXXXX",
    "first_seen": "2026-05-30T05:30:00+08:00",
    "last_sync": "2026-05-30T05:35:00+08:00",
    "trust_level": "trusted",
    "si_history": [0.95, 0.97, 0.92],
    "sync_count": 3
  }
}
```

---

## 🔄 完整工作流程

### 場景: 諸葛鑫在新設備上USB連接恢復身份

```
1. USB 插入新設備
   └─ CrossDeviceIdentifier.load_baseline_from_usb()
      └─ 加載: ~/龍魂_備份/habit_fingerprints/baseline_snapshot.json

2. 掃描本地操作記錄
   └─ identifier.scan_local_operations()
      └─ 讀取最近100條本地操作

3. 運行 F8 習慣匹配引擎
   └─ HabitFingerprintManager.compute_habit_match()
      └─ SI = 0.95 (95% 匹配度)

4. 驗證結果
   └─ SI >= 0.85?
      ├─ ✅ YES → 確認: 這是諸葛鑫
      └─ 🟡 NO (0.70-0.85) → 待審·需人工確認

5. 設備信任檢查
   └─ CrossDeviceIdentifier.verify_device_trust()
      ├─ 新設備 + SI >= 0.85? → "trusted"
      └─ 已知設備 + SI >= 0.75? → "trusted"

6. 自動同步決策
   └─ CrossDeviceIdentifier.auto_sync_decision()
      ├─ SI >= 0.85 + trusted → 雙向同步 (overwrite)
      ├─ SI >= 0.85 + pending → 單向讀取 (merge)
      └─ SI < 0.70 → 拒絕·等待人工確認

7. 執行同步
   ├─ refresh_dna_particles (從USB複製)
   ├─ update_habit_baseline (更新本地基線)
   ├─ log_sync_operation (記錄同步操作)
   └─ grant_device_access (授予設備權限)

8. 完成
   └─ ✅ ~/.龍魂/ 完整恢復
      └─ 所有操作日記·DNA粒子·習慣基線全部可用
```

---

## 💻 使用示例 (集成四引擎)

### 例 1: 記錄新操作並生成DNA

```python
from operation_log_engine import (
    OperationLedger,
    DNAParticleGenerator
)

# 步驟1: 操作發生 → 追加到日記
ledger = OperationLedger()
op_record = ledger.append_operation(
    operation_type="工程",
    operation_name="L5-F8-implementation",
    device_id="MacBook-M4-Max-UID9622",
    agent_type="Claude Haiku 4.5",
    input_text="嘿嘿,,,帮我设计操作日记,,,我想同步本地",
    output_text="收到! 這是跨設備身份識別系統... 習慣會說話·DNA會認人",
    notes="核心操作·F8引擎啟動·焊死"
)

# 步驟2: 自動生成DNA粒子
gen = DNAParticleGenerator()
dna_particle = gen.generate_from_record(op_record)
dna_path = gen.save_particle(dna_particle)

print(f"✅ 操作已記錄: {op_record['operation_id']}")
print(f"✅ DNA粒子已生成: {dna_path}")
print(f"   DNA簽章: {dna_particle['dna']}")
```

### 例 2: 建立習慣基線

```python
from operation_log_engine import (
    OperationLedger,
    HabitFingerprintManager
)

# 讀取所有歷史操作
ledger = OperationLedger()
historical_ops = ledger.get_last_n_operations(n=50)

# 建立習慣基線
manager = HabitFingerprintManager()
baseline = manager.establish_baseline(historical_ops)
manager.save_baseline(baseline)

print(f"✅ 習慣基線建立完成")
print(f"   拼音錯別字: {list(baseline['typos'].keys())}")
print(f"   口頭禪: {list(baseline['catchphrases'].keys())}")
print(f"   信心度 (SI): {baseline['confidence_metrics']['overall_si']:.2%}")
```

### 例 3: 完整跨設備認人

```python
from operation_log_engine import (
    OperationLedger,
    HabitFingerprintManager,
    CrossDeviceIdentifier
)

# 從USB恢復基線
identifier = CrossDeviceIdentifier()
baseline = identifier.load_baseline_from_usb("/media/usb-drive")

# 掃描本地操作
local_ops = identifier.scan_local_operations(limit=100)

# 完整識別流程
result = identifier.identify_user(baseline, local_ops)

print(f"\n🌐 跨設備識別結果:")
print(f"   {result['identification']['message']}")
print(f"   SI分數: {result['identification']['si_score']:.2%}")
print(f"   信任等級: {result['trust']['trust_level']}")
print(f"   同步方向: {result['sync_decision']['sync_direction']}")

# 如果驗證通過 → 授予訪問權限
if result['identification']['verified']:
    device_record = identifier.grant_device_access(
        result['device_id'],
        access_level="full"
    )
    identifier.log_sync_operation(result)
    print(f"\n✅ 設備已授權·自動同步開始...")
```

---

## 🔧 配置與部署

### 目錄結構
```
~/.龍魂/
├── 操作日記/
│   ├── operation_ledger.jsonl          # 主日記文件
│   ├── dna_particles/
│   │   └── OP-*.dna.json               # DNA粒子庫
│   ├── habit_fingerprints/
│   │   ├── baseline_snapshot.json      # 習慣基線
│   │   ├── pinyin_typos.json
│   │   ├── catchphrases.json
│   │   ├── polyphonic_prefs.json
│   │   └── wuxing_profile.json
│   └── device_trust/
│       ├── device_registry.json        # 設備信任列表
│       └── sync_operations.jsonl       # 同步日誌
└── 草日誌.md                             # 工程進度記錄
```

### 初始化
```python
from operation_log_engine import OperationLedger

# 首次初始化·自動創建所有目錄
ledger = OperationLedger()
# 結果: ~/.龍魂/操作日記/{dna_particles,habit_fingerprints,device_trust}/ 全部創建
```

---

## ✅ Phase 2.1 驗收標準

- [x] **operation_ledger.py** - append-only JSONL + SHA-256鏈 + 習慣提取
- [x] **dna_particle_generator.py** - 10字段DNA粒子 + 三色評判
- [x] **habit_fingerprint_manager.py** - F8習慣提取 + SI信心度計算
- [x] **cross_device_identifier.py** - 完整識別流程 + 設備信任 + 自動同步
- [x] **包結構完整** - `__init__.py` + imports + 可直接 `from operation_log_engine import *`
- [x] **CLI示例** - 每個模組都有完整的 `if __name__ == "__main__"` 演示

---

## 🎯 Phase 2.2-3 預期 (06-04~06-07)

| 週期 | 任務 | 優先級 | 預期完成 |
|------|------|--------|---------|
| 06-04~06-05 | 本地同步實現 (衝突檢測) | P1 | USB sync + merge strategy |
| 06-06~06-07 | 多簽門整合 (本地驗證) | P1 | 3/3 multisig + device seal |
| 06-08~06-15 | 儀表板 (可視化查詢) | P2 | Web UI 或 CLI 查詢工具 |

---

## 📍 DNA鏈路

**父 DNA** (Phase 1):
```
#龍芯⚡️2026-05-30-IRON-QC-QUAD-ACTIVATION-v1.0
```

**本 DNA** (Phase 2.1):
```
#龍芯⚡️2026-05-30-OPERATION-LOG-ENGINE-v1.0
```

**下一 DNA** (Phase 2.2):
```
#龍芯⚡️2026-06-07-PHASE-2-COMPLETE-L5-L4-INTEGRATION-v1.0
```

---

**責任**: UID9622·不免責
**時間戳**: 2026-05-30 05:55 CST
**驗收**: ✅ Phase 2.1 完全就緒

