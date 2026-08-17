#!/bin/bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/bin/bash
# ╔═══════════════════════════════════════════════════════════════╗
# ║  🐉 龍魂·备份状态通知 v1.0                                     ║
# ║  Backup Notify · 备份完成/失败推送                             ║
# ╠═══════════════════════════════════════════════════════════════╣
# ║  DNA: #龍芯⚡️2026-07-12-BARK-BACKUP-NOTIFY-v1.0              ║
# ║  触发: 备份脚本执行后调用此脚本                                  ║
# ║  用法: bash executors/bark/backup_notify.sh [success|fail] "详情" ║
# ╚═══════════════════════════════════════════════════════════════╝

set -euo pipefail

BASE_DIR="/opt/longhun-system"
BARK_SENDER="${BASE_DIR}/executors/bark/bark_send.py"
STATUS="${1:-success}"
DETAIL="${2:-无详细信息}"

TS=$(date '+%Y-%m-%d %H:%M:%S')
HOSTNAME=$(hostname)

# ── 备份信息 ──
BACKUP_SIZE=""
BACKUP_PATH=""
if [ -d "/data/backups" ]; then
    LATEST_BACKUP=$(ls -t /data/backups/ 2>/dev/null | head -1)
    if [ -n "${LATEST_BACKUP}" ]; then
        BACKUP_PATH="/data/backups/${LATEST_BACKUP}"
        BACKUP_SIZE=$(du -sh "${BACKUP_PATH}" 2>/dev/null | cut -f1)
    fi
fi

# ── 磁盘剩余 ──
DISK_AVAIL=$(df -h /data 2>/dev/null | tail -1 | awk '{print $4} "可用"')

if [ "${STATUS}" = "success" ]; then
    TITLE="✅ 龍魂备份完成"
    BODY="📦 备份成功 · ${TS}

文件: ${BACKUP_PATH:-未知}
大小: ${BACKUP_SIZE:-未知}
磁盘剩余: ${DISK_AVAIL}
主机: ${HOSTNAME}

详情: ${DETAIL}

━━━━━━━━━━━━━━━━━━
${TS} · 鲲鹏 · 龍魂系统"
else
    TITLE="❌ 龍魂备份失败"
    BODY="📦 备份失败 · ${TS}

主机: ${HOSTNAME}
原因: ${DETAIL}
磁盘剩余: ${DISK_AVAIL}

请检查备份日志。

━━━━━━━━━━━━━━━━━━
${TS} · 鲲鹏 · 龍魂系统"
fi

echo "${BODY}" | python3 "${BARK_SENDER}" "${TITLE}" --stdin --group "龍魂备份" 2>&1
