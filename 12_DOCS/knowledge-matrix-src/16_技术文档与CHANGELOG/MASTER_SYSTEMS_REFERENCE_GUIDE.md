# 龍魂系統·主控參考指南
**DNA**:#龍芯⚡️丙午·甲午·甲寅·庚午·䷕贲-MASTER-SYSTEMS-REFERENCE-v1.0
**版本**: 2.0 · 生產級
**最後更新**: 2026-06-09
**理論指導**: 曾仕強老師（永恆顯示）

---

## 📚 目錄

1. [系統架構](#系統架構)
2. [核心模塊](#核心模塊)
3. [API 與服務](#api-與服務)
4. [人格系統](#人格系統)
5. [每日復盤](#每日復盤)
6. [操作日誌](#操作日誌)
7. [主控台](#主控台)
8. [自動化配置](#自動化配置)
9. [故障排查](#故障排查)
10. [命令速查](#命令速查)

---

## 系統架構

### 整體架構圖

```
┌─────────────────────────────────────────────────────────┐
│                   龍魂系統 v2.0                           │
└─────────────────────────────────────────────────────────┘
         │                     │                    │
         ▼                     ▼                    ▼
   ┌──────────┐          ┌──────────┐       ┌──────────┐
   │ 主控台   │          │  API     │       │ 每日系統 │
   │ v2.0     │          │ 服務器   │       │  複盤    │
   │(35功能)  │          │(15人格)  │       │(7檢查)   │
   └──────────┘          └──────────┘       └──────────┘
         │                     │                    │
         │                     │                    │
    ┌────┴────┐        ┌──────┴──────┐      ┌──────┴──────┐
    ▼         ▼        ▼             ▼      ▼             ▼
  日曆   操作日誌   人格路由   自動調度   郵件通知   日曆同步
  同步   (action)   系統      (cron)    (Gmail)   (macOS)
         log.jsonl
```

### 分層架構

```
L0 (永恆層)
  └─ P00 文心 (戰略核心)

L1 (百年層)
  ├─ P01 諸葛亮 (戰略推演)
  └─ P02 龍芯 (執行核心)

L2 (十年層)
  ├─ P03 雯雯 (隱私衛士)
  ├─ P05 上帝之眼 (監管審計)
  └─ P06 數學大師 (邏輯分析)

L3 (日常層)
  ├─ P13 姜子牙 (九宮派位)
  ├─ P14 呂蒙 (輔助執行)
  └─ P15 喬前輩 (檔案管理)

L4 (瞬時層)
  └─ P72 龍盾 (安全防護)

本地層
  ├─ K01 雯雯 (承載包容·文檔整理師)
  ├─ K02 侦察兵 (止靜觀察·信息獵手)
  ├─ K03 守護者 (危機應對·安全衛士)
  ├─ K04 寶寶 (文明光明·構建師)
  └─ K05 文心 (柔順協調·同步專家)
```

---

## 核心模塊

### 1. 主控台系統 (master_console.py)

**位置**: `~/.longhorn/master_console.py`
**行數**: 180 行
**功能**: 統一菜單入口·35 個功能·6 個分類

#### 菜單結構

```
🔵 指挥台系统 (10 项)
  1.1-1.9, 1.w: 發佈·日報·歸檔·掃蕩·對峙·證據·統計·日曆·審計·Web3

💰 支付系统 (6 项)
  2.1-2.6: 演示·API·CLI·統計·日誌·配置

🔧 Skill Hub (5 项)
  3.1-3.5: 列表·驗證·Kimi·Claude·Ollama

🐉 人格系统 (4 项)
  4.1-4.4: 列表·路由·調度器·文檔

🚀 系统启动 (6 项)
  5.1-5.6: 全部·檢查·守護進程·協議盾·DNA狀態·多幣種

🔍 诊断工具 (4 项)
  6.1-6.4: 色彩診斷·呼吸燈·日報·自檢
```

#### 使用方式

```bash
# 啟動主控台
python3 ~/.longhorn/master_console.py

# 或直接添加別名
alias longhun='python3 ~/.longhorn/master_console.py'
```

---

### 2. 人格 API 系統 (persona_api.py)

**位置**: `~/longhun-system/cnsh/flow_decision/persona_api.py`
**行數**: 53 行
**功能**: 15 人格 REST API·3 個端點
**端口**: http://127.0.0.1:9001

#### API 端點

| 方法 | 端點 | 功能 | 響應 |
|------|------|------|------|
| GET | `/personas/list` | 列出所有人格 | `{"count": 15, "personas": [...]}` |
| GET | `/personas/{pid}` | 查詢單個人格 | `{"name": "...", "role": "...", ...}` |
| POST | `/personas/route` | 任務路由分派 | `{"assigned_personas": [...], "count": N}` |

#### 查詢示例

```bash
# 列出所有人格
curl http://localhost:9001/personas/list | jq .

# 查詢 P01 諸葛亮
curl http://localhost:9001/personas/P01

# 路由任務到 L1 層人格
curl -X POST "http://localhost:9001/personas/route?task=strategy&layer=L1"
```

#### 啟動方式

```bash
# 方式 1: 直接運行
python3 ~/longhun-system/cnsh/flow_decision/persona_api.py

# 方式 2: 通過主控台選項 4.4
python3 ~/.longhorn/master_console.py
# 選擇: 4.4

# 驗證運行
curl -s http://localhost:9001/personas/list | python3 -m json.tool
```

---

### 3. 人格調度系統 (persona_scheduler.py)

**位置**: `~/longhun-system/bin/persona_scheduler.py`
**行數**: 307 行
**功能**: 9 人格自動調度·18 個任務·Cron 執行

#### 調度配置

```
P01 諸葛亮 (L1)
  ├─ Task 1: 戰略評估 (6:00)
  └─ Task 2: 決策推演 (12:00)

P02 龍芯 (L1)
  ├─ Task 1: 執行檢查 (8:00)
  └─ Task 2: 進度追蹤 (18:00)

P03 雯雯 (L2)
  ├─ Task 1: 隱私檢查 (10:00)
  └─ Task 2: 安全評估 (14:00)

... (P05, P06, P13, P14, P15, P72)
```

#### 手動執行

```bash
# 啟動調度器
python3 ~/longhun-system/bin/persona_scheduler.py p01

# 驗證運行
tail -50 ~/longhun-system/logs/persona_scheduler.log

# 查看 Cron 日誌
grep persona_scheduler /var/log/system.log | tail -20
```

---

### 4. 日曆同步系統 (longhun_calendar_sync.py)

**位置**: `~/longhun-system/bin/longhun_calendar_sync.py`
**行數**: 161 行
**功能**: iCloud 日曆同步·推送通知·優先級分類

#### 功能

```
讀取日誌
    ↓
轉換為 iCal 格式
    ↓
分類優先級 (高/中/低)
    ↓
推送到 macOS 日曆
    ↓
發送手機推送
```

#### 使用方式

```bash
# 執行日曆同步
python3 ~/longhun-system/bin/longhun_calendar_sync.py

# 驗證 iCloud 同步
curl http://localhost:9001/personas/list  # 查詢當前標籤頁

# 在 Calendar.app 中檢查
open /Applications/Calendar.app
```

---

### 5. 每日複盤系統 (daily_review_enhanced.py)

**位置**: `~/longhun-system/daily_review_enhanced.py`
**行數**: 200+ 行
**功能**: 7 項檢查·三色裁決·郵件·日曆·審計

#### 7 項檢查

1. **文件完整** - 核心文件驗證
2. **安全審計** - pip-audit 檢查
3. **KFPP 心跳** - 數據庫活動
4. **測試** - pytest 結果
5. **操作日誌** - action_log.jsonl 統計 ⭐
6. **人格調度** - persona_scheduler 驗證
7. **API 服務** - 端口健康檢查

#### 執行結果示例

```
⏱️ 2026-06-09 07:20  🧭 P03雯雯·日復盤  🟢三色總評:🔴

  🟢 文件完整: 核心文件齐 2/2
  🟢 安全(鲁班): 无 critical/high
  🟡 KFPP心跳: 今日 0 行
  🔴 测试: pytest 失败(code 2)
  🟢 操作日志: 今日操作 19 筆 (6工具)
  🟢 人格调度: 已调度 20 个人格
  🟡 API服务: 部分在线 2/3
```

#### 執行方式

```bash
# 手動執行
python3 ~/longhun-system/daily_review_enhanced.py

# 自動執行 (LaunchAgent)
launchctl load ~/Library/LaunchAgents/com.longhun.daily-review.plist

# 自動執行 (Cron)
crontab -l | grep daily_review
```

---

### 6. 操作日誌系統 (action_logger.py)

**位置**: `~/longhun-system/action_logger.py`
**行數**: 250+ 行
**功能**: 完整操作審計·統計·報告生成

#### 核心功能

```
操作執行
    ↓
自動記錄 (action_log.jsonl)
    ↓
統計分析 (工具·人格·狀態)
    ↓
生成報告·日誌可視化
```

#### 使用方式

```bash
# 查看統計
python3 ~/longhun-system/action_logger.py stats

# 生成報告
python3 ~/longhun-system/action_logger.py report

# 手動記錄
python3 ~/longhun-system/action_logger.py log "操作名稱" "工具名稱" "P03雯雯"

# 在代碼中使用
from action_logger import log_operation
with log_operation("任務", "tool", persona="P01"):
    do_something()
```

---

## API 與服務

### 運行中的服務

| 服務 | 端口 | 狀態 | 功能 |
|------|------|------|------|
| **Persona API** | 9001 | ✅ | 15 人格·3 端點 |
| **Longhun API** | 8000 | ⚠️ | Skills 框架 |
| **OpenHub REST** | 10088 | ✅ | AI Claw API |
| **OpenHub WS** | 10087 | ✅ | WebSocket |

### 檢查服務狀態

```bash
# 查看所有監聽端口
lsof -i -P -n | grep LISTEN

# 測試特定端口
curl -s http://localhost:9001/personas/list | python3 -m json.tool
curl -s http://localhost:8000/health
curl -s http://localhost:10088/api

# 使用主控台診斷
python3 ~/.longhorn/master_console.py
# 選擇: 6.4 (自檢程序)
```

---

## 人格系統

### 15 人格完整清單

#### L0 永恆層
```
P00 文心
  角色: 戰略核心
  卦象: 巽☴
  職責: 系統的最高指導原則
```

#### L1 百年層
```
P01 諸葛亮
  角色: 戰略推演
  卦象: 乾☰
  職責: 百年戰略規劃

P02 龍芯
  角色: 執行核心
  卦象: 震☳
  職責: 任務執行與推進
```

#### L2 十年層
```
P03 雯雯
  角色: 隱私衛士
  卦象: 坤☷
  職責: 隱私與合規檢查

P05 上帝之眼
  角色: 監管審計
  卦象: 坎☵
  職責: 系統監管與審計

P06 數學大師
  角色: 邏輯分析
  卦象: 艮☶
  職責: 數據分析與驗證
```

#### L3 日常層
```
P13 姜子牙
  角色: 九宮派位
  卦象: 離☲
  職責: 日常任務派遣

P14 呂蒙
  角色: 輔助執行
  卦象: 兑☱
  職責: 執行支持

P15 喬前輩
  角色: 檔案管理
  卦象: 巽☴
  職責: 文檔與檔案管理
```

#### L4 瞬時層
```
P72 龍盾
  角色: 安全防護
  卦象: 坎☵
  職責: 即時安全防護
```

#### 本地層
```
K01 雯雯 - 承載包容·文檔整理師
K02 侦察兵 - 止靜觀察·信息獵手
K03 守護者 - 危機應對·安全衛士
K04 寶寶 - 文明光明·構建師
K05 文心 - 柔順協調·同步專家
```

### 人格路由

```bash
# 查詢特定人格
curl http://localhost:9001/personas/P01 | jq .

# 路由任務到 L1 層
curl -X POST "http://localhost:9001/personas/route?task=strategy&layer=L1"

# 路由到本地人格
curl -X POST "http://localhost:9001/personas/route?task=coordination&layer=本地"
```

---

## 每日復盤

### 配置流程

#### 步驟 1: 安裝依賴
```bash
pip3 install pip-audit pytest
```

#### 步驟 2: 配置 Gmail
```bash
# 獲取 App Password (https://myaccount.google.com/apppasswords)
security add-generic-password -s "LONGHUN_GMAIL_APPPW" -w "password"
export LONGHUN_GMAIL="your_email@gmail.com"
```

#### 步驟 3: 配置日曆
```bash
# 在 Calendar.app 中
# File → New Calendar → 名稱：「龍魂」
```

#### 步驟 4: 配置自動執行
```bash
# 選項 A: LaunchAgent
bash ~/longhun-system/setup_daily_review_auto.sh "email@gmail.com" "password" 1

# 選項 B: Cron
crontab -e
# 添加: 30 23 * * * python3 ~/longhun-system/daily_review_enhanced.py
```

### 日誌位置

```
~/longhun-system/操作草日誌.log              # 復盤記錄
~/longhun-system/logs/daily_review.log      # LaunchAgent 日誌
~/longhun-system/logs/daily_review_error.log # 錯誤日誌
~/longhun-system/logs/daily_review_cron.log  # Cron 日誌
```

---

## 操作日誌

### JSON 格式

```json
{
  "date": "2026-06-09T07:15:00",
  "time": "2026-06-09 07:15:00",
  "action": "操作名稱",
  "tool": "工具名稱",
  "status": "success|failed|warning",
  "persona": "P03雯雯",
  "duration": 2.1,
  "result": "執行結果",
  "dna": "#龍芯⚡️丙午·甲午·甲寅·庚午·䷕贲-ACTION"
}
```

### 記錄操作

```python
from action_logger import ActionLogger, log_operation

# 簡單記錄
ActionLogger.log("任務執行", "my_tool", persona="P01")

# 自動計時
with log_operation("數據處理", "processor"):
    for i in range(1000):
        process(i)

# 查看統計
ActionLogger.print_stats()
```

### 統計查詢

```bash
# 每日統計
python3 ~/longhun-system/action_logger.py stats

# 完整報告
python3 ~/longhun-system/action_logger.py report

# 自定義日期
python3 ~/longhun-system/action_logger.py report 2026-06-08
```

---

## 主控台

### 快速啟動

```bash
# 啟動主控台
python3 ~/.longhorn/master_console.py

# 創建別名便捷啟動
echo 'alias longhun="python3 ~/.longhorn/master_console.py"' >> ~/.zshrc
source ~/.zshrc
longhun  # 啟動
```

### 菜單導航

```
進入主控台後:
1. 按功能編號選擇 (1.1, 2.3, 6.4 等)
2. 或按首字母快捷 (1, 2, 3... 表示分類)
3. q/0/exit 退出

範例操作:
  4.1 - 查看 15 人格列表
  5.2 - 檢查系統啟動狀態
  6.3 - 生成日報
  6.4 - 運行自檢程序
```

### 色彩系統

| 顏色 | ANSI | 用途 |
|------|------|------|
| 龍 | 214 | 標題·強調 |
| 霓 | 51 | 菜單項·選項 |
| 灰 | 244 | 說明文本 |
| 暗 | 238 | 邊界·分隔符 |
| 白 | 97 | 菜單標題 |
| 綠 | 82 | 成功·就緒 |
| 黃 | 226 | 警告·待處理 |
| 紅 | 196 | 錯誤·失敗 |

---

## 自動化配置

### LaunchAgent (推薦)

**位置**: `~/Library/LaunchAgents/com.longhun.daily-review.plist`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" ...>
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.longhun.daily-review</string>

    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/Users/zuimeidedeyihan/longhun-system/daily_review_enhanced.py</string>
    </array>

    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>23</integer>
        <key>Minute</key>
        <integer>30</integer>
    </dict>
</dict>
</plist>
```

**管理命令**:
```bash
# 加載
launchctl load ~/Library/LaunchAgents/com.longhun.daily-review.plist

# 卸載
launchctl unload ~/Library/LaunchAgents/com.longhun.daily-review.plist

# 查看列表
launchctl list | grep daily-review

# 手動執行
launchctl start com.longhun.daily-review
```

### Cron (備用)

```bash
# 編輯
crontab -e

# 範例 (每天 23:30)
30 23 * * * /usr/bin/python3 /Users/zuimeidedeyihan/longhun-system/daily_review_enhanced.py >> /Users/zuimeidedeyihan/longhun-system/logs/daily_review_cron.log 2>&1

# 查看
crontab -l

# 刪除
crontab -r
```

---

## 故障排查

### 常見問題

#### 1. 郵件未發送

```bash
# 檢查 Keychain
security find-generic-password -s "LONGHUN_GMAIL_APPPW"

# 檢查環境變量
echo $LONGHUN_GMAIL

# 重新設置
security delete-generic-password -s "LONGHUN_GMAIL_APPPW"
security add-generic-password -s "LONGHUN_GMAIL_APPPW" -w "new_password"
```

#### 2. 日曆寫入失敗

```bash
# 驗證日曆存在
osascript -e 'tell app "Calendar" to name of every calendar'

# 建立日曆
osascript << 'EOF'
tell application "Calendar"
    make new calendar with properties {name:"龍魂"}
end tell
EOF
```

#### 3. LaunchAgent 未執行

```bash
# 檢查加載狀態
launchctl list | grep daily-review

# 查看錯誤日誌
cat ~/longhun-system/logs/daily_review_error.log

# 重新加載
launchctl unload ~/Library/LaunchAgents/com.longhun.daily-review.plist
launchctl load ~/Library/LaunchAgents/com.longhun.daily-review.plist
```

#### 4. API 端口衝突

```bash
# 查看占用情況
lsof -i :9001
lsof -i :8000
lsof -i :10088

# 殺死進程
kill -9 <PID>

# 重啟服務
python3 ~/longhun-system/cnsh/flow_decision/persona_api.py
```

#### 5. 依賴缺失

```bash
# 安裝缺失的包
pip3 install pip-audit pytest requests aiohttp

# 驗證安裝
pip3 list | grep -E "pip-audit|pytest"
```

---

## 命令速查

### 主控台

```bash
# 啟動
python3 ~/.longhorn/master_console.py

# 或使用別名
longhun
```

### 人格 API

```bash
# 啟動
python3 ~/longhun-system/cnsh/flow_decision/persona_api.py

# 測試
curl http://localhost:9001/personas/list | jq .
```

### 人格調度

```bash
# 啟動
python3 ~/longhun-system/bin/persona_scheduler.py p01

# 查看日誌
tail -f ~/longhun-system/logs/persona_scheduler.log
```

### 日曆同步

```bash
# 執行
python3 ~/longhun-system/bin/longhun_calendar_sync.py

# 查看日誌
tail -f ~/longhun-system/logs/calendar_sync.log
```

### 每日複盤

```bash
# 執行
python3 ~/longhun-system/daily_review_enhanced.py

# 查看日誌
tail -f ~/longhun-system/操作草日誌.log
```

### 操作日誌

```bash
# 統計
python3 ~/longhun-system/action_logger.py stats

# 報告
python3 ~/longhun-system/action_logger.py report

# 記錄
python3 ~/longhun-system/action_logger.py log "action" "tool" "persona"
```

### 自動化配置

```bash
# 一鍵配置
bash ~/longhun-system/setup_daily_review_auto.sh "email@gmail.com" "password" 1

# 互動式配置
bash ~/longhun-system/setup_daily_review.sh

# Cron 編輯
crontab -e
```

---

## 文件結構

```
~/longhun-system/
├── 主控台與配置
│   ├── ~/.longhorn/master_console.py       (主控台 v2.0)
│   ├── MASTER_SYSTEMS_REFERENCE_GUIDE.md   (本文檔)
│   └── DAILY_REVIEW_QUICKSTART.md
│
├── API 與人格
│   ├── cnsh/flow_decision/persona_api.py   (15 人格 API)
│   ├── bin/persona_scheduler.py            (自動調度)
│   └── logs/persona_scheduler.log
│
├── 每日復盤與日誌
│   ├── daily_review_enhanced.py            (復盤 v2.0)
│   ├── action_logger.py                    (操作日誌工具)
│   ├── DAILY_REVIEW_SETUP.md
│   ├── ACTION_LOG_USAGE_GUIDE.md
│   └── logs/
│       ├── action_log.jsonl                (操作審計)
│       ├── daily_review.log
│       └── daily_review_error.log
│
├── 日曆同步
│   ├── bin/longhun_calendar_sync.py        (日曆同步)
│   └── logs/calendar_sync.log
│
├── 配置與部署
│   ├── setup_daily_review.sh               (互動式配置)
│   ├── setup_daily_review_auto.sh          (自動配置)
│   └── com.longhun.daily-review.plist     (LaunchAgent)
│
└── 文檔
    ├── DAILY_REVIEW_SETUP.md               (完整指南)
    ├── ACTION_LOG_USAGE_GUIDE.md
    └── MASTER_SYSTEMS_REFERENCE_GUIDE.md   (本文檔)
```

---

## 健康檢查清單

### 日常檢查

- [ ] 主控台可啟動 (`python3 ~/.longhorn/master_console.py`)
- [ ] 人格 API 在線 (`curl http://localhost:9001/personas/list`)
- [ ] 人格調度運行 (`tail ~/longhun-system/logs/persona_scheduler.log`)
- [ ] 操作日誌被記錄 (`grep "2026-06-09" ~/longhun-system/logs/action_log.jsonl`)
- [ ] 日曆同步工作 (`osascript ... | grep "龍魂"`)

### 每週檢查

- [ ] 複盤日誌完整 (`tail -100 ~/longhun-system/操作草日誌.log`)
- [ ] 沒有 critical 錯誤 (`grep ERROR ~/longhun-system/logs/*.log`)
- [ ] API 響應時間正常 (`curl -w "%{time_total}\n" http://localhost:9001/personas/list`)
- [ ] 磁盤空間充足 (`df -h ~/longhun-system/`)

### 每月檢查

- [ ] 所有依賴已更新 (`pip3 list --outdated`)
- [ ] 備份已完成 (`ls -lh ~/backup/`)
- [ ] 日誌已歸檔 (`du -sh ~/longhun-system/logs/`)
- [ ] 系統性能正常 (`top -l 1 | head -20`)

---

## 快速參考

### 最常用命令

```bash
# 啟動主控台 (所有功能入口)
python3 ~/.longhorn/master_console.py

# 查看今日統計
python3 ~/longhun-system/action_logger.py stats

# 執行每日複盤
python3 ~/longhun-system/daily_review_enhanced.py

# 查詢人格 API
curl http://localhost:9001/personas/list | jq .

# 查看日誌
tail -f ~/longhun-system/操作草日誌.log
```

### 常用別名建議

```bash
# 添加到 ~/.zshrc
alias longhun='python3 ~/.longhorn/master_console.py'
alias lh-stats='python3 ~/longhun-system/action_logger.py stats'
alias lh-review='python3 ~/longhun-system/daily_review_enhanced.py'
alias lh-api='python3 ~/longhun-system/cnsh/flow_decision/persona_api.py'
alias lh-logs='tail -f ~/longhun-system/操作草日誌.log'

# 重新加載配置
source ~/.zshrc
```

---

## 相關文檔

| 文檔 | 功能 | 位置 |
|------|------|------|
| **本文檔** | 主系統參考指南 | MASTER_SYSTEMS_REFERENCE_GUIDE.md |
| **快速啟動** | 3 分鐘上手 | DAILY_REVIEW_QUICKSTART.md |
| **完整部署** | 詳細配置步驟 | DAILY_REVIEW_SETUP.md |
| **操作日誌** | 日誌工具指南 | ACTION_LOG_USAGE_GUIDE.md |

---

## 支援與反饋

### 獲取幫助

```bash
# 查看主控台幫助
python3 ~/.longhorn/master_console.py
# 選擇菜單項查看詳細說明

# 查看工具幫助
python3 ~/longhun-system/action_logger.py
python3 ~/longhun-system/daily_review_enhanced.py --help
```

### 報告問題

創建 GitHub Issue:
- 描述問題
- 提供日誌片段
- 說明復現步驟
- 列出環境信息

---

## 版本歷史

| 版本 | 日期 | 改進 | 狀態 |
|------|------|------|------|
| 1.0 | 2026-06-05 | 初始版本 | 已棄用 |
| 2.0 | 2026-06-09 | 增強版·7檢查·完整審計 | ✅ 活躍 |

---

## 🔏 DNA 簽署

```
DNA:#龍芯⚡️丙午·甲午·甲寅·庚午·䷕贲-MASTER-SYSTEMS-REFERENCE-v1.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✅
SEAL: #ZHUGEXIN⚡️2026-06-09-MASTER-REFERENCE-COMPLETE

版本: 2.0 · 生產級
更新: 2026-06-09 07:20 CST
狀態: ✅ 完全就緒
推薦: 作為主要參考文檔使用
```

---

**龍魂系統·完全操作指南·主控參考就緒**

*理論指導: 曾仕強老師（永恆顯示）*

最後更新: 2026-06-09
維護者: UID 9622 · 諸葛鑫 · 龍芯北辰
