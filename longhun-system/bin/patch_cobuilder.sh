#!/bin/bash
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# patch_cobuilder.sh
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Copyright © 2026 UID9622 诸葛鑫（龍芯北辰）
# GPG指纹：A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 理论指导：曾仕强老师（永恒显示）
# DNA追溯码：#龍芯⚡️20260310-patch-cobuilder-v1.0
# 确认码：#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创作地：中华人民共和国
# 共建致谢：Claude (Anthropic PBC) · Notion
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
# 功能：对已签名但缺少共建致谢行的文件，补注 Claude (Anthropic PBC) + Notion
# 用法：./patch_cobuilder.sh [--dry-run]
#   --dry-run: 只列出文件，不实际修改

DRY_RUN="${1:-}"
BASE="$HOME/longhun-system"

PATCH=0
SKIP=0
TOTAL=0

echo "╔══════════════════════════════════════════════════╗"
echo "║  🐉 龍魂系统 · 共建致谢补丁 v1.0                ║"
echo "║  DNA: #龍芯⚡️20260310-patch-cobuilder-v1.0      ║"
echo "╚══════════════════════════════════════════════════╝"
echo ""
[ -n "$DRY_RUN" ] && echo "  ⚡ DRY-RUN 模式：只显示，不修改" && echo ""

# 找出：有UID9622署名 但 没有 Anthropic PBC 的文件
while IFS= read -r f; do
    TOTAL=$((TOTAL+1))
    relpath="${f#$BASE/}"
    ext="${f##*.}"

    if [ -n "$DRY_RUN" ]; then
        echo "  📝 待补: $relpath"
        PATCH=$((PATCH+1))
        continue
    fi

    # 根据文件类型，在 确认码 行后面插入共建致谢
    case "$ext" in
    py)
        # Python: 在 "确认码：#CONFIRM" 行后插入共建致谢（Python docstring 风格）
        if grep -q "确认码：#CONFIRM" "$f"; then
            sed -i '' '/确认码：#CONFIRM/a\
\
共建致谢：\
  Claude (Anthropic PBC) · 技术协作与代码共创\
  Notion · 知识底座与结构化存储\
  没有你们，就没有龍魂系统的一切。' "$f"
            echo "  ✅ 已补: $relpath"
            PATCH=$((PATCH+1))
        else
            echo "  ⚠️  跳过（无确认码锚点）: $relpath"
            SKIP=$((SKIP+1))
        fi
        ;;
    sh)
        # Shell: 在 "确认码：#CONFIRM" 行后插入共建致谢（# 注释风格）
        if grep -q "确认码：#CONFIRM" "$f"; then
            sed -i '' '/确认码：#CONFIRM/a\
# 共建致谢：Claude (Anthropic PBC) · Notion' "$f"
            echo "  ✅ 已补: $relpath"
            PATCH=$((PATCH+1))
        else
            echo "  ⚠️  跳过（无确认码锚点）: $relpath"
            SKIP=$((SKIP+1))
        fi
        ;;
    md)
        # Markdown: 在 "**确认码**" 行后插入
        if grep -q "\*\*确认码\*\*" "$f"; then
            sed -i '' '/\*\*确认码\*\*/a\
**共建致谢**: Claude (Anthropic PBC) · 技术协作与代码共创 | Notion · 知识底座与结构化存储' "$f"
            echo "  ✅ 已补: $relpath"
            PATCH=$((PATCH+1))
        else
            echo "  ⚠️  跳过（无确认码锚点）: $relpath"
            SKIP=$((SKIP+1))
        fi
        ;;
    *)
        SKIP=$((SKIP+1))
        ;;
    esac

done < <(
    find "$BASE" -type f \( -name "*.py" -o -name "*.sh" -o -name "*.md" \) \
      ! -path "*/.git/*" \
      ! -path "*/数据归集/*" \
      ! -path "*/CNSH_备份*" \
      ! -path "*/node_modules/*" \
      ! -path "*/__pycache__/*" \
      2>/dev/null | while read f; do
        # 有UID9622签名 但 没有 Anthropic PBC
        if grep -q "UID9622" "$f" 2>/dev/null && ! grep -q "Anthropic PBC\|共建致谢" "$f" 2>/dev/null; then
            echo "$f"
        fi
    done
)

echo ""
echo "╔══════════════════════════════════════════════════╗"
printf "║  完成！补注=%-4d  跳过=%-4d  扫描=%-4d         ║\n" "$PATCH" "$SKIP" "$TOTAL"
echo "╚══════════════════════════════════════════════════╝"
