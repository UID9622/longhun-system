#!/bin/bash
# ─────────────────────────────────────────────────────────────
# DNA: #龍芯⚡️2026-09-05-TOPO-DAILY-ARCHIVE-v1.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# 协议: CC BY-NC-SA 4.0（核心思想层）
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 任务: 每日 00:10 拓扑归档快照（lh topo archive 对外交付）
#       → ~/.longhun/topo_archive_YYYYMMDD.json + 站点 archive/ + 自动 GPG + 页面重建上线
# 说明: 重试 3 次 × 300s；archive 内含 export-page(变更可视化/声明刷新)+mkdocs build+rsync
# ─────────────────────────────────────────────────────────────
export PATH="/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/opt/homebrew/bin"
cd /Users/zuimeidedeyihan/longhun-system || exit 1
for i in 1 2 3; do
  /usr/bin/python3 08_BIN/lh_topo.py archive 对外交付 \
    >> logs/topo_archive_launchd.log 2>&1 && exit 0
  sleep 300
done
echo "[$(date '+%F %T')] topo archive FAILED after 3 tries" \
  >> logs/topo_archive_launchd.err.log
exit 1
