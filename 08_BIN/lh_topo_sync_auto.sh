#!/bin/bash
# ============================================================
# 龍魂 · 通心译拓扑自动同步 wrapper（launchd com.longhun.topo-sync）
# 每日 4:00 执行 lh topo sync 通心译 · 失败重试 3 次 × 间隔 300s
# DNA: #龍芯⚡️丙午·丁酉·己卯·酉时·䷛大过-TOPO-SYNC-AUTO-v1.0
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# 协议: CC BY-NC-SA 4.0（核心思想层） · 工程实现: MulanPSL v2
# ============================================================
cd /Users/zuimeidedeyihan/longhun-system || exit 1
LOG_DIR="$HOME/.longhun/logs"
mkdir -p "$LOG_DIR"
LOG="$LOG_DIR/topo-sync.log"

echo "=== topo-sync $(date '+%Y-%m-%d %H:%M:%S') ===" >> "$LOG"
for i in 1 2 3; do
  # launchd 环境无代理变量；保险清代理防 socks5h 劫持
  env -u HTTP_PROXY -u HTTPS_PROXY -u ALL_PROXY -u http_proxy -u https_proxy -u all_proxy \
    /usr/bin/python3 bin/lh.py topo sync 通心译 >> "$LOG" 2>&1
  rc=$?
  if [ "$rc" -eq 0 ]; then
    echo "[OK] 通心译拓扑同步成功(第 ${i} 次尝试)" >> "$LOG"
    exit 0
  fi
  echo "[RETRY ${i}/3] 同步失败 rc=${rc} · 300s 后重试" >> "$LOG"
  [ "$i" -lt 3 ] && sleep 300
done
echo "[FAIL] 通心译拓扑同步连续 3 次失败，待下轮" >> "$LOG"
exit 1
