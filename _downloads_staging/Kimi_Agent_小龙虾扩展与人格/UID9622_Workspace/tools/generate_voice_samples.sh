#!/bin/bash
# 🐉 龙魂系统 · 女声样本批量生成
# 为几位推荐女声生成同一句测试音频，方便老大直接试听对比。
# 用法: tools/generate_voice_samples.sh
# DNA: #龍芯⚡️2026-06-27-LONGHUN-VOICE-SAMPLES-GEN-v1.0

WORKSPACE="/Users/zuimeidedeyihan/Downloads/Kimi_Agent_小龙虾扩展与人格/UID9622_Workspace"
PY="/usr/bin/python3"
[ -x "$PY" ] || PY="python3"

SAMPLE_TEXT="老大你好，我是龙魂系统助手宝宝。"
OUT_DIR="${WORKSPACE}/temp/voice/samples"
mkdir -p "$OUT_DIR"

# 推荐女声候选
SPEAKERS=("Daisy Studious" "Gracie Wise" "Claribel Dervla" "Tammie Ema" "Sofia Hellen")

ensure_server() {
  if curl -s --max-time 2 http://localhost:9624/health >/dev/null 2>&1; then
    return 0
  fi
  echo "请先启动龍魂语音合成服务：tools/baobao_speak.sh '测试'" >&2
  exit 1
}

generate_for_speaker() {
  local spk="$1"
  local safe
  safe=$(echo "$spk" | tr ' ' '_' | tr -cd '[:alnum:]_-')
  local out="${OUT_DIR}/sample_${safe}.wav"
  local payload
  payload=$("$PY" -c "import json,sys; print(json.dumps({'text': sys.argv[1], 'profile': 'assistant', 'speaker': sys.argv[2], 'output_path': sys.argv[3]}))" "$SAMPLE_TEXT" "$spk" "$out")
  local resp
  resp=$(curl -s --max-time 180 -X POST http://localhost:9624/speak \
    -H 'Content-Type: application/json' \
    -d "$payload" 2>/dev/null)
  local audio_file
  audio_file=$("$PY" -c "import json,sys; print(json.loads(sys.stdin.read()).get('audio_file',''))" <<< "$resp")
  if [ -n "$audio_file" ] && [ -f "$audio_file" ]; then
    echo "✅ $spk → $audio_file"
  else
    echo "❌ $spk 生成失败"
  fi
}

ensure_server

echo "🐉 正在为以下女声生成样本："
echo "DNA: #龍芯⚡️2026-06-27-LONGHUN-VOICE-SAMPLES-GEN-v1.0"
echo ""
for spk in "${SPEAKERS[@]}"; do
  generate_for_speaker "$spk"
done

echo ""
echo "样本位置: $OUT_DIR"
echo "试听方法: afplay ${OUT_DIR}/sample_Daisy_Studious.wav"
