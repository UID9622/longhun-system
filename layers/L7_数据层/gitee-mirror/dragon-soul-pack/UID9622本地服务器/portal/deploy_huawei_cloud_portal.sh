#!/usr/bin/env bash
# 龍魂统一门户 longhun888.com · 华为云/鲲鹏一键部署
# DNA: #龍芯⚡️2026-07-04-LONGHUN888-PORTAL-DEPLOY-v1.0
set -euo pipefail

# ─────────────────────────────────────────
# 前置环境变量（必须）
#   export HW_ACCESS_KEY_ID=你的AK
#   export HW_SECRET_ACCESS_KEY=你的SK
#   export HW_REGION=cn-southwest-2
#   export HW_ECS_IP=你的弹性公网IP
#   export HW_ECS_USER=root
#   export HW_SWR_SERVER=swr.cn-southwest-2.myhuaweicloud.com
#   export HW_SWR_ORGANIZATION=你的组织名
# ─────────────────────────────────────────

REQUIRED_VARS=(HW_ACCESS_KEY_ID HW_SECRET_ACCESS_KEY HW_REGION HW_ECS_IP HW_ECS_USER HW_SWR_SERVER HW_SWR_ORGANIZATION)
for v in "${REQUIRED_VARS[@]}"; do
    if [[ -z "${!v:-}" ]]; then
        echo "❌ 缺少环境变量: $v"
        exit 1
    fi
done

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PORTAL_DIR="$(cd "$(dirname "$0")" && pwd)"
VERSION=${VERSION:-$(date +%Y%m%d%H%M%S)}
SWR_IMAGE="${HW_SWR_SERVER}/${HW_SWR_ORGANIZATION}/cnsh-editor-api:${VERSION}"
REMOTE_DIR="/opt/longhun888"

echo "🐉 龍魂统一门户 longhun888.com · 华为云/鲲鹏部署"
echo "    API 镜像: ${SWR_IMAGE}"
echo "    ECS: ${HW_ECS_IP}"
echo "    版本: ${VERSION}"

# 1. 构建并推送 CNSH Editor API 镜像
echo "🔨 步骤 1/6: 构建 ARM64 镜像..."
cd "${REPO_ROOT}"
docker buildx build \
    --platform linux/arm64 \
    -t "${SWR_IMAGE}" \
    -f integrated-modules/cnsh_editor_api/Dockerfile \
    --push \
    .

# 2. 登录 SWR
echo "🔐 步骤 2/6: 登录华为云 SWR..."
docker login -u "${HW_ACCESS_KEY_ID}" -p "${HW_SECRET_ACCESS_KEY}" "${HW_SWR_SERVER}" || true

# 3. 确保远程目录存在
echo "📂 步骤 3/6: 准备 ECS 目录..."
ssh -o StrictHostKeyChecking=no "${HW_ECS_USER}@${HW_ECS_IP}" "mkdir -p ${REMOTE_DIR}"

# 4. 上传门户文件到 ECS
echo "📤 步骤 4/6: 上传门户文件..."
rsync -avz --delete \
    "${PORTAL_DIR}/" \
    "${HW_ECS_USER}@${HW_ECS_IP}:${REMOTE_DIR}/"

# 5. 远程启动 Docker Compose
echo "🚀 步骤 5/6: 在 ECS 上启动服务..."
ssh -o StrictHostKeyChecking=no "${HW_ECS_USER}@${HW_ECS_IP}" <<EOF
set -e
cd ${REMOTE_DIR}
echo "SWR_IMAGE=${SWR_IMAGE}" > .env

docker pull "${SWR_IMAGE}"
docker compose down 2>/dev/null || true
docker compose up -d

sleep 3
echo "=== 容器状态 ==="
docker compose ps
EOF

# 6. 公网探测
echo "🩺 步骤 6/6: 公网健康检查..."
sleep 5
curl -s "http://${HW_ECS_IP}/" | head -c 200 || true
echo ""
curl -s "http://${HW_ECS_IP}/api/v1/health" | head -c 200 || true
echo ""

echo ""
echo "✅ 部署完成"
echo "   门户: http://${HW_ECS_IP}/"
echo "   编辑器: http://${HW_ECS_IP}/editor/"
echo "   API 文档: http://${HW_ECS_IP}/docs"
echo "   DNA: #龍芯⚡️2026-07-04-LONGHUN888-PORTAL-DEPLOY-v1.0"
echo ""
echo "⚠️  域名 longhun888.com 需要在 DNS 解析到 ${HW_ECS_IP}"
echo "⚠️  若需 HTTPS，请配置 SSL 证书（华为云 SSL / certbot）"

# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# DNA: #龍芯⚡️丙午·丙申·甲寅·申时·节-CONFIRM-SEAL-deploy_huawei_cloud_-262D6A26
