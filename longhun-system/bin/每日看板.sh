#!/bin/bash
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 龍魂每日看板 · 一眼看全貌
# DNA: #龍芯⚡️2026-03-18-每日看板-v1.0
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

BASE="$HOME/longhun-system"
TODAY=$(date '+%Y-%m-%d')
NOW=$(date '+%Y-%m-%d %H:%M:%S')

# 颜色
GR='\033[0;32m'  # 绿
YE='\033[0;33m'  # 黄
RD='\033[0;31m'  # 红
CY='\033[0;36m'  # 青
BL='\033[1;34m'  # 蓝
NC='\033[0m'     # 重置

服务状态() {
    local port=$1
    local name=$2
    if lsof -i :$port > /dev/null 2>&1; then
        echo -e "  ${GR}🟢${NC} $name"
    else
        echo -e "  ${RD}🔴${NC} $name"
    fi
}

# ── 农历 ─────────────────────────────────
LUNAR=$(python3 -c "
import datetime
lunar_months = [
    ('正月',(2026,2,17)),('二月',(2026,3,18)),('三月',(2026,4,17)),
    ('四月',(2026,5,16)),('五月',(2026,6,15)),('六月',(2026,7,14)),
    ('七月',(2026,8,12)),('八月',(2026,9,11)),('九月',(2026,10,10)),
    ('十月',(2026,11,9)),('十一月',(2026,12,9)),('十二月',(2027,1,7)),
]
days=['初一','初二','初三','初四','初五','初六','初七','初八','初九','初十',
      '十一','十二','十三','十四','十五','十六','十七','十八','十九','二十',
      '廿一','廿二','廿三','廿四','廿五','廿六','廿七','廿八','廿九','三十']
today=datetime.date.today()
for i in range(len(lunar_months)-1):
    m,s=lunar_months[i]; ns=datetime.date(*lunar_months[i+1][1]); st=datetime.date(*s)
    if st<=today<ns:
        print(f'丙午年{m}{days[(today-st).days]}'); break
else: print('丙午年')
" 2>/dev/null || echo "丙午年")

clear
echo ""
echo -e "${CY}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BL}  🐉 龍魂每日看板  ·  $TODAY  ·  $LUNAR${NC}"
echo -e "${CY}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

# ══ 1. 服务状态 ════════════════════════════
echo ""
echo -e "${YE}  ⚡ 服务状态${NC}"
服务状态 8765  "龍魂本地服务  http://localhost:8765"
服务状态 11434 "Ollama模型    http://localhost:11434"
服务状态 3000  "Open WebUI    http://localhost:3000"

# ══ 2. 今日活动统计 ════════════════════════
echo ""
echo -e "${YE}  📊 今日活动（$TODAY）${NC}"

# 今日操作数
TODAY_OPS=0
if [ -f "$BASE/logs/action_log.jsonl" ]; then
    TODAY_OPS=$(grep -c "\"$TODAY" "$BASE/logs/action_log.jsonl" 2>/dev/null || echo 0)
fi
echo "  · 工具调用次数：${TODAY_OPS} 次"

# 今日会话数
TODAY_SESSIONS=0
if [ -f "$BASE/logs/session_log.jsonl" ]; then
    TODAY_SESSIONS=$(grep -c "$TODAY" "$BASE/logs/session_log.jsonl" 2>/dev/null || echo 0)
fi
echo "  · 今日会话数：  ${TODAY_SESSIONS} 次"

# 今日审计
TODAY_AUDIT=0
if [ -f "$BASE/logs/audit_log.jsonl" ]; then
    TODAY_AUDIT=$(grep -c "$TODAY" "$BASE/logs/audit_log.jsonl" 2>/dev/null; true)
    [ -z "$TODAY_AUDIT" ] && TODAY_AUDIT=0
fi
echo "  · 审计记录：    ${TODAY_AUDIT} 条"

# 最后同步时间
LAST_SYNC=""
if [ -f "$BASE/logs/同步日志.log" ]; then
    LAST_SYNC=$(grep "同步完成" "$BASE/logs/同步日志.log" 2>/dev/null | tail -1 | cut -c2-17)
fi
[ -n "$LAST_SYNC" ] && echo "  · 最后同步：    $LAST_SYNC" || echo "  · 最后同步：    今日未同步"

# ══ 3. 星辰记忆 ═══════════════════════════
echo ""
echo -e "${YE}  🌟 星辰记忆库${NC}"
STAR_COUNT=0
if [ -f "$HOME/.star-memory/index.json" ]; then
    STAR_COUNT=$(python3 -c "import json; d=json.load(open('$HOME/.star-memory/index.json')); print(len(d))" 2>/dev/null || echo 0)
fi
STAR_SIZE=$(du -sh "$HOME/.star-memory/" 2>/dev/null | cut -f1)
echo "  · 记忆条数：    ${STAR_COUNT} 条"
echo "  · 占用空间：    ${STAR_SIZE}"

# ══ 4. 资源库统计 ══════════════════════════
echo ""
echo -e "${YE}  📦 资源库文件统计${NC}"

count_dir() {
    local dir="$1"
    local label="$2"
    if [ -d "$dir" ]; then
        local cnt=$(find "$dir" -type f 2>/dev/null | wc -l | tr -d ' ')
        printf "  · %-12s %4s 个文件\n" "$label" "$cnt"
    fi
}

count_dir "$BASE/资源库/图片归档"   "图片归档"
count_dir "$BASE/资源库/视频归档"   "视频归档"
count_dir "$BASE/资源库/文档归档"   "文档归档"
count_dir "$BASE/资源库/代码归档"   "代码归档"
count_dir "$BASE/资源库/压缩包归档" "压缩包"
count_dir "$BASE/资源库/待处理"     "待处理"
count_dir "$BASE/私密区"            "私密区"

# ══ 5. 磁盘空间 ═══════════════════════════
echo ""
echo -e "${YE}  💾 空间使用${NC}"
DISK_FREE=$(df -h ~ | tail -1 | awk '{print $4}')
DISK_TOTAL=$(df -h ~ | tail -1 | awk '{print $2}')
DISK_PCT=$(df ~ | tail -1 | awk '{print $5}')
BASE_SIZE=$(du -sh "$BASE" 2>/dev/null | cut -f1)
echo "  · 系统剩余：    ${DISK_FREE} / ${DISK_TOTAL}  (已用${DISK_PCT})"
echo "  · 龍魂系统：    ${BASE_SIZE}"

DESKTOP_CNT=$(find "$HOME/Desktop" -maxdepth 1 -type f 2>/dev/null | wc -l | tr -d ' ')
DOWN_CNT=$(find "$HOME/Downloads" -maxdepth 1 -type f 2>/dev/null | wc -l | tr -d ' ')
echo "  · 桌面文件：    ${DESKTOP_CNT} 个"
echo "  · 下载文件夹：  ${DOWN_CNT} 个"

# ══ 6. 封印资产速览 ═══════════════════════
echo ""
echo -e "${YE}  🔒 封印资产（${NC}$(ls "$BASE/封印库/"*.json 2>/dev/null | wc -l | tr -d ' ')个已封印${YE}）${NC}"
for f in "$BASE/封印库/"*_封印包.json; do
    [ -f "$f" ] || continue
    name=$(python3 -c "import json; d=json.load(open('$f')); print(d.get('名称','?'))" 2>/dev/null)
    echo "  · $name"
done

# ══ 7. 最近5条操作记录 ════════════════════
echo ""
echo -e "${YE}  📋 最近操作记录${NC}"
if [ -f "$BASE/logs/action_log.jsonl" ]; then
    python3 - << 'PYEOF'
import json, os
log = os.path.expanduser("~/longhun-system/logs/action_log.jsonl")
lines = open(log).readlines()[-5:]
for l in lines:
    try:
        d = json.loads(l)
        t = d.get('time','')[:16]
        tool = d.get('tool','')
        target = d.get('target','')[:35]
        print(f"  · {t}  {tool:<8}  {target}")
    except: pass
PYEOF
else
    echo "  · 暂无记录"
fi

# ══ 快捷操作提示 ══════════════════════════
echo ""
echo -e "${CY}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "  ${GR}lh${NC}=指挥台  ${GR}lh-sync${NC}=同步  ${GR}lh-sort${NC}=整理  ${GR}lh-clean${NC}=清垃圾"
echo -e "${CY}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
