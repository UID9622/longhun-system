#!/bin/bash
# 龍魂操作系统启动脚本 (Linux/macOS)
# DNA追溯码: #龍芯⚡️2026-02-02-启动脚本-v1.0

clear
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🐉 龍魂操作系统 v1.0 启动器"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "支持平台: Linux/macOS/Windows/鸿蒙/iOS"
echo "创建者: UID9622"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📋 请选择要启动的模块："
echo ""
echo "[1] 🎨 CNSH中文编程环境"
echo "[2] 🚨 公安联动系统"  
echo "[3] 🔐 双重认证系统"
echo "[4] 🐉 龍魂操作系统（统一控制台）"
echo "[5] 📖 查看完整文档"
echo "[0] 退出"
echo ""
read -p "请输入选项 (0-5): " choice

case $choice in
    1)
        echo ""
        echo "🎨 启动CNSH中文编程环境..."
        if command -v open &> /dev/null; then
            open cnsh-editor-v2.html
        elif command -v xdg-open &> /dev/null; then
            xdg-open cnsh-editor-v2.html
        else
            echo "请手动打开: cnsh-editor-v2.html"
        fi
        echo "✅ CNSH编辑器已在浏览器中打开！"
        ;;
    2)
        echo ""
        echo "🚨 启动公安联动系统..."
        python3 longhun_police_system.py
        ;;
    3)
        echo ""
        echo "🔐 启动双重认证系统..."
        echo ""
        echo "选择运行模式："
        echo "[1] Python后台服务"
        echo "[2] Web演示界面"
        read -p "请选择 (1-2): " auth_choice
        
        if [ "$auth_choice" = "1" ]; then
            python3 longhun_dual_auth.py
        else
            if command -v open &> /dev/null; then
                open dual-auth-demo.html
            elif command -v xdg-open &> /dev/null; then
                xdg-open dual-auth-demo.html
            else
                echo "请手动打开: dual-auth-demo.html"
            fi
            echo "✅ 双重认证演示已在浏览器中打开！"
        fi
        ;;
    4)
        echo ""
        echo "🐉 启动龍魂操作系统统一控制台..."
        echo ""
        echo "选择运行模式："
        echo "[1] Python后台服务"
        echo "[2] Web控制台界面"
        read -p "请选择 (1-2): " os_choice
        
        if [ "$os_choice" = "1" ]; then
            python3 longhun_os.py
        else
            if command -v open &> /dev/null; then
                open longhun-os-console.html
            elif command -v xdg-open &> /dev/null; then
                xdg-open longhun-os-console.html
            else
                echo "请手动打开: longhun-os-console.html"
            fi
            echo "✅ 龍魂控制台已在浏览器中打开！"
        fi
        ;;
    5)
        echo ""
        echo "📖 打开完整文档..."
        if command -v open &> /dev/null; then
            open README.md
        elif command -v xdg-open &> /dev/null; then
            xdg-open README.md
        else
            cat README.md
        fi
        ;;
    0)
        echo ""
        echo "感谢使用龍魂操作系统！"
        echo "敬礼！老兵！🫡"
        exit 0
        ;;
    *)
        echo "无效选项"
        exit 1
        ;;
esac

echo ""
read -p "按Enter键退出..."
