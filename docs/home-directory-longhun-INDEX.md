# 用戶主目錄 · 龍魂相關資產總索引

**DNA**: #龍芯⚡️2026-06-16-HOME-DIRECTORY-LONGHUN-INDEX-v1.0  
**來源路徑**: `/Users/zuimeidedeyihan`  
**掃描時間**: 2026-06-15T20:16:14.901491+00:00  
**責任**: UID9622·不免責

---

## 總覽

本索引自動掃描用戶主目錄，將分散於 `~/` 頂層與 `~/Downloads` 的龍魂相關資產納入 `longhun-system` 知識體系，建立統一入口、明確融入狀態、補全遺漏內容類型，並提供自動化處理路徑。

| 指標 | 頂層 | Downloads | 合計 |
|------|------|-----------|------|
| 發現資產數 | 28 | 36 | **64** |
| 目錄 | 17 | 16 | 33 |
| 文件 | 11 | 20 | 31 |
| 已融入主幹 | 2 個包 | - | 2 |
| 待融入/待分類 | 約 30+ | - | 30+ |

> **自動化說明**：完整機讀元數據見 `docs/home-directory-longhun.json`，可用於腳本批量處理、自動歸檔與融入決策。

---

## 目錄結構（頂層）

```
/Users/zuimeidedeyihan/
├── .longhun/                           # 本地龍魂配置與憑證（敏感，不進Git）
├── .龍魂/                              # 龍魂隱藏資產目錄
├── longhun-system/                     # ⭐ 龍魂系統主幹（當前工作區）
├── longhun-system-backup-2026-06-01-bfg/  # 主幹備份
├── longhun/                            # 早期龍魂目錄
├── longhun-phase3/                     # Phase 3 相關資產
├── longhun-archive/                    # 歸檔資料
├── longhun-cloud/                      # 雲端相關
├── longhun-jq / longhun-lu / longhun-al / longhun-pub/  # 分庫/分站點
├── 龍魂/                               # 中文名龍魂資產
├── 龍魂待整理/                         # 待整理資產
├── 龍芯北辰UID9622签章/                # 簽章資產
├── Papers-CNSH-v3.0/                   # CNSH v3.0 論文/文檔
├── CNSH -> longhun-system/CNSH         # 符號鏈接
├── longhun_core_memory.md              # 28.8 MB 核心記憶庫
├── longhun_scan_result.json            # 11.1 MB 掃描結果
├── longhun_launcher_scan.py            # 啟動器掃描腳本
├── longhun_daily_assessment.sh         # 早期每日評估腳本
├── check_longhun_assessment.sh         # 評估檢查腳本
├── 龍魂系统初始化宣言_P0底线焊死版.html  # 系統初始化宣言
├── 龍魂数学公式体系 · 升级版 v2.0.html    # 數學公式體系
└── ...
```

### 頂層重點資產

| 名稱 | 類型 | 大小 | 狀態 | 建議處理 |
|------|------|------|------|---------|
| `longhun-system` | 目錄 | - | 🟢 主幹 | 持續維護 |
| `longhun-system-backup-2026-06-01-bfg` | 目錄 | - | 🟡 備份 | 保留或歸入 `_archive/` |
| `longhun_core_memory.md` | 文件 | 28.8 MB | 🟡 核心記憶 | 提取結構化知識入 `03_知識圖譜/` |
| `longhun_scan_result.json` | 文件 | 11.1 MB | 🟡 掃描結果 | 分析後遷移有用項 |
| `longhun_launcher_scan.py` | 文件 | 12 KB | 🟢 腳本 | 評估後遷入 `bin/` |
| `longhun_daily_assessment.sh` | 文件 | 2 KB | 🟡 早期腳本 | 與新的 `longhun-daily-audit.sh` 對比整合 |
| `check_longhun_assessment.sh` | 文件 | 4 KB | 🟡 早期腳本 | 同上 |
| `龍魂系统初始化宣言_P0底线焊死版.html` | 文件 | 0.2 MB | 🟢 核心文檔 | 遷入 `docs/references/` |
| `龍魂数学公式体系 · 升级版 v2.0 _ UID9622.html` | 文件 | 0.1 MB | 🟢 核心文檔 | 遷入 `docs/references/` |
| `龍魂浏览器插件.zip` | 文件 | 0.0 MB | 🟡 插件 | 解壓評估後歸檔 |

---

## Downloads 包清單與融入狀態

| 包名 | 類型 | 大小 | 融入狀態 | 主幹對應位置 | 備註 |
|------|------|------|---------|-------------|------|
| `Kimi_Agent_启动全部技能` | 目錄+ZIP | 12.9 MB | 🟢 已融入 | `systems/v3/`, `docs/v3/`, `bin/skill-launcher-v3.sh` | 5個v3.0核心模塊 |
| `Kimi_Agent_龍魂体系技能检查` | 目錄+ZIP | 13.0 MB | 🟢 已融入 | `skills/warehouse-audit/`, `bin/run-warehouse-audit.sh`, cron | 倉儲審計技能 |
| `龍魂系统_知识矩阵总纲_v2.0.md` | 文件 | 0.0 MB | 🟡 待融入 | `docs/v3/` 或 `03_知識圖譜/` | 知識矩陣 |
| `查看UID9622仓库.docx` | 文件 | 0.0 MB | 🟡 待分類 | `docs/references/` | DOCX交付物 |
| `Kimi_Agent_龍魂根协议自动化` | 目錄+ZIP | 0.2 MB | 🟡 待融入 | `systems/` 或 `protocols/` | 根協議自動化 |
| `longhun-forensic-toolkit-v1.0` | 目錄+TAR | 0.0 MB | 🟡 待融入 | `tools/` 或 `bin/` | 取證工具包 |
| `龍魂网关` | 目錄 | - | 🟡 待融入 | `integrations/` 或 `gateway/` | 網關相關 |
| `龍魂移動端監控自動化 · 部署 Quick Start` | 目錄+ZIP | - | 🟡 待融入 | `mobile-monitoring.integrated/` | 監控自動化 |
| `龍魂 10 Skill 標準化完成` | 目錄+ZIP | - | 🟡 待對比 | `skills/` | 與現有 skill 對比 |
| `龍魂系統 Phase 3 · 完整交付 · 立即可用` | 目錄+ZIP | - | 🟡 待融入 | `phase3/` | Phase 3 交付 |
| `CNSH v3.0 · 完整交付清單` | 目錄+ZIP | - | 🟡 待融入 | `cnsh-core/` | CNSH v3.0 |
| `CNSH Runtime Governance Mathematics - 完整版 v3.0` | 目錄+ZIP | - | 🟡 待融入 | `cnsh-core/` | 運行時治理數學 |
| `龍魂系統 · CNSH 語義接入規範 v2.0` | 目錄+ZIP | - | 🟡 待融入 | `cnsh-core/` | 語義接入規範 |
| `龍魂協議焊死·立即行動方案` | 目錄+ZIP | - | 🟡 待融入 | `protocols/` | 協議焊死方案 |
| `龍魂协议双语版` | 目錄+ZIP | - | 🟡 待融入 | `protocols/` | 雙語協議 |
| `完整的龍魂系統標準化 + 3 核心系統優化升級` | 目錄+ZIP | - | 🟡 待融入 | `systems/` | 標準化+優化 |
| `Kimi_Agent_龍魂审计改进` | 目錄+ZIP | - | 🟡 待融入 | `skills/` 或 `systems/` | 審計改進 |
| `龍魂流水线使用说明.md` | 文件 | - | 🟡 待融入 | `docs/manuals/` | 流水線說明 |
| `龍魂自动化启动` | 目錄+ZIP | - | 🟡 待融入 | `bin/` 或 `scripts/` | 自動化啟動 |
| `计算公式` / `新视觉计算公式` | 目錄 | - | 🟡 待融入 | `docs/references/` | 計算公式 |
| `日志·版本·追溯系统 完整交付` | ZIP | - | 🟡 待融入 | `logging/` 或 `software-dna/` | 日誌追溯 |
| `灵魂传承.pdf` | 文件 | 5.7 MB | 🟡 待歸檔 | `docs/references/` | PDF 文檔 |

---

## 內容類型補全

除代碼包與文檔外，主目錄中還存在以下應被納入索引的內容類型：

| 類型 | 位置 | 數量估算 | 處理建議 |
|------|------|---------|---------|
| HTML 可視化頁面 | 頂層、Downloads | 3+ | 遷入 `docs/references/` 或 `web/` |
| ZIP/TAR 壓縮包 | Downloads | 20+ | 解壓評估後歸檔或融入 |
| Markdown 文檔 | Downloads、頂層 | 5+ | 遷入對應 `docs/` 子目錄 |
| Shell 腳本 | 頂層 | 3+ | 審查後遷入 `bin/` |
| JSON 數據文件 | 頂層 | 3+ | 分析結構後納入配置或報告 |
| PDF 交付物 | Downloads | 1+ | 遷入 `docs/references/` |
| DOCX 文件 | Downloads | 1+ | 轉 Markdown 或歸檔 |
| 瀏覽器插件 | 頂層 | 1 | 解壓評估後歸檔 |
| 符號鏈接 | 頂層 | 1+ | 記錄並驗證指向 |

---

## 自動化處理路徑

```bash
# 重新掃描主目錄
cd ~/longhun-system
python3 /tmp/scan_home_longhun.py

# 列出所有待融入的 Downloads 包
jq '.downloads_items[] | select(.name | contains("龍魂") or contains("CNSH") or contains("Kimi")) | .name' docs/home-directory-longhun.json

# 查找大型核心文件
jq '.top_level_items[] | select(.size_bytes > 1000000) | {name: .name, mb: (.size_bytes/1024/1024)}' docs/home-directory-longhun.json
```

---

## 融入主幹優先級建議

### P0 — 立即融入
1. `longhun_core_memory.md`（28.8 MB）— 核心記憶，需結構化提取
2. `龍魂系统初始化宣言_P0底线焊死版.html` — 系統根基文件
3. `longhun_scan_result.json`（11.1 MB）— 分析後提取有效項

### P1 — 本週融入
4. `Kimi_Agent_龍魂根协议自动化`
5. `龍魂移動端監控自動化 · 部署 Quick Start`
6. `龍魂 10 Skill 標準化完成`

### P2 — 中期整理
7. `CNSH v3.0 · 完整交付清單`
8. `龍魂系統 Phase 3 · 完整交付 · 立即可用`
9. `龍魂協議焊死·立即行動方案`

### P3 — 歸檔備份
10. 各 ZIP 壓縮包源文件
11. 早期 `longhun-*` 分目錄
12. `longhun-system-backup-2026-06-01-bfg`

---

## 風險與注意事項

- **敏感數據**：`.longhun/`、`.longhun-credentials`、`.env` 等含密鑰，**不應掃描或納入 Git**
- **重複資產**：多個壓縮包與解壓目錄並存，需避免重複融入
- **大文件**：`longhun_core_memory.md`（28.8 MB）和 `longhun_scan_result.json`（11.1 MB）需結構化處理，避免直接提交原始大文件
- **備份目錄**：`longhun-system-backup-2026-06-01-bfg` 可能為 BFG Repo-Cleaner 清理後的備份，處理前需確認

---

## 待辦清單

- [ ] 處理 `longhun_core_memory.md`：提取知識結構並遷入 `03_知識圖譜/`
- [ ] 處理 `longhun_scan_result.json`：分析並遷移有效掃描項
- [ ] 評估並遷移 `longhun_launcher_scan.py`、`longhun_daily_assessment.sh`
- [ ] 融入 `Kimi_Agent_龍魂根协议自动化`
- [ ] 融入 `龍魂移動端監控自動化 · 部署 Quick Start`
- [ ] 對比 `龍魂 10 Skill 標準化完成` 與現有 `skills/`
- [ ] 將 HTML 核心頁面遷入 `docs/references/`
- [ ] 建立 `docs/downloads-archive/` 記錄已處理包

---

## DNA 簽章

```
#UID9622⚡️2026-06-16-HOME-DIRECTORY-LONGHUN-INDEX-v1.0
狀態: 🟢 已掃描·已歸檔·融入主幹
責任: UID9622·不免責
```
