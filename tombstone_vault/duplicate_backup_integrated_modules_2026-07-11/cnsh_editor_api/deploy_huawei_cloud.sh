#!/usr/bin/env bash
# 龍魂 CNSH Editor API · 华为云/鲲鹏部署脚本
# DNA: #龍芯⚡️2026-07-04-CNSH-API-DEPLOY-HUAWEI-v1.0
set -euo pipefail

# ─────────────────────────────────────────
# 使用前必须在华为云控制台准备以下信息，并填入环境变量：
#   export HW_ACCESS_KEY_ID=你的AK
#   export HW_SECRET_ACCESS_KEY=你的SK
#   export HW_REGION=cn-southwest-2
#   export HW_ECS_IP=你的弹性公网IP
#   export HW_ECS_USER=root
#   export HW_SWR_SERVER=你的SWR域名（如 swr.cn-southwest-2.myhuaweicloud.com）
#   export HW_SWR_ORGANIZATION=你的组织名
#   export HW_SWR_REPOSITORY=cnsh-editor-api
# ─────────────────────────────────────────

REQUIRED_VARS=(HW_ACCESS_KEY_ID HW_SECRET_ACCESS_KEY HW_REGION HW_ECS_IP HW_ECS_USER HW_SWR_SERVER HW_SWR_ORGANIZATION HW_SWR_REPOSITORY)
for v in "${REQUIRED_VARS[@]}"; do
    if [[ -z "${!v:-}" ]]; then
        echo "❌ 缺少环境变量: $v"
        echo "请先配置华为云 AK/SK、区域、ECS IP、SWR 镜像仓库信息。"
        exit 1
    fi
done

VERSION=${VERSION:-$(date +%Y%m%d%H%M%S)}
IMAGE="${HW_SWR_SERVER}/${HW_SWR_ORGANIZATION}/${HW_SWR_REPOSITORY}:${VERSION}"
LATEST="${HW_SWR_SERVER}/${HW_SWR_ORGANIZATION}/${HW_SWR_REPOSITORY}:latest"

echo "🐉 龍魂 CNSH Editor API · 华为云/鲲鹏部署"
echo "    版本: ${VERSION}"
echo "    镜像: ${IMAGE}"

# 1. 使用 buildx 构建多架构镜像（默认鲲鹏 ARM64）
echo "🔨 步骤 1/5: 构建 ARM64 镜像..."
docker buildx build \
    --platform linux/arm64 \
    -t "${IMAGE}" \
    -t "${LATEST}" \
    -f integrated-modules/cnsh_editor_api/Dockerfile \
    --push \
    .

# 2. 登录华为云 SWR（若未登录）
echo "🔐 步骤 2/5: 登录华为云 SWR..."
docker login -u "${HW_ACCESS_KEY_ID}" -p "${HW_SECRET_ACCESS_KEY}" "${HW_SWR_SERVER}" || true

# 3. 推送镜像（buildx --push 已推送，此处做二次校验）
echo "📤 步骤 3/5: 校验镜像推送..."
docker pull "${IMAGE}" || true

# 4. SSH 到华为云 ECS 部署容器
echo "🚀 步骤 4/5: 在华为云 ECS 上部署..."
ssh -o StrictHostKeyChecking=no "${HW_ECS_USER}@${HW_ECS_IP}" <<EOF
set -e
echo "拉取镜像: ${IMAGE}"
docker pull "${IMAGE}"
echo "停止旧容器..."
docker rm -f cnsh-editor-api 2>/dev/null || true
echo "启动新容器（paid tier · 完整全能版）..."
docker run -d \
    --name cnsh-editor-api \
    --restart unless-stopped \
    -e CNSH_API_TIER=paid \
    -e CNSH_API_HOST=0.0.0.0 \
    -e CNSH_API_PORT=8000 \
    -p 8000:8000 \
    "${IMAGE}"
echo "等待服务就绪..."
sleep 5
curl -s http://localhost:8000/api/v1/health | head -c 200
echo ""
EOF

# 5. 本地探测公网健康接口
echo "🩺 步骤 5/5: 公网健康检查..."
sleep 3
curl -s "http://${HW_ECS_IP}:8000/api/v1/health" | head -c 200 || true
echo ""

echo "✅ 部署完成。访问地址："
echo "   编辑器: http://${HW_ECS_IP}:8000/editor"
echo "   API 文档: http://${HW_ECS_IP}:8000/docs"
echo "   DNA: #龍芯⚡️2026-07-04-CNSH-API-DEPLOY-HUAWEI-v1.0"
