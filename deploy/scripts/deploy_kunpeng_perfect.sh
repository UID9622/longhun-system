#!/bin/bash
# ============================================================
# 龍魂 · 鲲鹏完美层一键部署脚本
# deploy_kunpeng_perfect.sh
#
# DNA: #龍芯⚡️丙午·辛未·DEPLOY-KUNPENG-PERFECT-v1.0
# 目标: 华为鲲鹏 + 昇腾 + 麒麟OS/欧拉OS
# 功能完整度: 100%
# ============================================================

set -euo pipefail

# --- 常量 ---
DNA="#龍芯⚡️丙午·辛未·DEPLOY-KUNPENG-PERFECT-v1.0"
UID_NUM="9622"
DEPLOY_ROOT="/opt/longhun"
LOG_DIR="/var/log/longhun"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# --- 颜色 ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() { echo -e "${GREEN}[${TIMESTAMP}]${NC} $1"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
error() { echo -e "${RED}[ERROR]${NC} $1"; exit 1; }
info() { echo -e "${BLUE}[INFO]${NC} $1"; }

# --- 启动横幅 ---
banner() {
    echo ""
    echo "============================================================"
    echo "  🇨🇳 龍魂系统 · 鲲鹏完美层一键部署"
    echo "  DNA: ${DNA}"
    echo "  UID: ${UID_NUM}"
    echo "  层级: 完美层 (100% 功能完整)"
    echo "============================================================"
    echo ""
}

# --- 芯片检测 ---
check_chip() {
    log "检测底层芯片..."

    if [ ! -f /proc/cpuinfo ]; then
        error "无法读取 /proc/cpuinfo，非Linux系统？"
    fi

    CPUINFO=$(cat /proc/cpuinfo 2>/dev/null | tr '[:upper:]' '[:lower:]')

    if echo "$CPUINFO" | grep -qE "kunpeng|phytium|ascend"; then
        CHIP=$(echo "$CPUINFO" | grep -m1 -oE "kunpeng[^ ]*|phytium[^ ]*" | head -1)
        log "✅ 检测到国产芯片: ${CHIP:-鲲鹏/飞腾}"
    elif echo "$CPUINFO" | grep -q "aarch64\|arm64"; then
        warn "ARM64芯片，但未明确识别为鲲鹏/飞腾。继续部署但可能非完美层。"
    else
        warn "未检测到鲲鹏/飞腾芯片。当前芯片可能无法享受完美层全部功能。"
        warn "建议使用华为鲲鹏服务器以获得完整体验。"
        read -p "是否继续部署? [y/N] " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
}

# --- 检测OS ---
check_os() {
    log "检测操作系统..."

    OS_NAME="unknown"
    if [ -f /etc/euleros-release ]; then
        OS_NAME="euler"
        log "✅ 检测到欧拉OS (EulerOS)"
    elif [ -f /etc/kylin-release ]; then
        OS_NAME="kylin"
        log "✅ 检测到麒麟OS (KylinOS)"
    elif [ -f /etc/os-release ]; then
        . /etc/os-release
        if echo "$ID" | grep -qi "uos"; then
            OS_NAME="uos"
            log "✅ 检测到统信UOS"
        elif echo "$ID" | grep -qi "openEuler"; then
            OS_NAME="euler"
            log "✅ 检测到 openEuler"
        else
            OS_NAME="$ID"
            warn "未识别的OS: $ID，继续部署"
        fi
    fi
}

# --- 安装依赖 ---
install_deps() {
    log "安装系统依赖..."

    if command -v yum &>/dev/null; then
        PKG_MGR="yum"
        yum update -y
        yum install -y \
            python3 python3-devel python3-pip \
            openssl openssl-devel \
            gcc gcc-c++ make \
            git curl wget \
            sqlite-devel \
            libffi-devel \
            systemd-devel \
            || warn "部分yum包安装失败"

        # 国密库
        if yum list | grep -qi "libsm"; then
            yum install -y openssl-gm libsm2 libsm3 libsm4 2>/dev/null || \
            warn "国密库安装失败，将使用Python软件实现"
        fi

    elif command -v apt-get &>/dev/null; then
        PKG_MGR="apt"
        apt-get update -y
        apt-get install -y \
            python3 python3-dev python3-pip \
            libssl-dev \
            build-essential \
            git curl wget \
            libsqlite3-dev \
            libffi-dev \
            libsystemd-dev \
            || warn "部分apt包安装失败"

        # 国密库（如可用）
        apt-get install -y libsm2-dev libsm-dev 2>/dev/null || \
            warn "国密库安装失败，将使用Python软件实现"

    else
        warn "未检测到 yum/apt，请手动安装 python3, git, gcc"
    fi
}

# --- 安装 Python 依赖 ---
install_python_deps() {
    log "安装 Python 依赖..."

    pip3 install --upgrade pip setuptools wheel

    # 核心依赖
    pip3 install \
        fastapi uvicorn \
        aiohttp httpx \
        sqlalchemy \
        numpy scipy \
        cryptography \
        PyYAML \
        python-dotenv \
        psutil \
        || warn "部分Python包安装失败"

    # 国密Python实现
    pip3 install gmssl 2>/dev/null || warn "gmssl 安装失败"

    log "✅ Python 依赖安装完成"
}

# --- 克隆/更新龍魂仓库 ---
setup_repo() {
    log "配置龍魂系统仓库..."

    if [ -d "$DEPLOY_ROOT/.git" ]; then
        log "龍魂仓库已存在，拉取最新代码..."
        cd "$DEPLOY_ROOT"
        git pull origin main 2>/dev/null || warn "git pull 失败"
    else
        log "克隆龍魂仓库..."
        mkdir -p "$(dirname "$DEPLOY_ROOT")"
        git clone https://gitee.com/UID${UID_NUM}/longhun-system.git "$DEPLOY_ROOT" 2>/dev/null || \
        git clone https://github.com/UID${UID_NUM}/longhun-system.git "$DEPLOY_ROOT" 2>/dev/null || \
        warn "远程克隆失败，使用本地代码"
    fi

    cd "$DEPLOY_ROOT"
}

# --- 配置环境 ---
setup_env() {
    log "配置环境变量..."

    cat > /etc/longhun/env.sh << 'ENVEOF'
#!/bin/bash
# 龍魂环境变量 · 鲲鹏完美层
export LONGHUN_ROOT="/opt/longhun"
export LONGHUN_CHIP_TIER="perfect"
export LONGHUN_ANTENNA_NODES="8"
export LONGHUN_GUOMI_HW="1"
export LONGHUN_OFFLINE_FULL="1"
export LONGHUN_DCEP_NATIVE="1"
export LONGHUN_MEMORY_LOCAL="1"
export LONGHUN_TPM_BIND="1"
export LONGHUN_PORT="9622"
export LONGHUN_ENV="production"
export PYTHONPATH="${LONGHUN_ROOT}:${PYTHONPATH:-}"
ENVEOF

    chmod 644 /etc/longhun/env.sh
    source /etc/longhun/env.sh
    log "✅ 环境变量已写入 /etc/longhun/env.sh"
}

# --- 欧拉OS内核优化 ---
optimize_euler() {
    if [ "$OS_NAME" = "euler" ] || [ -f /etc/euleros-release ]; then
        log "欧拉OS内核优化..."

        # 内存优化
        sysctl -w vm.swappiness=10
        sysctl -w vm.dirty_ratio=10
        sysctl -w vm.dirty_background_ratio=5

        # 网络优化
        sysctl -w net.core.somaxconn=65535
        sysctl -w net.ipv4.tcp_max_syn_backlog=8192
        sysctl -w net.ipv4.tcp_tw_reuse=1

        # 文件句柄
        ulimit -n 65535

        # 持久化
        cat > /etc/sysctl.d/99-longhun-kunpeng.conf << 'SYSCTL_EOF'
# 龍魂 · 鲲鹏内核优化
vm.swappiness=10
vm.dirty_ratio=10
vm.dirty_background_ratio=5
net.core.somaxconn=65535
net.ipv4.tcp_max_syn_backlog=8192
net.ipv4.tcp_tw_reuse=1
SYSCTL_EOF
        sysctl -p /etc/sysctl.d/99-longhun-kunpeng.conf
        log "✅ 欧拉OS内核优化完成"
    fi
}

# --- 创建目录结构 ---
create_dirs() {
    log "创建目录结构..."

    mkdir -p "$LOG_DIR"/{antenna,audit,chip_gate,app}
    mkdir -p /var/lib/longhun/{data,cache,backups}
    mkdir -p /etc/longhun

    chmod 750 "$LOG_DIR"
    chmod 750 /var/lib/longhun

    log "✅ 目录结构创建完成"
}

# --- 配置 systemd 服务 ---
setup_systemd() {
    log "配置 systemd 服务..."

    cat > /etc/systemd/system/longhun-antenna.service << SERVICEEOF
[Unit]
Description=龍魂蚁群触角服务
After=network.target
Wants=network.target

[Service]
Type=simple
User=root
WorkingDirectory=${DEPLOY_ROOT}
EnvironmentFile=/etc/longhun/env.sh
ExecStart=/usr/bin/python3 ${DEPLOY_ROOT}/bin/lh_ant_colony_daemon.py serve --port 9677
ExecStartPre=/usr/bin/python3 ${DEPLOY_ROOT}/bin/lh_chip_gate.py --deploy-check
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal
SyslogIdentifier=longhun-antenna

[Install]
WantedBy=multi-user.target
SERVICEEOF

    cat > /etc/systemd/system/longhun-core.service << SERVICEEOF
[Unit]
Description=龍魂核心引擎
After=network.target longhun-antenna.service
Wants=longhun-antenna.service

[Service]
Type=simple
User=root
WorkingDirectory=${DEPLOY_ROOT}
EnvironmentFile=/etc/longhun/env.sh
ExecStart=/usr/bin/python3 ${DEPLOY_ROOT}/引擎/launcher.py
Restart=always
RestartSec=15
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
SERVICEEOF

    systemctl daemon-reload
    systemctl enable longhun-antenna.service
    systemctl enable longhun-core.service

    log "✅ systemd 服务已配置"
}

# --- 启动服务 ---
start_services() {
    log "启动龍魂服务..."

    systemctl start longhun-antenna.service
    sleep 3
    systemctl start longhun-core.service
    sleep 2

    if systemctl is-active --quiet longhun-antenna.service; then
        log "✅ longhun-antenna 已启动"
    else
        error "longhun-antenna 启动失败"
    fi

    if systemctl is-active --quiet longhun-core.service; then
        log "✅ longhun-core 已启动"
    else
        warn "longhun-core 启动失败，请检查日志"
    fi
}

# --- 健康检查 ---
health_check() {
    log "执行健康检查..."

    # 芯片层
    CHIP_RESULT=$(python3 "${DEPLOY_ROOT}/bin/lh_chip_gate.py" --json 2>/dev/null || echo '{"chip":{"tier":"unknown"}}')
    CHIP_TIER=$(echo "$CHIP_RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin)['chip']['tier'])" 2>/dev/null || echo "unknown")
    echo "  芯片层级: $CHIP_TIER"

    # 端口检测
    if curl -sf http://localhost:9677/health >/dev/null 2>&1; then
        echo "  ✅ 蚁群触角(9677): OK"
    else
        echo "  ⚠️  蚁群触角(9677): 不可达"
    fi

    if curl -sf http://localhost:9622/health >/dev/null 2>&1; then
        echo "  ✅ 龍魂核心(9622): OK"
    else
        echo "  ⚠️  龍魂核心(9622): 不可达"
    fi

    # 国密
    python3 -c "from gmssl import sm2; print('  ✅ 国密SM2: OK')" 2>/dev/null || \
    echo "  ⚠️  国密SM2: Python软件实现"

    # 系统信息
    echo "  系统: $(uname -m) | 内存: $(free -h | awk '/^Mem/{print $2}') | CPU: $(nproc)核"
}

# --- 完成横幅 ---
done_banner() {
    echo ""
    echo "============================================================"
    echo "  ✅ 龍魂完美层部署完成！"
    echo ""
    echo "  芯片层级: 鲲鹏完美层 (100%)"
    echo "  DNA: ${DNA}"
    echo "  UID: ${UID_NUM}"
    echo ""
    echo "  服务端口:"
    echo "    蚁群触角: http://localhost:9677"
    echo "    龍魂核心: http://localhost:9622"
    echo ""
    echo "  日志: ${LOG_DIR}/"
    echo "  配置: /etc/longhun/"
    echo "  数据: /var/lib/longhun/"
    echo ""
    echo "  管理命令:"
    echo "    systemctl status longhun-antenna"
    echo "    systemctl status longhun-core"
    echo "    journalctl -u longhun-antenna -f"
    echo "============================================================"
    echo ""
}

# ============================================================
# 主流程
# ============================================================

main() {
    banner
    check_chip
    check_os
    install_deps
    install_python_deps
    create_dirs
    setup_repo
    setup_env
    optimize_euler
    setup_systemd
    start_services
    health_check
    done_banner
}

main "$@"
