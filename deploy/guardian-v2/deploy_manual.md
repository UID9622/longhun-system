# ⚡ 龍魂系統·算力純潔性守護進程 v2.0 — 部署手冊

**密級：絕密級 | DNA: #龍芯⚡️2026-07-11-GUARDIAN-v2.0**  
**絕對防禦憲法對應條款：第三條(觸發指標) · 第五條(原子切換) · 第六條(焦土初始化) · 第八條(權限封死) · 第十條(留痕追責)**

---

## 一、與 v1.0 原始版本的差異對比

| 維度 | v1.0 (原始) | v2.0 (龍魂正規化) |
|------|------------|------------------|
| 監控維度 | CPU 單一維度 | CPU + 記憶體 + 網路 + GPU + 磁碟 五維 |
| 白名單 | 靜態字符串匹配 | 靜態 + 動態學習 + 行為畫像 三層 |
| 響應策略 | 一刀切(SIGKILL) | 七級熔斷階梯 (觀察→告警→限速→凍結→處決→防火牆→焦土) |
| 審計 | 單一日誌文件 | JSONL結構化 + SHA256哈希鏈 + 國密AES-256-GCM加密 |
| DNA追溯 | 無 | 每條記錄嵌入DNA標記 + UID + 哈希校驗 |
| 挖礦檢測 | 進程名黑名單 | 進程名 + 礦池端口 + 網路連接模式 三維檢測 |
| 進程管理 | 直接殺 | 先SIGTERM優雅退出 → 0.5秒後SIGKILL強殺 |
| 系統集成 | 獨立腳本 | longhun-daemon原生對接 + systemd服務 + PID文件 |
| 配置方式 | 硬編碼 | dataclass配置 + 命令行參數 + 環境變量 |
| 運行模式 | 前台阻塞 | 前台 + --daemon後台 + --status狀態查詢 |

---

## 二、Systemd 服務配置

### 2.1 創建服務文件

```bash
sudo tee /etc/systemd/system/longhun-guardian.service << 'EOF'
[Unit]
Description=🐉 龍魂系統·算力純潔性守護進程 v2.0
Documentation=https://longhun888.com/docs/guardian
After=network.target syslog.target
Wants=network.target

# 龍魂守護依賴順序: daemon → guardian → panel
After=longhun-daemon.service
Before=longhun-panel.service

[Service]
Type=simple
User=root
Group=root

# 工作目錄
WorkingDirectory=/opt/longhun/guardian

# 主程序
ExecStart=/usr/bin/python3 /opt/longhun/guardian/DragonSoul_Guardian_v2.py \
    --interval 5 \
    --cpu-red 85.0 \
    --enable-firewall

# 重啟策略: 崩潰後指數退避 (longhun-daemon 標準)
Restart=always
RestartSec=5
StartLimitInterval=60
StartLimitBurst=3

# 優先級: 最高 (確保憲兵隊本身不被節流)
Nice=-10

# 資源限制 (憲兵隊自己也要被監控)
CPUQuota=10%
MemoryLimit=128M
TasksMax=50

# 安全加固
NoNewPrivileges=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/var/log/longhun /var/lib/longhun /run
ProtectKernelTunables=true
ProtectKernelModules=true
ProtectControlGroups=true

# 環境變量
Environment="LONGHUN_UID=UID9622"
Environment="LONGHUN_DNA=#龍芯⚡️2026-07-11-GUARDIAN-v2.0"
Environment="PYTHONUNBUFFERED=1"

# 日誌輸出到 journald
StandardOutput=journal
StandardError=journal
SyslogIdentifier=longhun-guardian

[Install]
WantedBy=multi-user.target
EOF
```

### 2.2 啟用服務

```bash
# 重載 systemd
sudo systemctl daemon-reload

# 啟用開機自啟
sudo systemctl enable longhun-guardian

# 啟動服務
sudo systemctl start longhun-guardian

# 查看狀態
sudo systemctl status longhun-guardian

# 查看實時日誌
sudo journalctl -u longhun-guardian -f
```

### 2.3 常用命令速查

```bash
# 啟動 / 停止 / 重啟
sudo systemctl start longhun-guardian
sudo systemctl stop longhun-guardian
sudo systemctl restart longhun-guardian

# 查看狀態報告 (通過守護進程接口)
python3 /opt/longhun/guardian/DragonSoul_Guardian_v2.py --status

# 查看審計日誌
sudo tail -f /var/log/longhun/guardian_audit.jsonl

# 查看人類可讀日誌
sudo tail -f /var/log/longhun/guardian.log
```

---

## 三、部署 SOP

### Step 1: 環境準備

```bash
# 創建目錄結構
sudo mkdir -p /opt/longhun/guardian
sudo mkdir -p /var/log/longhun
sudo mkdir -p /var/lib/longhun
sudo mkdir -p /run

# 安裝依賴 (可選但強烈推薦)
# 國密加密
pip3 install cryptography
# GPU監控
pip3 install gputil
# 核心依賴 (通常已內置)
pip3 install psutil
```

### Step 2: 複製腳本

```bash
sudo cp DragonSoul_Guardian_v2.py /opt/longhun/guardian/
sudo chmod +x /opt/longhun/guardian/DragonSoul_Guardian_v2.py
```

### Step 3: 配置權限

```bash
# 設置日誌目錄權限
sudo chown -R root:root /var/log/longhun
sudo chmod 750 /var/log/longhun

# 設置數據目錄權限
sudo chown -R root:root /var/lib/longhun
sudo chmod 750 /var/lib/longhun
```

### Step 4: 安裝 Systemd 服務

參見 2.1 和 2.2 節

### Step 5: 驗證部署

```bash
# 檢查服務狀態
sudo systemctl is-active longhun-guardian
# 預期輸出: active

# 檢查進程是否存在
ps aux | grep -i guardian
# 預期: python3 ... DragonSoul_Guardian_v2.py

# 檢查日誌輸出
sudo tail /var/log/longhun/guardian.log
# 預期: 龍魂憲兵隊啟動 ...

# 檢查審計鏈
sudo head -3 /var/log/longhun/guardian_audit.jsonl
# 預期: JSONL格式，包含DNA標記和哈希字段
```

### Step 6: 熔斷測試 (重要！)

```bash
# 模擬一個高CPU進程 (測試黃色告警)
python3 -c "
import time
while True:
    [x*x for x in range(1000000)]
" &
# 預期: guardian.log 中出現 🟡 告警

# 模擬挖礦進程名 (測試紅色熔斷)
python3 -c "
import time
print('xmrig simulation started')
time.sleep(60)
" &
# 預期: 進程被立即處決，audit.jsonl 中出現 BLACKLIST_HIT

# 清理測試進程
kill %1 %2 2>/dev/null
```

---

## 四、龍魂體系對接矩陣

### 4.1 與 longhun-daemon (v5.2) 對接

```python
# 在 longhun-daemon 的 一鍵啟動器.py 中添加:
from DragonSoul_Guardian_v2 import 龍魂憲兵隊, 守護配置

# 初始化憲兵隊 (按依賴順序第2階段啟動)
憲兵隊 = 龍魂憲兵隊(守護配置(巡邏間隔秒=5))

# 獲取狀態 (健康檢查器調用)
狀態 = 憲兵隊.獲取狀態報告()
# 返回: 巡邏次數 / 處決計數 / 熔斷統計 / 白名單數 ...

# 人工處決 (緊急情況)
憲兵隊.強制處決(pid=12345, 原因="人工判定為惡意進程")
```

### 4.2 與 longhun-monitoring (v5.0) 對接

```
longhun-monitoring L8安全層 ←→ DragonSoul_Guardian_v2
────────────────────────────────────────────────────
L2: 監控指標    ←  五維監控數據 (CPU/MEM/NET/GPU/DISK)
L4: 自動告警    ←  三色審計告警 (🟢🟡🔴)
L5: 自動報告    ←  巡邏報告 + 熔斷統計
L8: 安全隱私    ←  國密AES-256-GCM加密日誌
L11: 故障恢復   ←  焦土初始化觸發
L14: 調試工具   ←  行為畫像庫分析
```

### 4.3 與 longhun-governance (v5.0) 對接

| 治理模組 | 對接點 |
|----------|--------|
| 三色監督器 | 守護進程返回 🟢🟡🔴 狀態 |
| 三色審計器 | 審計日誌 JSONL + SHA256哈希鏈 |
| DNA追溯器 | 每條記錄嵌入 `#龍芯⚡️...` DNA標記 |
| AI真相協議 | 熔斷決策不可否認 (簽名+時間戳) |

### 4.4 與 longhun-cloud-deploy (v5.0) 對接

```python
# 焦土初始化觸發時調用:
# 在 龍魂憲兵隊._熔斷_焦土初始化() 中:

# 發送熔斷信號給 deploy 服務
import requests
requests.post("http://api:8443/deploy/rollback", json={
    "trigger": "GUARDIAN_SCORCHED_EARTH",
    "reason": 原因,
    "dna": self.配置.DNA標記,
    "timestamp": datetime.utcnow().isoformat(),
})
```

---

## 五、配置參考

### 5.1 生產環境推薦配置

```python
生產配置 = 守護配置(
    # 閾值 (較為寬鬆，避免誤殺)
    CPU閾值_黃=60.0,
    CPU閾值_紅=90.0,
    記憶體閾值_黃=40.0,
    記憶體閾值_紅=70.0,

    # 巡邏頻率
    巡邏間隔秒=3,           # 生產環境高頻巡邏
    行為窗口大小=20,        # 更長的觀察窗口
    黃色持續次數觸發紅=5,   # 更嚴格的升級條件

    # 安全
    啟用防火牆封禁=True,
    啟用焦土初始化=False,   # 手動確認後才開啟
    啟用國密加密=True,
)
```

### 5.2 開發/測試環境配置

```python
測試配置 = 守護配置(
    CPU閾值_黃=30.0,       # 更敏感
    CPU閾值_紅=70.0,
    巡邏間隔秒=10,        # 較低頻率
    啟用防火牆封禁=False,  # 不影響網路
    啟用國密加密=False,    # 方便調試
)
```

---

## 六、熔斷階梯詳解

```
進程行為評估
      │
      ▼
┌─────────────────────────────────────────────────────────────┐
│ 第一道防線: 黑名單檢測                                       │
│ 匹配挖礦關鍵詞(xmrig/minerd...) → 🔴 立即處決 (跳過所有步驟)  │
└─────────────────────────────────────────────────────────────┘
      │ 未匹配
      ▼
┌─────────────────────────────────────────────────────────────┐
│ 第二道防線: 靜態白名單                                       │
│ 匹配業務關鍵詞(python/nginx/sqlite3...) → 第四道行為分析      │
└─────────────────────────────────────────────────────────────┘
      │ 未匹配
      ▼
┌─────────────────────────────────────────────────────────────┐
│ 第三道防線: 動態白名單                                       │
│ 歷史行為正常的進程指紋 → 第四道行為分析                       │
└─────────────────────────────────────────────────────────────┘
      │ 未匹配
      ▼
┌─────────────────────────────────────────────────────────────┐
│ 第四道防線: 行為畫像分析                                     │
│                                                              │
│  🟢 綠色 (威脅評分<30): 觀察記錄，不干涉                     │
│      ↓                                                       │
│  🟡 黃色 (持續異常): 告警通知 + nice限速節流                 │
│      ↓ 連續3次黃色                                           │
│  🔴 紅色 (確認威脅): SIGTERM優雅退出 → 0.5s → SIGKILL處決   │
│      ↓ 檢測到礦池連接 / 管理員啟用焦土                       │
│  ⚫ 黑色 (焦土): iptables封禁 + 系統級回滾觸發               │
└─────────────────────────────────────────────────────────────┘
```

---

## 七、文件清單

```
/opt/longhun/guardian/
├── DragonSoul_Guardian_v2.py      # 主守護進程 (本文件)
├── whitelist.json                  # 動態白名單持久化
└── config.json                     # 運行時配置 (可選)

/var/log/longhun/
├── guardian.log                    # 人類可讀日誌
└── guardian_audit.jsonl            # 結構化審計鏈 (不可篡改)

/var/lib/longhun/
└── guardian_whitelist.json         # 動態白名單持久化

/etc/systemd/system/
└── longhun-guardian.service        # systemd 服務配置

/run/
└── longhun_guardian.pid            # PID 文件
```

---

## 八、DNA追溯驗證

每條審計記錄格式:

```json
{
  "時間戳": "2026-07-11T12:00:00Z",
  "級別": "🔴RED",
  "事件類型": "KILL",
  "內容": "🔴 進程已處決 PID:12345 Name:xmrig | 挖礦黑名單匹配:xmrig",
  "DNA": "#龍芯⚡️2026-07-11-GUARDIAN-v2.0",
  "UID": "UID9622",
  "巡邏序號": 1440,
  "元數據": {
    "pid": 12345,
    "name": "xmrig",
    "reason": "挖礦黑名單匹配:xmrig",
    "cpu_history": [0, 0, 92.5, 95.1, 94.8],
    "威脅評分": 97.3,
    "kill_count": 1
  },
  "哈希": "a1b2c3d4e5f67890"  // SHA256前16位，防篡改
}
```

驗證命令:
```bash
# 驗證最新記錄的哈希
jq -r '{時間戳,級別,事件類型,內容,DNA,UID,巡邏序號,元數據}' \
   /var/log/longhun/guardian_audit.jsonl | tail -1 | sha256sum | cut -c1-16
# 應與記錄中的"哈希"字段匹配
```

---

**DNA錨定**: `#龍芯⚡️2026-07-11-GUARDIAN-v2.0-LK9X-772Z`  
**君子協議**: CC BY-NC-SA 4.0 | **絕對防禦憲法**: v1.0 | **簽署人**: UID9622
