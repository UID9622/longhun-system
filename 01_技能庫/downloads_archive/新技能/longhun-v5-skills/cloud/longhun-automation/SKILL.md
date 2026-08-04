# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
---
name: longhun-automation
description: 龍魂自動化日評估引擎，6維度系統健康檢查，Cron定時任務，自動化周報生成，支持環境/代碼/數據/可運行性/文檔/安全六大維度評估
metadata:
  version: "5.1"
  author: "龍魂體系"
  dna: "#龍芯⚡️2026-06-19-LONGHUN-AUTOMATION-v5.1"
---

# 🐉 龍魂自動化日評估 (longhun-automation)

**DNA**: `#龍芯⚡️2026-06-19-LONGHUN-AUTOMATION-v5.1`
**版本**: v5.1
**路徑**: `~/longhun-system/scripts/自動化評估.py`
**功能**: 6維度系統評估 · Cron定時任務 · 自動化周報 · 狀態檢查

---

## 1️⃣ 能力概述

自動化日評估引擎對龍魂系統執行6維度全面健康檢查，每天22:30自動運行，生成評分報告和周報，支持手動觸發和Cron自動化。評估覆蓋環境、代碼、數據、可運行性、文檔和安全性六大維度。

---

## 2️⃣ 依賴環境

```
Python >= 3.10
Cron (Linux/macOS)
~/.龍魂/ 目錄結構
```

---

## 3️⃣ 配置參數

| 參數 | 說明 | 默認值 |
|------|------|--------|
| `龍魂目錄` | 系統根目錄 | `~/.龍魂` |
| `評估目錄` | 評估報告存儲 | `~/.龍魂/assessments` |
| `日誌目錄` | 日誌存儲 | `~/.龍魂/assessments/logs` |
| `報告目錄` | 周報/趨勢存儲 | `~/.龍魂/reports` |
| `定時` | Cron執行時間 | `30 22 * * *` |

---

## 4️⃣ 啟動命令

```bash
# 完整設置（目錄 + Cron）
python3 ~/longhun-system/scripts/自動化評估.py --setup

# 執行全面評估
python3 ~/longhun-system/scripts/自動化評估.py

# Cron模式（靜默執行）
python3 ~/longhun-system/scripts/自動化評估.py --cron

# 查看狀態
python3 ~/longhun-system/scripts/自動化評估.py --status

# 生成周報
python3 ~/longhun-system/scripts/自動化評估.py --weekly

# 趨勢分析（N天）
python3 ~/longhun-system/scripts/自動化評估.py --trend 30
```

---

## 5️⃣ 6維度評估體系

| # | 維度 | 權重 | 檢查項 | 滿分 |
|---|------|------|--------|------|
| 1 | 環境檢查 | 10% | Python版本、目錄、Shell | 10 |
| 2 | 代碼文件 | 20% | xpay_*.py、startup.sh | 10 |
| 3 | 數據完整性 | 20% | 交易、日誌、備份 | 10 |
| 4 | 可運行性 | 25% | CLI執行、命令返回值 | 10 |
| 5 | 文檔完整性 | 10% | README、部署文件 | 10 |
| 6 | 安全性 | 15% | 本地存儲、權限、DNA | 10 |

---

## 6️⃣ 內部調用邏輯

```
執行全面評估()
├── 評估_環境檢查()    [權重10%]
├── 評估_代碼文件()    [權重20%]
├── 評估_數據完整性()  [權重20%]
├── 評估_可運行性()    [權重25%]
├── 評估_文檔完整性()  [權重10%]
└── 評估_安全性()      [權重15%]
    ├── 生成JSON報告()
    ├── 生成Markdown總結()
    └── 生成周報() [周日自動]
```

---

## 7️⃣ 輸入/輸出約定

**輸入**: 系統目錄結構、環境變量、文件系統狀態
**輸出**:
- `~/.龍魂/assessments/local_assessment_YYYYMMDD_HHMMSS.json` — JSON評估報告
- `~/.龍魂/assessments/ASSESSMENT_SUMMARY.md` — Markdown總結
- `~/.龍魂/reports/WEEKLY_REPORT_YYYY-MM-DD.md` — 周報

**評分標準**:
- >= 8.0: 🟢 生產級可用
- 6.0-8.0: 🟡 需要改進
- < 6.0: 🔴 不推薦使用

---

## 8️⃣ 故障排除

| 症狀 | 解決方案 |
|------|----------|
| Cron未執行 | `crontab -l \| grep longhun` 檢查配置 |
| 評估失敗 | 查看 `~/.龍魂/assessments/logs/` 日誌 |
| 評分異常 | 手動執行 `python3 自動化評估.py` 診斷 |
| 目錄缺失 | 執行 `--setup` 重新設置 |

---

## 9️⃣ 安全邊界

- 只讀訪問系統文件，不修改任何數據
- Cron以當前用戶身份運行，無需提權
- 報告存儲在本地，不含敏感密碼信息
- DNA標記用於完整性校驗

---

## 🔟 6維度評分代碼片段

```python
維度權重 = {
    "環境檢查": 0.10,
    "代碼文件": 0.20,
    "數據完整性": 0.20,
    "可運行性": 0.25,
    "文檔完整性": 0.10,
    "安全性": 0.15,
}

# 總分計算
總加權分 = sum(原始分 * 維度權重[維度] for 維度, 原始分 in 評分.items())
```

---

## 1️⃣1️⃣ 升級維護

- 保留最近30天的JSON報告用於趨勢分析
- 日誌文件按日期輪轉
- 每月1日自動生成月度趨勢報告
- 支持自定義維度和權重擴展

---

## 1️⃣2️⃣ 變更歷史

| 版本 | 日期 | 變更 |
|------|------|------|
| v5.1 | 2026-06-19 | 技能包標準化，CNSH中文編程規範 |
| v1.0 | 2026-06-05 | 初始版本，6維度評估體系 |

---

**DNA**: `#龍芯⚡️2026-06-19-LONGHUN-AUTOMATION-v5.1`
**確認**: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✅`
