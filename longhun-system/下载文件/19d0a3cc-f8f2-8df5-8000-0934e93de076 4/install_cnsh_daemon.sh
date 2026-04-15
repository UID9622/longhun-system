#!/bin/bash
# CNSH 一键安装守护脚本
# 在服务器上执行：curl -sSL http://你的地址/install_cnsh_daemon.sh | bash
# 或者先下载再执行

echo "═══════════════════════════════════════════════════════════════"
echo "🐉 CNSH 龍魂系统 - 守护安装脚本"
echo "   UID9622 专用"
echo "═══════════════════════════════════════════════════════════════"
echo ""

# 检查是否在root权限下运行
if [ "$EUID" -ne 0 ]; then 
    echo "❌ 请使用root权限运行: sudo bash install_cnsh_daemon.sh"
    exit 1
fi

# 检查CNSH目录是否存在
if [ ! -d "/root/cnsh" ]; then
    echo "❌ /root/cnsh 目录不存在！"
    echo "   请先克隆仓库: git clone https://gitee.com/uid9622/cnsh.git /root/cnsh"
    exit 1
fi

echo "📦 步骤1/5: 创建systemd服务..."

cat > /etc/systemd/system/cnsh.service << 'EOF'
[Unit]
Description=CNSH 龍魂系统 - UID9622
Documentation=https://gitee.com/uid9622/cnsh
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/cnsh

# 启动前检查
ExecStartPre=/bin/bash -c 'if [ ! -f /root/cnsh/src/server.js ]; then echo "错误: server.js不存在"; exit 1; fi'

# 启动命令
ExecStart=/usr/bin/node /root/cnsh/src/server.js

# 优雅停止
ExecStop=/bin/kill -SIGTERM $MAINPID
ExecStopPost=/bin/sleep 2

# 重启策略：挂了自动重启
Restart=always
RestartSec=5
StartLimitInterval=60s
StartLimitBurst=10

# 环境变量
Environment=NODE_ENV=production
Environment=CNSH_MODE=daemon
Environment=UID9622_HOME=/root/cnsh
Environment=PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

# 日志
StandardOutput=append:/var/log/cnsh/cnsh.log
StandardError=append:/var/log/cnsh/cnsh-error.log

# 资源限制（防止吃光内存）
MemoryMax=512M
CPUQuota=50%

[Install]
WantedBy=multi-user.target
EOF

echo "✅ systemd服务创建完成"
echo ""

echo "📦 步骤2/5: 创建日志目录..."
mkdir -p /var/log/cnsh
touch /var/log/cnsh/cnsh.log
touch /var/log/cnsh/cnsh-error.log
touch /var/log/cnsh/monitor.log
echo "✅ 日志目录创建完成"
echo ""

echo "📦 步骤3/5: 创建监控脚本..."

cat > /root/cnsh/monitor.sh << 'EOF'
#!/bin/bash
# CNSH 监控脚本 - 每分钟检查一次
# UID9622 专用

LOG_FILE="/var/log/cnsh/monitor.log"
PID_FILE="/var/run/cnsh-monitor.pid"

# 防止重复运行
if [ -f "$PID_FILE" ]; then
    OLD_PID=$(cat "$PID_FILE")
    if ps -p "$OLD_PID" > /dev/null 2>&1; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] 监控脚本已在运行 (PID: $OLD_PID)" >> $LOG_FILE
        exit 0
    fi
fi
echo $$ > "$PID_FILE"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> $LOG_FILE
}

# 清理旧日志（保留7天）
if [ $(date +%M) -eq 00 ]; then
    find /var/log/cnsh -name "*.log" -mtime +7 -delete 2>/dev/null
fi

# 检查服务进程
check_process() {
    if ! pgrep -f "cnsh/src/server.js" > /dev/null 2>&1; then
        log "⚠️ CNSH进程不存在"
        return 1
    fi
    return 0
}

# 检查端口
check_port() {
    if ! ss -tlnp | grep -q ":3000"; then
        log "⚠️ 端口3000未监听"
        return 1
    fi
    return 0
}

# 检查内存
check_memory() {
    MEM_USAGE=$(free | awk '/Mem:/ {printf "%.0f", $3/$2 * 100}')
    if [ "$MEM_USAGE" -gt 85 ]; then
        log "⚠️ 内存使用过高: ${MEM_USAGE}%"
        return 1
    fi
    return 0
}

# 检查磁盘
check_disk() {
    DISK_USAGE=$(df / | awk 'NR==2 {print $5}' | sed 's/%//')
    if [ "$DISK_USAGE" -gt 90 ]; then
        log "⚠️ 磁盘使用过高: ${DISK_USAGE}%"
        return 1
    fi
    return 0
}

# 主检查
log "🔍 开始健康检查..."

NEED_RESTART=0

if ! check_process; then
    NEED_RESTART=1
fi

if ! check_port; then
    NEED_RESTART=1
fi

if ! check_memory; then
    NEED_RESTART=1
fi

if ! check_disk; then
    NEED_RESTART=1
fi

if [ $NEED_RESTART -eq 1 ]; then
    log "🔄 正在重启CNSH服务..."
    systemctl restart cnsh
    sleep 3
    
    # 验证重启成功
    if pgrep -f "cnsh/src/server.js" > /dev/null 2>&1; then
        log "✅ CNSH服务重启成功"
    else
        log "❌ CNSH服务重启失败，请手动检查"
    fi
else
    log "✅ 所有检查通过，服务运行正常"
fi

# 清理PID文件
rm -f "$PID_FILE"
EOF

chmod +x /root/cnsh/monitor.sh
echo "✅ 监控脚本创建完成"
echo ""

echo "📦 步骤4/5: 配置定时任务..."

# 创建crontab
cat > /etc/cron.d/cnsh-monitor << 'EOF'
# CNSH 龍魂系统监控 - 每分钟检查一次
# UID9622 专用
SHELL=/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

* * * * * root /root/cnsh/monitor.sh >> /var/log/cnsh/cron.log 2>&1

# 每天凌晨3点重启服务（清理内存）
0 3 * * * root systemctl restart cnsh

# 每周一清理日志
0 4 * * 1 root find /var/log/cnsh -name "*.log" -mtime +7 -delete
EOF

chmod 644 /etc/cron.d/cnsh-monitor
echo "✅ 定时任务配置完成"
echo ""

echo "📦 步骤5/5: 启用服务..."

# 重新加载systemd
systemctl daemon-reload

# 启用开机启动
systemctl enable cnsh

# 启动服务
systemctl start cnsh

# 等待服务启动
sleep 3

echo "✅ 服务已启用"
echo ""

echo "═══════════════════════════════════════════════════════════════"
echo "🎉 CNSH 龍魂系统守护安装完成！"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "📋 管理命令："
echo "   systemctl start cnsh      # 启动服务"
echo "   systemctl stop cnsh       # 停止服务"
echo "   systemctl restart cnsh    # 重启服务"
echo "   systemctl status cnsh     # 查看状态"
echo "   systemctl disable cnsh    # 取消开机启动"
echo ""
echo "📊 查看日志："
echo "   tail -f /var/log/cnsh/cnsh.log         # 主日志"
echo "   tail -f /var/log/cnsh/cnsh-error.log   # 错误日志"
echo "   tail -f /var/log/cnsh/monitor.log      # 监控日志"
echo ""
echo "🔍 快速诊断："
echo "   ps aux | grep cnsh        # 查看进程"
echo "   ss -tlnp | grep 3000      # 查看端口"
echo "   systemctl is-active cnsh  # 检查运行状态"
echo ""
echo "🐉 UID9622 - 龍魂系统永不掉线！"
echo "═══════════════════════════════════════════════════════════════"
