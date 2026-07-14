<!--
  龍魂·六层来源链 / LongHun Six-Layer Source Chain
  1 道统层 Dao           : 曾仕强老师
  2 精神层 Spirit        : Steve Jobs
  3 设备层 Device        : Apple
  4 技术层 Technology    : Open Source
  5 系统层 System        : UID9622
  6 生命层 Life          : CNSH · LongHun (诸葛鑫 / 龍芯北辰)
  DNA追溯码:#龍芯⚡️2026-06-02-CNSH-SOVEREIGN-PUBLISH-METADATA-FILE1282-v2.0
  铁律: 来源不可删 · 影响不可覆 · 贡献不可抹 (rule_01 来源必标)
  文件: IMPLEMENTATION_GUIDE.md | 标记时间: 2026-06-03T07:46:12+0800
-->
# 🧬 龍魂操作日记系统 · Phase 2.1 实现指南

**DNA**: `#龍芯⚡️2026-05-30-OPERATION-LOG-ENGINE-v1.0`
**责任**: UID9622·不免责
**日期**: 2026-05-30 (卯时末·火时)

---

## 📋 核心架构 (四引擎系统)

### 1️⃣ OperationLedger (操作日记)
**文件**: `core/operation_ledger.py`

**功能**:
- append-only JSONL 日记 (每次操作一条·不可修改)
- SHA-256 parent-hash 链式验证 (无断裂)
- 自动习惯提取 (拼音错别字、口头禅、逗号习惯)
- 时辰 + 数字根计算

**核心方法**:
```python
ledger = OperationLedger()

# 追加操作到日记
record = ledger.append_operation(
    operation_type="工程",
    operation_name="L5-F8-implementation",
    device_id="MacBook-M4-Max-UID9622",
    agent_type="Claude Haiku 4.5",
    input_text="嘿嘿,,,帮我设计操作日记",
    output_text="收到! 这是跨设备身份识别系统...",
    rules_triggered=["§9.27", "§11.2"],
    persona_active="P02",
    persona_weight=0.50,
    notes="核心操作·F8引擎启动"
)

# 验证链完整性
ledger.verify_chain_integrity()  # True if no breaks

# 获取统计
stats = ledger.get_stats()  # {total_operations, average_habit_match, device_count}
```

**存储结构**:
```
~/.龍魂/操作日记/
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
- 从操作记录生成 DNA 粒子 (身份证)
- 10 字段决策收据格式
- 三色评判 (🟢🟡🔴)
- 粒子验证 + 证明导出

**核心方法**:
```python
gen = DNAParticleGenerator()

# 从操作记录生成 DNA 粒子
dna_particle = gen.generate_from_record(operation_record)

# 保存粒子
file_path = gen.save_particle(dna_particle)
# 结果: ~/.龍魂/operattion_日记/dna_particles/OP-*.dna.json

# 加载粒子
particle = gen.load_particle("OP-20260530-053000-abc123")

# 验证粒子哈希
is_valid = gen.verify_particle_hash("OP-20260530-053000-abc123")

# 导出粒子作为证明 (含十字段摘要)
proof = gen.export_particle_proof("OP-20260530-053000-abc123")
```

**DNA粒子结构** (10字段):
```json
{
  "identity": {
    "uid": "UID9622",
    "gpg_prefix": "A2D0092CEE2E5BA87035600924C3704A8CC26D5F",
    "device_id": "MacBook-M4-Max-UID9622"
  },
  "temporal_anchor": {
    "iso8601": "2026-05-30T05:30:00+08:00",
    "shichen": "卯时末",
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
  "dna": "#龍芯⚡️2026-05-30-OP-_-L5-F8_A334-v1.0",
  "hash": "sha256_hash_value",
  "parent_hash": "previous_operation_hash",
  "ten_fields": {
    "summary": "工程-L5-F8-implementation",
    "path": "OP-20260530-053000-abc123",
    "route": "P02",
    "weight": 0.50,
    "risk_color": "🟢",
    "rules": "§9.27,§11.2",
    "three_color": "🟢 通过",
    "bias_source": "龍魂文化向量(道德经)",
    "vendor_policy": "Notion AI default security",
    "dna_trace": "#龍芯⚡️2026-05-30-OP-_-L5-F8_A334-v1.0"
  }
}
```

---

### 3️⃣ HabitFingerprintManager (习惯指纹)
**文件**: `core/habit_fingerprint_manager.py`

**功能**:
- F8 习惯不动点提取 (拼音错别字、口头禅、多音字偏好)
- 基线建立 (baseline_snapshot)
- 习惯匹配度计算 (SI 信心度)
- 跨设备身份验证

**核心方法**:
```python
manager = HabitFingerprintManager()

# 从操作记录建立习惯基线
baseline = manager.establish_baseline(operation_records)
manager.save_baseline(baseline)

# 提取新文本的习惯特征
habits = manager.extract_habit_features("嘿嘿,,,帮我做个新功能")

# 计算新文本与基线的匹配度
overall_si, match_scores = manager.compute_habit_match("嘿嘿,,,帮我设计...")

# 验证身份 (自动判决: 通过/待审/失败)
is_verified, message, si = manager.verify_identity(new_text, threshold=0.85)
# 返回: (True, "✅ Confirmed (SI=95%)", 0.95)
```

**习惯基线结构**:
```json
{
  "typos": {
    "得/的": 0.35,
    "哪/那": 0.15
  },
  "catchphrases": {
    "嘿嘿": 0.92,
    "焊死": 0.78,
    "宝宝": 0.65,
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

**SI 信心度判决**:
- `SI >= 0.85` → ✅ 确认身份 (自动通过)
- `SI 0.70-0.85` → 🟡 身份待审 (需人工确认)
- `SI < 0.70` → 🔴 身份验证失败 (拒绝访问)

---

### 4️⃣ CrossDeviceIdentifier (跨设备识别)
**文件**: `core/cross_device_identifier.py`

**功能**:
- F8 习惯引擎整合
- 设备信任管理 + 设备封印
- 自动同步决策
- 完整的跨设备认人流程

**核心方法**:
```python
identifier = CrossDeviceIdentifier()

# 从USB加载习惯基线
baseline = identifier.load_baseline_from_usb("/media/usb-drive")

# 扫描本地操作记录
local_ops = identifier.scan_local_operations(limit=100)

# 获取当前设备ID
device_id = identifier.get_device_id()  # MacBook-M4-Max-UID9622

# 完整识别流程 (一个方法搞定)
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

# 根据结果授予设备访问权限
if result['identification']['verified']:
    device_record = identifier.grant_device_access(device_id, "full")

# 记录同步操作
identifier.log_sync_operation(result)

# 查询所有可信设备
trusted_devices = identifier.get_trusted_devices()
```

**设备注册结构**:
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

### 场景: 诸葛鑫在新设备上USB连接恢复身份

```
1. USB 插入新设备
   └─ CrossDeviceIdentifier.load_baseline_from_usb()
      └─ 加载: ~/龍魂_备份/habit_fingerprints/baseline_snapshot.json

2. 扫描本地操作记录
   └─ identifier.scan_local_operations()
      └─ 读取最近100条本地操作

3. 运行 F8 习惯匹配引擎
   └─ HabitFingerprintManager.compute_habit_match()
      └─ SI = 0.95 (95% 匹配度)

4. 验证结果
   └─ SI >= 0.85?
      ├─ ✅ YES → 确认: 这是诸葛鑫
      └─ 🟡 NO (0.70-0.85) → 待审·需人工确认

5. 设备信任检查
   └─ CrossDeviceIdentifier.verify_device_trust()
      ├─ 新设备 + SI >= 0.85? → "trusted"
      └─ 已知设备 + SI >= 0.75? → "trusted"

6. 自动同步决策
   └─ CrossDeviceIdentifier.auto_sync_decision()
      ├─ SI >= 0.85 + trusted → 双向同步 (overwrite)
      ├─ SI >= 0.85 + pending → 单向读取 (merge)
      └─ SI < 0.70 → 拒绝·等待人工确认

7. 执行同步
   ├─ refresh_dna_particles (从USB复制)
   ├─ update_habit_baseline (更新本地基线)
   ├─ log_sync_operation (记录同步操作)
   └─ grant_device_access (授予设备权限)

8. 完成
   └─ ✅ ~/.龍魂/ 完整恢复
      └─ 所有操作日记·DNA粒子·习惯基线全部可用
```

---

## 💻 使用示例 (集成四引擎)

### 例 1: 记录新操作并生成DNA

```python
from operation_log_engine import (
    OperationLedger,
    DNAParticleGenerator
)

# 步骤1: 操作发生 → 追加到日记
ledger = OperationLedger()
op_record = ledger.append_operation(
    operation_type="工程",
    operation_name="L5-F8-implementation",
    device_id="MacBook-M4-Max-UID9622",
    agent_type="Claude Haiku 4.5",
    input_text="嘿嘿,,,帮我设计操作日记,,,我想同步本地",
    output_text="收到! 这是跨设备身份识别系统... 习惯会说话·DNA会认人",
    notes="核心操作·F8引擎启动·焊死"
)

# 步骤2: 自动生成DNA粒子
gen = DNAParticleGenerator()
dna_particle = gen.generate_from_record(op_record)
dna_path = gen.save_particle(dna_particle)

print(f"✅ 操作已记录: {op_record['operation_id']}")
print(f"✅ DNA粒子已生成: {dna_path}")
print(f"   DNA签章: {dna_particle['dna']}")
```

### 例 2: 建立习惯基线

```python
from operation_log_engine import (
    OperationLedger,
    HabitFingerprintManager
)

# 读取所有历史操作
ledger = OperationLedger()
historical_ops = ledger.get_last_n_operations(n=50)

# 建立习惯基线
manager = HabitFingerprintManager()
baseline = manager.establish_baseline(historical_ops)
manager.save_baseline(baseline)

print(f"✅ 习惯基线建立完成")
print(f"   拼音错别字: {list(baseline['typos'].keys())}")
print(f"   口头禅: {list(baseline['catchphrases'].keys())}")
print(f"   信心度 (SI): {baseline['confidence_metrics']['overall_si']:.2%}")
```

### 例 3: 完整跨设备认人

```python
from operation_log_engine import (
    OperationLedger,
    HabitFingerprintManager,
    CrossDeviceIdentifier
)

# 从USB恢复基线
identifier = CrossDeviceIdentifier()
baseline = identifier.load_baseline_from_usb("/media/usb-drive")

# 扫描本地操作
local_ops = identifier.scan_local_operations(limit=100)

# 完整识别流程
result = identifier.identify_user(baseline, local_ops)

print(f"\n🌐 跨设备识别结果:")
print(f"   {result['identification']['message']}")
print(f"   SI分数: {result['identification']['si_score']:.2%}")
print(f"   信任等级: {result['trust']['trust_level']}")
print(f"   同步方向: {result['sync_decision']['sync_direction']}")

# 如果验证通过 → 授予访问权限
if result['identification']['verified']:
    device_record = identifier.grant_device_access(
        result['device_id'],
        access_level="full"
    )
    identifier.log_sync_operation(result)
    print(f"\n✅ 设备已授权·自动同步开始...")
```

---

## 🔧 配置与部署

### 目录结构
```
~/.龍魂/
├── 操作日记/
│   ├── operation_ledger.jsonl          # 主日记文件
│   ├── dna_particles/
│   │   └── OP-*.dna.json               # DNA粒子库
│   ├── habit_fingerprints/
│   │   ├── baseline_snapshot.json      # 习惯基线
│   │   ├── pinyin_typos.json
│   │   ├── catchphrases.json
│   │   ├── polyphonic_prefs.json
│   │   └── wuxing_profile.json
│   └── device_trust/
│       ├── device_registry.json        # 设备信任列表
│       └── sync_operations.jsonl       # 同步日志
└── 草日志.md                             # 工程进度记录
```

### 初始化
```python
from operation_log_engine import OperationLedger

# 首次初始化·自动创建所有目录
ledger = OperationLedger()
# 结果: ~/.龍魂/操作日记/{dna_particles,habit_fingerprints,device_trust}/ 全部创建
```

---

## ✅ Phase 2.1 验收标准

- [x] **operation_ledger.py** - append-only JSONL + SHA-256链 + 习惯提取
- [x] **dna_particle_generator.py** - 10字段DNA粒子 + 三色评判
- [x] **habit_fingerprint_manager.py** - F8习惯提取 + SI信心度计算
- [x] **cross_device_identifier.py** - 完整识别流程 + 设备信任 + 自动同步
- [x] **包结构完整** - `__init__.py` + imports + 可直接 `from operation_log_engine import *`
- [x] **CLI示例** - 每个模组都有完整的 `if __name__ == "__main__"` 演示

---

## 🎯 Phase 2.2-3 预期 (06-04~06-07)

| 周期 | 任务 | 优先级 | 预期完成 |
|------|------|--------|---------|
| 06-04~06-05 | 本地同步实现 (冲突检测) | P1 | USB sync + merge strategy |
| 06-06~06-07 | 多签门整合 (本地验证) | P1 | 3/3 multisig + device seal |
| 06-08~06-15 | 仪表板 (可视化查询) | P2 | Web UI 或 CLI 查询工具 |

---

## 📍 DNA链路

**父 DNA** (Phase 1):
```#龍芯⚡️2026-05-30-IRON-QC-QUAD-ACTIVATION_A23B-v1.0
```

**本 DNA** (Phase 2.1):
```#龍芯⚡️2026-05-30-OPERATION-LOG-ENGINE_BE54-v1.0
```

**下一 DNA** (Phase 2.2):
```#龍芯⚡️2026-06-07-PHASE-2-COMPLETE-L5-L4-INTEGRATION_3394-v1.0
```

---

**责任**: UID9622·不免责
**时间戳**: 2026-05-30 05:55 CST
**验收**: ✅ Phase 2.1 完全就绪

