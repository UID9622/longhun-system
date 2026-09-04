#!/bin/bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 🐉 龍魂终端工具安装脚本
# 安装内容:
#   1. 将 ~/longhun-system/bin 加入 PATH
#   2. 注册 cd-lh 函数
#   3. 注册 longhun_welcome 欢迎板
#   4. 可选开启自动欢迎板 (LONGHUN_AUTO_BANNER=1)
#
# DNA: #龍芯⚡️丙午·甲午·己巳·庚午·䷃蒙-LONGHUN-TERMINAL-INSTALL-v2.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

set -e

LH_ROOT="${LONGHUN_ROOT:-$HOME/longhun-system}"
BIN_DIR="$LH_ROOT/bin"
SHELL_FILE=""

# 探测当前 shell
if [ -n "$ZSH_VERSION" ] || [ "$(basename "$SHELL")" = "zsh" ]; then
    SHELL_FILE="$HOME/.zshrc"
elif [ -n "$BASH_VERSION" ] || [ "$(basename "$SHELL")" = "bash" ]; then
    SHELL_FILE="$HOME/.bashrc"
else
    echo "⚠️ 无法识别 shell，默认写入 ~/.zshrc 和 ~/.bashrc"
    SHELL_FILE="$HOME/.zshrc"
fi

# 标记块
MARKER_BEGIN="# >>> 龍魂终端工具 BEGIN <<<"
MARKER_END="# <<< 龍魂终端工具 END >>>"

# 安装块内容
INSTALL_BLOCK="$MARKER_BEGIN
# 🐉 龍魂终端统一入口 (由 install-terminal.sh 安装)
export LONGHUN_ROOT=\"$LH_ROOT\"
export PATH=\"$BIN_DIR:\$PATH\"

# 进入龍魂根目录
cd-lh() {
    cd \"\$LONGHUN_ROOT\" && pwd
}

# 龍魂欢迎板
longhun_welcome() {
    local CYAN='\\033[0;36m'
    local GREEN='\\033[0;32m'
    local YELLOW='\\033[1;33m'
    local MAGENTA='\\033[0;35m'
    local BLUE='\\033[0;34m'
    local NC='\\033[0m'
    local PWD_DISP=\"\$(pwd | sed \"s|\$HOME|~|\" | cut -c1-45)\"
    local PAD=\"\$(printf '%*s' \$((46 - \${#PWD_DISP})) '')\"
    echo \"\"
    echo -e \"\${CYAN}╔═══════════════════════════════════════════════════════╗\${NC}\"
    echo -e \"\${CYAN}║\${NC}  \${GREEN}🐉 龍魂终端 v2.0 · UID9622\${NC}                        \${CYAN}║\${NC}\"
    echo -e \"\${CYAN}╠═══════════════════════════════════════════════════════╣\${NC}\"
    echo -e \"\${CYAN}║\${NC}  \${YELLOW}📅\${NC} \$(date '+%Y-%m-%d %H:%M:%S')  \${YELLOW}👤\${NC}\$(whoami)          \${CYAN}║\${NC}\"
    echo -e \"\${CYAN}║\${NC}  \${YELLOW}📍\${NC} \${PWD_DISP}\${PAD}\${CYAN}║\${NC}\"
    echo -e \"\${CYAN}╠═══════════════════════════════════════════════════════╣\${NC}\"
    echo -e \"\${CYAN}║\${NC}  \${MAGENTA}💡 快捷指令:\${NC}  lh | longhun-check | cd-lh            \${CYAN}║\${NC}\"
    echo -e \"\${CYAN}║\${NC}  \${MAGENTA}🔧 常用命令:\${NC}  状态 启动 人格 技能 cnsh 签名       \${CYAN}║\${NC}\"
    echo -e \"\${CYAN}║\${NC}            审计 每日复盘 操作台 门户 命令           \${CYAN}║\${NC}\"
    echo -e \"\${CYAN}╚═══════════════════════════════════════════════════════╝\${NC}\"
    echo \"\"
}

# 交互式 shell 自动显示欢迎板 + 体检（默认关闭，设 LONGHUN_AUTO_BANNER=1 开启）
if [[ \$- == *i* && \"\${LONGHUN_AUTO_BANNER:-0}\" == \"1\" ]]; then
    longhun_welcome
    longhun-check
fi

# 清理旧版 lh 别名/函数，确保新的 PATH 入口生效
unalias lh longhun 龍魂 2>/dev/null || true
if type unfunction >/dev/null 2>&1; then
    unfunction lh 2>/dev/null || true
else
    unset -f lh 2>/dev/null || true
fi
$MARKER_END"

# 为指定 rc 文件安装
install_to_rc() {
    local rc="$1"
    if [ ! -f "$rc" ]; then
        touch "$rc"
    fi
    # 如果已存在旧标记，先删除
    if grep -q "$MARKER_BEGIN" "$rc"; then
        echo "🔄 更新已存在的龍魂终端配置: $rc"
        awk -v begin="$MARKER_BEGIN" -v end="$MARKER_END" '
            $0 == begin {skip=1; next}
            $0 == end {skip=0; next}
            !skip {print}
        ' "$rc" > "$rc.tmp" && mv "$rc.tmp" "$rc"
    else
        echo "🆕 安装龍魂终端配置到: $rc"
    fi
    echo "" >> "$rc"
    echo "$INSTALL_BLOCK" >> "$rc"
    echo "" >> "$rc"
}

install_to_rc "$SHELL_FILE"
# 同时尝试另一个常用 rc，确保覆盖
OTHER_RC=""
if [ "$SHELL_FILE" = "$HOME/.zshrc" ]; then
    OTHER_RC="$HOME/.bashrc"
else
    OTHER_RC="$HOME/.zshrc"
fi
if [ -f "$OTHER_RC" ]; then
    install_to_rc "$OTHER_RC"
fi

echo ""
echo "✅ 龍魂终端工具安装完成"
echo "   根目录: $LH_ROOT"
echo "   bin 目录: $BIN_DIR"
echo "   生效配置: $SHELL_FILE"
echo ""
echo "💡 请运行以下命令使配置生效:"
echo "   source $SHELL_FILE"
echo ""
echo "🚀 安装后可用命令:"
echo "   lh              # 龍魂指挥台"
echo "   longhun-check   # 系统体检"
echo "   cd-lh           # 进入龍魂根目录"
echo ""
echo "🎨 开启自动欢迎板:"
echo "   echo 'export LONGHUN_AUTO_BANNER=1' >> $SHELL_FILE"
echo ""
echo "DNA: #龍芯⚡️丙午·甲午·己巳·庚午·䷃蒙-LONGHUN-TERMINAL-INSTALL-v2.0"
