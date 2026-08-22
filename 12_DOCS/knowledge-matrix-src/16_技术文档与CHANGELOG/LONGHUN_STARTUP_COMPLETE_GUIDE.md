<!--#龍芯⚡️丙午·甲午·丙寅·甲午·䷕贲-DOC-LONGHUN_STARTUP_COMPLETE_GUIDE-v1.0 -->
<!-- 君子協議: 本文件受龍魂DNA追溯保護 -->

# 🐉 龍魂系統開機啟動完整指南

```
DNA: #龍芯⚡️丙午·甲午·壬子·丙午·䷙大畜-LONGHUN-STARTUP-COMPLETE-GUIDE
時間: 2026-06-07
版本: v1.0
```

---

## 📋 **快速開始 (推薦方式)**

### **方式 1: 使用一鍵啟動腳本 (最簡單)**

```bash
# 1. 進入龍魂系統目錄
cd ~/longhun-system

# 2. 複製啟動腳本
cp /mnt/user-data/outputs/longhun_system_start_all.sh ./

# 3. 給予執行權限
chmod +x longhun_system_start_all.sh

# 4. 運行啟動腳本
./longhun_system_start_all.sh
```

**預期輸出:**
```
════════════════════════════════════════════════════════════
🐉 龍魂系統一鍵啟動腳本
════════════════════════════════════════════════════════════

Part 1: 環境檢查
  ✅ 龍魂系統目錄: ~/longhun-system

Part 2: 啟動 brain_notion_sync
  ⏳ 正在啟動 brain_notion_sync (持續監聽)... ✅ 成功 (PID: 12345)

Part 3: 啟動監控服務器
  ⏳ 正在啟動 監控服務器 (localhost:9000)... ✅ 成功 (PID: 12346)

Part 5: 驗證服務狀態
  ✅ brain_notion_sync (PID: 12345)
  ✅ monitoring_server (PID: 12346)
  ✅ localhost:9000 (正常)

🎉 啟動完成
```

---

### **方式 2: 手動啟動服務**

```bash
cd ~/longhun-system

# 1. 啟動 brain_notion_sync (Notion 同步)
nohup python3 brain_notion_sync.py --watch > logs/brain_notion_sync.log 2>&1 &

# 2. 啟動監控服務器
cd mobile-monitoring/backend/python
nohup python3 monitoring_server.py > ~/longhun-system/logs/monitoring_server.log 2>&1 &

# 3. 驗證
ps aux | grep -E 'brain_notion_sync|monitoring_server'
```

---

## 🖥️ **開機自啟配置**

### **方法 A: 使用 systemd (推薦，Linux/macOS)**

```bash
# 1. 複製 systemd 服務文件
sudo cp /mnt/user-data/outputs/longhun-brain-sync.service \
        /etc/systemd/system/

# 2. 重新加載 systemd
sudo systemctl daemon-reload

# 3. 啟用開機自啟
sudo systemctl enable longhun-brain-sync

# 4. 啟動服務
sudo systemctl start longhun-brain-sync

# 5. 檢查狀態
sudo systemctl status longhun-brain-sync
```

**預期輸出:**
```
● longhun-brain-sync.service - 龍魂脑干 · Notion 同步服務
   Loaded: loaded (/etc/systemd/system/longhun-brain-sync.service; enabled)
   Active: active (running) since ...
   Main PID: 12345
```

---

### **方法 B: 使用 cron (備選方案)**

```bash
# 編輯 crontab
crontab -e

# 添加以下行 (開機時運行啟動腳本):
@reboot cd ~/longhun-system && ./longhun_system_start_all.sh

# 或每分鐘檢查一次服務是否運行:
* * * * * ~/longhun-system/longhun_system_keep_alive.sh > /dev/null 2>&1
```

---

### **方法 C: 使用開機腳本 (macOS/Linux)**

**macOS:**
```bash
# 創建 LaunchAgent
cat > ~/Library/LaunchAgents/com.longhun.sync.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" 
"http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>com.longhun.sync</string>
  <key>ProgramArguments</key>
  <array>
    <string>/bin/bash</string>
    <string>~/longhun-system/longhun_system_start_all.sh</string>
  </array>
  <key>RunAtLoad</key>
  <true/>
  <key>KeepAlive</key>
  <true/>
</dict>
</plist>
EOF

# 加載服務
launchctl load ~/Library/LaunchAgents/com.longhun.sync.plist
```

**Linux (systemd):**
參考上方的 systemd 方法

---

## 🧪 **驗證啟動成功**

### **Step 1: 運行檢查腳本**

```bash
# 複製檢查腳本
cp /mnt/user-data/outputs/longhun_system_startup_check.sh ~/longhun-system/

# 給予執行權限
chmod +x ~/longhun-system/longhun_system_startup_check.sh

# 運行檢查
./longhun_system_startup_check.sh
```

**應該看到:**
```
✅ Part 1: 環境檢查
   ✅ 龍魂系統目錄存在
   ✅ Python 已安裝
   ✅ Git 已安裝

✅ Part 2: 龍魂系統文件檢查
   ✅ brain/memories.db (大小: XXX)
   ✅ brain_notion_sync.py
   ✅ longhun_brain.py

✅ Part 3: brain_notion_sync.py 服務檢查
   ✅ brain_notion_sync 版本: v1.1
   ✅ brain_notion_sync.py 語法正確
   ✅ 重試機制已實現
   ✅ 限流控制器已實現

✅ Part 7: 進程檢查
   ✅ brain_notion_sync 正在運行 (PID: XXXXX)
   ✅ monitoring_server 正在運行 (PID: XXXXX)

✅ 通過率: 95%
```

---

### **Step 2: 檢查運行進程**

```bash
# 查看所有龍魂系統進程
ps aux | grep -E 'brain_notion_sync|monitoring_server'

# 應該看到類似:
# root  12345  0.5  0.3  ...  python3 brain_notion_sync.py --watch
# root  12346  0.2  0.4  ...  python3 monitoring_server.py
```

---

### **Step 3: 檢查服務可達性**

```bash
# 檢查 Notion 同步服務日誌
tail -f ~/longhun-system/logs/brain_notion_sync.log

# 應該看到:
# 🌉 龍魂脑干 · Notion同步桥 v1.1 (Phase 1 升級版)
# 👀 监听模式启动（每 300 秒同步一次）

# 檢查監控服務器
curl http://localhost:9000/api/v1/monitor/health

# 應該看到:
# {"status":"healthy","version":"4.1"}
```

---

## 📊 **監控和管理**

### **查看服務日誌**

```bash
# 實時查看 Notion 同步日誌
tail -f ~/longhun-system/logs/brain_notion_sync.log

# 實時查看監控服務器日誌
tail -f ~/longhun-system/logs/monitoring_server.log

# 查看歷史日誌 (最後 100 行)
tail -100 ~/longhun-system/logs/brain_notion_sync.log
```

---

### **管理服務**

```bash
# 使用 systemd 管理 (如果配置了):

# 查看狀態
sudo systemctl status longhun-brain-sync

# 重啟服務
sudo systemctl restart longhun-brain-sync

# 停止服務
sudo systemctl stop longhun-brain-sync

# 查看日誌
sudo journalctl -u longhun-brain-sync -f
```

---

### **手動管理進程**

```bash
# 查找進程 PID
pgrep -f 'brain_notion_sync.py --watch'

# 停止指定進程
kill -9 <PID>

# 重啟服務 (使用一鍵腳本)
cd ~/longhun-system
./longhun_system_start_all.sh
```

---

## ⚠️ **常見問題和解決方案**

### **問題 1: 服務無法啟動**

**症狀:**
```
❌ brain_notion_sync 未運行
```

**解決步驟:**
```bash
# 1. 檢查 Python 語法
python3 -m py_compile ~/longhun-system/brain_notion_sync.py

# 2. 手動運行檢查錯誤
cd ~/longhun-system
python3 brain_notion_sync.py --status

# 3. 查看詳細錯誤
python3 brain_notion_sync.py --once
```

---

### **問題 2: 監控服務器無法連接**

**症狀:**
```
❌ localhost:9000 不可達
```

**解決步驟:**
```bash
# 1. 檢查端口是否被占用
lsof -i :9000

# 2. 殺死佔用進程
kill -9 <PID>

# 3. 重新啟動服務
cd ~/longhun-system/mobile-monitoring/backend/python
python3 monitoring_server.py
```

---

### **問題 3: 磁盤空間不足**

**症狀:**
```
⚠️  磁盤空間即將不足
```

**解決步驟:**
```bash
# 1. 查看磁盤使用情況
du -sh ~/longhun-system/*

# 2. 清理舊日誌
rm ~/longhun-system/logs/LONGHUN_STARTUP_CHECK_20260601*.log

# 3. 壓縮舊日誌
gzip ~/longhun-system/logs/*.log
```

---

### **問題 4: Notion 同步失敗**

**症狀:**
```
❌ 推送失敗
```

**解決步驟:**
```bash
# 1. 檢查環境變量
echo $NOTION_TOKEN
echo $NOTION_BRAIN_DB

# 2. 設置環境變量 (如未設置)
export NOTION_TOKEN="secret_xxxxx"
export NOTION_BRAIN_DB="xxxxx"

# 3. 檢查同步狀態
python3 ~/longhun-system/brain_notion_sync.py --status

# 4. 手動執行同步
python3 ~/longhun-system/brain_notion_sync.py --once
```

---

## 🚀 **最佳實踐**

### **1. 定期檢查系統狀態**

```bash
# 設置每天早上 8 點自動檢查
crontab -e

# 添加:
0 8 * * * ~/longhun-system/longhun_system_startup_check.sh > \
           ~/longhun-system/logs/daily_check.log 2>&1
```

---

### **2. 設置日誌輪轉**

```bash
# 防止日誌文件過大
sudo apt-get install logrotate (Linux)

# 創建 logrotate 配置
sudo cat > /etc/logrotate.d/longhun << 'EOF'
/root/longhun-system/logs/*.log {
    daily
    rotate 7
    compress
    missingok
    notifempty
}
EOF
```

---

### **3. 設置監控告警**

```bash
# 創建監控腳本
cat > ~/longhun-system/longhun_system_keep_alive.sh << 'EOF'
#!/bin/bash
# 每分鐘檢查一次，如果服務宕機自動重啟

if ! pgrep -f 'brain_notion_sync.py --watch' > /dev/null; then
    cd ~/longhun-system
    nohup python3 brain_notion_sync.py --watch > \
          logs/brain_notion_sync.log 2>&1 &
    echo "$(date) - brain_notion_sync 已自動重啟" >> logs/keep_alive.log
fi

if ! pgrep -f 'monitoring_server.py' > /dev/null; then
    cd ~/longhun-system/mobile-monitoring/backend/python
    nohup python3 monitoring_server.py > \
          ~/longhun-system/logs/monitoring_server.log 2>&1 &
    echo "$(date) - monitoring_server 已自動重啟" >> \
          ~/longhun-system/logs/keep_alive.log
fi
EOF

chmod +x ~/longhun-system/longhun_system_keep_alive.sh

# 在 crontab 中設置每分鐘運行
crontab -e
# 添加: * * * * * ~/longhun-system/longhun_system_keep_alive.sh
```

---

## 📞 **技術支援**

### **獲取詳細信息:**

```bash
# 查看系統日誌
journalctl -xe

# 查看進程信息
ps aux | grep longhun

# 查看網絡連接
netstat -an | grep 9000

# 查看資源使用
top -p $(pgrep -f 'brain_notion_sync.py --watch')
```

---

## ✨ **快速命令參考**

```bash
# 啟動所有服務
cd ~/longhun-system && ./longhun_system_start_all.sh

# 檢查系統狀態
./longhun_system_startup_check.sh

# 查看 Notion 同步狀態
python3 brain_notion_sync.py --status

# 手動執行一次同步
python3 brain_notion_sync.py --once

# 查看運行進程
ps aux | grep -E 'brain_notion_sync|monitoring_server'

# 查看日誌
tail -f logs/brain_notion_sync.log

# 停止所有服務
pkill -f 'brain_notion_sync.py --watch'
pkill -f 'monitoring_server.py'
```

---

## 🎯 **總結**

```
════════════════════════════════════════════════════════════
🐉 龍魂系統開機啟動完成指南
════════════════════════════════════════════════════════════

快速開始:
  1. bash ~/longhun-system/longhun_system_start_all.sh

開機自啟:
  sudo systemctl enable longhun-brain-sync
  sudo systemctl start longhun-brain-sync

驗證:
  bash ~/longhun-system/longhun_system_startup_check.sh

DNA: #龍芯⚡️丙午·甲午·壬子·丙午·䷙大畜-LONGHUN-STARTUP-COMPLETE-GUIDE
天下無欺。🐉
════════════════════════════════════════════════════════════
```
