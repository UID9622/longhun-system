#!/bin/bash
# CNSH 快速启动脚本 - 手动执行用
# 在服务器上运行: bash cnsh_quick_start.sh

echo "🐉 CNSH 龍魂系统 - 快速启动"
echo "═══════════════════════════════════════════════════════════════"

# 检查是否已安装守护
if [ -f "/etc/systemd/system/cnsh.service" ]; then
    echo "✅ 守护服务已安装"
    echo ""
    echo "当前状态:"
    systemctl is-active cnsh && echo "   🟢 运行中" || echo "   🔴 已停止"
    echo ""
    echo "请选择操作:"
    echo "   1) 启动服务"
    echo "   2) 停止服务"
    echo "   3) 重启服务"
    echo "   4) 查看状态"
    echo "   5) 查看日志"
    echo "   6) 重新安装守护"
    echo "   0) 退出"
    echo ""
    read -p "请输入选项 [0-6]: " choice
    
    case $choice in
        1) systemctl start cnsh && echo "✅ 服务已启动" || echo "❌ 启动失败" ;;
        2) systemctl stop cnsh && echo "✅ 服务已停止" || echo "❌ 停止失败" ;;
        3) systemctl restart cnsh && echo "✅ 服务已重启" || echo "❌ 重启失败" ;;
        4) systemctl status cnsh ;;
        5) tail -f /var/log/cnsh/cnsh.log ;;
        6) bash install_cnsh_daemon.sh ;;
        0) echo "👋 再见"; exit 0 ;;
        *) echo "❌ 无效选项" ;;
    esac
else
    echo "⚠️ 守护服务未安装"
    echo ""
    echo "请选择:"
    echo "   1) 安装守护（推荐，开机自动启动）"
    echo "   2) 临时启动（不安装守护）"
    echo "   0) 退出"
    echo ""
    read -p "请输入选项 [0-2]: " choice
    
    case $choice in
        1) 
            if [ -f "install_cnsh_daemon.sh" ]; then
                bash install_cnsh_daemon.sh
            else
                echo "❌ install_cnsh_daemon.sh 不存在"
                echo "   请先下载安装脚本"
            fi
            ;;
        2) 
            echo "🚀 临时启动CNSH..."
            cd /root/cnsh
            nohup node src/server.js > /tmp/cnsh.log 2>&1 &
            sleep 2
            if pgrep -f "cnsh/src/server.js" > /dev/null; then
                echo "✅ CNSH已临时启动"
                echo "   PID: $(pgrep -f "cnsh/src/server.js")"
                echo "   日志: tail -f /tmp/cnsh.log"
            else
                echo "❌ 启动失败"
            fi
            ;;
        0) echo "👋 再见"; exit 0 ;;
        *) echo "❌ 无效选项" ;;
    esac
fi
