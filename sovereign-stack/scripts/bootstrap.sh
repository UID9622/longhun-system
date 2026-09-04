#!/bin/bash
# 🐉 龍魂 sovereign-stack 一键启动脚本 v2.0
# 原则：个人开发者一条命令跑起来
# DNA: #龍芯⚡️2026-08-31-BOOTSTRAP-V2.0-UID9622
# 创建者: 诸葛鑫（UID9622）· 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# 协议: MulanPSL v2（工程实现层）
set -e
cd "$(dirname "$0")/.."   # 进入项目根目录

echo "🐉 龍魂 sovereign-stack 启动中..."
echo "🧬 DNA: #龍芯⚡️$(date +%Y-%m-%d)-BOOTSTRAP-START-UID9622"

# ── 检查依赖
command -v python3 >/dev/null 2>&1 || { echo "❌ 需要安装 Python 3.11+"; exit 1; }
HAS_DOCKER=1
command -v docker >/dev/null 2>&1 || { echo "🟡 未安装 Docker，跳过容器服务（SearXNG/依赖隔离）"; HAS_DOCKER=0; }

# ── 安装 Python 依赖
echo "📦 安装 Python 依赖..."
pip3 install -r pricing/requirements.txt -q
pip3 install -r search-engine/requirements.txt -q
[ -f free-tier/requirements.txt ] && pip3 install -r free-tier/requirements.txt -q || true
[ -f evaluator/requirements.txt ] && pip3 install -r evaluator/requirements.txt -q || true

# ── 构建镜像（容错：缺 Dockerfile 的模块跳过）
if [ "$HAS_DOCKER" = "1" ]; then
  [ -f api-gateway/Dockerfile ] && { echo "🔨 构建 API 网关镜像..."; docker build -t sovereign-gateway api-gateway -q; } || echo "🟡 api-gateway/Dockerfile 缺失，跳过镜像构建"
  [ -f search-engine/Dockerfile ] && { docker build -t longhun-searcher search-engine -q; } || true

  # ── 启动 SearXNG（本地搜索·完全免费）
  echo "🔍 启动本地搜索引擎（SearXNG）..."
  docker compose -f search-engine/searxng-compose.yml up -d 2>/dev/null || docker-compose -f search-engine/searxng-compose.yml up -d 2>/dev/null || echo "🟡 SearXNG 启动跳过（Compose 不可用）"
  sleep 3

  # ── 启动依赖隔离沙箱（容错）
  [ -f dependency-isolation/docker-compose.yml ] && { echo "🏗️ 启动依赖隔离沙箱..."; docker compose -f dependency-isolation/docker-compose.yml up -d; } || true
fi

# ── 启动 API 网关（容错）
if [ "$HAS_DOCKER" = "1" ] && [ -f api-gateway/Dockerfile ]; then
  echo "🚪 启动 API 网关..."
  docker run -d -p 9000:9000 \
    -e BACKEND_URL="${BACKEND_URL:-http://host.docker.internal:8080}" \
    -e METER_URL="http://host.docker.internal:8897" \
    --name sovereign-gateway \
    sovereign-gateway 2>/dev/null || docker start sovereign-gateway
fi

# ── 启动搜索服务（多后端）
echo "🔍 启动搜索服务..."
mkdir -p ~/.longhun/logs
nohup python3 search-engine/search.py --server \
  > ~/.longhun/logs/search.log 2>&1 &
echo "  搜索服务已在 :8890 启动"

# ── 启动计量服务（按量计费）
echo "💰 启动计量服务..."
nohup python3 pricing/meter.py \
  > ~/.longhun/logs/meter.log 2>&1 &
echo "  计量服务已在 :8897 启动"

# ── 启动配额管理（个人开发者免费额度）
echo "👤 启动配额管理..."
nohup python3 free-tier/quota_manager.py \
  > ~/.longhun/logs/quota.log 2>&1 &
echo "  配额管理已在 :8895 启动"

sleep 2

echo ""
echo "╔══════════════════════════════════════════╗"
echo "║  ✅ 龍魂 sovereign-stack 启动完成！      ║"
echo "║                                          ║"
echo "║  服务端口：                              ║"
echo "║  🚪 API 网关:    http://localhost:9000   ║"
echo "║  🔍 搜索服务:    http://localhost:8890   ║"
echo "║  🔍 SearXNG:     http://localhost:8888   ║"
echo "║  💰 计量服务:    http://localhost:8897   ║"
echo "║  👤 配额管理:    http://localhost:8895   ║"
echo "║  🔌 依赖隔离:    http://localhost:5001   ║"
echo "║                                          ║"
echo "║  验证：                                  ║"
echo "║  curl http://localhost:9000/health       ║"
echo "║  curl http://localhost:8890/health       ║"
echo "╚══════════════════════════════════════════╝"
echo ""
echo "🧬 DNA: #龍芯⚡️$(date +%Y-%m-%d)-BOOTSTRAP-DONE-V2.0-UID9622"
echo "🔐 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
