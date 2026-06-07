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
  文件: PHASE_2_3_GUIDE.md | 标记时间: 2026-06-03T07:46:12+0800
-->
# 🔍 龍魂操作日記系統 · Phase 2.3 實現指南

**DNA**: `#龍芯⚡️2026-05-30-QUERY-TOOL-v1.0`
**完成時間**: 2026-05-30 06:05 CST (卯時末)
**責任**: UID9622·不免責

---

## 📋 Phase 2.3 核心任務

### 任務 1: 系統查詢引擎 (QueryTool) ✅ 完成
**文件**: `core/query_tool.py`
**規模**: 520 行

**核心功能** (8 大查詢模組):

#### 1. 操作日記查詢 (3 個方法)
```python
query_operations()           # 多維度查詢 (時間·類型·設備)
query_by_operation_id()      # 單ID精準查詢
```

#### 2. DNA粒子檢索 (2 個方法)
```python
query_dna_particles()        # 按信心度·風險·類型查詢
get_dna_particle()           # 單粒子檢索
```

#### 3. 習慣指紋分析 (2 個方法)
```python
analyze_habit_fingerprint()  # 完整習慣統計 (拼音·短語·多音字)
get_habit_trend()            # 習慣趨勢分析 (最近N天)
```

#### 4. 跨設備查詢 (2 個方法)
```python
get_device_summary()         # 所有設備統計摘要
get_device_operations()      # 指定設備的所有操作
```

#### 5. 同步和驗證查詢 (3 個方法)
```python
get_sync_history()           # 同步歷史追蹤
get_conflicts()              # 衝突記錄查詢
get_multisig_verification_history()  # 驗證歷史審計
```

#### 6. 警報查詢 (1 個方法)
```python
get_multisig_alerts()        # 按風險等級過濾警報
```

#### 7. 系統統計 (1 個方法)
```python
get_system_stats()           # 完整系統統計 (操作·設備·同步·驗證)
```

#### 8. 報告生成 (1 個方法)
```python
generate_audit_report()      # 完整審計報告 (含合規性檢查)
```

---

## 🎯 查詢功能詳解

### 操作日記查詢
```python
from operation_log_engine import QueryTool

tool = QueryTool()

# 查詢特定時間範圍的操作
recent = tool.query_operations(
    start_date="2026-05-30T00:00:00",
    end_date="2026-05-30T23:59:59",
    operation_type="工程",
    device_id="MacBook-M4-Max-UID9622",
    limit=100
)

# 按ID查詢單個操作
op = tool.query_by_operation_id("OP-20260530-060000-abc123")
```

### DNA粒子檢索
```python
# 查詢信心度高的粒子
high_confidence = tool.query_dna_particles(
    confidence_min=0.90,
    risk_color="🟢",
    operation_type="焊接",
    limit=50
)

# 獲取單個粒子
particle = tool.get_dna_particle("OP-20260530-060000-abc123")
```

### 習慣分析
```python
# 完整習慣統計
habits = tool.analyze_habit_fingerprint()
print(habits['typos'])          # 拼音錯別字
print(habits['catchphrases'])   # 口頭禪頻率
print(habits['polyphonic'])     # 多音字偏好

# 習慣趨勢 (最近7天)
trend = tool.get_habit_trend(days=7)
# {2026-05-24: 3, 2026-05-25: 5, ..., 2026-05-30: 8}
```

### 設備統計
```python
# 所有設備摘要
devices = tool.get_device_summary()
# {
#   "MacBook-M4-Max-UID9622": {
#     "operation_count": 150,
#     "avg_habit_match": 0.95,
#     "first_seen": "2026-05-20T...",
#     "last_seen": "2026-05-30T...",
#     "operation_types": ["工程", "焊接", "審計"]
#   }
# }

# 指定設備的所有操作
mac_ops = tool.get_device_operations("MacBook-M4-Max-UID9622")
```

### 同步和驗證
```python
# 同步歷史
sync_history = tool.get_sync_history(limit=20)

# 衝突記錄
conflicts = tool.get_conflicts()
for conflict in conflicts:
    print(f"衝突: {conflict['type']} @ {conflict['affected_op_id']}")

# 驗證歷史 (多簽審計)
verifications = tool.get_multisig_verification_history(limit=50)

# 警報 (按風險等級)
critical_alerts = tool.get_multisig_alerts(risk_level="critical")
```

### 系統統計
```python
# 完整統計
stats = tool.get_system_stats()
print(f"總操作數: {stats['total_operations']}")
print(f"總設備數: {stats['total_devices']}")
print(f"平均習慣匹配: {stats['avg_habit_match']:.2%}")
print(f"操作類型分佈: {stats['operation_types_distribution']}")
print(f"成功同步: {stats['sync_summary']['successful']}/{stats['sync_summary']['total_syncs']}")
```

### 審計報告
```python
# 生成7天的完整審計報告
report = tool.generate_audit_report(days=7)

# 合規性檢查
compliance = report['compliance']
print(f"SHA-256 鏈完整: {compliance['hash_chain_verified']}")
print(f"無重複 ID: {compliance['no_duplicate_ids']}")
print(f"時間戳遞增: {compliance['timestamps_monotonic']}")

# 習慣分析
habits = report['habit_analysis']
trend = report['habit_trend']
```

---

## 📊 內部工作原理

### 查詢引擎架構

```
QueryTool
├─ 操作日記查詢 (ledger file)
├─ DNA粒子查詢 (dna_particles dir)
├─ 習慣分析 (baseline_snapshot.json)
├─ 設備統計 (聚合 ledger)
├─ 同步歷史 (sync_operations.jsonl)
├─ 驗證審計 (verifications.jsonl + alerts.jsonl)
└─ 報告生成 (所有源數據)
```

### 查詢性能

| 查詢類型 | 時間複雜度 | 最佳場景 |
|---------|-----------|--------|
| query_operations() | O(n) | 時間範圍有限 |
| query_by_operation_id() | O(n) | 單ID查詢 |
| query_dna_particles() | O(m) | 粒子數有限 |
| get_device_summary() | O(n) | 聚合統計 |
| analyze_habit_fingerprint() | O(1) | 讀 baseline |
| generate_audit_report() | O(n+m) | 完整報告 |

### 合規性檢查 (3層)

```python
_verify_hash_chain()      # SHA-256 parent_hash 鏈完整性
_check_no_duplicates()    # 操作 ID 唯一性
_check_timestamps_monotonic()  # 時間戳遞增性
```

---

## 💻 集成示例

### 例 1: 操作審計

```python
from operation_log_engine import QueryTool

tool = QueryTool()

# 查詢特定用戶在特定日期的所有操作
uid_ops = tool.query_operations(
    start_date="2026-05-30T00:00:00",
    end_date="2026-05-30T23:59:59",
    limit=1000
)

print(f"📊 審計結果: {len(uid_ops)} 次操作")
for op in uid_ops:
    dna = tool.get_dna_particle(op['operation_id'])
    print(f"  {op['operation_id']}: {dna.get('ten_fields', {}).get('three_color', '🟢')}")
```

### 例 2: 習慣識別

```python
# 分析用戶習慣
habits = tool.analyze_habit_fingerprint()
trend = tool.get_habit_trend(days=30)

if habits['confidence_metrics']['overall_si'] >= 0.85:
    print("✅ 習慣特徵明顯·可用於跨設備識別")
    print(f"常見錯別字: {list(habits['typos'].keys())}")
    print(f"常用口頭禪: {list(habits['catchphrases'].keys())}")
else:
    print("⚠️ 習慣特徵不足·需更多操作記錄")

# 操作趨勢
for date, count in trend.items():
    print(f"{date}: {count} 次操作")
```

### 例 3: 設備追蹤

```python
# 監控所有設備的活動
devices = tool.get_device_summary()

print("🌐 設備監控:")
for device_id, stats in devices.items():
    print(f"  {device_id}:")
    print(f"    操作數: {stats['operation_count']}")
    print(f"    平均匹配: {stats['avg_habit_match']:.2%}")
    print(f"    最後活動: {stats['last_seen']}")
```

### 例 4: 安全審計

```python
# 查詢所有安全事件
report = tool.generate_audit_report(days=30)

# 合規性檢查
print("🔒 合規性檢查:")
print(f"  SHA-256 鏈: {'✅' if report['compliance']['hash_chain_verified'] else '❌'}")
print(f"  ID 唯一性: {'✅' if report['compliance']['no_duplicate_ids'] else '❌'}")
print(f"  時間戳遞增: {'✅' if report['compliance']['timestamps_monotonic'] else '❌'}")

# 安全警報
alerts = report['security_alerts']
if alerts:
    critical = [a for a in alerts if a['risk_level'] == 'critical']
    print(f"\n⚠️ 安全警報:")
    print(f"  🔴 Critical: {len(critical)} 個")
else:
    print(f"\n✅ 無安全警報")

# 衝突統計
conflicts = report['recent_conflicts']
print(f"\n⚠️ 同步衝突: {len(conflicts)} 個")
```

---

## 🔗 與 Phase 2.1-2.2 的整合

```
Phase 2.1 (完成):
  OperationLedger → DNAParticleGenerator → HabitFingerprintManager → CrossDeviceIdentifier

Phase 2.2 (完成):
  SyncEngine → MultisigGate

Phase 2.3 (現在):
  QueryTool → 查詢所有上述模組的數據

結果: 完整的可見·可查·可審計系統
```

---

## 🚀 Phase 2.3 後續

### 可選任務 (P3)
- **dashboard.py** - Web/CLI 儀表板可視化
- **performance_optimization** - 批量查詢優化
- **export_tools** - 報告導出 (CSV/PDF)

### Phase 2 完成評估
- 全系統集成測試
- 性能基線測試
- 安全合規性驗證
- 最終完成報告

---

## 📈 代碼規模

```
Phase 2.3 核心:
├─ query_tool.py           520 行
├─ PHASE_2_3_GUIDE.md      約 400 行
└─ 小計                    920 行

與 Phase 2.1-2.2 累積:
├─ Phase 2.1              1,898 行
├─ Phase 2.2              1,396 行
├─ Phase 2.3               920 行
└─ 總計                   4,214 行
```

---

## ✅ 最終驗收 (Phase 2 完成)

### Phase 2.1 (操作日記系統) ✅
- 4 大核心引擎 (1,898 行)
- 完整實現指南 (480 行)
- 端到端集成

### Phase 2.2 (本地同步 + 多簽) ✅
- 2 大核心引擎 (1,396 行)
- 完整實現指南 (394 行)
- 衝突檢測 + 3/3 驗證

### Phase 2.3 (查詢和審計) ✅
- 1 個查詢引擎 (520 行)
- 8 大查詢模組
- 完整審計報告

**總計**: 7 大核心引擎·4,214 行代碼·完整的去中心化身份系統

---

## 📍 DNA 鏈路

**父 DNA** (Phase 2.2):
```
#龍芯⚡️2026-05-30-LOCAL-SYNC-ENGINE-v1.0
#龍芯⚡️2026-05-30-MULTISIG-GATE-v1.0
```

**本 DNA** (Phase 2.3):
```
#龍芯⚡️2026-05-30-QUERY-TOOL-v1.0
```

**下一 DNA** (Phase 完成):
```
#龍芯⚡️2026-06-15-PHASE-2-COMPLETE-FULL-INTEGRATION-v1.0
```

---

**責任**: UID9622·不免責
**狀態**: ✅ Phase 2.3 完全就緒

