#!/data/data/com.termux/files/usr/bin/bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂 · Termux 安卓自动版环境初始化
# DNA:#龍芯⚡️2026-06-16-LONGHUN-ANDROID-AUTO-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

set -e

echo "🐉 龍魂 Termux 安卓自动版初始化"
echo "================================"

# 安装基础依赖
pkg update -y
pkg install -y python git curl termux-api

# 创建工作目录
mkdir -p ~/longhun-android

# 下载龍魂安卓客户端
cat > ~/longhun-android/longhun-client.sh <<'EOF'
#!/data/data/com.termux/files/usr/bin/bash
# 龍魂安卓客户端 · 定时轮询操作台 API
BASE="${LONGHUN_BASE:-http://127.0.0.1:9622}"
INTERVAL="${LONGHUN_INTERVAL:-60}"
LOG="~/longhun-android/client.log"

echo "🐉 龍魂安卓客户端启动"
echo "BASE: $BASE"
echo "轮询间隔: ${INTERVAL}s"

while true; do
  TS=$(date '+%Y-%m-%d %H:%M:%S')
  HEALTH=$(curl -s "$BASE/api/health" || echo '{"status":"offline"}')
  echo "[$TS] health: $HEALTH" >> "$LOG"

  # 每 5 次轮询执行一次 mcp-skill 工作流自检
  if [ $(($(date +%s) / INTERVAL % 5)) -eq 0 ]; then
    echo "[$TS] 执行自检工作流 mcp-skill" >> "$LOG"
    curl -s -X POST "$BASE/api/workflows/mcp-skill/run" \
      -H "Content-Type: application/json" -d '{}' >> "$LOG" 2>&1
    echo "" >> "$LOG"
  fi

  sleep "$INTERVAL"
done
EOF

chmod +x ~/longhun-android/longhun-client.sh

# 创建启动快捷
cat > ~/longhun-android/start.sh <<'EOF'
#!/data/data/com.termux/files/usr/bin/bash
nohup bash ~/longhun-android/longhun-client.sh > /dev/null 2>&1 &
echo "✅ 龍魂安卓客户端已后台启动"
EOF
chmod +x ~/longhun-android/start.sh

echo ""
echo "✅ 初始化完成"
echo "启动命令: bash ~/longhun-android/start.sh"
echo "查看日志: tail -f ~/longhun-android/client.log"
