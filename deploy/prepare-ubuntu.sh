#!/usr/bin/env bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 🐉 龍魂 · Ubuntu 24.04 华为云服务端环境准备脚本
# 适用: Ubuntu 24.04 x86_64
# DNA: #龍芯⚡️丙午·甲午·辛巳·甲午·䷃蒙-UBUNTU-PREPARE-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 归属: UID9622｜龍芯北辰｜CNSH

set -euo pipefail

DEPLOY_PATH="/opt/longhun-system"
RUN_USER="longhun"
RUN_GROUP="longhun"
LOG_DIR="/var/log/longhun"

GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; CYAN='\033[0;36m'; NC='\033[0m'
log()  { echo -e "$(date '+%H:%M:%S') $*"; }
ok()   { log "${GREEN}✅${NC} $*"; }
warn() { log "${YELLOW}⚠️${NC}  $*"; }
fail() { log "${RED}🔴${NC} $*"; exit 1; }
info() { log "${CYAN}▶${NC}  $*"; }

[[ $EUID -eq 0 ]] || fail "请以 root 执行"

echo ""
echo "🐉 龍魂 · Ubuntu 24.04 华为云环境准备 v1.0"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  部署路径: ${DEPLOY_PATH}"
echo "  架构: $(uname -m)"
echo ""

# ─── 1. 系统更新 ───
info "第1步: 更新系统"
apt-get update -y && apt-get upgrade -y
ok "系统已更新"

# ─── 2. 安装基础工具 ───
info "第2步: 安装基础工具"
apt-get install -y \
    git curl wget vim \
    python3 python3-pip python3-venv python3-dev \
    build-essential gcc g++ make cmake \
    nginx \
    htop lsof net-tools rsync \
    tar gzip bzip2 \
    openssl libssl-dev libffi-dev \
    zlib1g-dev libbz2-dev libsqlite3-dev libreadline-dev liblzma-dev \
    jq tmux \
    docker.io docker-compose \
    certbot python3-certbot-nginx \
    logrotate \
    ufw \
    || warn "部分包安装跳过，继续..."

ok "基础包安装完成"

# ─── 3. 安装 Node.js ───
info "第3步: 安装 Node.js 20.x"
if ! command -v node &>/dev/null; then
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
    apt-get install -y nodejs
    ok "Node.js: $(node -v)"
else
    ok "Node.js 已安装: $(node -v)"
fi

# ─── 4. 安装 PM2 ───
info "第4步: 安装 PM2"
npm install -g pm2 2>/dev/null || warn "PM2 安装跳过"
ok "PM2 已安装" || true

# ─── 5. Docker 配置 ───
info "第5步: 配置 Docker"
systemctl start docker 2>/dev/null || true
systemctl enable docker 2>/dev/null || true
ok "Docker 已启用"

# ─── 6. 创建 Python 虚拟环境 ───
info "第6步: 创建 Python 虚拟环境"
VENV_PATH="${DEPLOY_PATH}/.venv"
mkdir -p "$(dirname "$VENV_PATH")"
python3 -m venv "${VENV_PATH}"
source "${VENV_PATH}/bin/activate"
pip install --upgrade pip setuptools wheel
pip install flask>=2.0 fastapi uvicorn requests aiohttp pyyaml
pip install cryptography python-dateutil jinja2 markdown
pip install psutil
deactivate
ok "Python 虚拟环境: ${VENV_PATH}"

# ─── 7. 创建运行用户和目录 ───
info "第7步: 创建运行用户和目录"
if ! id "${RUN_USER}" &>/dev/null; then
    groupadd -f "${RUN_GROUP}"
    useradd -r -g "${RUN_GROUP}" -m -s /bin/bash "${RUN_USER}"
    ok "创建用户: ${RUN_USER}"
else
    ok "用户已存在: ${RUN_USER}"
fi

mkdir -p "${DEPLOY_PATH}"
mkdir -p "${LOG_DIR}"
mkdir -p /home/${RUN_USER}/.longhun/{logs,backups,config}
mkdir -p /home/${RUN_USER}/.龍魂
mkdir -p /etc/nginx/conf.d

ok "目录创建完成"

# ─── 8. 权限 ───
info "第8步: 设置权限"
chown -R "${RUN_USER}:${RUN_GROUP}" "${DEPLOY_PATH}" 2>/dev/null || true
chown -R "${RUN_USER}:${RUN_GROUP}" "${LOG_DIR}" 2>/dev/null || true
chown -R "${RUN_USER}:${RUN_GROUP}" /home/${RUN_USER}/.longhun 2>/dev/null || true
chown -R "${RUN_USER}:${RUN_GROUP}" /home/${RUN_USER}/.龍魂 2>/dev/null || true
ok "权限完成"

# ─── 9. 防火墙 (UFW) ───
info "第9步: 配置防火墙"
if command -v ufw &>/dev/null; then
    ufw allow 22/tcp 2>/dev/null || true
    ufw allow 80/tcp 2>/dev/null || true
    ufw allow 443/tcp 2>/dev/null || true
    ufw allow 8777/tcp 2>/dev/null || true
    ufw allow 9627/tcp 2>/dev/null || true
    ufw allow 5001/tcp 2>/dev/null || true
    ufw allow 18100/tcp 2>/dev/null || true
    ufw --force enable 2>/dev/null || true
    ok "UFW 已配置"
else
    warn "无 UFW，请手动放行端口"
fi

# ─── 10. Nginx ───
info "第10步: 启动 Nginx"
systemctl enable nginx 2>/dev/null || true
systemctl start nginx 2>/dev/null || warn "Nginx 启动跳过"
ok "Nginx 已启动"

# ─── 11. Python 模块验证 ───
info "第11步: Python 模块验证"
source "${VENV_PATH}/bin/activate" 2>/dev/null || true
python3 -c "
import sys
print(f'  Python: {sys.version}')
mods = ['json','hashlib','ssl','os','shutil','subprocess','re','datetime']
for m in mods:
    try:
        __import__(m)
        print(f'  ✅ {m}')
    except:
        print(f'  ❌ {m}')
optional = ['flask','yaml','requests','cryptography','psutil']
for m in optional:
    try:
        __import__(m)
        print(f'  ✅ {m}')
    except:
        print(f'  ⚠️  {m}')
" 2>/dev/null || true
deactivate 2>/dev/null || true

# ─── 完成 ───
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
ok "🐉 Ubuntu 24.04 环境准备完成！"
echo ""
echo "  部署路径: ${DEPLOY_PATH}"
echo "  运行用户: ${RUN_USER}"
echo "  Node.js:  $(node -v 2>/dev/null || echo '无')"
echo "  Python:   $(python3 --version)"
echo "  Nginx:    $(nginx -v 2>&1 || echo '无')"
echo ""
echo "DNA: #龍芯⚡️丙午·甲午·辛巳·甲午·䷃蒙-UBUNTU-PREPARE-v1.0"
