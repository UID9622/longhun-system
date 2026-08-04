#!/bin/bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# DNA: #龍芯⚡️丙午·乙未·乙丑·泰-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/bin/bash
# 龍魂 · 监管审计系列17篇 本地站启动脚本 (命名隧道版)
# 用法: bash start.sh
# 公开地址: https://docs.longhun888.com  (独立隧道 longhun-docs，不碰主站 longhun888.com)
set -e
D="/Users/zuimeidedeyihan/longhun-system/docs/监管审计系列17篇"
PORT=8080

echo "🐉 启动本地文档服务器 (目录: $D)..."
python3 -m http.server "$PORT" --directory "$D" > /tmp/longhun_docs_8080.log 2>&1 &
echo $! > /tmp/longhun_docs_8080.pid
sleep 1
curl -s -o /dev/null -w "✅ 本地: http://localhost:$PORT (HTTP %{http_code})\n" "http://localhost:$PORT/"

echo "🚀 启动 Cloudflare 命名隧道 longhun-docs → docs.longhun888.com ..."
cloudflared tunnel --config ~/.cloudflared/longhun-docs.yml run longhun-docs > /tmp/longhun_docs_tunnel.log 2>&1 &
echo $! > /tmp/longhun_docs_tunnel.pid
sleep 3
echo "✅ 公开站: https://docs.longhun888.com"
echo ""
echo "📌 注意: 站当前跑在本机，本机休眠/关机则站下。要7x24需迁华为鲲鹏。"
echo "关闭: bash $D/stop.sh"
