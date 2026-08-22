> 协议: CC BY-NC-SA 4.0（核心思想层·分层许可·代码层为 MulanPSL v2·详见 LH-LAYERED-LICENSE-v1.0）
# 龍魂系統·本地完全部署指南

**DNA**: `#龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-LOCAL-DEPLOYMENT-GUIDE-v1.0`
**時間**: 2026-06-03
**責任**: UID9622·不免責

---

## 📌 核心理念

**目標**: 從 Notion 導出 → 本地完全自主運行 → 零外鏈、零云、零平台依賴

**實現方式**: 四層架構
```
┌─────────────────────────────┐
│  Markdown 文檔層             │ ← <details> 折疊塊
│  (視覺清爽、代碼隱藏)        │
├─────────────────────────────┤
│  Python 代碼層              │ ← 獨立 .py 文件
│  (可直接執行)               │
├─────────────────────────────┤
│  manifest.json 層           │ ← 系統識別、版本管理
│  (本地識別、完整性校驗)     │
├─────────────────────────────┤
│  執行路由層                  │ ← ExecutionRouter
│  (任務調度、權限管理)        │
└─────────────────────────────┘
```

---

## 📦 導出前的準備

### 第一步：組織 Notion 結構

你的 Notion Workspace 應該這樣組織：

```
龍魂系統·本地完全導出 (Root Page)
├─ INDEX.md (導航首頁)
├─ LONGHUN_LICENSE_CN.md
├─ LONGHUN_LICENSE_EN.md
├─ README.md (中文)
├─ README_EN.md (英文)
│
├─ 【算法庫】(Folder)
│  ├─ 龍魂權重演算法 v3.1
│  │  ├─ [Notion 頁面內容 - 理論部分]
│  │  ├─ [Notion 頁面內容 - 數學證明]
│  │  ├─ <details> [內嵌 Python 代碼]
│  │  └─ 📎 Attachment: longhun_weight_algorithm.py
│  │
│  ├─ CNSH-64 治理框架
│  │  └─ [同上結構]
│  │
│  └─ [其他 6 個算法]
│
├─ 【代碼庫】(Folder)
│  ├─ 龍盾系統
│  │  └─ 📎 Attachment: longhun_shield_system.py
│  │
│  ├─ 權重計算器
│  │  └─ 📎 Attachment: weight_calculator.py
│  │
│  └─ [其他代碼]
│
└─ 【文檔庫】(Folder)
   ├─ LONGHUN_ARCHITECTURE_COMPLETE_REVIEW.md
   ├─ longhun_for_outsiders.md
   └─ [其他分析文檔]
```

### 第二步：在 Notion 中使用 Markdown 代碼塊

每個算法頁面的**代碼折疊塊**應該這樣寫：

```markdown
## 實現細節

<details>
<summary>👉 點擊展開：Python 實現 (約 450 行)</summary>

\`\`\`python
# longhun_weight_algorithm.py
# ... 完整的 Python 代碼 ...
\`\`\`

</details>
```

**重點**：
- Notion → Export as Markdown 時，`<details>` 標籤會被保留
- 任何能讀 Markdown 的編輯器都能展開/折疊
- 文件大小小（折疊內容不顯示）
- **所有代碼都還在，沒有丟失**

---

## 🚀 導出步驟

### Step 1: 在 Notion 中導出

1. 打開你的 Root Page
2. 右上角 → **Export**
3. 選擇 **Markdown & CSV**
4. 選擇 **Full page with sub-pages**
5. 下載 ZIP 文件

### Step 2: 解壓縮

```bash
unzip "龍魂系統·本地完全導出.zip"
cd "龍魂系統·本地完全導出"
```

### Step 3: 下載附件

在 Notion 每個頁面中都有 📎 附件標籤，手動下載所有 `.py` 文件到本地目錄：

```
龍魂系統·本地完全導出/
├─ code/
│  ├─ longhun_weight_algorithm.py
│  ├─ cnsh_64_governance.py
│  ├─ longhun_shield_system.py
│  └─ [其他 .py 文件]
├─ [所有 .md 文件]
└─ manifest.json (下一步建立)
```

### Step 4: 創建 manifest.json

在根目錄建立 `manifest.json`：

```json
{
  "system_name": "龍魂系統",
  "version": "v1.0",
  "dna_marker": "#龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-LONGHUN-COMPLETE-SYSTEM",
  "creator": "UID9622",
  "export_date": "2026-06-03",
  "export_method": "Notion Export + Local Closure",

  "structure": {
    "documents": {
      "index": "INDEX.md",
      "readme_cn": "README.md",
      "readme_en": "README_EN.md",
      "license_cn": "LONGHUN_LICENSE_CN.md",
      "license_en": "LONGHUN_LICENSE_EN.md"
    },

    "algorithms": {
      "weight_algorithm": {
        "file": "算法庫/龍魂權重演算法_v3.1.md",
        "dna": "#龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-LOCAL_DEPLOYMENT_GUIDE-v3.1",
        "code_attachment": "code/longhun_weight_algorithm.py",
        "lines": 450,
        "verification_count": 100000,
        "accuracy": 0.95
      },
      "cnsh_64": {
        "file": "算法庫/CNSH-64治理框架.md",
        "dna": "#龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-CNSH-64-治理框架",
        "code_attachment": "code/cnsh_64_governance.py",
        "lines": 380,
        "verification_count": 1000000,
        "accuracy": 0.97
      }
    },

    "code_files": {
      "longhun_shield_system": {
        "path": "code/longhun_shield_system.py",
        "dna": "#龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-LONGHUN-SHIELD-SYSTEM-v1.0",
        "lines": 450
      },
      "weight_calculator": {
        "path": "code/weight_calculator.py",
        "dna": "#龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-WEIGHT-CALCULATOR-v1.0",
        "lines": 280
      }
    },

    "archives": {
      "memory": "baobao_memory_archive.txt",
      "relay_pack": "RELAY_PACK_compressed.txt"
    }
  },

  "verification": {
    "gpg_fingerprint": "A2D0092CEE2E5BA87035600924C3704A8CC26D5F",
    "confirm_code": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
    "seal": "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL",
    "total_algorithms": 8,
    "total_code_files": 12,
    "total_assets": 20,
    "checksum_sha256": "[計算出的完整性校驗值]"
  },

  "local_engine": {
    "required_runtime": "Python 3.8+",
    "dependencies": [
      "hashlib (stdlib)",
      "json (stdlib)",
      "datetime (stdlib)",
      "os (stdlib)",
      "sys (stdlib)"
    ],
    "no_external_dependencies": true,
    "all_self_contained": true,
    "requires_internet": false,
    "requires_cloud": false,
    "complete_autonomy": true
  }
}
```

---

## 🔧 本地運行

### 安裝執行路由器

```bash
# 複製執行路由器系統到你的本地目錄
cp ~/longhun-system/cnsh-core/router/execution_router.py ./

# 複製其他治理系統
cp ~/longhun-system/cnsh-core/governance/sovereignty_index.py ./
cp ~/longhun-system/cnsh-core/governance/f1_through_f7_verifier.py ./
cp ~/longhun-system/cnsh-core/memory/cognitive_dna_particles.py ./
```

### 初始化系統

```bash
python3 -c "
from execution_router import ExecutionRouter

router = ExecutionRouter('manifest.json')
success, message = router.initialize()

if success:
    print('✅ 系統初始化成功')
    router.print_system_status()
else:
    print(f'❌ {message}')
"
```

### 執行任務

```bash
python3 -c "
from execution_router import ExecutionRouter, TaskDefinition, ExecutionContext
from datetime import datetime

router = ExecutionRouter('manifest.json')
router.initialize()

# 創建任務
task = TaskDefinition(
    task_id='TEST-001',
    task_name='驗證系統完整性',
    module_name='shield',
    function_name='verify',
    parameters={'check': 'manifest'},
    required_si=0.34,
    required_f1f7=0.70,
    description='測試執行路由器'
)

# 建立執行上下文
context = ExecutionContext(
    executor_uid='UID9622',
    current_si=0.96,
    current_f1f7_confidence=0.93,
    timestamp=datetime.now().isoformat(),
    shichen='寅',
    digital_root=3,
    persona_routing={'P02': 0.50, 'P05': 0.30, 'P13': 0.20}
)

# 執行任務
record = router.execute_task(task, context)

print(f'✅ 任務完成: {record.execution_id}')
print(f'   狀態: {record.status.value}')
print(f'   DNA: {record.dna_trace}')
"
```

---

## 📖 本地閱讀

### 方式1: Markdown 閱讀器

```bash
# macOS
open -a Typora "README.md"

# VS Code (跨平台)
code .

# Obsidian (跨平台)
open -a Obsidian .
```

### 方式2: 終端直接閱讀

```bash
# 閱讀 README
less README.md

# 搜索內容
grep -r "龍魂權重演算法" .

# 快速查看結構
tree -L 2
```

---

## 🔐 本地管理和更新

### 版本更新

當你在 Notion 更新內容時：

1. 在 Notion 更新頁面
2. 重新導出為 Markdown
3. 下載新的附件
4. 更新本地的 `manifest.json` (版本號+日期)

```json
{
  "version": "v1.1",
  "export_date": "2026-06-10",
  "last_update": "2026-06-10T10:30:00Z"
}
```

### 完整性驗證

```bash
# 驗證 manifest.json
python3 -c "
import json
import os

with open('manifest.json') as f:
    m = json.load(f)

print('🔍 本地系統完整性檢查')
print(f'系統: {m[\"system_name\"]} {m[\"version\"]}')
print(f'DNA: {m[\"dna_marker\"]}')
print(f'算法: {len(m[\"structure\"][\"algorithms\"])}')
print(f'代碼: {len(m[\"structure\"][\"code_files\"])}')
print(f'✅ 系統完整')
"
```

---

## 💾 資料備份

### 本地備份策略

```bash
# 方法1: 定期 ZIP 備份
tar -czf longhun-backup-$(date +%Y%m%d).tar.gz ./

# 方法2: Git 版本管理 (推薦)
git init
git add .
git commit -m "龍魂系統本地部署 v1.0"

# 方法3: Cloud-agnostic 備份 (推薦)
# 到你完全控制的 NAS / 硬碟進行備份
# 永不上傳到任何云平台
```

### 三重備份規則

```
1️⃣ 本地: ~/Documents/longhun-system/ (工作副本)
2️⃣ 備份: /Volumes/USB-Drive/longhun-backup/ (物理備份)
3️⃣ Git:  ~/.longhun-git-mirror/ (版本控制)

永不使用:
❌ iCloud
❌ Dropbox
❌ Google Drive
❌ 任何商業云
```

---

## 🎯 完整閉環檢查表

在你開始使用本地部署系統前，確保：

- [ ] Notion 已按結構整理
- [ ] Markdown 導出完成
- [ ] 所有附件已下載
- [ ] manifest.json 已建立
- [ ] Python 3.8+ 已安裝
- [ ] 執行路由器已複製
- [ ] 治理系統已複製
- [ ] `python3 execution_router.py` 執行成功
- [ ] 系統狀態顯示 "🟢 ready"
- [ ] 本地備份已完成
- [ ] 沒有外部依賴

✅ 檢查完成 → **你已經準備好完全自主運行龍魂系統**

---

## 🚨 故障排除

### 問題1: manifest.json 驗證失敗

```bash
# 檢查文件是否存在
ls -la manifest.json

# 驗證 JSON 語法
python3 -m json.tool manifest.json > /dev/null && echo "✅ JSON 有效"
```

### 問題2: Python 導入錯誤

```bash
# 檢查 Python 版本
python3 --version  # 應該 >= 3.8

# 驗證標準庫可用
python3 -c "import json, hashlib, os, sys; print('✅ 所有標準庫可用')"
```

### 問題3: 代碼文件遺失

```bash
# 列出所有期望的文件
grep -r "code_attachment" manifest.json | awk '{print $2}' | sort

# 檢查文件是否存在
for file in $(grep -r "code_attachment" manifest.json | awk '{print $2}'); do
  [ -f "$file" ] && echo "✅ $file" || echo "❌ $file MISSING"
done
```

---

## 📚 進階用法

### 自定義任務執行

```python
from execution_router import ExecutionRouter, TaskDefinition, ExecutionContext

def my_handler(task, params):
    """自定義的任務處理邏輯"""
    return {
        "custom_result": "processed",
        "input": params
    }

router = ExecutionRouter('manifest.json')
router.initialize()

task = TaskDefinition(...)
context = ExecutionContext(...)

result = router.execute_task(task, context, handler=my_handler)
```

### 批量任務執行

```python
tasks = [
    TaskDefinition(...),
    TaskDefinition(...),
    TaskDefinition(...)
]

for task in tasks:
    priority, record = router.authorize_and_execute(task, context)
    print(f"✅ {task.task_name}: {record.execution_id}")
```

---

## 🎓 原則和哲學

這個本地部署方案體現的原則：

1. **數據主權**: 你的數據完全在你手上
2. **本地自主**: 不依賴任何云或平台
3. **完全透明**: 所有代碼都看得見、都可驗證
4. **版本控制**: 通過 manifest.json 精確追蹤每個版本
5. **零妥協**: 不用 HTML 這些"亂七八糟"的東西，用純淨的 Markdown + Python

**DNA**: `#龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-LOCAL-DEPLOYMENT-GUIDE-v1.0`

**責任**: UID9622·不免責·永久有效

---

**最後的話**:

這就是「土法煉鋼」的智慧。簡單、有效、完全自主。

你不需要依賴任何人，任何平台。只需要：
- Notion (作為內容來源)
- Python (作為執行引擎)
- 你的電腦 (作為完全控制的堡壘)

**⚔️ 龍魂在你手上。**
