#!/bin/bash
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# ╔══════════════════════════════════════════════════════════════╗
# ║  🐉 龍魂·万年历预警日历 一键部署脚本 v1.1                     ║
# ║  Deploy Calendar · 万年历通知窗口 + ICS订阅 + 篡改巡检 cron     ║
# ╚══════════════════════════════════════════════════════════════╝
# DNA: #龍芯⚡️丙午·丙申·戊午·未时·䷐随-DEPLOY-CALENDAR-v1.1-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# License: MulanPSL v2 · 用法: bash deploy/scripts/deploy_calendar.sh

set -euo pipefail
SSH="ssh -i ~/.ssh/longhun_kunpeng_ed25519 -o ConnectTimeout=10"
REMOTE="root@119.13.90.27"
CAL="/opt/longhun/calendar"
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"

echo "── 0/6 远程建目录 ──"
$SSH "$REMOTE" "mkdir -p $CAL/www $CAL/bin $CAL/data $CAL/state"
echo "   OK"

echo "── 1/6 同步万年历页面 ──"
scp -rq "$ROOT/widgets/longhun-perpetual-calendar/." "$REMOTE:$CAL/www/"
echo "   OK"

echo "── 2/6 同步引擎 + 巡检脚本 ──"
scp -q "$ROOT/bin/lh_dna_scan.py" "$ROOT/bin/lh_calendar_feed.py" "$REMOTE:$CAL/bin/"
scp -q "$ROOT/deploy/scripts/calendar/run_scan.sh" "$REMOTE:$CAL/bin/run_scan.sh"
$SSH "$REMOTE" "chmod +x $CAL/bin/run_scan.sh"
echo "   OK"

echo "── 3/6 初始化数据 + 首跑建基线 ──"
$SSH "$REMOTE" "cd $CAL && python3 bin/lh_dna_scan.py watch /opt/longhun-system --state state/scan_state.json --new-out /dev/null || true; python3 bin/lh_calendar_feed.py --data-dir data add --level 🟢 --title '龍魂万年历·预警日历上线' --desc '鲲鹏自动巡检每小时运行 · GPG签名+DNA四柱双重校验' || true; cp -f data/events.json data/longhun.ics www/ 2>/dev/null || true"
echo "   OK"

echo "── 4/6 nginx 挂载 /calendar/ ──"
$SSH "$REMOTE" 'python3 - <<PYEOF
conf = "/etc/nginx/conf.d/longhun-8080.conf"
text = open(conf).read()
block = """
    location /calendar/ {
        alias /opt/longhun/calendar/www/;
        charset utf-8;
        add_header Cache-Control \\"no-cache\\";
    }
    location /calendar {
        return 301 /calendar/;
    }
"""
if "location /calendar/" in text:
    print("SKIP: /calendar/ 已存在")
else:
    text = text.replace("    location / {", block + "    location / {", 1)
    open(conf, "w").write(text)
    print("INSERTED")
PYEOF'
$SSH "$REMOTE" "nginx -t >/dev/null 2>&1 && systemctl reload nginx && echo '   nginx RELOADED'"

echo "── 5/6 cron 挂载每小时巡检 ──"
$SSH "$REMOTE" "(crontab -l 2>/dev/null | grep -v 'run_scan.sh'; echo '5 * * * * /opt/longhun/calendar/bin/run_scan.sh >> /var/log/longhun/calendar_scan.log 2>&1') | crontab -"
mkdir -p /var/log/longhun 2>/dev/null || true
echo "   OK"

echo "── 6/6 立即实测一次巡检 ──"
$SSH "$REMOTE" "bash $CAL/bin/run_scan.sh; echo 'RC='\$?"

echo ""
echo "🎉 部署完成：http://119.13.90.27:8080/calendar/"
echo "   ICS订阅:  http://119.13.90.27:8080/calendar/longhun.ics"
echo "   webcal:   webcal://119.13.90.27:8080/calendar/longhun.ics"
