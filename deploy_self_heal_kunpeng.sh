#!/usr/bin/env bash
# 🐉 龍魂 · 自修复引擎鲲鹏部署脚本
# DNA: #龍芯⚡️丙午·丙申·庚申·亥时-SELF-HEAL-KUNPENG-UID9622

set -euo pipefail

KUNPENG_USER="root"
KUNPENG_HOST="119.13.90.27"
KUNPENG_DIR="/opt/longhun-system"
LOCAL_DIR="$HOME/longhun-system"

echo "🐉 部署自修复引擎到鲲鹏 ($KUNPENG_HOST)..."

# 1. 确保鲲鹏目录存在
ssh "$KUNPENG_USER@$KUNPENG_HOST" "mkdir -p $KUNPENG_DIR/bin $KUNPENG_DIR/04_AUDIT $KUNPENG_DIR/08_STATE"

# 2. 同步自修复脚本
scp "$LOCAL_DIR/bin/lh_self_heal.py" "$KUNPENG_USER@$KUNPENG_HOST:$KUNPENG_DIR/bin/lh_self_heal.py"
scp "$LOCAL_DIR/pyrightconfig.json" "$KUNPENG_USER@$KUNPENG_HOST:$KUNPENG_DIR/pyrightconfig.json"

# 3. 设置可执行权限
ssh "$KUNPENG_USER@$KUNPENG_HOST" "chmod +x $KUNPENG_DIR/bin/lh_self_heal.py"

# 4. 添加定时任务（每 6 小时运行一次）
CRON_LINE="0 */6 * * * cd $KUNPENG_DIR && python3 $KUNPENG_DIR/bin/lh_self_heal.py 1 >> $KUNPENG_DIR/logs/self_heal.log 2>&1"
ssh "$KUNPENG_USER@$KUNPENG_HOST" "
  (crontab -l 2>/dev/null | grep -v 'lh_self_heal.py' || true)
  echo '$CRON_LINE'
" | ssh "$KUNPENG_USER@$KUNPENG_HOST" "crontab -"

# 5. 立即执行一次验证
ssh "$KUNPENG_USER@$KUNPENG_HOST" "cd $KUNPENG_DIR && python3 $KUNPENG_DIR/bin/lh_self_heal.py 1"

echo "✅ 自修复引擎已部署到鲲鹏，每 6 小时自动巡检修复"
echo "   日志: $KUNPENG_DIR/logs/self_heal.log"
echo "   审计: $KUNPENG_DIR/04_AUDIT/self_heal.jsonl"
