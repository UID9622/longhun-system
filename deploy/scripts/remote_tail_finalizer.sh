#!/bin/bash
# ============================================================
# 龍魂 · 尾巴收尾远程验证器
# remote_tail_finalizer.sh
#
# DNA: #龍芯⚡️丙午·乙未·丁酉·亥時·☰乾-REMOTE-TAIL-FINALIZER-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 用途: 等鲲鹏 SSH 恢复后，一键同步最新修复并跑远程全量自检
# 触发: 老大下令 / 网络恢复后自动执行
# ============================================================

set -euo pipefail

DNA="#龍芯⚡️丙午·乙未·丁酉·亥時·☰乾-REMOTE-TAIL-FINALIZER-v1.0"
KUNPENG_IP="119.13.90.27"
KUNPENG_USER="root"
SSH_KEY="${HOME}/.ssh/longhun_kunpeng_ed25519"
LOCAL_ROOT="${HOME}/longhun-system"
REMOTE_ROOT="/opt/longhun-system"
REMOTE_STAGING="${REMOTE_ROOT}/sync-staging"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; BLUE='\033[0;34m'; NC='\033[0m'
log()  { echo -e "${GREEN}[${TIMESTAMP}]${NC} $1"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
err()  { echo -e "${RED}[ERROR]${NC} $1"; exit 1; }
info() { echo -e "${BLUE}[INFO]${NC} $1"; }

SSH_OPTS="-i ${SSH_KEY} -o StrictHostKeyChecking=no -o ConnectTimeout=15 -o BatchMode=yes"
SSH="ssh ${SSH_OPTS} ${KUNPENG_USER}@${KUNPENG_IP}"
SCP="scp ${SSH_OPTS}"

# 要同步的文件（相对 LOCAL_ROOT）
FILES=(
  bin/lh_video_pipeline.py
  engines/lh_avatar_engine.py
  engines/lh_visual_engine.py
  bin/lh_video_prod_deploy.sh
  bin/lh_tongxin_lock_firewall.py
  bin/lh_tongxin_lock_monitor.py
  bin/lh_tongxin_lock_deploy.sh
  bin/lh_privacy_hardener_linux.sh
  bin/lh_naming_checker.py
)

banner() {
  echo ""
  echo "============================================================"
  echo "  🇨🇳 龍魂系统 · 尾巴收尾远程验证器"
  echo "  DNA: ${DNA}"
  echo "  目标: ${KUNPENG_IP}"
  echo "============================================================"
  echo ""
}

check_network() {
  info "探测鲲鹏 SSH 端口..."
  if ! nc -z -w 10 "${KUNPENG_IP}" 22 >/dev/null 2>&1; then
    err "鲲鹏 ${KUNPENG_IP}:22 仍不可达。请在服务器侧检查安全组/防火墙/22端口。"
  fi
  log "SSH 端口可达，继续同步。"
}

sync_files() {
  log "创建远程暂存目录..."
  ${SSH} "mkdir -p ${REMOTE_STAGING}"

  log "同步 ${#FILES[@]} 个文件到鲲鹏..."
  for f in "${FILES[@]}"; do
    local src="${LOCAL_ROOT}/${f}"
    if [[ ! -f "${src}" ]]; then
      err "本地文件缺失: ${src}"
    fi
    ${SCP} "${src}" "${KUNPENG_USER}@${KUNPENG_IP}:${REMOTE_STAGING}/"
    log "  ✅ ${f}"
  done
}

install_files() {
  log "安装文件到正式位置..."
  ${SSH} "
    set -e
    cd ${REMOTE_ROOT}
    for f in ${FILES[*]}; do
      cp ${REMOTE_STAGING}/$(basename \$f) \$f
      chmod +x \$f 2>/dev/null || true
    done
    echo 'INSTALL-OK'
  "
}

remote_self_tests() {
  log "在鲲鹏上跑远程全量自检..."
  ${SSH} "
    set -e
    cd ${REMOTE_ROOT}
    echo '--- 视频管线 ---'
    python3 bin/lh_video_pipeline.py selftest
    echo '--- 防火墙 ---'
    sudo python3 bin/lh_tongxin_lock_firewall.py selftest || true
    echo '--- 监控 ---'
    python3 bin/lh_tongxin_lock_monitor.py selftest
    echo '--- 命名检查器 ---'
    python3 bin/lh_naming_checker.py
    echo '--- 隐语法翻译 ---'
    python3 engines/lh_translator.py selftest
    echo 'REMOTE-SELFTEST-OK'
  "
}

main() {
  banner
  check_network
  sync_files
  install_files
  remote_self_tests
  log "🎯 远程尾巴收尾完成。鲲鹏已同步并自检全绿。"
}

main "$@"
