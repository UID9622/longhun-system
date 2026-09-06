#!/bin/bash
# ─────────────────────────────────────────────────────────────
# DNA: #龍芯⚡️2026-09-05-HEALTH-SNAPSHOT-DAILY-v1.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# 协议: CC BY-NC-SA 4.0（核心思想层）
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 任务: 每日 07:00 / 21:00 健康快照（lh health snapshot·静默·复用 topo-archive 模式）
#       → ~/.longhun/health_snapshots/YYYY-MM-DD/{07,21}.json
# 说明: 静默运行（--quiet 仅错误写日志）；快照引擎内部含健康判定(🟢🟡🔴)
# ─────────────────────────────────────────────────────────────
export PATH="/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/opt/homebrew/bin"
cd /Users/zuimeidedeyihan/longhun-system || exit 1
for i in 1 2 3; do
  /usr/bin/python3 08_BIN/lh_health_snapshot.py snapshot --quiet \
    >> logs/health_snapshot_launchd.log 2>&1 && break
  sleep 300
done
# v1.1 (2026-09-06): 快照后自动同步到 Notion 公开库(失败不阻塞·静默)
/usr/bin/python3 08_BIN/lh_health_sync.py sync --quiet \
  >> logs/health_snapshot_launchd.log 2>&1
# v1.2 (2026-09-06): 全模块公开化同步(耻辱墙/拓扑/管线/感知·失败不阻塞·零新增守护)
# v1.3 (2026-09-06): 先采集 model/deploy 源(ollama+launchd+鲲鹏)再同步 10 库全量
/usr/bin/python3 08_BIN/lh_notion_collect.py all --quiet \
  >> logs/health_snapshot_launchd.log 2>&1
/usr/bin/python3 08_BIN/lh_notion_sync.py sync --quiet \
  >> logs/health_snapshot_launchd.log 2>&1
exit 0
