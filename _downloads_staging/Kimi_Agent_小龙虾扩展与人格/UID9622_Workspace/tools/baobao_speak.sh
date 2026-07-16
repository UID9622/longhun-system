#!/bin/bash
# 🐉 龙魂系统 · 宝宝语音播报入口
# 默认使用女声助手音色（assistant）；内容播报可用 --profile uid9622 切回 UID9622 本音。
# 用法:
#   tools/baobao_speak.sh "请老大吩咐"
#   tools/baobao_speak.sh --profile uid9622 "这里是 UID9622 的解说稿"
# DNA: #龍芯⚡️2026-06-27-LONGHUN-SPEAK-ENTRY-v2.1

WORKSPACE="/Users/zuimeidedeyihan/Downloads/Kimi_Agent_小龙虾扩展与人格/UID9622_Workspace"
VOICE_TWIN="/Users/zuimeidedeyihan/longhun-system/voice-twin"
PROFILE="assistant"

# 解析参数
while [[ "$1" == --* ]]; do
  case "$1" in
    --profile)
      PROFILE="$2"
      shift 2
      ;;
    --profile=*)
      PROFILE="${1#*=}"
      shift
      ;;
    *)
      shift
      ;;
  esac
done

TEXT="${1:-龙魂系统已就绪，请老大吩咐。}"
TS=$(date '+%Y%m%d_%H%M%S')
OUTPUT="${WORKSPACE}/temp/voice/baobao_tts_${PROFILE}_${TS}.wav"

mkdir -p "$(dirname "$OUTPUT")"

VENV_PY="${VOICE_TWIN}/.venv-tts/bin/python"
SERVER_PY="${WORKSPACE}/backend_personas/baobao/audio_engine/xtts_server.py"
PY="/usr/bin/python3"
[ -x "$PY" ] || PY="python3"

ensure_tts_server() {
  if curl -s --max-time 2 http://localhost:9624/health >/dev/null 2>&1; then
    return 0
  fi
  if [ -x "$VENV_PY" ] && [ -f "$SERVER_PY" ]; then
    echo "🐉 启动龍魂语音合成服务（profile=${PROFILE}）..." >&2
    nohup "$VENV_PY" "$SERVER_PY" >> "${WORKSPACE}/logs/xtts_server.log" 2>&1 &
    for i in $(seq 1 60); do
      sleep 1
      if curl -s --max-time 2 http://localhost:9624/health >/dev/null 2>&1; then
        return 0
      fi
    done
  fi
  return 1
}

speak_xtts() {
  local payload
  payload=$("$PY" -c "import json,sys; print(json.dumps({'text': sys.argv[1], 'profile': sys.argv[2], 'output_path': sys.argv[3]}))" "$1" "$2" "$3")
  local resp
  resp=$(curl -s --max-time 180 -X POST http://localhost:9624/speak \
    -H 'Content-Type: application/json' \
    -d "$payload" 2>/dev/null)
  local audio_file
  audio_file=$("$PY" -c "import json,sys; print(json.loads(sys.stdin.read()).get('audio_file',''))" <<< "$resp")
  if [ -n "$audio_file" ] && [ -f "$audio_file" ]; then
    if command -v afplay >/dev/null 2>&1; then
      afplay "$audio_file"
    fi
    # 额外复制到工作空间留痕
    cp "$audio_file" "$OUTPUT" 2>/dev/null || true
    return 0
  fi
  return 1
}

speak_fallback() {
  if command -v say >/dev/null 2>&1; then
    say -v "Tingting" "$1" 2>/dev/null || say -v "Yue (Premium)" "$1" 2>/dev/null || say "$1" 2>/dev/null || true
  fi
}

# 主逻辑
if ensure_tts_server && speak_xtts "$TEXT" "$PROFILE" "$OUTPUT"; then
  echo "DNA: #龍芯⚡️2026-06-27-LONGHUN-SPEAK-ENTRY-v2.1"
  exit 0
fi

# 完全失败时回退
speak_fallback "$TEXT"
echo "DNA: #龍芯⚡️2026-06-27-LONGHUN-SPEAK-ENTRY-v2.1-FALLBACK"
exit 0
