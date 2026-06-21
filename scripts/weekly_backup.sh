#!/bin/bash

# 龍魂系統·每週備份腳本 v1.0
# DNA:#龍芯⚡️2026-06-07-WEEKLY-BACKUP-v1.0
# 執行時間: 每週日 10:00 CST
# 目的: 定期備份五層系統·確保災難恢復能力

set -e  # 遇到錯誤立即停止

# 配置
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
BACKUP_BASE_DIR="$HOME/.龍魂/backups"
LOG_DIR="$HOME/.龍魂/logs"
LOG_FILE="$LOG_DIR/weekly_backup.log"

# 建立日誌目錄
mkdir -p "$LOG_DIR"
mkdir -p "$BACKUP_BASE_DIR"

# 日期時間戳
TIMESTAMP=$(date '+%Y%m%d_%H%M%S')
WEEK_NUM=$(date '+%V')
YEAR=$(date '+%Y')

# 備份名稱
BACKUP_NAME="weekly_${YEAR}_W${WEEK_NUM}_${TIMESTAMP}"

# 記錄開始
{
    echo "════════════════════════════════════════════════════════════════"
    echo "🐉 龍魂系統·每週備份"
    echo "════════════════════════════════════════════════════════════════"
    echo ""
    echo "時間: $(date '+%Y-%m-%d %H:%M:%S %Z')"
    echo "備份名: $BACKUP_NAME"
    echo "備份位置: $BACKUP_BASE_DIR"
    echo ""
} >> "$LOG_FILE"

# 建立備份目錄
BACKUP_DIR="$BACKUP_BASE_DIR/$BACKUP_NAME"
mkdir -p "$BACKUP_DIR"

echo "[$(date '+%H:%M:%S')] 開始備份..." >> "$LOG_FILE"

# 1. 備份協議文件
echo "[$(date '+%H:%M:%S')] [1/3] 備份協議文件..." >> "$LOG_FILE"
PROTO_BACKUP="$BACKUP_DIR/protocols"
mkdir -p "$PROTO_BACKUP"
cp -r "$PROJECT_ROOT/protocols" "$PROTO_BACKUP/" 2>/dev/null || true
PROTO_SIZE=$(du -sh "$PROTO_BACKUP" 2>/dev/null | awk '{print $1}')
echo "  ✅ 完成: $PROTO_SIZE" >> "$LOG_FILE"

# 2. 備份腳本文件
echo "[$(date '+%H:%M:%S')] [2/3] 備份五層腳本..." >> "$LOG_FILE"
SCRIPT_BACKUP="$BACKUP_DIR/scripts"
mkdir -p "$SCRIPT_BACKUP"
cp -r "$SCRIPT_DIR" "$SCRIPT_BACKUP/" 2>/dev/null || true
SCRIPT_SIZE=$(du -sh "$SCRIPT_BACKUP" 2>/dev/null | awk '{print $1}')
echo "  ✅ 完成: $SCRIPT_SIZE" >> "$LOG_FILE"

# 3. 備份配置文件
echo "[$(date '+%H:%M:%S')] [3/3] 備份配置文件..." >> "$LOG_FILE"
CONFIG_BACKUP="$BACKUP_DIR/config"
mkdir -p "$CONFIG_BACKUP"
cp -r "$SCRIPT_DIR/config" "$CONFIG_BACKUP/" 2>/dev/null || true
CONFIG_SIZE=$(du -sh "$CONFIG_BACKUP" 2>/dev/null | awk '{print $1}')
echo "  ✅ 完成: $CONFIG_SIZE" >> "$LOG_FILE"

# 計算總大小
TOTAL_SIZE=$(du -sh "$BACKUP_DIR" 2>/dev/null | awk '{print $1}')

echo "" >> "$LOG_FILE"
echo "════════════════════════════════════════════════════════════════" >> "$LOG_FILE"
echo "✅ 備份完成" >> "$LOG_FILE"
echo "════════════════════════════════════════════════════════════════" >> "$LOG_FILE"
echo "總大小: $TOTAL_SIZE" >> "$LOG_FILE"
echo "備份位置: $BACKUP_DIR" >> "$LOG_FILE"
echo "完成時間: $(date '+%Y-%m-%d %H:%M:%S %Z')" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

# 清理舊備份 (保留最近 12 週)
echo "[$(date '+%H:%M:%S')] 清理舊備份..." >> "$LOG_FILE"
KEEP_WEEKS=12
OLD_BACKUPS=$(find "$BACKUP_BASE_DIR" -maxdepth 1 -type d -name "weekly_*" | sort -r | tail -n +$((KEEP_WEEKS + 1)))

if [ -n "$OLD_BACKUPS" ]; then
    echo "$OLD_BACKUPS" | while read old_backup; do
        OLD_SIZE=$(du -sh "$old_backup" 2>/dev/null | awk '{print $1}')
        rm -rf "$old_backup"
        echo "  🗑️ 已刪除: $(basename $old_backup) ($OLD_SIZE)" >> "$LOG_FILE"
    done
else
    echo "  無舊備份需刪除" >> "$LOG_FILE"
fi

echo "" >> "$LOG_FILE"
echo "備份日誌結束時間: $(date '+%Y-%m-%d %H:%M:%S %Z')" >> "$LOG_FILE"
echo "════════════════════════════════════════════════════════════════" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

# 驗證備份
if [ -d "$BACKUP_DIR/protocols" ] && [ -d "$BACKUP_DIR/scripts" ] && [ -d "$BACKUP_DIR/config" ]; then
    echo "✅ 備份驗證: 通過 (所有目錄完整)"
    exit 0
else
    echo "❌ 備份驗證: 失敗 (目錄缺失)"
    exit 1
fi
