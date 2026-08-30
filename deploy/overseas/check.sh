#!/usr/bin/env bash
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# ═══════════════════════════════════════════════════════════
# 龍魂海外节点 · 健康检查 v1.0
# DNA: #龍芯⚡️丙午·丙申·壬申·亥时·䷕贲-OVERSEAS-CHECK-v1.0-9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 用法: bash check.sh [--bark]
# ═══════════════════════════════════════════════════════════
set -uo pipefail

HOST="${HOST:-127.0.0.1}"
PORT="${GATEWAY_PORT:-8788}"
URL="http://$HOST:$PORT/health"
BARK_KEY="${BARK_KEY:-}"

echo "== 龍魂海外节点健康检查 =="

if curl -sf --max-time 8 "$URL" > /tmp/lh-overseas-health.json 2>/dev/null; then
  echo "✅ AI 网关正常: $URL"
  python3 -m json.tool /tmp/lh-overseas-health.json 2>/dev/null | grep -E '"(status|node|openai|claude|gemini)"' | head -6
  STATUS="ok"
else
  echo "🔴 AI 网关异常: $URL"
  STATUS="down"
fi

# 可选 Bark 推送
if [ -n "$BARK_KEY" ] && [ -n "$STATUS" ]; then
  TITLE="龍魂海外节点 $STATUS"
  MSG="AI网关 $URL → $STATUS"
  curl -sf -X POST "https://api.day.app/$BARK_KEY/$TITLE/$MSG" >/dev/null 2>&1 && echo "📱 Bark 已推送" || echo "ℹ️ Bark 推送失败(无网络/无key)"
fi

[ "$STATUS" = "ok" ] && exit 0 || exit 1
