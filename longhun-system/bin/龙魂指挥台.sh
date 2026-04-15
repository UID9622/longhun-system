#!/bin/bash
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 龍魂指挥台 · 一键启动盾
# DNA: #龍芯⚡️2026-03-18-指挥台-v1.0
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 作者: UID9622 诸葛鑫（龍芯北辰）
# 理论指导: 曾仕强老师（永恒显示）
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 快捷键绑定方法：
#   Automator → 快速操作 → Shell脚本 → 绑定快捷键
#   或 macOS 快捷指令 App → 新建 → 运行Shell脚本
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

BIN="$HOME/longhun-system/bin"
LOG="$HOME/longhun-system/logs/指挥台.log"
NOW=$(date '+%Y-%m-%d %H:%M:%S')

通知() {
    osascript -e "display notification \"$2\" with title \"🐉 龍魂指挥台\" subtitle \"$1\" sound name \"Glass\"" 2>/dev/null
}

写日志() {
    echo "[$NOW] $1" >> "$LOG"
}

打印标题() {
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  🐉 龍魂指挥台 · $1"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
}

检查服务状态() {
    local port=$1
    local name=$2
    if lsof -i :$port > /dev/null 2>&1; then
        echo "  ✅ $name · 端口$port · 在线"
        return 0
    else
        echo "  🔴 $name · 端口$port · 离线"
        return 1
    fi
}

# ── 菜单 ──────────────────────────────────
打印标题 "一键启动盾 v1.0"
echo "  DNA: #龍芯⚡️2026-03-18-指挥台-v1.0"
echo "  时间: $NOW"
echo ""
echo "  【当前状态】"
检查服务状态 8765 "龍魂本地服务"
检查服务状态 11434 "Ollama模型服务"
echo ""
echo "  【选择操作】"
echo "  1  一键启动所有服务"
echo "  2  一键同步（Notion ↔ 本地 + Git）"
echo "  3  整理新文件（桌面/下载 → 对应文件夹）"
echo "  4  清理垃圾（临时文件+旧日志）"
echo "  5  查看资产总索引"
echo "  6  全套运行（1+2+3+4）"
echo "  0  退出"
echo ""
echo -n "  输入编号: "
read -r choice

case "$choice" in
    1)
        bash "$BIN/启动所有服务.sh"
        ;;
    2)
        bash "$BIN/一键同步.sh"
        ;;
    3)
        bash "$BIN/新文件整理.sh"
        ;;
    4)
        bash "$BIN/清理垃圾.sh"
        ;;
    5)
        python3 "$HOME/longhun-system/资源管家.py"
        ;;
    6)
        bash "$BIN/启动所有服务.sh"
        bash "$BIN/一键同步.sh"
        bash "$BIN/新文件整理.sh"
        bash "$BIN/清理垃圾.sh"
        通知 "全套完成" "服务启动·同步·整理·清垃圾全部完成"
        ;;
    0)
        echo "  再见！"
        exit 0
        ;;
    *)
        echo "  无效输入"
        ;;
esac

写日志 "指挥台操作: 选择=$choice"
