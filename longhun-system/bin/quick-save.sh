#!/bin/bash
# 🚀 龍魂快速保存 - 永不丢失
# DNA: #龍芯⚡️2026-04-06-QUICK-SAVE-v1.0
# 用法: ./quick-save.sh "你的记录内容"

set -e

BACKUP_DIR="$HOME/longhun-system/backups"
TODAY=$(date +%Y-%m-%d)
BACKUP_FILE="$BACKUP_DIR/backup-$TODAY.jsonl"

# 确保目录存在
mkdir -p "$BACKUP_DIR"

# 获取内容
CONTENT="${1:-$(cat)}"

if [ -z "$CONTENT" ]; then
    echo "❌ 错误: 没有提供内容"
    echo "用法: ./quick-save.sh \"你的记录\""
    echo "或者: echo \"你的记录\" | ./quick-save.sh"
    exit 1
fi

# 保存记录
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
ESCAPED_CONTENT=$(echo "$CONTENT" | sed 's/"/\\"/g' | tr '\n' ' ')

echo "{\"timestamp\":\"$TIMESTAMP\",\"tag\":\"MANUAL\",\"content\":\"$ESCAPED_CONTENT\"}" >> "$BACKUP_FILE"

echo "✅ 已保存: $BACKUP_FILE"
echo "📝 内容: $CONTENT"
echo "⏰ 时间: $TIMESTAMP"

# 显示今天的所有记录
echo ""
echo "📋 今日所有记录:"
cat "$BACKUP_FILE" | jq -r '.timestamp + " | " + .content' 2>/dev/null || cat "$BACKUP_FILE"
