#!/bin/bash
# 龍魂实时监控 · 文件变动自动记录
# DNA: #龍芯⚡️2026-03-18-实时监控-v1.0

BASE="$HOME/longhun-system"
LOG="$BASE/logs/变动日志.jsonl"
mkdir -p "$BASE/logs"

log_change() {
    local file="$1"
    local event="$2"
    local now=$(date -u '+%Y-%m-%dT%H:%M:%SZ')
    echo "{\"time\":\"$now\",\"event\":\"$event\",\"file\":\"$file\"}" >> "$LOG"
}

echo "🔍 实时监控启动 · 监控目录: $BASE"
echo "📝 变动日志: $LOG"
echo "按 Ctrl+C 停止"
echo ""

fswatch -r \
    --exclude ".*\\.pyc" \
    --exclude "__pycache__" \
    --exclude "\\.DS_Store" \
    --exclude "logs/" \
    --exclude "\\.git/" \
    --latency 2 \
    "$BASE/bin" \
    "$BASE/封印库" \
    "$HOME/.star-memory/vault" \
    "$HOME/.claude/projects/-Users-zuimeidedeyihan/memory" | while read -r changed_file; do
        echo "  📌 $(date '+%H:%M:%S') 变动: $(basename "$changed_file")"
        log_change "$changed_file" "modified"
        # 触发看板刷新通知
        osascript -e "display notification \"$(basename "$changed_file")\" with title \"📌 文件变动\" subtitle \"$(date '+%H:%M:%S')\"" 2>/dev/null
done
