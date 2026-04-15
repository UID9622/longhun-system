#!/bin/bash
# 龍魂自動歸檔 · 每次對話結束執行
SESSION_DIR="$HOME/longhun-system/sessions"
mkdir -p "$SESSION_DIR"
SESSION_FILE="$SESSION_DIR/session_$(date +%Y%m%d_%H%M%S).md"
{
  echo "# 🐉 龍魂會話歸檔 · $(date '+%Y-%m-%d %H:%M:%S')"
  echo ""
  echo "$1"
  echo ""
  echo "---"
  echo "DNA: #龍芯⚡️$(date +%Y%m%d)-session-$(date +%H%M%S)"
} > "$SESSION_FILE"
echo "$SESSION_FILE"
