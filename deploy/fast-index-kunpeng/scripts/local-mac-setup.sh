#!/bin/bash
# 🐉 龍魂 · 快速索引底座 · Mac 本地命令封装
# DNA: #龍芯⚡️丙午·丙申·壬戌·乙巳·䷾既济-FAST-INDEX-MAC-SETUP-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

set -e

KUNPENG_IP=${1:-}
if [[ -z "$KUNPENG_IP" ]]; then
    echo "用法: $0 <鲲鹏IP>"
    exit 1
fi

LONGHUN_DIR="$HOME/.longhun"
mkdir -p "$LONGHUN_DIR/bin" "$LONGHUN_DIR/scripts" "$LONGHUN_DIR/configs"

# 写入 tunnel 脚本
cat > "$LONGHUN_DIR/scripts/fast-index-tunnel.sh" << EOF
#!/bin/bash
# SSH 隧道到鲲鹏快速索引服务
ssh -N -L 8768:127.0.0.1:8768 -L 11434:127.0.0.1:11434 root@$KUNPENG_IP
EOF
chmod +x "$LONGHUN_DIR/scripts/fast-index-tunnel.sh"

# 写入 lh fast-index 代理脚本
cat > "$LONGHUN_DIR/bin/lh-fast-index" << 'EOF'
#!/bin/bash
# lh fast-index 命令代理
CMD=$1
shift || true

case "$CMD" in
    tunnel)
        echo "🔄 建立 SSH 隧道..."
        exec "$HOME/.longhun/scripts/fast-index-tunnel.sh"
        ;;
    open)
        echo "🌐 打开快速索引服务..."
        open http://127.0.0.1:8768
        ;;
    index)
        curl -s -X POST http://127.0.0.1:8768/index -H "Content-Type: application/json" -d "{}"
        echo ""
        ;;
    search)
        QUERY="$*"
        curl -s "http://127.0.0.1:8768/search?q=$(printf '%s' "$QUERY" | python3 -c 'import urllib.parse,sys; print(urllib.parse.quote(sys.stdin.read()))')"
        echo ""
        ;;
    push)
        curl -s http://127.0.0.1:8768/push
        echo ""
        ;;
    stats)
        curl -s http://127.0.0.1:8768/stats
        echo ""
        ;;
    *)
        echo "用法: lh fast-index [tunnel|open|index|search <query>|push|stats]"
        ;;
esac
EOF
chmod +x "$LONGHUN_DIR/bin/lh-fast-index"

# 添加到 PATH（如果尚未添加）
if ! grep -q "$LONGHUN_DIR/bin" "$HOME/.zshrc" 2>/dev/null && ! grep -q "$LONGHUN_DIR/bin" "$HOME/.bashrc" 2>/dev/null; then
    echo "export PATH=\"$LONGHUN_DIR/bin:\$PATH\"" >> "$HOME/.zshrc"
    echo "✅ 已添加 $LONGHUN_DIR/bin 到 PATH（zsh）"
fi

echo "✅ Mac 本地命令封装完成"
echo "   用法: lh fast-index tunnel    # 建立隧道"
echo "         lh fast-index open      # 打开服务"
echo "         lh fast-index search 主权网关"
echo ""
echo "⚠️  请重新加载 shell 或执行: export PATH=\"$LONGHUN_DIR/bin:\$PATH\""
