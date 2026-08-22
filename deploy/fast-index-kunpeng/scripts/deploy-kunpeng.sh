#!/bin/bash
# 🐉 龍魂 · 快速索引底座 · 鲲鹏 ARM64 一键部署脚本
# DNA: #龍芯⚡️丙午·丙申·壬戌·乙巳·䷾既济-FAST-INDEX-KUNPENG-DEPLOY-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

set -e

echo "🐉 开始部署龍魂快速索引底座到鲲鹏..."

# 检查架构
ARCH=$(uname -m)
if [[ "$ARCH" != "aarch64" && "$ARCH" != "arm64" ]]; then
    echo "⚠️ 当前架构 $ARCH，本脚本针对鲲鹏 ARM64 (aarch64) 优化"
fi

# 检查 Docker
if ! command -v docker &> /dev/null; then
    echo "❌ 未检测到 docker，请先安装 Docker"
    exit 1
fi
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ 未检测到 docker-compose，请先安装"
    exit 1
fi

COMPOSE_FILE="docker-compose.kunpeng.yml"

# 设置项目路径
export LONGHUN_SYSTEM_PATH=${LONGHUN_SYSTEM_PATH:-/opt/longhun-system}
if [[ ! -d "$LONGHUN_SYSTEM_PATH" ]]; then
    echo "⚠️ 项目路径 $LONGHUN_SYSTEM_PATH 不存在，将使用当前目录映射"
    export LONGHUN_SYSTEM_PATH=$(cd ../.. && pwd)
fi

echo "📁 项目路径: $LONGHUN_SYSTEM_PATH"

# 确保入口脚本存在
if [[ ! -f "$LONGHUN_SYSTEM_PATH/05_ENGINES/lh_fast_index_core.py" ]]; then
    echo "❌ 未找到 05_ENGINES/lh_fast_index_core.py，请确认 LONGHUN_SYSTEM_PATH"
    exit 1
fi

# 启动服务
echo "🚀 启动 Ollama + 快速索引服务..."
if docker compose version &> /dev/null; then
    docker compose -f "$COMPOSE_FILE" up -d
else
    docker-compose -f "$COMPOSE_FILE" up -d
fi

# 拉取嵌入模型
echo "⬇️ 预拉取嵌入模型 nomic-embed-text..."
sleep 5
docker exec longhun-ollama ollama pull nomic-embed-text || echo "⚠️ 模型拉取可能仍在后台进行，稍后可重试"

# 索引项目文档
echo "📚 索引项目文档..."
sleep 3
curl -s -X POST http://127.0.0.1:8768/index \
    -H "Content-Type: application/json" \
    -d "{\"dir\":\"/opt/longhun-system/12_DOCS\",\"pattern\":\"*.md\"}" || echo "⚠️ 索引接口暂未就绪，可手动执行"

echo ""
echo "✅ 部署完成"
echo "   服务地址: http://127.0.0.1:8768"
echo "   Ollama  : http://127.0.0.1:11434"
echo "   查看状态: curl http://127.0.0.1:8768/stats"
