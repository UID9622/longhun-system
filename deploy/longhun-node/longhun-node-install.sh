#!/bin/bash
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂系统 · 节点一键部署脚本 v2.0
# DNA: #龍芯⚡️丙午·辛未·乙酉·卯时·䷅讼-NODE-INSTALL-v2.0
# 功能：自动检查Docker、生成DNA、构建/拉取镜像、启动节点

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

DNA_ANCHOR="#龍芯⚡️丙午·辛未·乙酉·卯时·䷅讼-TRAIN-DATA-SOURCES-v2.0"
CONFIRM="#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"

echo "🐉 龍魂节点部署器 v2.0"
echo "🐉 DNA: $DNA_ANCHOR"
echo "🐉 $CONFIRM"
echo "🐉 项目: $PROJECT_ROOT"
echo ""

# ============ 配置 ============
NODE_NAME="${NODE_NAME:-longhun-node}"
REGISTRY_URL="${REGISTRY_URL:-http://localhost:9623}"
DATA_DIR="${DATA_DIR:-$HOME/longhun-node-data}"
PORT="${PORT:-9622}"

# ============ 检查Docker ============
echo "🔧 检查环境..."

DOCKER_AVAILABLE=false
if command -v docker &> /dev/null && docker info &> /dev/null 2>&1; then
    DOCKER_VERSION=$(docker --version | grep -oE '[0-9]+\.[0-9]+' | head -1)
    echo "✅ Docker: $DOCKER_VERSION"
    DOCKER_AVAILABLE=true
else
    echo "⚠️  Docker 不可用，将使用本地进程模式部署"
fi

# ============ 生成节点DNA ============
echo ""
echo "🧬 生成节点身份..."

TIMESTAMP=$(date +%s)
RAND=$(openssl rand -hex 4 2>/dev/null || cat /dev/urandom | head -c 8 | xxd -p 2>/dev/null || echo "$RANDOM")
NODE_ID="LH-${TIMESTAMP}-${RAND}"
NODE_DNA=$(echo -n "${NODE_ID}${DNA_ANCHOR}" | shasum -a 256 | cut -c1-16)

mkdir -p "$DATA_DIR"/{logs,fetched,cleaned,train,audit,config}

# 写入环境配置
cat > "$DATA_DIR/config/node.env" << EOF
LONGHUN_NODE_ID=$NODE_ID
LONGHUN_NODE_DNA=$NODE_DNA
LONGHUN_REGISTRY_URL=$REGISTRY_URL
LONGHUN_DNA_ANCHOR=$DNA_ANCHOR
LONGHUN_CONFIRM=$CONFIRM
LONGHUN_DEPLOYED_AT=$(date -Iseconds)
LONGHUN_PROJECT_ROOT=$PROJECT_ROOT
EOF

echo "✅ 节点ID: $NODE_ID"
echo "✅ 节点DNA: $NODE_DNA"
echo "✅ 配置: $DATA_DIR/config/node.env"

# ============ Docker模式 ============
if [ "$DOCKER_AVAILABLE" = true ] && [ "${USE_DOCKER:-yes}" != "no" ]; then
    echo ""
    echo "🐳 Docker模式部署..."

    DOCKERFILE="$PROJECT_ROOT/docker/longhun-node.Dockerfile"
    if [ ! -f "$DOCKERFILE" ]; then
        echo "⚠️  Dockerfile不存在: $DOCKERFILE"
        echo "   使用本地进程模式..."
        DOCKER_AVAILABLE=false
    else
        echo "🔨 构建镜像..."
        cd "$PROJECT_ROOT"
        docker build -t longhun/node:v2.0 -f "$DOCKERFILE" . 2>&1 | tail -5

        # 检查端口占用
        if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
            echo "⚠️  端口 $PORT 被占用，尝试停止旧容器..."
            docker stop "$NODE_NAME" 2>/dev/null || true
            docker rm "$NODE_NAME" 2>/dev/null || true
            sleep 1
        fi

        # 启动
        echo "🚀 启动容器..."
        docker run -d \
            --name "$NODE_NAME" \
            --restart unless-stopped \
            -v "$DATA_DIR:/data" \
            -v "$PROJECT_ROOT:/project:ro" \
            -p "$PORT:9622" \
            --env-file "$DATA_DIR/config/node.env" \
            -e TZ=Asia/Shanghai \
            longhun/node:v2.0

        sleep 2

        if docker ps | grep -q "$NODE_NAME"; then
            echo ""
            echo "═══════════════════════════════════════════════════════"
            echo "✅ Docker节点部署成功！"
            echo "═══════════════════════════════════════════════════════"
            echo ""
            echo "📡 节点信息:"
            echo "   节点ID:   $NODE_ID"
            echo "   节点DNA:  $NODE_DNA"
            echo "   容器名:   $NODE_NAME"
            echo "   本地端口: http://localhost:$PORT"
            echo "   数据目录: $DATA_DIR"
            echo "   注册中心: $REGISTRY_URL"
            echo ""
            echo "📋 常用命令:"
            echo "   docker logs -f $NODE_NAME"
            echo "   docker stop $NODE_NAME"
            echo "   docker restart $NODE_NAME"
            echo ""
            exit 0
        else
            echo "❌ 容器启动失败"
            docker logs "$NODE_NAME" 2>/dev/null || true
            exit 1
        fi
    fi
fi

# ============ 本地进程模式 ============
echo ""
echo "🖥️  本地进程模式部署..."

# 创建启动脚本
LAUNCH_SCRIPT="$DATA_DIR/start_node.sh"
cat > "$LAUNCH_SCRIPT" << 'LAUNCH_EOF'
#!/bin/bash
# 龍魂节点本地启动脚本
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/config/node.env"

echo "🐉 龍魂节点启动 (本地进程)"
echo "🐉 节点: $LONGHUN_NODE_ID"

# 启动心跳
python3 "$LONGHUN_PROJECT_ROOT/deploy/longhun-node/node_heartbeat.py" \
    --registry "$LONGHUN_REGISTRY_URL" \
    --node-id "$LONGHUN_NODE_ID" \
    --interval 300 &

# 启动审计（可选）
# python3 "$LONGHUN_PROJECT_ROOT/deploy/longhun-node/node_audit.py" --daemon &

echo "✅ 节点已启动"
echo "📋 查看心跳: tail -f /dev/null"  # 占位
wait
LAUNCH_EOF

chmod +x "$LAUNCH_SCRIPT"

echo ""
echo "═══════════════════════════════════════════════════════"
echo "✅ 本地节点部署完成！"
echo "═══════════════════════════════════════════════════════"
echo ""
echo "📡 节点信息:"
echo "   节点ID:   $NODE_ID"
echo "   节点DNA:  $NODE_DNA"
echo "   数据目录: $DATA_DIR"
echo "   注册中心: $REGISTRY_URL"
echo "   项目路径: $PROJECT_ROOT"
echo ""
echo "📋 启动命令:"
echo "   bash $LAUNCH_SCRIPT"
echo ""
echo "🔍 手动心跳测试:"
echo "   cd $PROJECT_ROOT"
echo "   python3 deploy/longhun-node/node_heartbeat.py --registry $REGISTRY_URL --node-id $NODE_ID --once"
echo ""
echo "🔍 审计测试:"
echo "   cd $PROJECT_ROOT"
echo "   LONGHUN_NODE_ID=$NODE_ID python3 deploy/longhun-node/node_audit.py"
echo ""
echo "🐉 龍魂系统 · 节点已就位"
echo "🐉 $CONFIRM"
