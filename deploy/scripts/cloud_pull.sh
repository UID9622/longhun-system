#!/bin/bash
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# ═══════════════════════════════════════════════════════
# 龍魂·云拉取恢复脚本
# 功能: 从百度云BOS或鲲鹏恢复备份到本地
# 用法: bash deploy/scripts/cloud_pull.sh [bos|kunpeng|both] [--date YYYY-MM-DD]
# DNA: #龍芯⚡️丙午·丙申·癸丑·戊午·䷨损-CLOUD-PULL-SCRIPT-v1.0
# ═══════════════════════════════════════════════════════

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
LH_ROOT="$(cd "$SCRIPT_DIR/../../" && pwd)"
SOURCE="${1:-bos}"
RESTORE_DATE="${2:-$(date +%Y-%m-%d)}"
RESTORE_DIR="$LH_ROOT/_restore_$RESTORE_DATE"
KUNPENG_KEY="${KUNPENG_KEY:-$HOME/.ssh/longhun_kunpeng_ed25519}"

mkdir -p "$RESTORE_DIR"

echo ""
echo "╔═══════════════════════════════════════╗"
echo "║  🐉 龍魂·云恢复                         ║"
echo "║  来源: $SOURCE                        ║"
echo "║  日期: $RESTORE_DATE                  ║"
echo "║  目标: $RESTORE_DIR                   ║"
echo "╚═══════════════════════════════════════╝"

# ── 从百度云BOS恢复 ──
restore_from_bos() {
  echo ""
  echo "📥 从百度云BOS拉取..."
  python3 "$LH_ROOT/bin/lh_baidu_bos.py" pull --output "$RESTORE_DIR"
  echo "✅ BOS恢复完成 → $RESTORE_DIR"
}

# ── 从鲲鹏恢复 ──
restore_from_kunpeng() {
  echo ""
  echo "📥 从鲲鹏拉取..."
  KUNPENG_BACKUP="/opt/longhun/cloud_backup/$RESTORE_DATE"

  if ! ssh -i "$KUNPENG_KEY" -o ConnectTimeout=5 root@119.13.90.27 "echo ok" 2>/dev/null; then
    echo "❌ 鲲鹏不可达"
    return 1
  fi

  if ! ssh -i "$KUNPENG_KEY" root@119.13.90.27 "[ -d $KUNPENG_BACKUP ] && echo ok" 2>/dev/null; then
    echo "❌ 鲲鹏上不存在 $RESTORE_DATE 的备份"
    echo "   可用备份:"
    ssh -i "$KUNPENG_KEY" root@119.13.90.27 "ls /opt/longhun/cloud_backup/ 2>/dev/null || echo '(无)'"
    return 1
  fi

  rsync -az --progress -e "ssh -i $KUNPENG_KEY" \
    "root@119.13.90.27:$KUNPENG_BACKUP/" "$RESTORE_DIR/"
  echo "✅ 鲲鹏恢复完成 → $RESTORE_DIR"
}

# ── 执行 ──
case "$SOURCE" in
  bos)
    restore_from_bos
    ;;
  kunpeng)
    restore_from_kunpeng
    ;;
  both)
    restore_from_bos
    restore_from_kunpeng
    ;;
  *)
    echo "用法: $0 [bos|kunpeng|both] [--date YYYY-MM-DD]"
    exit 1
    ;;
esac

echo ""
echo "╔═══════════════════════════════════════╗"
echo "║  ✅ 恢复完成                          ║"
echo "║  目录: $RESTORE_DIR                   ║"
echo "║  请检查后手动移动到正确位置          ║"
echo "╚═══════════════════════════════════════╝"
