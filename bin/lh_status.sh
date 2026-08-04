#!/usr/bin/env bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂系统运行状态一览
# DNA:#龍芯⚡️2026-06-17-LONGHUN-STATUS-FILE1-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

cd "$(dirname "$0")/.."
ROOT="$(pwd)"

echo "═══════════════════════════════════════════════════"
echo "  🐉 龍魂系统运行状态"
echo "═══════════════════════════════════════════════════"
echo "  项目根目录: $ROOT"
echo "  当前时间: $(date)"
echo ""

status_port() {
    local port=$1 name=$2
    if lsof -ti:"$port" >/dev/null 2>&1; then
        echo "  ✅ $name (port $port): 运行中"
    else
        echo "  ⏹️  $name (port $port): 未启动"
    fi
}

status_port 9622 "龍魂操作台"
status_port 9001 "Persona API"
status_port 8001 "监控服务"

echo ""
if [ -f ~/Library/LaunchAgents/com.uid9622.longhun.autostart.plist ]; then
    if launchctl list | grep -q com.uid9622.longhun.autostart; then
        echo "  ✅ 开机自启动: 已安装并载入"
    else
        echo "  ⚠️  开机自启动: 已安装但未载入"
    fi
else
    echo "  ⏹️  开机自启动: 未安装"
fi

echo ""
echo "  最近日志:"
for f in autostart.log control-panel.log cnsh-autostart.log daily-audit.log; do
    if [ -f "logs/$f" ]; then
        echo "    - logs/$f ($(stat -f%Sm -t '%Y-%m-%d %H:%M' logs/$f))"
    fi
done

echo ""
echo "═══════════════════════════════════════════════════"
