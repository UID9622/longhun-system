#!/bin/bash
# 龍魂天罗地网同步器 · 定时脚本
# 每小时执行一次

LOG="$(dirname "$0")/sync.log"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] ▶ 开始同步" >> "$LOG"

cd "$(dirname "$0")"
python3 sync_to_notion.py >> "$LOG" 2>&1
CODE=$?

if [ $CODE -eq 0 ]; then
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] ✅ 同步成功" >> "$LOG"
else
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] ❌ 同步失败 (exit $CODE)" >> "$LOG"
fi

# 日志只保留最新500行
tail -500 "$LOG" > "$LOG.tmp" && mv "$LOG.tmp" "$LOG"
