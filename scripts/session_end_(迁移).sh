#!/bin/bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
#
# DNA: #龍芯⚡️丙午·乙未·丙申·甲午·䷙大畜-迁移-session_end-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# 协议: CC BY-NC-SA 4.0
# 来源: 龍魂待整理/06-工具脚本/files/brain-pack/bin/session_end.sh
# 迁移日期: 2026-07-21
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 三色: 🟢 旧档案吸收·DNA嵌入
#

#!/usr/bin/env bash
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
