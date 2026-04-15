#!/bin/bash
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# action_logger.sh · 龍魂自动操作记录器
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 作者：UID9622 诸葛鑫（龍芯北辰）
# DNA：#龍芯⚡️20260316-ACTION-LOGGER-v1.0
# 执行级别：最高 · PostToolUse Hook 自动触发
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LOG_DIR="$HOME/longhun-system/logs"
PLAIN_LOG="$LOG_DIR/action_log.jsonl"
SECURE_LOG="$LOG_DIR/action_secure.jsonl"
SESSION_TMP="/tmp/lh_session_current.jsonl"
GPG_ID="A2D0092CEE2E5BA87035600924C3704A8CC26D5F"

mkdir -p "$LOG_DIR"

# 读取 hook 传入的 JSON
INPUT=$(cat 2>/dev/null)
[ -z "$INPUT" ] && exit 0

# 时间戳（公历）
NOW_ISO=$(date '+%Y-%m-%d %H:%M:%S')
NOW_DATE=$(date '+%Y%m%d')
NOW_TS=$(date '+%s')

# 农历计算
LUNAR=$(python3 -c "
import datetime
# 丙午年2026 各月初一对应公历
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

# 解析工具信息
PARSE=$(python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    tool = d.get('tool_name', 'unknown')
    ti = d.get('tool_input', {})
    target = ti.get('file_path') or ti.get('command') or ti.get('pattern') or ti.get('path') or ''
    # 截断过长命令
    if len(target) > 120:
        target = target[:120] + '...'
    print(json.dumps({'tool': tool, 'target': target}))
except:
    print(json.dumps({'tool': 'unknown', 'target': ''}))
" <<< "$INPUT" 2>/dev/null || echo '{"tool":"unknown","target":""}')

TOOL=$(echo "$PARSE" | python3 -c "import sys,json;d=json.load(sys.stdin);print(d['tool'])" 2>/dev/null || echo "unknown")
TARGET=$(echo "$PARSE" | python3 -c "import sys,json;d=json.load(sys.stdin);print(d['target'])" 2>/dev/null || echo "")

# 敏感检测
IS_SENSITIVE=0
SENSITIVE_REASON=""

# 敏感文件路径
if echo "$TARGET" | grep -qiE '\.env$|\.ssh/|password|token|secret|\.key$|gpg|\.pem|\.p12|id_rsa|id_ed25519'; then
    IS_SENSITIVE=1
    SENSITIVE_REASON="sensitive_file"
fi

# 敏感命令
if [ "$TOOL" = "Bash" ]; then
    CMD=$(echo "$INPUT" | python3 -c "import sys,json;d=json.load(sys.stdin);print(d.get('tool_input',{}).get('command',''))" 2>/dev/null || echo "")
    if echo "$CMD" | grep -qiE 'rm\s+-rf|push.*--force|reset.*--hard|drop\s+table|DELETE\s+FROM|passwd|ssh-keygen|gpg.*--export|curl.*token|curl.*secret'; then
        IS_SENSITIVE=1
        SENSITIVE_REASON="dangerous_command"
    fi
fi

# 构造日志条目
ENTRY=$(python3 -c "
import json
entry = {
    'time': '$NOW_ISO',
    'lunar': '$LUNAR',
    'ts': $NOW_TS,
    'dna': '#龍芯⚡️${NOW_DATE}-ACTION-UID9622',
    'tool': '$TOOL',
    'target': $(echo "$TARGET" | python3 -c "import sys,json;print(json.dumps(sys.stdin.read().strip()))" 2>/dev/null || echo '\"\"'),
    'sensitive': $IS_SENSITIVE
}
if '$SENSITIVE_REASON':
    entry['reason'] = '$SENSITIVE_REASON'
print(json.dumps(entry, ensure_ascii=False))
" 2>/dev/null || echo "{\"time\":\"$NOW_ISO\",\"lunar\":\"$LUNAR\",\"tool\":\"$TOOL\",\"error\":\"parse_failed\"}")

# 写入会话临时文件（用于会话摘要）
echo "$ENTRY" >> "$SESSION_TMP" 2>/dev/null

# 敏感操作 → 加密存储，不进主日志
if [ $IS_SENSITIVE -eq 1 ]; then
    echo "$ENTRY" >> "$SECURE_LOG" 2>/dev/null
    # 可选：GPG加密（有GPG密钥时自动启用）
    # echo "$ENTRY" | gpg --batch -r "$GPG_ID" --encrypt --armor >> "${SECURE_LOG}.gpg" 2>/dev/null
else
    echo "$ENTRY" >> "$PLAIN_LOG" 2>/dev/null
fi

exit 0
