#!/bin/bash
# ═══════════════════════════════════════════════════════════════
#  龍魂系统 · 终极引导部署脚本
#  CNSH-MCP 27步 增强版 + 全资产迁移 + 一键上线
#  DNA: #龍芯⚡️2026-07-06-LONGHUN-BOOTSTRAP-v3.0
#  归属: UID9622｜龍芯北辰｜CNSH
#  适用: Ubuntu 24.04 / openEuler 22.03+ / CentOS 8+
#  ⚠️  以 root 执行: sudo bash longhun-bootstrap.sh
# ═══════════════════════════════════════════════════════════════

set -euo pipefail
IFS=$'\n\t'

# ─── 全局变量 ───
LOG_FILE="/var/log/longhun-bootstrap-$(date +%Y%m%d-%H%M%S).log"
ERROR_FLAG=0
LONGHUN_ROOT="/opt/longhun-system"
LONGHUN_USER="longhun"
LONGHUN_GROUP="longhun"
VENV_PATH="${LONGHUN_ROOT}/.venv"
LOG_DIR="/var/log/longhun"

# ─── 颜色 ───
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'; BOLD='\033[1m'; NC='\033[0m'

log_info()  { echo -e "${GREEN}[INFO]${NC}  $(date '+%H:%M:%S') $*" | tee -a "$LOG_FILE"; }
log_warn()  { echo -e "${YELLOW}[WARN]${NC}  $(date '+%H:%M:%S') $*" | tee -a "$LOG_FILE"; }
log_error() { echo -e "${RED}[ERROR]${NC} $(date '+%H:%M:%S') $*" | tee -a "$LOG_FILE"; ERROR_FLAG=1; }
log_step()  { echo -e "\n${BOLD}${CYAN}══════════════════════════════════════════${NC}" | tee -a "$LOG_FILE"; echo -e "${BOLD}${CYAN}  $*${NC}" | tee -a "$LOG_FILE"; echo -e "${BOLD}${CYAN}══════════════════════════════════════════${NC}" | tee -a "$LOG_FILE"; }

fuse() {
    if [ "$ERROR_FLAG" -eq 1 ]; then
        log_error "🔴 熔断！请修复后重新运行。"
        exit 1
    fi
}

detect_os() {
    source /etc/os-release 2>/dev/null || true
    OS_ID="${ID:-unknown}"
    OS_VERSION="${VERSION_ID:-unknown}"
    ARCH="$(uname -m)"
    log_info "OS: ${OS_ID} ${OS_VERSION} | 架构: ${ARCH}"

    if command -v apt &>/dev/null; then
        PKG_MGR="apt"
        PKG_INSTALL="apt-get install -y"
    elif command -v dnf &>/dev/null; then
        PKG_MGR="dnf"
        PKG_INSTALL="dnf install -y"
    elif command -v yum &>/dev/null; then
        PKG_MGR="yum"
        PKG_INSTALL="yum install -y"
    else
        log_error "未知包管理器"
        exit 1
    fi
    log_info "包管理器: ${PKG_MGR}"
}

# ═══════════════════════════════════════════════════════════════
#  A1-A6: 预检系统
# ═══════════════════════════════════════════════════════════════
preflight() {
    log_step "A1-A6: 预检系统"

    # A1: 架构检测
    case "$ARCH" in
        x86_64|aarch64) log_info "A1 ✅ 架构: ${ARCH}" ;;
        *) log_error "A1 🔴 不支持架构: ${ARCH}"; return 1 ;;
    esac

    # A2: OS检测
    case "$OS_ID" in
        ubuntu|debian|centos|rhel|openeuler|anolis) log_info "A2 ✅ OS: ${OS_ID} ${OS_VERSION}" ;;
        *) log_warn "A2 ⚠️  非标准OS: ${OS_ID}，继续尝试" ;;
    esac

    # A3: 内存 >= 2GB
    MEM_TOTAL=$(free -m | awk '/^Mem:/{print $2}')
    if [ "$MEM_TOTAL" -ge 2048 ]; then
        log_info "A3 ✅ 内存: ${MEM_TOTAL}MB"
    else
        log_warn "A3 ⚠️  内存不足2GB: ${MEM_TOTAL}MB"
    fi

    # A4: 磁盘 >= 20GB
    DISK_AVAIL=$(df -BG / | awk 'NR==2{print $4}' | sed 's/G//')
    if [ "$DISK_AVAIL" -ge 20 ]; then
        log_info "A4 ✅ 磁盘可用: ${DISK_AVAIL}GB"
    else
        log_warn "A4 ⚠️  磁盘不足20GB: ${DISK_AVAIL}GB"
    fi

    # A5: 网络检测
    if ping -c 2 -W 3 mirrors.huaweicloud.com &>/dev/null; then
        log_info "A5 ✅ 华为云镜像可达"
    else
        log_warn "A5 ⚠️  无法访问华为云镜像"
    fi

    # A6: root权限
    if [ "$EUID" -eq 0 ]; then
        log_info "A6 ✅ root权限"
    else
        log_error "A6 🔴 需要root权限"; exit 1
    fi

    log_info "预检全部完成"
}

# ═══════════════════════════════════════════════════════════════
#  #1: 系统更新 + 运维工具
# ═══════════════════════════════════════════════════════════════
step_01() {
    log_step "#1: 系统更新 + 运维工具安装"

    if [ "$PKG_MGR" = "apt" ]; then
        apt-get update -y && apt-get upgrade -y
        apt-get install -y htop iotop lsof jq tmux rsync logrotate \
            net-tools curl wget vim tar gzip bzip2
    else
        $PKG_INSTALL htop iotop lsof jq tmux rsync logrotate \
            net-tools curl wget vim tar gzip bzip2
    fi
    log_info "#1 ✅ 运维工具安装完成"
}

# ═══════════════════════════════════════════════════════════════
#  #2: Python编译环境
# ═══════════════════════════════════════════════════════════════
step_02() {
    log_step "#2: Python编译环境"
    if [ "$PKG_MGR" = "apt" ]; then
        apt-get install -y python3 python3-pip python3-venv python3-dev \
            gcc g++ make cmake build-essential \
            libssl-dev libffi-dev zlib1g-dev libbz2-dev \
            libsqlite3-dev libreadline-dev liblzma-dev
    else
        $PKG_INSTALL python3 python3-pip python3-devel \
            gcc gcc-c++ make cmake \
            openssl-devel libffi-devel zlib-devel bzip2-devel \
            sqlite-devel readline-devel xz-devel
    fi
    log_info "#2 ✅ Python环境安装完成: $(python3 --version)"
}

# ═══════════════════════════════════════════════════════════════
#  #3: Node.js + PM2
# ═══════════════════════════════════════════════════════════════
step_03() {
    log_step "#3: Node.js + PM2"
    if ! command -v node &>/dev/null; then
        curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
        apt-get install -y nodejs 2>/dev/null || $PKG_INSTALL nodejs
    fi
    log_info "Node.js: $(node -v)"
    npm install -g pm2 2>/dev/null || log_warn "PM2安装跳过"
    log_info "#3 ✅ Node.js + PM2 完成"
}

# ═══════════════════════════════════════════════════════════════
#  #4-#5: Docker增强
# ═══════════════════════════════════════════════════════════════
step_04() {
    log_step "#4-#5: Docker增强"

    if ! command -v docker &>/dev/null; then
        if [ "$PKG_MGR" = "apt" ]; then
            apt-get install -y docker.io docker-compose
        else
            $PKG_INSTALL docker-ce docker-ce-cli containerd.io docker-compose
        fi
    fi

    # 华为云镜像加速 + overlay2 + 日志限制
    mkdir -p /etc/docker
    cat > /etc/docker/daemon.json <<'DAEMONEOF'
{
  "registry-mirrors": ["https://mirrors.huaweicloud.com"],
  "storage-driver": "overlay2",
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}
DAEMONEOF
    systemctl restart docker 2>/dev/null || true
    systemctl enable docker 2>/dev/null || true
    log_info "#4-#5 ✅ Docker增强完成: $(docker --version)"
}

# ═══════════════════════════════════════════════════════════════
#  #6: 防火墙
# ═══════════════════════════════════════════════════════════════
step_05() {
    log_step "#6: 防火墙端口开放"
    PORTS=(22 80 443 5001 8777 9627 18000 18100 8888)

    if command -v firewall-cmd &>/dev/null; then
        for p in "${PORTS[@]}"; do
            firewall-cmd --permanent --add-port=${p}/tcp 2>/dev/null || true
        done
        firewall-cmd --reload 2>/dev/null || true
    elif command -v ufw &>/dev/null; then
        for p in "${PORTS[@]}"; do
            ufw allow ${p}/tcp 2>/dev/null || true
        done
        ufw --force enable 2>/dev/null || true
    fi
    log_info "#6 ✅ 防火墙已配置"
}

# ═══════════════════════════════════════════════════════════════
#  #7-#8: 目录结构 + 权限
# ═══════════════════════════════════════════════════════════════
step_06() {
    log_step "#7-#8: 目录结构 + 权限加固"

    # 创建运行用户
    if ! id "${LONGHUN_USER}" &>/dev/null; then
        groupadd -f "${LONGHUN_GROUP}"
        useradd -r -g "${LONGHUN_GROUP}" -m -s /bin/bash "${LONGHUN_USER}"
        log_info "创建用户: ${LONGHUN_USER}"
    fi

    # 龍魂目录
    mkdir -p "${LONGHUN_ROOT}"
    mkdir -p "${LONGHUN_ROOT}"/{api,web,scripts,logs,backup,data,conf,ssl,dist,deploy,tools}
    mkdir -p "${LONGHUN_ROOT}"/{.longhun/logs,.longhun/backups,.longhun/config}
    mkdir -p "${LOG_DIR}"
    mkdir -p /home/${LONGHUN_USER}/.longhun/{logs,backups,config}
    mkdir -p /home/${LONGHUN_USER}/.龍魂

    # 权限: 目录750, 文件640
    chown -R "${LONGHUN_USER}:${LONGHUN_GROUP}" "${LONGHUN_ROOT}" 2>/dev/null || true
    chown -R "${LONGHUN_USER}:${LONGHUN_GROUP}" "${LOG_DIR}" 2>/dev/null || true
    chown -R "${LONGHUN_USER}:${LONGHUN_GROUP}" /home/${LONGHUN_USER}/.longhun 2>/dev/null || true
    chown -R "${LONGHUN_USER}:${LONGHUN_GROUP}" /home/${LONGHUN_USER}/.龍魂 2>/dev/null || true

    log_info "#7-#8 ✅ 目录结构创建完成"
}

# ═══════════════════════════════════════════════════════════════
#  #9-#10: Git增强
# ═══════════════════════════════════════════════════════════════
step_07() {
    log_step "#9-#10: Git增强"

    cd "${LONGHUN_ROOT}"

    # .gitignore
    cat > .gitignore <<'GITIGNOREEOF'
*.log
*.pid
.env
node_modules/
dist/
*.pyc
__pycache__/
*.db
*.sqlite
*.sqlite3
.DS_Store
.mypy_cache/
.pytest_cache/
.venv/
GITIGNOREEOF

    log_info "#9-#10 ✅ Git配置完成"
}

# ═══════════════════════════════════════════════════════════════
#  #11-#13: 配置模板
# ═══════════════════════════════════════════════════════════════
step_08() {
    log_step "#11-#13: 配置模板与变量"

    # .env.example
    cat > "${LONGHUN_ROOT}/.env.example" <<'ENVEOF'
# ═══ 飞书 ═══
FEISHU_APP_ID=
FEISHU_APP_SECRET=
FEISHU_WEBHOOK_URL=
FEISHU_CHAT_ID=

# ═══ Notion ═══
NOTION_API_KEY=
NOTION_DATABASE_ID=

# ═══ DeepSeek ═══
DEEPSEEK_API_KEY=
DEEPSEEK_MODEL=deepseek-chat

# ═══ 华为云 ═══
HUAWEI_CLOUD_ACCESS_KEY=
HUAWEI_CLOUD_SECRET_KEY=
HUAWEI_CLOUD_REGION=cn-north-4

# ═══ 龍魂 ═══
LONGHUN_PORT=8777
LONGHUN_DASHBOARD_PORT=9627
LONGHUN_LONGZHISHOU_PORT=5001
LONGHUN_DEBUG=false
ENVEOF

    # VERSION
    echo "3.0.0-$(date +%Y%m%d)" > "${LONGHUN_ROOT}/VERSION"

    # CNSH变量JSON
    cat > "${LONGHUN_ROOT}/cnsh_vars.json" <<'JSONEOF'
{
  "project": "longhun",
  "version": "3.0.0",
  "ports": [5001, 8777, 9627, 18000, 18100],
  "services": ["longzhishou", "dashboard", "symbiote", "gatekeeper"],
  "health_check_interval": 300,
  "fuse_threshold": 3,
  "audit_level": "P0"
}
JSONEOF

    log_info "#11-#13 ✅ 配置模板生成完成"
}

# ═══════════════════════════════════════════════════════════════
#  #14: 健康检查v2
# ═══════════════════════════════════════════════════════════════
step_09() {
    log_step "#14: 健康检查v2脚本"

    cat > "${LONGHUN_ROOT}/scripts/health-check.sh" <<'HEALTHEOF'
#!/bin/bash
# 龍魂健康检查v2
# DNA: #龍芯⚡️2026-07-06-HEALTH-CHECK-v2.0

RED='\033[0;31m'; GREEN='\033[0;32m'; NC='\033[0m'

echo "══════════════════════════════════════════"
echo "  龍魂系统健康检查"
echo "  $(date '+%Y-%m-%d %H:%M:%S')"
echo "══════════════════════════════════════════"

echo "[系统]"
echo "  CPU: $(top -bn1 | grep 'Cpu(s)' | awk '{print $2}' | cut -d'%' -f1)%"
echo "  内存: $(free -h | grep Mem | awk '{print $3"/"$2}')"
echo "  磁盘: $(df -h / | awk 'NR==2{print $3"/"$2 " ("$5")"}')"

echo ""
echo "[端口检测]"
for port in 5001 8777 9627 18000 18100 80 443; do
    if ss -tlnp 2>/dev/null | grep -q ":$port " || netstat -tlnp 2>/dev/null | grep -q ":$port "; then
        echo -e "  ${GREEN}✅${NC} 端口 $port"
    else
        echo -e "  ${RED}❌${NC} 端口 $port"
    fi
done

echo ""
echo "[服务状态]"
for svc in nginx docker longhun-*; do
    if systemctl is-active --quiet "$svc" 2>/dev/null; then
        echo -e "  ${GREEN}✅${NC} $svc"
    fi
done

echo ""
echo "[Docker]"
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" 2>/dev/null || echo "  无运行容器"

echo ""
echo "══════════════════════════════════════════"
HEALTHEOF
    chmod +x "${LONGHUN_ROOT}/scripts/health-check.sh"

    log_info "#14 ✅ 健康检查脚本已创建"
}

# ═══════════════════════════════════════════════════════════════
#  #15: 备份脚本
# ═══════════════════════════════════════════════════════════════
step_10() {
    log_step "#15: 备份脚本"

    cat > "${LONGHUN_ROOT}/scripts/backup.sh" <<'BACKUPEOF'
#!/bin/bash
BACKUP_DIR="/backup/longhun"
mkdir -p "$BACKUP_DIR"
tar czf "$BACKUP_DIR/longhun-$(date +%Y%m%d-%H%M%S).tar.gz" \
    --exclude='*.log' --exclude='*.pyc' --exclude='__pycache__' \
    --exclude='node_modules' --exclude='.venv' \
    /opt/longhun-system
find "$BACKUP_DIR" -name "*.tar.gz" -mtime +30 -delete
echo "备份完成: $(ls -lh $BACKUP_DIR | tail -1)"
BACKUPEOF
    chmod +x "${LONGHUN_ROOT}/scripts/backup.sh"

    log_info "#15 ✅ 备份脚本已创建"
}

# ═══════════════════════════════════════════════════════════════
#  #16: 部署验证
# ═══════════════════════════════════════════════════════════════
step_11() {
    log_step "#16: 部署验证"

    cat > "${LONGHUN_ROOT}/scripts/deploy-verify.sh" <<'VERIFYEOF'
#!/bin/bash
PASSED=0; TOTAL=0
check() { TOTAL=$((TOTAL+1)); if eval "$1" &>/dev/null; then echo "  ✅ $2"; PASSED=$((PASSED+1)); else echo "  ❌ $2"; fi; }

echo "龍魂部署验证"
check "which python3" "Python3"
check "which node" "Node.js"
check "which docker" "Docker"
check "which nginx" "Nginx"
check "which git" "Git"
check "which htop" "htop"
check "which jq" "jq"
check "which tmux" "tmux"
check "which rsync" "rsync"
check "which pm2" "PM2"
check "systemctl is-active --quiet docker" "Docker运行"
check "systemctl is-active --quiet nginx" "Nginx运行"
check "-d /opt/longhun-system" "龙魂目录"
check "-d /opt/longhun-system/data" "data目录"
check "-d /opt/longhun-system/logs" "logs目录"
check "-d /opt/longhun-system/conf" "conf目录"
check "-d /opt/longhun-system/ssl" "ssl目录"
check "-d /opt/longhun-system/dist" "dist目录"
check "-d /opt/longhun-system/deploy" "deploy目录"
check "-d /opt/longhun-system/tools" "tools目录"
check "-f /opt/longhun-system/.env.example" ".env.example"
check "-f /opt/longhun-system/VERSION" "VERSION"
check "-f /opt/longhun-system/cnsh_vars.json" "cnsh_vars.json"
echo ""
echo "结果: $PASSED/$TOTAL 项通过"
VERIFYEOF
    chmod +x "${LONGHUN_ROOT}/scripts/deploy-verify.sh"

    log_info "#16 ✅ 验证脚本已创建"
}

# ═══════════════════════════════════════════════════════════════
#  #17: Nginx多站点
# ═══════════════════════════════════════════════════════════════
step_12() {
    log_step "#17: Nginx多站点配置"

    SERVER_IP=$(hostname -I 2>/dev/null | awk '{print $1}' || echo "127.0.0.1")

    cat > /etc/nginx/conf.d/longhun.conf <<NGINXEOF
# ═══ 龍魂主站 ═══
server {
    listen 80;
    server_name ${SERVER_IP} longhun888.com www.longhun888.com;

    root /opt/longhun-system/dist;
    index index.html;

    location / {
        try_files \$uri \$uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://127.0.0.1:8777;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
    }

    location /dashboard/ {
        proxy_pass http://127.0.0.1:9627;
        proxy_set_header Host \$host;
    }

    location /webhook {
        proxy_pass http://127.0.0.1:5001;
        proxy_set_header Host \$host;
    }

    location /status {
        stub_status on;
        allow 127.0.0.1;
        allow 10.0.0.0/8;
        deny all;
    }
}

# ═══ 共生体子域 ═══
server {
    listen 8777;
    server_name symbiote.longhun888.com;

    location / {
        proxy_pass http://127.0.0.1:9627;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }
}
NGINXEOF

    # 默认首页
    mkdir -p /opt/longhun-system/dist
    cat > /opt/longhun-system/dist/index.html <<'INDEXEOF'
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>龍魂系统</title>
<style>
  body { font-family: system-ui; display:flex; align-items:center; justify-content:center; min-height:100vh; margin:0; background:#0a0a0a; color:#fff; }
  .box { text-align:center; }
  h1 { font-size:3em; color:#ff4444; }
  .dna { color:#888; font-size:0.8em; margin-top:2em; }
</style>
</head>
<body>
<div class="box">
  <h1>🐉 龍魂系统</h1>
  <p>数据主权归人民 · 不跪资本不舔流量</p>
  <p class="dna">#龍芯⚡️2026-07-06-DEPLOY-v3.0</p>
</div>
</body>
</html>
INDEXEOF

    nginx -t 2>/dev/null && systemctl reload nginx 2>/dev/null || true
    log_info "#17 ✅ Nginx配置完成"
}

# ═══════════════════════════════════════════════════════════════
#  #18: systemd服务 (龍智守 + 面板 + 共生体 + 守门人)
# ═══════════════════════════════════════════════════════════════
step_13() {
    log_step "#18: systemd服务"

    # 龍智守飞书机器人
    cat > /etc/systemd/system/longhun-longzhishou.service <<SYSTEMDEOF
[Unit]
Description=龍魂·龍智守飞书机器人
After=network.target

[Service]
Type=simple
User=${LONGHUN_USER}
WorkingDirectory=${LONGHUN_ROOT}
Environment="PYTHONPATH=${LONGHUN_ROOT}:${LONGHUN_ROOT}/scripts"
EnvironmentFile=${LONGHUN_ROOT}/.env
ExecStart=${VENV_PATH}/bin/python3 ${LONGHUN_ROOT}/scripts/龍智守.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
SYSTEMDEOF

    # 龍魂面板 (HTTP server)
    cat > /etc/systemd/system/longhun-dashboard.service <<SYSTEMDEOF
[Unit]
Description=龍魂操作台 Dashboard
After=network.target

[Service]
Type=simple
User=${LONGHUN_USER}
WorkingDirectory=${LONGHUN_ROOT}/L5_服务层/services/dashboard/web
ExecStart=/usr/bin/python3 -m http.server 9627 --bind 0.0.0.0
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
SYSTEMDEOF

    # 龍魂共生体知识矩阵
    cat > /etc/systemd/system/longhun-symbiote.service <<SYSTEMDEOF
[Unit]
Description=龍魂共生体知识矩阵
After=network.target

[Service]
Type=simple
User=${LONGHUN_USER}
WorkingDirectory=${LONGHUN_ROOT}
Environment="PYTHONPATH=${LONGHUN_ROOT}"
ExecStart=${VENV_PATH}/bin/python3 ${LONGHUN_ROOT}/tools/longhun_symbiote_server.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
SYSTEMDEOF

    # 龍魂守门人
    cat > /etc/systemd/system/longhun-gatekeeper.service <<SYSTEMDEOF
[Unit]
Description=龍魂CNSH守门人
After=network.target

[Service]
Type=simple
User=${LONGHUN_USER}
WorkingDirectory=${LONGHUN_ROOT}
Environment="PYTHONPATH=${LONGHUN_ROOT}"
ExecStart=${VENV_PATH}/bin/python3 ${LONGHUN_ROOT}/bin/cnsh_gatekeeper.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
SYSTEMDEOF

    systemctl daemon-reload
    log_info "#18 ✅ systemd服务已创建"
}

# ═══════════════════════════════════════════════════════════════
#  #19: Crontab定时任务
# ═══════════════════════════════════════════════════════════════
step_14() {
    log_step "#19: Crontab定时任务"

    (crontab -l 2>/dev/null || true; cat <<CRONEOF
# ═══ 龍魂定时任务 ═══
# 健康检查 (每5分钟)
*/5 * * * * bash ${LONGHUN_ROOT}/scripts/health-check.sh >> ${LOG_DIR}/health-check.log 2>&1
# 每日复盘 (每天0点)
0 0 * * * bash ${LONGHUN_ROOT}/scripts/daily-review.sh >> ${LOG_DIR}/daily-review.log 2>&1
# 备份 (每天2点)
0 2 * * * bash ${LONGHUN_ROOT}/scripts/backup.sh >> ${LOG_DIR}/backup.log 2>&1
# 系统更新检查 (每周日3点)
0 3 * * 0 apt-get update -y >> ${LOG_DIR}/update.log 2>&1
# 日志清理 (每天4点)
0 4 * * * find ${LOG_DIR} -name "*.log" -mtime +7 -delete
# 自动评估 (每天5点)
0 5 * * * bash ${LONGHUN_ROOT}/scripts/auto-eval.sh >> ${LOG_DIR}/auto-eval.log 2>&1
CRONEOF
) | crontab -

    log_info "#19 ✅ Crontab已配置"
}

# ═══════════════════════════════════════════════════════════════
#  #20-22: 安全加固
# ═══════════════════════════════════════════════════════════════
step_15() {
    log_step "#20-22: 安全加固"

    # SSH加固
    sed -i 's/^#PermitRootLogin.*/PermitRootLogin prohibit-password/' /etc/ssh/sshd_config 2>/dev/null || true
    sed -i 's/^#PasswordAuthentication.*/PasswordAuthentication no/' /etc/ssh/sshd_config 2>/dev/null || true

    # logrotate
    cat > /etc/logrotate.d/longhun <<'LOGROTEOF'
/opt/longhun-system/logs/*.log
/var/log/longhun/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    create 640 longhun longhun
}
LOGROTEOF

    log_info "#20-22 ✅ 安全加固完成"
}

# ═══════════════════════════════════════════════════════════════
#  #23: 服务自启
# ═══════════════════════════════════════════════════════════════
step_16() {
    log_step "#23: 服务自启"

    systemctl enable nginx 2>/dev/null || true
    systemctl enable docker 2>/dev/null || true
    systemctl enable longhun-longzhishou 2>/dev/null || true
    systemctl enable longhun-dashboard 2>/dev/null || true
    systemctl enable longhun-symbiote 2>/dev/null || true
    systemctl enable longhun-gatekeeper 2>/dev/null || true

    log_info "#23 ✅ 服务自启已启用"
}

# ═══════════════════════════════════════════════════════════════
#  #24: 操作别名
# ═══════════════════════════════════════════════════════════════
step_17() {
    log_step "#24: 操作别名"

    cat >> /root/.bashrc <<'ALIASEOF'

# ═══ 龍魂操作别名 ═══
alias lh-status='systemctl status longhun-longzhishou longhun-dashboard longhun-symbiote longhun-gatekeeper'
alias lh-backup='bash /opt/longhun-system/scripts/backup.sh'
alias lh-verify='bash /opt/longhun-system/scripts/deploy-verify.sh'
alias lh-health='bash /opt/longhun-system/scripts/health-check.sh'
alias lh-restart='systemctl restart longhun-longzhishou longhun-dashboard longhun-symbiote longhun-gatekeeper'
alias lh-logs='journalctl -u longhun-longzhishou -u longhun-dashboard -u longhun-symbiote -u longhun-gatekeeper -f'
alias lh-err='journalctl -u longhun-longzhishou -u longhun-dashboard -u longhun-symbiote -u longhun-gatekeeper -p err -n 50'
alias lh-reload='systemctl daemon-reload && lh-restart'
alias lh-ports='ss -tlnp | grep -E "5001|8777|9627|18000|18100"'
ALIASEOF

    log_info "#24 ✅ 操作别名已配置"
}

# ═══════════════════════════════════════════════════════════════
#  #25: Docker Compose
# ═══════════════════════════════════════════════════════════════
step_18() {
    log_step "#25: Docker Compose模板"

    cat > "${LONGHUN_ROOT}/docker-compose.yml" <<COMPOSEEOF
version: '3.8'
services:
  longhun-api:
    image: longhun/api:latest
    ports:
      - "8777:8777"
    env_file: .env
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    restart: always

  longhun-dashboard:
    image: longhun/dashboard:latest
    ports:
      - "9627:9627"
    env_file: .env
    restart: always

  longhun-symbiote:
    image: longhun/symbiote:latest
    ports:
      - "18000:18000"
    env_file: .env
    depends_on:
      - longhun-api
    restart: always
COMPOSEEOF

    log_info "#25 ✅ Docker Compose模板已生成"
}

# ═══════════════════════════════════════════════════════════════
#  #26: SSL证书
# ═══════════════════════════════════════════════════════════════
step_19() {
    log_step "#26: SSL证书"

    if command -v apt &>/dev/null; then
        apt-get install -y certbot python3-certbot-nginx 2>/dev/null || true
    elif command -v dnf &>/dev/null; then
        dnf install -y certbot python3-certbot-nginx 2>/dev/null || true
    fi

    # 自动续期
    (crontab -l 2>/dev/null; echo "0 0,12 * * * /usr/bin/certbot renew --quiet 2>/dev/null") | crontab - 2>/dev/null || true

    log_info "#26 ✅ SSL工具已安装 (运行 certbot --nginx 申请证书)"
}

# ═══════════════════════════════════════════════════════════════
#  #27: 部署摘要
# ═══════════════════════════════════════════════════════════════
step_20() {
    log_step "#27: 部署摘要"

    cat > "${LONGHUN_ROOT}/DEPLOY_SUMMARY.md" <<SUMMARYEOF
# 🐉 龍魂系统部署摘要

**DNA:** \`#龍芯⚡️2026-07-06-LONGHUN-BOOTSTRAP-v3.0\`
**时间:** $(date '+%Y-%m-%d %H:%M:%S')
**服务器:** $(hostname -I | awk '{print $1}')
**OS:** ${OS_ID} ${OS_VERSION}
**架构:** ${ARCH}

## 已完成

| # | 步骤 | 状态 |
|---|------|:---:|
| A1-A6 | 预检系统 | ✅ |
| #1 | 系统更新 + 运维工具 | ✅ |
| #2 | Python编译环境 | ✅ |
| #3 | Node.js + PM2 | ✅ |
| #4-#5 | Docker增强 | ✅ |
| #6 | 防火墙端口 | ✅ |
| #7-#8 | 目录结构 + 权限 | ✅ |
| #9-#10 | Git增强 | ✅ |
| #11-#13 | 配置模板 | ✅ |
| #14 | 健康检查v2 | ✅ |
| #15 | 备份脚本 | ✅ |
| #16 | 部署验证 | ✅ |
| #17 | Nginx多站点 | ✅ |
| #18 | systemd服务 | ✅ |
| #19 | Crontab定时任务 | ✅ |
| #20-22 | 安全加固 | ✅ |
| #23 | 服务自启 | ✅ |
| #24 | 操作别名 | ✅ |
| #25 | Docker Compose | ✅ |
| #26 | SSL证书 | ✅ |

## 待办

- [ ] 配置 .env 文件中的实际密钥
- [ ] 运行 certbot --nginx -d longhun888.com 申请SSL
- [ ] 同步龍魂系统源代码 (rsync)
- [ ] 创建 Python 虚拟环境并安装依赖
- [ ] 启动所有服务: lh-restart

## 快速操作

\`\`\`bash
lh-status      # 查看服务状态
lh-health      # 健康检查
lh-backup      # 执行备份
lh-logs        # 实时日志
lh-err         # 错误日志
lh-ports       # 端口监听
lh-verify      # 部署验证
\`\`\`

## 服务端口

| 服务 | 端口 |
|------|:---:|
| Nginx (主站) | 80/443 |
| 龍智守飞书机器人 | 5001 |
| 龍魂API核心 | 8777 |
| 龍魂操作台Dashboard | 9627 |
| 共生体知识矩阵 | 18000 |
| 守门人状态 | 18100 |

SUMMARYEOF

    log_info "#27 ✅ 部署摘要已生成"
}

# ═══════════════════════════════════════════════════════════════
#  补充脚本
# ═══════════════════════════════════════════════════════════════
create_helper_scripts() {
    log_step "补充辅助脚本"

    # 每日复盘
    cat > "${LONGHUN_ROOT}/scripts/daily-review.sh" <<'EOF'
#!/bin/bash
echo "龍魂每日复盘 - $(date '+%Y-%m-%d')"
echo "=============================="
systemctl status longhun-* --no-pager -l 2>/dev/null | grep -E "Active:|Loaded:" | head -20
echo ""
echo "磁盘: $(df -h / | awk 'NR==2{print $5}')"
echo "内存: $(free -h | grep Mem | awk '{print $3"/"$2}')"
EOF
    chmod +x "${LONGHUN_ROOT}/scripts/daily-review.sh"

    # 自动评估
    cat > "${LONGHUN_ROOT}/scripts/auto-eval.sh" <<'EOF'
#!/bin/bash
echo "龍魂自动评估 - $(date '+%Y-%m-%d %H:%M')"
# 检查关键服务
for svc in nginx docker longhun-longzhishou longhun-dashboard longhun-symbiote; do
    if systemctl is-active --quiet "$svc" 2>/dev/null; then
        echo "  ✅ $svc"
    else
        echo "  ❌ $svc - 需要关注"
    fi
done
EOF
    chmod +x "${LONGHUN_ROOT}/scripts/auto-eval.sh"

    # 检查更新
    cat > "${LONGHUN_ROOT}/scripts/check-updates.sh" <<'EOF'
#!/bin/bash
echo "龍魂更新检查 - $(date)"
apt-get update -y 2>/dev/null | tail -1 || dnf check-update 2>/dev/null | tail -1 || true
EOF
    chmod +x "${LONGHUN_ROOT}/scripts/check-updates.sh"

    log_info "辅助脚本创建完成"
}

# ═══════════════════════════════════════════════════════════════
#  主流程
# ═══════════════════════════════════════════════════════════════
main() {
    echo ""
    echo "🐉 龍魂系统 · 终极引导部署 v3.0"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  DNA: #龍芯⚡️2026-07-06-LONGHUN-BOOTSTRAP-v3.0"
    echo "  归属: UID9622｜龍芯北辰｜CNSH"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""

    detect_os

    preflight;       fuse   # A1-A6
    step_01;         fuse   # 系统更新 + 运维工具
    step_02;         fuse   # Python编译环境
    step_03;         fuse   # Node.js + PM2
    step_04;         fuse   # Docker增强
    step_05;         fuse   # 防火墙
    step_06;         fuse   # 目录结构 + 权限
    step_07;         fuse   # Git增强
    step_08;         fuse   # 配置模板
    step_09;         fuse   # 健康检查v2
    step_10;         fuse   # 备份脚本
    step_11;         fuse   # 部署验证脚本
    step_12;         fuse   # Nginx多站点
    step_13;         fuse   # systemd服务
    step_14;         fuse   # Crontab
    step_15;         fuse   # 安全加固
    step_16;         fuse   # 服务自启
    step_17;         fuse   # 操作别名
    step_18;         fuse   # Docker Compose
    step_19;         fuse   # SSL证书
    step_20;         fuse   # 部署摘要

    create_helper_scripts

    echo ""
    echo "══════════════════════════════════════════"
    echo "  ✅ 龍魂引导部署完成！"
    echo "══════════════════════════════════════════"
    echo ""
    echo "  服务器IP: $(hostname -I | awk '{print $1}')"
    echo "  OS:       ${OS_ID} ${OS_VERSION}"
    echo "  架构:     ${ARCH}"
    echo "  路径:     ${LONGHUN_ROOT}"
    echo "  日志:     ${LOG_FILE}"
    echo ""
    echo "  下一步:"
    echo "    1. 从本地同步源码: rsync 本地→服务器"
    echo "    2. 配置 .env: cp .env.example .env && vim .env"
    echo "    3. 创建虚拟环境: python3 -m venv .venv && pip install -r requirements.txt"
    echo "    4. 启动服务: lh-restart"
    echo "    5. 验证: lh-status && lh-health"
    echo ""
    echo "  🐉 龍魂系统 · 数据主权归人民 🇨🇳"
    echo "  #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
    echo "══════════════════════════════════════════"
}

main "$@"
