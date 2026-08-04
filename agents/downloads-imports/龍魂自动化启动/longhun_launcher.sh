#!/bin/bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
# 龍魂支付系统 · 主启动菜单
# LongHun System · Main Launcher Menu

clear

echo "╔════════════════════════════════════════════════════════════╗"
echo "║                                                            ║"
echo "║          🐉 龍魂支付系统 · 启动菜单                        ║"
echo "║          LongHun Payment System Launcher                  ║"
echo "║                                                            ║"
echo "║          Made with 💛 by UID9622 (诸葛鑫)                 ║"
echo "║                                                            ║"
echo "╚════════════════════════════════════════════════════════════╝"

echo ""
echo "请选择启动模式 (输入数字 1-8，然后按 Enter):"
echo ""
echo "  【演示和测试】"
echo "    1) 🎬 演示模式          - 快速5秒演示，看系统运行"
echo "    2) 🧪 自动化焊接        - 创建7笔测试交易，生成DNA"
echo "    3) 📊 系统统计          - 查看交易数、金额、费用"
echo ""
echo "  【交互操作】"
echo "    4) 💻 CLI命令行工具     - 手动创建交易、查询、导出"
echo "    5) 🌐 API服务器        - 启动Flask API (localhost:8888)"
echo "    6) 📜 启动脚本菜单      - 完整的交互式菜单"
echo ""
echo "  【维护和日志】"
echo "    7) 📋 查看日志          - 实时监控系统日志"
echo "    8) 🔧 系统健康检查      - 检查数据库、文件、权限"
echo ""
echo "  【其他】"
echo "    0) 🚪 退出              - 关闭菜单"
echo ""
echo "════════════════════════════════════════════════════════════"
echo ""

read -p "你的选择 [0-8]: " choice

LAUNCHER_PATH="/Users/zuimeidedeyihan/Downloads/龍魂自动化启动/longhun_launcher.sh"

case $choice in
    1)
        echo ""
        echo "🎬 启动演示模式..."
        echo ""
        cd ~/.龍魂/xpay
        python3 xpay_core.py
        echo ""
        read -p "按 Enter 返回菜单..."
        exec bash "$LAUNCHER_PATH"
        ;;
    2)
        echo ""
        echo "🧪 启动自动化焊接工程..."
        echo ""
        cd ~/.龍魂/xpay
        bash longhun_welding_automation.sh
        echo ""
        echo "✅ 焊接完成！"
        echo ""
        echo "📋 查看日志:"
        echo "   cat ~/.龍魂/xpay/logs/welding_*.log"
        echo ""
        read -p "按 Enter 返回菜单..."
        exec bash "$LAUNCHER_PATH"
        ;;
    3)
        echo ""
        echo "📊 系统统计..."
        echo ""
        cd ~/.龍魂/xpay
        python3 xpay_cli.py stats
        echo ""
        read -p "按 Enter 返回菜单..."
        exec bash "$LAUNCHER_PATH"
        ;;
    4)
        echo ""
        echo "💻 CLI命令行工具已启动"
        echo ""
        echo "可用命令:"
        echo "  transaction create --amount 100 --currency CNY --sender UID9622 --recipient UID1001"
        echo "  stats"
        echo "  export --path ~/dna_backup.json"
        echo ""
        echo "进入交互模式..."
        echo ""
        cd ~/.龍魂/xpay
        bash startup.sh
        echo ""
        read -p "按 Enter 返回菜单..."
        exec bash "$LAUNCHER_PATH"
        ;;
    5)
        echo ""
        echo "🌐 启动API服务器 (Flask)..."
        echo ""
        echo "API将在以下地址运行:"
        echo "  http://localhost:8888"
        echo ""
        echo "按 Ctrl+C 停止服务器"
        echo ""
        cd ~/.龍魂/xpay
        python3 xpay_server.py
        echo ""
        read -p "按 Enter 返回菜单..."
        exec bash "$LAUNCHER_PATH"
        ;;
    6)
        echo ""
        echo "📜 启动交互式菜单..."
        echo ""
        cd ~/.龍魂/xpay
        bash startup.sh
        echo ""
        read -p "按 Enter 返回菜单..."
        exec bash "$LAUNCHER_PATH"
        ;;
    7)
        echo ""
        echo "📋 查看系统日志 (Ctrl+C 退出)..."
        echo ""
        mkdir -p ~/.龍魂/xpay/logs
        tail -f ~/.龍魂/xpay/logs/*.log
        echo ""
        read -p "按 Enter 返回菜单..."
        exec bash "$LAUNCHER_PATH"
        ;;
    8)
        echo ""
        echo "🔧 系统健康检查..."
        echo ""
        echo "检查项目:"
        echo ""

        # 检查Python
        python_version=$(python3 --version 2>&1)
        echo "✅ Python版本: $python_version"

        # 检查目录
        if [ -d ~/.龍魂/xpay ]; then
            echo "✅ XPay目录: ~/.龍魂/xpay"
        else
            echo "❌ XPay目录: 不存在"
        fi

        # 检查数据库
        if [ -f ~/.龍魂/xpay/db/xpay.db ]; then
            echo "✅ 数据库: 存在"
        else
            echo "⚠️  数据库: 尚未创建 (首次运行时自动创建)"
        fi

        # 检查日志目录
        if [ -d ~/.龍魂/xpay/logs ]; then
            log_count=$(ls -1 ~/.龍魂/xpay/logs/*.log 2>/dev/null | wc -l)
            echo "✅ 日志目录: 存在 ($log_count 个日志文件)"
        else
            echo "⚠️  日志目录: 不存在 (将在首次运行时创建)"
        fi

        # 检查关键文件
        echo ""
        echo "关键文件检查:"
        for file in xpay_core.py xpay_cli.py xpay_server.py startup.sh; do
            if [ -f ~/.龍魂/xpay/$file ]; then
                echo "  ✅ $file"
            else
                echo "  ❌ $file (缺失)"
            fi
        done

        echo ""
        echo "💡 提示: 如果有文件缺失，请确保XPay已正确部署"
        echo ""
        read -p "按 Enter 返回菜单..."
        exec bash "$LAUNCHER_PATH"
        ;;
    0)
        echo ""
        echo "🚪 再见！龍魂与你同在。🐉"
        echo ""
        exit 0
        ;;
    *)
        echo ""
        echo "❌ 无效的选择，请输入 0-8"
        echo ""
        sleep 2
        exec bash "$LAUNCHER_PATH"
        ;;
esac

# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# DNA: #龍芯⚡️丙午·丙申·甲寅·申时·丰-CONFIRM-SEAL-longhun_launcher-9802441E
