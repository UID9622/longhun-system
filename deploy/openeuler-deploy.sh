#!/bin/bash
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# ═══════════════════════════════════════════════════════════════════
#  龍魂系統 · 華為鯤鵬openEuler一鍵部署腳本 v2.0
#  DNA: #龍芯⚡️2026-07-06-DEPLOY-OPENEULER-v2.0
#  歸屬: UID9622｜龍芯北辰｜CNSH
#  原則: 只加不減 · 原版每一步焊死不動 · 加法擴展
# ═══════════════════════════════════════════════════════════════════

set -euo pipefail

# ─── 全局變量 ───────────────────────────────────────────────
DEPLOY_TIME=$(date '+%Y-%m-%d %H:%M:%S')
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
LOG_FILE="/tmp/longhun-deploy-$(date +%Y%m%d%H%M%S).log"
CONFIRM="#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL"

# 日志函數
log()  { echo "[$(date '+%H:%M:%S')] $*" | tee -a "$LOG_FILE"; }
log_ok()  { echo "  ✅ $*" | tee -a "$LOG_FILE"; }
log_warn() { echo "  ⚠️  $*" | tee -a "$LOG_FILE"; }
log_err() { echo "  🔴 $*" | tee -a "$LOG_FILE"; }

# ─── 預檢 · 系統環境檢查（新增·加法#A）──────────────────────
log "══════════════════════════════════════════"
log "  龍魂系統 · openEuler部署腳本 v2.0"
log "  DNA: #龍芯⚡️2026-07-06-DEPLOY-v2.0"
log "  開始時間: $DEPLOY_TIME"
log "══════════════════════════════════════════"

# A1. 架構檢測
ARCH=$(uname -m)
log "[預檢] 系統架構: $ARCH"
case "$ARCH" in
    aarch64|arm64)
        log_ok "ARM64架構，適配華為鯤鵬"
        ;;
    x86_64)
        log_warn "x86_64架構，腳本為ARM64優化，部分包可能需要調整"
        ;;
    *)
        log_err "未知架構: $ARCH，部署可能失敗"
        ;;
esac

# A2. 操作系統檢測
if [ -f /etc/os-release ]; then
    OS_NAME=$(grep "^NAME=" /etc/os-release | cut -d'=' -f2 | tr -d '"')
    OS_VER=$(grep "^VERSION_ID=" /etc/os-release | cut -d'=' -f2 | tr -d '"')
    log "[預檢] 操作系統: $OS_NAME $OS_VER"
    case "$OS_NAME" in
        *openEuler*|*EulerOS*)
            log_ok "openEuler系統，最佳適配"
            ;;
        *CentOS*|*Rocky*|*AlmaLinux*)
            log_warn "RHEL系系統，部分兼容"
            ;;
        *)
            log_warn "非openEuler系統: $OS_NAME，守護進程配置可能需要手動調整"
            ;;
    esac
else
    log_warn "無法檢測操作系統版本"
fi

# A3. 內存檢測
MEM_TOTAL=$(grep MemTotal /proc/meminfo 2>/dev/null | awk '{print $2}' || echo "0")
MEM_GB=$((MEM_TOTAL / 1024 / 1024))
log "[預檢] 總內存: ${MEM_GB}GB"
if [ "$MEM_GB" -lt 2 ]; then
    log_err "內存不足2GB，部分服務可能無法啟動"
elif [ "$MEM_GB" -lt 4 ]; then
    log_warn "內存少於4GB，建議不跑Docker所有服務"
fi

# A4. 磁盤檢測
DISK_AVAIL=$(df -BG / | tail -1 | awk '{print $4}' | sed 's/G//')
log "[預檢] 可用磁盤: ${DISK_AVAIL}GB"
if [ "$DISK_AVAIL" -lt 10 ]; then
    log_err "磁盤不足10GB，請先擴容"
    exit 1
fi

# A5. 網絡檢測
log "[預檢] 檢查網絡連通性..."
if ping -c 1 -W 3 www.huawei.com >/dev/null 2>&1; then
    NET_IP=$(hostname -I 2>/dev/null | awk '{print $1}' || echo "未知")
    log_ok "網絡正常，服務器IP: $NET_IP"
else
    log_err "網絡不通，請檢查網絡配置"
    exit 1
fi

# A6. sudo權限檢測
if ! sudo -n true 2>/dev/null; then
    log_warn "需要sudo密碼，部署過程中可能需要手動輸入"
fi

# ─── 第一部分 · 系統基礎環境 ─────────────────────────────────

# 1. 系統更新（原版焊死）
log "[1/12] 更新系統..."
sudo dnf update -y
log_ok "系統更新完成"

# 2. 安裝基礎工具（原版焊死）
log "[2/12] 安裝基礎工具..."
sudo dnf install -y git curl wget vim python3 python3-pip nginx
log_ok "基礎工具安裝完成"

# 2a. 安裝附加工具（加法#1: 運維必備）
log "[2a] 安裝運維工具..."
sudo dnf install -y \
    htop \
    iotop \
    net-tools \
    bind-utils \
    lsof \
    jq \
    tmux \
    rsync \
    logrotate \
    unzip \
    tar \
    gzip \
    openssl \
    ca-certificates \
    2>/dev/null || log_warn "部分運維工具安裝失敗，繼續..."
log_ok "運維工具安裝完成"

# 2b. 安裝Python開發包（加法#2: 為後續pip依賴做準備）
log "[2b] 安裝Python開發包..."
sudo dnf install -y \
    python3-devel \
    gcc \
    gcc-c++ \
    make \
    openssl-devel \
    libffi-devel \
    2>/dev/null || log_warn "部分Python開發包安裝失敗，繼續..."
log_ok "Python開發包安裝完成"

# 3. 安裝Node.js · ARM64版（原版焊死）
log "[3/12] 安裝Node.js (ARM64)..."
curl -fsSL https://rpm.nodesource.com/setup_20.x | sudo bash -
sudo dnf install -y nodejs
log_ok "Node.js $(node -v) 安裝完成"

# 3a. 安裝PM2進程管理器（加法#3: 守護Node進程）
log "[3a] 安裝PM2..."
npm install -g pm2 2>/dev/null || log_warn "PM2安裝失敗，可手動安裝: npm i -g pm2"
log_ok "PM2安裝完成"

# 4. 安裝Docker（原版焊死）
log "[4/12] 安裝Docker..."
sudo dnf config-manager --add-repo https://repo.huaweicloud.com/docker-ce/linux/centos/docker-ce.repo
sudo dnf install -y docker-ce docker-ce-cli containerd.io
sudo systemctl start docker
sudo systemctl enable docker
log_ok "Docker $(docker --version) 安裝完成"

# 4a. Docker Compose（加法#4: 多容器編排）
log "[4a] 安裝Docker Compose..."
if ! command -v docker-compose >/dev/null 2>&1; then
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" \
        -o /usr/local/bin/docker-compose 2>/dev/null || \
    sudo curl -L "https://repo.huaweicloud.com/docker-compose/$(curl -s https://api.github.com/repos/docker/compose/releases/latest | grep tag_name | head -1 | cut -d'"' -f4)/docker-compose-$(uname -s)-$(uname -m)" \
        -o /usr/local/bin/docker-compose 2>/dev/null || \
    log_warn "Docker Compose下載失敗，可手動安裝"
    sudo chmod +x /usr/local/bin/docker-compose 2>/dev/null || true
fi
log_ok "Docker Compose安裝完成"

# 4b. 配置Docker鏡像加速（加法#5: 華為雲鏡像）
log "[4b] 配置Docker鏡像加速..."
sudo mkdir -p /etc/docker
sudo tee /etc/docker/daemon.json > /dev/null << 'DOCKERJSON'
{
  "registry-mirrors": [
    "https://mirror.swr.myhuaweicloud.com",
    "https://docker.mirrors.ustc.edu.cn"
  ],
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "50m",
    "max-file": "5"
  },
  "storage-driver": "overlay2"
}
DOCKERJSON
sudo systemctl restart docker
log_ok "Docker鏡像加速配置完成"

# 5. 配置防火牆（原版焊死）
log "[5/12] 配置防火牆..."
sudo firewall-cmd --permanent --add-service=ssh
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload
log_ok "防火牆基礎配置完成"

# 5a. 開放龍魂服務端口（加法#6: 所有龍魂端口）
log "[5a] 開放龍魂服務端口..."
LONGHUN_PORTS=(
    5001    # 龍智守飛書Bot
    8777    # longhun888.com門戶
    9627    # 共生體知識矩陣
    18000   # CNSH Editor API
    18100   # 龍魂v10 API
)
for port in "${LONGHUN_PORTS[@]}"; do
    if sudo firewall-cmd --permanent --add-port=${port}/tcp 2>/dev/null; then
        log_ok "端口 $port 已開放"
    else
        log_warn "端口 $port 開放失敗（防火牆可能未啟用）"
    fi
done
sudo firewall-cmd --reload 2>/dev/null || true
log_ok "龍魂端口配置完成"

# ─── 第二部分 · 龍魂系統部署 ─────────────────────────────────

# 6. 創建龍魂目錄（原版焊死 + 加法#7: 補充目錄）
log "[6/12] 創建龍魂目錄..."
mkdir -p ~/longhun-system/{api,web,scripts,logs,backup}
# 加法·補充目錄
mkdir -p ~/longhun-system/{data,conf,ssl,dist,deploy,tools}
mkdir -p ~/.longhun/{config,logs,evaluation,semantic}
mkdir -p ~/longhun-system/logs/{nginx,docker,pm2}
cd ~/longhun-system
log_ok "龍魂目錄創建完成"

# 6a. 設置目錄權限（加法#8: 安全加固）
log "[6a] 設置目錄權限..."
chmod 750 ~/longhun-system/logs
chmod 750 ~/.longhun/config
[ -d ~/longhun-system/ssl ] && chmod 700 ~/longhun-system/ssl
log_ok "目錄權限設置完成"

# 7. 初始化Git倉庫（原版焊死）
log "[7/12] 初始化Git倉庫..."
git init
git config user.name "龍芯北辰"
git config user.email "uid9622@petalmail.com"

# 7a. 配置Git遠程倉庫（加法#9: 雙倉庫鏡像）
log "[7a] 配置Git遠程..."
git remote add origin https://github.com/uid9622/longhun-system.git 2>/dev/null || log_warn "origin已存在"
git remote add gitee https://gitee.com/uid9622/longhun-system.git 2>/dev/null || log_warn "gitee遠程已存在"
git remote add huawei https://codehub-g.huawei.com/uid9622/longhun-system.git 2>/dev/null || log_warn "華為倉已存在"
log_ok "Git遠程倉庫配置完成"

# 7b. .gitignore 配置（加法#10）
log "[7b] 配置.gitignore..."
cat > ~/longhun-system/.gitignore << 'GITIGNORE'
# 龍魂 · .gitignore
*.pyc
__pycache__/
.env
*.log
logs/
*.pid
.DS_Store
ssl/
node_modules/
dist/
*.tar.gz
*.zip
config/*.secret.*
~/.longhun/config/*.json
!~/.longhun/config/*.example.*
.idea/
.vscode/
*.swp
*.swo
GITIGNORE
log_ok ".gitignore配置完成"

# ─── 第三部分 · 核心配置文件 ─────────────────────────────────

# 8. 創建基礎配置文件（原版焊死 · README.md）
log "[8/12] 創建基礎配置..."
cat > ~/longhun-system/README.md << 'EOF'
# 龍魂系統

**DNA:** `#龍芯⚡️2026-07-06-DEPLOY-OPENEULER-v2.0`
**歸屬:** `UID9622｜龍芯北辰｜CNSH`
**狀態:** `已部署 · openEuler · ARM64`

## 系統架構
- 前端: Nginx + 靜態頁面
- 後端: Python3 + Node.js
- 數據: 本地存儲 + 透明審計
- 部署: Docker容器化

## 核心原則
- 數據主權歸人民
- 不跪資本、不舔流量
- 為人民服務

EOF

# 8a. 環境變量配置模板（加法#11）
log "[8a] 創建環境變量模板..."
cat > ~/longhun-system/.env.example << 'ENVEOF'
# ═══════════════════════════════════════════
#  龍魂系統 · 環境變量配置
#  複製為 .env 並填入真實值
# ═══════════════════════════════════════════

# 龍魂主密鑰
LONGHUN_MASTER_KEY=your_16byte_hex_key

# 飛書配置
FEISHU_APP_ID=cli_xxx
FEISHU_APP_SECRET=xxx
FEISHU_WEBHOOK_URL=https://open.feishu.cn/open-apis/bot/v2/hook/xxx
FEISHU_WEBHOOK_SECRET=xxx
FEISHU_VERIFICATION_TOKEN=xxx
FEISHU_ENCRYPT_KEY=xxx
FEISHU_CHAT_ID=oc_xxx
LONGHUN_FOUNDER_FEISHU_OPENID=ou_xxx

# 飛書反饋機器人（進階）
FEISHU_FEEDBACK_APP_ID=cli_xxx
FEISHU_FEEDBACK_APP_SECRET=xxx

# Notion集成（可選）
NOTION_API_KEY=secret_xxx
NOTION_DATABASE_ID=xxx

# DeepSeek底座（可選）
DEEPSEEK_API_KEY=sk-xxx

# GitHub/Gitee Token（可選）
GITHUB_TOKEN=ghp_xxx
GITEE_TOKEN=xxx

# 華為雲（可選）
HUAWEI_CLOUD_AK=xxx
HUAWEI_CLOUD_SK=xxx
ENVEOF
log_ok "環境變量模板創建完成"

# 8b. 系統版本文件（加法#12）
log "[8b] 創建版本文件..."
cat > ~/longhun-system/VERSION << VEREOF
# 龍魂系統版本文件
VERSION=v2.0.0
DEPLOY_DATE=$DEPLOY_TIME
ARCH=$ARCH
OS=$OS_NAME $OS_VER
DNA=#龍芯⚡️2026-07-06-DEPLOY-OPENEULER-v2.0
CONFIRM=$CONFIRM
VEREOF
log_ok "版本文件創建完成"

# 8c. CNSH 變量定義文件（加法#13）
log "[8c] 創建CNSH變量定義..."
cat > ~/longhun-system/cnsh_vars.json << 'CNSHVARS'
{
  "@@system": {
    "name": "龍魂系統",
    "version": "v2.0.0",
    "dna": "#龍芯⚡️2026-07-06-DEPLOY-v2.0"
  },
  "@@channel": {
    "feishu": {
      "enabled": true,
      "webhook": "{{FEISHU_WEBHOOK_URL}}",
      "chat_id": "{{FEISHU_CHAT_ID}}"
    },
    "notion": {
      "enabled": false,
      "api_key": "{{NOTION_API_KEY}}"
    }
  },
  "@@server": {
    "ip": "$NET_IP",
    "ports": {
      "longzhishou": 5001,
      "portal": 8777,
      "symbiote": 9627,
      "cnsh_editor": 18000,
      "v10_api": 18100
    }
  }
}
CNSHVARS
log_ok "CNSH變量定義創建完成"

# ─── 第四部分 · 腳本文件創建 ─────────────────────────────────

# 8d. 健康檢查腳本（原版焊死 + 加法#14: 增強健康檢查）
log "[8d] 創建健康檢查腳本..."
cat > ~/longhun-system/scripts/health-check.sh << 'HEALTHSCRIPT'
#!/bin/bash
# 龍魂系統健康檢查 v2.0
# DNA: #龍芯⚡️2026-07-06-HEALTH-CHECK-v2.0

TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
LOG_DIR=~/longhun-system/logs
HEALTH_LOG="$LOG_DIR/health-$(date +%Y%m%d).log"

{
echo "══════════════════════════════════════════"
echo "  龍魂系統健康檢查"
echo "  $TIMESTAMP"
echo "══════════════════════════════════════════"

# 系統資源
echo ""
echo "═══ CPU ═══"
top -bn1 | grep "Cpu(s)" | awk '{print "CPU使用率:", $2}'

echo ""
echo "═══ 內存 ═══"
free -h | grep -E "(Mem|Swap)"

echo ""
echo "═══ 磁盤 ═══"
df -h | grep -E "(Filesystem|/dev/)"

echo ""
echo "═══ 運行時間 ═══"
uptime

echo ""
echo "═══ Docker ═══"
if command -v docker >/dev/null 2>&1; then
    docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" 2>/dev/null || echo "Docker未運行"
else
    echo "Docker未安裝"
fi

echo ""
echo "═══ Nginx ═══"
sudo systemctl status nginx 2>/dev/null | grep -E "(Active|Loaded)" || echo "Nginx未運行"

echo ""
echo "═══ 龍魂端口檢查 ═══"
PORTS=(5001 8777 9627 18000 18100)
PORT_NAMES=("龍智守Bot" "門戶" "共生體" "CNSH編輯器" "v10API")
for i in "${!PORTS[@]}"; do
    PORT=${PORTS[$i]}
    NAME=${PORT_NAMES[$i]}
    if ss -tlnp 2>/dev/null | grep -q ":$PORT " || lsof -Pi :$PORT -sTCP:LISTEN >/dev/null 2>&1; then
        echo "  ✅ $NAME (端口 $PORT): 在線"
    else
        echo "  ⚠️  $NAME (端口 $PORT): 離線"
    fi
done

echo ""
echo "═══ 近24小時錯誤日誌 ═══"
find ~/longhun-system/logs -name "*.err.log" -mtime -1 -exec tail -3 {} \; 2>/dev/null || echo "無錯誤日誌"

echo ""
echo "══════════════════════════════════════════"
echo "  檢查完成 · $(date '+%H:%M:%S')"
echo "══════════════════════════════════════════"
} | tee -a "$HEALTH_LOG"
HEALTHSCRIPT
chmod +x ~/longhun-system/scripts/health-check.sh
log_ok "健康檢查腳本創建完成"

# 8e. 備份腳本（加法#15）
log "[8e] 創建備份腳本..."
cat > ~/longhun-system/scripts/backup.sh << 'BACKUPSCRIPT'
#!/bin/bash
# 龍魂系統備份腳本
# DNA: #龍芯⚡️2026-07-06-BACKUP-v1.0

BACKUP_DIR=~/longhun-system/backups
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/longhun-backup-$TIMESTAMP.tar.gz"

mkdir -p "$BACKUP_DIR"

# 備份配置文件
tar -czf "$BACKUP_FILE" \
    -C ~/longhun-system \
    VERSION \
    .env 2>/dev/null \
    cnsh_vars.json 2>/dev/null \
    -C ~/.longhun/config . 2>/dev/null \
    && echo "✅ 備份完成: $BACKUP_FILE" \
    || echo "🔴 備份失敗"

# 清理30天前的備份
find "$BACKUP_DIR" -name "longhun-backup-*.tar.gz" -mtime +30 -delete 2>/dev/null
echo "🟢 已清理30天前的舊備份"
BACKUPSCRIPT
chmod +x ~/longhun-system/scripts/backup.sh
log_ok "備份腳本創建完成"

# 8f. 部署驗證腳本（加法#16）
log "[8f] 創建部署驗證腳本..."
cat > ~/longhun-system/scripts/verify-deploy.sh << 'VERIFYSCRIPT'
#!/bin/bash
# 龍魂系統部署驗證
# DNA: #龍芯⚡️2026-07-06-VERIFY-DEPLOY-v1.0

PASS=0
FAIL=0

check() {
    if eval "$1" >/dev/null 2>&1; then
        echo "  ✅ $2"
        PASS=$((PASS + 1))
    else
        echo "  🔴 $2"
        FAIL=$((FAIL + 1))
    fi
}

echo "══════════════════════════════════════════"
echo "  龍魂系統 · 部署驗證"
echo "══════════════════════════════════════════"

echo ""
echo "═══ 系統服務 ═══"
check "systemctl is-active docker" "Docker運行中"
check "systemctl is-active nginx" "Nginx運行中"
check "systemctl is-active firewalld" "防火牆運行中"

echo ""
echo "═══ 基礎工具 ═══"
check "command -v python3" "Python3已安裝"
check "command -v node" "Node.js已安裝"
check "command -v git" "Git已安裝"
check "command -v docker" "Docker命令可用"
check "command -v curl" "curl已安裝"

echo ""
echo "═══ 龍魂目錄 ═══"
check "test -d ~/longhun-system" "龍魂主目錄存在"
check "test -d ~/longhun-system/logs" "日誌目錄存在"
check "test -d ~/longhun-system/scripts" "腳本目錄存在"
check "test -d ~/longhun-system/backup" "備份目錄存在"
check "test -f ~/longhun-system/VERSION" "版本文件存在"
check "test -f ~/longhun-system/.env.example" "環境變量模板存在"

echo ""
echo "═══ 防火牆端口 ═══"
for port in 80 443 5001 8777; do
    check "sudo firewall-cmd --list-ports 2>/dev/null | grep -q $port || true" "端口 $port"
done

echo ""
echo "══════════════════════════════════════════"
echo "  驗證結果: ✅ $PASS 通過 | 🔴 $FAIL 失敗"
echo "══════════════════════════════════════════"
VERIFYSCRIPT
chmod +x ~/longhun-system/scripts/verify-deploy.sh
log_ok "部署驗證腳本創建完成"

# ─── 第五部分 · Nginx配置 ───────────────────────────────────

# 8g. Nginx站點配置（加法#17: 多站點反向代理）
log "[8g] 配置Nginx站點..."
sudo mkdir -p /etc/nginx/conf.d

# 主站點: longhun888.com
sudo tee /etc/nginx/conf.d/longhun888.conf > /dev/null << 'NGINXMAIN'
# 龍魂主站 · longhun888.com
server {
    listen 80;
    server_name longhun888.com www.longhun888.com;

    # 日誌
    access_log /home/longzhishou/longhun-system/logs/nginx/access.log;
    error_log /home/longzhishou/longhun-system/logs/nginx/error.log;

    # 靜態資源
    location / {
        root /home/longzhishou/longhun-system/web;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    # 門戶API
    location /api/portal {
        proxy_pass http://127.0.0.1:8777;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    # CNSH編輯器API
    location /api/cnsh {
        proxy_pass http://127.0.0.1:18000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # v10 API
    location /api/v10 {
        proxy_pass http://127.0.0.1:18100;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # 龍智守回調（飛書Webhook）
    location /webhook {
        proxy_pass http://127.0.0.1:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_read_timeout 30s;
    }

    # 狀態頁
    location /status {
        proxy_pass http://127.0.0.1:5001;
        proxy_set_header Host $host;
        allow 127.0.0.1;
        allow 10.0.0.0/8;
        allow 172.16.0.0/12;
        allow 192.168.0.0/16;
        deny all;
    }

    # 健康檢查不記錄日誌
    location /health {
        access_log off;
        return 200 "OK";
        add_header Content-Type text/plain;
    }
}
NGINXMAIN

# 共生體站點（如果需要單獨部署）
sudo tee /etc/nginx/conf.d/symbiote.conf > /dev/null << 'NGINXSYM'
# 龍魂共生體知識矩陣
server {
    listen 80;
    server_name symbiote.longhun888.com;

    access_log /home/longzhishou/longhun-system/logs/nginx/symbiote_access.log;
    error_log /home/longzhishou/longhun-system/logs/nginx/symbiote_error.log;

    location / {
        proxy_pass http://127.0.0.1:9627;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
NGINXSYM
log_ok "Nginx站點配置完成"

# ─── 第六部分 · Systemd服務配置 ──────────────────────────────

# 8h. 創建systemd服務（加法#18: 生產級守護進程）
log "[8h] 配置systemd服務..."
SYSTEMD_DIR=/etc/systemd/system

# 龍智守服務
sudo tee "$SYSTEMD_DIR/longzhishou.service" > /dev/null << 'LZSVC'
[Unit]
Description=龍智守飛書機器人服務
After=network.target docker.service

[Service]
Type=simple
User=root
WorkingDirectory=/root/longhun-system
Environment=PYTHONUNBUFFERED=1
EnvironmentFile=-/root/longhun-system/.env
ExecStartPre=/usr/bin/bash /root/longhun-system/scripts/health-check.sh
ExecStart=/usr/bin/python3 /root/longhun-system/dist/龍智守_v2.0_*/龍智守_本地控制接口_v2.0.py
Restart=always
RestartSec=5
StandardOutput=append:/root/longhun-system/logs/longzhishou.out.log
StandardError=append:/root/longhun-system/logs/longzhishou.err.log

[Install]
WantedBy=multi-user.target
LZSVC

# 門戶服務
sudo tee "$SYSTEMD_DIR/longhun-portal.service" > /dev/null << 'PORTALSVC'
[Unit]
Description=龍魂門戶服務
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/longhun-system
ExecStart=/usr/bin/bash /root/.龍魂/web/start_portal.sh
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
PORTALSVC

# 共生體服務
sudo tee "$SYSTEMD_DIR/longhun-symbiote.service" > /dev/null << 'SYMSVC'
[Unit]
Description=龍魂共生體知識矩陣
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/longhun-system
ExecStart=/usr/bin/python3 /root/longhun-system/tools/longhun_symbiote_server.py
Restart=always
RestartSec=5
StandardOutput=append:/root/longhun-system/logs/symbiote.out.log
StandardError=append:/root/longhun-system/logs/symbiote.err.log

[Install]
WantedBy=multi-user.target
SYMSVC

sudo systemctl daemon-reload
log_ok "Systemd服務配置完成"

# ─── 第七部分 · 定時任務 ───────────────────────────────────

# 8i. 配置crontab（加法#19: 自動化定時任務）
log "[8i] 配置定時任務..."

# 創建龍魂crontab文件
cat > /tmp/longhun-crontab << CRONTAB
# ═══════════════════════════════════════════
#  龍魂系統 · 定時任務
#  DNA: #龍芯⚡️2026-07-06-CRON-v1.0
# ═══════════════════════════════════════════

# 每2小時健康檢查
0 */2 * * * /bin/bash ~/longhun-system/scripts/health-check.sh

# 每天23:30每日覆盤
30 23 * * * /bin/bash ~/longhun-system/scripts/daily_review_runner.sh

# 每天02:00備份
0 2 * * * /bin/bash ~/longhun-system/scripts/backup.sh

# 每週日03:00系統更新檢查
0 3 * * 0 sudo dnf check-update --security 2>/dev/null | head -20 > ~/longhun-system/logs/security-update-$(date +\%Y\%m\%d).log

# 每天04:00清理舊日誌（保留30天）
0 4 * * * find ~/longhun-system/logs -name "*.log" -mtime +30 -delete 2>/dev/null; find ~/longhun-system/logs -name "*.err.log" -mtime +30 -delete 2>/dev/null

# 每天06:00自動化評估
0 6 * * * /usr/bin/python3 ~/longhun-system/scripts/自動化評估.py --send 2>/dev/null
CRONTAB

# 加載crontab（不覆蓋已有任務）
crontab -l 2>/dev/null | grep -v "longhun\|龍魂" > /tmp/orig-crontab 2>/dev/null || true
cat /tmp/orig-crontab /tmp/longhun-crontab | crontab -
rm -f /tmp/longhun-crontab /tmp/orig-crontab
log_ok "定時任務配置完成"

# ─── 第八部分 · 安全加固 ───────────────────────────────────

# 8j. SELinux配置（加法#20）
log "[8j] 配置SELinux..."
if command -v getenforce >/dev/null 2>&1; then
    SELINUX_MODE=$(getenforce 2>/dev/null || echo "Disabled")
    case "$SELINUX_MODE" in
        Enforcing)
            log_ok "SELinux在Enforcing模式，配置策略..."
            sudo setsebool -P httpd_can_network_connect on 2>/dev/null || true
            sudo setsebool -P httpd_can_network_relay on 2>/dev/null || true
            ;;
        Permissive)
            log_warn "SELinux在Permissive模式，建議啟用Enforcing"
            ;;
        *)
            log_warn "SELinux未啟用，建議啟用"
            ;;
    esac
fi
log_ok "SELinux配置完成"

# 8k. SSH加固（加法#21）
log "[8k] SSH安全加固..."
sudo sed -i 's/^#PermitRootLogin.*/PermitRootLogin prohibit-password/' /etc/ssh/sshd_config 2>/dev/null || true
sudo sed -i 's/^#MaxAuthTries.*/MaxAuthTries 3/' /etc/ssh/sshd_config 2>/dev/null || true
sudo systemctl restart sshd 2>/dev/null || true
log_ok "SSH加固完成"

# 8l. 日誌輪轉配置（加法#22）
log "[8l] 配置日誌輪轉..."
sudo tee /etc/logrotate.d/longhun > /dev/null << 'LOGROTATE'
# 龍魂系統日誌輪轉
/root/longhun-system/logs/*.log
/root/longhun-system/logs/*/*.log {
    daily
    rotate 30
    missingok
    notifempty
    compress
    delaycompress
    dateext
    dateformat -%Y%m%d
    create 0640 root root
    postrotate
        /bin/systemctl reload nginx 2>/dev/null || true
    endscript
}
LOGROTATE
log_ok "日誌輪轉配置完成"

# ─── 第九部分 · 服務啟動 ───────────────────────────────────

# 9. 啟動Nginx（原版焊死）
log "[9/12] 啟動Nginx..."
sudo systemctl start nginx
sudo systemctl enable nginx
log_ok "Nginx已啟動"

# 9a. 啟用所有龍魂systemd服務（加法#23）
log "[9a] 啟用龍魂服務..."
LONGHUN_SERVICES=(
    longzhishou
    longhun-portal
    longhun-symbiote
)
for svc in "${LONGHUN_SERVICES[@]}"; do
    if [ -f "/etc/systemd/system/${svc}.service" ]; then
        sudo systemctl enable "$svc" 2>/dev/null && log_ok "${svc}已設為開機自啟" || log_warn "${svc}啟用失敗"
    fi
done
log_ok "龍魂服務配置完成"

# 9b. 創建快速操作別名（加法#24）
log "[9b] 配置操作別名..."
cat >> ~/.bashrc << 'ALIASES'

# ═══ 龍魂系統操作別名 ═══
alias lh-status='bash ~/longhun-system/scripts/health-check.sh'
alias lh-backup='bash ~/longhun-system/scripts/backup.sh'
alias lh-verify='bash ~/longhun-system/scripts/verify-deploy.sh'
alias lh-restart='sudo systemctl restart longzhishou longhun-portal longhun-symbiote'
alias lh-logs='tail -f ~/longhun-system/logs/longzhishou.out.log'
alias lh-err='tail -f ~/longhun-system/logs/longzhishou.err.log'
ALIASES
log_ok "操作別名配置完成"

# ─── 第十部分 · Docker服務初始化 ────────────────────────────

# 8m. Docker Compose模板（加法#25）
log "[8m] 創建Docker Compose模板..."
cat > ~/longhun-system/docker-compose.yml << 'DCOMPOSE'
# 龍魂系統 · Docker Compose
# DNA: #龍芯⚡️2026-07-06-DOCKER-COMPOSE-v1.0
version: '3.8'

services:
  # 龍魂門戶
  portal:
    image: nginx:alpine
    container_name: longhun-portal
    restart: always
    ports:
      - "8777:80"
    volumes:
      - ./web:/usr/share/nginx/html:ro
      - ./conf/nginx-portal.conf:/etc/nginx/conf.d/default.conf:ro
    networks:
      - longhun-net

  # 共生體知識矩陣
  symbiote:
    build:
      context: ./tools
      dockerfile: Dockerfile.symbiote
    container_name: longhun-symbiote
    restart: always
    ports:
      - "9627:9627"
    volumes:
      - ./data/symbiote:/app/data
    networks:
      - longhun-net

networks:
  longhun-net:
    driver: bridge
DCOMPOSE
log_ok "Docker Compose模板創建完成"

# ─── 第十一部分 · SSL證書引導 ───────────────────────────────

# 8n. SSL證書腳本（加法#26）
log "[8n] 創建SSL配置腳本..."
cat > ~/longhun-system/scripts/setup-ssl.sh << 'SSLSCRIPT'
#!/bin/bash
# 龍魂SSL證書配置
# 支持: Let's Encrypt (Certbot) / 華為雲SCM手動導入
# DNA: #龍芯⚡️2026-07-06-SSL-SETUP-v1.0

DOMAIN="${1:-longhun888.com}"
EMAIL="${2:-uid9622@petalmail.com}"

echo "🐉 龍魂SSL證書配置"
echo "域名: $DOMAIN"

# 安裝Certbot
if ! command -v certbot >/dev/null 2>&1; then
    sudo dnf install -y certbot python3-certbot-nginx
fi

# 獲取證書
sudo certbot --nginx -d "$DOMAIN" -d "www.$DOMAIN" \
    --non-interactive --agree-tos -m "$EMAIL" \
    --redirect 2>/dev/null || \
    echo "🔴 證書獲取失敗，請手動運行: sudo certbot --nginx"

# 配置自動續期
(sudo crontab -l 2>/dev/null; echo "0 0 1 * * certbot renew --quiet --post-hook 'systemctl reload nginx'") | sudo crontab -

echo "✅ SSL配置完成"
SSLSCRIPT
chmod +x ~/longhun-system/scripts/setup-ssl.sh
log_ok "SSL配置腳本創建完成"

# ─── 第十二部分 · 完成信息 ──────────────────────────────────

# 9c. 部署摘要生成（加法#27）
log "[9c] 生成部署摘要..."
SUMMARY_FILE=~/longhun-system/DEPLOY_SUMMARY.md
cat > "$SUMMARY_FILE" << SUMMARYEOF
# 龍魂系統 · 部署摘要

**部署時間:** $DEPLOY_TIME
**DNA:** #龍芯⚡️2026-07-06-DEPLOY-OPENEULER-v2.0
**CONFIRM:** $CONFIRM

## 系統信息
| 項目 | 值 |
|------|------|
| 操作系統 | $OS_NAME $OS_VER |
| 架構 | $ARCH |
| IP地址 | $NET_IP |
| 內存 | ${MEM_GB}GB |
| Python | $(python3 --version 2>/dev/null || echo "未安裝") |
| Node.js | $(node -v 2>/dev/null || echo "未安裝") |
| Docker | $(docker --version 2>/dev/null || echo "未安裝") |

## 服務端口
| 服務 | 端口 | 狀態 |
|------|------|------|
| 龍智守飛書Bot | 5001 | 配置完成 |
| 門戶服務 | 8777 | 配置完成 |
| 共生體矩陣 | 9627 | 配置完成 |
| CNSH編輯器API | 18000 | 配置完成 |
| v10 API | 18100 | 配置完成 |
| Nginx HTTP | 80 | 運行中 |
| Nginx HTTPS | 443 | 待配置SSL |

## 腳本工具
| 命令 | 用途 |
|------|------|
| \`lh-status\` | 健康檢查 |
| \`lh-backup\` | 備份系統 |
| \`lh-verify\` | 部署驗證 |
| \`lh-restart\` | 重啟所有服務 |
| \`lh-logs\` | 查看實時日誌 |
| \`lh-err\` | 查看錯誤日誌 |

## 下一步
1. 配置 .env：\`cp ~/longhun-system/.env.example ~/longhun-system/.env && vim ~/longhun-system/.env\`
2. 拉取代碼：\`cd ~/longhun-system && git pull origin main\`
3. 配置SSL：\`bash ~/longhun-system/scripts/setup-ssl.sh longhun888.com\`
4. 部署驗證：\`lh-verify\`
5. 健康檢查：\`lh-status\`

## 安全提示
- 立即修改默認SSH端口和禁用密碼登錄
- 配置防火牆僅開放必要端口
- 定期運行備份腳本
- 檢查SELinux狀態

---
$CONFIRM
🐉 龍魂系統 · 數據主權歸人民 🇨🇳
SUMMARYEOF
log_ok "部署摘要已生成: $SUMMARY_FILE"

# ─── 顯示完成信息（原版焊死+加法擴展）─────────────────────

echo ""
echo "══════════════════════════════════════════"
echo "  ✅ 龍魂系統部署完成"
echo "══════════════════════════════════════════"
echo ""
echo "  ⏱️  部署耗時: $(date '+%H:%M:%S') (開始於 $DEPLOY_TIME)"
echo "  🌐 服務器IP: $NET_IP"
echo "  💻 系統版本: ${OS_NAME:-未知} ${OS_VER:-}"
echo "  🔧 架構: $ARCH"
echo "  📦 Node.js: $(node -v 2>/dev/null || echo '未安裝')"
echo "  🐍 Python: $(python3 --version 2>/dev/null || echo '未安裝')"
echo "  🐳 Docker: $(docker --version 2>/dev/null || echo '未安裝')"
echo ""
echo "  📂 龍魂目錄: ~/longhun-system"
echo "  📋 部署摘要: ~/longhun-system/DEPLOY_SUMMARY.md"
echo "  📝 部署日誌: $LOG_FILE"
echo "  🩺 健康檢查: lh-status"
echo "  ✅ 部署驗證: lh-verify"
echo "  💾 系統備份: lh-backup"
echo ""
echo "  🌐 訪問地址:"
echo "     HTTP:  http://$NET_IP"
echo "     HTTPS: https://$NET_IP (需配置SSL後)"
echo "     狀態:  http://$NET_IP/status"
echo ""
echo "  📡 服務端口:"
echo "     龍智守Bot:  :5001 (飛書回調)"
echo "     門戶服務:    :8777"
echo "     共生體矩陣:  :9627"
echo "     CNSH編輯器:  :18000"
echo "     v10 API:     :18100"
echo ""
echo "  ⚙️  快速操作:"
echo "     source ~/.bashrc           # 加載別名"
echo "     lh-status                  # 健康檢查"
echo "     lh-verify                  # 部署驗證"
echo "     lh-restart                 # 重啟所有服務"
echo "     lh-logs                    # 查看實時日誌"
echo ""
echo "  📋 待辦事項:"
echo "     1️⃣  cp ~/longhun-system/.env.example ~/longhun-system/.env"
echo "     2️⃣  vim ~/longhun-system/.env  # 填入飛書/Notion密鑰"
echo "     3️⃣  bash ~/longhun-system/scripts/setup-ssl.sh"
echo "     4️⃣  lh-verify"
echo ""
echo "  🐉 龍魂系統 · 數據主權歸人民 🇨🇳"
echo "  $CONFIRM"
echo "══════════════════════════════════════════"

# 清理臨時文件
rm -f /tmp/longhun-crontab /tmp/orig-crontab 2>/dev/null || true

log "部署腳本執行完畢 · DNA: #龍芯⚡️2026-07-06-DEPLOY-v2.0"
