#!/bin/bash
# ─────────────────────────────────────────────────────────────
# DNA: #龍芯⚡️2026-09-05-HEALTH-WEEKLY-REPORT-v1.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# 协议: CC BY-NC-SA 4.0（核心思想层）
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 任务: 每周日 23:00 一周健康报告（lh health report·静默·自动GPG+耻辱墙）
#       → ~/.longhun/health_weekly/health_report_YYYY-MM-DD.md
# ─────────────────────────────────────────────────────────────
export PATH="/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/opt/homebrew/bin"
cd /Users/zuimeidedeyihan/longhun-system || exit 1
for i in 1 2 3; do
  /usr/bin/python3 08_BIN/lh_health_snapshot.py report --quiet \
    >> logs/health_weekly_launchd.log 2>&1 && break
  sleep 300
done
# v1.1 (2026-09-06): 周报后自动同步到 Notion 公开库(失败不阻塞·静默)
/usr/bin/python3 08_BIN/lh_health_sync.py sync --quiet \
  >> logs/health_weekly_launchd.log 2>&1
exit 0
