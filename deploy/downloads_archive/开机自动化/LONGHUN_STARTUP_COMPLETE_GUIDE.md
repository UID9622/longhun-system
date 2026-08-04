# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 🐉 龍魂系统开机启动完整指南

```
DNA: #龍芯⚡️2026-06-07-LONGHUN-STARTUP-COMPLETE-GUIDE
时间: 2026-06-07
版本: v1.0
```

---

## 📋 **快速开始 (推荐方式)**

### **方式 1: 使用一键启动脚本 (最简单)**

```bash
# 1. 进入龍魂系统目录
cd ~/longhun-system

# 2. 复制启动脚本
cp /mnt/user-data/outputs/longhun_system_start_all.sh ./

# 3. 给予执行权限
chmod +x longhun_system_start_all.sh

# 4. 运行启动脚本
./longhun_system_start_all.sh
```

**预期输出:**
```
════════════════════════════════════════════════════════════
🐉 龍魂系统一键启动脚本
════════════════════════════════════════════════════════════

Part 1: 环境检查
  ✅ 龍魂系统目录: ~/longhun-system

Part 2: 启动 brain_notion_sync
  ⏳ 正在启动 brain_notion_sync (持续监听)... ✅ 成功 (PID: 12345)

Part 3: 启动监控服务器
  ⏳ 正在启动 监控服务器 (localhost:9000)... ✅ 成功 (PID: 12346)

Part 5: 验证服务状态
  ✅ brain_notion_sync (PID: 12345)
  ✅ monitoring_server (PID: 12346)
  ✅ localhost:9000 (正常)

🎉 启动完成
```

---

### **方式 2: 手动启动服务**

```bash
cd ~/longhun-system

# 1. 启动 brain_notion_sync (Notion 同步)
nohup python3 brain_notion_sync.py --watch > logs/brain_notion_sync.log 2>&1 &

# 2. 启动监控服务器
cd mobile-monitoring/backend/python
nohup python3 monitoring_server.py > ~/longhun-system/logs/monitoring_server.log 2>&1 &

# 3. 验证
ps aux | grep -E 'brain_notion_sync|monitoring_server'
```

---

## 🖥️ **开机自启配置**

### **方法 A: 使用 systemd (推荐，Linux/macOS)**

```bash
# 1. 复制 systemd 服务文件
sudo cp /mnt/user-data/outputs/longhun-brain-sync.service \
        /etc/systemd/system/

# 2. 重新加载 systemd
sudo systemctl daemon-reload

# 3. 启用开机自启
sudo systemctl enable longhun-brain-sync

# 4. 启动服务
sudo systemctl start longhun-brain-sync

# 5. 检查状态
sudo systemctl status longhun-brain-sync
```

**预期输出:**
```
● longhun-brain-sync.service - 龍魂脑干 · Notion 同步服务
   Loaded: loaded (/etc/systemd/system/longhun-brain-sync.service; enabled)
   Active: active (running) since ...
   Main PID: 12345
```

---

### **方法 B: 使用 cron (备选方案)**

```bash
# 编辑 crontab
crontab -e

# 添加以下行 (开机时运行启动脚本):
@reboot cd ~/longhun-system && ./longhun_system_start_all.sh

# 或每分钟检查一次服务是否运行:
* * * * * ~/longhun-system/longhun_system_keep_alive.sh > /dev/null 2>&1
```

---

### **方法 C: 使用开机脚本 (macOS/Linux)**

**macOS:**
```bash
# 创建 LaunchAgent
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

# 加载服务
launchctl load ~/Library/LaunchAgents/com.longhun.sync.plist
```

**Linux (systemd):**
参考上方的 systemd 方法

---

## 🧪 **验证启动成功**

### **Step 1: 运行检查脚本**

```bash
# 复制检查脚本
cp /mnt/user-data/outputs/longhun_system_startup_check.sh ~/longhun-system/

# 给予执行权限
chmod +x ~/longhun-system/longhun_system_startup_check.sh

# 运行检查
./longhun_system_startup_check.sh
```

**应该看到:**
```
✅ Part 1: 环境检查
   ✅ 龍魂系统目录存在
   ✅ Python 已安装
   ✅ Git 已安装

✅ Part 2: 龍魂系统文件检查
   ✅ brain/memories.db (大小: XXX)
   ✅ brain_notion_sync.py
   ✅ longhun_brain.py

✅ Part 3: brain_notion_sync.py 服务检查
   ✅ brain_notion_sync 版本: v1.1
   ✅ brain_notion_sync.py 语法正确
   ✅ 重试机制已实现
   ✅ 限流控制器已实现

✅ Part 7: 进程检查
   ✅ brain_notion_sync 正在运行 (PID: XXXXX)
   ✅ monitoring_server 正在运行 (PID: XXXXX)

✅ 通过率: 95%
```

---

### **Step 2: 检查运行进程**

```bash
# 查看所有龍魂系统进程
ps aux | grep -E 'brain_notion_sync|monitoring_server'

# 应该看到类似:
# root  12345  0.5  0.3  ...  python3 brain_notion_sync.py --watch
# root  12346  0.2  0.4  ...  python3 monitoring_server.py
```

---

### **Step 3: 检查服务可达性**

```bash
# 检查 Notion 同步服务日志
tail -f ~/longhun-system/logs/brain_notion_sync.log

# 应该看到:
# 🌉 龍魂脑干 · Notion同步桥 v1.1 (Phase 1 升级版)
# 👀 监听模式启动（每 300 秒同步一次）

# 检查监控服务器
curl http://localhost:9000/api/v1/monitor/health

# 应该看到:
# {"status":"healthy","version":"4.1"}
```

---

## 📊 **监控和管理**

### **查看服务日志**

```bash
# 实时查看 Notion 同步日志
tail -f ~/longhun-system/logs/brain_notion_sync.log

# 实时查看监控服务器日志
tail -f ~/longhun-system/logs/monitoring_server.log

# 查看历史日志 (最后 100 行)
tail -100 ~/longhun-system/logs/brain_notion_sync.log
```

---

### **管理服务**

```bash
# 使用 systemd 管理 (如果配置了):

# 查看状态
sudo systemctl status longhun-brain-sync

# 重启服务
sudo systemctl restart longhun-brain-sync

# 停止服务
sudo systemctl stop longhun-brain-sync

# 查看日志
sudo journalctl -u longhun-brain-sync -f
```

---

### **手动管理进程**

```bash
# 查找进程 PID
pgrep -f 'brain_notion_sync.py --watch'

# 停止指定进程
kill -9 <PID>

# 重启服务 (使用一键脚本)
cd ~/longhun-system
./longhun_system_start_all.sh
```

---

## ⚠️ **常见问题和解决方案**

### **问题 1: 服务无法启动**

**症状:**
```
❌ brain_notion_sync 未运行
```

**解决步骤:**
```bash
# 1. 检查 Python 语法
python3 -m py_compile ~/longhun-system/brain_notion_sync.py

# 2. 手动运行检查错误
cd ~/longhun-system
python3 brain_notion_sync.py --status

# 3. 查看详细错误
python3 brain_notion_sync.py --once
```

---

### **问题 2: 监控服务器无法连接**

**症状:**
```
❌ localhost:9000 不可达
```

**解决步骤:**
```bash
# 1. 检查端口是否被占用
lsof -i :9000

# 2. 杀死占用进程
kill -9 <PID>

# 3. 重新启动服务
cd ~/longhun-system/mobile-monitoring/backend/python
python3 monitoring_server.py
```

---

### **问题 3: 磁盘空间不足**

**症状:**
```
⚠️  磁盘空间即将不足
```

**解决步骤:**
```bash
# 1. 查看磁盘使用情况
du -sh ~/longhun-system/*

# 2. 清理旧日志
rm ~/longhun-system/logs/LONGHUN_STARTUP_CHECK_20260601*.log

# 3. 压缩旧日志
gzip ~/longhun-system/logs/*.log
```

---

### **问题 4: Notion 同步失败**

**症状:**
```
❌ 推送失败
```

**解决步骤:**
```bash
# 1. 检查环境变量
echo $NOTION_TOKEN
echo $NOTION_BRAIN_DB

# 2. 设置环境变量 (如未设置)
export NOTION_TOKEN="secret_xxxxx"
export NOTION_BRAIN_DB="xxxxx"

# 3. 检查同步状态
python3 ~/longhun-system/brain_notion_sync.py --status

# 4. 手动执行同步
python3 ~/longhun-system/brain_notion_sync.py --once
```

---

## 🚀 **最佳实践**

### **1. 定期检查系统状态**

```bash
# 设置每天早上 8 点自动检查
crontab -e

# 添加:
0 8 * * * ~/longhun-system/longhun_system_startup_check.sh > \
           ~/longhun-system/logs/daily_check.log 2>&1
```

---

### **2. 设置日志轮转**

```bash
# 防止日志文件过大
sudo apt-get install logrotate (Linux)

# 创建 logrotate 配置
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

### **3. 设置监控告警**

```bash
# 创建监控脚本
cat > ~/longhun-system/longhun_system_keep_alive.sh << 'EOF'
#!/bin/bash
# 每分钟检查一次，如果服务宕机自动重启

if ! pgrep -f 'brain_notion_sync.py --watch' > /dev/null; then
    cd ~/longhun-system
    nohup python3 brain_notion_sync.py --watch > \
          logs/brain_notion_sync.log 2>&1 &
    echo "$(date) - brain_notion_sync 已自动重启" >> logs/keep_alive.log
fi

if ! pgrep -f 'monitoring_server.py' > /dev/null; then
    cd ~/longhun-system/mobile-monitoring/backend/python
    nohup python3 monitoring_server.py > \
          ~/longhun-system/logs/monitoring_server.log 2>&1 &
    echo "$(date) - monitoring_server 已自动重启" >> \
          ~/longhun-system/logs/keep_alive.log
fi
EOF

chmod +x ~/longhun-system/longhun_system_keep_alive.sh

# 在 crontab 中设置每分钟运行
crontab -e
# 添加: * * * * * ~/longhun-system/longhun_system_keep_alive.sh
```

---

## 📞 **技术支援**

### **获取详细信息:**

```bash
# 查看系统日志
journalctl -xe

# 查看进程信息
ps aux | grep longhun

# 查看网络连接
netstat -an | grep 9000

# 查看资源使用
top -p $(pgrep -f 'brain_notion_sync.py --watch')
```

---

## ✨ **快速命令参考**

```bash
# 启动所有服务
cd ~/longhun-system && ./longhun_system_start_all.sh

# 检查系统状态
./longhun_system_startup_check.sh

# 查看 Notion 同步状态
python3 brain_notion_sync.py --status

# 手动执行一次同步
python3 brain_notion_sync.py --once

# 查看运行进程
ps aux | grep -E 'brain_notion_sync|monitoring_server'

# 查看日志
tail -f logs/brain_notion_sync.log

# 停止所有服务
pkill -f 'brain_notion_sync.py --watch'
pkill -f 'monitoring_server.py'
```

---

## 🎯 **总结**

```
════════════════════════════════════════════════════════════
🐉 龍魂系统开机启动完成指南
════════════════════════════════════════════════════════════

快速开始:
  1. bash ~/longhun-system/longhun_system_start_all.sh

开机自启:
  sudo systemctl enable longhun-brain-sync
  sudo systemctl start longhun-brain-sync

验证:
  bash ~/longhun-system/longhun_system_startup_check.sh

DNA: #龍芯⚡️2026-06-07-LONGHUN-STARTUP-COMPLETE-GUIDE
天下无欺。🐉
════════════════════════════════════════════════════════════
```
