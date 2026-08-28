#!/usr/bin/env bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 🐉 龍魂 · 华为云自动同步守护
# DNA: #龍芯⚡️丙午·丙申·乙卯·辰时·䷌同人-SYNC-WORKER-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#
# 用途：定时检测华为云连通性，连通即增量同步。
# 部署：cron 每10分钟执行一次
#   */10 * * * * /bin/bash /Users/zuimeidedeyihan/longhun-system/deploy/auto_sync/longhun_sync_worker.sh >> /Users/zuimeidedeyihan/longhun-system/deploy/auto_sync/sync.log 2>&1
#
# 铁律：
#   - 不删远程文件（rsync --delete 默认关闭）
#   - 不覆盖远程的 .kunpeng_* / .env 等敏感配置
#   - 连接失败静默跳过，不报警

set -euo pipefail

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'; NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
LOG_FILE="${SCRIPT_DIR}/sync.log"
CONFIG_FILE="${PROJECT_ROOT}/deploy/.kunpeng_config"

# 加载配置
if [[ -f "$CONFIG_FILE" ]]; then
    source "$CONFIG_FILE"
else
    echo "[$(date '+%m-%d %H:%M')] ⚠️ 配置未找到，跳过。请先执行: bash deploy/connect-kunpeng.sh config"
    exit 0
fi

log() { echo "[$(date '+%m-%d %H:%M:%S')] $*"; }

# ─── 步骤 1: 快速连通性检查 ───
log "🔍 检测 ${KUNPENG_MGMT_IP}..."

if ! ssh -i "${KUNPENG_KEY}" \
    -p "${KUNPENG_SSH_PORT}" \
    -o StrictHostKeyChecking=accept-new \
    -o ConnectTimeout=8 \
    -o BatchMode=yes \
    "${KUNPENG_USER}@${KUNPENG_MGMT_IP}" \
    "echo ok" &>/dev/null; then
    log "⏳ 不可达，下次再试。"
    exit 0
fi

log "✅ 连通，开始同步..."

# ─── 步骤 2: 确认远程目录存在 ───
ssh -i "${KUNPENG_KEY}" \
    -p "${KUNPENG_SSH_PORT}" \
    -o ConnectTimeout=10 \
    "${KUNPENG_USER}@${KUNPENG_MGMT_IP}" \
    "mkdir -p ${KUNPENG_DEPLOY_PATH}" 2>/dev/null || true

# ─── 步骤 3: rsync 增量同步 ───
EXCLUDES=(
    ".git/" "__pycache__/" "*.pyc" "*.pyo"
    ".mypy_cache/" ".pytest_cache/" ".venv/" "venv/" "node_modules/"
    ".vscode/" ".idea/" ".DS_Store" "logs/" "*.log"
    "*.dSYM/" ".codebuddy/" "backups/"
    "deploy/.kunpeng_*" "deploy/.env*"
    "*.db" "*.sqlite" "*.sqlite3"
    # ─── 8/28 大目录排除（防全仓同步踩坑）───
    "08_BIN/story_factory/third_party/" "龍魂成片/" "videos/" "voices/"
    "models/" "11_DATA/" "_work/" "archive/"
    "_private/" "browser_profile/" "dist/" "build_ide/" "dist_ide/" "_QUARANTINE/"
    "*/target/" "*.app/" "*.ckpt" "*.safetensors"
)

EXC_ARGS=""
for p in "${EXCLUDES[@]}"; do
    EXC_ARGS="${EXC_ARGS} --exclude='${p}'"
done

eval rsync -avz --progress \
    ${EXC_ARGS} \
    -e "ssh -p ${KUNPENG_SSH_PORT} -i ${KUNPENG_KEY} -o StrictHostKeyChecking=accept-new -o ConnectTimeout=15" \
    "${PROJECT_ROOT}/" \
    "${KUNPENG_USER}@${KUNPENG_MGMT_IP}:${KUNPENG_DEPLOY_PATH}/" \
    2>&1 | tail -3

# ─── 步骤 4: 修正脚本权限 ───
ssh -i "${KUNPENG_KEY}" \
    -p "${KUNPENG_SSH_PORT}" \
    -o ConnectTimeout=10 \
    "${KUNPENG_USER}@${KUNPENG_MGMT_IP}" \
    "find ${KUNPENG_DEPLOY_PATH} -name '*.sh' -exec chmod +x {} \;" 2>/dev/null || true

# ─── 事件数 ───
SYNC_COUNT=$(rsync -an --itemize-changes ${EXC_ARGS} \
    -e "ssh -p ${KUNPENG_SSH_PORT} -i ${KUNPENG_KEY} -o ConnectTimeout=10" \
    "${PROJECT_ROOT}/" \
    "${KUNPENG_USER}@${KUNPENG_MGMT_IP}:${KUNPENG_DEPLOY_PATH}/" 2>/dev/null | wc -l | tr -d ' ')

log "✅ 同步完成 | 变化文件数: ${SYNC_COUNT}"

# ─── 日志轮转：超过500行裁一半 ───
MAX_LINES=500
CURRENT_LINES=$(wc -l < "$LOG_FILE" 2>/dev/null || echo 0)
if [ "$CURRENT_LINES" -gt "$MAX_LINES" ]; then
    tail -n "$MAX_LINES" "$LOG_FILE" > "${LOG_FILE}.tmp" && mv "${LOG_FILE}.tmp" "$LOG_FILE"
fi
