#!/bin/bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
# 龍魂爬虫伦理检查器 v1.0
# DNA: #龍芯⚡️丙午·乙未·甲辰-爬虫伦理-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# 协议: CC BY-NC-SA 4.0
#
# 功能：任何爬虫任务启动前，必须先过伦理检查。
# 核心理念：人永远是1 — 人不可以被当成数据点。
#
# 用法:
#   bash bin/lh_crawler_ethics.sh <爬虫脚本路径>
#   bash bin/lh_crawler_ethics.sh --check-dir <目录>

set -euo pipefail

RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

DNA="#龍芯⚡️丙午·乙未·甲辰-爬虫伦理-v1.0"
EXIT_CODE=0

echo ""
echo -e "${CYAN}🐉 龍魂爬虫伦理检查${NC}"
echo -e "${CYAN}${DNA}${NC}"
echo ""

# ──── 参数解析 ────
TARGET=""
CHECK_DIR=""

if [[ $# -eq 0 ]]; then
    echo "用法: $0 <爬虫脚本路径> | --check-dir <目录>"
    exit 1
fi

if [[ "$1" == "--check-dir" ]]; then
    CHECK_DIR="$2"
else
    TARGET="$1"
fi

# ──── 收集要检查的文件 ────
FILES=()
if [[ -n "$CHECK_DIR" ]]; then
    if [[ ! -d "$CHECK_DIR" ]]; then
        echo -e "${RED}❌ 目录不存在: $CHECK_DIR${NC}"
        exit 1
    fi
    echo "📂 检查目录: $CHECK_DIR"
    mapfile -t FILES < <(find "$CHECK_DIR" -type f \( -name "*.py" -o -name "*.sh" -o -name "*.cnsh" -o -name "*.json" \) 2>/dev/null || true)
else
    if [[ ! -f "$TARGET" ]]; then
        echo -e "${RED}❌ 文件不存在: $TARGET${NC}"
        exit 1
    fi
    FILES=("$TARGET")
fi

if [[ ${#FILES[@]} -eq 0 ]]; then
    echo -e "${YELLOW}🟡 未找到可检查的文件${NC}"
    exit 0
fi

echo "📋 检查 ${#FILES[@]} 个文件"
echo ""

# ──── 检查函数 ────
TOTAL_PASS=0
TOTAL_WARN=0
TOTAL_FAIL=0

check_file() {
    local file="$1"
    local content
    content=$(cat "$file" 2>/dev/null || echo "")

    if [[ -z "$content" ]]; then
        return
    fi

    local file_pass=0
    local file_warn=0
    local file_fail=0

    # ── 检查1: 是否在爬取"用户"数据（硬性禁止）──
    # 检测爬取用户/个人信息的模式
    if echo "$content" | grep -iE "(scrape|crawl|extract).+(user|用户|个人信息|IP地址|个人资料|手机号|身份证)" > /dev/null 2>&1; then
        echo -e "${RED}❌ [$file] 禁止爬取用户/个人信息${NC}"
        file_fail=$((file_fail + 1))
    fi

    # ── 检查2: 是否在爬取"数据点"（警告）──
    if echo "$content" | grep -iE "(data point|样本|标注|标签|training data|训练数据)" > /dev/null 2>&1; then
        echo -e "${YELLOW}🟡 [$file] 检测到数据点/训练数据模式，确认不是在把人当数据点${NC}"
        file_warn=$((file_warn + 1))
    fi

    # ── 检查3: 是否声明了数据来源（必须）──
    if ! echo "$content" | grep -iE "(来源|source|origin|公开|来源:)" > /dev/null 2>&1; then
        echo -e "${RED}❌ [$file] 必须声明数据来源${NC}"
        file_fail=$((file_fail + 1))
    fi

    # ── 检查4: 是否包含"本源声明"（建议）──
    if ! echo "$content" | grep -iE "(人永远是1|本源|GIGO|底座铁律|数据主权)" > /dev/null 2>&1; then
        echo -e "${YELLOW}🟡 [$file] 建议补充本源声明（人永远是1/底座铁律）${NC}"
        file_warn=$((file_warn + 1))
    fi

    # ── 检查5: 是否在做"去水印/洗来源"（硬性禁止）──
    if echo "$content" | grep -iE "(去水印|洗来源|移除.*水印|remov.*watermark|strip.*source)" > /dev/null 2>&1; then
        echo -e "${RED}❌ [$file] 禁止去水印/洗来源操作（违反战后整顿协议）${NC}"
        file_fail=$((file_fail + 1))
    fi

    # ── 检查6: 是否涉及"偷偷/不留记录/绕审计"（硬性禁止）──
    if echo "$content" | grep -iE "(不留记录|绕过.*审|绕过.*查|no.*trace|隐藏.*请求|伪装.*爬虫为正常)" > /dev/null 2>&1; then
        echo -e "${RED}❌ [$file] 禁止绕过审计的爬虫操作${NC}"
        file_fail=$((file_fail + 1))
    fi

    TOTAL_PASS=$((TOTAL_PASS + file_pass))
    TOTAL_WARN=$((TOTAL_WARN + file_warn))
    TOTAL_FAIL=$((TOTAL_FAIL + file_fail))
}

# ──── 执行检查 ────
for f in "${FILES[@]}"; do
    check_file "$f"
done

# ──── 汇总 ────
echo ""
echo "═══════════════════════════════════════"
echo -e "🐉 伦理检查汇总"
echo "═══════════════════════════════════════"
echo -e "文件数: ${#FILES[@]}"
echo -e "硬性拒绝: ${RED}${TOTAL_FAIL}${NC}"
echo -e "警告: ${YELLOW}${TOTAL_WARN}${NC}"

if [[ $TOTAL_FAIL -gt 0 ]]; then
    echo ""
    echo -e "${RED}❌ 爬虫伦理检查未通过（${TOTAL_FAIL} 项硬性禁止）${NC}"
    echo -e "${RED}   人永远是1。绕过此检查 = 挑战底座铁律。${NC}"
    EXIT_CODE=1
elif [[ $TOTAL_WARN -gt 0 ]]; then
    echo ""
    echo -e "${YELLOW}🟡 爬虫伦理检查通过（${TOTAL_WARN} 项警告·建议复核）${NC}"
    echo -e "${GREEN}   检查项全部通过，可以继续。${NC}"
else
    echo ""
    echo -e "${GREEN}✅ 爬虫伦理检查通过 · 全部符合底座铁律${NC}"
fi

echo ""
exit $EXIT_CODE
