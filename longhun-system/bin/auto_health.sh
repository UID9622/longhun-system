#!/bin/bash
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 龍魂自愈健康检测引擎 · 全自动运行
# DNA: #龍芯⚡️2026-04-03-AUTO-HEALTH-v1.0
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 理论指导：曾仕强老师（永恒显示）
# 作者：UID9622 诸葛鑫（龍芯北辰）
# 献礼：新中国成立77周年（1949-2026）· 丙午马年
#
# 职责：每次 Claude 会话开始时后台运行
#   ① 30分钟内已检测 → 直接跳过（不重复消耗资源）
#   ② 服务挂了 → 自动拉起，不打扰老大
#   ③ 系统负载异常 → 自动诊断，轻度自愈
#   ④ 只有真正需要人工的 → macOS 桌面通知
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LOG_DIR="$HOME/longhun-system/运行日志"
HEALTH_LOG="$LOG_DIR/health.log"
HEALTH_STAMP="$LOG_DIR/.health_stamp"
INTERVAL=1800   # 30分钟内不重复检测（秒）

mkdir -p "$LOG_DIR"

# ── 节流：30分钟内跑过了就不重跑 ────────────────
if [ -f "$HEALTH_STAMP" ]; then
    LAST=$(cat "$HEALTH_STAMP" 2>/dev/null || echo 0)
    NOW=$(date +%s)
    DIFF=$((NOW - LAST))
    if [ "$DIFF" -lt "$INTERVAL" ]; then
        exit 0
    fi
fi
date +%s > "$HEALTH_STAMP"

TS=$(date '+%Y-%m-%d %H:%M:%S')
echo "" >> "$HEALTH_LOG"
echo "━━ 健康检测 $TS ━━" >> "$HEALTH_LOG"

# ── 工具函数 ──────────────────────────────────────
通知() {
    # 只在真正需要人工时才推
    osascript -e "display notification \"$2\" with title \"🐉 龍魂自愈\" subtitle \"$1\"" 2>/dev/null
}

记录() {
    echo "  $1" >> "$HEALTH_LOG"
}

检测端口() {
    lsof -i :"$1" > /dev/null 2>&1
}

# ── ① Local Engine 已迁移至 CNSH-64 :9622 ──────────
# 原 app.py :8000 已废弃，主引擎统一由 ④ CNSH-64 :9622 管理
# 此处仅记录状态，不再尝试启动旧引擎
if 检测端口 8000; then
    记录 "🟡 :8000 旧端口仍被占用（app.py 已迁移至 :9622）"
else
    记录 "⚪ :8000 已废弃（主引擎 → :9622 CNSH-64）"
fi

# ── ② 龍魂本地服务 :8765 ──────────────────────────
if ! 检测端口 8765; then
    SERVICE="$HOME/longhun-system/core/longhun_local_service.py"
    if [ -f "$SERVICE" ]; then
        记录 "🔴 :8765 未运行，自动拉起..."
        nohup python3 "$SERVICE" > "$LOG_DIR/服务输出.log" 2>&1 &
        sleep 2
        检测端口 8765 && 记录 "🟢 :8765 龍魂本地服务 · 启动成功" \
                       || 记录 "🟡 :8765 启动中，下次检测再确认"
    else
        记录 "⚪ :8765 longhun_local_service.py 不存在，跳过"
    fi
else
    记录 "🟢 :8765 龍魂本地服务 · 正常"
fi

# ── ③ Ollama :11434 ───────────────────────────────
if ! 检测端口 11434; then
    if command -v ollama &>/dev/null; then
        记录 "🔴 :11434 Ollama 未运行，自动拉起..."
        nohup ollama serve > "$LOG_DIR/ollama输出.log" 2>&1 &
        sleep 2
        检测端口 11434 && 记录 "🟢 :11434 Ollama · 启动成功" \
                         || 记录 "🟡 :11434 Ollama · 启动中"
    else
        记录 "⚪ :11434 Ollama 未安装，跳过"
    fi
else
    记录 "🟢 :11434 Ollama · 正常"
fi

# ── ④ CNSH-64 :9622 ───────────────────────────────
CNSH_CORE="$HOME/longhun-system/cnsh-core"
if 检测端口 9622; then
    记录 "🟢 :9622 CNSH-64 · 正常"
elif [ -d "$CNSH_CORE" ]; then
    记录 "🔴 :9622 CNSH-64 未运行，自动拉起..."
    cd "$CNSH_CORE" && nohup python3 -m uvicorn api.main:app \
        --host 127.0.0.1 --port 9622 --log-level warning \
        > "$LOG_DIR/cnsh9622.log" 2>&1 &
    sleep 2
    检测端口 9622 && 记录 "🟢 :9622 CNSH-64 · 启动成功" \
                   || 记录 "🟡 :9622 CNSH-64 · 启动中"
else
    记录 "⚪ :9622 cnsh-core 目录不存在，跳过"
fi

# ── ⑤ Open WebUI :8080 ───────────────────────────
OPENWEBUI="/Library/Frameworks/Python.framework/Versions/3.11/bin/open-webui"
if ! 检测端口 8080; then
    if [ -f "$OPENWEBUI" ]; then
        记录 "🔴 :8080 Open WebUI 未运行，自动拉起..."
        nohup "$OPENWEBUI" serve > "$LOG_DIR/openwebui输出.log" 2>&1 &
        sleep 3
        检测端口 8080 && 记录 "🟢 :8080 Open WebUI · 启动成功" \
                        || 记录 "🟡 :8080 Open WebUI · 启动中（需约30秒）"
    else
        记录 "⚪ :8080 open-webui 未找到，跳过"
    fi
else
    记录 "🟢 :8080 Open WebUI · 正常"
fi

# ── ⑥ 系统负载自适应诊断 ─────────────────────────
# macOS: loadavg 格式 "{ 1.23 2.34 3.45 }"
LOAD=$(sysctl -n vm.loadavg 2>/dev/null | awk '{print $2}' | cut -d. -f1)
CPU_COUNT=$(sysctl -n hw.ncpu 2>/dev/null || echo 4)
THRESHOLD=$((CPU_COUNT * 2))   # 超过 CPU核数×2 才报警

if [ -n "$LOAD" ] && [ "$LOAD" -gt "$THRESHOLD" ] 2>/dev/null; then
    记录 "⚠️  系统负载偏高 (load=$LOAD, 阈值=$THRESHOLD)"

    # 找出前3个高CPU进程
    TOP_PROCS=$(ps -Ao pid,pcpu,comm --sort=-pcpu 2>/dev/null \
        | grep -v -E "^(PID|  PID)" | head -3)
    记录 "   高CPU进程: $TOP_PROCS"

    # 磁盘空间检查
    DISK_USE=$(df -h "$HOME" 2>/dev/null | awk 'NR==2{print $5}' | tr -d '%')
    if [ -n "$DISK_USE" ] && [ "$DISK_USE" -gt 90 ] 2>/dev/null; then
        记录 "🔴 磁盘空间不足 (已用 $DISK_USE%) → 需要清理"
        通知 "磁盘空间告警" "已用 ${DISK_USE}%，请及时清理"
    fi

    # 负载持续过高 → 推通知让老大知道（但不自动杀进程）
    通知 "系统负载偏高" "load=${LOAD}，核数=${CPU_COUNT}，查 logs/health.log"
else
    if [ -n "$LOAD" ]; then
        记录 "🟢 系统负载正常 (load=$LOAD)"
    fi
fi

# ── ⑦ 磁盘空间日常检查 ───────────────────────────
DISK_USE=$(df -h "$HOME" 2>/dev/null | awk 'NR==2{print $5}' | tr -d '%')
if [ -n "$DISK_USE" ]; then
    if [ "$DISK_USE" -gt 90 ] 2>/dev/null; then
        记录 "🔴 磁盘 ${DISK_USE}% — 危险"
    elif [ "$DISK_USE" -gt 80 ] 2>/dev/null; then
        记录 "🟡 磁盘 ${DISK_USE}% — 偏高"
    else
        记录 "🟢 磁盘 ${DISK_USE}% — 正常"
    fi
fi

# ── ⑧ 日志自动归档（超过20MB就截断保留最后500行）──
for LOGFILE in "$LOG_DIR/engine输出.log" "$LOG_DIR/服务输出.log" \
               "$LOG_DIR/openwebui输出.log" "$LOG_DIR/ollama输出.log"; do
    if [ -f "$LOGFILE" ]; then
        SIZE=$(du -k "$LOGFILE" 2>/dev/null | cut -f1)
        if [ -n "$SIZE" ] && [ "$SIZE" -gt 20480 ] 2>/dev/null; then
            tail -500 "$LOGFILE" > "${LOGFILE}.tmp" && mv "${LOGFILE}.tmp" "$LOGFILE"
            记录 "🗜️  $(basename $LOGFILE) 已自动截断（保留最后500行）"
        fi
    fi
done

记录 "✅ 检测完成 · DNA: #龍芯⚡️$(date +%Y%m%d%H%M%S)-HEALTH"
