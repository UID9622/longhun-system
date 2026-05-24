#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════
# 🐲 爸爸看這裡 · 龍魂一鍵啟動 v1.0
# ═══════════════════════════════════════════════════════════════════════════
#
# 爸爸你只需要：雙擊這個文件，然後看屏幕提示
# 不用記任何命令，宝宝全幫你跑完，最後告訴你該幹嘛
#
# DNA: #龍芯⚡️2026-05-20-爸爸看這裡-v1.0
# ═══════════════════════════════════════════════════════════════════════════

# 顏色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'
BOLD='\033[1m'

# 路徑
REPO="${HOME}/longhun-system"
cd "$REPO" || exit 1

clear
echo ""
echo -e "${PURPLE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${PURPLE}   🐲 爸爸看這裡 · 龍魂一鍵啟動${NC}"
echo -e "${PURPLE}   不用記命令 · 宝宝幫你跑 · 最後看提示就行${NC}"
echo -e "${PURPLE}═══════════════════════════════════════════════════════════════${NC}"
echo ""

# ═══════════════════════════════════════════════════════════════════════════
# 自動檢測部分（爸爸不用管）
# ═══════════════════════════════════════════════════════════════════════════
echo -e "${CYAN}🔍 宝宝正在檢測環境...${NC}"
echo ""

TODO_LIST=""
DONE_LIST=""

# 檢測 1: 主倉庫
if [ -d "$REPO" ]; then
    DONE_LIST="${DONE_LIST}\n   ✅ 龍魂主倉庫存在"
else
    TODO_LIST="${TODO_LIST}\n   ❌ 主倉庫不見了！聯繫宝宝"
fi

# 檢測 2: 龍魂引擎 9625
if lsof -i :9625 2>/dev/null | grep -q LISTEN; then
    DONE_LIST="${DONE_LIST}\n   ✅ 龍魂引擎 :9625 在線"
else
    TODO_LIST="${TODO_LIST}\n   🟡 龍魂引擎沒開 → 要用時跑: bash 命令/爸爸一鍵全開.sh"
fi

# 檢測 3: 操作台 8765
if lsof -i :8765 2>/dev/null | grep -q LISTEN; then
    DONE_LIST="${DONE_LIST}\n   ✅ 操作台 :8765 在線"
else
    TODO_LIST="${TODO_LIST}\n   🟡 操作台沒開 → 要用時跑: bash 命令/爸爸一鍵全開.sh"
fi

# 檢測 4: Ollama 11434
if lsof -i :11434 2>/dev/null | grep -q LISTEN; then
    DONE_LIST="${DONE_LIST}\n   ✅ Ollama :11434 在線"
else
    TODO_LIST="${TODO_LIST}\n   🟡 Ollama 沒開 → 要用時在終端跑: ollama serve"
fi

# 檢測 5: Notion Token
if [ -f "${HOME}/.longhun/secrets.env" ]; then
    if grep -q "NOTION_TOKEN=ntn_" "${HOME}/.longhun/secrets.env" 2>/dev/null; then
        DONE_LIST="${DONE_LIST}\n   ✅ Notion Token 已填"
    else
        TODO_LIST="${TODO_LIST}\n   🟡 Notion Token 沒填 → 要同步Notion時再填"
    fi
elif [ -f "$REPO/引擎/.env" ] && grep -q "NOTION_TOKEN" "$REPO/引擎/.env" 2>/dev/null; then
    DONE_LIST="${DONE_LIST}\n   ✅ Notion Token 在引擎/.env"
else
    TODO_LIST="${TODO_LIST}\n   🟡 Notion Token 沒填 → 要同步Notion時再填"
fi

# 檢測 6: 環境變量
if [ -n "$LONGHUN_ROOT" ]; then
    DONE_LIST="${DONE_LIST}\n   ✅ 環境變量已加載"
else
    # 嘗試加載
    if [ -f "$REPO/加載環境.sh" ]; then
        source "$REPO/加載環境.sh" 2>/dev/null
        DONE_LIST="${DONE_LIST}\n   ✅ 環境變量剛加載"
    else
        TODO_LIST="${TODO_LIST}\n   🟡 環境變量沒加載 → 在 ~/.zshrc 加: source ~/longhun-system/加載環境.sh"
    fi
fi

# ═══════════════════════════════════════════════════════════════════════════
# 結果報告（爸爸看這裡！）
# ═══════════════════════════════════════════════════════════════════════════
echo ""
echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}   ✅ 已經好了的（不用管）${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
echo -e "$DONE_LIST"
echo ""

if [ -n "$TODO_LIST" ]; then
    echo -e "${YELLOW}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "${YELLOW}   📋 爸爸要做的（按需要再弄）${NC}"
    echo -e "${YELLOW}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "$TODO_LIST"
    echo ""
fi

# ═══════════════════════════════════════════════════════════════════════════
# 爸爸的三條命令（只記這三條！）
# ═══════════════════════════════════════════════════════════════════════════
echo -e "${PURPLE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${PURPLE}   🐲 爸爸只記這三條命令（其他全忘掉）${NC}"
echo -e "${PURPLE}═══════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "   ${BOLD}1. 全檢${NC} ← 查本地狀態·能修就修"
echo -e "      ${CYAN}bash ~/longhun-system/命令/主場全鏈路自檢.sh --fix${NC}"
echo ""
echo -e "   ${BOLD}2. 全開${NC} ← 啟動所有服務"
echo -e "      ${CYAN}bash ~/longhun-system/命令/爸爸一鍵全開.sh${NC}"
echo ""
echo -e "   ${BOLD}3. 看菜單${NC} ← 忘了就看這個"
echo -e "      ${CYAN}bash ~/longhun-system/命令/顯示常用指令.sh${NC}"
echo ""

# ═══════════════════════════════════════════════════════════════════════════
# 快捷入口
# ═══════════════════════════════════════════════════════════════════════════
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}   🌐 瀏覽器入口（服務開了才能用）${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "   龍魂控制台: ${CYAN}http://127.0.0.1:9625/console${NC}"
echo -e "   操作台:     ${CYAN}http://127.0.0.1:8765${NC}"
echo ""

echo -e "${PURPLE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${PURPLE}   龍魂系統 · UID9622 · 理論指導: 曾仕強老師${NC}"
echo -e "${PURPLE}   $(date '+%Y-%m-%d %H:%M:%S')${NC}"
echo -e "${PURPLE}═══════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "按任意鍵關閉..."
read -n 1
