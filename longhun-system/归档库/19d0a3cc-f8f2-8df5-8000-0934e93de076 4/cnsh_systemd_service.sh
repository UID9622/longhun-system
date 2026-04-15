#!/bin/bash
# CNSH 开机自动启动 + 监控守护脚本
# 安装到服务器后，开机自动运行，挂了自动重启
# UID9622 专用

echo "🐉 CNSH 系统守护脚本 - 安装中..."

# 创建systemd服务文件
cat > /etc/systemd/system/cnsh.service << 'EOF'
[Unit]
Description=CNSH 龍魂系统 - UID9622
Documentation=https://gitee.com/uid9622/cnsh
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/cnsh

# 启动命令
ExecStart=/usr/bin/node /root/cnsh/src/server.js

# 重启策略：挂了自动重启，最多10次
Restart=always
RestartSec=5
StartLimitInterval=60s
StartLimitBurst=10

# 环境变量
Environment=NODE_ENV=production
Environment=CNSH_MODE=daemon
Environment=UID9622_HOME=/root/cnsh

# 日志
StandardOutput=append:/var/log/cnsh/cnsh.log
StandardError=append:/var/log/cnsh/cnsh-error.log

[Install]
WantedBy=multi-user.target
EOF

# 创建日志目录
mkdir -p /var/log/cnsh

# 创建监控脚本
cat > /root/cnsh/monitor.sh << 'EOF'
#!/bin/bash
# CNSH 监控脚本 - 每分钟检查一次

LOG_FILE="/var/log/cnsh/monitor.log"
CNSH_URL="http://localhost:3000/health"  # 假设服务有健康检查接口

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> $LOG_FILE
}

# 检查服务是否在运行
check_service() {
    if ! pgrep -f "cnsh/src/server.js" > /dev/null; then
        log "⚠️ CNSH服务未运行，准备重启..."
        systemctl restart cnsh
        log "✅ CNSH服务已重启"
        return 1
    fi
    return 0
}

# 检查端口是否监听
check_port() {
    if ! netstat -tlnp | grep -q ":3000"; then
        log "⚠️ 端口3000未监听，准备重启..."
        systemctl restart cnsh
        log "✅ CNSH服务已重启"
        return 1
    fi
    return 0
}

# 检查内存使用（超过80%重启）
check_memory() {
    MEM_USAGE=$(free | grep Mem | awk '{printf "%.0f", $3/$2 * 100}')
    if [ "$MEM_USAGE" -gt 80 ]; then
        log "⚠️ 内存使用过高: ${MEM_USAGE}%，准备重启CNSH..."
        systemctl restart cnsh
        log "✅ CNSH服务已重启"
        return 1
    fi
    return 0
}

# 主检查
log "🔍 开始监控检查..."
check_service
check_port
check_memory
log "✅ 监控检查完成"
EOF

chmod +x /root/cnsh/monitor.sh

# 创建crontab定时任务
cat > /etc/cron.d/cnsh-monitor << 'EOF'
# CNSH 监控 - 每分钟检查一次
* * * * * root /root/cnsh/monitor.sh
EOF

# 重新加载systemd
systemctl daemon-reload

# 启用开机启动
systemctl enable cnsh

echo "✅ CNSH系统守护安装完成！"
echo ""
echo "📋 使用命令："
echo "   systemctl start cnsh    # 启动服务"
echo "   systemctl stop cnsh     # 停止服务"
echo "   systemctl restart cnsh  # 重启服务"
echo "   systemctl status cnsh   # 查看状态"
echo ""
echo "📊 查看日志："
echo "   tail -f /var/log/cnsh/cnsh.log"
echo "   tail -f /var/log/cnsh/monitor.log"
echo ""
echo "🐉 UID9622 - 龍魂系统永不掉线！"
