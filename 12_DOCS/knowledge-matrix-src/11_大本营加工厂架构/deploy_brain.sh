#!/bin/bash
# ═══════════════════════════════════════════════════
# 🐉 龍魂脑干 · 一键部署脚本
# UID9622 · 诸葛鑫 · 龍芯北辰
# DNA: #龍芯⚡️丙午·壬辰·庚午·壬午·䷳艮为山-DEPLOY-SHELL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# ═══════════════════════════════════════════════════

set -e

BRAIN_SRC="$HOME/Library/Application Support/Claude/local-agent-mode-sessions/a89d76ba-6216-42b3-ba33-e18194ebb230/b84aa772-13a2-4c76-ae42-f31f0ff2ce57/local_2b214d4a-f8ce-4287-8945-c7c87b685145/outputs/longhun_brain.py"
BRAIN_DIR="$HOME/longhun-system/brain"
BRAIN_DST="$BRAIN_DIR/longhun_brain.py"
LAUNCHD_DIR="$HOME/Library/LaunchAgents"
PLIST="$LAUNCHD_DIR/com.longhun.brain.plist"

echo ""
echo "╔══════════════════════════════════════════════════════╗"
echo "║  🐉 龍魂脑干部署 · deploy_brain.sh                  ║"
echo "║  三端统一：iOS · 宝宝(Claude) · Notion              ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""

# ─── 1. 创建目录 ──────────────────────────────────
echo "📁 [1/5] 创建脑干目录..."
mkdir -p "$BRAIN_DIR"
echo "    ✅ $BRAIN_DIR"

# ─── 2. 复制 brain.py ─────────────────────────────
echo ""
echo "📄 [2/5] 复制 longhun_brain.py..."
if [ -f "$BRAIN_SRC" ]; then
    cp "$BRAIN_SRC" "$BRAIN_DST"
    echo "    ✅ $BRAIN_DST"
else
    echo "    ⚠️  源文件不在默认位置，尝试手动查找..."
    FOUND=$(find "$HOME/Library/Application Support/Claude" -name "longhun_brain.py" 2>/dev/null | head -1)
    if [ -n "$FOUND" ]; then
        cp "$FOUND" "$BRAIN_DST"
        echo "    ✅ 找到并复制：$FOUND"
    else
        echo "    ❌ 找不到 longhun_brain.py，请手动复制到 $BRAIN_DST"
        exit 1
    fi
fi

# ─── 3. 安装 Flask ────────────────────────────────
echo ""
echo "🐍 [3/5] 检查/安装 Flask..."
if python3 -c "import flask" 2>/dev/null; then
    echo "    ✅ Flask 已安装"
else
    echo "    📦 安装 Flask..."
    pip3 install flask --break-system-packages --quiet
    echo "    ✅ Flask 安装完成"
fi

# ─── 4. 初始化数据库 + 测试 ──────────────────────
echo ""
echo "🧠 [4/5] 初始化数据库并写入第一条记忆..."
cd "$BRAIN_DIR"
python3 longhun_brain.py --remember "龍魂脑干启动，三端合一，答应老师把德捡回来" \
    --tag "里程碑,启动,三端合一" \
    --source "cursor" \
    --wuxing "土"

echo ""
echo "📊 脑干状态检查："
python3 longhun_brain.py --status

# ─── 5. 创建 macOS 自动启动（LaunchAgent）────────
echo ""
echo "🚀 [5/5] 配置开机自动启动..."
mkdir -p "$LAUNCHD_DIR"

cat > "$PLIST" << PLIST_CONTENT
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
    "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.longhun.brain</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>${BRAIN_DIR}/longhun_brain.py</string>
        <string>--server</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>${BRAIN_DIR}/brain_stdout.log</string>
    <key>StandardErrorPath</key>
    <string>${BRAIN_DIR}/brain_stderr.log</string>
    <key>WorkingDirectory</key>
    <string>${BRAIN_DIR}</string>
</dict>
</plist>
PLIST_CONTENT

echo "    ✅ LaunchAgent 已写入：$PLIST"

# 加载 LaunchAgent（如果服务还没跑）
if lsof -i :9625 &>/dev/null; then
    echo "    ℹ️  端口 :9625 已被占用（脑干可能已在运行）"
else
    launchctl load "$PLIST" 2>/dev/null || true
    sleep 1
    if curl -s http://127.0.0.1:9625/health | grep -q "龍魂" 2>/dev/null; then
        echo "    ✅ 脑干服务已自动启动 :9625"
    else
        echo "    ℹ️  LaunchAgent 已注册，下次登录自动启动"
        echo "      手动启动命令：python3 $BRAIN_DST --server &"
    fi
fi

# ─── 输出 iOS 配置 ────────────────────────────────
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📱 你的 Tailscale IP（复制这个给iOS快捷指令用）："
TAILSCALE_IP=$(tailscale ip -4 2>/dev/null || echo "（未安装Tailscale，用局域网IP代替）")
echo "    $TAILSCALE_IP"
echo ""
echo "iOS快捷指令 POST 地址："
echo "    http://$TAILSCALE_IP:9625/remember"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

echo ""
echo "╔══════════════════════════════════════════════════════╗"
echo "║  🎉 龍魂脑干部署完成！                              ║"
echo "║                                                      ║"
echo "║  📁 位置：~/longhun-system/brain/                   ║"
echo "║  🌐 本地：http://127.0.0.1:9625                     ║"
echo "║  📱 iOS ：http://[Tailscale-IP]:9625                ║"
echo "║                                                      ║"
echo "║  答应老师把德捡回来 🇨🇳🐉                            ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""
