#!/usr/bin/env bash
# 🐉 龍魂 · 鲲鹏 MCP Server 一键部署脚本 v1.0
# DNA: #龍芯⚡️2026-09-04-LONGHUN-KUNPENG-MCP-DEPLOY-v1.0-UID9622
# 创建者: 诸葛鑫（UID9622） · 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2
# 用法: bash deploy/longhun-mcp/deploy_to_kunpeng.sh [--admin-on]
#   --admin-on  同时 enable 高危层(8767·默认仅本机127.0.0.1)
# 端口裁决 2026-09-04: 原 8765 被鲲鹏 longhun-cal(cal_server) 占用 → admin 换 8767
# 前置: ~/.ssh/longhun_kunpeng_ed25519 · 鲲鹏 root@119.13.90.27

set -euo pipefail

LH_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
SRC="${LH_ROOT}/deploy/longhun-mcp"
KUNPENG=root@119.13.90.27
SSH_KEY=~/.ssh/longhun_kunpeng_ed25519
REMOTE=/opt/longhun-system/deploy/longhun-mcp
ADMIN_ON=0
[[ "${1:-}" == "--admin-on" ]] && ADMIN_ON=1

echo "🐉 鲲鹏 MCP Server 部署 → ${KUNPENG}"
echo "  源: ${SRC}"

# 1. rsync 源码（含 config/systemd；排除 *.asc 避免覆盖远端签名）
ssh -i "$SSH_KEY" "$KUNPENG" "mkdir -p ${REMOTE} /var/log/longhun-mcp"
rsync -az --delete \
  -e "ssh -i $SSH_KEY" \
  --exclude '*.asc' \
  "${SRC}/" "${KUNPENG}:${REMOTE}/"

# 2. 安装 systemd 单元
ssh -i "$SSH_KEY" "$KUNPENG" "
  set -e
  for u in readonly audit admin; do
    cp ${REMOTE}/systemd/lh-mcp-\${u}.service /etc/systemd/system/
  done
  systemctl daemon-reload
"

# 3. 启动只读/审计（安全区常开）
ssh -i "$SSH_KEY" "$KUNPENG" "
  systemctl enable lh-mcp-readonly lh-mcp-audit 2>/dev/null || true
  systemctl restart lh-mcp-readonly lh-mcp-audit
"

# 4. 高危层：默认 disabled，仅显式 --admin-on
if [[ $ADMIN_ON -eq 1 ]]; then
  ssh -i "$SSH_KEY" "$KUNPENG" "systemctl enable lh-mcp-admin 2>/dev/null || true; systemctl restart lh-mcp-admin"
  echo "⚠️  高危层已启动(127.0.0.1:8767·白名单受限)"
else
  ssh -i "$SSH_KEY" "$KUNPENG" "systemctl disable lh-mcp-admin 2>/dev/null || true; systemctl stop lh-mcp-admin 2>/dev/null || true"
  echo "ℹ️  高危层保持 disabled（需时: systemctl enable --now lh-mcp-admin）"
fi

# 5. 远端健康自检（在鲲鹏内 curl localhost）
echo "── 健康自检 ──"
ssh -i "$SSH_KEY" "$KUNPENG" "
  for port in 8763 8764 8767; do
    body=\$(curl -s -m 3 -o /dev/null -w '%{http_code}' \\
      -H 'Accept: application/json' \\
      -H 'Content-Type: application/json' \\
      --data '{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"ping\"}' \\
      http://127.0.0.1:\${port}/mcp 2>/dev/null || echo 000)
    case \$body in
      200|204) echo \"  ✅ :\${port} MCP ping OK\" ;;
      000)     echo \"  🟡 :\${port} 未监听(admin 默认 disabled 属正常)\" ;;
      *)       echo \"  🟡 :\${port} HTTP \$body\" ;;
    esac
  done
"
echo "✅ 部署完成。接入指南: docs/鲲鹏MCP接入指南-v1.0.md"
