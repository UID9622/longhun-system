#!/bin/bash
# 🐉 龍魂 · 信任链实战部署脚本
# DNA: #龍芯⚡️丙午·甲申·辛丑·坤卦-DEPLOY-TRUST-CHAIN-UID9622
# 版本: v1.1.0
# 用途: 生产环境一键部署信任链验证服务、监控告警、健康检查
# License: MulanPSL v2

set -euo pipefail

# -----------------------------------------------------------------------------
# 默认配置
# -----------------------------------------------------------------------------
ENV="dev"
DOMAIN="localhost"
PORT=8777
STORAGE="./.dna-chain"
GPG_KEY=""
RETENTION_DAYS=3650
HASH_ALGO="sha256"
BATCH_SIZE=1000
VERIFY_WORKERS=4
FEISHU_WEBHOOK=""
ALERT_LEVEL="warning"
VERIFY_ONLY=false

# -----------------------------------------------------------------------------
# 颜色输出
# -----------------------------------------------------------------------------
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# -----------------------------------------------------------------------------
# 打印帮助信息
# -----------------------------------------------------------------------------
usage() {
    cat << EOF
🐉 龍魂信任链 · 部署脚本

用法: $0 [选项]

选项:
  --env               环境: dev/test/production (默认: dev)
  --domain            服务域名 (默认: localhost)
  --port              服务端口 (默认: 8777)
  --storage           签章链存储路径 (默认: ./.dna-chain)
  --gpg-key           GPG密钥ID (推荐配置)
  --retention         签章保留天数 (默认: 3650)
  --hash-algo         哈希算法: sha256/sm3 (默认: sha256)
  --batch-size        批量签章大小 (默认: 1000)
  --verify-workers    验证并发数 (默认: 4)
  --feishu-webhook    飞书告警Webhook
  --alert-level       告警级别: info/warning/error (默认: warning)
  --verify-only       仅运行验证，不部署服务
  -h, --help          显示本帮助

示例:
  $0 --env production --domain trust.uid9622.cn --gpg-key A2D0092CEE2E5BA87035600924C3704A8CC26D5F
EOF
}

# -----------------------------------------------------------------------------
# 解析命令行参数
# -----------------------------------------------------------------------------
while [[ $# -gt 0 ]]; do
    case "$1" in
        --env) ENV="$2"; shift 2 ;;
        --domain) DOMAIN="$2"; shift 2 ;;
        --port) PORT="$2"; shift 2 ;;
        --storage) STORAGE="$2"; shift 2 ;;
        --gpg-key) GPG_KEY="$2"; shift 2 ;;
        --retention) RETENTION_DAYS="$2"; shift 2 ;;
        --hash-algo) HASH_ALGO="$2"; shift 2 ;;
        --batch-size) BATCH_SIZE="$2"; shift 2 ;;
        --verify-workers) VERIFY_WORKERS="$2"; shift 2 ;;
        --feishu-webhook) FEISHU_WEBHOOK="$2"; shift 2 ;;
        --alert-level) ALERT_LEVEL="$2"; shift 2 ;;
        --verify-only) VERIFY_ONLY=true; shift ;;
        -h|--help) usage; exit 0 ;;
        *) echo -e "${RED}未知参数: $1${NC}"; usage; exit 1 ;;
    esac
done

# -----------------------------------------------------------------------------
# 打印部署信息
# -----------------------------------------------------------------------------
echo ""
echo -e "${BLUE}🐉 龍魂信任链 · 部署开始${NC}"
echo -e "${BLUE}========================================${NC}"
echo "  环境:        $ENV"
echo "  域名:        $DOMAIN"
echo "  端口:        $PORT"
echo "  存储路径:    $STORAGE"
echo "  GPG密钥:     ${GPG_KEY:-未配置(演示模式)}"
echo "  哈希算法:    $HASH_ALGO"
echo "  保留天数:    $RETENTION_DAYS"
echo "  批量大小:    $BATCH_SIZE"
echo "  验证并发:    $VERIFY_WORKERS"
echo "  飞书告警:    ${FEISHU_WEBHOOK:-未配置}"
echo ""

# -----------------------------------------------------------------------------
# 步骤1: 环境检查
# 检查必要命令是否存在
# -----------------------------------------------------------------------------
echo -e "${YELLOW}[1/7] 环境检查...${NC}"

for cmd in bash python3 curl; do
    if ! command -v "$cmd" &> /dev/null; then
        echo -e "${RED}❌ 缺少必要命令: $cmd${NC}"
        exit 1
    fi
done

# 检查哈希命令（macOS用shasum，Linux用sha256sum）
if command -v shasum &> /dev/null; then
    HASH_CMD="shasum -a 256"
elif command -v sha256sum &> /dev/null; then
    HASH_CMD="sha256sum"
else
    echo -e "${RED}❌ 缺少哈希计算命令: shasum 或 sha256sum${NC}"
    exit 1
fi

echo -e "  ${GREEN}✅ 环境检查通过${NC}"

# -----------------------------------------------------------------------------
# 步骤2: 依赖安装
# 生产环境可在此安装 python 依赖，如 flask/fastapi/prometheus-client
# -----------------------------------------------------------------------------
echo -e "${YELLOW}[2/7] 依赖安装...${NC}"

if [ "$ENV" = "production" ]; then
    # 示例：安装服务依赖
    # pip install -r requirements.txt
    echo -e "  ${YELLOW}⚠️ 生产环境请确保已安装 requirements.txt 中的依赖${NC}"
else
    echo -e "  ${GREEN}✅ 开发/测试环境跳过依赖安装${NC}"
fi

# -----------------------------------------------------------------------------
# 步骤3: 配置GPG密钥
# 如果没有配置GPG密钥，则进入演示模式（仅哈希验证）
# -----------------------------------------------------------------------------
echo -e "${YELLOW}[3/7] 配置GPG密钥...${NC}"

if [ -n "$GPG_KEY" ]; then
    if ! gpg --list-secret-keys "$GPG_KEY" &> /dev/null; then
        echo -e "${RED}❌ GPG密钥 $GPG_KEY 未找到${NC}"
        exit 1
    fi
    echo -e "  ${GREEN}✅ GPG密钥已配置: $GPG_KEY${NC}"
else
    echo -e "  ${YELLOW}⚠️ 未配置GPG密钥，进入演示模式（仅哈希验证）${NC}"
fi

# -----------------------------------------------------------------------------
# 步骤4: 初始化链目录
# 创建存储目录并设置严格权限（700）
# 如果目录已存在且包含链，则跳过初始化
# -----------------------------------------------------------------------------
echo -e "${YELLOW}[4/7] 初始化链目录...${NC}"

mkdir -p "$STORAGE"
chmod 700 "$STORAGE"

if [ ! -f "$STORAGE/chain_head.json" ]; then
    # 生成创世文件
    GENESIS_FILE="$STORAGE/genesis.txt"
    cat > "$GENESIS_FILE" << GENESIS
# 龍魂信任链 · 创世版本
# 环境: $ENV
# 域名: $DOMAIN
# DNA: #龍芯⚡️丙午·甲申·辛丑·坤卦-GENESIS-$ENV-UID9622
GENESIS

    GENESIS_HASH=$($HASH_CMD "$GENESIS_FILE" | awk '{print $1}')

    cat > "$STORAGE/chain_head.json" << JSONHEAD
{
  "genesis_hash": "$GENESIS_HASH",
  "author": "UID9622",
  "environment": "$ENV",
  "domain": "$DOMAIN",
  "created_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "chain_version": "1.1.0",
  "hash_algo": "$HASH_ALGO"
}
JSONHEAD

    echo -e "  ${GREEN}✅ 链目录已初始化${NC}"
else
    echo -e "  ${GREEN}✅ 链目录已存在，跳过初始化${NC}"
fi

# -----------------------------------------------------------------------------
# 步骤5: 部署验证服务
# 仅演示模式：生成一个简单的 systemd 服务文件和启动脚本
# 真实场景应替换为 Python/Go 编写的服务
# -----------------------------------------------------------------------------
echo -e "${YELLOW}[5/7] 部署验证服务...${NC}"

SERVICE_NAME="longhun-trust-chain"
SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"
START_SCRIPT="$STORAGE/start_server.sh"

cat > "$START_SCRIPT" << STARTER
#!/bin/bash
# 启动信任链验证服务（占位脚本）
# 真实生产环境请替换为实际服务启动命令
# 示例: python3 /opt/longhun/trust_chain_server.py --port $PORT --storage $STORAGE

echo "🐉 启动龍魂信任链验证服务"
echo "  端口: $PORT"
echo "  存储: $STORAGE"

# 这里使用 Python 内置 http.server 作为占位，仅用于演示
# 生产环境请勿使用！
cd "$STORAGE"
python3 -m http.server $PORT
STARTER

chmod +x "$START_SCRIPT"

if [ "$ENV" = "production" ] && [ -d /etc/systemd/system ]; then
    cat > "$SERVICE_FILE" << SYSTEMD
[Unit]
Description=龍魂信任链验证服务
After=network.target

[Service]
Type=simple
User=longhun
Group=longhun
WorkingDirectory=$STORAGE
ExecStart=$START_SCRIPT
Restart=always
RestartSec=5
Environment=ENV=$ENV
Environment=PORT=$PORT
Environment=STORAGE=$STORAGE

[Install]
WantedBy=multi-user.target
SYSTEMD

    systemctl daemon-reload
    systemctl enable "$SERVICE_NAME"
    systemctl restart "$SERVICE_NAME"
    echo -e "  ${GREEN}✅ systemd服务已部署并启动${NC}"
else
    echo -e "  ${YELLOW}⚠️ 非生产环境，跳过systemd部署${NC}"
    echo -e "  ${YELLOW}   可手动运行: $START_SCRIPT${NC}"
fi

# -----------------------------------------------------------------------------
# 步骤6: 配置监控告警
# 生成 Prometheus 配置和告警脚本
# -----------------------------------------------------------------------------
echo -e "${YELLOW}[6/7] 配置监控告警...${NC}"

ALERT_SCRIPT="$STORAGE/alert.sh"

cat > "$ALERT_SCRIPT" << ALERTER
#!/bin/bash
# 龍魂信任链 · 告警脚本
# 触发条件：验证失败 / 篡改检测 / 存储超过80% / GPG密钥即将过期

LEVEL="\$1"
MESSAGE="\$2"
WEBHOOK="$FEISHU_WEBHOOK"

if [ -z "\$WEBHOOK" ]; then
    echo "未配置飞书Webhook，仅打印告警: [\$LEVEL] \$MESSAGE"
    exit 0
fi

curl -s -X POST -H "Content-Type: application/json" \\
    "\$WEBHOOK" \\
    -d "{\"msg_type\":\"text\",\"content\":{\"text\":\"🐉龍魂信任链告警\\n级别: \$LEVEL\\n消息: \$MESSAGE\"}}"
ALERTER

chmod +x "$ALERT_SCRIPT"

# 生成 Prometheus 抓取配置
mkdir -p "$STORAGE/monitor"
cat > "$STORAGE/monitor/prometheus.yml" << PROM
# 龍魂信任链 Prometheus 配置
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'longhun-trust-chain'
    static_configs:
      - targets: ['$DOMAIN:$PORT']
    metrics_path: /metrics
PROM

if [ -n "$FEISHU_WEBHOOK" ]; then
    echo -e "  ${GREEN}✅ 监控告警已配置${NC}"
else
    echo -e "  ${YELLOW}⚠️ 未配置飞书Webhook，告警仅本地打印${NC}"
fi

# -----------------------------------------------------------------------------
# 步骤7: 健康检查
# 检查服务是否可达，链目录权限是否正确
# -----------------------------------------------------------------------------
echo -e "${YELLOW}[7/7] 健康检查...${NC}"

HEALTH_OK=true

# 检查存储权限
PERM=$(stat -c %a "$STORAGE" 2>/dev/null || stat -f %Lp "$STORAGE" 2>/dev/null)
if [ "$PERM" != "700" ]; then
    echo -e "  ${YELLOW}⚠️ 存储目录权限为 $PERM，建议设置为 700${NC}"
fi

# 检查链头文件
if [ ! -f "$STORAGE/chain_head.json" ]; then
    echo -e "  ${RED}❌ 链头文件缺失${NC}"
    HEALTH_OK=false
fi

# 检查服务端口（如果服务已启动）
if curl -s "http://$DOMAIN:$PORT/health" &> /dev/null; then
    echo -e "  ${GREEN}✅ 验证服务健康检查通过${NC}"
else
    echo -e "  ${YELLOW}⚠️ 验证服务未启动或健康接口未实现${NC}"
fi

# -----------------------------------------------------------------------------
# 部署结论
# -----------------------------------------------------------------------------
echo ""
echo -e "${BLUE}========================================${NC}"
if [ "$HEALTH_OK" = true ]; then
    echo -e "${GREEN}✅ 部署完成${NC}"
    echo ""
    echo "  服务地址: http://$DOMAIN:$PORT"
    echo "  存储路径: $STORAGE"
    echo "  启动脚本: $START_SCRIPT"
    echo "  告警脚本: $ALERT_SCRIPT"
    echo "  监控配置: $STORAGE/monitor/prometheus.yml"
    echo ""
    echo "  常用命令:"
    echo "    验证链:     curl -X POST http://$DOMAIN:$PORT/chain/verify"
    echo "    健康检查:   curl http://$DOMAIN:$PORT/health"
    echo "    查看指标:   curl http://$DOMAIN:$PORT/metrics"
else
    echo -e "${RED}🔴 部署存在异常，请检查上方日志${NC}"
    exit 1
fi

# -----------------------------------------------------------------------------
# 仅验证模式：如果开启 --verify-only，部署后执行一次链验证
# -----------------------------------------------------------------------------
if [ "$VERIFY_ONLY" = true ]; then
    echo -e "${YELLOW}🔍 运行验证...${NC}"
    bash "$START_SCRIPT" &
    SERVER_PID=$!
    sleep 2
    curl -s -X POST "http://$DOMAIN:$PORT/chain/verify" || true
    kill "$SERVER_PID" 2>/dev/null || true
fi
