#!/bin/bash

# 龍魂窗口启动回忆脚本
# DNA: #龍芯⚡️20260525|WINDOW-AWAKENING|v1.0|xxxxx
# 每次打开新窗口时自动运行，快速恢复上下文

echo "═══════════════════════════════════════════════════"
echo "🐉 龍魂·窗口启动 — 记忆恢复模式"
echo "═══════════════════════════════════════════════════"
echo ""

# 获取最后一次对话时间
LAST_DIALOGUE=$(tail -3 ~/longhun-system/DIALOGUE_ENTRY.md 2>/dev/null | head -1)
echo "📍 上次对话记录:"
echo "   $LAST_DIALOGUE"
echo ""

# 显示最近3条记忆
echo "📊 最近记忆链（3条）:"
tail -3 ~/longhun-system/memory.jsonl 2>/dev/null | python3 -m json.tool 2>/dev/null | head -30
echo ""

# 显示系统状态
echo "⚡ 系统状态检查:"
if [ -f ~/longhun-system/config.json ]; then
    echo "   ✅ 配置文件: 存在"
    cat ~/longhun-system/config.json | python3 -c "import sys, json; d=json.load(sys.stdin); print('   所有者:', d.get('owner', 'unknown')); print('   系统名:', d.get('system_name', 'unknown'))"
else
    echo "   ❌ 配置文件: 缺失"
fi

echo ""
echo "💡 快速指令提示:"
echo "   龍 状态      — 查看所有子系统"
echo "   龍 回顾      — 显示完整链条"
echo "   龍 记忆      — 访问星辰记忆"
echo "   龍 同步      — 检查Notion状态"
echo ""
echo "═══════════════════════════════════════════════════"
echo ""
