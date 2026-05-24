#!/usr/bin/env bash
set -euo pipefail

# 用法:
#   cp deploy/cloudflared/config.example.yml deploy/cloudflared/config.yml
#   # 编辑 config.yml 填 tunnel id / credentials / hostname
#   bash deploy/cloudflared/start_tunnel.sh

ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
CONFIG_FILE="$ROOT_DIR/deploy/cloudflared/config.yml"

if ! command -v cloudflared >/dev/null 2>&1; then
  echo "缺少 cloudflared，请先安装。"
  echo "macOS: brew install cloudflared"
  exit 1
fi

if [[ ! -f "$CONFIG_FILE" ]]; then
  echo "没找到 $CONFIG_FILE"
  echo "先执行:"
  echo "  cp deploy/cloudflared/config.example.yml deploy/cloudflared/config.yml"
  echo "再把 tunnel/hostname 改成你的真实值。"
  exit 1
fi

echo "启动 cloudflared tunnel..."
echo "配置文件: $CONFIG_FILE"
exec cloudflared tunnel --config "$CONFIG_FILE" run
