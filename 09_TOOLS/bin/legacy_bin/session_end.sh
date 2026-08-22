#!/usr/bin/env bash
# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# session_end.sh
# 龍魂终端宝宝会话结束钩子 stub
# 老大终端启动时反复报错: No such file or directory
# 本 stub 让 hook 不再噪音 · 实际想做留痕功能可以后续填

# 留痕到本机 (可选)
LOG_DIR="${LOG_DIR:-/Users/zuimeidedeyihan/longhun-system/logs}"
mkdir -p "$LOG_DIR" 2>/dev/null

TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)
echo "{\"ts\":\"$TS\",\"event\":\"session_end\",\"agent\":\"claude-code\"}" \
  >> "$LOG_DIR/session_end.jsonl" 2>/dev/null

# 必须 exit 0 · 否则 Claude Code 报 non-blocking status code
exit 0
