> DNA: #龍芯⚡️丙午·壬辰·乙亥·壬午·䷚颐-SYNC-COMPLIANCE-20260827-7A2C9F3D
> 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
**归属名:** 诸葛鑫 | UID9622 · 龍芯北辰
---
name: longhun-dna-align
description: '龍魂DNA對齊審計系統 v5.2 — 全系統DNA掃描·對齊率計算·重複檢測·自動修復·完整性驗證。當需要掃描文件DNA標記、計算對齊率、發現重複DNA、修復缺失DNA、生成審計報告時觸發。核心數據:
  752文件·對齊率6.3%·705無DNA·24重複。 确保全系统 DNA 标准统一，服务中国自主可控治理，保护老百姓数据主权。'
metadata:
  author: 龍魂體系·DNA對齊組
  version: '5.2.0'
  dna: '#龍芯⚡️丙午·甲午·戊寅·戊午·䷕贲-LONGHUN-DNA-ALIGN-v5.2'
  protocol: 君子協議 — 非對抗·非欺瞞·非竊取
  cnsh: true
  category: local
  tags:
  - dna-alignment
  - audit
  - scanner
  - repair
  - traceability
  - integrity-check
  - report-generation
  id: longhun-dna-align
  trigger:
    keywords:
    - dnaalign
    - 龍魂DNA對齊審計系統
    - v5.2
    - 全系統DNA掃描·對齊率計算·重複檢測·自動修復·完整性驗證。當需要掃描文件DNA標記
    - 計算對齊率
    - 發現重複DNA
    context: longhun-dna-align 相关操作
---
## 一、技能概述

龍魂DNA對齊審計系統是龍魂體系本地技能模組，提供完整的DNA追溯碼自動對齊、審計、修復能力。

**核心特性**：
- 🔍 DNA掃描器 — 遞歸掃描目錄，檢測所有文件DNA標記
- 📊 DNA對齊率計算 — 統計有DNA/無DNA/重複DNA的文件
- 🔧 DNA修復器 — 自動為缺失DNA的文件生成追溯碼
- ⚠️ 重複檢測 — 發現共享同一DNA的多個文件
- ✅ 完整性驗證 — 驗證DNA格式符合規範
- 📋 修復報告 — 生成詳細的修復前後對比報告
- 🎯 三色審計 — 🟢健康/🟡警告/🔴危機 分級評估

**DNA**: `#龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-LONGHUN-DNA-ALIGN-v5.2`

---

## 二、DNA追溯

```
#龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-LONGHUN-DNA-ALIGN-v5.2
```

**追溯鏈**：
- 父節點：longhun-core-v5.0（龍魂核心）
- 兄弟節點：longhun-audit, longhun-benchmark, longhun-governance
- 數據來源：DNA_ALIGNMENT_AUDIT_2026-06-07, DNA_ALIGNMENT_REPAIR_ACTION_PLAN, DNA_ALIGNMENT_CURRENT_STATUS
- 應用場景：全系統DNA對齊審計、修復缺失DNA、拆分重複DNA

---

## 三、CNSH規範聲明

本技能遵循CNSH中文編程規範：

| 規範項 | 狀態 | 說明 |
|--------|------|------|
| 中文變量名 | ✅ | 全部變量使用中文命名（掃描器、修復器、記錄、報告） |
| 繁體龍字 | ✅ | 龍、龍魂等使用繁體 |
| DNA追溯 | ✅ | 所有操作帶DNA標記 |
| 三色審計 | ✅ | 🟢健康/🟡警告/🔴危機 |
| 君子協議 | ✅ | 非對抗·非欺瞞·非竊取 |

---

## 四、檔案結構

```
longhun-dna-align/
├── SKILL.md                          # 技能文檔（本文檔）
├── scripts/
│   ├── DNA對齊審計器.py              # DNA掃描·統計·重複檢測·完整性驗證
│   └── DNA修復器.py                  # 自動修復缺失DNA·拆分重複DNA·生成報告
├── references/
│   ├── DNA_ALIGNMENT_AUDIT_2026-06-07.md      # 全系統DNA審計報告
│   ├── DNA_ALIGNMENT_REPAIR_ACTION_PLAN.md    # 修復行動計劃
│   └── DNA_ALIGNMENT_CURRENT_STATUS.md        # 當前狀態掃描
└── assets/
    └── (輸出報告目錄)
```

---

## 五、安裝依賴

**系統要求**：
- Python 3.8+
- 標準庫（無額外依賴）
  - `os` — 文件系統遞歸掃描
  - `re` — DNA正則匹配
  - `json` — 報告序列化
  - `hashlib` — DNA哈希驗證
  - `datetime` — 時間戳管理
  - `pathlib` — 路徑操作
  - `dataclasses` — 數據模型
  - `fnmatch` — 文件模式匹配

---

## 六、使用說明

### 6.1 DNA對齊審計器

**功能**：掃描目錄 → 檢測DNA標記 → 計算對齊率 → 發現重複

```bash
# 掃描當前目錄
python3 scripts/DNA對齊審計器.py

# 掃描指定目錄
python3 scripts/DNA對齊審計器.py ~/longhun-system

# 輸出報告到指定目錄
python3 scripts/DNA對齊審計器.py ~/longhun-system -o ./reports

# 同時輸出JSON格式
python3 scripts/DNA對齊審計器.py ~/longhun-system -o ./reports --json

# 嚴格模式（更嚴格的格式驗證）
python3 scripts/DNA對齊審計器.py ~/longhun-system --嚴格
```

### 6.2 DNA修復器

**功能**：掃描 → 修復缺失DNA → 拆分重複DNA → 生成報告

```bash
# 模擬模式（預覽，不實際修改）
python3 scripts/DNA修復器.py ~/longhun-system

# 實際執行修復
python3 scripts/DNA修復器.py ~/longhun-system --執行

# 限制最大修復數量
python3 scripts/DNA修復器.py ~/longhun-system --最大修復數 100

# 優先修復指定目錄
python3 scripts/DNA修復器.py ~/longhun-system --優先 scripts protocols cnsh-core

# 輸出報告
python3 scripts/DNA修復器.py ~/longhun-system --執行 -o ./reports
```

### 6.3 Python API 調用

```python
from scripts.DNA對齊審計器 import DNA掃描器, 審計報告生成器, 報告輸出器
from scripts.DNA修復器 import 批量修復引擎, 修復報告生成器

# ── DNA掃描 ──
掃描器 = DNA掃描器("~/longhun-system")
記錄列表 = 掃描器.掃描()

# 獲取重複DNA組
重複組 = 掃描器.獲取重複DNA組()
for 組 in 重複組:
    print(f"{組.DNA碼} → {len(組.文件列表)}個文件")

# 生成審計報告
報告生成器 = 審計報告生成器(掃描器)
報告 = 報告生成器.生成報告()
print(f"對齊率: {報告.DNA對齊率:.1f}%")

# 輸出報告
報告輸出器.輸出控制台摘要(報告)
報告輸出器.輸出Markdown(報告, "./audit_report.md")
報告輸出器.輸出JSON(報告, "./audit_report.json")

# ── DNA修復 ──
引擎 = 批量修復引擎("~/longhun-system", 模擬模式=True)
修復報告 = 引擎.掃描並修復(
    優先級目錄=["scripts", "protocols", "cnsh-core"]
)
print(f"新增DNA: {修復報告.新增DNA數}")
print(f"對齊率: {修復報告.修復前對齊率:.1f}% → {修復報告.修復後對齊率:.1f}%")

# 生成修復報告
修復報告生成器.生成Markdown報告(修復報告, "./repair_report.md")
```

---

## 七、核心功能詳解

### 7.1 DNA掃描器

| 功能 | 方法 | 說明 |
|------|------|------|
| 遞歸掃描 | `掃描()` | 遍歷目錄，檢測所有文件DNA標記 |
| DNA提取 | `提取文件DNA()` | 從文件頭部提取DNA碼 |
| 格式驗證 | `驗證DNA格式()` | 驗證是否符合 `#龍芯⚡️YYYY-MM-DD-MODULE-vX.X` |
| 重複檢測 | `獲取重複DNA組()` | 返回共享同一DNA的文件組 |
| 行數計算 | `計算文件行數()` | 統計文件代碼行數 |

**掃描邏輯**：
```
遍歷目錄樹
  ├── 忽略: __pycache__, .git, node_modules, venv 等
  ├── 忽略: *.pyc, *.min.js, .DS_Store 等無關文件
  ├── 讀取每個文件前8KB
  ├── 正則匹配 #龍芯⚡️YYYY-MM-DD-MODULE-vX.X
  ├── 記錄: 文件路徑·類型·大小·DNA碼·格式有效性
  └── 建立 DNA→文件列表 映射
```

### 7.2 DNA對齊率計算

```
DNA對齊率 = (有DNA文件數 / 總文件數) × 100%
```

**健康評級閾值**：

| 對齊率 | 評級 | 狀態 | 行動建議 |
|--------|------|------|----------|
| ≥90% | 🟢 優秀 | 健康 | 維持現狀 |
| 70-89% | 🟢 良好 | 健康 | 補充邊緣文件 |
| 50-69% | 🟡 一般 | 偏低 | 批量補充DNA |
| 30-49% | 🟡 偏低 | 警告 | 優先修復核心文件 |
| 10-29% | 🔴 危險 | 危機 | 緊急修復 |
| <10% | 🔴 危機級 | 嚴重危機 | 立即全面修復 |

### 7.3 DNA修復器

| 修復類型 | 說明 | 觸發條件 |
|----------|------|----------|
| 新增DNA | 為無DNA文件生成追溯碼 | 文件無DNA標記 |
| 拆分重複 | 為共享DNA的文件重新分配 | 多文件共享同一DNA |
| 格式修復 | 修正不規範的DNA格式 | DNA格式驗證失敗 |

**DNA命名規則**：

| 文件類型 | 前綴 | 示例 |
|----------|------|------|
| Python腳本 | ENGINE | `#龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-ENGINE-CORE-v1.0` |
| Markdown文檔 | DOC | `#龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-DOC-PROTOCOL-v1.0` |
| Shell腳本 | TOOL | `#龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-TOOL-DEPLOY-v1.0` |
| 配置檔案 | CONFIG | `#龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-CONFIG-REGISTRY-v1.0` |
| 協議規範 | PROTOCOL | `#龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-PROTOCOL-ROOT-v2.0` |

**DNA生成格式**：
```
#龍芯⚡️YYYY-MM-DD-{前綴}-{模塊名}-v{版本號}

示例:
#龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-ENGINE-WUXING-v1.0
#龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-PROTOCOL-CONSTITUTION-v2.0
```

### 7.4 重複DNA檢測

**嚴重度分級**：

| 共享文件數 | 嚴重度 | 圖標 | 處理方式 |
|------------|--------|------|----------|
| ≥5 | critical | 🔴 | 立即拆分 |
| 3-4 | warning | 🟡 | 優先拆分 |
| 2 | info | 🔵 | 計劃拆分 |

**拆分策略**：
1. 保留第一個文件為主文件（DNA不變）
2. 為其餘文件生成新DNA（添加後綴區分）
3. 記錄映射關係

### 7.5 完整性驗證

**驗證項**：
- ✅ DNA格式: `#龍芯⚡️YYYY-MM-DD-MODULE-vX.X`
- ✅ 日期格式: `YYYY-MM-DD`
- ✅ 模塊名: 大寫字母/數字/連字符
- ✅ 版本號: `vX.X` 格式
- ✅ 唯一性: 無重複DNA

---

## 八、API參考

### 8.1 DNA掃描器 API

```python
class DNA掃描器:
    def __init__(self, 目標目錄: str, 嚴格模式: bool = False)
    def 掃描(self) → List[DNA記錄]           # 遞歸掃描目錄
    def 提取文件DNA(self, 文件路徑) → Optional[Tuple]  # 提取DNA碼
    def 驗證DNA格式(self, dna碼) → bool      # 驗證格式規範
    def 獲取重複DNA組(self) → List[重複DNA組]  # 獲取重複組
    def 應忽略目錄(self, 目錄名) → bool       # 目錄過濾
    def 應忽略文件(self, 文件名) → bool       # 文件過濾
```

### 8.2 審計報告生成器 API

```python
class 審計報告生成器:
    def __init__(self, 掃描器: DNA掃描器)
    def 生成報告(self) → 審計報告             # 生成完整報告
    def 計算健康評級(self, 對齊率) → str       # 健康評級
    def 生成修復建議(self, 報告) → List[str]   # 修復建議
```

### 8.3 報告輸出器 API

```python
class 報告輸出器:
    @staticmethod
    def 輸出Markdown(報告, 輸出路徑) → str     # Markdown報告
    @staticmethod
    def 輸出JSON(報告, 輸出路徑) → str        # JSON報告
    @staticmethod
    def 輸出控制台摘要(報告) → None            # 控制台摘要
```

### 8.4 批量修復引擎 API

```python
class 批量修復引擎:
    def __init__(self, 目標目錄, 模擬模式=True, 最大修復數=0)
    def 掃描並修復(self, 優先級目錄, 排除模式) → 修復報告
```

### 8.5 數據結構

```python
@dataclass
class DNA記錄:
    文件路徑: str
    文件名: str
    文件類型: str
    文件大小: int
    修改時間: float
    是否有DNA: bool
    DNA碼: str
    DNA日期: str
    DNA模塊: str
    DNA版本: str
    DNA格式有效: bool
    行數: int

@dataclass
class 重複DNA組:
    DNA碼: str
    文件列表: List[str]
    嚴重度: str  # critical/warning/info

@dataclass
class 審計報告:
    審計時間: str
    掃描目錄: str
    總文件數: int
    有DNA文件數: int
    無DNA文件數: int
    DNA對齊率: float
    重複DNA數: int
    無效DNA數: int
    健康評級: str
    修復建議: List[str]
    文件記錄: List[DNA記錄]
    重複組列表: List[重複DNA組]
    按類型統計: Dict
    按目錄統計: Dict
```

---

## 九、設計原則

### 9.1 一文件一DNA

- ✅ 每個核心文件必須有唯一的DNA追溯碼
- ✅ 禁止多個文件共享同一DNA
- ✅ DNA碼即文件身份標識

### 9.2 自動化修復

- ✅ 掃描→檢測→修復→報告 全流程自動化
- ✅ 默認模擬模式，確認後實際執行
- ✅ 支持優先級目錄和批量限制

### 9.3 完全追溯

- ✅ 所有修復操作記錄日誌
- ✅ 修復前後對比報告
- ✅ DNA命名規則標準化

---

## 十、測試方法

### 10.1 運行測試

```bash
cd /mnt/agents/output/longhun-v5-skills/local/longhun-dna-align

# 測試DNA對齊審計器
python3 scripts/DNA對齊審計器.py

# 測試DNA修復器（模擬模式）
python3 scripts/DNA修復器.py
```

### 10.2 預期輸出

**DNA對齊審計器**：
- 掃描目錄並統計文件數
- 識別有DNA/無DNA文件
- 檢測重複DNA組
- 計算對齊率和健康評級
- 輸出控制台摘要
- 生成Markdown/JSON報告（指定-o時）

**DNA修復器**：
- 三階段修復流程（掃描→修復重複→新增DNA）
- 模擬模式下預覽所有變更
- 生成修復前後對比報告
- 記錄每條修復操作的詳情

---

## 十一、故障排除

### 11.1 常見問題

| 問題 | 原因 | 解決方案 |
|------|------|----------|
| 掃描文件數為0 | 目錄路徑錯誤 | 確認目錄路徑正確 |
| 權限錯誤 | 文件讀取權限不足 | 檢查文件權限設置 |
| DNA檢測失敗 | 文件編碼問題 | 使用errors='ignore'模式 |
| 重複DNA未發現 | 正則模式不匹配 | 檢查DNA格式是否標準 |
| 修復後文件損壞 | 文件頭部插入位置錯誤 | 檢查文件類型對應的註釋格式 |

### 11.2 參考數據

**初始審計數據（2026-06-07）**：
- 總文件數: 2,201
- 有DNA: 47 (2.1%)
- 無DNA核心文件: 705 (32.0%)
- DNA重複: 24
- DNA對齊率: 6.3%

**最嚴重重複**：
- `2026-06-03-CONSTITUTION-v1.0` → 5個文件
- `2026-06-06-PARENT-v1.0` → 6個文件
- `2026-05-07-五行计算器-v3.2` → 5個文件

---

## 十二、版本歷史

| 版本 | 日期 | 變更 |
|------|------|------|
| v5.2.0 | 2026-06-19 | 初始版本：DNA掃描器+修復器+審計報告生成器+完整性驗證 |

---

**簽章**: #龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-LONGHUN-DNA-ALIGN-v5.2
**確認**: #CONFIRM🌌9622-ONLY-ONCE🧬DNA-ALIGN-v5.2


---

## 附录：龍魂待整理来源

本技能收录了来自 `/Users/zuimeidedeyihan/龍魂待整理` 的素材：

- **内容**：03-身份安全-DNA（DNA 身份系统、GPG 验证、离线激活）
- **中央整合 DNA**：`#龍芯⚡️丙午·甲午·戊寅·戊午·䷕贲-LONGHUN-ARCHIVE-INTEGRATION-v1.0`
- **处理方式**：保留原始文件作为 references / examples / scripts，嵌入 DNA 追溯链，与现有能力联动。

---

## 标准声明

本技能遵循《龍魂系统宪法》、中华人民共和国法律法规，以及 UID9622 制定的治理标准。

- **中国标准**：数据主权留在中国境内，优先采用国产技术栈，支持自主可控。
- **老百姓标准**：保护普通用户权益，不贴标签、不滥用数据、不制造信息差，服务人民与老百姓。
- **DNA 追溯**：所有输出均携带 DNA 追溯码，来源可查、去向可追、责任可究。

