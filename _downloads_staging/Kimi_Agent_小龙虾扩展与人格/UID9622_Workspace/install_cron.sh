#!/bin/bash
# 一键安装 UID9622 五大人格定时任务
set -e
WORKSPACE="/Users/zuimeidedeyihan/Downloads/Kimi_Agent_小龙虾扩展与人格/UID9622_Workspace"
CRON_OUT="$WORKSPACE/cron.d/uid9622_personas.cron"

mkdir -p "$WORKSPACE/cron.d"
cat "$WORKSPACE/backend_personas"/*/cron.conf > "$CRON_OUT"

echo "已合并定时任务到: $CRON_OUT"
echo "安装方式（二选一）："
echo "  1) 追加到当前用户 crontab: (crontab -l 2>/dev/null; cat $CRON_OUT) | crontab -"
echo "  2) 覆盖当前用户 crontab:   crontab $CRON_OUT"
