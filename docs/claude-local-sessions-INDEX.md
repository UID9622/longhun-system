# Claude Local Agent Mode Sessions · 目錄索引

**DNA**: #龍芯⚡️2026-06-16-CLAUDE-SESSIONS-INDEX-v1.0  
**來源路徑**: `/Users/zuimeidedeyihan/Library/Application Support/Claude/local-agent-mode-sessions`  
**掃描時間**: 2026-06-15T20:01:05.742530+00:00  
**責任**: UID9622·不免責

---

## 總覽

本索引自動掃描 Claude Desktop 本地代理模式會話目錄，將分散的會話文件、HTML 工件與插件資源納入 `longhun-system` 知識體系，方便後續查找、回溯與自動化處理。

| 指標 | 數值 |
|------|------|
| 頂層會話/文件夾 | 5 個 |
| 發現文件總數 | 2,076 個 |
| HTML 工件 | 66 個 |
| Markdown 文檔 | 260 個 |
| Python 腳本 | 349 個 |
| 字體/資源 | 270 個 |
| JSON/JSONL | 147 個 |
| 其他 | 994 個 |

> **自動化說明**：完整機讀元數據見同目錄 `claude-local-sessions.json`，可由後續腳本加載、搜索與同步。

---

## 目錄結構

```
local-agent-mode-sessions/
├── 21488a5a-cc58-4eb9-9d63-7ad4997159db/   # 會話目錄（輕量）
├── 30d8b41e-a62b-4651-84e2-f8919e07359b/   # 會話目錄
├── a89d76ba-6216-42b3-ba33-e18194ebb230/   # 會話目錄（含大量產出）
├── skills-plugin/                          # Claude Skills 插件資源
└── 终极流场/                               # 龍魂流場 HTML 工件集合
```

### 文件夾詳情

| 文件夾 | 文件數 | 說明 | 狀態 |
|--------|--------|------|------|
| `终极流场` | 9 | 龍魂流場系列可視化入口頁面 | 🟢 核心工件 |
| `skills-plugin` | 1,702 | Claude Skills 插件運行時資源（字體、XSD、腳本等） | 🟡 運行時依賴 |
| `a89d76ba-...` | 353 | 某次會話產出（多格式） | 🟡 待分類 |
| `30d8b41e-...` | 11 | 會話快照/記錄 | 🟡 待分類 |
| `21488a5a-...` | 1 | 會話殘留文件 | 🟡 待清理 |

---

## 核心 HTML 工件目錄

`终极流场/` 文件夾保存了龍魂系統的可視化入口與流場頁面，是當前最值得重點維護的區域。

| 文件名 | 標題 | 版本 | 標籤 | 大小 | 狀態 |
|--------|------|------|------|------|------|
| `dragon-core.html` | UID9622 · 龍魂入口 | v1.0 | `入口` `核心` `UID9622` | 4.3 KB | 🟢 就緒 |
| `longhun_fixed_point_v1.html` | 🐉 龍魂不动点·固定宝宝 v1.0 | v1.0 | `不動點` `固定寶寶` `元知` | 33.9 KB | 🟢 就緒 |
| `longhun_flow_portal_v2.html` | 🐉 龍魂流場 · 元世界入口 · UID9622 | v2.0 | `流場` `入口` `元世界` | 32.1 KB | 🟢 就緒 |
| `longhun-flow-field-v10.html` | 🐉 龍魂流場 · 不動點透視圖 v10 · CNSH v1.1 · UID9622 | v10 | `流場` `不動點` `CNSH` | 35.1 KB | 🟢 就緒 |
| `longhun-sandbox-dropzone-v1.2-local.html` | 龍魂沙盒分拣台 v1.2（本地页） | v1.2 | `沙盒` `分揀` `本地` | 17.6 KB | 🟢 就緒 |
| `longhun-unified-v10.html` | 🐲 龍魂統一流場 v10 · LH-CDNA v1.2 · UID9622 | v10 | `統一流場` `CDNA` | 78.1 KB | 🟢 就緒 |
| `longhun-unified-v10_副本.html` | 🐲 龍魂統一流場 v10.1 · LH-CDNA v1.2 · 流場架构图 · UID9622 | v10.1 | `統一流場` `CDNA` `副本` | 93.2 KB | 🟢 就緒 |
| `longhun-unified-v9.html` | 🐲 龍魂統一流場 v9 · 洛書渦流×三才軌道 · UID9622 | v9 | `統一流場` `洛書` `三才` | 59.5 KB | 🟢 就緒 |
| `龍魂流场20260426l.html` | 🐉 龍魂流場 · 元世界入口 · UID9622 | 2026-04-26 | `流場` `入口` `早期版` | 23.7 KB | 🟡 存檔 |

### 版本演進鏈

```
龍魂流场20260426l.html (2026-04-26)
    ↓
longhun_flow_portal_v2.html (v2)
    ↓
longhun-fixed-point_v1.html (v1) + longhun-flow-field-v10.html (v10)
    ↓
longhun-unified-v9.html (v9)
    ↓
longhun-unified-v10.html (v10) ── longhun-unified-v10_副本.html (v10.1)
    ↓
dragon-core.html (入口匯總)
    ↓
longhun-sandbox-dropzone-v1.2-local.html (本地分揀台)
```

---

## 內容類型補全

除上述 HTML 工件外，會話目錄中還包含以下應被納入索引的內容類型：

| 類型 | 數量 | 處理建議 |
|------|------|---------|
| `.md` 文檔 | 260 | 提取標題與標籤，納入知識圖譜 |
| `.py` 腳本 | 349 | 識別入口函數，評估是否遷移至 `systems/` 或 `bin/` |
| `.json/.jsonl` | 147 | 結構化數據，可用於配置/審計追溯 |
| `.sh` 腳本 | 24 | 審查後納入 `bin/` 或文檔化 |
| `.txt` 純文本 | 241 | 多為日誌/輸出，按會話歸檔 |
| `.pdf` | 14 | 重要交付物，建議遷移至 `docs/references/` |
| `.png/.mp4` | 4 | 截圖/錄屏，建議遷移至 `docs/v3/screenshots/` 或類似目錄 |
| `.swift` | 13 | 可能為 iOS/原生工具原型，需單獨評估 |
| `.xsd/.xml/.ttf` | 885 | 多為 `skills-plugin` 運行時資源，通常無需遷移 |

---

## 與 longhun-system 主幹的關聯

| 本地會話產出 | 主幹對應位置 | 備註 |
|-------------|-------------|------|
| `终极流场/*.html` | `web/`、`docs/references/` | 可視化入口，可嵌入 Phase 3 Web UI |
| 會話中的 `.py` 腳本 | `systems/v3/`、`bin/`、`skills/py-skills/` | 已吸收 5 個 v3.0 核心模塊 |
| 會話中的 `.md` 文檔 | `docs/v3/`、`06_技術文檔/` | 知識矩陣與接口契約 |
| `.pdf` 交付物 | `docs/references/` | 證書/報告 |
| 截圖/錄屏 | `docs/v3/screenshots/` | 已複製 5 張 skill 截圖 |

---

## 自動化維護命令

```bash
# 重新掃描並更新 JSON 索引
cd ~/longhun-system
python3 - << 'PY'
import json, subprocess
subprocess.run(["python3", "/tmp/generate_sessions_index.py"], check=True)
print("索引已更新")
PY

# 列出所有 HTML 工件
jq '.artifacts[] | select(.filename | endswith(".html")) | {file: .filename, title: .title}' docs/claude-local-sessions.json

# 查找某個關鍵詞
jq '.artifacts[] | select(.title | contains("流場")) | .absolute_path' docs/claude-local-sessions.json
```

---

## 待辦與風險

- [ ] 清理 `21488a5a-...` 等空會話殘留文件夾
- [ ] 將 `终极流场/` 中 v9/v10 版本統一，避免 `_副本` 長期並存
- [ ] 評估 `a89d76ba-...` 會話產出的 353 個文件，識別可遷移至主幹的內容
- [ ] 為 `skills-plugin/` 建立獨立備份策略（運行時依賴，不進 Git）
- [ ] 將 `.pdf` 與媒體文件遷移至 `docs/references/` 並更新本索引

---

## DNA 簽章

```
#UID9622⚡️2026-06-16-CLAUDE-SESSIONS-INDEX-v1.0
狀態: 🟢 已掃描·已歸檔·融入主幹
責任: UID9622·不免責
```
