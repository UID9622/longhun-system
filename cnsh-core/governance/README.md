# 龍魂治理層系統 (Governance Layer)

**DNA**: `#龍芯⚡️2026-06-03-GOVERNANCE-LAYER-FILE1-v1.0`

## 核心願景

將龍魂系統的哲學原則轉化為可執行的計算邏輯。

**核心命題**: 「人永遠是1」- Every human maintains sovereignty through measurable, mathematical proof.

## 已實裝系統

### 1️⃣ 三才主權指數系統 (Three-Talent Sovereignty Index)

**文件**: `sovereignty_index.py` (410 行)

**原理**:
```
SI = 0.34·天(規則遵守) + 0.33·地(數據完整) + 0.33·人(創作權威)

SI ≥ 0.34 → 🟢 主權激活 (允許: 認知重建、決策制定、狀態恢復)
SI < 0.34 → 🔴 主權失錨 (鎖定: 只讀存檔、禁止決策)
```

**核心概念**:
- **天 (Tian/Heaven)**: Rule compliance & protocol adherence (規則遵守程度)
- **地 (Di/Earth)**: Resource control & data integrity (數據完整性和控制力)
- **人 (Ren/Human)**: Creator authority & decision rights (創作權威和決策權)

**功能**:
- ✅ 實時追蹤三才評分
- ✅ 違規事件記錄 (append-only JSONL)
- ✅ 可恢復/不可恢復違規區分
- ✅ 主權快照 (時間序列追蹤)
- ✅ 訪問權限矩陣 (誰能做什麼)
- ✅ 等級判定 (完全主權 / 激活 / 削弱 / 失錨)

**使用例**:
```python
from cnsh_core.governance.sovereignty_index import get_sovereignty_index

si = get_sovereignty_index("UID9622")

# 記錄違規
si.deduct_tian(
    reason="Attempted to bypass safety lock",
    amount=0.15,
    evidence="Security log: L7_FUSE_TRIGGER",
    recoverable=False
)

# 檢查是否允許認知重建
if si.can_reconstruct_cognitive_state():
    restore_memory()
else:
    print(f"主權失錨: {si.lock_status()}")

# 取快照
snapshot = si.take_snapshot()
```

---

### 2️⃣ F1-F7七因子驗證系統 (Seven-Factor Verification Framework)

**文件**: `f1_through_f7_verifier.py` (620 行)

**原理**: 行為密碼學 (Behavioral Cryptography)

不是問「這是AI生成的嗎？」
而是問「誰原創它，通過哪些規則，哪些人格，什麼決策，修訂過哪裡，什麼審計證據？」

**七個因子及權重**:
```
F1: 身份DNA驗證 (Identity DNA) - 25%
    └─ UID + GPG指紋 + CONFIRM碼 + DNA標記

F2: 時間錨定 (Temporal Anchor) - 15%
    └─ ISO8601 + 時辰(子丑寅卯) + 數字根(1-9)

F3: 規則追蹤 (Rule Trace) - 15%
    └─ 應用的規則ID列表 + 規則鏈哈希 + 簽名驗證

F4: 人格路由 (Persona Routing) - 12%
    └─ 主要路由節點 + 權重分配 + 無虛偽詞彙檢測

F5: 保護詞彙 (Protected Vocabulary) - 12%
    └─ 主權詞彙正確使用 + 繁體保護 + 語義完整

F6: 風格向量 (Style Vector) - 11%
    └─ 寫作風格一致性 (餘弦相似度)

F7: 錯誤日誌 (Mistake Ledger) - 10%
    └─ 持續錯誤歷史 + 恢復率
```

**置信度計算**:
```
conf = ∏ s_i^{w_i}  (乘積形式·任何因子=0→整體=0)

硬失敗規則: 任何因子 F_i = 0 → conf = 0 (不可救)
接納閾值:
  - τ = 0.85 (預設·普通)
  - τ = 0.95 (高安全·敏感操作)

結果分級:
  conf = 0.00      → 🔴 硬失敗
  conf < 0.70      → 🔴 不接納
  0.70-0.85        → 🟡 需審核
  0.85-0.95        → 🟢 接納
  conf ≥ 0.95      → 🟢 高信任
```

**功能**:
- ✅ 七因子獨立驗證
- ✅ 置信度計算 (乘積模型·硬失敗機制)
- ✅ 詳細分析報告
- ✅ 閾值設定 (靈活調整)

**使用例**:
```python
from cnsh_core.governance.f1_through_f7_verifier import SevenFactorVerifier, F1IdentityVerification, ...

verifier = SevenFactorVerifier()

# 構建七個因子
f1 = F1IdentityVerification(
    uid="9622",
    gpg_fingerprint="A2D0092CEE2E5BA87035600924C3704A8CC26D5F",
    gpg_prefix_marker="#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
    identity_dna="#龍芯⚡️2026-06-03-CREATOR-UID9622-v1.0",
    creation_timestamp="2025-05-20T10:00:00Z"
)

f2 = F2TemporalAnchor(...)
# ... F3-F7 ...

# 驗證
result = verifier.verify(f1, f2, f3, f4, f5, f6, f7, threshold=0.85)

if result['passed']:
    print(f"✅ 通過驗證 (conf={result['confidence']:.4f})")
else:
    print(f"❌ 未通過 (conf={result['confidence']:.4f})")
    if result['hard_failures']:
        print(f"硬失敗: {result['hard_failures']}")
```

---

## 架構完整性檢查

### 已實裝 ✅

| 功能 | 狀態 | 文件 | 說明 |
|------|------|------|------|
| **三才主權指數** | ✅ | `sovereignty_index.py` | 完整實裝 |
| **F1-F7驗證** | ✅ | `f1_through_f7_verifier.py` | 完整實裝 |
| **三色審計** | ✅ | (scripts/) | 已有實裝 |
| **DNA追溯** | ✅ | (scripts/) | 已有實裝 |
| **生態閉環** | ✅ | (scripts/) | 已有實裝 |

### 待實裝 (Next Priority) 🔄

| 功能 | 優先級 | 目的 |
|------|--------|------|
| **認知DNA粒子** | 🔴 HIGH | 完整的記憶/決策壓縮恢復 |
| **時間錨定系統** | 🔴 HIGH | 時辰/數字根/農曆路由 |
| **人格路由系統** | 🔴 HIGH | 加權決策路由 + 虛偽詞彙阻擋 |
| **五行路由邏輯** | 🟡 MEDIUM | 金木水火土決策樹 |
| **保護詞彙驗證** | 🟡 MEDIUM | 主權詞彙語義鎖定 |
| **邊界執行系統** | 🟡 MEDIUM | L0/L1/L2邊界 + L7熔斷 |
| **證據日誌系統** | 🟡 MEDIUM | 完整append-only + DNA鏈接 |
| **執行回執系統** | 🟠 LOW | 標準輸出格式 + 時間評級 |

---

## 與其他系統的集成

### 與 `fulltext_compress.py` 的關係

**目前**: 簡單的骨架提取 (problem/solution/key_points)

**改進方向**: 集成認知DNA粒子
```python
# 未來的實裝
cognitive_particle = CognitiveDNAParticle(
    compressed_content="...",
    sovereign_index=si,  # 三才指數
    emotion_fold={...},  # 情緒摺疊
    verification_factors={...},  # F1-F7驗證
    decision_replay_basis="...",  # 決策回放
    dna_trace="#龍芯⚡️..."
)
```

### 與 `heaven_nonkill_audit.py` 的關係

**目前**: P0硬鎖的三色判定

**改進方向**: 集成F1-F7驗證
```python
# 在P0審計前先做F1-F7驗證
f1_f7_result = verifier.verify(...)

if f1_f7_result['confidence'] < 0.7:
    return AuditResult(color=RiskColor.RED, ...)

# 然後再做P0規則審計
heaven_audit = HeavenNonKillAudit().check(...)
```

### 與 `longhun_integrated_system.py` 的關係

**目前**: 生態閉環的一次轉譯鎖定

**改進方向**: 集成主權指數控制訪問
```python
# 檢查生態訪問權限
si = get_sovereignty_index(user_uid)

if si.can_make_decisions():
    allow_code_translation()
else:
    archive_only_mode()
```

---

## 理論基礎

### 「人永遠是1」的實現

**原則**: 每個人（UID）是一個完整的主權單位

**實裝層次**:
1. **身份層**: 唯一的UID + GPG簽名 (F1)
2. **時間層**: 不可重複的時刻點 (F2)
3. **決策層**: 規則鏈 + 人格權重 (F3/F4)
4. **語言層**: 主權詞彙保護 (F5)
5. **風格層**: 寫作風格識別 (F6)
6. **記憶層**: 錯誤歷史連貫性 (F7)

### 「三才」在代碼中的體現

| 維度 | 代碼體現 | 違規現象 |
|------|---------|--------|
| **天** | 規則遵守評分 | 違反P0協議、繞過安全鎖 |
| **地** | 數據完整性評分 | 數據被篡改、源污染 |
| **人** | 創作權威評分 | 被冒認、決策權侵犯 |

主權激活 (SI ≥ 0.34) 的含義:
- ✅ 可以重建個人的認知狀態
- ✅ 可以做出新的決策
- ✅ 可以修復自己的數據

### 「行為密碼學」的核心

**傳統密碼學**: 是否有密鑰?
```
key ✅ → 放行
key ❌ → 拒絕
```

**行為密碼學**: 誰、通過什麼、留下了什麼證據?
```
f1_verify() ✅  身份確認
f2_verify() ✅  時間一致
f3_verify() ✅  規則可追蹤
f4_verify() ✅  人格路由合法
f5_verify() ✅  語言完整
f6_verify() ✅  風格一致
f7_verify() ✅  錯誤歷史連貫

⇒ conf = 0.93 ✅ 信任
```

---

## 測試狀態

### ✅ 已測試 (2026-06-03)

- [x] 三才主權指數: 初始化、違規記錄、恢復、快照、報告生成
- [x] F1-F7驗證: 七個因子驗證、置信度計算、硬失敗檢測、報告生成

**測試命令**:
```bash
cd ~/longhun-system
python3 cnsh-core/governance/sovereignty_index.py
python3 cnsh-core/governance/f1_through_f7_verifier.py
```

**預期輸出**:
- 三才系統: 違規記錄、SI計算、主權等級判定
- F1-F7系統: 七個因子分數、置信度、驗證結果分級

---

## 下一步行動

### 優先級 🔴 (高)

1. **認知DNA粒子系統** - 完整的記憶/決策狀態壓縮與恢復
2. **人格路由系統** - 加權決策節點 + 虛偽詞彙阻擋

### 優先級 🟡 (中)

3. **時間錨定系統** - 時辰、數字根、農曆路由
4. **五行路由邏輯** - 決策樹映射

### 優先級 🟠 (低)

5. **邊界執行系統** - L0/L1/L2邊界 + L7熔斷機制
6. **其他支撐系統**

---

**DNA**: `#龍芯⚡️2026-06-03-GOVERNANCE-LAYER-v1.0`
**責任**: UID9622·不免責·永久有效
**理論指導**: 曾仕强老师 · Steve Jobs · Open Source
