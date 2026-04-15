#!/bin/bash
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# session_end.sh · 会话结束自动摘要归档
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 作者：UID9622 诸葛鑫（龍芯北辰）
# DNA：#龍芯⚡️20260316-SESSION-END-v1.0
# 执行级别：最高 · Stop Hook 自动触发
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LOG_DIR="$HOME/longhun-system/logs"
SESSION_LOG="$LOG_DIR/session_log.jsonl"
SESSION_TMP="/tmp/lh_session_current.jsonl"

mkdir -p "$LOG_DIR"

NOW_ISO=$(date '+%Y-%m-%d %H:%M:%S')
NOW_DATE=$(date '+%Y%m%d')

# 农历
LUNAR=$(python3 -c "
import datetime
lunar_months = [
    ('正月', (2026,2,17)), ('二月', (2026,3,18)), ('三月', (2026,4,17)),
    ('四月', (2026,5,16)), ('五月', (2026,6,15)), ('六月', (2026,7,14)),
    ('七月', (2026,8,12)), ('八月', (2026,9,11)), ('九月', (2026,10,10)),
    ('十月', (2026,11,9)), ('十一月', (2026,12,9)), ('十二月', (2027,1,7)),
    ('正月(丁未)', (2027,1,29)),
]
days_cn = ['初一','初二','初三','初四','初五','初六','初七','初八','初九','初十',
           '十一','十二','十三','十四','十五','十六','十七','十八','十九','二十',
           '廿一','廿二','廿三','廿四','廿五','廿六','廿七','廿八','廿九','三十']
today = datetime.date.today()
result = '丙午年'
for i in range(len(lunar_months)-1):
    m_name, m_start = lunar_months[i]
    next_start = datetime.date(*lunar_months[i+1][1])
    start = datetime.date(*m_start)
    if start <= today < next_start:
        day_n = (today - start).days
        result = f'丙午年{m_name}{days_cn[day_n]}'
        break
print(result)
" 2>/dev/null || echo "丙午年农历")

# 统计本次会话操作
if [ -f "$SESSION_TMP" ]; then
    TOTAL=$(wc -l < "$SESSION_TMP" 2>/dev/null || echo 0)
    TOTAL=$(echo $TOTAL | tr -d ' ')

    SUMMARY=$(python3 -c "
import json, collections
tools = []
targets = []
sensitive_count = 0
try:
    with open('$SESSION_TMP') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                d = json.loads(line)
                tools.append(d.get('tool','?'))
                t = d.get('target','')
                if t:
                    targets.append(t)
                if d.get('sensitive', 0):
                    sensitive_count += 1
            except:
                pass
counter = collections.Counter(tools)
top = [f'{k}×{v}' for k,v in counter.most_common(5)]
print(json.dumps({
    'tool_summary': ', '.join(top),
    'files_touched': list(dict.fromkeys([t for t in targets if '/' in t or '.' in t]))[:10],
    'sensitive_ops': sensitive_count
}, ensure_ascii=False))
" 2>/dev/null || echo '{"tool_summary":"","files_touched":[],"sensitive_ops":0}')

    python3 -c "
import json
s = json.loads('$SUMMARY' if '$SUMMARY' else '{\"tool_summary\":\"\",\"files_touched\":[],\"sensitive_ops\":0}')
entry = {
    'event': 'session_end',
    'time': '$NOW_ISO',
    'lunar': '$LUNAR',
    'dna': '#龍芯⚡️${NOW_DATE}-SESSION-END-UID9622',
    'total_ops': $TOTAL,
    'tool_summary': s.get('tool_summary',''),
    'files_touched': s.get('files_touched',[]),
    'sensitive_ops': s.get('sensitive_ops', 0)
}
print(json.dumps(entry, ensure_ascii=False))
" >> "$SESSION_LOG" 2>/dev/null

    # 清理临时文件
    rm -f "$SESSION_TMP" 2>/dev/null
else
    # 无操作的空会话也记录
    echo "{\"event\":\"session_end\",\"time\":\"$NOW_ISO\",\"lunar\":\"$LUNAR\",\"dna\":\"#龍芯⚡️${NOW_DATE}-SESSION-END-UID9622\",\"total_ops\":0}" >> "$SESSION_LOG" 2>/dev/null
fi

exit 0
