#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════
# M75 渲染引擎部署脚本 · 本机 / 鲲鹏 双模式
# DNA: #龍芯⚡️2026-08-25-RENDER-DEPLOY-v1.0-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 用法: bash deploy_render.sh [local|kunpeng]
#   本机: 后台启动 lh render server (127.0.0.1:8788 · 8972 已被 flow-field-api 占用)
#   鲲鹏: rsync → docker compose build → up → 健康检查
# ═══════════════════════════════════════════════════════════════
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
MODE="${1:-kunpeng}"
SSH_KEY="${SSH_KEY:-$HOME/.ssh/longhun_kunpeng_ed25519}"
HOST="root@119.13.90.27"
REMOTE_BASE="/opt/longhun"
RENDER_REMOTE="$REMOTE_BASE/render"

kunpeng() {
  echo "==> [1/4] rsync render/ → $HOST:$RENDER_REMOTE"
  ssh -i "$SSH_KEY" "$HOST" "mkdir -p $RENDER_REMOTE/data/renders $RENDER_REMOTE/templates"
  rsync -az --delete \
    --exclude '__pycache__' --exclude '*.pyc' --exclude '*.asc' \
    --exclude '.git' --exclude 'tests' --exclude 'logs' \
    -e "ssh -i $SSH_KEY" \
    "$ROOT/render/" "$HOST:$RENDER_REMOTE/"

  echo "==> [2/4] rsync docker-compose.render.yml"
  rsync -az -e "ssh -i $SSH_KEY" \
    "$ROOT/render/docker-compose.render.yml" "$HOST:$REMOTE_BASE/docker-compose.render.yml"

  echo "==> [3/4] docker compose build & up (ARM64·2核·耐心等)"
  ssh -i "$SSH_KEY" "$HOST" \
    "cd $REMOTE_BASE && docker compose -f docker-compose.render.yml build lh-render 2>&1 | tail -5 && docker compose -f docker-compose.render.yml up -d lh-render 2>&1 | tail -5"

  echo "==> [4/4] 健康检查"
  sleep 8
  ssh -i "$SSH_KEY" "$HOST" \
    "curl -s --max-time 10 http://127.0.0.1:8788/render/health || echo '健康检查失败：容器可能还在启动'" || true
}

local_start() {
  echo "==> 本机模式"
  if lsof -i :8788 -P -n >/dev/null 2>&1; then
    echo "  渲染服务已在运行 (127.0.0.1:8788)"
    curl -s --max-time 5 http://127.0.0.1:8788/render/health
  else
    cd "$ROOT" && nohup python3 08_BIN/lh_render.py server > logs/render_server.log 2>&1 &
    echo "  已后台启动 PID=$!"
    sleep 3
    curl -s --max-time 5 http://127.0.0.1:8788/render/health
  fi
}

case "$MODE" in
  local)   local_start ;;
  kunpeng) kunpeng ;;
  *) echo "用法: bash deploy_render.sh [local|kunpeng]"; exit 1 ;;
esac
echo ""
echo "==> 部署完成 🟢"
