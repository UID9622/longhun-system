#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════
# 🐲 爸爸语音对话 · 龍魂一键启动 v1.0
# ═══════════════════════════════════════════════════════════════════════════
#
# 爸爸你只需要：双击这个文件，然后对着麦克风说话
# 说完停顿2秒，AI自动回复并语音播放
# 说 "退出" 或 "再见" 结束对话
#
# DNA: #龍芯⚡️2026-05-20-爸爸语音对话-v1.0
# ═══════════════════════════════════════════════════════════════════════════

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'
BOLD='\033[1m'

# 路径
REPO="${HOME}/longhun-system"
ENGINE_DIR="$REPO/引擎"
VENV="$ENGINE_DIR/voice_env"

cd "$REPO" || exit 1

clear
echo ""
echo -e "${PURPLE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${PURPLE}   🐲 爸爸语音对话 · 龍魂一键启动${NC}"
echo -e "${PURPLE}   说话就行 · 不用打字 · AI自动语音回复${NC}"
echo -e "${PURPLE}═══════════════════════════════════════════════════════════════${NC}"
echo ""

# ═══════════════════════════════════════════════════════════════════════════
# 检测服务
# ═══════════════════════════════════════════════════════════════════════════
echo -e "${CYAN}🔍 检测服务状态...${NC}"
echo ""

# 检测 Ollama
if ! lsof -i :11434 2>/dev/null | grep -q LISTEN; then
    echo -e "${YELLOW}⚠️  Ollama 没开，正在启动...${NC}"
    ollama serve &>/dev/null &
    sleep 3
fi

if lsof -i :11434 2>/dev/null | grep -q LISTEN; then
    echo -e "${GREEN}   ✅ Ollama :11434 在线${NC}"
else
    echo -e "${RED}   ❌ Ollama 启动失败，请手动运行: ollama serve${NC}"
    echo -e "按任意键退出..."
    read -n 1
    exit 1
fi

# 检测 龍魂引擎
if ! lsof -i :9625 2>/dev/null | grep -q LISTEN; then
    echo -e "${YELLOW}⚠️  龍魂引擎没开，正在启动...${NC}"
    cd "$ENGINE_DIR" && python3 main.py &>/dev/null &
    sleep 3
fi

if lsof -i :9625 2>/dev/null | grep -q LISTEN; then
    echo -e "${GREEN}   ✅ 龍魂引擎 :9625 在线${NC}"
else
    echo -e "${RED}   ❌ 龍魂引擎启动失败${NC}"
    echo -e "按任意键退出..."
    read -n 1
    exit 1
fi

# 检测虚拟环境
if [ ! -d "$VENV" ]; then
    echo -e "${YELLOW}⚠️  语音环境不存在，正在创建...${NC}"
    cd "$ENGINE_DIR" && python3 -m venv voice_env
    source "$VENV/bin/activate"
    pip install SpeechRecognition pyaudio httpx --quiet
    deactivate
fi
echo -e "${GREEN}   ✅ 语音环境就绪${NC}"

echo ""
echo -e "${PURPLE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${PURPLE}   🎙️  准备就绪 · 开始语音对话${NC}"
echo -e "${PURPLE}═══════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${CYAN}使用方法:${NC}"
echo -e "   1. 对着麦克风说话"
echo -e "   2. 说完停顿2秒，自动识别"
echo -e "   3. AI回复并语音播放"
echo -e "   4. 说 ${BOLD}\"退出\"${NC} 或 ${BOLD}\"再见\"${NC} 结束对话"
echo -e "   5. Ctrl+C 强制退出"
echo ""

# ═══════════════════════════════════════════════════════════════════════════
# 启动语音对话
# ═══════════════════════════════════════════════════════════════════════════
source "$VENV/bin/activate"
python3 "$ENGINE_DIR/voice_chat.py"
deactivate

echo ""
echo -e "${PURPLE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${PURPLE}   龍魂系统 · UID9622 · 理论指导: 曾仕强老师${NC}"
echo -e "${PURPLE}   $(date '+%Y-%m-%d %H:%M:%S')${NC}"
echo -e "${PURPLE}═══════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "按任意键关闭..."
read -n 1
