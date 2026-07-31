#!/bin/bash

# 龍魂系统·每周备份脚本 v1.0
# DNA:#龍芯⚡️2026-06-07-WEEKLY-BACKUP-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 执行时间: 每周日 10:00 CST
# 目的: 定期备份五层系统·确保灾难恢复能力

set -e  # 遇到错误立即停止

# 配置
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
BACKUP_BASE_DIR="$HOME/.龍魂/backups"
LOG_DIR="$HOME/.龍魂/logs"
LOG_FILE="$LOG_DIR/weekly_backup.log"

# 建立日志目录
mkdir -p "$LOG_DIR"
mkdir -p "$BACKUP_BASE_DIR"

# 日期时间戳
TIMESTAMP=$(date '+%Y%m%d_%H%M%S')
WEEK_NUM=$(date '+%V')
YEAR=$(date '+%Y')

# 备份名称
BACKUP_NAME="weekly_${YEAR}_W${WEEK_NUM}_${TIMESTAMP}"

# 记录开始
{
    echo "════════════════════════════════════════════════════════════════"
    echo "🐉 龍魂系统·每周备份"
    echo "════════════════════════════════════════════════════════════════"
    echo ""
    echo "时间: $(date '+%Y-%m-%d %H:%M:%S %Z')"
    echo "备份名: $BACKUP_NAME"
    echo "备份位置: $BACKUP_BASE_DIR"
    echo ""
} >> "$LOG_FILE"

# 建立备份目录
BACKUP_DIR="$BACKUP_BASE_DIR/$BACKUP_NAME"
mkdir -p "$BACKUP_DIR"

echo "[$(date '+%H:%M:%S')] 开始备份..." >> "$LOG_FILE"

# 1. 备份协议文件
echo "[$(date '+%H:%M:%S')] [1/3] 备份协议文件..." >> "$LOG_FILE"
PROTO_BACKUP="$BACKUP_DIR/protocols"
mkdir -p "$PROTO_BACKUP"
cp -r "$PROJECT_ROOT/protocols" "$PROTO_BACKUP/" 2>/dev/null || true
PROTO_SIZE=$(du -sh "$PROTO_BACKUP" 2>/dev/null | awk '{print $1}')
echo "  ✅ 完成: $PROTO_SIZE" >> "$LOG_FILE"

# 2. 备份脚本文件
echo "[$(date '+%H:%M:%S')] [2/3] 备份五层脚本..." >> "$LOG_FILE"
SCRIPT_BACKUP="$BACKUP_DIR/scripts"
mkdir -p "$SCRIPT_BACKUP"
cp -r "$SCRIPT_DIR" "$SCRIPT_BACKUP/" 2>/dev/null || true
SCRIPT_SIZE=$(du -sh "$SCRIPT_BACKUP" 2>/dev/null | awk '{print $1}')
echo "  ✅ 完成: $SCRIPT_SIZE" >> "$LOG_FILE"

# 3. 备份配置文件
echo "[$(date '+%H:%M:%S')] [3/3] 备份配置文件..." >> "$LOG_FILE"
CONFIG_BACKUP="$BACKUP_DIR/config"
mkdir -p "$CONFIG_BACKUP"
cp -r "$SCRIPT_DIR/config" "$CONFIG_BACKUP/" 2>/dev/null || true
CONFIG_SIZE=$(du -sh "$CONFIG_BACKUP" 2>/dev/null | awk '{print $1}')
echo "  ✅ 完成: $CONFIG_SIZE" >> "$LOG_FILE"

# 计算总大小
TOTAL_SIZE=$(du -sh "$BACKUP_DIR" 2>/dev/null | awk '{print $1}')

echo "" >> "$LOG_FILE"
echo "════════════════════════════════════════════════════════════════" >> "$LOG_FILE"
echo "✅ 备份完成" >> "$LOG_FILE"
echo "════════════════════════════════════════════════════════════════" >> "$LOG_FILE"
echo "总大小: $TOTAL_SIZE" >> "$LOG_FILE"
echo "备份位置: $BACKUP_DIR" >> "$LOG_FILE"
echo "完成时间: $(date '+%Y-%m-%d %H:%M:%S %Z')" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

# 清理旧备份 (保留最近 12 周)
echo "[$(date '+%H:%M:%S')] 清理旧备份..." >> "$LOG_FILE"
KEEP_WEEKS=12
OLD_BACKUPS=$(find "$BACKUP_BASE_DIR" -maxdepth 1 -type d -name "weekly_*" | sort -r | tail -n +$((KEEP_WEEKS + 1)))

if [ -n "$OLD_BACKUPS" ]; then
    echo "$OLD_BACKUPS" | while read old_backup; do
        OLD_SIZE=$(du -sh "$old_backup" 2>/dev/null | awk '{print $1}')
        rm -rf "$old_backup"
        echo "  🗑️ 已删除: $(basename $old_backup) ($OLD_SIZE)" >> "$LOG_FILE"
    done
else
    echo "  无旧备份需删除" >> "$LOG_FILE"
fi

echo "" >> "$LOG_FILE"
echo "备份日志结束时间: $(date '+%Y-%m-%d %H:%M:%S %Z')" >> "$LOG_FILE"
echo "════════════════════════════════════════════════════════════════" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

# 验证备份
if [ -d "$BACKUP_DIR/protocols" ] && [ -d "$BACKUP_DIR/scripts" ] && [ -d "$BACKUP_DIR/config" ]; then
    echo "✅ 备份验证: 通过 (所有目录完整)"
    exit 0
else
    echo "❌ 备份验证: 失败 (目录缺失)"
    exit 1
fi
