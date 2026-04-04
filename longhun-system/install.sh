#!/bin/bash
# ═══════════════════════════════════════════════════════════
# 龍魂系统 · 新设备一键安装脚本
# DNA: #龍芯⚡️20260321-INSTALL-v1.0
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 作者: 诸葛鑫（UID9622）
# 理论指导: 曾仕强老师（永恒显示）
# ═══════════════════════════════════════════════════════════
set -e

LONGHUN_DIR="$HOME/longhun-system"
LAUNCHAGENTS_DIR="$HOME/Library/LaunchAgents"

echo ""
echo "════════════════════════════════════════════════════"
echo "  龍魂系统 · 一键安装"
echo "  DNA: #龍芯⚡️20260321-INSTALL-v1.0"
echo "════════════════════════════════════════════════════"
echo ""

# ── 1. 检查基础依赖 ──
echo "[1/6] 检查基础依赖..."
command -v python3 >/dev/null 2>&1 || { echo "❌ 请先安装 Python3"; exit 1; }
command -v git     >/dev/null 2>&1 || { echo "❌ 请先安装 Git";     exit 1; }
command -v brew    >/dev/null 2>&1 || echo "⚠️  Homebrew未安装，部分功能可能受限"
echo "✅ 基础依赖检查通过"

# ── 2. 安装 Python 依赖 ──
echo ""
echo "[2/6] 安装 Python 依赖..."
pip3 install flask flask-cors python-dotenv requests numpy --quiet
echo "✅ Python 依赖安装完成"

# ── 3. 创建必要目录 ──
echo ""
echo "[3/6] 创建系统目录..."
mkdir -p "$HOME/.longhun/evidence"
mkdir -p "$HOME/.longhorn/certs"
mkdir -p "$HOME/.longhun"
mkdir -p "$LONGHUN_DIR/logs"
mkdir -p "$LONGHUN_DIR/reports"
echo "✅ 目录创建完成"

# ── 4. 注册 LaunchAgents（开机自启）──
echo ""
echo "[4/6] 注册开机自启服务..."

# 主服务启动器
cat > "$LAUNCHAGENTS_DIR/com.longhun.startup.plist" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.longhun.startup</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>$LONGHUN_DIR/bin/启动所有服务.sh</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>StandardOutPath</key>
    <string>$LONGHUN_DIR/logs/开机启动输出.log</string>
    <key>StandardErrorPath</key>
    <string>$LONGHUN_DIR/logs/开机启动错误.log</string>
    <key>KeepAlive</key>
    <false/>
</dict>
</plist>
EOF

# 每小时同步
cat > "$LAUNCHAGENTS_DIR/com.longhun.sync.plist" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.longhun.sync</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>$LONGHUN_DIR/bin/一键同步.sh</string>
    </array>
    <key>StartInterval</key>
    <integer>3600</integer>
    <key>StandardOutPath</key>
    <string>$LONGHUN_DIR/logs/定时同步输出.log</string>
    <key>StandardErrorPath</key>
    <string>$LONGHUN_DIR/logs/定时同步错误.log</string>
</dict>
</plist>
EOF

# 每晚22点整理
cat > "$LAUNCHAGENTS_DIR/com.longhun.cleanup.plist" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.longhun.cleanup</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>-c</string>
        <string>bash $LONGHUN_DIR/bin/新文件整理.sh && bash $LONGHUN_DIR/bin/清理垃圾.sh</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>22</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>$LONGHUN_DIR/logs/定时整理输出.log</string>
    <key>StandardErrorPath</key>
    <string>$LONGHUN_DIR/logs/定时整理错误.log</string>
</dict>
</plist>
EOF

# 加载所有 LaunchAgents
for plist in com.longhun.startup com.longhun.sync com.longhun.cleanup; do
    launchctl unload "$LAUNCHAGENTS_DIR/${plist}.plist" 2>/dev/null || true
    launchctl load   "$LAUNCHAGENTS_DIR/${plist}.plist" 2>/dev/null && echo "  ✅ $plist 已注册" || echo "  ⚠️  $plist 注册失败（可手动加载）"
done

# ── 5. Git 配置 ──
echo ""
echo "[5/6] Git 配置检查..."
if ! git -C "$LONGHUN_DIR" remote get-url gitee >/dev/null 2>&1; then
    echo "⚠️  Gitee remote 未配置，请手动运行："
    echo "    git remote add gitee git@gitee.com:uid9622_admin/cnsh-editor-phb.git"
else
    echo "✅ Gitee remote 已配置"
fi
if ! git -C "$LONGHUN_DIR" remote get-url github >/dev/null 2>&1; then
    echo "⚠️  GitHub remote 未配置，请手动运行："
    echo "    git remote add github git@github.com:UID9622/ai-truth-protocol.git"
else
    echo "✅ GitHub remote 已配置"
fi

# ── 6. 提示手动完成项 ──
echo ""
echo "[6/6] 需要手动完成的项目..."
echo ""
echo "  🔑 密钥（在新设备上重新存入Keychain）："
echo "     security add-generic-password -s longhun-notion-token -a uid9622 -w <token>"
echo "     bash $LONGHUN_DIR/bin/save_wx_secret.sh"
echo ""
echo "  🤖 AI服务（新设备需重新安装）："
echo "     curl -fsSL https://ollama.com/install.sh | sh"
echo "     ollama pull qwen2.5:72b"
echo "     pip install open-webui"
echo ""
echo "  🔐 GPG密钥（从备份恢复）："
echo "     gpg --import <你的私钥备份文件>"
echo ""
echo "════════════════════════════════════════════════════"
echo "  ✅ 安装完成！"
echo "  启动服务：bash $LONGHUN_DIR/bin/启动所有服务.sh"
echo "  检查状态：bash $LONGHUN_DIR/bin/api_check.sh"
echo "  DNA: #龍芯⚡️20260321-INSTALL-v1.0"
echo "════════════════════════════════════════════════════"
echo ""
