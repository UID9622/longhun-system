#!/bin/bash
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 龙魂系统 · 批量补充署名头脚本
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Copyright © 2026 UID9622 诸葛鑫（龍芯北辰）
# GPG指纹：A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# DNA追溯码：#龍芯⚡️2026-03-10-BATCH-SIGN-v1.0
# 确认码：#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
# 用法: ./batch_sign_headers.sh [段号 1-5] [--dry-run]
#   段1: CNSH-整理版（核心CNSH实现）
#   段2: CNSH-v1.0-完整实现
#   段3: 根目录脚本（agent_daemon.py / brain_sync.py 等）
#   段4: 🔧 AI技术架构分析中心
#   段5: 所有未签名文件（全量扫描）
#
# --dry-run: 只列出待处理文件，不实际修改

SEGMENT="${1:-1}"
DRY_RUN="${2:-}"
BASE="$HOME/longhun-system"
TODAY=$(date '+%Y-%m-%d')
TODAY_COMPACT=$(date '+%Y%m%d')

GPG_KEY="A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
AUTHOR="UID9622 诸葛鑫（龍芯北辰）"
SIGN_LOG="$BASE/logs/batch_sign_$(date '+%Y%m%d_%H%M%S').log"
mkdir -p "$BASE/logs"

ADD=0
SKIP=0
FAIL=0

# ── 检测文件是否已有署名 ─────────────────────────────
has_signature() {
    grep -q "#龍芯⚡️\|DNA追溯\|UID9622\|GPG指纹.*A2D0" "$1" 2>/dev/null
}

# ── 生成项目名（从路径提取） ──────────────────────────
get_project_name() {
    local f="$1"
    local name
    name=$(basename "$f" | sed 's/\.[^.]*$//' | tr ' ' '-' | tr '[:upper:]' '[:lower:]')
    echo "$name"
}

# ── 在文件头部插入署名 ───────────────────────────────
prepend_signature() {
    local f="$1"
    local ext="${f##*.}"
    local proj
    proj=$(get_project_name "$f")
    local dna="#龍芯⚡️${TODAY_COMPACT}-${proj}-v1.0"

    case "$ext" in
    py)
        # 检查是否有 shebang
        local first
        first=$(head -1 "$f")
        if [[ "$first" == "#!/"* ]]; then
            # 在 shebang 后插入
            local tmp
            tmp=$(mktemp)
            head -1 "$f" > "$tmp"
            cat >> "$tmp" << PYEOF
# -*- coding: utf-8 -*-
"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
$(basename "$f")
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Copyright © 2026 ${AUTHOR}
Licensed under the Apache License, Version 2.0

作者：${AUTHOR}
创作地：中华人民共和国
GPG指纹：${GPG_KEY}
理论指导：曾仕强老师（永恒显示）
DNA追溯码：${dna}
确认码：#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

共建致谢：
  Claude (Anthropic PBC) · 技术协作与代码共创
  Notion · 知识底座与结构化存储
  没有你们，就没有龍魂系统的一切。

献礼：新中国成立77周年（1949-2026）· 丙午马年
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
PYEOF
            tail -n +2 "$f" >> "$tmp"
            mv "$tmp" "$f"
        else
            local tmp
            tmp=$(mktemp)
            cat > "$tmp" << PYEOF
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
$(basename "$f")
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Copyright © 2026 ${AUTHOR}
Licensed under the Apache License, Version 2.0

作者：${AUTHOR}
创作地：中华人民共和国
GPG指纹：${GPG_KEY}
理论指导：曾仕强老师（永恒显示）
DNA追溯码：${dna}
确认码：#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

共建致谢：
  Claude (Anthropic PBC) · 技术协作与代码共创
  Notion · 知识底座与结构化存储
  没有你们，就没有龍魂系统的一切。

献礼：新中国成立77周年（1949-2026）· 丙午马年
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

PYEOF
            cat "$f" >> "$tmp"
            mv "$tmp" "$f"
        fi
        ;;
    sh)
        local first
        first=$(head -1 "$f")
        local tmp
        tmp=$(mktemp)
        if [[ "$first" == "#!/"* ]]; then
            head -1 "$f" > "$tmp"
            cat >> "$tmp" << SHEOF
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# $(basename "$f")
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Copyright © 2026 ${AUTHOR}
# GPG指纹：${GPG_KEY}
# 理论指导：曾仕强老师（永恒显示）
# DNA追溯码：${dna}
# 确认码：#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创作地：中华人民共和国
# 共建致谢：Claude (Anthropic PBC) · Notion
# 献礼：新中国成立77周年（1949-2026）· 丙午马年
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SHEOF
            tail -n +2 "$f" >> "$tmp"
        else
            cat > "$tmp" << SHEOF
#!/bin/bash
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# $(basename "$f")
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Copyright © 2026 ${AUTHOR}
# GPG指纹：${GPG_KEY}
# 理论指导：曾仕强老师（永恒显示）
# DNA追溯码：${dna}
# 确认码：#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创作地：中华人民共和国
# 共建致谢：Claude (Anthropic PBC) · Notion
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SHEOF
            cat "$f" >> "$tmp"
        fi
        mv "$tmp" "$f"
        ;;
    md)
        local tmp
        tmp=$(mktemp)
        cat > "$tmp" << MDEOF
**DNA追溯码**: ${dna}
**GPG指纹**: ${GPG_KEY}
**确认码**: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
**创建者**: ${AUTHOR}
**理论指导**: 曾仕强老师（永恒显示）
**创作地**: 中华人民共和国
**共建致谢**: Claude (Anthropic PBC) · 技术协作与代码共创 | Notion · 知识底座与结构化存储
**献礼**: 新中国成立77周年（1949-2026）· 丙午马年

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

MDEOF
        cat "$f" >> "$tmp"
        # 文档尾部追加
        echo "" >> "$tmp"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" >> "$tmp"
        echo "**版权所有 © 2026 UID9622** · **祖国万岁！人民万岁！** 🇨🇳" >> "$tmp"
        mv "$tmp" "$f"
        ;;
    *)
        return 1
        ;;
    esac
    return 0
}

# ── 段定义 ───────────────────────────────────────────
get_files_for_segment() {
    local seg="$1"
    case "$seg" in
    1)
        echo "【段1】CNSH-整理版（核心CNSH实现）"
        find "$BASE/CNSH-整理版" -type f \( -name "*.py" -o -name "*.sh" -o -name "*.md" \) \
          ! -path "*/.git/*" 2>/dev/null
        ;;
    2)
        echo "【段2】CNSH-v1.0-完整实现"
        find "$BASE/CNSH-v1.0-完整实现" -type f \( -name "*.py" -o -name "*.sh" -o -name "*.md" \) \
          ! -path "*/.git/*" 2>/dev/null
        ;;
    3)
        echo "【段3】根目录核心脚本"
        find "$BASE" -maxdepth 1 -type f \( -name "*.py" -o -name "*.sh" \) 2>/dev/null
        find "$BASE/bin" -type f \( -name "*.py" -o -name "*.sh" \) 2>/dev/null
        ;;
    4)
        echo "【段4】🔧 AI技术架构分析中心"
        find "$BASE/🔧 AI技术架构分析中心" -type f -name "*.md" \
          ! -path "*/.git/*" 2>/dev/null
        ;;
    5)
        echo "【段5】全量扫描（未签名文件）"
        find "$BASE" -type f \( -name "*.py" -o -name "*.sh" -o -name "*.md" \) \
          ! -path "*/.git/*" \
          ! -path "*/数据归集/*" \
          ! -path "*/CNSH_备份*" \
          ! -path "*/node_modules/*" \
          ! -path "*/__pycache__/*" \
          2>/dev/null
        ;;
    esac
}

# ── 主流程 ───────────────────────────────────────────
echo "╔══════════════════════════════════════════════════╗"
echo "║  🐉 龙魂系统 · 批量补充署名头 v1.0               ║"
echo "║  DNA: #龍芯⚡️2026-03-10-BATCH-SIGN-v1.0         ║"
echo "╚══════════════════════════════════════════════════╝"
echo ""
[ -n "$DRY_RUN" ] && echo "  ⚡ DRY-RUN 模式：只显示，不修改" && echo ""

SIGN_LIST="$BASE/logs/gpg_sign_list_${TODAY_COMPACT}.txt"
> "$SIGN_LIST"

while IFS= read -r line; do
    # 跳过段描述行
    [[ "$line" == 【*】* ]] && echo "$line" && continue
    f="$line"
    [ -z "$f" ] && continue
    [ ! -f "$f" ] && continue

    ext="${f##*.}"
    [[ ! "$ext" =~ ^(py|sh|md)$ ]] && continue

    if has_signature "$f"; then
        SKIP=$((SKIP+1))
        continue
    fi

    fname=$(basename "$f")
    relpath="${f#$BASE/}"

    if [ -n "$DRY_RUN" ]; then
        echo "  📝 待签: $relpath"
        ADD=$((ADD+1))
        continue
    fi

    prepend_signature "$f"
    if [ $? -eq 0 ]; then
        echo "  ✅ 已签: $relpath"
        echo "$f" >> "$SIGN_LIST"
        ADD=$((ADD+1))
    else
        echo "  ⚠️  跳过: $relpath"
        FAIL=$((FAIL+1))
    fi
done < <(get_files_for_segment "$SEGMENT")

echo ""
echo "╔══════════════════════════════════════════════════╗"
echo "║  完成！新增=$ADD  已有=$SKIP  跳过=$FAIL           ║"
if [ -z "$DRY_RUN" ] && [ $ADD -gt 0 ]; then
echo "║  GPG签名清单: logs/gpg_sign_list_${TODAY_COMPACT}.txt  ║"
echo "║                                                  ║"
echo "║  下一步：运行 gpg_sign_all.sh 完成GPG签名         ║"
fi
echo "╚══════════════════════════════════════════════════╝"
