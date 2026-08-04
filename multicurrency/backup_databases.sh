#!/bin/bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL

# 龍魂多币种·备份脚本
# DNA:#龍芯⚡️2026-06-07-BACKUP-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

BACKUP_DIR="$HOME/.龍魂/backups"
TIMESTAMP=$(date '+%Y%m%d_%H%M%S')
LOG_FILE="$HOME/.龍魂/backup.log"

mkdir -p "$BACKUP_DIR"

echo "[$(date)] 🔄 开始备份..." | tee -a "$LOG_FILE"

# 备份 Notion 同步数据库
if [ -f "$HOME/.龍魂/notion_sync.db" ]; then
    cp "$HOME/.龍魂/notion_sync.db" "$BACKUP_DIR/notion_sync.db.$TIMESTAMP.bak"
    echo "[$(date)] ✅ Notion 数据库备份完成" | tee -a "$LOG_FILE"
fi

# 备份多币种数据库
if [ -f "$HOME/.龍魂/multicurrency.db" ]; then
    cp "$HOME/.龍魂/multicurrency.db" "$BACKUP_DIR/multicurrency.db.$TIMESTAMP.bak"
    echo "[$(date)] ✅ 多币种数据库备份完成" | tee -a "$LOG_FILE"
fi

# 清理 7 天以前的备份
find "$BACKUP_DIR" -name "*.bak" -mtime +7 -delete
echo "[$(date)] 🧹 旧备份已清理" | tee -a "$LOG_FILE"

# 显示备份统计
BACKUP_COUNT=$(ls "$BACKUP_DIR"/*.bak 2>/dev/null | wc -l)
BACKUP_SIZE=$(du -sh "$BACKUP_DIR" 2>/dev/null | awk '{print $1}')
echo "[$(date)] 📊 备份统计: $BACKUP_COUNT 个文件, 总大小 $BACKUP_SIZE" | tee -a "$LOG_FILE"

echo "[$(date)] ✅ 备份完成" | tee -a "$LOG_FILE"
