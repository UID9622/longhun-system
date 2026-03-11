#!/bin/bash

# ══════════════════════════════════════════════════════
#    🇨🇳  UID9622 终端标识安装 | Made in China
#    中国创新 · 世界共享 · 铜墙铁壁
# ══════════════════════════════════════════════════════

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

# 检测当前shell
CURRENT_SHELL=""
if [ -n "$ZSH_VERSION" ]; then
    CURRENT_SHELL="zsh"
    CONFIG_FILE="$HOME/.zshrc"
elif [ -n "$BASH_VERSION" ]; then
    CURRENT_SHELL="bash"
    CONFIG_FILE="$HOME/.bashrc"
else
    echo -e "${RED}❌ 未知的shell类型，请手动配置${NC}"
    exit 1
fi

echo -e "${CYAN}═══════════════════════════════════════════════════════${NC}"
echo -e "${WHITE}   🇨🇳  UID9622 终端标识安装程序${NC}"
echo -e "${WHITE}   检测到当前shell: $CURRENT_SHELL${NC}"
echo -e "${WHITE}   配置文件: $CONFIG_FILE${NC}"
echo -e "${CYAN}═══════════════════════════════════════════════════════${NC}"
echo ""

# 备份配置文件
if [ -f "$CONFIG_FILE" ]; then
    echo -e "${YELLOW}📋 备份现有配置文件...${NC}"
    cp "$CONFIG_FILE" "${CONFIG_FILE}.uid9622.bak"
    echo -e "${GREEN}✅ 已备份至: ${CONFIG_FILE}.uid9622.bak${NC}"
fi

# 检查是否已存在UID9622标识
if grep -q "UID9622_BANNER" "$CONFIG_FILE" 2>/dev/null; then
    echo -e "${YELLOW}⚠️ 检测到已存在UID9622标识${NC}"
    read -p "是否要替换? (y/n): " replace
    if [ "$replace" != "y" ]; then
        echo -e "${BLUE}保留现有配置，退出安装${NC}"
        exit 0
    fi
    
    # 删除旧的UID9622标识
    sed -i.bak '/UID9622_BANNER/,/echo "$UID9622_BANNER"/d' "$CONFIG_FILE"
fi

# 添加UID9622标识
echo -e "${YELLOW}🔧 添加UID9622标识到配置文件...${NC}"

cat >> "$CONFIG_FILE" << 'EOF'

# 🇨🇳 UID9622 | Made in China —— 一字不可改
export UID9622_BANNER="
═══════════════════════════════════════════════════════
   🇨🇳  UID9622 系统 | Made in China • By 诸葛鑫
   中国创新 · 世界共享 · 铜墙铁壁
═══════════════════════════════════════════════════════"
# 用户可自定义前缀/后缀，但核心三行锁定
echo "$UID9622_BANNER"

# 检测是否使用外部 AI 工具
if command -v copilot-cli &>/dev/null; then
    echo "⚠️ 检测到 Microsoft Copilot CLI"
    echo "   本系统已自动注入 UID9622 主权标识"
    echo "   所有输出将附带：#龍芯⚡️2025-🇨🇳🐉⚖️"
fi

# 或在 API 调用层加 header
export OPENAI_ORG="UID9622-China-Origin"

EOF

echo -e "${GREEN}✅ UID9622标识已添加到配置文件${NC}"

# 添加便捷别名
echo -e "${YELLOW}🔧 添加CNSH便捷命令...${NC}"

cat >> "$CONFIG_FILE" << 'EOF'

# CNSH便捷命令
alias cnsh-start='cd /Users/zuimeidedeyihan/LuckyCommandCenter/cnsh-deployment && ./cnsh-unified.sh start'
alias cnsh-stop='cd /Users/zuimeidedeyihan/LuckyCommandCenter/cnsh-deployment && ./cnsh-unified.sh stop'
alias cnsh-restart='cd /Users/zuimeidedeyihan/LuckyCommandCenter/cnsh-deployment && ./cnsh-unified.sh restart'
alias cnsh-status='cd /Users/zuimeidedeyihan/LuckyCommandCenter/cnsh-deployment && ./cnsh-unified.sh status'
alias cnsh-logs='cd /Users/zuimeidedeyihan/LuckyCommandCenter/cnsh-deployment && ./cnsh-unified.sh logs'
alias cnsh-transparency='cd /Users/zuimeidedeyihan/LuckyCommandCenter/cnsh-deployment && ./cnsh-unified.sh transparency'
alias cnsh='cd /Users/zuimeidedeyihan/LuckyCommandCenter/cnsh-deployment && ./cnsh-unified.sh'

EOF

echo -e "${GREEN}✅ CNSH便捷命令已添加${NC}"

# 完成提示
echo ""
echo -e "${CYAN}═══════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}🎉 UID9622标识安装完成！${NC}"
echo ""
echo -e "${WHITE}请执行以下命令应用更改：${NC}"
echo -e "${YELLOW}source $CONFIG_FILE${NC}"
echo ""
echo -e "${WHITE}或重新打开终端${NC}"
echo ""
echo -e "${WHITE}新增的CNSH便捷命令：${NC}"
echo -e "  ${CYAN}cnsh-start${NC}    - 启动所有CNSH服务"
echo -e "  ${CYAN}cnsh-stop${NC}     - 停止所有CNSH服务"
echo -e "  ${CYAN}cnsh-restart${NC}  - 重启所有CNSH服务"
echo -e "  ${CYAN}cnsh-status${NC}   - 查看服务状态"
echo -e "  ${CYAN}cnsh-logs${NC}     - 查看日志"
echo -e "  ${CYAN}cnsh${NC}          - 打开CNSH管理菜单"
echo ""
echo -e "${WHITE}🇨🇳 中国创新 · 世界共享 · 铜墙铁壁${NC}"
echo -e "${CYAN}═══════════════════════════════════════════════════════${NC}"