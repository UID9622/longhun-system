#!/bin/bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# ============================================
# 龍魂系统 · DNA 服务器一键部署脚本 v2.0
# 在华为云鲲鹏服务器(119.13.90.27)上执行
# UID9622 | 龍芯北辰
# DNA: #龍芯⚡️丙午·辛未·乙酉·亥时·䷏豫-DNA-DEPLOY-v2.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# ============================================
set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log()  { echo -e "${GREEN}[INFO]${NC}  $*"; }
warn() { echo -e "${YELLOW}[WARN]${NC}  $*"; }
err()  { echo -e "${RED}[ERROR]${NC} $*"; exit 1; }

echo "╔══════════════════════════════════════════╗"
echo "║   龍魂系统 · DNA 验证服务器部署 v2.0    ║"
echo "║   UID9622 | 龍芯北辰                     ║"
echo "╚══════════════════════════════════════════╝"
echo ""

# ============================================
# 0. 权限检查
# ============================================
if [[ $EUID -ne 0 ]]; then
    err "请用 root 执行: sudo bash deploy-dna-server.sh"
fi

# ============================================
# 1. 系统依赖
# ============================================
log "Step 1/8: 安装系统依赖..."
apt-get update -qq
apt-get install -y -qq python3 python3-pip python3-venv curl

# ============================================
# 2. 创建工作目录
# ============================================
log "Step 2/8: 创建工作目录..."
mkdir -p /var/longhun/dna-registry
mkdir -p /var/longhun/backups

# ============================================
# 3. 部署服务器代码
# ============================================
log "Step 3/8: 部署服务器代码..."
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
if [[ -f "${SCRIPT_DIR}/longhun_dna_server.py" ]]; then
    cp "${SCRIPT_DIR}/longhun_dna_server.py" /var/longhun/
    log "  已复制: longhun_dna_server.py"
else
    err "  找不到 longhun_dna_server.py，请先放到本脚本同级目录"
fi
chmod +x /var/longhun/longhun_dna_server.py

# ============================================
# 4. Python 虚拟环境 + 依赖
# ============================================
log "Step 4/8: 安装 Python 依赖..."
if [[ ! -d /var/longhun/venv ]]; then
    python3 -m venv /var/longhun/venv
fi

/var/longhun/venv/bin/pip install --quiet --upgrade pip
/var/longhun/venv/bin/pip install --quiet flask gunicorn

# ============================================
# 5. 生成管理员密钥哈希（安全存储）
# ============================================
log "Step 5/8: 配置管理员密钥..."
ENV_FILE="/var/longhun/.env"

if [[ ! -f "$ENV_FILE" ]]; then
    # 默认密钥，建议部署后修改
    ADMIN_KEY="LONGHUN-UID9622-ROOT-ONLY"
    KEY_HASH=$(echo -n "$ADMIN_KEY" | sha256sum | awk '{print $1}')

    cat > "$ENV_FILE" << EOF
# 龍魂 DNA 服务器环境变量
LH_DNA_DATA_DIR=/var/longhun/dna-registry
LH_DNA_LOG_FILE=/var/longhun/dna-verify.log
LH_DNA_MAX_AGE=2592000
LH_DNA_GRACE_PERIOD=300
LH_DNA_ADMIN_KEY_HASH=sha256:${KEY_HASH}
LH_DNA_RATE_LIMIT_WINDOW=60
LH_DNA_RATE_LIMIT_MAX=30
EOF
    chmod 600 "$ENV_FILE"
    log "  管理员密钥已生成，哈希: sha256:${KEY_HASH}"
    warn "  ⚠️  部署完成后请修改默认密钥！"
    warn "  export LH_DNA_ADMIN_KEY_HASH=\"sha256:\$(echo -n '你的新密钥' | sha256sum | awk '{print \$1}')\""
fi

# ============================================
# 6. 创建 longhun 用户
# ============================================
log "Step 6/8: 创建服务用户..."
if ! id longhun &>/dev/null; then
    useradd -r -s /bin/false -m -d /var/longhun longhun
fi
chown -R longhun:longhun /var/longhun

# ============================================
# 7. 安装 systemd 服务
# ============================================
log "Step 7/8: 安装 systemd 服务..."

# 写生产级 systemd 配置（带环境变量注入）
cat > /etc/systemd/system/longhun-dna.service << 'SYSTEMD_EOF'
[Unit]
Description=龍魂系统 DNA 验证服务器 v2.0
Documentation=https://uid9622.cn
After=network.target network-online.target
Wants=network-online.target

[Service]
Type=simple
User=longhun
Group=longhun
WorkingDirectory=/var/longhun
EnvironmentFile=-/var/longhun/.env
ExecStart=/var/longhun/venv/bin/gunicorn \
    --workers 2 \
    --bind 0.0.0.0:7700 \
    --timeout 30 \
    --graceful-timeout 10 \
    --max-requests 10000 \
    --max-requests-jitter 1000 \
    --access-logfile /var/longhun/gunicorn-access.log \
    --error-logfile /var/longhun/gunicorn-error.log \
    --log-level info \
    --capture-output \
    longhun_dna_server:app
ExecStartPre=/bin/mkdir -p /var/longhun/dna-registry
Restart=on-failure
RestartSec=10
StartLimitInterval=300
StartLimitBurst=5

# 安全加固
NoNewPrivileges=yes
PrivateTmp=yes
ProtectSystem=strict
ProtectHome=yes
ReadWritePaths=/var/longhun
ReadOnlyPaths=/usr/bin/python3 /var/longhun/venv
ProtectKernelTunables=yes
ProtectKernelModules=yes
ProtectControlGroups=yes
RestrictRealtime=yes
RestrictNamespaces=yes
MemoryDenyWriteExecute=no

# 日志
StandardOutput=journal
StandardError=journal
SyslogIdentifier=longhun-dna

[Install]
WantedBy=multi-user.target
SYSTEMD_EOF

systemctl daemon-reload
systemctl enable longhun-dna

# 先停掉旧进程（如果存在）
systemctl stop longhun-dna 2>/dev/null || true
sleep 1

systemctl start longhun-dna

# ============================================
# 8. 验证
# ============================================
log "Step 8/8: 验证服务..."

# 等待服务启动
for i in $(seq 1 10); do
    if systemctl is-active --quiet longhun-dna; then
        break
    fi
    log "  等待服务启动... (${i}/10)"
    sleep 2
done

echo ""
echo "╔══════════════════════════════════════════╗"
echo "║            部署结果                      ║"
echo "╚══════════════════════════════════════════╝"

# 服务状态
if systemctl is-active --quiet longhun-dna; then
    echo -e "  服务状态: ${GREEN}✅ ACTIVE${NC}"
else
    echo -e "  服务状态: ${RED}❌ FAILED${NC}"
    echo ""
    echo "  排查命令:"
    echo "    systemctl status longhun-dna"
    echo "    journalctl -u longhun-dna -n 50 --no-pager"
    exit 1
fi

# 健康检查
HEALTH=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:7700/health 2>/dev/null || echo "000")
if [[ "$HEALTH" == "200" ]]; then
    echo -e "  健康检查: ${GREEN}✅ 200 OK${NC}"
    echo ""
    echo "  响应内容:"
    curl -s http://localhost:7700/health | python3 -m json.tool 2>/dev/null || curl -s http://localhost:7700/health
else
    echo -e "  健康检查: ${RED}❌ HTTP ${HEALTH}${NC}"
    warn "  API 可能还在启动中，稍等再试"
fi

# 外网地址
echo ""
PUBLIC_IP=$(curl -s --connect-timeout 5 ifconfig.me 2>/dev/null || echo "未知")
echo "  API 地址: http://${PUBLIC_IP}:7700"
echo "  日志文件: /var/longhun/dna-verify.log"
echo "  注册目录: /var/longhun/dna-registry/"
echo ""
echo "  常用命令:"
echo "    systemctl status longhun-dna     # 查看状态"
echo "    journalctl -u longhun-dna -f    # 实时日志"
echo "    systemctl restart longhun-dna   # 重启"
echo ""
echo "  下一步:"
echo "    1. 华为云安全组放行 TCP 7700"
echo "    2. 修改默认管理员密钥:"
echo "       vim /var/longhun/.env"
echo "       systemctl restart longhun-dna"
echo "    3. 在客户端运行: bash dna-generator.sh"
echo "    4. 调用 POST /dna/register 注册设备"
echo ""
echo "╔══════════════════════════════════════════╗"
echo "║  部署完成 · DNA: #龍芯⚡️丙午·辛未·乙酉·亥时·䷏豫  ║"
echo "╚══════════════════════════════════════════╝"
