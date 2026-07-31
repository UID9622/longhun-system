#!/usr/bin/env bash
# 🐉 龍魂系统开机自启动脚本 v3.1
# 统一启动常驻服务 + 认知压缩 + 分层治理自愈
# 已集成反熔断守卫：过载检查 → 执行 → 输出契约校验 → 审计日志
#
# DNA:#龍芯⚡️2026-06-25-LONGHUN-AUTOSTART-v3.1
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

set -e

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
export PYTHONPATH="$ROOT${PYTHONPATH:+:$PYTHONPATH}"
LOG_DIR="$ROOT/logs"
mkdir -p "$LOG_DIR"

LOG_FILE="$LOG_DIR/autostart.log"
GUARD="python3 $ROOT/personas/runtime/anti_blowout_guard.py --json"

echo "🐉 龍魂系统开机自启动 · $(date)" >> "$LOG_FILE"

# 1) 启动核心服务
$GUARD --op deploy --evidence '{"artifact_path":"bin/longhun-launcher.py","mode":"autostart"}' -- python3 "$ROOT/bin/longhun-launcher.py" start --autostart >> "$LOG_FILE" 2>&1 || true

# 2) 自动压缩技能
$GUARD --op compress --evidence '{"artifact_path":"scripts/longhun_compression_engine.py"}' -- python3 "$ROOT/scripts/longhun_compression_engine.py" --compress-all-skills >> "$LOG_FILE" 2>&1 || true

# 3) 分层治理自愈
$GUARD --op audit --evidence '{"artifact_path":"bin/longhun-governance.py"}' -- python3 "$ROOT/bin/longhun-governance.py" heal --json >> "$LOG_DIR/governance-autostart.json" 2>&1 || true

# 4) 生成状态看板快照
$GUARD --op check --evidence '{"artifact_path":"bin/longhun-status.py"}' -- python3 "$ROOT/bin/longhun-status.py" >> "$LOG_DIR/autostart-status.log" 2>&1 || true

# 5) 每日复盘
$GUARD --op daily_review --evidence '{"artifact_path":"daily_review.py"}' -- python3 "$ROOT/daily_review.py" >> "$LOG_FILE" 2>&1 || true

# 6) 启动龍魂移动端监控常驻守护进程
MONITORING_DAEMON="$HOME/.龍魂/monitoring/daemon.sh"
if [ -f "$MONITORING_DAEMON" ]; then
    $GUARD --op monitoring --evidence "{\"artifact_path\":\"$MONITORING_DAEMON\",\"mode\":\"autostart\"}" -- bash "$MONITORING_DAEMON" start >> "$LOG_FILE" 2>&1 || true
else
    echo "⚠️  移动端监控守护进程未安装: $MONITORING_DAEMON" >> "$LOG_FILE"
fi

# 7) 启动龍魂·主动观察记录协议（若 30 分钟内未扫描）
OBSERVER_HOOK="$HOME/.龍魂/observer/hooks/session-start.sh"
if [ -f "$OBSERVER_HOOK" ]; then
    $GUARD --op observer --evidence "{\"artifact_path\":\"$OBSERVER_HOOK\",\"mode\":\"autostart\"}" -- bash "$OBSERVER_HOOK" >> "$LOG_FILE" 2>&1 || true
else
    echo "⚠️  主动观察协议未安装: $OBSERVER_HOOK" >> "$LOG_FILE"
fi

# 8) 启动老百姓维权助手 + 本地法律引擎
RIGHTS_ASSISTANT="$ROOT/人民维权助手/启动维权助手.sh"
LEGAL_ENGINE="$ROOT/法律引擎/启动法律引擎.sh"
if [ -f "$RIGHTS_ASSISTANT" ]; then
    bash "$RIGHTS_ASSISTANT" >> "$LOG_FILE" 2>&1 || true
    echo "✅ 维权助手已启动" >> "$LOG_FILE"
else
    echo "⚠️ 维权助手启动脚本未找到: $RIGHTS_ASSISTANT" >> "$LOG_FILE"
fi
if [ -f "$LEGAL_ENGINE" ]; then
    bash "$LEGAL_ENGINE" >> "$LOG_FILE" 2>&1 || true
    echo "✅ 本地法律引擎已启动" >> "$LOG_FILE"
else
    echo "⚠️ 本地法律引擎启动脚本未找到: $LEGAL_ENGINE" >> "$LOG_FILE"
fi

# 9) 启动龍魂核心服务（Phase3 / 宝宝守护 / 操作台）
CORE_SERVICES="$HOME/.龍魂/services/service-manager.sh"
if [ -f "$CORE_SERVICES" ]; then
    $GUARD --op autostart --evidence "{\"artifact_path\":\"$CORE_SERVICES\",\"mode\":\"core-services\"}" -- bash "$CORE_SERVICES" start >> "$LOG_FILE" 2>&1 || true
else
    echo "⚠️  核心服务管理器未安装: $CORE_SERVICES" >> "$LOG_FILE"
fi

# 10) 启动 longhun888.com 门户相关服务（CNSH Editor API :18000 + 门户服务器 :8777 + Cloudflare Tunnel）
PORTAL_FIX="$ROOT/tools/补全服务.sh"
if [ -f "$PORTAL_FIX" ]; then
    echo "▶ 启动 longhun888.com 门户服务" >> "$LOG_FILE"
    bash "$PORTAL_FIX" >> "$LOG_FILE" 2>&1 || true
else
    echo "⚠️  门户补全脚本未找到: $PORTAL_FIX" >> "$LOG_FILE"
fi

# 11) 启动龍魂 v10.0 API 演示服务器（端口 18100）
V10_API_SERVER="$ROOT/notion_absorb/v10_api_skill/longhun_v10_api_server.py"
if [ -f "$V10_API_SERVER" ]; then
    echo "▶ 启动龍魂 v10.0 API 服务器" >> "$LOG_FILE"
    pkill -f "longhun_v10_api_server.py" 2>/dev/null || true
    sleep 1
    PY3="/opt/homebrew/bin/python3.12"
    if [ ! -x "$PY3" ]; then
        PY3="python3"
    fi
    nohup "$PY3" "$V10_API_SERVER" >> "$LOG_DIR/longhun_v10_api_server.out.log" 2>&1 &
    sleep 2
    if lsof -Pi :18100 -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo "✅ 龍魂 v10.0 API 服务器已启动（:18100）" >> "$LOG_FILE"
    else
        echo "🔴 龍魂 v10.0 API 服务器启动失败" >> "$LOG_FILE"
    fi
else
    echo "⚠️  龍魂 v10.0 API 服务器未找到: $V10_API_SERVER" >> "$LOG_FILE"
fi

# 12) 启动龍魂共生体知识矩阵服务器（端口 9627）
SYMBIOTE_SERVER="$ROOT/tools/longhun_symbiote_server.py"
if [ -f "$SYMBIOTE_SERVER" ]; then
    echo "▶ 启动龍魂共生体知识矩阵服务器" >> "$LOG_FILE"
    /usr/sbin/lsof -ti:9627 2>/dev/null | xargs kill -9 2>/dev/null || true
    sleep 1
    nohup /usr/bin/python3 "$SYMBIOTE_SERVER" >> "$LOG_DIR/symbiote_server.log" 2>&1 &
    sleep 2
    if lsof -Pi :9627 -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo "✅ 龍魂共生体知识矩阵已启动（:9627）" >> "$LOG_FILE"
    else
        echo "🔴 龍魂共生体知识矩阵启动失败" >> "$LOG_FILE"
    fi
else
    echo "⚠️  龍魂共生体服务器未找到: $SYMBIOTE_SERVER" >> "$LOG_FILE"
fi

# 13) 启动龍智守飞书机器人服务（端口 5001）
LONGZHISHOU_START="$ROOT/bin/start_longzhishou.sh"
if [ -f "$LONGZHISHOU_START" ]; then
    echo "▶ 启动龍智守飞书机器人" >> "$LOG_FILE"
    bash "$LONGZHISHOU_START" >> "$LOG_FILE" 2>&1 || true
else
    echo "⚠️  龍智守启动脚本未找到: $LONGZHISHOU_START" >> "$LOG_FILE"
fi

echo "✅ 开机自启动流程结束 · $(date)" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"
