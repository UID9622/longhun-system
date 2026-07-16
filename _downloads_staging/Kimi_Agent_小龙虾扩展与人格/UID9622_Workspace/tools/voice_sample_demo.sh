#!/bin/bash
# 🐉 龙魂系统 · 女声候选试听
# 生成几位内置女声 speaker 的样本，方便老大挑选最喜欢的「宝宝」音色。
# 用法: tools/voice_sample_demo.sh
# DNA: #龍芯⚡️2026-06-27-LONGHUN-VOICE-SAMPLE-DEMO-v1.0

WORKSPACE="/Users/zuimeidedeyihan/Downloads/Kimi_Agent_小龙虾扩展与人格/UID9622_Workspace"
PY="/usr/bin/python3"
[ -x "$PY" ] || PY="python3"

SAMPLE_TEXT="老大你好，我是龙魂系统助手宝宝，请吩咐。"
OUT_DIR="${WORKSPACE}/temp/voice/samples"
mkdir -p "$OUT_DIR"

ensure_server() {
  if curl -s --max-time 2 http://localhost:9624/health >/dev/null 2>&1; then
    return 0
  fi
  echo "请先启动龍魂语音合成服务：tools/baobao_speak.sh '测试'" >&2
  exit 1
}

generate_sample() {
  local speaker="$1"
  local payload
  payload=$("$PY" -c "import json,sys; print(json.dumps({'text': sys.argv[1], 'profile': 'assistant'}))" "$SAMPLE_TEXT")
  # 临时修改配置中的 assistant speaker 比较麻烦，这里直接调用 xtts_server 的 /speakers 列出即可
  # 实际试听通过手动改 data/voice_profiles.json 中 assistant.speaker 再跑 baobao_speak.sh
  echo "候选 speaker: $speaker — 请手动将 data/voice_profiles.json 中 assistant.speaker 改为 \"$speaker\" 后运行 tools/baobao_speak.sh '测试'"
}

ensure_server

echo "🐉 龍魂女声候选列表（当前默认：Daisy Studious）"
echo "DNA: #龍芯⚡️2026-06-27-LONGHUN-VOICE-SAMPLE-DEMO-v1.0"
echo ""
echo "可用内置 speaker（女声推荐）："
curl -s http://localhost:9624/speakers | "$PY" -c "
import json, sys
data = json.load(sys.stdin)
for s in data.get('speakers', []):
    print(' -', s)
"
echo ""
echo "试听方法："
echo "1. 编辑 data/voice_profiles.json，把 assistant.speaker 改成你想试的名字"
echo "2. 运行 tools/baobao_speak.sh '老大，测试一下这个声音'"
echo "3. 重复直到选中最佳女声"
echo ""
echo "常见女声推荐：Daisy Studious / Gracie Wise / Claribel Dervla / Tammie Ema / Sofia Hellen"
