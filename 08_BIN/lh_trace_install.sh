#!/bin/bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂·底座痕迹采集引擎 — 一键安装脚本 v1.0
# DNA: #龍芯⚡️丙午·乙未·壬寅·巳时·☰乾-TRACE-INSTALL-V1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# 协议: CC BY-NC-SA 4.0
#
# 用法:
#   chmod +x bin/lh_trace_install.sh
#   ./bin/lh_trace_install.sh              # macOS 交互安装
#   ./bin/lh_trace_install.sh --all        # 全部自动安装（含 launchd）
#   ./bin/lh_trace_install.sh --uninstall  # 卸载
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
LONGHUN_ROOT="$(dirname "$SCRIPT_DIR")"
LAUNCHD_LABEL="com.longhun.trace-collector"
PLIST_PATH="$HOME/Library/LaunchAgents/${LAUNCHD_LABEL}.plist"
COLLECTOR_BIN="$LONGHUN_ROOT/bin/lh_base_trace_collector.py"
DATA_DIR="$HOME/.longhun/traces"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

banner() {
    echo ""
    echo -e "${YELLOW}⚡ 龍魂·底座痕迹采集引擎 — 安装程序${NC}"
    echo -e "${YELLOW}   DNA: #龍芯⚡️丙午·乙未·壬寅·巳时·☰乾-TRACE-INSTALL-V1.0${NC}"
    echo ""
}

check_python() {
    if command -v python3 &>/dev/null; then
        PY_VER=$(python3 --version 2>&1 | cut -d' ' -f2)
        echo -e "  ${GREEN}✅ Python3 $PY_VER${NC}"
        return 0
    else
        echo -e "  ${RED}❌ 未找到 python3${NC}"
        return 1
    fi
}

check_deps() {
    echo -e "${BLUE}[1/5] 检查依赖...${NC}"
    local all_ok=true
    
    check_python || all_ok=false
    
    # 检查采集器脚本
    if [ -f "$COLLECTOR_BIN" ]; then
        echo -e "  ${GREEN}✅ 采集引擎脚本存在${NC}"
    else
        echo -e "  ${RED}❌ 采集引擎脚本不存在: $COLLECTOR_BIN${NC}"
        all_ok=false
    fi
    
    # 检查 ps/lsof 命令
    for cmd in ps lsof who; do
        if command -v $cmd &>/dev/null; then
            echo -e "  ${GREEN}✅ $cmd${NC}"
        else
            echo -e "  ${RED}❌ $cmd 不可用${NC}"
            all_ok=false
        fi
    done
    
    if [ "$all_ok" = false ]; then
        echo -e "${RED}依赖检查未通过${NC}"
        exit 1
    fi
}

create_data_dir() {
    echo -e "${BLUE}[2/5] 创建数据目录...${NC}"
    mkdir -p "$DATA_DIR"
    chmod 700 "$DATA_DIR"
    echo -e "  ${GREEN}✅ $DATA_DIR${NC}"
}

install_launchd() {
    echo -e "${BLUE}[3/5] 安装 macOS launchd 服务...${NC}"
    
    if [ "$(uname)" != "Darwin" ]; then
        echo -e "  ${YELLOW}⏭️ 非 macOS，跳过 launchd${NC}"
        return
    fi
    
    mkdir -p "$HOME/Library/LaunchAgents"
    
    cat > "$PLIST_PATH" << PLISTEOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>${LAUNCHD_LABEL}</string>
    
    <key>ProgramArguments</key>
    <array>
        <string>${COLLECTOR_BIN}</string>
        <string>start</string>
    </array>
    
    <key>WorkingDirectory</key>
    <string>${LONGHUN_ROOT}</string>
    
    <key>RunAtLoad</key>
    <true/>
    
    <key>KeepAlive</key>
    <true/>
    
    <key>ThrottleInterval</key>
    <integer>5</integer>
    
    <key>StandardOutPath</key>
    <string>${DATA_DIR}/collector.log</string>
    
    <key>StandardErrorPath</key>
    <string>${DATA_DIR}/collector.err</string>
    
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/opt/homebrew/bin</string>
        <key>HOME</key>
        <string>${HOME}</string>
    </dict>
</dict>
</plist>
PLISTEOF
    
    # 先停止旧服务
    launchctl unload "$PLIST_PATH" 2>/dev/null || true
    
    # 加载服务
    launchctl load "$PLIST_PATH" 2>/dev/null
    echo -e "  ${GREEN}✅ launchd 服务已安装并启动${NC}"
    echo -e "  管理命令:"
    echo -e "    launchctl list | grep longhun           # 查看状态"
    echo -e "    launchctl unload $PLIST_PATH             # 停止"
    echo -e "    launchctl load $PLIST_PATH               # 启动"
}

install_test() {
    echo -e "${BLUE}[4/5] 自检...${NC}"
    
    # 启动采集器（如果未运行）
    if ! python3 "$COLLECTOR_BIN" status 2>/dev/null; then
        echo -e "  ${YELLOW}→ 启动采集引擎...${NC}"
        python3 "$COLLECTOR_BIN" start &
        COLLECTOR_PID=$!
        sleep 3
    fi
    
    # 健康检查
    for i in $(seq 1 5); do
        if curl -sf http://127.0.0.1:18775/health > /dev/null 2>&1; then
            echo -e "  ${GREEN}✅ 采集引擎 API 可达${NC}"
            HEALTH_DATA=$(curl -sf http://127.0.0.1:18775/health 2>/dev/null)
            echo -e "  ${GREEN}   响应: $HEALTH_DATA${NC}"
            
            # 等几秒让采集器采集一些事件
            sleep 10
            
            # 检查事件采集
            EVENTS_DATA=$(curl -sf http://127.0.0.1:18775/status 2>/dev/null || echo '{"events":{}}')
            echo -e "  ${GREEN}   状态: $EVENTS_DATA${NC}"
            return 0
        fi
        sleep 2
    done
    
    echo -e "  ${RED}❌ 采集引擎 API 不可达${NC}"
    return 1
}

install_chrome_plugin() {
    echo -e "${BLUE}[5/5] Chrome 插件安装指引...${NC}"
    
    PLUGIN_DIR="$LONGHUN_ROOT/web/chrome-extensions/browser-historian"
    
    if [ -f "$PLUGIN_DIR/manifest.json" ]; then
        VER=$(python3 -c "import json; print(json.load(open('$PLUGIN_DIR/manifest.json'))['version'])" 2>/dev/null || echo "?")
        echo -e "  ${GREEN}✅ 浏览器史官插件 v$VER${NC}"
        echo -e "  安装步骤:"
        echo -e "    1. 打开 Chrome → chrome://extensions"
        echo -e "    2. 打开右上角「开发者模式」"
        echo -e "    3. 点击「加载已解压的扩展程序」"
        echo -e "    4. 选择目录: $PLUGIN_DIR"
        echo -e "    5. 点击插件图标，切换到「底座痕迹」标签页"
    else
        echo -e "  ${RED}❌ 插件目录不存在: $PLUGIN_DIR${NC}"
    fi
}

finish() {
    echo ""
    echo -e "${GREEN}════════════════════════════════════════${NC}"
    echo -e "${GREEN}  安装完成！${NC}"
    echo -e "${GREEN}════════════════════════════════════════${NC}"
    echo ""
    echo -e "  ${YELLOW}快捷命令:${NC}"
    echo "    python3 bin/lh_base_trace_collector.py status   # 查看采集状态"
    echo "    curl http://127.0.0.1:18775/health               # API健康检查"
    echo "    curl http://127.0.0.1:18775/status               # 采集统计"
    echo ""
    echo -e "  ${YELLOW}日志路径:${NC}"
    echo "    $DATA_DIR/collector.log"
    echo "    $DATA_DIR/collector.err"
    echo "    $DATA_DIR/trace.db"
    echo ""
    echo -e "  ${YELLOW}Chrome插件:${NC}"
    echo "    打开 chrome://extensions → 加载已解压 → 选择 web/chrome-extensions/browser-historian"
    echo ""
}

uninstall_all() {
    echo -e "${YELLOW}卸载底座痕迹采集引擎...${NC}"
    
    # 停止 launchd
    if [ -f "$PLIST_PATH" ]; then
        launchctl unload "$PLIST_PATH" 2>/dev/null || true
        rm -f "$PLIST_PATH"
        echo "  ✅ launchd 服务已移除"
    fi
    
    # 停止进程
    python3 "$COLLECTOR_BIN" stop 2>/dev/null || true
    
    # 保留数据目录（不删除）
    echo "  ℹ️ 数据目录保留: $DATA_DIR"
    echo "  ℹ️ 如需删除: rm -rf $DATA_DIR"
    
    echo -e "${GREEN}卸载完成${NC}"
}

# ─── 主流程 ───────────────────────────────────────────
banner

case "${1:-}" in
    --uninstall)
        uninstall_all
        exit 0
        ;;
    --all)
        AUTO=true
        ;;
    *)
        AUTO=false
        ;;
esac

check_deps
create_data_dir

if [ "$(uname)" = "Darwin" ]; then
    install_launchd
fi

install_test
install_chrome_plugin
finish
