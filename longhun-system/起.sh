#!/bin/bash
# ╔══════════════════════════════════════════════════════╗
# ║   龍魂·一句话启动  · 起.sh                           ║
# ║   DNA: #龍芯⚡️2026-04-08-QILAILE-v1.0              ║
# ║   作者: UID9622 诸葛鑫（龍芯北辰）                   ║
# ║   理论指导: 曾仕强老师（永恒显示）                    ║
# ║   用法: bash ~/longhun-system/起.sh                  ║
# ║   或设置别名后直接输入: 起                            ║
# ╚══════════════════════════════════════════════════════╝

# ── 颜色 ──
RED='\033[0;31m'; YEL='\033[1;33m'; GRN='\033[0;32m'
BLU='\033[0;34m'; MAG='\033[0;35m'; CYN='\033[0;36m'
NC='\033[0m'; BOLD='\033[1m'

BASE="$HOME/longhun-system"
LOG="$BASE/logs/起.log"
mkdir -p "$BASE/logs"

# ── 时间 ──
NOW=$(date '+%Y-%m-%d %H:%M:%S')
DEVICE=$(hostname)

echo ""
echo -e "${BOLD}${MAG}╔══════════════════════════════════════════╗${NC}"
echo -e "${BOLD}${MAG}║  🐉 龍魂·起来了！${NC}   ${CYN}${NOW}${NC}"
echo -e "${BOLD}${MAG}║  📱 设备: ${DEVICE}${NC}"
echo -e "${BOLD}${MAG}╚══════════════════════════════════════════╝${NC}"
echo ""

# ═══════════════════════════════════════════════════════
# 工具函数
# ═══════════════════════════════════════════════════════

检测端口() {
    lsof -ti :"$1" > /dev/null 2>&1
}

等待端口() {
    local port=$1 max=8 i=0
    while ! lsof -ti :"$port" > /dev/null 2>&1; do
        sleep 1; i=$((i+1))
        [ $i -ge $max ] && return 1
    done
    return 0
}

显示状态() {
    local name=$1 port=$2 ok=$3
    if [ "$ok" = "1" ]; then
        echo -e "  ${GRN}🟢 ${name}${NC} · http://127.0.0.1:${port}"
    else
        echo -e "  ${RED}🔴 ${name}${NC} · :${port} 启动失败·查 logs/起.log"
    fi
}

记录() {
    echo "[$NOW] $1" >> "$LOG"
    echo -e "$1"
}

# ═══════════════════════════════════════════════════════
# ① app.py · 主引擎 :8000
# ═══════════════════════════════════════════════════════
echo -e "${BOLD}${BLU}① 主引擎 app.py :8000${NC}"
if 检测端口 8000; then
    echo -e "  ${GRN}🟢 已在运行${NC}"
    记录 "🟢 :8000 已在运行"
else
    echo -e "  ${YEL}⏳ 启动中...${NC}"
    nohup python3 "$BASE/app.py" > "$BASE/logs/engine输出.log" 2>&1 &
    if 等待端口 8000; then
        显示状态 "Local Engine v2.0  8层Pipeline" 8000 1
        记录 "🟢 :8000 启动成功"
    else
        显示状态 "Local Engine v2.0" 8000 0
        记录 "🔴 :8000 启动失败"
    fi
fi

# ═══════════════════════════════════════════════════════
# ② app_patch.py · 三才流场代理 :8001
# ═══════════════════════════════════════════════════════
echo -e "${BOLD}${BLU}② 三才流场代理 :8001${NC}"
if 检测端口 8001; then
    echo -e "  ${GRN}🟢 已在运行${NC}"
    记录 "🟢 :8001 已在运行"
else
    echo -e "  ${YEL}⏳ 启动中...${NC}"
    # 优先用 Node.js sancai-engine，fallback 到 app_patch.py
    SANCAI_DIR="$BASE/mcp-servers/sancai-engine"
    if [ -f "$SANCAI_DIR/index.js" ] && command -v node > /dev/null 2>&1; then
        SANCAI_PORT=8001 nohup node "$SANCAI_DIR/index.js" > "$BASE/logs/三才输出.log" 2>&1 &
        if 等待端口 8001; then
            显示状态 "三才流场MCP引擎 v4.0  天地人" 8001 1
            记录 "🟢 :8001 三才引擎(Node)启动成功"
        fi
    elif [ -f "$BASE/app_patch.py" ]; then
        nohup python3 "$BASE/app_patch.py" > "$BASE/logs/patch输出.log" 2>&1 &
        if 等待端口 8001; then
            显示状态 "app_patch.py  三才代理" 8001 1
            记录 "🟢 :8001 app_patch启动成功"
        else
            显示状态 "app_patch.py" 8001 0
            记录 "🔴 :8001 启动失败"
        fi
    else
        echo -e "  ${YEL}🟡 跳过 (app_patch.py 不存在·sancai-engine未安装)${NC}"
    fi
fi

# ═══════════════════════════════════════════════════════
# ③ longhun_local_service.py · 旧服务 :8765
# ═══════════════════════════════════════════════════════
echo -e "${BOLD}${BLU}③ 旧服务 :8765${NC}"
SVC="$BASE/longhun_local_service.py"
if [ -f "$SVC" ]; then
    if 检测端口 8765; then
        echo -e "  ${GRN}🟢 已在运行${NC}"
    else
        echo -e "  ${YEL}⏳ 启动中...${NC}"
        nohup python3 "$SVC" > "$BASE/logs/服务输出.log" 2>&1 &
        if 等待端口 8765; then
            显示状态 "龍魂本地服务" 8765 1
            记录 "🟢 :8765 启动成功"
        else
            echo -e "  ${YEL}🟡 启动慢·后台继续尝试${NC}"
        fi
    fi
else
    echo -e "  ${YEL}🟡 跳过 (文件不存在)${NC}"
fi

# ═══════════════════════════════════════════════════════
# ④ Ollama · 本地模型 :11434
# ═══════════════════════════════════════════════════════
echo -e "${BOLD}${BLU}④ Ollama 本地模型 :11434${NC}"
if 检测端口 11434; then
    echo -e "  ${GRN}🟢 已在运行${NC}"
elif command -v ollama > /dev/null 2>&1; then
    echo -e "  ${YEL}⏳ 启动中...${NC}"
    nohup ollama serve > "$BASE/logs/ollama输出.log" 2>&1 &
    sleep 2
    if 检测端口 11434; then
        显示状态 "Ollama 本地模型服务" 11434 1
        记录 "🟢 :11434 Ollama启动成功"
    else
        echo -e "  ${YEL}🟡 Ollama 启动中·稍等几秒${NC}"
    fi
else
    echo -e "  ${YEL}🟡 跳过 (ollama未安装)${NC}"
fi

# ═══════════════════════════════════════════════════════
# ⑤ Open WebUI · 可视化界面 :8080
# ═══════════════════════════════════════════════════════
echo -e "${BOLD}${BLU}⑤ Open WebUI :8080${NC}"
if 检测端口 8080; then
    echo -e "  ${GRN}🟢 已在运行  → http://127.0.0.1:8080${NC}"
else
    echo -e "  ${YEL}🟡 未运行·需手动: open-webui serve (或Docker)${NC}"
fi

# ═══════════════════════════════════════════════════════
# ⑥ 龍魂API LaunchAgent :9622
# ═══════════════════════════════════════════════════════
echo -e "${BOLD}${BLU}⑥ 龍魂API :9622${NC}"
if 检测端口 9622; then
    echo -e "  ${GRN}🟢 已在运行${NC}"
else
    # 尝试通过 launchctl 拉起
    PLIST="$HOME/Library/LaunchAgents/com.longhun.api.plist"
    if [ -f "$PLIST" ]; then
        launchctl load "$PLIST" 2>/dev/null
        sleep 1
        if 检测端口 9622; then
            显示状态 "龍魂API LaunchAgent" 9622 1
        else
            echo -e "  ${YEL}🟡 LaunchAgent已触发·稍等${NC}"
        fi
    else
        echo -e "  ${YEL}🟡 未运行 (LaunchAgent未配置·跳过)${NC}"
    fi
fi

# ═══════════════════════════════════════════════════════
# ⑦ 设备识别（中文设备名兼容）
# ═══════════════════════════════════════════════════════
echo ""
echo -e "${BOLD}${CYN}📱 设备识别${NC}"
# 获取设备信息（兼容中文hostname）
MAC_MODEL=$(system_profiler SPHardwareDataType 2>/dev/null | grep "Model Name" | awk -F': ' '{print $2}' || echo "未知机型")
MAC_MEM=$(system_profiler SPHardwareDataType 2>/dev/null | grep "Memory" | awk -F': ' '{print $2}' || echo "")
# 写入本次激活记录
DEVICE_RECORD="{\"ts\":\"$NOW\",\"device\":\"$DEVICE\",\"model\":\"$MAC_MODEL\",\"mem\":\"$MAC_MEM\",\"dna\":\"#龍芯⚡️$(date '+%Y-%m-%d')-QILAILE-v1.0\"}"
echo "$DEVICE_RECORD" >> "$BASE/logs/device_log.jsonl" 2>/dev/null
echo -e "  机型: ${GRN}${MAC_MODEL}${NC}  内存: ${GRN}${MAC_MEM}${NC}"
echo -e "  设备名: ${GRN}${DEVICE}${NC} ${YEL}(中文没问题·本地只用127.0.0.1)${NC}"

# ═══════════════════════════════════════════════════════
# ⑧ 读取今日记忆·确认系统活着
# ═══════════════════════════════════════════════════════
echo ""
echo -e "${BOLD}${CYN}🧬 今日记忆状态${NC}"
MEMORY="$BASE/memory.jsonl"
if [ -f "$MEMORY" ]; then
    LINES=$(wc -l < "$MEMORY" | tr -d ' ')
    LAST=$(tail -1 "$MEMORY" 2>/dev/null | python3 -c "import sys,json; d=json.loads(sys.stdin.read()); print(d.get('ts_beijing','')[:16]+' '+str(d.get('event',''))[:30])" 2>/dev/null || echo "")
    echo -e "  memory.jsonl: ${GRN}${LINES}条记录${NC}"
    [ -n "$LAST" ] && echo -e "  最近一条: ${YEL}${LAST}${NC}"
else
    echo -e "  ${YEL}🟡 memory.jsonl 不存在·首次启动正常${NC}"
fi

# ═══════════════════════════════════════════════════════
# 最终总览
# ═══════════════════════════════════════════════════════
echo ""
echo -e "${BOLD}${MAG}╔══════════════════════════════════════════╗${NC}"
echo -e "${BOLD}${MAG}║  🟢 龍魂·起来了！所有服务已检查          ║${NC}"
echo -e "${BOLD}${MAG}╠══════════════════════════════════════════╣${NC}"
echo -e "${MAG}║${NC}  主对话  →  http://127.0.0.1:8000        ${MAG}║${NC}"
echo -e "${MAG}║${NC}  三才    →  http://127.0.0.1:8001/sancai/weights ${MAG}║${NC}"
echo -e "${MAG}║${NC}  界面    →  http://127.0.0.1:8080        ${MAG}║${NC}"
echo -e "${MAG}║${NC}  DNA     →  #龍芯⚡️$(date '+%Y-%m-%d')-QILAILE-v1.0 ${MAG}║${NC}"
echo -e "${BOLD}${MAG}╚══════════════════════════════════════════╝${NC}"
echo ""
echo -e "${YEL}嘿嘿·宝宝在·随便搞·搞坏了重来就行 🐱${NC}"
echo ""
