#!/bin/bash
# ╔══════════════════════════════════════════════════════╗
# ║   龍魂·别名一次性安装                                 ║
# ║   运行一次·以后输入「起」就行                         ║
# ║   DNA: #龍芯⚡️2026-04-08-ALIAS-INSTALL-v1.0        ║
# ╚══════════════════════════════════════════════════════╝

BASE="$HOME/longhun-system"
SHELL_RC=""

# 检测用的是哪个 shell
if [ -n "$ZSH_VERSION" ] || [ "$(basename "$SHELL")" = "zsh" ]; then
    SHELL_RC="$HOME/.zshrc"
elif [ -n "$BASH_VERSION" ] || [ "$(basename "$SHELL")" = "bash" ]; then
    SHELL_RC="$HOME/.bashrc"
    [ -f "$HOME/.bash_profile" ] && SHELL_RC="$HOME/.bash_profile"
fi

ALIAS_BLOCK='
# ════ 龍魂·快捷命令 ════
alias 起="bash ~/longhun-system/起.sh"
alias longhun="bash ~/longhun-system/起.sh"
alias 检查="python3 ~/longhun-system/bin/health_check.py"
alias 记忆="tail -20 ~/longhun-system/memory.jsonl | python3 -c \"import sys,json; [print(json.loads(l).get('"'"'ts_beijing'"'"',' ')[:16], json.loads(l).get('"'"'event'"'"',' ')[:50]) for l in sys.stdin if l.strip()]\" 2>/dev/null"
alias 三才="curl -s http://127.0.0.1:8001/sancai/weights 2>/dev/null | python3 -m json.tool || echo 三才引擎未启动"
alias 宝宝="bash ~/longhun-system/起.sh"
# ════════════════════════
'

echo ""
echo "🐉 龍魂·别名安装"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ -z "$SHELL_RC" ]; then
    echo "⚠️  检测不到 .zshrc/.bashrc，手动添加以下内容到你的 shell 配置文件："
    echo "$ALIAS_BLOCK"
else
    # 检查是否已经安装过
    if grep -q "龍魂·快捷命令" "$SHELL_RC" 2>/dev/null; then
        echo "✅ 别名已经安装过了，跳过"
    else
        echo "$ALIAS_BLOCK" >> "$SHELL_RC"
        echo "✅ 已写入 $SHELL_RC"
    fi

    echo ""
    echo "现在执行这个让它立刻生效："
    echo ""
    echo "  source $SHELL_RC"
    echo ""
    echo "以后打开任何终端，输入："
    echo ""
    echo "  起       ← 一键启动所有服务"
    echo "  宝宝     ← 同上（嘿嘿）"
    echo "  检查     ← 健康检测"
    echo "  三才     ← 查看天地人实时权重"
    echo "  记忆     ← 查看最近20条记忆"
    echo ""
fi

echo "DNA: #龍芯⚡️$(date '+%Y-%m-%d')-ALIAS-INSTALL-v1.0"
echo "🟢 完成！"
