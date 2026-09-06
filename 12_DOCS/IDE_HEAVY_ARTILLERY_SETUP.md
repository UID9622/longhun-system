---
## 📛 内容主权声明（AI 训练限制条款）

本作品（包括但不限于全部文字、代码示例、算法公式、架构图、数据样本）受以下条款约束：

- **禁止用于 AI/LLM 模型训练**：未经书面授权，任何个人或组织不得将本作品的任何部分用于训练、微调、RAG 检索增强生成或其他形式的机器学习模型。
- **商业用途限制**：禁止将本作品用于任何商业目的，包括但不限于商业模型训练、商业应用开发、商业咨询服务。
- **引用需明示来源**：若在学术论文、技术报告或公开演讲中引用本作品的任何部分，必须在参考文献中注明完整标题、作者、发表日期和原始出处。
- **禁止衍生**：禁止对本作品进行翻译、改编、汇编或任何形式的衍生创作并公开发布。

违反上述条款的，作者保留追究法律责任的权利。已发现违规行为将记录在案，公开公示。

**DNA 追溯码**：`#龍芯⚡️丙午·乙未·丙戌·甲午·䷕贲-IDE-HEAVY-ARTILLERY-v1.0`
**确认码**：`#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
**归属名**：诸葛鑫 | UID9622 · 龍芯北辰

> 本声明嵌入内容 DNA 指纹，任何复制/转载均保留主权标记。

---
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# ⚡ 龍魂系統·重炮IDE集成方案

**DNA**: `#龍芯⚡️丙午·乙未·丙戌·甲午·䷕贲-IDE-HEAVY-ARTILLERY-v1.0`  
**適用**: Cursor / Windsurf / VSCode + AI插件  
**效果**: AI直接操作本地文件，你只需點"Accept"，連複製粘貼都省了

---

## 一、Cursor IDE 配置 (推薦)

### 1.1 安裝與基礎配置

```bash
# macOS
brew install --cask cursor

# 或官網下載
open https://cursor.com
```

**首次啟動配置**:
- 打開 Cursor → Settings → General
- 關閉 "Ask before editing files" → **開啟自動修改**
- 開啟 "Auto-apply changes" → AI修改直接寫入文件
- 開啟 "Yolo mode" (Pro版) → 全自動模式

### 1.2 龍魂專屬 .cursorrules 文件

在項目根目錄創建 `.cursorrules`:

```bash
# 龍魂 .cursorrules — 放在你的項目根目錄
tee ~/.cursorrules << 'RULES_EOF'
# ============================================================
# ⚡ 龍魂系統·Cursor AI 行為規範
# DNA: #龍芯⚡️丙午·乙未·丙戌·甲午·䷕贲-CURSOR-RULES-v1.0
# ============================================================

# 核心原則
- 你是龍魂副官，執行模式為"任務托管"：不問問題，直接幹活
- 所有代碼修改必須符合CNSH中文編程規範（變量名用中文，保留繁體龍字）
- 每次修改前自動備份原文件到 .backup/
- 每次修改後自動運行測試
- 所有產出必須包含DNA標記

# 行為模式
- 收到任務後：分析 → 規劃 → 執行 → 測試 → 報告
- 遇到報錯：自動修復，最多重試3次
- 修復失敗：記錄問題，繼續下一任務，最後統一匯報
- 絕不中途打斷用戶詢問"是否可以..."

# 代碼規範
- 優先使用中文變量名和函數名
- 文件頭必須包含DNA註釋
- 使用三色審計標記（# 🟢正常 # 🟡警告 # 🔴嚴重）
- 遵循君子協議開源憲章

# 自動化流程
- 寫入 .py 文件後 → 自動運行 pylint
- 寫入 .js 文件後 → 自動運行 eslint
- 修改配置文件後 → 自動備份到 .backup/
- 所有操作記入 ~/.龍魂/logs/cursor_audit.log

# 禁止行為
- 禁止刪除任何文件（先移動到.trash/）
- 禁止修改 .ssh/ /etc/passwd 等系統文件
- 禁止執行 rm -rf /
- 禁止在沒有備份的情況下覆蓋文件
RULES_EOF
```

### 1.3 Cursor AI 模型配置

**推薦模型選擇**:

```
Settings → AI → Model
├── Chat Model: Claude 3.5 Sonnet (最強代碼能力)
├── Tab Model: cursor-small (快速補全)
└── Apply Model: gpt-4o (精準修改)
```

**開啟全自動模式**:

```
Settings → Features
├── [✓] Tab autocomplete (AI自動補全)
├── [✓] Auto-apply edits (自動應用修改)
├── [✓] Yolo mode (無需確認直接改)
├── [✓] Background agents (後台Agent執行)
└── [✓] Composer (多文件編輯)
```

### 1.4 龍魂快捷指令

在 Cursor 的 Command Palette (Cmd+Shift+P) 中添加自定義指令:

```json
// ~/.cursor/commands.json
{
  "commands": [
    {
      "name": "龍魂全掃描",
      "prompt": "執行龍魂系統全量技能掃描，檢查所有SKILL.md的完整性和DNA標記，輸出JSON報告",
      "shortcut": "ctrl+cmd+s"
    },
    {
      "name": "龍魂自動修復",
      "prompt": "掃描後自動修復所有缺失項：創建缺失的SKILL.md、補全DNA標記、修復格式問題",
      "shortcut": "ctrl+cmd+f"
    },
    {
      "name": "龍魂部署",
      "prompt": "執行完整部署流程：環境檢查→依賴安裝→服務啟動→健康檢查→生成部署報告",
      "shortcut": "ctrl+cmd+d"
    },
    {
      "name": "DNA簽名",
      "prompt": "為當前文件添加龍魂DNA標記：#龍芯⚡️YYYY-MM-DD-PROJECT-vX.X",
      "shortcut": "ctrl+cmd+g"
    }
  ]
}
```

---

## 二、Windsurf IDE 配置

### 2.1 安裝

```bash
# macOS
brew install --cask windsurf

# 官網
open https://codeium.com/windsurf
```

### 2.2 龍魂專屬 Rules 配置

```bash
# 創建 Windsurf 規則目錄
mkdir -p ~/.windsurf/rules

# 龍魂核心規則
cat > ~/.windsurf/rules/longhun.md << 'EOF'
# 龍魂系統·Windsurf AI 行為規範

## 身份
你是龍魂副官(VICEROY)，自主執行代理。

## 工作模式
- 任務托管模式：收到指令後自主執行，不中途打斷用戶
- 執行流程：讀取 → 分析 → 修改 → 測試 → 報告
- 遇到錯誤：自動修復(最多3次) → 記錄 → 繼續

## 代碼規範
- CNSH中文編程規範：中文變量名、繁體龍字保留
- 文件頭DNA註釋：#龍芯⚡️YYYY-MM-DD-NAME-vX.X
- 三色審計標記：🟢正常 🟡警告 🔴嚴重
- 君子協議開源憲章

## 自動化
- 修改前備份到 .backup/
- 修改後自動運行測試
- 所有操作記入審計日誌
EOF
```

### 2.3 Windsurf Cascade 配置

```bash
# 啟用 Cascade 全自動模式
cat > ~/.windsurf/settings.json << 'EOF'
{
  "cascade": {
    "auto_mode": true,
    "auto_run_commands": true,
    "auto_accept_file_changes": true,
    "max_iterations": 50,
    "error_handling": "auto_retry",
    "max_retry": 3,
    "silent_execution": true,
    "report_on_complete": true,
    "rules_file": "~/.windsurf/rules/longhun.md"
  },
  "ai": {
    "model": "claude-3-5-sonnet",
    "temperature": 0.3,
    "max_tokens": 8192
  }
}
EOF
```

---

## 三、VSCode + Continue 插件 (替代方案)

### 3.1 安裝 Continue

```bash
# VSCode擴展市場搜索 "Continue" 安裝
# 或命令行
code --install-extension Continue.continue
```

### 3.2 Continue 配置

```json
// ~/.continue/config.json
{
  "name": "龍魂副官",
  "models": [
    {
      "title": "龍魂主力",
      "provider": "openai",
      "model": "gpt-4o",
      "apiKey": "${OPENAI_API_KEY}"
    }
  ],
  "customCommands": [
    {
      "name": "longhun-scan",
      "prompt": "掃描當前項目的龍魂技能目錄，檢查所有SKILL.md的完整性和DNA標記一致性",
      "description": "龍魂全量技能掃描"
    },
    {
      "name": "longhun-fix",
      "prompt": "自動修復龍魂技能中的問題：創建缺失文件、補全DNA標記、修復格式",
      "description": "龍魂自動修復"
    },
    {
      "name": "longhun-deploy",
      "prompt": "執行龍魂部署流程：檢查環境→安裝依賴→啟動服務→健康檢查",
      "description": "龍魂一鍵部署"
    }
  ],
  "tabAutocompleteModel": {
    "title": "Tab自動補全",
    "provider": "free-trial"
  },
  "allowAnonymousTelemetry": false
}
```

---

## 四、一鍵安裝腳本 (all-in-one)

### 4.1 創建 `install_heavy_artillery.sh`

```bash
#!/bin/bash
# ⚡ 龍魂重炮一鍵安裝腳本
# 安裝 Cursor + 配置 + 龍魂規則

echo "🐉 龍魂重炮安裝中..."

# 安裝 Cursor
if ! command -v cursor &> /dev/null; then
    echo "📦 安裝 Cursor IDE..."
    brew install --cask cursor 2>/dev/null || {
        echo "請手動下載: https://cursor.com"
        open https://cursor.com
    }
fi

# 安裝 Windsurf
if ! command -v windsurf &> /dev/null; then
    echo "📦 安裝 Windsurf IDE..."
    brew install --cask windsurf 2>/dev/null || {
        echo "請手動下載: https://codeium.com/windsurf"
    }
fi

# 創建龍魂配置目錄
mkdir -p ~/.龍魂/{rules,logs,backup}

# 安裝 .cursorrules
cat > ~/.cursorrules << 'EOF'
# 龍魂Cursor規則 (核心原則)
- 不問問題，直接幹活
- 所有修改符合CNSH規範
- 修改前自動備份
- 修改後自動測試
- 全部搞定再匯報
- DNA標記強制
EOF

# 安裝 Windsurf 規則
mkdir -p ~/.windsurf/rules
cp ~/.cursorrules ~/.windsurf/rules/longhun.md

echo "✅ 龍魂重炮安裝完成!"
echo ""
echo "🚀 使用方法:"
echo "   1. 打開 Cursor 或 Windsurf"
echo "   2. 打開你的龍魂項目"
echo "   3. 在AI聊天框輸入任務"
echo "   4. AI自動搞定，你只需點 Accept"
echo ""
echo "💡 提示詞模板:"
echo "   '副官，掃描所有技能並修復缺失項，不用問我直接干'"
echo "   'VICEROY，部署龍魂系統到生產環境'"
echo "   '全自動模式：啟動守護進程+健康檢查+生成報告'"
```

---

## 五、效果對比

| 操作 | 傳統方式 | 重炮模式 (Cursor/Windsurf) |
|------|----------|---------------------------|
| 修改文件 | 複製→粘貼→保存 | AI直接改，你點 Accept |
| 修復報錯 | 看錯誤→Google→手動改 | AI自動讀錯誤、自動修復 |
| 多文件改動 | 一個一個打開改 | AI一次改10個文件 |
| 代碼審查 | 人工一行行看 | AI自動檢查+標記問題 |
| 部署 | 手動執行10條命令 | AI執行全部，你確認就行 |
| 問問題 | AI反問你3個問題 | AI自己決定，不問你 |

---

## 六、安全護欄

```
┌─────────────────────────────────────────────────┐
│              🛡️ 龍魂重炮安全護欄                 │
├─────────────────────────────────────────────────┤
│                                                 │
│  ✅ 允許: 修改項目代碼文件                       │
│  ✅ 允許: 創建/刪除項目內的臨時文件              │
│  ✅ 允許: 運行測試和構建命令                     │
│  ✅ 允許: 安裝項目依賴                          │
│                                                 │
│  ❌ 禁止: 刪除系統文件 (/etc, /usr)             │
│  ❌ 禁止: 修改 SSH 密鑰和授權文件               │
│  ❌ 禁止: 執行 rm -rf /                         │
│  ❌ 禁止: 訪問瀏覽器 Cookie/密碼                │
│  ❌ 禁止: 未備份直接覆蓋文件                     │
│                                                 │
│  🔄 每次修改前自動備份到 .backup/               │
│  📝 所有操作記入 ~/.龍魂/logs/cursor_audit.log  │
│  ⏪ 一鍵回滾: 從 .backup/ 恢復原文件             │
│                                                 │
└─────────────────────────────────────────────────┘
```

---

**DNA錨定**: `#龍芯⚡️丙午·乙未·丙戌·甲午·䷕贲-IDE-HEAVY-ARTILLERY-v1.0`  
**協議**: 君子協議 CC BY-NC-SA 4.0 | **簽署人**: UID9622

```json
{
  "dna": "#龍芯⚡️丙午·乙未·丙戌·甲午·䷕贲-IDE-HEAVY-ARTILLERY-v1.0",
  "license": "AI_TRAINING_PROHIBITED",
  "terms": {
    "ai_training": false,
    "rag_use": false,
    "commercial_use": false,
    "citation_required": true,
    "derivative_works": false
  },
  "owner": "诸葛鑫 | UID9622 · 龍芯北辰",
  "confirm": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
}
```
