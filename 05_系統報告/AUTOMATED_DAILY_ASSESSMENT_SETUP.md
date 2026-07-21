# 🐉 龍魂系統 · 自動化日評估 · 完整設定指南

**設定日期**: 2026-06-05 19:15 CST
**DNA**:#龍芯⚡️2026-06-05-AUTOMATED-ASSESSMENT-v1.0
**責任**: UID9622 (Claude Code)

---

## ✅ 已部署組件

### 1️⃣ 評估引擎
```
文件: ~/local_assessment_engine.py
大小: 16 KB
功能: 執行 6 維度系統評估
狀態: ✅ 就緒
```

### 2️⃣ Cron 執行腳本
```
文件: ~/longhun_daily_assessment.sh
大小: 1.9 KB
功能: Cron 任務包裝、日誌管理
狀態: ✅ 就緒
```

### 3️⃣ 狀態檢查工具
```
文件: ~/check_longhun_assessment.sh
大小: 2.1 KB
功能: 快速評估狀態查詢
狀態: ✅ 就緒
```

### 4️⃣ Cron 任務
```
配置: 30 22 * * * /bin/bash /Users/zuimeidedeyihan/longhun_daily_assessment.sh
時間: 每天 22:30 (下午 10:30)
狀態: ✅ 已啟用
```

### 5️⃣ 報告目錄
```
位置: ~/.龍魂/assessments/
子目錄: logs/
狀態: ✅ 已創建
```

---

## 📊 評估維度 (6 個)

| # | 維度 | 檢查項目 | 權重 | 滿分 |
|---|------|---------|------|------|
| 1 | 環境檢查 | Python版本、目錄、Shell | 10% | 10.0 |
| 2 | 代碼文件 | xpay_*.py、startup.sh 等 | 20% | 10.0 |
| 3 | 數據完整性 | 交易、日誌、備份 | 20% | 10.0 |
| 4 | 可運行性 | CLI 執行、命令返回值 | 25% | 10.0 |
| 5 | 文檔完整性 | README、部署文件 | 10% | 10.0 |
| 6 | 安全性 | 本地存儲、權限、DNA | 15% | 10.0 |

---

## 🚀 快速開始

### 方式 1: 查看評估狀態
```bash
bash ~/check_longhun_assessment.sh
```

### 方式 2: 手動運行評估
```bash
python3 ~/local_assessment_engine.py
```

### 方式 3: 查看最新報告
```bash
cat ~/.龍魂/assessments/ASSESSMENT_SUMMARY.md
```

### 方式 4: 提取評分
```bash
python3 -c "
import json, glob
f = sorted(glob.glob('$HOME/.龍魂/assessments/local_assessment_*.json'))[-1]
d = json.load(open(f))
print(f'評分: {d[\"total_score\"]}/10')
print(f'狀態: {d[\"status\"]}')
"
```

---

## ⏱️ 執行時間表

### 每日執行流程

```
22:00 │ 系統通知: 今日對話歸檔
      │
22:30 │ ⭐ 龍魂系統自動化日評估 (Cron)
      │   • 檢查環境
      │   • 檢查代碼
      │   • 驗證數據
      │   • 執行可運行性測試
      │   • 生成報告 (~3-5 分鐘)
      │
23:00 │ 龍魂每日復盤 (daily_review.py)
      │   • 檢查文件完整性
      │   • 檢查安全性
      │   • 檢查測試
      │   • 生成三色審計
      │   • 發送郵件
      │
23:30 │ 完成
```

---

## 📁 文件結構

```
~/ (用戶主目錄)
├── local_assessment_engine.py          (評估引擎)
├── longhun_daily_assessment.sh         (Cron 執行腳本)
├── check_longhun_assessment.sh         (狀態檢查工具)
│
└── .龍魂/
    └── assessments/
        ├── local_assessment_YYYYMMDD_HHMMSS.json  (評估報告)
        ├── ASSESSMENT_SUMMARY.md                  (文本總結)
        ├── CRON_SETUP.md                          (設定詳情)
        └── logs/
            ├── daily_assessment_YYYYMMDD_HHMMSS.log (執行日誌)
            └── ...
```

---

## 🔍 監控與維護

### 日常檢查 (推薦每天檢查一次)
```bash
# 快速檢查狀態
bash ~/check_longhun_assessment.sh

# 查看評分
python3 -c "
import json, glob
f = sorted(glob.glob('$HOME/.龍魂/assessments/local_assessment_*.json'))[-1]
print(json.load(open(f))['total_score'])" | xargs -I {} echo "評分: {}/10"
```

### 每週檢查 (推薦每週檢查一次)
```bash
# 查看評分趨勢
for f in $(ls -t ~/.龍魂/assessments/local_assessment_*.json | head -7); do
    score=$(python3 -c "import json; print(json.load(open('$f'))['total_score'])")
    date=$(basename $f | cut -d_ -f3-4)
    echo "$date: $score/10"
done

# 查看最近的改進項目
cat ~/.龍魂/assessments/ASSESSMENT_SUMMARY.md | grep -A 10 "可改進項目"
```

### 定期清理 (推薦每月執行一次)
```bash
# 保留最近 30 天的報告
find ~/.龍魂/assessments -name "local_assessment_*.json" -mtime +30 -delete

# 保留最近 30 天的日誌
find ~/.龍魂/assessments/logs -name "*.log" -mtime +30 -delete
```

---

## 🔧 故障排查

### 症狀 1: 沒有自動執行
**檢查**:
```bash
# 查看 Cron 任務
crontab -l | grep longhun_daily_assessment

# 查看系統日誌
log stream --predicate 'process == "cron"' --level debug | head -20
```

**解決**:
```bash
# 重新添加 Cron 任務
(crontab -l 2>/dev/null; echo "30 22 * * * /bin/bash $HOME/longhun_daily_assessment.sh") | crontab -
```

### 症狀 2: 評估失敗
**檢查**:
```bash
# 查看執行日誌
tail -50 ~/.龍魂/assessments/logs/daily_assessment_*.log

# 手動運行評估
python3 ~/local_assessment_engine.py
```

### 症狀 3: 報告評分異常
**檢查**:
```bash
# 驗證系統狀態
ls -la ~/.龍魂/xpay/
python3 ~/.龍魂/xpay/xpay_cli.py stats

# 檢查文件是否完整
python3 ~/local_assessment_engine.py
```

---

## 📊 典型輸出

### 評估報告
```json
{
  "total_score": 9.7,
  "max_score": 10.0,
  "status": "✅ 生產級可用",
  "assessments": [
    {
      "category": "環境檢查",
      "score": 10.0,
      "results": {...}
    },
    ...
  ]
}
```

### 執行日誌
```
════════════════════════════════════════════════════════════
🐉 龍魂系統 · 自動化日評估
時間: 2026-06-06 22:30:15
════════════════════════════════════════════════════════════

【環境檢查】
  評分: 10.0/10 (權重 10%)
  • python_version: Python 3.14.3
  • longhun_dir: /Users/.../​.龍魂
  • xpay_dir: /Users/.../​.龍魂/xpay
  • shell_config: ~/.zshrc

[更多評估詳情...]

執行狀態: ✅ 成功
結束時間: 2026-06-06 22:30:28
最新報告: /Users/.../​.龍魂/assessments/local_assessment_20260606_223015.json
評分: 9.7/10 | 狀態: ✅ 生產級可用
════════════════════════════════════════════════════════════
```

---

## 🎯 關鍵指標

### 系統健康度
- **評分 ≥ 8.0**: 🟢 生產級可用
- **評分 6.0-8.0**: 🟡 需要改進
- **評分 < 6.0**: 🔴 不推薦

### 各維度權重
- 可運行性最高 (25%) → 系統能否正常工作
- 代碼文件次之 (20%) → 核心功能是否完整
- 數據完整性 (20%) → 交易記錄是否安全
- 安全性 (15%) → 本地存儲是否安全
- 環境配置 (10%) → 運行環境是否正確
- 文檔完整性最低 (10%) → 文檔是否齐全

---

## 📚 相關文檔

| 文檔 | 位置 | 用途 |
|------|------|------|
| 評估總結 | `~/.龍魂/assessments/ASSESSMENT_SUMMARY.md` | 快速了解系統狀態 |
| Cron 設定 | `~/.龍魂/assessments/CRON_SETUP.md` | Cron 任務詳情 |
| XPay 部署 | `~/.claude/projects/.../XPAY_DEPLOYMENT.md` | XPay 系統詳情 |
| 啟動菜單修復 | `~/.claude/projects/.../XPAY_LAUNCHER_FIX.md` | 啟動器問題解決 |

---

## 🔐 數據保留策略

```
【短期 (7 天)】
  • 所有評估報告和日誌保存
  • 用於週趨勢分析

【中期 (30 天)】
  • 每天保留一份報告
  • 用於月度趨勢分析

【長期】
  • 保留關鍵里程碑報告
  • 用於版本對比
```

---

## ✨ 最佳實踐

1. **定期查看評分** - 每週查看一次評分變化
2. **閱讀可改進項目** - 及時修復系統問題
3. **保持監控活躍** - 遇到評分下降立即查詢原因
4. **定期清理舊日誌** - 保持存儲整潔
5. **測試新功能** - 變更系統後手動運行評估驗證

---

## 🟢 設定驗收

| 項目 | 狀態 | 備註 |
|------|------|------|
| 評估引擎 | ✅ | 16 KB · 6 維度 |
| Cron 任務 | ✅ | 每天 22:30 執行 |
| 執行腳本 | ✅ | 1.9 KB · 可執行 |
| 狀態工具 | ✅ | 2.1 KB · 快速查詢 |
| 報告目錄 | ✅ | 已創建 · 可寫入 |
| 初始評分 | ✅ | 9.7/10 · 生產級 |

---

## 📞 支援與反饋

若有任何問題或改進建議:
1. 查看故障排查章節
2. 運行 `bash ~/check_longhun_assessment.sh` 檢查狀態
3. 查看日誌檔案 `~/.龍魂/assessments/logs/`
4. 手動運行 `python3 ~/local_assessment_engine.py`

---

**老大，龍魂系統自動化日評估已完全部署。每天 22:30 自動執行，無需人工干預。**

🐉 **準備就緒。**

---

**簽証**:#龍芯⚡️2026-06-05-AUTOMATED-ASSESSMENT-v1.0
**設定者**: UID9622 (Claude Code)
**確認**: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✅
