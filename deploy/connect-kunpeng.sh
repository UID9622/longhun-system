#!/usr/bin/env bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 🐉 龍魂 · 鲲鹏服务器 mgmt 连接脚本
# 支持: 密码登录 (首次) → 自动装密钥 → 后续免密
# DNA: #龍芯⚡️2026-07-06-KUNPENG-CONNECT-v2.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# GPG: 9622-ONLY

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CONFIG_FILE="${SCRIPT_DIR}/.kunpeng_config"
AUTH_FILE="${SCRIPT_DIR}/.kunpeng_auth"          # 密码临时暂存（首次用完即删）
LOG_FILE="${SCRIPT_DIR}/connect.log"

# ─── 颜色 ───
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'; BOLD='\033[1m'; NC='\033[0m'

log()  { echo -e "$(date '+%H:%M:%S') $*" | tee -a "$LOG_FILE"; }
ok()   { log "${GREEN}✅${NC} $*"; }
warn() { log "${YELLOW}⚠️${NC}  $*"; }
fail() { log "${RED}🔴${NC} $*"; exit 1; }
info() { log "${CYAN}▶${NC}  $*"; }
header() { echo -e "\n${BOLD}${CYAN}$*${NC}"; }

# ─── 加载配置 ───
load_config() {
    if [[ -f "$CONFIG_FILE" ]]; then
        source "$CONFIG_FILE"
        ok "已加载连接配置"
    else
        warn "首次使用，先配置一下（就 3 个问题）"
        configure
    fi
}

# ─── 超级简化的配置流程 ───
configure() {
    header "🐉 龍魂 · 鲲鹏服务器连接配置"
    echo ""
    echo "  只需要 3 个信息："
    echo ""

    read -r -p "  ① 鲲鹏 mgmt IP 地址: " KUNPENG_MGMT_IP
    read -r -p "  ② SSH 用户名 [默认 root]: " KUNPENG_USER
    KUNPENG_USER="${KUNPENG_USER:-root}"
    read -r -p "  ③ SSH 端口 [默认 22]: " KUNPENG_SSH_PORT
    KUNPENG_SSH_PORT="${KUNPENG_SSH_PORT:-22}"
    echo ""
    echo "  ⚡ 密码等连接时再输入，输入后系统自动生成密钥替换密码"
    echo ""

    # 写入基础配置（不含密码）
    cat > "$CONFIG_FILE" << EOF
# 龍魂·鲲鹏连接配置
# DNA: #龍芯⚡️2026-07-06-KUNPENG-CONFIG-v2.0
KUNPENG_MGMT_IP="${KUNPENG_MGMT_IP}"
KUNPENG_USER="${KUNPENG_USER}"
KUNPENG_SSH_PORT="${KUNPENG_SSH_PORT}"
KUNPENG_DEPLOY_PATH="${KUNPENG_DEPLOY_PATH:-/opt/longhun-system}"
KUNPENG_RUN_USER="${KUNPENG_RUN_USER:-longhun}"
KUNPENG_KEY="${HOME}/.ssh/longhun_kunpeng_ed25519"
KUNPENG_DOMAIN=""
EOF
    chmod 600 "$CONFIG_FILE"
    ok "配置已保存 → 接下来请执行 check 测试连接"
}

# ─── SSH 命令工厂（自动选密钥 or 密码） ───
_ssh_opts() {
    local opts="-p ${KUNPENG_SSH_PORT} -o StrictHostKeyChecking=accept-new -o ConnectTimeout=10"
    if [[ -f "${KUNPENG_KEY:-/nonexistent}" ]]; then
        opts="$opts -i ${KUNPENG_KEY}"
    fi
    echo "$opts"
}

ssh_cmd() {
    local opts
    opts=$(_ssh_opts)
    ssh $opts "${KUNPENG_USER}@${KUNPENG_MGMT_IP}" "$@"
}

# ─── 尝试密钥连接，失败则要求输入密码 ───
# 返回 0 = 密钥可用, 1 = 需要密码
try_key_auth() {
    if ssh_cmd "echo ok" &>/dev/null; then
        return 0
    fi
    return 1
}

# ─── 用 expect 通过密码连接并执行命令 ───
ssh_with_password() {
    local password="$1"
    shift
    # expect 是 macOS/Linux 自带工具，无需安装
    expect << EOFEXPECT
        set timeout 15
        spawn ssh -p ${KUNPENG_SSH_PORT} -o StrictHostKeyChecking=accept-new -o ConnectTimeout=10 ${KUNPENG_USER}@${KUNPENG_MGMT_IP} $*
        expect {
            "assword:"        { send "${password}\r" }
            "yes/no"          { send "yes\r"; exp_continue }
            "Connection refused" { puts "🔴 连接被拒绝"; exit 1 }
            timeout           { puts "🔴 连接超时"; exit 1 }
        }
        expect {
            "assword:"        { puts "🔴 密码错误"; exit 1 }
            eof
        }
        catch wait result
        exit [lindex \$result 3]
EOFEXPECT
}

# ─── 交互式 SSH（给用户自己玩的） ───
interactive() {
    info "进入交互式 SSH 会话..."
    if try_key_auth; then
        exec ssh $(_ssh_opts) "${KUNPENG_USER}@${KUNPENG_MGMT_IP}"
    else
        echo ""
        warn "密钥不可用，请手动输入密码登录"
        exec ssh $(_ssh_opts) "${KUNPENG_USER}@${KUNPENG_MGMT_IP}"
    fi
}

# ─── 生成密钥对 + 密码登录装密钥 → 以后免密 ───
setup_key_auth() {
    local pw="$1"

    header "🔑 设置免密登录"

    # 1. 如果密钥不存在则生成
    if [[ ! -f "${KUNPENG_KEY}" ]]; then
        info "生成 ED25519 密钥对..."
        ssh-keygen -t ed25519 -f "${KUNPENG_KEY}" -N "" -C "longhun-kunpeng-$(date +%Y%m%d)" -q
        ok "密钥已生成: ${KUNPENG_KEY}"
    fi

    # 2. 读取公钥
    local pubkey
    pubkey=$(cat "${KUNPENG_KEY}.pub")
    info "公钥: ${pubkey:0:60}..."

    # 3. 用 expect 密码登录，把公钥写入服务器
    info "正在用密码登录并安装公钥..."
    expect << EOFEXPECT
        set timeout 30
        spawn ssh -p ${KUNPENG_SSH_PORT} -o StrictHostKeyChecking=accept-new -o ConnectTimeout=10 ${KUNPENG_USER}@${KUNPENG_MGMT_IP} "mkdir -p ~/.ssh && chmod 700 ~/.ssh && echo '${pubkey}' >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"
        expect {
            "assword:"        { send "${pw}\r" }
            "yes/no"          { send "yes\r"; exp_continue }
            "Connection refused" { puts "🔴 连接被拒绝"; exit 1 }
            timeout           { puts "🔴 连接超时"; exit 1 }
        }
        expect {
            "assword:"        { puts "🔴 密码错误"; exit 1 }
            eof
        }
        catch wait result
        exit [lindex \$result 3]
EOFEXPECT

    # 4. 验证密钥是否生效
    if try_key_auth; then
        ok "免密登录设置成功！以后不需要密码了 🎉"
        # 删除临时密码文件（如果存在）
        rm -f "$AUTH_FILE"
        return 0
    else
        fail "密钥安装失败，请检查密码是否正确"
    fi
}

# ─── 一键部署（核心入口） ───
deploy() {
    header "🚀 龍魂 · 鲲鹏一键部署"
    echo ""

    # 需要密码吗？
    if ! try_key_auth; then
        echo "  需要你的密码来初始连接（仅此一次，之后用密钥）"
        echo ""
        read -r -s -p "  请输入 ${KUNPENG_USER}@${KUNPENG_MGMT_IP} 的密码: " password
        echo ""

        if [[ -z "$password" ]]; then
            fail "密码不能为空"
        fi

        setup_key_auth "$password"
        # 密码存内存，用完即弃，不落盘
        unset password
    else
        ok "密钥连接正常，跳过密码"
    fi

    echo ""
    info "=== Step 1/4 服务端环境预检 ==="
    server_check

    echo ""
    info "=== Step 2/4 上传环境准备脚本 ==="
    scp -P "${KUNPENG_SSH_PORT}" -i "${KUNPENG_KEY}" \
        -o StrictHostKeyChecking=accept-new \
        "${SCRIPT_DIR}/prepare-openEuler.sh" \
        "${KUNPENG_USER}@${KUNPENG_MGMT_IP}:/tmp/prepare-openEuler.sh" 2>/dev/null || {
            # scp -i 失败，用 ssh + stdin
            ssh_cmd "cat > /tmp/prepare-openEuler.sh" < "${SCRIPT_DIR}/prepare-openEuler.sh"
        }
    ok "环境脚本已上传"

    echo ""
    info "=== Step 3/4 执行 openEuler 环境准备 ==="
    ssh_cmd "bash /tmp/prepare-openEuler.sh" || warn "部分环境准备有警告，继续..."

    echo ""
    info "=== Step 4/4 同步龍魂系统文件 ==="
    do_full_sync

    echo ""
    info "=== 部署 systemd 服务 ==="
    setup_services

    echo ""
    ok "🎉 鲲鹏 openEuler 部署完成！"
    echo ""
    echo "  📍 系统路径: ${KUNPENG_DEPLOY_PATH}"
    echo "  🌐 HTTP 端口: 80/443 (Nginx) + 9627 (Dashboard 直连)"
    echo ""
    echo "  验证命令:"
    echo "    curl http://${KUNPENG_MGMT_IP}:9627/"
    echo ""
    echo "  管理命令:"
    echo "    bash deploy/connect-kunpeng.sh ssh   # SSH 连上服务器"
    echo "    bash deploy/connect-kunpeng.sh sync  # 增量同步"
}

# ─── 服务器预检 ───
server_check() {
    info "目标: ${KUNPENG_USER}@${KUNPENG_MGMT_IP}:${KUNPENG_SSH_PORT}"

    echo ""
    ssh_cmd "cat /etc/openEuler-release 2>/dev/null || cat /etc/os-release 2>/dev/null | head -3" 2>/dev/null || echo "  (OS 信息暂不可用，继续...)"
    local arch
    arch=$(ssh_cmd "uname -m" 2>/dev/null || echo "unknown")
    if [[ "$arch" == "aarch64" ]]; then
        ok "架构: aarch64 (鲲鹏 ARM64) ✓"
    else
        warn "架构: $arch (预期 aarch64，但继续尝试)"
    fi
    ssh_cmd "lscpu 2>/dev/null | grep -E 'Model name|CPU\(s\)' | head -3" 2>/dev/null || true
    ssh_cmd "free -h 2>/dev/null | head -2" 2>/dev/null || true
    ssh_cmd "df -h / 2>/dev/null | tail -1" 2>/dev/null || true
    ssh_cmd "python3 --version 2>/dev/null || echo 'Python3: 待安装'" 2>/dev/null || true
}

# ─── 全量同步 ───
do_full_sync() {
    info "rsync 同步龍魂系统全文..."

    # 确保目标目录存在
    ssh_cmd "mkdir -p ${KUNPENG_DEPLOY_PATH}"

    # 构建排除参数
    local excludes=(
        ".git/" "__pycache__/" "*.pyc" "*.pyo" ".mypy_cache/" ".pytest_cache/"
        ".venv/" "venv/" "env/" "node_modules/" ".next/" "dist/" "build/"
        ".vscode/" ".idea/" ".DS_Store" "logs/" "*.log" "*.tmp" "*.swp"
        "*.dSYM/" "*.app/" ".master_key" "*.pem" "*_config.json"
        "*.db" "*.sqlite" "*.sqlite3"
        "deploy/.kunpeng_config" "deploy/.kunpeng_auth"
        "backups/" "_archived_reports/"
    )

    local exc_args=""
    for p in "${excludes[@]}"; do
        exc_args="$exc_args --exclude='$p'"
    done

    local longhun_root
    longhun_root="$(cd "$SCRIPT_DIR/.." && pwd)"

    eval rsync -avz --progress $exc_args \
        -e "ssh -p ${KUNPENG_SSH_PORT} -i ${KUNPENG_KEY} -o StrictHostKeyChecking=accept-new" \
        "${longhun_root}/" \
        "${KUNPENG_USER}@${KUNPENG_MGMT_IP}:${KUNPENG_DEPLOY_PATH}/"

    # 修正权限
    ssh_cmd "find ${KUNPENG_DEPLOY_PATH}/bin -name '*.sh' -exec chmod +x {} \\;" 2>/dev/null || true
    ssh_cmd "find ${KUNPENG_DEPLOY_PATH}/scripts -name '*.sh' -exec chmod +x {} \\;" 2>/dev/null || true
    ssh_cmd "find ${KUNPENG_DEPLOY_PATH}/deploy -name '*.sh' -exec chmod +x {} \\;" 2>/dev/null || true

    ok "文件同步完成"
}

# ─── systemd 服务部署 ───
setup_services() {
    info "配置 systemd 守护服务..."

    # Nginx 安装
    ssh_cmd "which nginx 2>/dev/null || dnf install -y nginx" 2>/dev/null || warn "Nginx 跳过（不影响核心服务）"

    # 创建运行用户
    ssh_cmd "id ${KUNPENG_RUN_USER} 2>/dev/null || useradd -r -s /sbin/nologin -d ${KUNPENG_DEPLOY_PATH} ${KUNPENG_RUN_USER}" 2>/dev/null || true
    ssh_cmd "chown -R ${KUNPENG_RUN_USER}:${KUNPENG_RUN_USER} ${KUNPENG_DEPLOY_PATH}" 2>/dev/null || true

    # 创建 systemd 服务
    local server_ip="${KUNPENG_MGMT_IP}"

    # 服务 1: 龍魂核心
    cat << EOF | ssh_cmd "cat > /etc/systemd/system/longhun-core.service"
[Unit]
Description=龍魂核心服务
After=network.target

[Service]
Type=simple
User=${KUNPENG_RUN_USER}
WorkingDirectory=${KUNPENG_DEPLOY_PATH}
Environment="PYTHONPATH=${KUNPENG_DEPLOY_PATH}"
ExecStart=/usr/bin/python3 ${KUNPENG_DEPLOY_PATH}/cnsh-core/server.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

    # 服务 2: Dashboard (Python HTTP server 在 9627)
    cat << EOF | ssh_cmd "cat > /etc/systemd/system/longhun-dashboard.service"
[Unit]
Description=龍魂操作台 Dashboard
After=network.target longhun-core.service

[Service]
Type=simple
User=${KUNPENG_RUN_USER}
WorkingDirectory=${KUNPENG_DEPLOY_PATH}/L5_服务层/services/dashboard/web
ExecStart=/usr/bin/python3 -m http.server 9627 --bind 0.0.0.0
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

    # 启用服务
    ssh_cmd "systemctl daemon-reload"
    ssh_cmd "systemctl enable longhun-core longhun-dashboard"
    ssh_cmd "systemctl restart longhun-core longhun-dashboard" || warn "服务启动待检查"

    # 防火墙
    ssh_cmd "firewall-cmd --permanent --add-port=9627/tcp 2>/dev/null" || true
    ssh_cmd "firewall-cmd --permanent --add-port=80/tcp 2>/dev/null" || true
    ssh_cmd "firewall-cmd --reload 2>/dev/null" || true

    # Nginx 反代（如有）
    if ssh_cmd "which nginx" 2>/dev/null | grep -q nginx; then
        cat << EOF | ssh_cmd "cat > /etc/nginx/conf.d/longhun.conf 2>/dev/null" 2>/dev/null || true
server {
    listen 80;
    server_name ${server_ip};

    location / {
        proxy_pass http://127.0.0.1:9627;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }

    location /api/ {
        proxy_pass http://127.0.0.1:8777;
        proxy_set_header Host \$host;
    }
}
EOF
        ssh_cmd "systemctl enable nginx && systemctl restart nginx" 2>/dev/null || true
    fi

    ok "systemd 服务已部署"
}

# ─── 增量同步 ───
incremental_sync() {
    info "增量同步中..."
    do_full_sync  # 复用，实际的增量由 rsync 自动处理
}

# ─── 双节点 CLI 快捷入口 ───

dual_node() {
    local cmd="${1:-status}"
    shift 2>/dev/null || true
    python3 "${SCRIPT_DIR}/../L6_同步层/dual_node_cli.py" "$cmd" "$@"
}

# ─── 主入口 ───
main() {
    echo ""
    echo "🐉 龍魂 · 鲲鹏连接工具 v3.0"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""

    load_config

    case "${1:-}" in
        config|configure)
            configure
            echo ""
            echo "  下一步: bash deploy/connect-kunpeng.sh deploy"
            ;;
        check)
            server_check
            ;;
        ssh|connect|login)
            interactive
            ;;
        key|setup-key)
            read -r -s -p "密码: " pw
            echo ""
            setup_key_auth "$pw"
            unset pw
            ;;
        sync)
            incremental_sync
            ;;
        sync5|sync-all)
            # 五维全量同步（新协议）
            python3 "${SCRIPT_DIR}/../L6_同步层/dual_node_protocol.py" sync --json
            ;;
        deploy)
            deploy
            ;;
        status|dual-status)
            # 双节点状态总览
            python3 "${SCRIPT_DIR}/../L6_同步层/dual_node_cli.py" status
            ;;
        ask)
            # 推理: bash deploy/connect-kunpeng.sh ask "问题"
            shift
            python3 "${SCRIPT_DIR}/../L6_同步层/dual_node_cli.py" ask "$@"
            ;;
        train)
            # 训练: bash deploy/connect-kunpeng.sh train 任务名 数据路径
            shift
            python3 "${SCRIPT_DIR}/../L6_同步层/dual_node_cli.py" train "$@"
            ;;
        train-status)
            shift
            python3 "${SCRIPT_DIR}/../L6_同步层/dual_node_cli.py" train-status "$@"
            ;;
        checkpoint|ckpt)
            shift
            python3 "${SCRIPT_DIR}/../L6_同步层/dual_node_cli.py" checkpoint "$@"
            ;;
        health)
            python3 "${SCRIPT_DIR}/../L6_同步层/dual_node_cli.py" health
            ;;
        api-init)
            # 初始化双节点API认证
            python3 "${SCRIPT_DIR}/../L6_同步层/auth_middleware.py" init --role mac
            echo ""
            echo "  ⚠️  请在鲲鹏端也执行: python3 L6_同步层/auth_middleware.py init --role kunpeng"
            echo "  然后将鲲鹏端的 peer_api_key 填入 Mac 端的 .dual_node_keys"
            ;;
        api-serve)
            # 启动本地双节点API（开发/调试用）
            python3 "${SCRIPT_DIR}/../L6_同步层/dual_node_api.py" serve --role mac --host 127.0.0.1 --port 9634
            ;;
        # ─── FRP 隧道命令 ───
        tunnel|frp)
            # FRP 隧道管理
            shift 2>/dev/null || true
            python3 "${SCRIPT_DIR}/../L6_同步层/dual_node_cli.py" tunnel "$@"
            ;;
        tunnel-install)
            python3 "${SCRIPT_DIR}/../L6_同步层/dual_node_cli.py" tunnel install
            ;;
        tunnel-start)
            python3 "${SCRIPT_DIR}/../L6_同步层/dual_node_cli.py" tunnel start
            ;;
        tunnel-stop)
            python3 "${SCRIPT_DIR}/../L6_同步层/dual_node_cli.py" tunnel stop
            ;;
        tunnel-status)
            python3 "${SCRIPT_DIR}/../L6_同步层/dual_node_cli.py" tunnel status
            ;;
        tunnel-dashboard)
            python3 "${SCRIPT_DIR}/../L6_同步层/dual_node_cli.py" tunnel dashboard
            ;;
        tunnel-daemon)
            shift 2>/dev/null || true
            python3 "${SCRIPT_DIR}/../L6_同步层/dual_node_cli.py" tunnel daemon "$@"
            ;;
        help|--help|-h)
            echo "用法: bash deploy/connect-kunpeng.sh [命令]"
            echo ""
            echo "  基础:"
            echo "    config      初次配置（IP + 用户名，30 秒）"
            echo "    deploy      一键部署 🚀（全程自动）"
            echo "    check       检测服务器状态"
            echo "    sync        增量同步代码（rsync）"
            echo "    ssh         交互式 SSH 终端"
            echo ""
            echo "  双节点同步:"
            echo "    status      双节点状态总览"
            echo "    sync5       五维全量同步（代码+协议+知识+记忆+模型）"
            echo "    ask \"问题\"  推理（本地优先→鲲鹏fallback）"
            echo "    train 任务名 数据路径  提交训练到鲲鹏"
            echo "    train-status 任务名    查询训练进度"
            echo "    checkpoint  查看/拉取最新模型"
            echo "    health      健康检查"
            echo ""
            echo "  FRP 隧道:"
            echo "    tunnel-install   安装 frpc"
            echo "    tunnel-start     启动隧道"
            echo "    tunnel-stop      停止隧道"
            echo "    tunnel-status    隧道状态"
            echo "    tunnel-dashboard  打开Web面板"
            echo "    tunnel-daemon     守护模式（自动重连）"
            echo ""
            echo "  API管理:"
            echo "    api-init    初始化双节点API认证"
            echo "    api-serve   启动本地双节点API"
            echo ""
            echo "  DNA: #龍芯⚡️丙午·辛未·KUNPENG-CONNECT-v4.0"
            ;;
        *)
            echo "  用法: deploy | check | sync | sync5 | status | ask | train | checkpoint | health | ssh | tunnel"
            echo "  建议: bash deploy/connect-kunpeng.sh deploy  ← 一键搞定"
            echo "  帮助: bash deploy/connect-kunpeng.sh help"
            ;;
    esac
}

main "$@"
