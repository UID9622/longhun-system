#!/bin/bash
# ─────────────────────────────────────────────────────────────
# DNA: #龍芯⚡️2026-09-05-TOPO-FEEDBACK-AUTO-v1.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# 协议: CC BY-NC-SA 4.0（核心思想层）
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 任务: 每日 02:10 耻辱墙 topo-feedback 自动归档
#       → 拉取 GitHub issues(labels=topo-feedback) → 自动写入 topo_audit.jsonl
#         （append-only 链 + shame_wall.json 耻辱墙 topo-feedback 分类）
# 说明: 幂等去重（已归档不重复）· 重试 3 次 × 300s · 网络失败不阻断下次
# ─────────────────────────────────────────────────────────────
export PATH="/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/opt/homebrew/bin"
cd /Users/zuimeidedeyihan/longhun-system || exit 1
for i in 1 2 3; do
  /usr/bin/python3 08_BIN/lh_topo.py feedback 对外交付 \
    >> logs/topo_feedback_launchd.log 2>&1 && exit 0
  sleep 300
done
echo "[$(date '+%F %T')] topo feedback sync FAILED after 3 tries" \
  >> logs/topo_feedback_launchd.err.log
exit 1
