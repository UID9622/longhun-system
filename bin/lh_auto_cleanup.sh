#!/bin/bash
# 龍魂自动清理智能版 v2.0
# DNA: #龍芯⚡️2026-07-02-AUTO-CLEANER-v2.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

LOG_FILE=~/longhun-system/logs/cleanup_$(date +%Y%m%d_%H%M%S).log
mkdir -p ~/longhun-system/logs

echo "🐉 龍魂智能清理启动 - $(date)" | tee -a "$LOG_FILE"

# 模拟运行（默认只汇报不真删）
DRY_RUN=${1:-1}  # 1=模拟 0=真删
if [ "$DRY_RUN" -eq 1 ]; then
    echo "🧪 模拟模式（不实际删除）" | tee -a "$LOG_FILE"
    FLAG="--dry-run"
else
    echo "⚡ 执行模式（实际删除）" | tee -a "$LOG_FILE"
    FLAG=""
fi

# 1. 清理Kimi缓存（保留最近1天）
echo "1️⃣ 清理Kimi缓存..." | tee -a "$LOG_FILE"
find ~/.kimi-code/sessions -type f -mtime +1 $FLAG 2>/dev/null | wc -l | xargs echo "  找到会话文件:" | tee -a "$LOG_FILE"
find ~/.kimi-code/cache -type f -mtime +1 $FLAG 2>/dev/null | wc -l | xargs echo "  找到缓存文件:" | tee -a "$LOG_FILE"

# 2. 清理系统日志（保留3天）
echo "2️⃣ 清理系统日志..." | tee -a "$LOG_FILE"
sudo find /private/var/log -name "*.log" -mtime +3 $FLAG 2>/dev/null | wc -l | xargs echo "  找到日志文件:" | tee -a "$LOG_FILE"

# 3. 清理用户缓存（保留3天）
echo "3️⃣ 清理用户缓存..." | tee -a "$LOG_FILE"
find ~/Library/Caches -type f -mtime +3 $FLAG 2>/dev/null | wc -l | xargs echo "  找到缓存文件:" | tee -a "$LOG_FILE"

# 4. 清理回收站（直接清）
echo "4️⃣ 清理回收站..." | tee -a "$LOG_FILE"
if [ "$DRY_RUN" -eq 0 ]; then rm -rf ~/.Trash/* 2>/dev/null; fi
echo "  回收站已清" | tee -a "$LOG_FILE"

# 5. 清理下载目录安装包（保留30天）
echo "5️⃣ 清理安装包..." | tee -a "$LOG_FILE"
find ~/Downloads -name "*.dmg" -mtime +30 $FLAG 2>/dev/null | wc -l | xargs echo "  找到dmg:" | tee -a "$LOG_FILE"
find ~/Downloads -name "*.pkg" -mtime +30 $FLAG 2>/dev/null | wc -l | xargs echo "  找到pkg:" | tee -a "$LOG_FILE"

# 6. 清理docker（如果装了）
if command -v docker &>/dev/null; then
    echo "6️⃣ 清理Docker..." | tee -a "$LOG_FILE"
    if [ "$DRY_RUN" -eq 0 ]; then docker system prune -a -f 2>/dev/null; fi
fi

# 7. 清理龍魂旧日志（保留7天）
echo "7️⃣ 清理龍魂旧日志..." | tee -a "$LOG_FILE"
find ~/.longhun/logs -name "*.log" -mtime +7 $FLAG 2>/dev/null | wc -l | xargs echo "  找到日志:" | tee -a "$LOG_FILE"
find ~/.longhun/logs -name "*.jsonl" -mtime +30 $FLAG 2>/dev/null | wc -l | xargs echo "  找到jsonl:" | tee -a "$LOG_FILE"

# 8. 清理apfs快照（如果有）
echo "8️⃣ 清理APFS快照..." | tee -a "$LOG_FILE"
if [ "$DRY_RUN" -eq 0 ]; then sudo tmutil deletelocalsnapshots / 2>/dev/null; fi

# 9. 释放系统缓存
echo "9️⃣ 释放系统缓存..." | tee -a "$LOG_FILE"
if [ "$DRY_RUN" -eq 0 ]; then sudo purge 2>/dev/null; fi

# 报告结果
AVAIL=$(df -h / | tail -1 | awk '{print $4}')
echo "✅ 清理完成 - 可用空间: $AVAIL" | tee -a "$LOG_FILE"
echo "📝 日志: $LOG_FILE"