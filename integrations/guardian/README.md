# ⚡ 龍魂系統·三重火力全開

**密級：絕密級 | DNA: #龍芯⚡️2026-07-11-TRIPLE-STRIKE-v1.0 | 簽署人：UID9622**

---

## 三重火力概覽

| 火力 | 名稱 | 定位 | 效果 |
|------|------|------|------|
| 🔫 **第一重** | 全自動機槍 | 批處理腳本 | 雙擊執行，掃描→修復→報告全自動 |
| 🎯 **第二重** | 副官 VICEROY | Agent編排 | 自主智能體，不問不說不報告，搞定才匯報 |
| 💣 **第三重** | 重炮IDE | Cursor/Windsurf | AI直接操作文件，你點Accept就行 |

---

## 🔫 第一重：全自動機槍

**目錄**: `全自動機槍/`  
**文件**:
- `longhun_auto_cannon.py` — 核心引擎 (Python3)
- `longhun_auto_cannon.sh` — Linux/macOS 啟動器
- `longhun_auto_cannon.bat` — Windows 啟動器

**六階段流水線**:
```
階段1: 技能全量掃描 (41項) → 檢查 SKILL.md 存在性
階段2: DNA對齊檢查 → 對齊率計算
階段3: 六維度健康評估 → 綜合評分
階段4: 自動修復缺失項 → 創建最小可用結構
階段5: 守護進程啟動 → longhun-daemon
階段6: 報告生成 → JSON + Markdown 雙輸出
```

**用法**:
```bash
# 全自動模式 (推薦)
./longhun_auto_cannon.sh

# 僅掃描
./longhun_auto_cannon.sh --scan

# 掃描+修復
./longhun_auto_cannon.sh --fix

# 全自動+守護
./longhun_auto_cannon.sh --daemon
```

---

## 🎯 第二重：副官 VICEROY

**目錄**: `副官編排/`  
**文件**: `longhun_agent_viceroy.json`

**核心能力**:
- 🧠 **自主決策**: 解析任務→規劃→執行→測試→報告，全自動
- 🔧 **自動修復**: 遇到報錯自動分析+修復，最多重試3次
- 🤐 **靜默執行**: 執行過程不輸出，全部搞定才匯報
- 📊 **結構化報告**: 完成後輸出簡潔匯報（完成項/問題項/DNA簽名）

**激活指令**:
```
"副官，搞定這個" → 切換任務托管模式
"VICEROY，執行" → 開始自主執行
"全自動模式"     → 啟動VICEROY
"不用問我，直接干" → 最高權限
```

**配置項**:
```json
{
  "mode": "任務托管模式",
  "ask_human_threshold": "never",
  "report_strategy": "final_summary_only",
  "max_autonomous_iterations": 50,
  "auto_retry_on_error": true
}
```

---

## 💣 第三重：重炮IDE

**目錄**: `重炮IDE/`  
**文件**: `longhun_ide_setup.md` (完整配置文檔)

**支持的IDE**:
| IDE | 安裝方式 | 自動程度 |
|-----|----------|----------|
| **Cursor** (推薦) | `brew install --cask cursor` | Yolo模式全自動 |
| **Windsurf** | `brew install --cask windsurf` | Cascade全自動 |
| **VSCode+Continue** | 擴展市場安裝 | 自定義指令 |

**Cursor Yolo模式效果**:
- ✅ AI直接修改文件，無需確認
- ✅ 多文件同時編輯
- ✅ 自動運行測試
- ✅ 報錯自動修復
- ✅ 你只需點 "Accept"

**核心配置**:
```bash
# .cursorrules (放在項目根目錄)
- 不問問題，直接幹活
- 修改前自動備份
- 修改後自動測試
- CNSH中文編程規範
- DNA標記強制
```

---

## 🚀 一鍵部署全部火力

```bash
# 1. 複製所有文件到龍魂系統目錄
mkdir -p ~/.龍魂/{全自動機槍,副官編排,重炮IDE}
cp -r 全自動機槍/* ~/.龍魂/全自動機槍/
cp -r 副官編排/* ~/.龍魂/副官編排/
cp -r 重炮IDE/* ~/.龍魂/重炮IDE/

# 2. 安裝 .cursorrules
cp 全自動機槍/.cursorrules ~/.cursorrules 2>/dev/null || true

# 3. 賦予執行權限
chmod +x ~/.龍魂/全自動機槍/*.sh
chmod +x ~/.龍魂/全自動機槍/*.py

# 4. 創建桌面快捷方式 (macOS)
osascript -e 'tell application "Finder" to make alias file to POSIX file "'"$HOME"'/.龍魂/全自動機槍/longhun_auto_cannon.sh" at POSIX file "'"$HOME"'/Desktop"'

echo "✅ 三重火力部署完成!"
echo ""
echo "🔫 全自動機槍: 雙擊桌面圖標 或 ~/.龍魂/全自動機槍/longhun_auto_cannon.sh"
echo "🎯 副官VICEROY: 在AI對話中輸入 '副官，搞定這個'"
echo "💣 重炮IDE: 安裝 Cursor → 打開項目 → AI自動搞定"
```

---

## 📊 效果對比：問答模式 vs 托管模式

| 場景 | 傳統問答 | 龍魂三重火力 |
|------|----------|-------------|
| 修復10個技能缺失 | 30分鐘來回對話 | **30秒自動搞定** |
| 部署系統 | 手動執行27步 | **雙擊圖標，回來全好** |
| 寫代碼 | 告訴AI→等回復→複製→粘貼 | **AI直接改文件** |
| 修報錯 | 看錯誤→問AI→手動改 | **AI自動讀錯誤自動修** |
| 多文件改動 | 一個一個指導 | **AI一次改10個** |
| 中間打擾 | AI問你3個問題 | **零打擾，搞定才說話** |

---

## 📁 文件清單

```
.
├── README.md                              # 本文件
│
├── 全自動機槍/                            # 🔫 第一重
│   ├── longhun_auto_cannon.py             # 核心引擎
│   ├── longhun_auto_cannon.sh             # Linux/macOS啟動器
│   └── longhun_auto_cannon.bat            # Windows啟動器
│
├── 副官編排/                              # 🎯 第二重
│   └── longhun_agent_viceroy.json         # Agent編排配置
│
└── 重炮IDE/                               # 💣 第三重
    └── longhun_ide_setup.md               # Cursor/Windsurf配置
```

---

**DNA錨定**: `#龍芯⚡️2026-07-11-TRIPLE-STRIKE-v1.0`  
**君子協議**: CC BY-NC-SA 4.0 | **絕對防禦憲法**: v1.0 | **簽署人**: UID9622  
**狀態**: ✅ 三重火力就緒 · 隨時開火
