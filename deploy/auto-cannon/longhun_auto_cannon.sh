#!/bin/bash
# ==============================================================================
# ⚡ 龍魂系統·全自動機槍啟動器 (Linux/macOS)
# =============================================================================
# DNA: #龍芯⚡️2026-07-11-AUTO-CANNON-v1.0
# 效果: 雙擊一下(或 ./longhun_auto_cannon.sh)，去抽根煙，回來全搞定
# ==============================================================================

# 顏色定義
金="\033[38;5;220m"
紅="\033[38;5;196m"
綠="\033[38;5;82m"
藍="\033[38;5;81m"
灰="\033[38;5;240m"
粗="\033[1m"
關="\033[0m"

echo -e "${金}${粗}"
echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║                                                                  ║"
echo "║     🐉 龍魂系統·全自動機槍 v1.0 啟動中...                        ║"
echo "║     DNA: #龍芯⚡️2026-07-11-AUTO-CANNON-v1.0                     ║"
echo "║                                                                  ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo -e "${關}"

# 檢查 Python3
if ! command -v python3 &> /dev/null; then
    echo -e "${紅}❌ 錯誤: 未找到 python3，請先安裝 Python 3.10+${關}"
    exit 1
fi

echo -e "${藍}📍 Python3: $(which python3) ($(python3 --version))${關}"
echo -e "${藍}📍 當前目錄: $(pwd)${關}"
echo ""

# 確保輸出目錄存在
mkdir -p ~/.龍魂/reports ~/.龍魂/logs

# 尋找主腳本
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MAIN_SCRIPT="${SCRIPT_DIR}/longhun_auto_cannon.py"

if [ ! -f "$MAIN_SCRIPT" ]; then
    # 嘗試當前目錄
    MAIN_SCRIPT="./longhun_auto_cannon.py"
fi

if [ ! -f "$MAIN_SCRIPT" ]; then
    echo -e "${紅}❌ 錯誤: 找不到 longhun_auto_cannon.py${關}"
    echo -e "${灰}   請確保 .sh 和 .py 在同一目錄${關}"
    exit 1
fi

echo -e "${綠}✅ 找到主腳本: ${MAIN_SCRIPT}${關}"
echo ""

# 解析參數
ARGS=""
if [ "$1" == "--scan" ]; then
    ARGS="--scan"
    echo -e "${金}🔍 模式: 僅掃描${關}"
elif [ "$1" == "--fix" ]; then
    ARGS="--fix"
    echo -e "${金}🔧 模式: 掃描+修復${關}"
elif [ "$1" == "--report" ]; then
    ARGS="--report"
    echo -e "${金}📊 模式: 僅生成報告${關}"
elif [ "$1" == "--daemon" ]; then
    ARGS="--daemon"
    echo -e "${金}🚀 模式: 全自動 + 啟動守護進程${關}"
else
    echo -e "${金}⚡ 模式: 全自動 (掃描+修復+報告)${關}"
    echo -e "${灰}   提示: 加 --daemon 參數可同時啟動守護進程${關}"
fi

echo ""
echo -e "${藍}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${關}"
echo ""

# 執行!
START_TIME=$(date +%s)
python3 "$MAIN_SCRIPT" $ARGS
EXIT_CODE=$?
END_TIME=$(date +%s)
ELAPSED=$((END_TIME - START_TIME))

echo ""
echo -e "${藍}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${關}"
echo ""

if [ $EXIT_CODE -eq 0 ]; then
    echo -e "${綠}${粗}✅ 全自動機槍執行完成! 耗時: ${ELAPSED}秒${關}"
    echo -e "${灰}   報告位置: ~/.龍魂/reports/${關}"
    echo ""
    echo -e "${金}${粗}🚬 你可以去抽根煙了，回來全搞定。${關}"
else
    echo -e "${紅}${粗}❌ 執行過程中出現錯誤 (返回碼: ${EXIT_CODE})${關}"
fi

echo ""
read -n 1 -s -r -p "按任意鍵退出..."
echo ""
