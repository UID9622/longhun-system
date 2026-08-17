#!/bin/bash
# DNA: #龍芯⚡️丙午·丙申·己未·乙亥时·䷒临-ROLLBACK-v1.0-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# SPDX-License-Identifier: MulanPSL-2.0
# ==============================================================================
# 🐉 龍魂 · 一键回滚
# 修正11: 备份为时间戳目录 + manifest, 回滚取最新备份 (不再用不匹配的 date 格式)。
# 用法: sudo ./rollback.sh [备份目录]     # 缺省取 /var/backups/longhun 下最新
# ==============================================================================

set -euo pipefail

BACKUP_ROOT="/var/backups/longhun"

[ "$(id -u)" -eq 0 ] || { echo "🔴 请使用 root 权限运行: sudo $0" >&2; exit 1; }

# 取最新备份目录 (目录名为 YYYYMMDD_HHMMSS, 字典序即时间序)
BACKUP_DIR="${1:-$(ls -1d "${BACKUP_ROOT}"/*/ 2>/dev/null | sort | tail -1 || true)}"
[ -n "${BACKUP_DIR}" ] && [ -f "${BACKUP_DIR}/manifest.txt" ] \
    || { echo "🔴 未找到可用备份 (${BACKUP_ROOT}/*/manifest.txt)" >&2; exit 1; }

echo "🐉 龍魂 · 回滚到备份: ${BACKUP_DIR}"
echo "--- manifest ---"
cat "${BACKUP_DIR}/manifest.txt"
echo "----------------"

restore() {  # $1=备份名 $2=目标路径
    if [ -f "${BACKUP_DIR}/$1" ]; then
        cp -a "${BACKUP_DIR}/$1" "$2"
        echo "  恢复: $2"
    else
        echo "  跳过(备份中不存在, 首次部署前状态): $2 → 移除现文件"
        rm -f "$2"
    fi
}

restore nginx.conf /etc/nginx/nginx.conf
restore sites-available-longhun /etc/nginx/sites-available/longhun
restore longhun-api.service /etc/systemd/system/longhun-api.service
restore longhun-collab.service /etc/systemd/system/longhun-collab.service
restore longhun-bridge.service /etc/systemd/system/longhun-bridge.service
restore cron.d-longhun /etc/cron.d/longhun
restore logrotate-longhun /etc/logrotate.d/longhun

# sites-available/longhun 被移除时同步摘除软链
[ -e /etc/nginx/sites-available/longhun ] || rm -f /etc/nginx/sites-enabled/longhun

systemctl daemon-reload

if command -v nginx >/dev/null 2>&1; then
    if nginx -t; then
        systemctl reload nginx 2>/dev/null || systemctl restart nginx
        echo "✅ nginx 已回滚并重载"
    else
        echo "🔴 回滚后 nginx -t 仍失败, 请人工检查 /etc/nginx/" >&2
        exit 1
    fi
fi

for u in longhun-api longhun-collab longhun-bridge; do
    if [ -f "/etc/systemd/system/${u}.service" ]; then
        systemctl restart "${u}" || true
    fi
done

echo "✅ 回滚完成。验证: nginx -t && systemctl status nginx --no-pager"
