---
name: longhun-review
description: '龍魂每日復盤引擎，三色審計體系，支持郵件發送和日曆記錄，包含歷史趨勢追蹤和改進建議生成，覆蓋文件/安全/心跳/測試/日誌/評估/API/備份八大審計項。服務老百姓與系統治理，符合中國審計標準，每日自動審計復盤。'
metadata:
  version: '5.1'
  author: 龍魂體系
  dna: '#龍芯⚡️2026-07-03-LONGHUN-REVIEW-v5.1'
  id: longhun-review
  trigger:
    keywords:
    - review
    - 龍魂每日復盤引擎
    - 三色審計體系
    - 支持郵件發送和日曆記錄
    - 包含歷史趨勢追蹤和改進建議生成
    - 覆蓋文件/安全/心跳/測試/日誌/評估/API/備份八大審計項
    context: longhun-review 相关操作
  category: general
---
# 🐉 龍魂每日復盤引擎 (longhun-review)

**DNA**: `#龍芯⚡️2026-06-19-LONGHUN-REVIEW-v5.1`
**版本**: v5.1
**路徑**: `~/longhun-system/scripts/復盤引擎.py`
**功能**: 三色審計 · 郵件發送 · 復盤報告 · 歷史趨勢 · 改進建議

---

## 1️⃣ 能力概述

每日復盤引擎執行8項三色審計檢查，生成綜合復盤報告，支持郵件通知和日曆記錄。三色體系（🟢通過 🟡警告 🔴失敗）提供直觀的系統健康狀態評估，並基於歷史數據生成趨勢分析和改進建議。

---

## 2️⃣ 依賴環境

```
Python >= 3.10
pip-audit (安全審計)
pytest (測試框架)
Gmail SMTP (郵件通知)
macOS Calendar (日曆寫入，可選)
```

---

## 3️⃣ 配置參數

| 參數 | 環境變量 | 說明 |
|------|----------|------|
| 郵件發件人 | `LONGHUN_GMAIL` | Gmail地址 |
| 郵件密碼 | `LONGHUN_GMAIL_APPPW` | Gmail App密碼 |
| 郵件收件人 | `LONGHUN_EMAIL_TO` | 收件地址（默認同發件人） |
| 定時 | LaunchAgent/Cron | 每天23:30 |

---

## 4️⃣ 啟動命令

```bash
# 完整設置
python3 ~/longhun-system/scripts/復盤引擎.py --setup

# 執行復盤
python3 ~/longhun-system/scripts/復盤引擎.py

# Cron模式（自動發郵件）
python3 ~/longhun-system/scripts/復盤引擎.py --cron

# 發送郵件報告
python3 ~/longhun-system/scripts/復盤引擎.py --email

# 趨勢分析（N天）
python3 ~/longhun-system/scripts/復盤引擎.py --trend 30

# 分析三色審計日誌
python3 ~/longhun-system/scripts/復盤引擎.py --analyze-logs

# 安裝LaunchAgent (macOS)
python3 ~/longhun-system/scripts/復盤引擎.py --install-agent
```

---

## 5️⃣ 三色審計體系

| # | 審計項 | 說明 |
|---|--------|------|
| 1 | 文件完整 | 核心文件存在性檢查 |
| 2 | 安全(魯班) | pip-audit 漏洞掃描 |
| 3 | 系統心跳 | KFPP DB記錄數 |
| 4 | 測試 | pytest 測試通過率 |
| 5 | 操作日誌 | action_log.jsonl 統計 |
| 6 | 評估報告 | 日評估報告生成狀態 |
| 7 | API服務 | 服務端口健康檢查 |
| 8 | 備份狀態 | 備份文件存在性 |

---

## 6️⃣ 內部調用邏輯

```
執行全面復盤()
├── 審計_文件完整性()   → 三色結果
├── 審計_安全性()       → pip-audit
├── 審計_系統心跳()     → DB統計
├── 審計_測試狀態()     → pytest
├── 審計_操作日誌()     → action_log.jsonl
├── 審計_評估報告()     → 日評分報告
├── 審計_API服務()      → 端口檢查
└── 審計_備份狀態()     → 備份文件
    ├── 生成復盤報告()   → JSON + Markdown
    ├── 生成改進建議()   → 基於🔴🟡項
    ├── 發送復盤郵件()   → Gmail SMTP
    └── 寫入日曆()      → macOS Calendar
```

---

## 7️⃣ 輸入/輸出約定

**輸入**: 系統文件狀態、日誌文件、環境變量
**輸出**:
- `~/.龍魂/reviews/daily_review_YYYYMMDD_HHMMSS.json` — JSON復盤數據
- `~/.龍魂/reviews/daily_review_YYYY-MM-DD.md` — Markdown復盤報告
- `~/.龍魂/reports/REVIEW_TREND_YYYY-MM-DD.md` — 趨勢報告

**三色評級**:
- 🟢 通過數 > 警告數+失敗數: 系統正常
- 🟡 警告數 > 總數/3: 需改進
- 🔴 失敗數 > 0: 需立即關注

---

## 8️⃣ 故障排除

| 症狀 | 解決方案 |
|------|----------|
| pip-audit未找到 | `pip3 install pip-audit` |
| pytest未找到 | `pip3 install pytest` |
| 郵件發送失敗 | 檢查 LONGHUN_GMAIL 環境變量 |
| 日曆寫入失敗 | 確認「龍魂」日曆存在 |
| LaunchAgent未執行 | `launchctl list \| grep daily-review` |

---

## 9️⃣ 安全邊界

- 郵件密碼通過環境變量或Keychain存儲
- pip-audit只讀掃描，不修改依賴
- 日誌分析本地執行，不上傳數據
- 所有文件操作限制在~/.龍魂目錄內

---

## 🔟 三色審計核心代碼

```python
@dataclass
class 三色結果:
    顏色: str      # 🟢 🟡 🔴
    狀態: str      # 通過/警告/失敗
    詳情: str
    分值: float = 0.0  # 0-10

def 審計_文件完整性() -> 三色結果:
    核心文件 = [xpay_cli.py, xpay_core.py, xpay_db.py, startup.sh]
    存在數 = sum(1 for f in 核心文件 if f.exists())
    if 存在數 == len(核心文件):
        return 三色結果("🟢", "通過", f"核心文件齊 {存在數}/{總數}", 10.0)
    elif 存在數 >= 總數 // 2:
        return 三色結果("🟡", "警告", f"核心文件缺失 {總數 - 存在數} 個", 5.0)
    else:
        return 三色結果("🔴", "失敗", f"核心文件嚴重缺失", 2.0)
```

---

## 1️⃣1️⃣ 升級維護

- 復盤數據保留用於歷史趨勢分析
- 支持自定義審計項擴展
- 郵件模板可定制
- 趨勢報告自動生成（月初）

---

## 1️⃣2️⃣ 變更歷史

| 版本 | 日期 | 變更 |
|------|------|------|
| v5.1 | 2026-06-19 | 技能包標準化，CNSH中文編程規範 |
| v1.0 | 2026-06-09 | 初始版本，三色審計體系 |

---

**DNA**: `#龍芯⚡️2026-06-19-LONGHUN-REVIEW-v5.1`
**確認**: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✅`

---

## 标准声明

本技能遵循《龍魂系统宪法》、中华人民共和国法律法规，以及 UID9622 制定的治理标准。

- **中国标准**：数据主权留在中国境内，优先采用国产技术栈，支持自主可控。
- **老百姓标准**：保护普通用户权益，不贴标签、不滥用数据、不制造信息差，服务人民与老百姓。
- **DNA 追溯**：所有输出均携带 DNA 追溯码，来源可查、去向可追、责任可究。

