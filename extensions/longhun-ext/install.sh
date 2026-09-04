#!/bin/bash
# 龍魂9622·一键安装脚本 v2.0
# DNA(v∞): #龍芯⚡️丙午·丁酉·辛巳-LONGHUN-EXT-INSTALL-v2.0-2c7e5a9f
# 创建者: 诸葛鑫（UID9622） · 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 支持: macOS (Intel + Apple Silicon M1/M2/M3)
# 运行: chmod +x install.sh && ./install.sh

set -e
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'

echo -e "${GREEN}"
echo "🐉 龍魂9622引擎·一键安装 v2.0"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${NC}"

# ─── 检测 Apple Silicon ────────────────────────────────────
ARCH=$(uname -m)
if [ "$ARCH" = "arm64" ]; then
    echo -e "🍎 检测到 Apple Silicon (M系列芯片)"
    # Homebrew 在 Apple Silicon 默认在 /opt/homebrew
    export PATH="/opt/homebrew/bin:$PATH"
fi

# ─── Python 版本检查 ───────────────────────────────────────
PYTHON=$(command -v python3 || command -v python || echo "")
if [ -z "$PYTHON" ]; then
    echo -e "${RED}❌ 未找到 Python3${NC}"
    echo "请安装：brew install python3"
    exit 1
fi
PY_VER=$($PYTHON --version 2>&1)
echo -e "✅ Python: $PY_VER"

# ─── 创建目录 ─────────────────────────────────────────────
ENGINE_DIR="$HOME/longhun-engine"
EXT_DIR="$HOME/longhun-chrome-ext"
mkdir -p "$ENGINE_DIR"/{mvps,memory,static}
echo "✅ 目录创建：$ENGINE_DIR"

# ─── 安装 Python 依赖 ─────────────────────────────────────
echo "📦 安装 Python 依赖..."
$PYTHON -m pip install --user --quiet \
    fastapi uvicorn httpx python-dotenv pydantic
echo "✅ 基础依赖安装完成"

# 可选依赖（本地向量库·慢）
read -p "是否安装本地向量库（sentence-transformers·约500MB）？[y/N] " INSTALL_VEC
if [[ "$INSTALL_VEC" =~ ^[Yy]$ ]]; then
    $PYTHON -m pip install --user --quiet sentence-transformers faiss-cpu sqlite-utils
    echo "✅ 向量库安装完成"
fi

# ─── 复制引擎文件 ─────────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
if [ -f "$SCRIPT_DIR/engine/main.py" ]; then
    cp "$SCRIPT_DIR/engine/"*.py "$ENGINE_DIR/"
    echo "✅ 引擎文件复制完成"
fi

# 复制扩展文件
if [ -d "$SCRIPT_DIR" ]; then
    mkdir -p "$EXT_DIR"
    for f in manifest.json background.js content.js popup.html popup.js; do
        [ -f "$SCRIPT_DIR/$f" ] && cp "$SCRIPT_DIR/$f" "$EXT_DIR/" && echo "  ✓ $f"
    done
    [ -d "$SCRIPT_DIR/icons" ] && cp -r "$SCRIPT_DIR/icons" "$EXT_DIR/"
    echo "✅ Chrome扩展文件复制完成：$EXT_DIR"
fi

# ─── .env 模板 ────────────────────────────────────────────
if [ ! -f "$ENGINE_DIR/.env" ]; then
cat > "$ENGINE_DIR/.env" << 'ENVEOF'
# 龍魂9622引擎 · 环境变量
# DNA: #龍芯⚡️20260521-ENV-TEMPLATE

# Notion API (必填·记错本回写)
NOTION_TOKEN=请填入secret_开头的Notion Token
ERRATA_DB_ID=请填入记错本数据库ID

# AI 大脑 (至少填一个)
DEEPSEEK_API_KEY=sk-请填入
ANTHROPIC_API_KEY=sk-ant-请填入

# 苹果设备兼容 (iPhone/iPad同WiFi访问)
# 改为 true 后引擎监听局域网，iPhone可访问
APPLE_MODE=false

# 可选
DNA_LOG_DB_ID=请填入DNA日志数据库ID
ENVEOF
    echo "✅ .env 模板已创建：$ENGINE_DIR/.env"
    echo -e "${YELLOW}⚠️  请编辑 .env 填入您的 API Key${NC}"
fi

# ─── launchd 开机自启（Mac 专用） ─────────────────────────
PLIST="$HOME/Library/LaunchAgents/com.longhun.9622.plist"
cat > "$PLIST" << PLISTEOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>com.longhun.9622</string>
  <key>ProgramArguments</key>
  <array>
    <string>$PYTHON</string>
    <string>$ENGINE_DIR/main.py</string>
  </array>
  <key>WorkingDirectory</key>
  <string>$ENGINE_DIR</string>
  <key>RunAtLoad</key>
  <true/>
  <key>KeepAlive</key>
  <true/>
  <key>StandardOutPath</key>
  <string>$ENGINE_DIR/out.log</string>
  <key>StandardErrorPath</key>
  <string>$ENGINE_DIR/err.log</string>
</dict>
</plist>
PLISTEOF

launchctl unload "$PLIST" 2>/dev/null || true
launchctl load "$PLIST"
echo "✅ 开机自启已配置（launchd）"

# ─── 苹果图标生成（简版） ─────────────────────────────────
mkdir -p "$EXT_DIR/icons"
if ! command -v convert &>/dev/null; then
    echo -e "${YELLOW}⚠️  未找到 ImageMagick，跳过图标生成${NC}"
    echo "   可运行：brew install imagemagick"
    # 创建占位图标说明
    echo "请手动放置 16.png / 48.png / 128.png 到 $EXT_DIR/icons/" > "$EXT_DIR/icons/README.txt"
else
    # 用 ImageMagick 生成龍字图标
    for SIZE in 16 48 128; do
        convert -size ${SIZE}x${SIZE} xc:'#1a1a1a' \
            -fill '#D4AF37' -pointsize $((SIZE/2)) \
            -gravity center -annotate 0 '龍' \
            "$EXT_DIR/icons/${SIZE}.png" 2>/dev/null && \
            echo "  ✓ 图标 ${SIZE}x${SIZE}"
    done
fi

# ─── 测试引擎 ─────────────────────────────────────────────
echo ""
echo "🧪 测试引擎连接..."
sleep 2
if curl -s http://127.0.0.1:9622/api/health > /dev/null 2>&1; then
    echo -e "${GREEN}✅ 引擎在线！${NC}"
else
    echo -e "${YELLOW}⚠️  引擎启动中，稍后可手动测试：${NC}"
    echo "   curl http://127.0.0.1:9622/api/health"
fi

# ─── 完成提示 ─────────────────────────────────────────────
echo ""
echo -e "${GREEN}🎉 安装完成！${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📋 下一步："
echo "  1. 编辑 .env：nano $ENGINE_DIR/.env"
echo "  2. Chrome 安装扩展："
echo "     chrome://extensions → 开发者模式 → 加载已解压 → $EXT_DIR"
echo "  3. Safari 扩展（Mac）："
echo "     xcrun safari-web-extension-converter $EXT_DIR"
echo "  4. iPhone 访问（同WiFi）："
echo "     设置 APPLE_MODE=true，iPhone Safari 打开 http://[Mac局域网IP]:9622"
echo ""
echo "🧬 DNA: #龍芯⚡️$(date +%Y%m%d)-INSTALL-COMPLETE-v2.0"
echo "🔑 UID9622 · #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
