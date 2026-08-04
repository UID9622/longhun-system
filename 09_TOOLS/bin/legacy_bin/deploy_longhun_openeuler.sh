#!/bin/bash
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂系統 · 華為鯤鵬openEuler部署腳本
# DNA: #龍芯⚡️2026-07-06-DEPLOY-OPENEULER-v1.0
# 歸屬: UID9622｜龍芯北辰｜CNSH

set -e

echo "══════════════════════════════════════════"
echo "  龍魂系統 · openEuler部署腳本"
echo "  DNA: #龍芯⚡️2026-07-06-DEPLOY-v1.0"
echo "══════════════════════════════════════════"

# 1. 系統更新
echo "[1/8] 更新系統..."
sudo dnf update -y

# 2. 安裝基礎工具
echo "[2/8] 安裝基礎工具..."
sudo dnf install -y git curl wget vim python3 python3-pip nginx

# 3. 安裝Node.js (ARM64版)
echo "[3/8] 安裝Node.js..."
curl -fsSL https://rpm.nodesource.com/setup_20.x | sudo bash -
sudo dnf install -y nodejs

# 4. 安裝Docker (ARM64版)
echo "[4/8] 安裝Docker..."
sudo dnf config-manager --add-repo https://repo.huaweicloud.com/docker-ce/linux/centos/docker-ce.repo
sudo dnf install -y docker-ce docker-ce-cli containerd.io
sudo systemctl start docker
sudo systemctl enable docker

# 5. 配置防火牆
echo "[5/8] 配置防火牆..."
sudo firewall-cmd --permanent --add-service=ssh
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload

# 6. 創建龍魂目錄
echo "[6/8] 創建龍魂目錄..."
mkdir -p ~/longhun-system/{api,web,scripts,logs,backup}
cd ~/longhun-system

# 7. 初始化Git倉庫
echo "[7/8] 初始化Git倉庫..."
git init
git config user.name "龍芯北辰"
git config user.email "uid9622@petalmail.com"

# 8. 創建基礎配置文件
echo "[8/8] 創建基礎配置..."
cat > ~/longhun-system/README.md << 'EOF'
# 龍魂系統

**DNA:** `#龍芯⚡️2026-07-06-DEPLOY-OPENEULER-v1.0`
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

cat > ~/longhun-system/scripts/health-check.sh << 'EOF'
#!/bin/bash
# 龍魂系統健康檢查

echo "══════════════════════════════════════════"
echo "  龍魂系統健康檢查"
echo "  $(date '+%Y-%m-%d %H:%M:%S')"
echo "══════════════════════════════════════════"

echo "[CPU]"
top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1

echo "[內存]"
free -h | grep Mem

echo "[磁盤]"
df -h | grep -E "(Filesystem|/dev/)"

echo "[Docker]"
sudo docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

echo "[Nginx]"
sudo systemctl status nginx | grep Active

echo "══════════════════════════════════════════"
echo "  檢查完成"
echo "══════════════════════════════════════════"
EOF

chmod +x ~/longhun-system/scripts/health-check.sh

# 9. 啟動Nginx
echo "[啟動Nginx]"
sudo systemctl start nginx
sudo systemctl enable nginx

# 10. 顯示完成信息
echo ""
echo "══════════════════════════════════════════"
echo "  ✅ 龍魂系統部署完成"
echo "══════════════════════════════════════════"
echo ""
echo "  服務器IP: $(hostname -I | awk '{print $1}')"
echo "  系統版本: $(cat /etc/os-release | grep PRETTY_NAME | cut -d'=' -f2 | tr -d '"')"
echo "  架構: $(uname -m)"
echo "  Node.js: $(node -v)"
echo "  Python: $(python3 --version)"
echo "  Docker: $(docker --version)"
echo ""
echo "  龍魂目錄: ~/longhun-system"
echo "  健康檢查: ~/longhun-system/scripts/health-check.sh"
echo ""
echo "  🐉 龍魂系統 · 數據主權歸人民 🇨🇳"
echo "  #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
echo "══════════════════════════════════════════"
