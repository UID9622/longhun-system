#!/data/data/com.termux/files/usr/bin/bash
# 龍魂 · Termux 安卓自動版環境初始化
# DNA: #龍芯⚡️2026-06-16-LONGHUN-ANDROID-AUTO-v1.0

set -e

echo "🐉 龍魂 Termux 安卓自動版初始化"
echo "================================"

# 安裝基礎依賴
pkg update -y
pkg install -y python git curl termux-api

# 創建工作目錄
mkdir -p ~/longhun-android

# 下載龍魂安卓客戶端
cat > ~/longhun-android/longhun-client.sh <<'EOF'
#!/data/data/com.termux/files/usr/bin/bash
# 龍魂安卓客戶端 · 定時輪詢操作台 API
BASE="${LONGHUN_BASE:-http://127.0.0.1:9622}"
INTERVAL="${LONGHUN_INTERVAL:-60}"
LOG="~/longhun-android/client.log"

echo "🐉 龍魂安卓客戶端啟動"
echo "BASE: $BASE"
echo "輪詢間隔: ${INTERVAL}s"

while true; do
  TS=$(date '+%Y-%m-%d %H:%M:%S')
  HEALTH=$(curl -s "$BASE/api/health" || echo '{"status":"offline"}')
  echo "[$TS] health: $HEALTH" >> "$LOG"

  # 每 5 次輪詢執行一次 mcp-skill 工作流自檢
  if [ $(($(date +%s) / INTERVAL % 5)) -eq 0 ]; then
    echo "[$TS] 執行自檢工作流 mcp-skill" >> "$LOG"
    curl -s -X POST "$BASE/api/workflows/mcp-skill/run" \
      -H "Content-Type: application/json" -d '{}' >> "$LOG" 2>&1
    echo "" >> "$LOG"
  fi

  sleep "$INTERVAL"
done
EOF

chmod +x ~/longhun-android/longhun-client.sh

# 創建啟動快捷
cat > ~/longhun-android/start.sh <<'EOF'
#!/data/data/com.termux/files/usr/bin/bash
nohup bash ~/longhun-android/longhun-client.sh > /dev/null 2>&1 &
echo "✅ 龍魂安卓客戶端已後台啟動"
EOF
chmod +x ~/longhun-android/start.sh

echo ""
echo "✅ 初始化完成"
echo "啟動命令: bash ~/longhun-android/start.sh"
echo "查看日誌: tail -f ~/longhun-android/client.log"
