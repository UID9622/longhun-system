#!/bin/bash
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# DNA: #龍芯⚡️丙午·甲申·辛丑·甲午·䷁坤-DISK-MONITOR-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
THRESHOLD=85
CURRENT=$(df -h / | awk 'NR==2 {print $5}' | sed 's/%//')
LOG="/var/log/longhun-disk-monitor.log"
TS=$(date -Iseconds)

if [ "$CURRENT" -gt "$THRESHOLD" ]; then
    echo "[$TS] 🔴 磁盘告警：已使用 ${CURRENT}%，超过阈值 ${THRESHOLD}%" >> "$LOG"
    echo "[$TS] 📋 Top 5 大目录:" >> "$LOG"
    du -sh /* 2>/dev/null | sort -rh | head -5 >> "$LOG"
    echo "[$TS] 🔄 触发 Phase1 清理..." >> "$LOG"
    journalctl --vacuum-size=500M >> "$LOG" 2>&1
    rm -rf /tmp/* /var/tmp/* 2>/dev/null
    find /var/log -name '*.log' -mtime +180 -delete 2>/dev/null
    find /opt -type d -name '__pycache__' -exec rm -rf {} + 2>/dev/null
    docker system prune -a -f 2>/dev/null
    echo "[$TS] ✅ Phase1 完成，当前磁盘: $(df -h / | awk 'NR==2 {print $5}')" >> "$LOG"
else
    echo "[$TS] 🟢 磁盘正常：已使用 ${CURRENT}%" >> "$LOG"
fi
