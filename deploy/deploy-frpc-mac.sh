#!/bin/bash
# ============================================================================
# deploy-frpc-mac.sh — Mac M4 Max 一键部署 frpc 客户端
# DNA: #龍芯⚡️丙午·辛未·FRPC-MAC-v1.0
#
# 在 Mac 上执行，自动下载+配置+启动 frpc
# 效果: 127.0.0.1:9633 → 鲲鹏双节点API
# ============================================================================

set -e

LONGHUN_ROOT="${LONGHUN_ROOT:-$HOME/longhun-system}"
FRP_DIR="${LONGHUN_ROOT}/frpc"

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'; BOLD='\033[1m'; NC='\033[0m'

echo ""
echo -e "${BOLD}🐉 龍魂系统 · Mac frpc 部署${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# ─── 收集配置 ───
if [ -f "${LONGHUN_ROOT}/deploy/.kunpeng_config" ]; then
    source <(grep -E "^(FRP_SERVER|FRP_TOKEN)=" "${LONGHUN_ROOT}/deploy/.kunpeng_config" 2>/dev/null || true)
fi

read -p "公网frps服务器IP ${FRP_SERVER:+[$FRP_SERVER]}: " input
FRP_SERVER="${input:-$FRP_SERVER}"
if [ -z "$FRP_SERVER" ]; then
    echo -e "${RED}❌ 必须提供公网服务器IP${NC}"
    exit 1
fi

read -p "frp Token [${FRP_TOKEN:-LONGHUN2026_UID9622_KUNPENG}]: " input
FRP_TOKEN="${input:-${FRP_TOKEN:-LONGHUN2026_UID9622_KUNPENG}}"

# 保存配置
mkdir -p "${LONGHUN_ROOT}/deploy"
if grep -q "FRP_SERVER" "${LONGHUN_ROOT}/deploy/.kunpeng_config" 2>/dev/null; then
    sed -i '' "s/FRP_SERVER=.*/FRP_SERVER=${FRP_SERVER}/" "${LONGHUN_ROOT}/deploy/.kunpeng_config"
    sed -i '' "s/FRP_TOKEN=.*/FRP_TOKEN=${FRP_TOKEN}/" "${LONGHUN_ROOT}/deploy/.kunpeng_config"
else
    echo "FRP_SERVER=${FRP_SERVER}" >> "${LONGHUN_ROOT}/deploy/.kunpeng_config"
    echo "FRP_TOKEN=${FRP_TOKEN}" >> "${LONGHUN_ROOT}/deploy/.kunpeng_config"
fi

echo ""
echo -e "服务器: ${GREEN}${FRP_SERVER}${NC}"
echo -e "Token:  ${YELLOW}***${FRP_TOKEN: -4}${NC}"
read -p "确认部署? [Y/n]: " CONFIRM
CONFIRM=${CONFIRM:-Y}
if [[ ! "$CONFIRM" =~ ^[Yy]$ ]]; then
    echo "已取消"
    exit 0
fi

mkdir -p "${FRP_DIR}" "${LONGHUN_ROOT}/logs"

# ─── 1. 下载 Darwin ARM64 frpc ───
echo -e "\n${CYAN}[1/4] 下载 Darwin ARM64 frpc...${NC}"

FRP_VERSION="0.58.1"
ARCH=$(uname -m)
if [[ "$ARCH" == "arm64" ]] || [[ "$ARCH" == "aarch64" ]]; then
    FRP_ARCH="darwin_arm64"
else
    FRP_ARCH="darwin_amd64"
fi

cd /tmp
URL="https://github.com/fatedier/frp/releases/download/v${FRP_VERSION}/frp_${FRP_VERSION}_${FRP_ARCH}.tar.gz"

if ! curl -sL "$URL" -o frp.tar.gz; then
    echo -e "${RED}❌ 下载失败${NC}"
    echo "   手动: curl -L '$URL' -o /tmp/frp.tar.gz"
    echo "   然后重跑此脚本"
    exit 1
fi

tar -xzf frp.tar.gz
cp "frp_${FRP_VERSION}_${FRP_ARCH}/frpc" "${FRP_DIR}/frpc"
chmod +x "${FRP_DIR}/frpc"
rm -rf "frp_${FRP_VERSION}_${FRP_ARCH}" /tmp/frp.tar.gz

echo -e "   ✅ frpc 已安装到 ${FRP_DIR}/frpc"

# ─── 2. 写配置 ───
echo -e "${CYAN}[2/4] 写入配置...${NC}"

cat > "${FRP_DIR}/frpc.toml" << TOMLEOF
# 龍魂系统 · Mac frpc 配置
# DNA: #龍芯⚡️丙午·辛未·FRPC-MAC

serverAddr = "${FRP_SERVER}"
serverPort = 7000
auth.method = "token"
auth.token = "${FRP_TOKEN}"

# ── 反向访问鲲鹏 API (STCP visitor模式) ──
# 效果: 本机 127.0.0.1:9633 = 鲲鹏 9633 双节点API
[[visitors]]
name = "visit-kunpeng-api"
type = "stcp"
serverName = "longhun-kunpeng-api"
secretKey = "${FRP_TOKEN}"
bindAddr = "127.0.0.1"
bindPort = 9633

# ── 反向访问鲲鹏 SSH ──
# 效果: 本机 127.0.0.1:19622 = 鲲鹏 22 SSH
[[visitors]]
name = "visit-kunpeng-ssh"
type = "stcp"
serverName = "longhun-kunpeng-ssh"
secretKey = "${FRP_TOKEN}"
bindAddr = "127.0.0.1"
bindPort = 19622

# ── 暴露 Mac API 到公网（供鲲鹏回连） ──
[[proxies]]
name = "longhun-mac-api"
type = "tcp"
localIP = "127.0.0.1"
localPort = 9634
remotePort = 39622

log.to = "${LONGHUN_ROOT}/logs/frpc.log"
log.level = "info"
log.maxDays = 30
TOML EOF

# ─── 3. LaunchAgent (开机自启) ───
echo -e "${CYAN}[3/4] 配置 LaunchAgent (开机自启)...${NC}"

mkdir -p ~/Library/LaunchAgents

cat > ~/Library/LaunchAgents/com.longhun.frpc.plist << PLISTEOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.longhun.frpc</string>
    <key>ProgramArguments</key>
    <array>
        <string>${FRP_DIR}/frpc</string>
        <string>-c</string>
        <string>${FRP_DIR}/frpc.toml</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>${LONGHUN_ROOT}/logs/frpc.log</string>
    <key>StandardErrorPath</key>
    <string>${LONGHUN_ROOT}/logs/frpc-error.log</string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/usr/local/bin:/usr/bin:/bin:/opt/homebrew/bin</string>
    </dict>
</dict>
</plist>
PLISTEOF

# 停止旧实例
pkill -f "frpc.*frpc.toml" 2>/dev/null || true
sleep 1

# 加载
launchctl unload ~/Library/LaunchAgents/com.longhun.frpc.plist 2>/dev/null || true
launchctl load ~/Library/LaunchAgents/com.longhun.frpc.plist

# ─── 4. 验证 ───
echo -e "${CYAN}[4/4] 验证...${NC}"
sleep 3

# 检查进程
if pgrep -f "frpc.*frpc.toml" > /dev/null; then
    PID=$(pgrep -f "frpc.*frpc.toml" | head -1)
    echo -e "   frpc: ${GREEN}🟢 运行中 (PID: ${PID})${NC}"
else
    echo -e "   frpc: ${RED}🔴 未运行${NC}"
    echo -e "   ${CYAN}日志: tail -20 ${LONGHUN_ROOT}/logs/frpc.log${NC}"
fi

# 测试 API 通道
echo ""
if curl -s --connect-timeout 3 "http://127.0.0.1:9633/health" | grep -q "kunpeng"; then
    echo -e "   API:  ${GREEN}🟢 可达 (127.0.0.1:9633 → 鲲鹏){NC}"
else
    echo -e "   API:  ${YELLOW}🔴 暂不可达 (等待鲲鹏端 frpc 连接){NC}"
fi

# ─── 写快捷命令 ───
ALIAS_FILE="$HOME/.zshrc"
if [ -f "$HOME/.bashrc" ]; then ALIAS_FILE="$HOME/.bashrc"; fi

if ! grep -q "alias lh=" "$ALIAS_FILE" 2>/dev/null; then
    cat >> "$ALIAS_FILE" << 'ALIASEOF'

# 🐉 龍魂双节点
alias lh="python3 $HOME/longhun-system/L6_同步层/dual_node_cli.py"
alias lh-tunnel="lh tunnel"
alias lh-dashboard="lh tunnel dashboard"
ALIASEOF
fi

# ─── 完成 ───
echo ""
echo "════════════════════════════════════════════════"
echo -e "${BOLD}🐉 Mac frpc 部署完成${NC}"
echo "════════════════════════════════════════════════"
echo ""
echo "  快捷命令:"
echo -e "    ${CYAN}lh tunnel status${NC}    隧道状态"
echo -e "    ${CYAN}lh tunnel dashboard${NC}  打开Web面板"
echo -e "    ${CYAN}lh status${NC}           双节点总览"
echo ""
echo "  隧道映射:"
echo -e "    ${GREEN}127.0.0.1:9633${NC}  → 鲲鹏双节点 API"
echo -e "    ${GREEN}127.0.0.1:19622${NC} → 鲲鹏 SSH 跳板"
echo ""
echo "  管理:"
echo "    launchctl stop com.longhun.frpc    # 暂停"
echo "    launchctl start com.longhun.frpc   # 恢复"
echo "    tail -f ${LONGHUN_ROOT}/logs/frpc.log  # 日志"
echo ""
echo -e "  DNA: #龍芯⚡️丙午·辛未·FRPC-MAC-v1.0"
echo ""

# 自动 source
if [ -f "$HOME/.zshrc" ]; then
    source "$HOME/.zshrc" 2>/dev/null || true
fi
