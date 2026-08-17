#!/bin/bash
# 龍魂·lh 命令扩展 (portal 子命令)
# DNA: #龍芯⚡️丙午·甲申·丁未·离为火-lh扩展-v1.0
# 用法: lh portal <start|stop|sync|deploy|status>

set -euo pipefail

LONGHUN_DIR="${LONGHUN_DIR:-$HOME/.longhun}"
PORTAL_DIR="${LONGHUN_DIR}/portal"
SERVER_IP="${SERVER_IP:-119.13.90.27}"
SSH_KEY="${SSH_KEY:-$HOME/.ssh/longhun_kunpeng_ed25519}"

cmd="${1:-help}"
shift || true

case "$cmd" in
    start)
        echo "🐉 启动本地门户..."
        bash "$PORTAL_DIR/scripts/deploy-local.sh"
        ;;
    stop)
        echo "🐉 停止本地门户..."
        [[ -f /tmp/longhun-portal.pid ]] && kill $(cat /tmp/longhun-portal.pid) 2>/dev/null || true
        echo "已停止"
        ;;
    sync)
        echo "🐉 同步到服务器..."
        SERVER_IP=$SERVER_IP bash "$PORTAL_DIR/scripts/sync-to-server.sh"
        ;;
    deploy)
        echo "🐉 部署到服务器..."
        scp -i "$SSH_KEY" -r "$PORTAL_DIR/portal" "$PORTAL_DIR/scripts" root@$SERVER_IP:/root/longhun-portal-deploy/
        ssh -i "$SSH_KEY" root@$SERVER_IP "bash /root/longhun-portal-deploy/scripts/deploy-server.sh"
        ;;
    status)
        echo "🐉 本地状态:"
        if [[ -f /tmp/longhun-portal.pid ]] && kill -0 $(cat /tmp/longhun-portal.pid) 2>/dev/null; then
            echo "  本地服务: 运行中 (PID: $(cat /tmp/longhun-portal.pid))"
        else
            echo "  本地服务: 未运行"
        fi
        echo "  本地地址: http://localhost:8899"
        echo "  三入口:"
        echo "    普通者:   http://localhost:8899/index.html"
        echo "    无障碍:   http://localhost:8899/accessible.html"
        echo "    开发者:   http://localhost:8899/developer.html"
        ;;
    help|--help|-h|*)
        echo "🐉 lh portal 命令"
        echo ""
        echo "用法: lh portal <命令>"
        echo ""
        echo "命令:"
        echo "  start    启动本地门户 (localhost:8899)"
        echo "  stop     停止本地门户"
        echo "  sync     同步本地到服务器"
        echo "  deploy   一键部署到服务器 (Nginx + SSL)"
        echo "  status   查看状态"
        echo ""
        echo "环境变量:"
        echo "  SERVER_IP    服务器IP (默认: 119.13.90.27)"
        echo "  SSH_KEY      SSH密钥路径 (默认: ~/.ssh/id_ed25519)"
        ;;
esac
