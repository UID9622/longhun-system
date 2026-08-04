#!/bin/bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂系统 · 一键启动安装器
# LongHun System · One-Command Launcher Setup

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  🐉 龍魂支付系统 · 一键启动安装                            ║"
echo "║  超级简单 - 只需要记住一个单词                             ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# 检查Shell配置文件
if [[ $SHELL == *"zsh"* ]]; then
    RC_FILE="$HOME/.zshrc"
    echo "✅ 检测到: zsh (使用 ~/.zshrc)"
else
    RC_FILE="$HOME/.bashrc"
    echo "✅ 检测到: bash (使用 ~/.bashrc)"
fi

echo ""
echo "【配置1】创建龍魂启动别名"
echo "════════════════════════════════════════════════════════════"
echo ""

# 添加别名
cat >> "$RC_FILE" << 'ALIAS'

# 🐉 龍魂支付系统 · 一键启动
# 只需要输入: longhun
# 就会出现菜单，选择启动方式

alias longhun='bash ~/.龍魂/xpay/longhun_launcher.sh'
alias lh='bash ~/.龍魂/xpay/longhun_launcher.sh'
alias lh-demo='cd ~/.龍魂/xpay && python3 xpay_core.py'
alias lh-api='cd ~/.龍魂/xpay && python3 xpay_server.py'
alias lh-cli='cd ~/.龍魂/xpay && bash startup.sh'
alias lh-logs='tail -f ~/.龍魂/xpay/logs/*.log'
alias lh-stats='python3 ~/.龍魂/xpay/xpay_cli.py stats'

ALIAS

echo "✅ 别名已添加到 $RC_FILE"
echo ""
echo "你现在可以使用这些快捷命令："
echo "  longhun       → 启动主菜单"
echo "  lh            → 启动主菜单（缩写）"
echo "  lh-demo       → 演示模式"
echo "  lh-api        → API服务器"
echo "  lh-cli        → CLI交互"
echo "  lh-logs       → 查看日志"
echo "  lh-stats      → 查看统计"
echo ""

# 重新加载配置
echo "【配置2】重新加载Shell配置"
echo "════════════════════════════════════════════════════════════"
source "$RC_FILE"
echo "✅ 配置已重新加载"
echo ""

echo "【完成】"
echo "════════════════════════════════════════════════════════════"
echo "现在你可以在终端中使用以下命令:"
echo ""
echo "  🐉 longhun"
echo ""
echo "就会看到菜单，选择你要启动的功能"
echo ""
echo "试试看吧！"
echo "════════════════════════════════════════════════════════════"

# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# DNA: #龍芯⚡️丙午·丙申·甲寅·申时·困-CONFIRM-SEAL-setup_longhun_alias-3359C3D8
