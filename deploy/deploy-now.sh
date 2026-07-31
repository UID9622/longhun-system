#!/usr/bin/env bash
# 🐉 龍魂 · 一键部署到鲲鹏 v1.2
# DNA: #龍芯⚡️丙午·乙未·癸亥·蹇-DEPLOY-NOW-v1.2-FIX-SSH-EVAL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
set -euo pipefail

SSH_KEY="$HOME/.ssh/longhun_kunpeng_ed25519"
REMOTE="root@119.13.90.27"
REMOTE_PATH="/opt/longhun-system"
LOCAL_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; CYAN='\033[0;36m'; NC='\033[0m'
ok()  { echo -e "${GREEN}[OK]${NC}  $*"; }
warn(){ echo -e "${YELLOW}[WARN]${NC} $*"; }
err() { echo -e "${RED}[FAIL]${NC} $*"; exit 1; }
info(){ echo -e "${CYAN}[..]${NC}  $*"; }

SSH_OPTS="-p 22 -i ${SSH_KEY} -o StrictHostKeyChecking=accept-new -o ConnectTimeout=10"
SSH="ssh ${SSH_OPTS} ${REMOTE}"
RSYNC_E="ssh ${SSH_OPTS}"

info "=== Step 1/6 连接检测 ==="
if ${SSH} "echo OK" &>/dev/null; then
    ok "鲲鹏在线: ${REMOTE}"
else
    err "无法连接鲲鹏"
fi

info "=== Step 2/6 同步代码 ==="
cd "${LOCAL_ROOT}"

EXC_ARGS=()
EXC_PATTERNS=(
    ".git/" "__pycache__/" "*.pyc" "*.pyo" ".mypy_cache/" ".pytest_cache/"
    ".venv/" "venv/" "env/" "node_modules/" ".next/" "dist/" "build/"
    ".vscode/" ".idea/" ".DS_Store" "logs/" "*.log" "*.tmp" "*.swp"
    "*.dSYM/" "*.app/" "*.db" "*.sqlite" "*.sqlite3"
    "deploy/.kunpeng_config" "deploy/.kunpeng_auth" "backups/" "_archived_reports/"
    "models/" "_archive/" "_work/" "data/" "voices/" "L7_数据层/"
    "_private/" ".cnsh_credentials/" ".env" ".env.*"
    "config/api_keys.env" "deploy/config/.cloud_credentials" "deploy/.cloud_credentials"
    "*.pem" "*.key" "*.crt" "*_credentials*" "*secret*" "vault/" "keys/"
)

for p in "${EXC_PATTERNS[@]}"; do
    EXC_ARGS+=("--exclude=$p")
done

rsync -az --progress "${EXC_ARGS[@]}" \
    -e "${RSYNC_E}" \
    "${LOCAL_ROOT}/" "${REMOTE}:${REMOTE_PATH}/"

ok "代码同步完成"

info "=== Step 3/6 安装 Python 依赖 ==="
${SSH} "cd ${REMOTE_PATH} && pip3 install -r requirements.txt --quiet 2>&1 | tail -3" || warn "依赖安装有警告"

info "=== Step 4/6 重启服务 ==="
${SSH} "systemctl daemon-reload 2>/dev/null" || true
for svc in longhun-core longhun-dashboard longhun-five-harms; do
    if ${SSH} "systemctl is-enabled ${svc} 2>/dev/null" | grep -q enabled; then
        ${SSH} "systemctl restart ${svc}" && ok "重启: ${svc}" || warn "重启失败: ${svc}"
    else
        info "跳过（未启用）: ${svc}"
    fi
done

info "=== Step 5/6 部署 Nginx 配置 ==="
if ${SSH} "test -d /etc/nginx/conf.d"; then
    scp -i "${SSH_KEY}" -o StrictHostKeyChecking=accept-new \
        "${LOCAL_ROOT}/deploy/nginx-uid9622.cn.conf" \
        "${REMOTE}:/etc/nginx/conf.d/uid9622.cn.conf"
    ${SSH} "nginx -t && nginx -s reload" && ok "Nginx 配置更新+重载" || warn "Nginx 重载失败"
else
    info "跳过（无 Nginx）"
fi

info "=== Step 6/6 健康检查 ==="
sleep 2
${SSH} "curl -s http://localhost:9627/ 2>/dev/null | head -5" || warn "Dashboard 暂未响应"
${SSH} "ps aux | grep -E 'python3.*longhun|python3.*http.server 9627' | grep -v grep" | head -5 || warn "服务进程未找到"

echo ""
echo "🐉 部署完成！"
echo "   访问: http://119.13.90.27:9627/"
echo "   SSH:  ${SSH}"
