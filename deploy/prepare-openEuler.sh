#!/usr/bin/env bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 🐉 龍魂 · openEuler 鲲鹏服务端环境准备脚本
# 用途: 在华为鲲鹏 openEuler 服务器上安装所有依赖
# 适用: openEuler 22.03+ / 24.03+ (aarch64)
# 执行方式: 将此脚本上传到服务器后以 root 执行
#          ssh root@mgmt-ip 'bash -s' < prepare-openEuler.sh
# DNA: #龍芯⚡️2026-07-06-KUNPENG-OPENEULER-PREPARE-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

set -euo pipefail

# ─── 可配置参数 ───
DEPLOY_PATH="${LONGHUN_DEPLOY_PATH:-/opt/longhun-system}"
RUN_USER="${LONGHUN_RUN_USER:-longhun}"
RUN_GROUP="${LONGHUN_RUN_GROUP:-longhun}"
PYTHON_BIN="${LONGHUN_PYTHON:-python3}"
LOG_DIR="/var/log/longhun"

# ─── 颜色 ───
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m'

log()  { echo -e "$(date '+%H:%M:%S') $*"; }
ok()   { log "${GREEN}✅${NC} $*"; }
warn() { log "${YELLOW}⚠️${NC}  $*"; }
fail() { log "${RED}🔴${NC} $*"; exit 1; }
info() { log "${CYAN}▶${NC}  $*"; }

# ─── 权限检查 ───
if [[ $EUID -ne 0 ]]; then
    fail "请以 root 用户执行此脚本"
fi

echo ""
echo "🐉 龍魂 · openEuler 鲲鹏环境准备 v1.0"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  部署路径: ${DEPLOY_PATH}"
echo "  运行用户: ${RUN_USER}"
echo "  架构: $(uname -m)"
echo ""

# ─── 1. 检测 openEuler 版本 ───
info "第1步: 检测系统版本"
if [[ -f /etc/openEuler-release ]]; then
    ok "openEuler: $(cat /etc/openEuler-release)"
else
    warn "未检测到 /etc/openEuler-release，当前 OS:"
    head -3 /etc/os-release 2>/dev/null || true
fi

# ─── 2. 配置 DNF/YUM 源（确保 ARM64 可用） ───
info "第2步: 配置软件源"
# openEuler 默认源通常已包含 aarch64，确认一下
if dnf repolist 2>/dev/null | grep -q '^epol\|^OS\|^everything'; then
    ok "DNF 源可用"
else
    warn "软件源可能需要手动配置，尝试继续..."
fi

# ─── 3. 安装系统基础依赖 ───
info "第3步: 安装系统基础包"
dnf install -y --nogpgcheck \
    python3 \
    python3-devel \
    python3-pip \
    python3-setuptools \
    python3-wheel \
    gcc \
    gcc-c++ \
    make \
    git \
    curl \
    wget \
    vim \
    htop \
    lsof \
    net-tools \
    rsync \
    nginx \
    tar \
    gzip \
    bzip2 \
    openssl \
    openssl-devel \
    libffi-devel \
    zlib-devel \
    bzip2-devel \
    sqlite-devel \
    readline-devel \
    xz-devel \
    || warn "部分包安装跳过，继续..."

# 安装 EPOL (Extra Packages for openEuler) 中的额外包
dnf install -y --nogpgcheck \
    cmake 2>/dev/null || true
dnf install -y --nogpgcheck \
    nodejs npm 2>/dev/null || true

ok "系统包安装完成"

# ─── 4. 确认 Python 版本 ───
info "第4步: 确认 Python 版本"
PY_VERSION=$(${PYTHON_BIN} --version 2>&1 || echo "unknown")
ok "Python: ${PY_VERSION}"
${PYTHON_BIN} -c "import sys; print(f'  架构: {sys.platform}')" || true

# ─── 5. 安装 Python 虚拟环境 ───
info "第5步: 创建 Python 虚拟环境"
VENV_PATH="${DEPLOY_PATH}/.venv"
mkdir -p "$(dirname "$VENV_PATH")"
${PYTHON_BIN} -m venv "${VENV_PATH}" 2>/dev/null || {
    warn "venv 创建失败，安装 venv 包..."
    dnf install -y python3-virtualenv 2>/dev/null || pip3 install virtualenv
    ${PYTHON_BIN} -m venv "${VENV_PATH}"
}
ok "虚拟环境: ${VENV_PATH}"

# ─── 6. 安装 Python 依赖（ARM64 兼容） ───
info "第6步: 安装 Python 核心依赖"
source "${VENV_PATH}/bin/activate"

# 先升级 pip
pip install --upgrade pip setuptools wheel 2>&1 | tail -1 || true

# 核心框架
pip install flask>=2.0 2>&1 | tail -1 || warn "flask 可能需要编译安装"
pip install fastapi uvicorn 2>&1 | tail -1 || warn "fastapi 可能需要编译安装"
pip install requests aiohttp 2>&1 | tail -1 || true
pip install pyyaml 2>&1 | tail -1 || true

# 密码学 / 国密相关（ARM64 注意编译依赖）
info "  安装 cryptography（ARM64 需要编译）..."
pip install cryptography 2>&1 | tail -1 || {
    warn "cryptography 安装失败，尝试从系统包安装"
    dnf install -y python3-cryptography 2>/dev/null || true
}

# 如果系统有 python3-cryptography 包，优先用系统包
dnf install -y python3-cryptography python3-pyyaml 2>/dev/null || true

# 数据处理
pip install python-dateutil 2>&1 | tail -1 || true

# 可选：Web 相关
pip install jinja2 markdown 2>&1 | tail -1 || true

deactivate

ok "Python 依赖安装完成"

# ─── 7. 创建运行用户和目录 ───
info "第7步: 创建运行用户和目录"

# 创建用户
if ! id "${RUN_USER}" &>/dev/null; then
    groupadd -f "${RUN_GROUP}"
    useradd -r -g "${RUN_GROUP}" -m -s /bin/bash "${RUN_USER}" 2>/dev/null || \
    useradd -r -m -s /bin/bash "${RUN_USER}"
    ok "创建用户: ${RUN_USER}"
else
    ok "用户已存在: ${RUN_USER}"
fi

# 创建目录
mkdir -p "${DEPLOY_PATH}"
mkdir -p "${LOG_DIR}"
mkdir -p /home/${RUN_USER}/.longhun/logs
mkdir -p /home/${RUN_USER}/.longhun/backups
mkdir -p /home/${RUN_USER}/.longhun/config
mkdir -p /home/${RUN_USER}/.龍魂
mkdir -p /etc/nginx/conf.d

ok "目录创建完成"

# ─── 8. 设置文件权限 ───
info "第8步: 设置权限"
chown -R "${RUN_USER}:${RUN_GROUP}" "${DEPLOY_PATH}" 2>/dev/null || true
chown -R "${RUN_USER}:${RUN_GROUP}" "${LOG_DIR}" 2>/dev/null || true
chown -R "${RUN_USER}:${RUN_GROUP}" /home/${RUN_USER}/.longhun 2>/dev/null || true
chown -R "${RUN_USER}:${RUN_GROUP}" /home/${RUN_USER}/.龍魂 2>/dev/null || true
ok "权限设置完成"

# ─── 9. 配置防火墙 ───
info "第9步: 配置防火墙"
if command -v firewall-cmd &>/dev/null; then
    systemctl start firewalld 2>/dev/null || true
    systemctl enable firewalld 2>/dev/null || true
    firewall-cmd --permanent --add-service=http 2>/dev/null || true
    firewall-cmd --permanent --add-service=https 2>/dev/null || true
    firewall-cmd --permanent --add-port=8777/tcp 2>/dev/null || true
    firewall-cmd --permanent --add-port=9627/tcp 2>/dev/null || true
    firewall-cmd --permanent --add-port=18100/tcp 2>/dev/null || true
    firewall-cmd --permanent --add-port=8000/tcp 2>/dev/null || true
    firewall-cmd --reload 2>/dev/null || true
    ok "firewalld 已配置"
elif command -v iptables &>/dev/null; then
    iptables -I INPUT -p tcp --dport 80 -j ACCEPT 2>/dev/null || true
    iptables -I INPUT -p tcp --dport 443 -j ACCEPT 2>/dev/null || true
    iptables -I INPUT -p tcp --dport 8777 -j ACCEPT 2>/dev/null || true
    iptables -I INPUT -p tcp --dport 9627 -j ACCEPT 2>/dev/null || true
    ok "iptables 已配置"
else
    warn "未检测到防火墙，请手动放行端口: 80, 443, 8777, 9627, 18100"
fi

# ─── 10. 配置 SELinux（openEuler 默认 enforcing） ───
info "第10步: 配置 SELinux"
if command -v getenforce &>/dev/null; then
    SELINUX_MODE=$(getenforce 2>/dev/null || echo "Unknown")
    info "当前 SELinux 模式: ${SELINUX_MODE}"

    if [[ "$SELINUX_MODE" == "Enforcing" ]]; then
        # 允许 Nginx 反向代理
        setsebool -P httpd_can_network_connect 1 2>/dev/null || true

        # 为龍魂目录设置正确的 SELinux 上下文
        semanage fcontext -a -t httpd_sys_content_t "${DEPLOY_PATH}(/.*)?" 2>/dev/null || true
        restorecon -R "${DEPLOY_PATH}" 2>/dev/null || true

        # 日志目录
        semanage fcontext -a -t httpd_log_t "${LOG_DIR}(/.*)?" 2>/dev/null || true
        restorecon -R "${LOG_DIR}" 2>/dev/null || true

        ok "SELinux 策略已配置"
    fi
else
    ok "无 SELinux"
fi

# ─── 11. 开启 Nginx ───
info "第11步: 启动 Nginx"
if command -v nginx &>/dev/null; then
    systemctl enable nginx 2>/dev/null || true
    systemctl start nginx 2>/dev/null || warn "Nginx 启动跳过"
    ok "Nginx 已启用"
fi

# ─── 12. 检查 ARM64 特定兼容性 ───
info "第12步: ARM64 兼容性检查"

# 检查关键 Python 模块能否正常导入（在虚拟环境中）
source "${VENV_PATH}/bin/activate" 2>/dev/null || true
python3 -c "
import sys
print(f'  Python: {sys.version}')
print(f'  平台: {sys.platform}')
print(f'  架构: {sys.maxsize > 2**32 and \"64bit\" or \"32bit\"}')

mods = ['json', 'hashlib', 'ssl', 'os', 'shutil', 'subprocess', 're', 'datetime', 'collections', 'itertools']
for m in mods:
    try:
        __import__(m)
        print(f'  ✅ {m}')
    except:
        print(f'  ❌ {m} 缺失')

# 尝试可选模块
optional = ['flask', 'yaml', 'requests', 'cryptography']
for m in optional:
    try:
        __import__(m)
        print(f'  ✅ {m}')
    except:
        print(f'  ⚠️  {m} 未安装（可能需要在同步後安装）')
" 2>/dev/null || true
deactivate 2>/dev/null || true

# ─── 完成 ───
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
ok "🐉 openEuler 鲲鹏环境准备完成！"
echo ""
echo "  部署路径: ${DEPLOY_PATH}"
echo "  运行用户: ${RUN_USER}"
echo "  虚拟环境: ${VENV_PATH}"
echo "  日志目录: ${LOG_DIR}"
echo ""
echo "  下一步: 执行 sync-to-kunpeng.sh 搬迁系统文件"
echo ""
echo "DNA: #龍芯⚡️2026-07-06-KUNPENG-OPENEULER-PREPARE-v1.0"
