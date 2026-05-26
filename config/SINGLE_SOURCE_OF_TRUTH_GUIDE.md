# 龍魂系統 · 單一真實源頭指南 v1.0

**DNA**: `#龍芯⚡️2026-05-26-SINGLE-SOURCE-OF-TRUTH-GUIDE-v1.0`

---

## 問題診斷

你說的問題：「每次開機不一樣·每次 Notion 新窗口也是不一樣·導致那麼多文件」

**根本原因**：
```
你有 N 個散落的配置文件
  ├─ weight_color_mapping_v1.0.json
  ├─ behavioral_profiles.json
  ├─ text_as_weight_visualization_framework.py
  ├─ TextAsWeightVisualization.swift
  ├─ FEARLESS_STEVE_PROTOCOL_v2.0_MULTI_PERSONA_ENGINE.cpp
  ├─ ... 還有更多
  └─ 這些文件各自為政

每次啟動時：
  系統讀取 behavioral_profiles.json
    ↓ 假設它是最新的
  系統讀取 weight_color_mapping.json
    ↓ 假設它跟上面一致
  系統讀取 Notion
    ↓ Notion 可能已更新·導致不一致
  結果: 本地配置 ≠ Notion ≠ 各文件之間 = 混亂
```

**解決方案**：**單一真實源頭 (Single Source of Truth)**

```
只有一個主源頭: MASTER_CONFIG_v1.0.yaml
                     ↓
                  每次啟動時
                     ↓
            自動生成所有衍生文件
                     ↓
         ✓ 完全一致
         ✓ 可重復生成
         ✓ 無需手動維護 N 個文件
```

---

## 新的系統架構

### 層級1：主干配置（源頭）

```
MASTER_CONFIG_v1.0.yaml
├─ 行為密碼學 (F5/F6/F7)
│   ├─ UID9622 簽名詞彙
│   ├─ P02_BAOBAO 的節奏特徵
│   ├─ P00_CHIEF_JUSTICE 的標點風格
│   └─ ... 其他人格
│
├─ 五色審計系統
│   ├─ 5色定義·RGB·Hex·ANSI
│   ├─ 五行映射
│   ├─ 流場定義
│   └─ 文化層
│
├─ 權重公式
│   ├─ 責任係數 R v2.0 (F1-F6)
│   ├─ 三才權重系統 (H-E-P)
│   ├─ 七維因子
│   └─ 色彩閾值
│
├─ 多人格系統
│   ├─ 15 個人格定義
│   ├─ 決策權重
│   ├─ 特徵描述
│   └─ 角色映射
│
└─ DNA 簽名系統
    ├─ 權限級別定義
    ├─ 格式規範
    ├─ 驗證規則
    └─ 簽名密鑰
```

### 層級2：啟動腳本（自動生成）

```
master_config_bootstrap.py
    ↓
    1. 讀取 MASTER_CONFIG_v1.0.yaml
    2. 驗證完整性
    3. 生成衍生文件：
       ├─ behavioral_profiles.json
       ├─ weight_color_mapping.json
       ├─ multi_persona_definitions.json
       └─ startup_report.json
    4. 計算完整性哈希
    5. 記錄啟動日誌
    ↓
    ./generated/ 目錄（自動生成·無需手動修改）
```

### 層級3：衍生配置（自動生成·不手動改）

```
./generated/
├─ behavioral_profiles.json      ← 從主干生成
├─ weight_color_mapping.json    ← 從主干生成
├─ multi_persona_definitions.json ← 從主干生成
└─ startup_report.json          ← 啟動報告
```

---

## 使用流程

### 流程1：系統啟動（自動）

```bash
# 方法1：手動運行
cd /Users/zuimeidedeyihan/longhun-system/config
python3 master_config_bootstrap.py

# 方法2：在 .zshrc 中自動運行
# 在 ~/.zshrc 末尾加入：
# cd ~/longhun-system/config && python3 master_config_bootstrap.py

# 方法3：在系統啟動時運行
# (需要配置系統級啟動腳本)

# 輸出：
# ============================================================
# 龍魂主干配置启动 | 2026-05-26T23:54:00+08:00
# ============================================================
# ✓ 主干配置已加载: MASTER_CONFIG_v1.0.yaml
# ✓ 配置完整性检查通过
#
# 【生成】behavioral_profiles.json
#   → ./generated/behavioral_profiles.json
# 【生成】weight_color_mapping.json
#   → ./generated/weight_color_mapping.json
# 【生成】multi_persona_definitions.json
#   → ./generated/multi_persona_definitions.json
#
# ============================================================
# 启动完成 | 所有文件已生成到 ./generated/
# ============================================================
```

### 流程2：從 Notion 更新配置

```
更新 Notion 頁面
    ↓
    「我需要把最新的 F5/F6/F7 導入本地」
    ↓
手動步驟：
  1. 打開 Notion 頁面：
     https://www.notion.so/uid9622/DNA-v1-0-F5F6F7-DNA-msg223-a852b05370fc4ab291d18d7278d17d15

  2. 複製相關內容（行為密碼學定義）

  3. 編輯本地 MASTER_CONFIG_v1.0.yaml：
     behavioral_cryptography:
       F5_vocabulary:
         master_profile:
           UID9622:
             signature_words: [宝宝, 龍魂, DNA, ...]  ← 粘貼更新
             ...

  4. 運行啟動腳本：
     python3 master_config_bootstrap.py

  5. 驗證完整性：
     cat ./generated/behavioral_profiles.json

  6. 如果一切正常·提交變更：
     git add MASTER_CONFIG_v1.0.yaml
     git commit -m "feat: F5/F6/F7 最新定義·從 Notion 同步"
    ↓
系統自動：
  - 生成新的 behavioral_profiles.json
  - 更新所有衍生文件
  - 一切文件保持一致
```

### 流程3：添加新人格或新色彩

```
要添加新的人格 P15：

1. 編輯 MASTER_CONFIG_v1.0.yaml：
   multi_persona_system:
     P15:
       name: "新人格"
       role: "新角色"
       decision_weight: 75

2. 運行啟動腳本：
   python3 master_config_bootstrap.py

3. 檢查 generated/multi_persona_definitions.json
   確認 P15 已添加

4. 提交：
   git add MASTER_CONFIG_v1.0.yaml generated/
   git commit -m "feat: P15新人格·决策权重75"

結果：
  ✓ multi_persona_definitions.json 自動更新
  ✓ behavioral_profiles.json 自動更新
  ✓ 所有其他文件自動同步
  ✓ 無需手動修改 5 個文件
```

---

## 為什麼這樣做

### 優點1：無需維護 N 個文件

**舊方式**（你現在的情況）：
```
修改 weight_color_mapping.json
  ↓ 然後
修改 behavioral_profiles.json
  ↓ 然後
修改 multi_persona_definitions.json
  ↓ 然後
修改 FEARLESS_STEVE_PROTOCOL...
  ↓ 然後
修改 text_as_weight_visualization_framework.py
  ↓ 然後...

N 個文件同時改 = 容易出錯
```

**新方式**：
```
只修改 MASTER_CONFIG_v1.0.yaml
  ↓
運行啟動腳本 (1 個命令)
  ↓
所有文件自動一致

N 個文件 = 自動生成·不手動改
```

### 優點2：版本控制更清晰

**舊方式**：
```
git status
# 顯示：
#   modified: weight_color_mapping.json
#   modified: behavioral_profiles.json
#   modified: multi_persona_definitions.json
#   ...
# （很難看出真正改了什麼）
```

**新方式**：
```
git status
# 顯示：
#   modified: MASTER_CONFIG_v1.0.yaml
# （只有一個源頭改變）

git diff MASTER_CONFIG_v1.0.yaml
# （清晰地看到真正的改變）

衍生文件自動更新·git 歷史乾淨
```

### 優點3：完全可追溯

```
任何衍生文件都帶上「出生證」：

{
  "metadata": {
    "dna": "#龍芯⚡️2026-05-26-MASTER-CONFIG-CANONICAL-v1.0",
    "timestamp": "2026-05-26T23:54:00+08:00",
    "generated_from": "MASTER_CONFIG_v1.0.yaml",
    "integrity_hash": "abc123def456"
  }
}

意思：
  ✓ 這個 JSON 是自動生成的（不是手工編輯）
  ✓ 來自哪個源頭版本
  ✓ 何時生成
  ✓ 完整性哈希（驗證沒被修改）
```

### 優點4：防止「開機不一樣」

```
啟動時的流程：

系統啟動
  ↓
master_config_bootstrap.py 自動運行
  ↓
從 MASTER_CONFIG_v1.0.yaml 讀取
  ↓
生成 behavioral_profiles.json v123
生成 weight_color_mapping.json v123
生成 multi_persona_definitions.json v123
  ↓
系統看到的配置 = 完全一致

保證：
  ✓ 每次啟動·所有文件都是最新的
  ✓ 不會因為某個文件沒更新導致不一致
  ✓ 即使 Notion 更新了·下次啟動就會同步
```

---

## 遷移步驟（從舊方式到新方式）

### 步驟1：備份現有文件

```bash
cd /Users/zuimeidedeyihan/longhun-system/config

mkdir -p ./backup_old_files
cp *.json ./backup_old_files/
cp *.py ./backup_old_files/
# （保留舊文件·以防萬一）
```

### 步驟2：驗證 MASTER_CONFIG 完整

```bash
python3 -c "import yaml; yaml.safe_load(open('MASTER_CONFIG_v1.0.yaml'))"
# 輸出：無錯誤 = 配置有效
```

### 步驟3：運行啟動腳本

```bash
python3 master_config_bootstrap.py

# 輸出：
# ✓ 主干配置已加载
# ✓ 配置完整性检查通过
# 【生成】behavioral_profiles.json
# 【生成】weight_color_mapping.json
# 【生成】multi_persona_definitions.json
# ✓ 启动完成
```

### 步驟4：驗證生成的文件

```bash
# 檢查生成目錄
ls -la ./generated/

# 驗證文件內容
cat ./generated/behavioral_profiles.json | head -20
cat ./generated/weight_color_mapping.json | head -20

# 對比舊舊文件（應該基本一致）
diff behavioral_profiles.json ./generated/behavioral_profiles.json
```

### 步驟5：更新 .gitignore

```bash
# 在 .gitignore 中加入：
./generated/*

# 或在 git 中：
git rm --cached behavioral_profiles.json
git rm --cached weight_color_mapping.json
git rm --cached multi_persona_definitions.json

# （衍生文件由啟動腳本生成·不進版本控制）
```

### 步驟6：提交主干配置

```bash
git add MASTER_CONFIG_v1.0.yaml master_config_bootstrap.py
git commit -m "feat: 建立單一真實源頭·所有配置从MASTER_CONFIG生成"
```

---

## 日常操作

### 日常1：更新 Notion 內容

```
Notion 更新了 F5 詞彙
  ↓
編輯本地 MASTER_CONFIG_v1.0.yaml
  ↓
python3 master_config_bootstrap.py
  ↓
git add/commit
  ↓
完成·所有文件自動同步
```

### 日常2：添加新規則

```
要添加新的色彩阈值
  ↓
編輯 MASTER_CONFIG_v1.0.yaml 中的 weight_formulas
  ↓
python3 master_config_bootstrap.py
  ↓
所有涉及色彩的衍生文件自動更新
```

### 日常3：團隊協作

```
多人編輯同一個配置·如何處理？

舊方式：
  開發者A 改 behavioral_profiles.json
  開發者B 改 weight_color_mapping.json
  結果：合並衝突·很難解決

新方式：
  所有開發者只改 MASTER_CONFIG_v1.0.yaml
  （單一文件·衝突更容易解決）

  本地衍生文件自動生成·不進版本控制
  （無衝突·完全自動）
```

---

## 技術細節

### 啟動腳本做了什麼

```python
def run(self):
    """執行完整啟動流程"""

    # 1. 加載主干配置
    load_master_config()

    # 2. 驗證完整性
    validate_config()

    # 3. 生成衍生文件
    generate_behavioral_profiles()
    generate_weight_color_mapping()
    generate_multi_persona_definitions()

    # 4. 計算完整性哈希
    integrity_hash = compute_integrity_hash()

    # 5. 記錄啟動報告
    generate_startup_report()
```

### 啟動報告包含什麼

```json
{
  "timestamp": "2026-05-26T23:54:00+08:00",
  "status": "🟢 SUCCESS",
  "files_generated": [
    "behavioral_profiles.json",
    "weight_color_mapping.json",
    "multi_persona_definitions.json",
    "startup_report.json"
  ],
  "integrity_hash": "abc123def456",
  "dna": "#龍芯⚡️2026-05-26-MASTER-CONFIG-CANONICAL-v1.0",
  "notes": "所有配置文件從 MASTER_CONFIG_v1.0.yaml 一致生成·無人工修改"
}
```

---

## 常見問題

### Q1：如果啟動腳本失敗怎麼辦？

```
A: 檢查日誌：
   cat ./bootstrap.log

   常見原因：
   1. MASTER_CONFIG_v1.0.yaml 格式錯誤 → 用 yamllint 驗證
   2. 缺少必要的 section → 檢查 validate_config()
   3. 權限問題 → chmod +x master_config_bootstrap.py
```

### Q2：可以手動編輯 generated/ 裡的文件嗎？

```
A: 不建議。理由：

   手動編輯
     ↓ 下次啟動時
   被自動生成的版本覆蓋
     ↓
   你的改變丟失

   應該做：
   改 MASTER_CONFIG_v1.0.yaml
     ↓
   運行啟動腳本
```

### Q3：如何確認配置是一致的？

```
A: 運行啟動腳本後：
   cat ./generated/startup_report.json

   檢查：
   ✓ "status": "🟢 SUCCESS" ?
   ✓ integrity_hash 一致 ?
   ✓ 文件生成時間最新 ?

   如果都對·配置一致。
```

### Q4：為什麼要計算 integrity_hash？

```
A: 防止意外修改。

   假設某人手動編輯了 behavioral_profiles.json
     ↓
   下次你檢查時：
   integrity_hash 改變了
     ↓
   你知道文件被改過了
     ↓
   運行啟動腳本恢復到一致狀態
```

---

## 最終效果

**啟動前**（混亂）：
```
config/
├─ MASTER_CONFIG_v1.0.yaml (主干)
├─ behavioral_profiles.json (可能過期)
├─ weight_color_mapping.json (可能過期)
├─ multi_persona_definitions.json (可能過期)
├─ text_as_weight_visualization_framework.py (獨立)
├─ TextAsWeightVisualization.swift (獨立)
├─ FEARLESS_STEVE_PROTOCOL_v2.0_MULTI_PERSONA_ENGINE.cpp (獨立)
└─ ... 還有更多

「每次開機都不一樣」
```

**啟動後**（一致）：
```
config/
├─ MASTER_CONFIG_v1.0.yaml (唯一源頭)
├─ master_config_bootstrap.py (啟動腳本)
├─ generated/ (自動生成·無需手動改)
│   ├─ behavioral_profiles.json ✓ 最新
│   ├─ weight_color_mapping.json ✓ 最新
│   ├─ multi_persona_definitions.json ✓ 最新
│   └─ startup_report.json ✓ 驗證
└─ ... 其他源代碼文件

「每次啟動都一致·Notion 有變化時自動同步」
```

---

**DNA**: `#龍芯⚡️2026-05-26-SINGLE-SOURCE-OF-TRUTH-GUIDE-v1.0`

**CONFIRM**: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z` ✅
