#!/usr/bin/env bash
# 龍魂·自动对齐闭环 一键部署脚本 v2.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 用法：把本脚本和 bin/ 目录放到 ~/longhun-system/ 下，然后执行：
#   bash deploy_align_loop.sh
set -euo pipefail

BASE="$HOME/longhun-system"
cd "$BASE"

echo "==> 1/5 建目录"
mkdir -p bin reports logs/fixes archive/frozen

echo "==> 2/5 赋权"
chmod +x bin/lh_auto_align_daemon.py bin/lh_fix_missing_dna.py bin/lh_fix_missing_confirm.py 2>/dev/null || true

echo "==> 3/5 语法自检（不通过就停下，不装定时任务）"
python3 -m py_compile bin/lh_auto_align_daemon.py bin/lh_fix_missing_dna.py bin/lh_fix_missing_confirm.py
echo "    语法 OK"

echo "==> 4/5 干跑验证（只检测不改文件）"
python3 bin/lh_auto_align_daemon.py --dry-run || echo "    干跑有告警，先看输出再决定是否上定时"

echo "==> 5/5 安装定时任务（每小时一次，带 flock 防重入 + 日志按周切割）"
CRON_LINE='0 * * * * flock -n /tmp/lh_align.lock bash -c "cd $HOME/longhun-system && python3 bin/lh_auto_align_daemon.py >> logs/auto_align_$(date +\%Y\%W).log 2>&1"'
( crontab -l 2>/dev/null | grep -v "lh_auto_align_daemon" ; echo "$CRON_LINE" ) | crontab -
echo "    crontab 已更新："
crontab -l | grep "lh_auto_align_daemon" || true

echo ""
echo "✅ 部署完成。常用命令："
echo "   手动跑一轮:   python3 ~/longhun-system/bin/lh_auto_align_daemon.py"
echo "   只看不动手:   python3 ~/longhun-system/bin/lh_auto_align_daemon.py --dry-run"
echo "   看今天通知:   cat ~/longhun-system/logs/fixes/notifications_\$(date +%Y%m%d).log"
echo "   看归档:       ls ~/longhun-system/archive/archive_*.json"
