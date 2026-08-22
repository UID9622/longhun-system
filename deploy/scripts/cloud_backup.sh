#!/bin/bash
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# ═══════════════════════════════════════════════════════
# 龍魂·云备份自动脚本
# 功能: 增量备份 → 百度云BOS → 鲲鹏镜像
# 用法: bash deploy/scripts/cloud_backup.sh [full|incremental]
# DNA: #龍芯⚡️丙午·丙申·癸丑·戊午·䷨损-CLOUD-BACKUP-SCRIPT-v1.0
# ═══════════════════════════════════════════════════════

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
LH_ROOT="$(cd "$SCRIPT_DIR/../../" && pwd)"
LOG_FILE="$LH_ROOT/logs/cloud_backup.log"
TIMESTAMP=$(date +%Y-%m-%dT%H:%M:%S%z)
MODE="${1:-incremental}"

# 备份目录清单
BACKUP_DIRS=(
  "01_protocols"
  "02_SKILLS"
  "03_KNOWLEDGE_GRAPH"
  "04_ENGINES"
  "bin"
  "config"
  "data"
  "deploy"
  "personas"
  "portal"
  "web_apps"
)

mkdir -p "$LH_ROOT/logs"

log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

log "═══════════════════════════════════════"
log "🐉 龍魂云备份开始 (模式: $MODE)"
log "═══════════════════════════════════════"

# ── 1. 百度云BOS同步 ──
log "📤 Phase 1: 同步到百度云BOS..."
BOS_RESULT=0
for dir in "${BACKUP_DIRS[@]}"; do
  if [ -d "$LH_ROOT/$dir" ]; then
    log "  同步: $dir"
    python3 "$LH_ROOT/bin/lh_baidu_bos.py" sync "$LH_ROOT/$dir" >> "$LOG_FILE" 2>&1 || {
      log "  ⚠️ $dir 同步失败(继续)"
      BOS_RESULT=1
    }
  fi
done

if [ $BOS_RESULT -eq 0 ]; then
  log "✅ 百度云BOS同步完成"
else
  log "⚠️ 百度云BOS部分失败"
fi

# ── 2. 鲲鹏同步 ──
log "📤 Phase 2: 同步到鲲鹏 (119.13.90.27)..."
KUNPENG_KEY="${KUNPENG_KEY:-$HOME/.ssh/longhun_kunpeng_ed25519}"
KUNPENG_TARGET="/opt/longhun/cloud_backup/$(date +%Y-%m-%d)"

if ssh -i "$KUNPENG_KEY" -o ConnectTimeout=5 root@119.13.90.27 "echo ok" 2>/dev/null; then
  ssh -i "$KUNPENG_KEY" root@119.13.90.27 "mkdir -p $KUNPENG_TARGET" 2>/dev/null
  for dir in "${BACKUP_DIRS[@]}"; do
    if [ -d "$LH_ROOT/$dir" ]; then
      log "  鲲鹏同步: $dir"
      rsync -az --delete -e "ssh -i $KUNPENG_KEY" "$LH_ROOT/$dir/" "root@119.13.90.27:$KUNPENG_TARGET/$dir/" 2>/dev/null || log "  ⚠️ 鲲鹏同步 $dir 失败"
    fi
  done
  # 写备份索引
  echo "$TIMESTAMP | $MODE | $(du -sh "$LH_ROOT" 2>/dev/null | cut -f1)" | \
    ssh -i "$KUNPENG_KEY" root@119.13.90.27 "cat >> /opt/longhun/cloud_backup/index.log"
  log "✅ 鲲鹏同步完成 → $KUNPENG_TARGET"
else
  log "⚠️ 鲲鹏不可达，跳过鲲鹏同步"
fi

# ── 3. 过期备份清理 ──
log "🧹 Phase 3: 清理过期备份..."
python3 "$LH_ROOT/bin/lh_baidu_bos.py" clean >> "$LOG_FILE" 2>&1 || true

# 鲲鹏清理：只保留最近7天
if ssh -i "$KUNPENG_KEY" -o ConnectTimeout=5 root@119.13.90.27 "echo ok" 2>/dev/null; then
  ssh -i "$KUNPENG_KEY" root@119.13.90.27 \
    "find /opt/longhun/cloud_backup/ -maxdepth 1 -type d -mtime +7 -exec rm -rf {} \; 2>/dev/null; echo ok" || true
fi

log "✅ 备份完成"
log "═══════════════════════════════════════"

# ── 健康上报 ──
if command -v python3 &>/dev/null && [ -f "$LH_ROOT/deploy/scripts/health_check.sh" ]; then
  bash "$LH_ROOT/deploy/scripts/health_check.sh" 2>/dev/null || true
fi

echo ""
echo "╔═══════════════════════════════════════╗"
echo "║  🐉 云备份完成                        ║"
echo "║  模式: $MODE                         ║"
echo "║  日志: logs/cloud_backup.log         ║"
echo "╚═══════════════════════════════════════╝"
