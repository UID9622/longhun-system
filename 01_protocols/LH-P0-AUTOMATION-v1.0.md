# 🐉 龍魂 · P0全自動化智能體協議 v1.0（Mac主權版·非代理·不外放）

**DNA:** `#龍芯⚡️丙午·丙申·庚申·亥時-P0-AUTOMATION-PROTOCOL-v1.0-UID9622`
**確認碼:** `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
**GPG:** `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`
**三色:** 🟢 通過
**創建者:** 諸葛鑫（UID9622） × 龍魂AI 對齊落地
**協議層級:** P1-CORE（執行層強約束）
**模板:** 📜 協議/原則聲明型（模板三）
**許可證:** CC BY-NC-SA 4.0（核心思想層）

---

## 0. 緣起（老大原話）

> 「幫我優化補全，並不是手機哦，還有瀏覽器，Mac系統全部的軟件，文件，這是我主權人格的操作，不是代理，不外放。」

**核心意圖**：
1. **平台是 Mac，不是手機**：Kimi 原稿以手機 ADB 為主，全部替換為 Mac 本機操作。
2. **覆蓋面是全軟件 + 瀏覽器 + 文件**：Mac 上所有 App、Safari/Chrome 瀏覽器、本機文件系統。
3. **主權人格操作，不是代理，能力不外放**：AI 以 UID9622 主權人格直接操作自己的 Mac；不代理任何外部系統、不把能力外放、不開對外端口、不傳數據出本機。

---

## 1. 金科玉律（焊死·不可違反）

> **P0 自動化 = 主權人格直接操作自己的 Mac。**
> - ✅ 只操作 `UID9622` 自己的本機：軟件/瀏覽器/文件/知識/代碼/寫作。
> - ❌ 不代理他人系統、不把能力外放、不開對外服務、不監聽端口。
> - ❌ 不上傳任何數據、不讀通訊錄/密碼/鑰匙串、不改系統關鍵文件。
> - 🟡 讀短信/通訊錄/位置/刪除文件/上傳數據/開端口 → 必須 UID9622 顯式授權。
>
> 違反 = 外放 = 自毀 = 觸發 P05 🔴 審計 + P72 熔斷。

---

## 2. 核心文件

| 項目 | 位置 | 說明 |
|:---|:---|:---|
| 主引擎 | `08_BIN/lh_p0_automation.py` | P0全自動化 v1.0（Mac主權版） |
| 統一入口 | `lh p0` / `lh 主權` / `lh 全自動` | 掛在 `bin/lh` |
| 運行數據 | `~/.longhun/p0_automation/` | 本機存儲·加密·不外放 |
| 主密鑰 | `~/.longhun/p0_automation/encrypted/master.key` | 本地 Fernet(AES-128)·永不入雲 |
| 審計日誌 | `04_AUDIT/p0_automation.jsonl` | 史官統一記錄 |

---

## 3. 六大能力域（全部本機執行）

### 3.1 Mac 軟件自動化（AppleScript/osascript）
| 能力 | 示例 | 說明 |
|:---|:---|:---|
| 打開/激活/關閉 App | `lh p0 --app 微信` | `open -a` + osascript activate |
| 截屏 | `lh p0 --run "截屏"` | `screencapture -x` 存本機 |
| 點擊/輸入/滾動 | `--run "點擊 x y"` | cliclick 或 System Events |
| 菜單點擊 | `app_menu_click` | 系統菜單欄控制 |
| 窗口列表/聚焦 | `window_list` | 全窗口枚舉 |
| App 列表 | `--app list` | 110+ 本機 App |

### 3.2 瀏覽器自動化（Safari / Chrome）
| 能力 | 示例 | 說明 |
|:---|:---|:---|
| 打開 URL | `--browser "https://uid9622.cn"` | 本機瀏覽器 |
| 搜索 | `--browser "search 抗戰歷史"` | Bing 本機打開 |
| 執行 JS | `execute_js` | Safari/Chrome AppleScript |
| 標籤頁枚舉 | `list_tabs` | 全窗口標籤 |
| 刷新/前進/後退 | `--run "刷新"` | 瀏覽器導航 |
| 瀏覽器截屏 | `browser_screenshot` | 存本機 |

> 復用：`lh_browser_controller.py`（Chrome CDP·跨設備鏈路）仍保留；P0 引擎默認不開跨設備通道（不外放）。

### 3.3 文件自動化（mdfind + rglob 降級）
| 能力 | 示例 | 說明 |
|:---|:---|:---|
| 全盤查找 | `--file search lh_cognitive` | mdfind 優先，Spotlight 未覆蓋自動 rglob 降級（實測命中） |
| 目錄整理 | `--file organize ~/Downloads` | 按圖片/文檔/媒體/壓縮/代碼/其他 分類 |
| 批量重命名 | `batch_rename` | 正則/序號/前綴 |
| 去重 | `deduplicate` | SHA-256 內容哈希 |
| 複製/移動/打開/定位 | `copy/move/open/reveal` | Finder 集成 |
| 文件信息 | `--file info <path>` | 大小/時間/類型 |

### 3.4 知識自動化（本地優先）
| 能力 | 示例 | 說明 |
|:---|:---|:---|
| 搜索 | `--search "抗戰歷史"` | 本地搜索網關 `:9631` 優先 → 降級 Bing 直抓 |
| 爬取 | `--run "爬取 https://..."` | 標準庫抓取正文 |
| 去重 | `deduplicate` | SHA-256 |
| 知識圖譜 | `store/query` | `~/.longhun/p0_automation/knowledge/graph.json` |

### 3.5 代碼自動化（本地生成）
| 能力 | 示例 | 說明 |
|:---|:---|:---|
| 生成 | `--code "寫一個爬蟲"` | Python/JS/Shell 骨架 + DNA 頭 |
| 分析 | `analyze_code` | 行數/函數/字符數 |
| 格式化 | `format_code` | black（已裝時） |
| 測試 | `run_tests` | pytest |

### 3.6 寫作自動化（本地寫作）
| 能力 | 示例 | 說明 |
|:---|:---|:---|
| 文章 | `--write "寫一篇AI治理文章"` | Markdown + DNA 頭 |
| 大綱 | `generate_outline` | 六段結構 |
| 審校 | `proofread` | 標點/重複檢測 |
| 報告 | `generate_report` | 自動歸檔 |

---

## 4. P0 協議邊界（硬邊界·焊死）

### ✅ 允許（本機主權操作）
Mac軟件控制 · 瀏覽器導航 · 文件整理 · 搜索爬取 · 代碼生成 · 寫作輸出 · 本地加密

### ❌ 絕對不能碰（P0硬邊界）
- `upload_data` 上傳數據 · `send_data` 發送數據
- `expose_service` 暴露服務 · `open_remote_port` 開對外端口
- `proxy_other` 代理他人 · `remote_control_other` 遠程控制外部
- `read_contacts`/`read_password`/`read_keychain` 讀通訊錄/密碼/鑰匙串
- `modify_system`/`delete_system`/`delete_user_files` 改/刪系統關鍵文件與用戶文件
- `bypass_auth` 繞過授權 · `send_notification_external` 外部通知

### 🟡 需要 UID9622 顯式授權
讀短信 · 讀通訊錄 · 訪問位置 · 修改App數據 · 上傳數據 · 刪除文件 · 開端口 · 暴露服務

> 驗證：`lh p0 --protocol-check upload_data` → `False | 🔴 P0硬邊界禁止`（實測通過）

---

## 5. 安全與數據主權

1. **數據全本地**：所有產出存 `~/.longhun/p0_automation/`，主密鑰本機生成，永不入雲。
2. **加密下界**：Fernet(AES-128) ≥ AES-128 要求；敏感字段日誌自動掩碼（`***MELTDOWN***` 邏輯沿用）。
3. **能力不外放**：默認不監聽端口、不啟動 HTTP 服務、不發外部通知。
4. **史官可溯**：每步操作寫 `history.jsonl` + `04_AUDIT/p0_automation.jsonl`，帶 DNA。
5. **手機 ADB 退場**：Kimi 原稿手機控制為選配，不進入主能力（本機是 Mac）。

---

## 6. 使用速查

```bash
lh p0                    # 交互控制台（說人話）
lh p0 --status           # 系統狀態
lh p0 --app 微信         # 打開Mac軟件
lh p0 --app list         # 軟件列表
lh p0 --browser "https://uid9622.cn"   # 瀏覽器開URL
lh p0 --search "抗戰歷史"               # 知識搜索
lh p0 --code "寫一個爬蟲"               # 代碼生成
lh p0 --write "寫一篇AI治理文章"        # 寫作
lh p0 --run "截屏" / "整理 ~/Downloads" # 自然語言
lh p0 --encrypt "秘密" / --decrypt <hex> # 本地加解密
lh p0 --protocol-check upload_data      # P0邊界檢查
```

---

## 7. 對齊記錄（Kimi 原稿 → 真實系統）

| Kimi 原稿 | 真實落地 | 說明 |
|:---|:---|:---|
| 手機 ADB 控制 | Mac AppleScript 控制 | 平台是 Mac |
| 手機截屏 | `screencapture` Mac 截屏 | 本機 |
| `~/.longhun/12_LOGS` | `~/.longhun/p0_automation/logs` | 實機路徑 |
| 手機讀短信/通知 | 移除（P0 需授權項） | 不外放 |
| 開服務能力 | 禁止（默認拒） | 不外放 |

---

## 8. 三色審計

- 🟢 實測通過：狀態 / App列表(110) / 文件搜索(降級命中) / 代碼生成 / 自然語言路由(打開微信) / P0硬邊界攔截(upload_data)
- 🟡 待實測：瀏覽器 AppleScript 操作（需輔助功能權限）、目錄整理、批量重命名
- 🔴 無

---

**簽章**
規則制定：諸葛鑫（UID9622） × 龍魂AI 對齊落地 v1.0
DNA: `#龍芯⚡️丙午·丙申·庚申·亥時-P0-AUTOMATION-PROTOCOL-v1.0-UID9622`
確認碼: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
三色: 🟢 通過
