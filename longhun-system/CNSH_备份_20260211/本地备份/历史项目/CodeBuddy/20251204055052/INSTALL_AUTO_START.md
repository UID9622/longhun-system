# MCP-mini 自动启动配置指南

## 🚀 快速启动（推荐）

### 使用服务管理脚本
```bash
# 启动服务
./service.sh start

# 停止服务
./service.sh stop

# 重启服务  
./service.sh restart

# 查看状态
./service.sh status
```

## 🖥️ macOS 系统级自动启动

### 安装 LaunchAgent（开机自启动）
```bash
# 1. 复制 plist 文件到用户 LaunchAgents 目录
cp com.uid9622.mcp-mini.plist ~/Library/LaunchAgents/

# 2. 加载 LaunchAgent
launchctl load ~/Library/LaunchAgents/com.uid9622.mcp-mini.plist

# 3. 启动服务
launchctl start com.uid9622.mcp-mini
```

### 卸载 LaunchAgent
```bash
# 停止服务
launchctl stop com.uid9622.mcp-mini

# 卸载 LaunchAgent
launchctl unload ~/Library/LaunchAgents/com.uid9622.mcp-mini.plist

# 删除 plist 文件
rm ~/Library/LaunchAgents/com.uid9622.mcp-mini.plist
```

## 🐳 Docker 自动启动

### 使用 Docker Compose
```bash
# 启动服务（后台运行，自动重启）
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down

# 重启服务
docker-compose restart
```

### Docker 开机自启动
```bash
# 设置 Docker 开机自启动
sudo brew services start docker

# 或者使用系统命令
sudo launchctl load -w /Library/LaunchDaemons/com.docker.docker.plist
```

## 📱 推荐方案

### 方案一：简单使用（推荐日常使用）
```bash
# 添加到 .zshrc 或 .bash_profile 的别名
echo 'alias mcp-start="cd /Users/zuimeidedeyihan/CodeBuddy/20251204055052 && ./service.sh start"' >> ~/.zshrc
echo 'alias mcp-stop="cd /Users/zuimeidedeyihan/CodeBuddy/20251204055052 && ./service.sh stop"' >> ~/.zshrc
echo 'alias mcp-status="cd /Users/zuimeidedeyihan/CodeBuddy/20251204055052 && ./service.sh status"' >> ~/.zshrc

# 重新加载配置
source ~/.zshrc
```

使用时只需：
```bash
mcp-start    # 启动服务
mcp-status   # 查看状态  
mcp-stop     # 停止服务
```

### 方案二：完全自动化（适合服务器）
使用 LaunchAgent 实现开机自启动，服务崩溃自动重启。

### 方案三：Docker 方式（适合生产环境）
数据持久化，隔离性好，便于管理。

## 🔍 故障排除

### 端口被占用
```bash
# 查看占用端口的进程
lsof -i :8787

# 强制结束进程
kill -9 $(lsof -ti:8787)
```

### 查看日志
```bash
# 服务日志
tail -f logs/mcp.log

# 错误日志
tail -f logs/mcp_error.log
```

### 手动启动（调试模式）
```bash
cd /Users/zuimeidedeyihan/CodeBuddy/20251204055052
source venv/bin/activate
python3 app.py
```

## 📊 服务监控

服务启动后可访问：
- **主服务**: http://localhost:8787
- **审计记录**: http://localhost:8787/audit?limit=10
- **人格配置**: http://localhost:8787/personas
- **甲骨片段**: http://localhost:8787/bones

---

**推荐使用方案一的别名方式，简单便捷！** 🎯

---
🔐 数字主权签名防护系统
📅 签名时间: 2025-12-18 03:24:11
🧬 DNA追溯码: #CNSH-SIGNATURE-9bec5842-20251218032411
🌐 签名人: 龙魂文化加密系统
💬 方言确认: 东北话确认：没毛病，内容真实可靠
⚡ 卦象防护: 蒙卦：山下出泉，君子以果行育德
📜 内容哈希: 90fe613b021f7c64
⚠️ 警告: 未经授权修改将触发DNA追溯系统
