#!/usr/bin/env bash
# 🐉 龍魂 · DeepSeek Harness 鲲鹏一键部署脚本
# DNA: #龍芯⚡️丙午·丙申·辛酉·丙申·䷉履-DSH-KUNPENG-DEPLOY-SCRIPT-UID9622

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_DIR"

echo "🐉 开始部署 DeepSeek Harness 到鲲鹏 ARM64..."

# ============================================================
# 1. 环境检查
# ============================================================
echo "📋 检查环境..."
if ! command -v docker >/dev/null 2>&1; then
    echo "❌ 未安装 Docker，请先安装 Docker Engine"
    exit 1
fi
if ! docker compose version >/dev/null 2>&1; then
    echo "❌ 需要 Docker Compose v2 (docker compose)，请安装 compose plugin"
    exit 1
fi

ARCH=$(uname -m)
if [ "$ARCH" != "aarch64" ] && [ "$ARCH" != "arm64" ]; then
    echo "⚠️ 当前架构为 $ARCH，本脚本主要针对 aarch64/arm64 优化"
fi

# ============================================================
# 2. 确认码闸门 (支持环境变量跳过交互, 供自动化 CI 使用)
# ============================================================
CONFIRM_CODE="${CONFIRM_CODE:-龍魂9622}"
if [ -t 0 ] && [ -z "${DSH_NONINTERACTIVE:-}" ]; then
    echo "🔐 确认码闸门：请输入 [龍魂9622] 继续 (或用 CONFIRM_CODE=龍魂9622 跳过)"
    read -r confirm
else
    confirm="$CONFIRM_CODE"
fi
if [ "$confirm" != "龍魂9622" ]; then
    echo "❌ 确认失败，已取消部署"
    exit 1
fi

# ============================================================
# 3. 生成龍魂 Profile (env_file 被 compose 真实引用)
# ============================================================
echo "🔧 生成龍魂配置..."
mkdir -p ~/.longhun/configs ~/.longhun/04_AUDIT

# 备份到本地用户目录便于审计
cp configs/longhun-system-prompt.md ~/.longhun/configs/longhun-system-prompt.md
cp configs/terminal-writer.yaml ~/.longhun/configs/terminal-writer.yaml

DEFAULT_MODEL="${DSH_DEFAULT_MODEL:-deepseek-r1:14b}"
cat > configs/dsh-kunpeng.env << EOF
# 🐉 龍魂 · DeepSeek Harness 环境变量 (docker-compose env_file, 由 deploy 脚本生成)
# 切换模型 = 修改 DSH_DEFAULT_MODEL 后执行: docker compose up -d --force-recreate dsh
DSH_DEFAULT_MODEL=${DEFAULT_MODEL}
DSH_LOG_LEVEL=info
EOF

# ============================================================
# 4. 拉取镜像并启动
# ============================================================
echo "🐳 拉取 ARM64 镜像..."
docker compose -f docker-compose.kunpeng.yml pull ollama dsh

echo "🚀 启动服务..."
docker compose -f docker-compose.kunpeng.yml up -d ollama

# 等待 Ollama 就绪
echo "⏳ 等待 Ollama 就绪..."
READY=0
for i in {1..30}; do
    if docker compose -f docker-compose.kunpeng.yml exec -T ollama ollama list >/dev/null 2>&1; then
        echo "✅ Ollama 已就绪"
        READY=1
        break
    fi
    echo "  等待中... ($i/30)"
    sleep 2
done
if [ "$READY" -eq 0 ]; then
    echo "❌ Ollama 未就绪，请检查: docker compose logs ollama"
    exit 1
fi

# 拉取默认模型 (仅当未下载时)
if ! docker compose -f docker-compose.kunpeng.yml exec -T ollama ollama list | grep -q "${DEFAULT_MODEL%%:*}"; then
    echo "📥 拉取默认模型 ${DEFAULT_MODEL}（首次约 9GB，可能需要 10-30 分钟）..."
    docker compose -f docker-compose.kunpeng.yml exec -T ollama ollama pull "$DEFAULT_MODEL" || {
        echo "⚠️ 模型拉取失败，可手动执行: docker compose exec ollama ollama pull $DEFAULT_MODEL"
    }
else
    echo "✅ 模型 ${DEFAULT_MODEL} 已存在，跳过拉取"
fi

echo "🚀 启动 DeepSeek Harness..."
docker compose -f docker-compose.kunpeng.yml up -d dsh

# ============================================================
# 5. 健康检查
# ============================================================
echo "🏥 健康检查..."
sleep 5
if curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:2283/api/health 2>/dev/null | grep -qE "200|404"; then
    echo "✅ dsh 服务可访问"
else
    echo "⚠️ dsh 尚未就绪，稍后可执行: docker compose logs -f dsh 查看"
fi

echo "📊 服务状态:"
docker compose -f docker-compose.kunpeng.yml ps

echo ""
echo "✅ 部署完成"
echo "   Web UI:  http://127.0.0.1:2283"
echo "   API:     http://127.0.0.1:2284"
echo "   Ollama:  http://127.0.0.1:11434"
echo "   看板:    http://127.0.0.1:2285 (需要: docker compose --profile dashboard up -d)"
echo ""
echo "   Mac 本地执行: make tunnel KUNPENG_IP=<IP>"
echo "   然后访问: http://127.0.0.1:2283"
