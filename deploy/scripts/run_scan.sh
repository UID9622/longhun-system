#!/bin/bash
# ╔══════════════════════════════════════════════════════════════╗
# ║  🐉 龍魂·篡改巡检 cron 入口 v1.1                              ║
# ║  每小时由 cron 调用：DNA扫描 → 新异常 → 日历事件 + Bark       ║
# ║  文明基因图谱 → 历史重演 + 预言 + H武器投影 发布到 www        ║
# ╚══════════════════════════════════════════════════════════════╝
# DNA: #龍芯⚡️丙午·丙申·戊午·未时·䷐随-CALENDAR-SCAN-CRON-v1.1-UID9622
# License: MulanPSL v2 · 部署位置: /opt/longhun/calendar/bin/run_scan.sh

set -u
BASE=/opt/longhun/calendar
STATE=$BASE/state
DATA=$BASE/data
WWW=$BASE/www
mkdir -p "$STATE" "$DATA" "$WWW"
cd "$BASE" || exit 0

# 1. watch 扫描：只报新增异常（首次已建基线）
python3 bin/lh_dna_scan.py watch /opt/longhun-system \
    --state "$STATE/scan_state.json" --new-out "$STATE/new_fail.json"
RC=$?

# 2. 新增异常 → 日历事件 + Bark
if [ "$RC" -eq 1 ]; then
    FAIL_N=$(python3 -c "import json;d=json.load(open('$STATE/new_fail.json'));print(len(d['new_sig_fail']))" 2>/dev/null)
    FAILS=$(python3 -c "import json;d=json.load(open('$STATE/new_fail.json'));print(' '.join(d['new_sig_fail'][:5]))" 2>/dev/null)
    DIFF_N=$(python3 -c "import json;d=json.load(open('$STATE/new_fail.json'));print(len(d['new_ganzhi_diff']))" 2>/dev/null)
    if [ "${FAIL_N:-0}" -gt 0 ]; then
        python3 bin/lh_calendar_feed.py --data-dir "$DATA" add --level 🔴 \
            --title "篡改检测告警：${FAIL_N} 个文件" \
            --desc "GPG签名失效：${FAILS}" || true
        python3 /opt/longhun-system/executors/bark/bark_send.py \
            "🐉篡改告警" "GPG签名失效 ${FAIL_N} 个文件：${FAILS}" 2>/dev/null || true
    fi
    if [ "${DIFF_N:-0}" -gt 0 ]; then
        python3 bin/lh_calendar_feed.py --data-dir "$DATA" add --level 🟡 \
            --title "DNA四柱差异告警" \
            --desc "标准算法重算不符 ${DIFF_N} 处（旧算法或修改未更新DNA），详见预警日历" || true
    fi
fi

# 3. 文明基因图谱：历史重演 + 预言 + H武器投影（三方向 · 深/宽/活）
#    输出 gene-map.json / prophecy.json / h-weapon.json → www/ 供页面渲染
if [ -f bin/lh_civilization_map.py ]; then
    python3 bin/lh_civilization_map.py scan --out "$WWW" --quiet 2>/dev/null || true
fi

# 4. 发布到 www（万年历面板 + 订阅源）
cp -f "$DATA/events.json" "$DATA/longhun.ics" "$WWW/" 2>/dev/null || true
exit 0
