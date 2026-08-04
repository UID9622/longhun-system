#!/bin/bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# ═══════════════════════════════════════════════════════════════
# 龍魂·内网互联 — 一键安装脚本
# DNA: #龍芯⚡️丙午·辛未·乙酉·未时·䷾既济-INTERNAL-NET-INSTALL-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# #CONFIRM🌌9622-ONLY-ONCE🧬INS1-001A
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
#
# 用法:
#   # 安装网关（鲲鹏服务器）
#   bash install.sh --role gateway --name "鲲鹏中心"
#
#   # 安装节点（任何设备）
#   bash install.sh --role peer --name "我的Mac" --type mac
#
#   # 安装全部（多节点编排，在一台机器上模拟）  
#   bash install.sh --role all
#
#   # 仅装依赖
#   bash install.sh --deps-only
# ═══════════════════════════════════════════════════════════════

set -e

# ── 颜色 ──
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

# ── 默认值 ──
ROLE="peer"
DEVICE_NAME=""
DEVICE_TYPE="auto"
GATEWAY="auto"
PORT=9622
INSTALL_DIR="$HOME/.longhun"
PROJECT_DIR=""
DEPS_ONLY=false
USE_DOCKER=false
FORCE=false

# ── Banner ──
print_banner() {
    echo ""
    echo -e "${BLUE}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║  🐉 龍魂·内网互联节点 — 一键安装 v1.0                         ║${NC}"
    echo -e "${BLUE}║                                                              ║${NC}"
    echo -e "${BLUE}║  一台鲲鹏当中心，所有设备内网直连，不经过云                      ║${NC}"
    echo -e "${BLUE}║  像插U盘一样，连WiFi/插网线即用                                 ║${NC}"
    echo -e "${BLUE}╚══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

# ── 帮助 ──
show_help() {
    echo "用法: bash install.sh [选项]"
    echo ""
    echo "选项:"
    echo "  --role ROLE        角色: gateway | peer | all (默认: peer)"
    echo "  --name NAME        设备名称 (默认: hostname)"
    echo "  --type TYPE        设备类型: mac|win|linux|kunpeng|loongson|phone|pad|raspberry|auto"
    echo "  --gateway IP       网关IP (默认: auto 自动发现)"
    echo "  --port PORT        网关端口 (默认: 9622)"
    echo "  --docker           使用Docker部署"
    echo "  --deps-only        仅安装依赖"
    echo "  --force            强制重装"
    echo "  --help             显示此帮助"
    echo ""
    echo "示例:"
    echo "  # 鲲鹏上安装中心网关"
    echo "  bash install.sh --role gateway --name '鲲鹏中心' --type kunpeng"
    echo ""
    echo "  # Mac上安装节点（自动发现网关）"
    echo "  bash install.sh --role peer --name 'Mac工作室' --type mac"
    echo ""
    echo "  # 用Docker一键启动所有节点"
    echo "  bash install.sh --role all --docker"
    echo ""
    echo "  # 家中电脑安装"
    echo "  bash install.sh --role peer --name '家里电脑'"
}

# ── 解析参数 ──
while [[ $# -gt 0 ]]; do
    case "$1" in
        --role)      ROLE="$2"; shift 2 ;;
        --name)      DEVICE_NAME="$2"; shift 2 ;;
        --type)      DEVICE_TYPE="$2"; shift 2 ;;
        --gateway)   GATEWAY="$2"; shift 2 ;;
        --port)      PORT="$2"; shift 2 ;;
        --docker)    USE_DOCKER=true; shift ;;
        --deps-only) DEPS_ONLY=true; shift ;;
        --force)     FORCE=true; shift ;;
        --help)      show_help; exit 0 ;;
        -h)          show_help; exit 0 ;;
        *)           echo -e "${RED}未知参数: $1${NC}"; show_help; exit 1 ;;
    esac
done

# ── 检测系统 ──
detect_system() {
    OS="$(uname -s)"
    ARCH="$(uname -m)"
    
    echo -e "${CYAN}📋 系统检测:${NC}"
    echo "   操作系统: $OS"
    echo "   架构:     $ARCH"

    if [ "$DEVICE_TYPE" = "auto" ] || [ -z "$DEVICE_TYPE" ]; then
        case "$OS" in
            Darwin)  DEVICE_TYPE="mac" ;;
            MINGW*|MSYS*|CYGWIN*) DEVICE_TYPE="win" ;;
            Linux)
                if [ -f /proc/cpuinfo ]; then
                    if grep -qi "kunpeng\|taishan" /proc/cpuinfo 2>/dev/null; then
                        DEVICE_TYPE="kunpeng"
                    elif grep -qi "loongson\|loongarch" /proc/cpuinfo 2>/dev/null; then
                        DEVICE_TYPE="loongson"
                    else
                        DEVICE_TYPE="linux"
                    fi
                else
                    DEVICE_TYPE="linux"
                fi
                ;;
            *) DEVICE_TYPE="unknown" ;;
        esac
    fi
    echo "   设备类型: $DEVICE_TYPE"

    if [ -z "$DEVICE_NAME" ]; then
        DEVICE_NAME="$(hostname)"
    fi
    echo "   设备名称: $DEVICE_NAME"
    echo ""
}

# ── 安装Python依赖 ──
install_python_deps() {
    echo -e "${YELLOW}📦 检查 Python 环境...${NC}"
    
    # 检查 Python3
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}❌ 未找到 Python3，请先安装 Python 3.9+${NC}"
        echo "   Mac:  brew install python@3.11"
        echo "   Ubuntu/Debian: sudo apt install python3 python3-pip"
        echo "   CentOS: sudo yum install python3 python3-pip"
        exit 1
    fi
    
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    echo -e "${GREEN}   Python: $PYTHON_VERSION${NC}"
    
    # 安装 pip 依赖
    echo -e "${YELLOW}📦 安装 Python 依赖...${NC}"
    pip3 install --user --quiet fastapi uvicorn requests python-multipart pyyaml 2>/dev/null || \
    pip3 install --quiet fastapi uvicorn requests python-multipart pyyaml 2>/dev/null || {
        echo -e "${YELLOW}⚠️ 用户级安装失败，尝试系统级...${NC}"
        sudo pip3 install fastapi uvicorn requests python-multipart pyyaml || {
            echo -e "${RED}❌ 依赖安装失败${NC}"
            exit 1
        }
    }
    echo -e "${GREEN}   ✅ 依赖安装完成${NC}"
}

# ── 安装Docker（如果需要）──
install_docker() {
    if command -v docker &> /dev/null; then
        echo -e "${GREEN}   Docker: $(docker --version)${NC}"
        return 0
    fi

    echo -e "${YELLOW}📦 安装 Docker...${NC}"
    
    case "$OS" in
        Darwin)
            echo -e "${YELLOW}   请手动安装 Docker Desktop:${NC}"
            echo "   https://www.docker.com/products/docker-desktop"
            echo -e "${RED}   安装后请重新运行此脚本${NC}"
            exit 1
            ;;
        Linux)
            if [ -f /etc/os-release ]; then
                . /etc/os-release
                case "$ID" in
                    ubuntu|debian)
                        curl -fsSL https://get.docker.com | sudo sh
                        sudo usermod -aG docker "$USER"
                        ;;
                    centos|rhel|fedora|rocky|almalinux)
                        sudo yum install -y docker
                        sudo systemctl enable docker
                        sudo systemctl start docker
                        sudo usermod -aG docker "$USER"
                        ;;
                    openeuler|kylin|uos)
                        # 国产系统
                        sudo yum install -y docker || sudo apt install -y docker.io
                        sudo systemctl enable docker
                        sudo systemctl start docker
                        sudo usermod -aG docker "$USER"
                        ;;
                    *)
                        curl -fsSL https://get.docker.com | sudo sh
                        ;;
                esac
            else
                curl -fsSL https://get.docker.com | sudo sh
            fi
            echo -e "${GREEN}   ✅ Docker 安装完成 (可能需要重新登录)${NC}"
            ;;
        *)
            echo -e "${RED}   请手动安装 Docker${NC}"
            exit 1
            ;;
    esac
}

# ── 复制脚本 ──
install_scripts() {
    echo -e "${YELLOW}📂 安装龍魂脚本...${NC}"
    
    # 查找项目目录
    if [ -z "$PROJECT_DIR" ]; then
        # 从当前脚本位置推断
        SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
        PROJECT_DIR="$(cd "$SCRIPT_DIR/../../.." && pwd 2>/dev/null || echo "$INSTALL_DIR")"
    fi
    
    mkdir -p "$INSTALL_DIR"/{scripts,config,logs,cache}
    
    # 复制核心脚本
    if [ -f "$SCRIPT_DIR/longhun-api-gateway.py" ]; then
        cp "$SCRIPT_DIR/longhun-api-gateway.py" "$INSTALL_DIR/scripts/"
        cp "$SCRIPT_DIR/longhun-peer-client.py" "$INSTALL_DIR/scripts/"
        cp "$SCRIPT_DIR/entrypoint.sh" "$INSTALL_DIR/"
        cp "$SCRIPT_DIR/config/default.yaml" "$INSTALL_DIR/config/"
        echo -e "${GREEN}   ✅ 脚本复制到: $INSTALL_DIR${NC}"
    else
        # 源码不在本地，下载
        echo -e "${YELLOW}   本地未找到脚本，将使用Docker部署${NC}"
        USE_DOCKER=true
    fi
}

# ── 配置 systemd 自启动 (Linux) ──
setup_systemd() {
    if [ "$OS" != "Linux" ]; then
        return
    fi

    echo -e "${YELLOW}⚙️ 配置 systemd 自启动...${NC}"
    
    SERVICE_FILE="/etc/systemd/system/longhun-internal-net.service"
    
    cat > /tmp/longhun-internal-net.service << EOF
[Unit]
Description=龍魂内网互联节点
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$INSTALL_DIR
Environment="LONGHUN_ROLE=$ROLE"
Environment="LONGHUN_DEVICE_NAME=$DEVICE_NAME"
Environment="LONGHUN_DEVICE_TYPE=$DEVICE_TYPE"
Environment="LONGHUN_GATEWAY=$GATEWAY"
Environment="LONGHUN_GATEWAY_PORT=$PORT"
ExecStart=$INSTALL_DIR/scripts/longhun-$([ "$ROLE" = "gateway" ] && echo "api-gateway.py --host 0.0.0.0 --port $PORT" || echo "peer-client.py $DEVICE_NAME $DEVICE_TYPE $GATEWAY --port $PORT --daemon")
Restart=always
RestartSec=10
StandardOutput=append:$INSTALL_DIR/logs/service.log
StandardError=append:$INSTALL_DIR/logs/service.log

[Install]
WantedBy=multi-user.target
EOF

    sudo mv /tmp/longhun-internal-net.service "$SERVICE_FILE"
    sudo systemctl daemon-reload
    sudo systemctl enable longhun-internal-net
    
    echo -e "${GREEN}   ✅ systemd 服务已配置${NC}"
    echo "   启动: sudo systemctl start longhun-internal-net"
    echo "   状态: sudo systemctl status longhun-internal-net"
    echo "   日志: sudo journalctl -u longhun-internal-net -f"
}

# ── 配置 launchd 自启动 (Mac) ──
setup_launchd() {
    if [ "$OS" != "Darwin" ]; then
        return
    fi

    echo -e "${YELLOW}⚙️ 配置 launchd 自启动...${NC}"
    
    PLIST_FILE="$HOME/Library/LaunchAgents/com.longhun.internal-net.plist"
    
    if [ "$ROLE" = "gateway" ]; then
        PROGRAM="$INSTALL_DIR/scripts/longhun-api-gateway.py"
        PROGRAM_ARGS="--host 0.0.0.0 --port $PORT"
    else
        PROGRAM="$INSTALL_DIR/scripts/longhun-peer-client.py"
        PROGRAM_ARGS="$DEVICE_NAME $DEVICE_TYPE $GATEWAY --port $PORT --daemon"
    fi
    
    cat > "$PLIST_FILE" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.longhun.internal-net</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>$PROGRAM</string>
        $(echo "$PROGRAM_ARGS" | xargs -n1 | sed 's/.*/<string>&<\/string>/')
    </array>
    <key>EnvironmentVariables</key>
    <dict>
        <key>LONGHUN_ROLE</key>
        <string>$ROLE</string>
        <key>LONGHUN_DEVICE_NAME</key>
        <string>$DEVICE_NAME</string>
        <key>LONGHUN_DEVICE_TYPE</key>
        <string>$DEVICE_TYPE</string>
        <key>LONGHUN_GATEWAY</key>
        <string>$GATEWAY</string>
    </dict>
    <key>WorkingDirectory</key>
    <string>$INSTALL_DIR</string>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>$INSTALL_DIR/logs/service.log</string>
    <key>StandardErrorPath</key>
    <string>$INSTALL_DIR/logs/service.log</string>
</dict>
</plist>
EOF

    launchctl load "$PLIST_FILE" 2>/dev/null
    echo -e "${GREEN}   ✅ launchd 服务已配置 (开机自启)${NC}"
}

# ── Docker 模式安装 ──
install_docker_mode() {
    echo -e "${YELLOW}🐳 Docker 模式安装...${NC}"
    
    # 确保 Docker 可用
    install_docker
    
    # 构建镜像
    if [ -f "$SCRIPT_DIR/../../../docker/Dockerfile.internal-net" ]; then
        DOCKERFILE="$(cd "$SCRIPT_DIR/../../.." && pwd)/docker/Dockerfile.internal-net"
        CONTEXT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
        
        echo -e "${YELLOW}🔨 构建 Docker 镜像...${NC}"
        docker build -t longhun/internal-net:latest -f "$DOCKERFILE" "$CONTEXT"
        echo -e "${GREEN}   ✅ 镜像构建完成${NC}"
    else
        echo -e "${YELLOW}   Dockerfile 不在本地，跳过构建。${NC}"
        echo -e "${YELLOW}   请确保已构建镜像: docker build -t longhun/internal-net:latest -f docker/Dockerfile.internal-net .${NC}"
    fi
    
    # 根据角色启动
    case "$ROLE" in
        gateway)
            echo -e "${GREEN}🚀 启动网关容器...${NC}"
            docker run -d \
                --name longhun-gateway \
                --network host \
                --restart unless-stopped \
                -e LONGHUN_ROLE=gateway \
                -e LONGHUN_DEVICE_NAME="$DEVICE_NAME" \
                -e LONGHUN_DEVICE_TYPE="$DEVICE_TYPE" \
                -e LONGHUN_GATEWAY_PORT="$PORT" \
                -v longhun-gateway-data:/opt/longhun/data \
                -v longhun-gateway-logs:/opt/longhun/logs \
                -v longhun-gateway-cache:/opt/longhun/cache \
                longhun/internal-net:latest gateway
            ;;
        peer)
            echo -e "${GREEN}🚀 启动节点容器...${NC}"
            docker run -d \
                --name longhun-peer \
                --network host \
                --restart unless-stopped \
                -e LONGHUN_ROLE=peer \
                -e LONGHUN_DEVICE_NAME="$DEVICE_NAME" \
                -e LONGHUN_DEVICE_TYPE="$DEVICE_TYPE" \
                -e LONGHUN_GATEWAY="$GATEWAY" \
                -e LONGHUN_GATEWAY_PORT="$PORT" \
                -v longhun-peer-data:/opt/longhun/data \
                -v longhun-peer-logs:/opt/longhun/logs \
                longhun/internal-net:latest peer
            ;;
        all)
            echo -e "${GREEN}🚀 一键启动全部节点 (Docker Compose)...${NC}"
            if [ -f "$SCRIPT_DIR/../../../docker/docker-compose.internal-net.yml" ]; then
                COMPOSE_FILE="$(cd "$SCRIPT_DIR/../../.." && pwd)/docker/docker-compose.internal-net.yml"
                docker compose -f "$COMPOSE_FILE" --profile all up -d
                echo -e "${GREEN}   ✅ 全部节点已启动${NC}"
                echo ""
                echo "   查看状态: docker compose -f $COMPOSE_FILE --profile all ps"
                echo "   查看日志: docker compose -f $COMPOSE_FILE --profile all logs -f"
                echo "   停止全部: docker compose -f $COMPOSE_FILE --profile all down"
            else
                echo -e "${RED}   未找到 compose 文件${NC}"
            fi
            ;;
    esac
    
    echo ""
    echo -e "${GREEN}════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}  🐉 龍魂内网节点部署完成${NC}"
    echo -e "${GREEN}════════════════════════════════════════════════════════${NC}"
    if [ "$ROLE" = "gateway" ]; then
        echo "  网关地址: http://$(hostname -I 2>/dev/null | awk '{print $1}' || echo 'localhost'):$PORT"
        echo "  健康检查: curl http://localhost:$PORT/health"
        echo "  查看节点: curl http://localhost:$PORT/peers"
    elif [ "$ROLE" = "peer" ]; then
        echo "  查看日志: docker logs -f longhun-peer"
    fi
    echo ""
}

# ═══════════════════════════════════════════════════════════
# 主流程
# ═══════════════════════════════════════════════════════════

main() {
    print_banner
    detect_system
    
    # 仅装依赖
    if [ "$DEPS_ONLY" = true ]; then
        install_python_deps
        echo -e "${GREEN}✅ 依赖安装完成${NC}"
        exit 0
    fi
    
    # Docker 模式
    if [ "$USE_DOCKER" = true ]; then
        install_docker_mode
        exit 0
    fi
    
    # 原生模式
    install_python_deps
    install_scripts
    
    echo ""
    echo -e "${CYAN}📋 安装配置:${NC}"
    echo "   角色:     $ROLE"
    echo "   设备:     $DEVICE_NAME ($DEVICE_TYPE)"
    echo "   网关:     $GATEWAY"
    echo "   端口:     $PORT"
    echo "   安装目录: $INSTALL_DIR"
    echo ""
    
    # 配置自启动
    case "$OS" in
        Linux)  setup_systemd ;;
        Darwin) setup_launchd ;;
    esac
    
    # 启动
    echo ""
    echo -e "${GREEN}════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}  🐉 龍魂内网节点安装完成${NC}"
    echo -e "${GREEN}════════════════════════════════════════════════════════${NC}"
    echo ""
    
    if [ "$ROLE" = "gateway" ]; then
        echo "  手动启动网关:"
        echo "    python3 $INSTALL_DIR/scripts/longhun-api-gateway.py --host 0.0.0.0 --port $PORT"
        echo ""
        echo "  或使用 systemd:"
        echo "    sudo systemctl start longhun-internal-net"
    else
        echo "  手动启动节点:"
        echo "    python3 $INSTALL_DIR/scripts/longhun-peer-client.py '$DEVICE_NAME' '$DEVICE_TYPE' '$GATEWAY' --port $PORT"
        echo ""
        echo "  或使用 systemd:"
        echo "    sudo systemctl start longhun-internal-net"
    fi
    
    echo ""
    echo "  安全措施 (自动启用):"
    echo "    L0·DNA签名验证"
    echo "    L1·三色审计追踪"
    echo "    L2·熔断控制"
    echo "    L3·输入过滤"
    echo "    L4·防投毒隔离"
    echo "    L5·芯片门禁"
    echo ""
}

main
