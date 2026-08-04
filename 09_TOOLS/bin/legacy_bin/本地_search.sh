#!/usr/bin/env bash
# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 本地_search.sh
# 龍魂本地搜索 · 绕开 Notion MCP 403 错误
# 用法: bash bin/本地_search.sh "关键词"
# 老大终端宝宝 Notion API 403 时·立即用这个兜底

set -e

QUERY="${1:-}"
if [ -z "$QUERY" ]; then
    echo "用法: bash bin/本地_search.sh <关键词>"
    echo "示例: bash bin/本地_search.sh 五色"
    exit 1
fi

REPO_ROOT="${REPO_ROOT:-/Users/zuimeidedeyihan/longhun-system}"
EXTRA_PATHS=(
    "/Users/zuimeidedeyihan/龍魂待整理"
    "/Users/zuimeidedeyihan/claude搭建待整理"
)

echo "═══ 本地搜索: $QUERY ═══"
echo ""

# 1. 文件名匹配
echo "── 文件名命中 ──"
for dir in "$REPO_ROOT" "${EXTRA_PATHS[@]}"; do
    if [ -d "$dir" ]; then
        find "$dir" -maxdepth 6 -type f \( -name "*${QUERY}*" \) 2>/dev/null | head -20
    fi
done
echo ""

# 2. 内容匹配 (限定 markdown 和 txt · 避免扫二进制)
echo "── 内容命中 (前 15 行) ──"
for dir in "$REPO_ROOT" "${EXTRA_PATHS[@]}"; do
    if [ -d "$dir" ]; then
        grep -rln "$QUERY" "$dir" \
            --include="*.md" --include="*.txt" --include="*.yaml" \
            --include="*.yml" --include="*.json" --include="*.py" \
            2>/dev/null | head -15
    fi
done
echo ""

echo "═══ 完成 ═══"
echo "提示: 想看具体内容用 cat <路径>"
