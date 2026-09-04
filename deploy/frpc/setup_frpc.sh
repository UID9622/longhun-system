#!/bin/bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# DNA: #龍芯⚡️丙午·乙未·乙未·子时·䷀乾-DEPLOY-FRPC-SETUP-v1.0-a1b2c3d6
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# 协议: CC BY-NC-SA 4.0
# 用途: 一键安装FRP客户端+配置+启动，打通Mac↔鲲鹏

set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
LH_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "🔗 龍魂 · Mac↔鲲鹏 FRP 穿透一键部署"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 1. 安装 frpc
echo ""
echo "[1/4] 检查 frpc..."
if command -v frpc &>/dev/null; then
    echo "  ✅ frpc 已安装: $(frpc --version 2>&1 | head -1)"
else
    echo "  📦 下载 frpc v0.61.2 (arm64)..."
    cd /tmp
    curl -sL "https://github.com/fatedier/frp/releases/download/v0.61.2/frp_0.61.2_darwin_arm64.tar.gz" -o frp.tar.gz
    tar xzf frp.tar.gz
    sudo cp frp_0.61.2_darwin_arm64/frpc /usr/local/bin/frpc
    sudo chmod +x /usr/local/bin/frpc
    rm -rf frp.tar.gz frp_0.61.2_darwin_arm64
    echo "  ✅ frpc 安装完成: $(frpc --version 2>&1 | head -1)"
fi

# 2. 创建日志目录
echo ""
echo "[2/4] 创建日志目录..."
mkdir -p "$LH_ROOT/logs"
echo "  ✅ logs/ 就绪"

# 3. 加载 launchd
echo ""
echo "[3/4] 加载 launchd 守护..."
PLIST_SRC="$SCRIPT_DIR/com.uid9622.longhun-frpc.plist"
PLIST_DST="$HOME/Library/LaunchAgents/com.uid9622.longhun-frpc.plist"

# 停止旧的（如果存在）
launchctl unload "$PLIST_DST" 2>/dev/null || true
cp "$PLIST_SRC" "$PLIST_DST"
launchctl load "$PLIST_DST"
echo "  ✅ launchd 已加载"

# 4. 验证
echo ""
echo "[4/4] 验证连接..."
sleep 2

# 检查frpc进程
if pgrep -f "frpc.*frpc.toml" > /dev/null; then
    echo "  ✅ frpc 进程运行中"
else
    echo "  🔴 frpc 进程未运行，查看日志:"
    tail -20 "$LH_ROOT/logs/frpc.err.log" 2>/dev/null || echo "  无错误日志"
    exit 1
fi

# 测试隧道
echo "  测试FRP隧道..."
if ssh -i ~/.ssh/longhun_kunpeng_ed25519 -o ConnectTimeout=5 root@119.13.90.27 "ss -tlnp | grep 18799" 2>/dev/null; then
    echo "  ✅ 鲲鹏端18799端口已监听"
else
    echo "  🟡 等待FRP注册...（最多30秒）"
    for i in $(seq 1 6); do
        sleep 5
        if ssh -i ~/.ssh/longhun_kunpeng_ed25519 -o ConnectTimeout=5 root@119.13.90.27 "ss -tlnp | grep 18799" 2>/dev/null; then
            echo "  ✅ 鲲鹏端18799端口已监听"
            break
        fi
        echo "    等待中... ($((i*5))s)"
    done
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎉 Mac↔鲲鹏 FRP 穿透部署完成！"
echo ""
echo "小艺桥接地址:"
echo "  本地: http://127.0.0.1:8799"
echo "  穿透: https://uid9622.cn/xiaoyi/  (需配置nginx)"
echo ""
echo "管理命令:"
echo "  launchctl list | grep frpc    # 查看状态"
echo "  launchctl unload $PLIST_DST     # 停止"
echo "  launchctl load $PLIST_DST       # 启动"
echo "  tail -f $LH_ROOT/logs/frpc.out.log  # 查看日志"
echo ""
echo "DNA: #龍芯⚡️丙午·乙未·乙未·子时·䷀乾-DEPLOY-FRPC-SETUP-v1.0-a1b2c3d6"
