#!/bin/bash
# 🐉 龙魂系统 · Siri 调用入口
# 由 Apple 快捷指令（Shortcuts）调用，把 Siri 识别到的文字交给宝宝中枢执行。
# DNA: #龍芯⚡️2026-06-27-LONGHUN-SYSTEM-SIRI-ENTRY-v1.0

WORKSPACE="/Users/zuimeidedeyihan/Downloads/Kimi_Agent_小龙虾扩展与人格/UID9622_Workspace"
INTENT="${1:-帮我查看系统状态}"
LOG="${WORKSPACE}/logs/siri_baobao.log"

# 中文语音反馈：优先本地 ChatTTS，未就绪回退 macOS say
SPEAK_SCRIPT="${WORKSPACE}/tools/baobao_speak.sh"
speak() {
  if [ -x "$SPEAK_SCRIPT" ]; then
    "$SPEAK_SCRIPT" "$1"
  elif command -v say >/dev/null 2>&1; then
    say -v "Yue (Premium)" "$1" 2>/dev/null || say -v "Tingting" "$1" 2>/dev/null || true
  fi
}

mkdir -p "$(dirname "$LOG")"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Siri 传入意图: ${INTENT}" >> "$LOG"

speak "龙魂系统收到，${INTENT}"

cd "$WORKSPACE" || exit 1
python3 backend_personas/builder/persona.py --intent "$INTENT" >> "$LOG" 2>&1
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
  speak "指令执行完成，请查看终端报告。"
else
  speak "执行遇到异常，请查看日志。"
fi

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 退出码: ${EXIT_CODE}" >> "$LOG"
exit $EXIT_CODE
