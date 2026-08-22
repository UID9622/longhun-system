#!/usr/bin/env bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂 DeepSeek 唯一监管加密执行者部署脚本（轻量包）
# 用法： ./scripts/deploy_deepseek_executor.sh [ECS_IP] [SSH_KEY]
# DNA: #龍芯⚡️丙午·甲午·癸酉·戊午·䷨损-DEEPSEEK-EXECUTOR-DEPLOY-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

set -euo pipefail

ECS_IP="${1:-119.13.90.27}"
SSH_KEY="${2:-$HOME/.ssh/id_ed25519_uid9622}"
REMOTE_USER="root"
REMOTE_DIR="/var/www/longhun/longhun-system"
SECRETS_REMOTE="/var/www/longhun/secrets.env"
SSH_OPTS="-i ${SSH_KEY} -o BatchMode=yes -o StrictHostKeyChecking=no -o ConnectTimeout=10"

echo "🐉 开始部署 DeepSeek 唯一监管加密执行器 -> ${ECS_IP}"

# 0. 创建轻量部署包
echo "📦 创建轻量部署包..."
PKG_DIR="$(mktemp -d)"
mkdir -p "${PKG_DIR}/sovereignty/portal" "${PKG_DIR}/scripts"
# 复制执行器、本地网关、加密工具、模型路由
for f in \
  sovereignty/portal/deepseek_executor.py \
  sovereignty/portal/local_secure_gateway.py \
  sovereignty/portal/longhun_crypto.py \
  sovereignty/portal/model_router.py \
  sovereignty/portal/__init__.py \
  sovereignty/__init__.py \
  scripts/longhun-deepseek-executor.service \
  scripts/longhun-local-gateway.service \
  scripts/nginx-deepseek-executor.conf; do
  cp -v "$(dirname "$0")/../${f}" "${PKG_DIR}/${f}" || true
done

# 避免 sovereignty/__init__.py 里未部署的模块导致 import 失败
: > "${PKG_DIR}/sovereignty/__init__.py"
: > "${PKG_DIR}/sovereignty/portal/__init__.py"

TAR="/tmp/longhun-deepseek-executor.tar.gz"
tar -czf "${TAR}" -C "${PKG_DIR}" .
rm -rf "${PKG_DIR}"

# 1. 上传并解压
ssh ${SSH_OPTS} "${REMOTE_USER}@${ECS_IP}" "mkdir -p ${REMOTE_DIR}"
scp ${SSH_OPTS} "${TAR}" "${REMOTE_USER}@${ECS_IP}:/tmp/"
ssh ${SSH_OPTS} "${REMOTE_USER}@${ECS_IP}" "tar -xzf /tmp/longhun-deepseek-executor.tar.gz -C ${REMOTE_DIR}"

# 2. 同步环境变量
if grep -q '^export LONGHUN_EXECUTOR_SECRET=' "$HOME/.longhun/secrets.env"; then
  echo "🔑 同步 secrets.env..."
  scp ${SSH_OPTS} "$HOME/.longhun/secrets.env" "${REMOTE_USER}@${ECS_IP}:${SECRETS_REMOTE}"
else
  echo "⚠️  本地 ~/.longhun/secrets.env 缺少 LONGHUN_EXECUTOR_SECRET，请先生成"
  exit 1
fi

# 3. 创建虚拟环境并安装依赖
ssh ${SSH_OPTS} "${REMOTE_USER}@${ECS_IP}" "
  cd ${REMOTE_DIR}
  if [ ! -d venv ]; then python3 -m venv venv; fi
  venv/bin/pip install -q --upgrade pip
  venv/bin/pip install -q fastapi uvicorn httpx cryptography requests pydantic
"

# 4. 安装 systemd 服务（源文件在本地 scripts/ 目录）
scp ${SSH_OPTS} "$(dirname "$0")/longhun-deepseek-executor.service" "${REMOTE_USER}@${ECS_IP}:/etc/systemd/system/"
scp ${SSH_OPTS} "$(dirname "$0")/longhun-local-gateway.service" "${REMOTE_USER}@${ECS_IP}:/etc/systemd/system/"
ssh ${SSH_OPTS} "${REMOTE_USER}@${ECS_IP}" "systemctl daemon-reload && systemctl enable longhun-deepseek-executor longhun-local-gateway"

# 5. 应用 Nginx 配置片段
NGINX_REMOTE="/etc/nginx/sites-enabled/longhun888.com"
NGINX_SNIPPET_LOCAL="$(dirname "$0")/nginx-deepseek-executor.conf"
NGINX_INCLUDE="/etc/nginx/longhun-executor.conf"
echo "🔧 注入 Nginx 配置片段..."
ssh ${SSH_OPTS} "${REMOTE_USER}@${ECS_IP}" "cp ${NGINX_REMOTE} ${NGINX_REMOTE}.bak.$(date +%Y%m%d%H%M%S)"
scp ${SSH_OPTS} "${NGINX_SNIPPET_LOCAL}" "${REMOTE_USER}@${ECS_IP}:${NGINX_INCLUDE}"
ssh ${SSH_OPTS} "${REMOTE_USER}@${ECS_IP}" "python3 - <<'PY'
path = '${NGINX_REMOTE}'
include_line = '    include ${NGINX_INCLUDE};'
with open(path, 'r') as f:
    text = f.read().rstrip()
# 删除可能已经存在的 include 行
lines = [l for l in text.splitlines() if l.strip() != include_line.strip()]
text = '\n'.join(lines)
# 在最后一个 '}' 前插入 include
last = text.rfind('}')
if last != -1:
    text = text[:last] + include_line + '\n' + text[last:]
with open(path, 'w') as f:
    f.write(text + '\n')
PY
nginx -t && systemctl reload nginx"

# 6. 启动/重启服务
ssh ${SSH_OPTS} "${REMOTE_USER}@${ECS_IP}" "systemctl restart longhun-local-gateway longhun-deepseek-executor"

# 7. 健康检查
sleep 3
ssh ${SSH_OPTS} "${REMOTE_USER}@${ECS_IP}" "curl -fsS http://127.0.0.1:9623/api/secure/health"
ssh ${SSH_OPTS} "${REMOTE_USER}@${ECS_IP}" "curl -fsS http://127.0.0.1:9453/health"

echo ""
echo "✅ DeepSeek 执行器部署完成"
echo "   本地网关: curl http://127.0.0.1:9622/api/secure/health"
echo "   执行器:   curl http://127.0.0.1:9453/health"
echo "   公网入口: https://longhun888.com/executor/execute"
echo "   DNA: #龍芯⚡️丙午·甲午·癸酉·戊午·䷨损-DEEPSEEK-EXECUTOR-DEPLOY-v1.0"
