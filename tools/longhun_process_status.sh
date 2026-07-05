#!/usr/bin/env bash
# 龍魂核心進程精聽腳本
# DNA: #龍芯⚡️2026-07-04-LONGHUN-PROCESS-STATUS-v1.0

set -uo pipefail

echo "🐉 龍魂核心進程精聽 · $(date)"
echo ""

# launchd 託管服務
echo "【LaunchAgent 託管】"
for svc in com.uid9622.longhun888-services com.uid9622.longhun.autostart com.longhun.portal com.longhun.capability-web com.longhun.kg-api com.longhun.gua-audit com.longhun.heart-talk; do
  line=$(launchctl list | awk -v s="$svc" '$3 == s {print}')
  if [ -n "$line" ]; then
    st=$(echo "$line" | awk '{print $2}')
    echo "  $svc : 狀態碼 $st"
  else
    echo "  $svc : 未加載"
  fi
done

echo ""
echo "【端口監聽】"
for port in 18000 8777 18100 9622 9623 8766 8844 8088 9624 9625 11434; do
  pid=$(lsof -Pi :$port -sTCP:LISTEN -t 2>/dev/null | head -1)
  if [ -n "$pid" ]; then
    cmd=$(ps -p $pid -o comm= 2>/dev/null | head -c 45)
    echo "  :$port ✅ PID $pid ($cmd)"
  else
    echo "  :$port 🔴 未監聽"
  fi
done

echo ""
echo "【Cloudflare Tunnel】"
if pgrep -f "cloudflared tunnel --config.*longhun888.yml" >/dev/null 2>&1; then
  echo "  longhun888 tunnel ✅ 運行中"
else
  echo "  longhun888 tunnel 🔴 未運行"
fi

echo ""
echo "【常用控制命令】"
echo "  重啟 longhun888 套件：launchctl unload ~/Library/LaunchAgents/com.uid9622.longhun888-services.plist && launchctl load ~/Library/LaunchAgents/com.uid9622.longhun888-services.plist"
echo "  手動啟動：bash ~/longhun-system/tools/start_longhun888_services.sh start"
echo "  查看狀態：bash ~/longhun-system/tools/start_longhun888_services.sh status"
