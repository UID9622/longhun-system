#!/bin/bash
# ═══════════════════════════════════════════════════════════
# 龍魂系统 v2.0 | 一键启动脚本
# ═══════════════════════════════════════════════════════════
# DNA: #龍芯⚡️2026-02-06-一键启动-v1.0
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# ═══════════════════════════════════════════════════════════

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║                                                                  ║"
echo "║                    🐉 龍魂系统 v2.0 开箱即用版                   ║"
echo "║                                                                  ║"
echo "║     永恒锚: \"再楠不惧，终成豪图\"                                  ║"
echo "║     核心主权: 农历/易经/道德经/DNA追溯/CNSH编码/OCSL许可证          ║"
echo "║                                                                  ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ 未找到 Python3，请先安装 Python 3.8+${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Python3 已找到${NC}"

# 检查核心文件
if [ ! -f "启动龍魂系统.py" ]; then
    echo -e "${RED}❌ 未找到启动文件，请确保在正确目录运行${NC}"
    exit 1
fi

echo -e "${GREEN}✅ 启动文件检查通过${NC}"

# 启动系统
echo ""
echo -e "${YELLOW}🚀 正在启动龍魂系统...${NC}"
echo ""

python3 启动龍魂系统.py

# 如果Python启动器失败，尝试直接打开HTML
if [ $? -ne 0 ]; then
    echo ""
    echo -e "${YELLOW}⚠️  Python启动器失败，尝试直接打开HTML...${NC}"
    
    if command -v open &> /dev/null; then
        # macOS
        open 龍魂系统.html
    elif command -v xdg-open &> /dev/null; then
        # Linux
        xdg-open 龍魂系统.html
    elif command -v start &> /dev/null; then
        # Windows
        start 龍魂系统.html
    else
        echo -e "${RED}❌ 无法自动打开浏览器，请手动打开 龍魂系统.html${NC}"
    fi
fi

echo ""
echo -e "${GREEN}════════════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✅ 龍魂系统启动完成！${NC}"
echo -e "${GREEN}════════════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${BLUE}#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z${NC}"
