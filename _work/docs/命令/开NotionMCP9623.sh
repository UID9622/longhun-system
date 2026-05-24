#!/usr/bin/env bash
# Notion MCP · 本机 9623（给 Notion 工作区 AI 调本地工具）
# DNA: #龍芯⚡️2026-05-17-NOTION-MCP-9623-v1.0
set -euo pipefail

ROOT="/Users/zuimeidedeyihan/longhun-system"
cd "$ROOT"

for f in "$ROOT/engine/.env" "$ROOT/.env"; do
  if [[ -f "$f" ]]; then
    set -a
    # shellcheck disable=SC1090
    source "$f"
    set +a
    break
  fi
done

if [[ -z "${NOTION_TOKEN:-}" ]]; then
  echo "🔴 还没填 NOTION_TOKEN"
  echo "   先跑: bash $ROOT/bin/帮你打开密钥填写"
  echo "   在 engine/.env 里写: NOTION_TOKEN=ntn_你的内部集成令牌"
  exit 1
fi

if lsof -i :9623 -sTCP:LISTEN -t >/dev/null 2>&1; then
  echo "🟡 9623 已在监听，不重复启动"
  lsof -i :9623 -sTCP:LISTEN | head -3
  echo ""
  echo "本机地址（Notion 里填这个，不是 /sse）:"
  echo "  http://127.0.0.1:9623/mcp"
  echo "健康检查: http://127.0.0.1:9623/health"
  exit 0
fi

export NOTION_TOKEN
echo "════════════════════════════════════════"
echo "  🐉 龍魂 Notion MCP · :9623"
echo "════════════════════════════════════════"
echo "  本机: http://127.0.0.1:9623/mcp"
echo "  健康: http://127.0.0.1:9623/health"
echo "  外网: 另开终端跑 cloudflared（见说明）"
echo "  停服: kill \$(lsof -t -i:9623)"
echo "════════════════════════════════════════"
exec npx -y @notionhq/notion-mcp-server --transport http --port 9623 --disable-auth
