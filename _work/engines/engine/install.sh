#!/bin/bash
# 龍魂9625·一键安装
# DNA: #龍芯⚡️2026-04-19-INSTALL-v1.0
# 用法: bash install.sh

set -e

ENGINE_DIR="$HOME/longhun-system/engine"
EXT_DIR="$HOME/longhun-system/chrome-ext"

echo "🐉 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "   龍魂9625·引擎安装"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 1. 装依赖
echo ""
echo "▶ 1/4 安装 Python 依赖..."
python3 -m pip install --user -r "$ENGINE_DIR/requirements.txt"
echo "  ✅ 依赖就位"

# 2. .env 模板
echo ""
echo "▶ 2/4 .env 配置..."
if [ ! -f "$ENGINE_DIR/.env" ]; then
    cp "$ENGINE_DIR/.env.example" "$ENGINE_DIR/.env"
    chmod 600 "$ENGINE_DIR/.env"
    echo "  ✅ 已创建 .env（请手动填入密钥：$ENGINE_DIR/.env）"
else
    echo "  ⏭️ .env 已存在·跳过"
fi

# 3. 软链已有 MVP 脚本（如果有）
echo ""
echo "▶ 3/4 软链已有 MVP..."
mkdir -p "$ENGINE_DIR/mvps"
for f in ethics_review_mvp.py longhun_wuxing_mvp.py sancai_router.py; do
    if [ -f "$HOME/$f" ]; then
        ln -sf "$HOME/$f" "$ENGINE_DIR/mvps/$f"
        echo "  ✅ 软链 ~/$f"
    elif [ -f "$HOME/longhun-system/bin/$f" ]; then
        ln -sf "$HOME/longhun-system/bin/$f" "$ENGINE_DIR/mvps/$f"
        echo "  ✅ 软链 bin/$f"
    fi
done

# 4. 写 launchd 开机自启（Mac）
echo ""
echo "▶ 4/4 开机自启..."
PLIST="$HOME/Library/LaunchAgents/com.longhun.9625.plist"
cat > "$PLIST" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key><string>com.longhun.9625</string>
    <key>ProgramArguments</key>
    <array>
        <string>$(which python3)</string>
        <string>$ENGINE_DIR/main.py</string>
    </array>
    <key>RunAtLoad</key><true/>
    <key>KeepAlive</key><true/>
    <key>StandardOutPath</key><string>$ENGINE_DIR/out.log</string>
    <key>StandardErrorPath</key><string>$ENGINE_DIR/err.log</string>
    <key>WorkingDirectory</key><string>$ENGINE_DIR</string>
</dict>
</plist>
EOF
echo "  ✅ LaunchAgent 已写入"
echo ""
echo "  启用: launchctl load $PLIST"
echo "  停用: launchctl unload $PLIST"

# 完成提示
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ 安装完成"
echo ""
echo "📝 下一步:"
echo "   1. 填写密钥: nano $ENGINE_DIR/.env"
echo "   2. 启动测试: python3 $ENGINE_DIR/main.py"
echo "   3. 健康检查: curl http://127.0.0.1:9625/api/health"
echo "   4. 装 Chrome 扩展:"
echo "      Chrome → chrome://extensions → 开发者模式 → 加载已解压"
echo "      选择: $EXT_DIR"
echo ""
echo "DNA: #龍芯⚡️2026-04-19-INSTALL-v1.0"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
