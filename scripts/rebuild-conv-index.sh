#!/usr/bin/env bash
set -euo pipefail
R="$HOME/longhun-system"
C="$R/CONVERSATIONS"

{
  echo "# CONVERSATIONS INDEX   $(date '+%Y-%m-%d %H:%M:%S')"
  echo ""
  echo "倒序排列。四方开工读 LATEST.md，查历史读本表。"
  echo ""
  echo "| 时间 | 执行方 | 人格 | 三色 | 主题 |"
  echo "|---|---|---|---|---|"
  find "$C" -name "*.md" ! -name "_TEMPLATE.md" ! -name "INDEX.md" ! -name "LATEST.md" \
    -type f | sort -r | while read -r f; do
    sid=$(grep -m1 '^session_id:' "$f" 2>/dev/null | sed 's/session_id: *//' || echo "?")
    ag=$(grep -m1 '^agent:'      "$f" 2>/dev/null | sed 's/agent: *//'      || echo "?")
    pe=$(grep -m1 '^persona:'    "$f" 2>/dev/null | sed 's/persona: *//'    || echo "?")
    tc=$(grep -m1 '^tricolor:'   "$f" 2>/dev/null | sed 's/tricolor: *//'   || echo "?")
    echo "| ${sid%%-*} | $ag | $pe | $tc | $sid |"
  done
} > "$C/INDEX.md"

{
  echo "# LATEST · 最近 5 轮对话全文"
  echo ""
  echo "> 四方开工第一眼看这里。再往前请查 INDEX.md。"
  echo ""
  find "$C" -name "*.md" ! -name "_TEMPLATE.md" ! -name "INDEX.md" ! -name "LATEST.md" \
    -type f | sort -r | head -5 | while read -r f; do
    echo "---"
    echo ""
    cat "$f"
    echo ""
  done
} > "$C/LATEST.md"

echo "OK INDEX.md=$(wc -c < "$C/INDEX.md" | tr -d ' ')B LATEST.md=$(wc -c < "$C/LATEST.md" | tr -d ' ')B"
