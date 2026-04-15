#!/bin/bash
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 清理垃圾 · 定期扫描清理临时文件
# DNA: #龍芯⚡️2026-03-18-清理垃圾-v1.0
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 作者: UID9622 诸葛鑫（龍芯北辰）
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 清理范围（安全，不动重要文件）：
#   macOS .DS_Store 文件
#   Python __pycache__ 目录
#   30天以上的旧日志（保留最新100行）
#   /tmp 下的龍魂临时文件
#   日志文件超过5MB时自动归档
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

BASE="$HOME/longhun-system"
LOG="$BASE/logs/清理日志.log"
NOW=$(date '+%Y-%m-%d %H:%M:%S')
本月=$(date '+%Y-%m')

通知() {
    osascript -e "display notification \"$2\" with title \"🧹 龍魂清理\" subtitle \"$1\"" 2>/dev/null
}
写日志() { echo "[$NOW] $1" >> "$LOG"; }

释放空间=0

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  🧹 清理垃圾 · $NOW"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# ── 1. 清 .DS_Store ───────────────────────
echo ""
echo "  【1】清理 .DS_Store"
数量=$(find "$BASE" -name ".DS_Store" 2>/dev/null | wc -l | tr -d ' ')
find "$BASE" -name ".DS_Store" -delete 2>/dev/null
echo "  ✅ 删除 ${数量} 个 .DS_Store"
写日志 "清理.DS_Store: ${数量}个"

# ── 2. 清 Python __pycache__ ─────────────
echo ""
echo "  【2】清理 Python 缓存"
数量=$(find "$BASE" -name "__pycache__" -type d 2>/dev/null | wc -l | tr -d ' ')
find "$BASE" -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null
find "$BASE" -name "*.pyc" -delete 2>/dev/null
echo "  ✅ 清理 ${数量} 个缓存目录"
写日志 "清理__pycache__: ${数量}个"

# ── 3. 清 /tmp 龍魂临时文件 ──────────────
echo ""
echo "  【3】清理临时文件"
数量=$(find /tmp -name "lh_*" -o -name "longhun_*" 2>/dev/null | wc -l | tr -d ' ')
find /tmp -name "lh_*" -delete 2>/dev/null
find /tmp -name "longhun_*" -delete 2>/dev/null
echo "  ✅ 清理 ${数量} 个临时文件"

# ── 4. 日志归档（超过2MB就归档）──────────
echo ""
echo "  【4】日志归档检查"
for 日志文件 in "$BASE/logs"/*.log "$BASE/logs"/*.jsonl; do
    [ -f "$日志文件" ] || continue
    大小=$(stat -f%z "$日志文件" 2>/dev/null || echo 0)
    文件名=$(basename "$日志文件")

    if [ "$大小" -gt 2097152 ]; then  # 超过2MB
        归档目录="$BASE/logs/归档/$本月"
        mkdir -p "$归档目录"
        归档名="${文件名%.log}_$(date +%Y%m%d).log"
        cp "$日志文件" "$归档目录/$归档名"
        # 只保留最新500行
        tail -500 "$日志文件" > "/tmp/lh_log_tmp"
        mv "/tmp/lh_log_tmp" "$日志文件"
        大小KB=$(( 大小 / 1024 ))
        echo "  📦 归档 $文件名 (${大小KB}KB) → 归档/$本月/"
        写日志 "归档日志: $文件名 ${大小KB}KB"
    fi
done
echo "  ✅ 日志检查完成"

# ── 5. 清 session_log 旧记录 (保留最新200条) ──
echo ""
echo "  【5】整理 session_log"
SESSION_LOG="$BASE/logs/session_log.jsonl"
if [ -f "$SESSION_LOG" ]; then
    总行数=$(wc -l < "$SESSION_LOG" | tr -d ' ')
    if [ "$总行数" -gt 200 ]; then
        tail -200 "$SESSION_LOG" > "/tmp/lh_session_tmp"
        mv "/tmp/lh_session_tmp" "$SESSION_LOG"
        echo "  ✅ session_log 精简: ${总行数}行 → 200行"
        写日志 "session_log精简: ${总行数}→200"
    else
        echo "  ✅ session_log 正常 (${总行数}行)"
    fi
fi

# ── 汇总 ────────────────────────────────
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  🧹 清理完成 · $NOW"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
通知 "清理完成" "垃圾清理完毕，系统更流畅"
写日志 "清理完成"
