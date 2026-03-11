#!/bin/bash
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# notion-monitor-daemon.sh
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Copyright © 2026 UID9622 诸葛鑫（龍芯北辰）
# GPG指纹：A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 理论指导：曾仕强老师（永恒显示）
# DNA追溯码：#龍芯⚡️20260310-notion-monitor-daemon-v1.0
# 确认码：#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 共建致谢：Claude (Anthropic PBC) · Notion
# 创作地：中华人民共和国
# 献礼：新中国成立77周年（1949-2026）· 丙午马年
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# CNSH Notion 页面监控器 - 后台服务管理脚本

# 脚本配置
SERVICE_NAME="notion-monitor"
PID_FILE="/Users/zuimeidedeyihan/LuckyCommandCenter/cnsh-deployment/.notion-monitor.pid"
LOG_FILE="/Users/zuimeidedeyihan/LuckyCommandCenter/cnsh-deployment/notion-monitor.log"
MONITOR_SCRIPT="/Users/zuimeidedeyihan/LuckyCommandCenter/cnsh-deployment/notion-monitor.js"

# 函数：显示帮助信息
show_help() {
    echo "CNSH Notion 页面监控器 - 后台服务管理"
    echo ""
    echo "用法: $0 {start|stop|restart|status|logs}"
    echo ""
    echo "命令:"
    echo "  start    - 启动监控器后台服务"
    echo "  stop     - 停止监控器后台服务"
    echo "  restart  - 重启监控器后台服务"
    echo "  status   - 查看监控器服务状态"
    echo "  logs     - 查看监控器日志"
    echo ""
}

# 函数：检查服务状态
check_status() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p "$PID" > /dev/null 2>&1; then
            return 0  # 运行中
        else
            rm -f "$PID_FILE"  # 清理无效的PID文件
            return 1  # 已停止
        fi
    else
        return 1  # 已停止
    fi
}

# 函数：启动服务
start_service() {
    if check_status; then
        echo "✅ Notion 监控器已在运行中 (PID: $(cat $PID_FILE))"
        return 0
    fi
    
    echo "🚀 正在启动 Notion 监控器后台服务..."
    
    # 确保日志目录存在
    mkdir -p "$(dirname "$LOG_FILE")"
    
    # 检查 Node.js 是否安装
    if ! command -v node &> /dev/null; then
        echo "❌ 错误: 未找到 Node.js，请先安装 Node.js"
        exit 1
    fi
    
    # 检查监控脚本是否存在
    if [ ! -f "$MONITOR_SCRIPT" ]; then
        echo "❌ 错误: 找不到监控脚本 $MONITOR_SCRIPT"
        exit 1
    fi
    
    # 检查依赖是否安装
    if [ ! -d "node_modules" ]; then
        echo "📦 正在安装依赖..."
        npm install
    fi
    
    # 启动后台服务
    nohup node "$MONITOR_SCRIPT" >> "$LOG_FILE" 2>&1 &
    PID=$!
    echo "$PID" > "$PID_FILE"
    
    # 验证启动是否成功
    sleep 2
    if check_status; then
        echo "✅ Notion 监控器已启动 (PID: $PID)"
        echo "📝 日志文件: $LOG_FILE"
        echo "💡 使用 '$0 logs' 查看日志，'$0 stop' 停止服务"
    else
        echo "❌ 启动失败，请检查日志: $LOG_FILE"
        rm -f "$PID_FILE"
        exit 1
    fi
}

# 函数：停止服务
stop_service() {
    if ! check_status; then
        echo "ℹ️ Notion 监控器未在运行"
        return 0
    fi
    
    PID=$(cat "$PID_FILE")
    echo "🛑 正在停止 Notion 监控器 (PID: $PID)..."
    
    # 尝试正常终止进程
    kill "$PID"
    
    # 等待进程结束
    for i in {1..10}; do
        if ! ps -p "$PID" > /dev/null 2>&1; then
            echo "✅ Notion 监控器已停止"
            rm -f "$PID_FILE"
            return 0
        fi
        sleep 1
    done
    
    # 如果正常终止失败，强制终止
    echo "⚠️ 正常终止失败，强制结束进程..."
    kill -9 "$PID" 2>/dev/null
    rm -f "$PID_FILE"
    echo "✅ Notion 监控器已强制停止"
}

# 函数：重启服务
restart_service() {
    echo "🔄 正在重启 Notion 监控器..."
    stop_service
    sleep 2
    start_service
}

# 函数：查看日志
view_logs() {
    if [ ! -f "$LOG_FILE" ]; then
        echo "📝 日志文件不存在"
        return 0
    fi
    
    echo "📝 Notion 监控器日志 (最近50行):"
    echo "----------------------------------------"
    tail -n 50 "$LOG_FILE"
    echo "----------------------------------------"
    echo "💡 使用 'tail -f $LOG_FILE' 实时查看日志"
}

# 主逻辑
case "$1" in
    start)
        start_service
        ;;
    stop)
        stop_service
        ;;
    restart)
        restart_service
        ;;
    status)
        if check_status; then
            echo "✅ Notion 监控器正在运行 (PID: $(cat $PID_FILE))"
            echo "📝 日志文件: $LOG_FILE"
        else
            echo "❌ Notion 监控器未在运行"
        fi
        ;;
    logs)
        view_logs
        ;;
    *)
        show_help
        exit 1
        ;;
esac

exit 0