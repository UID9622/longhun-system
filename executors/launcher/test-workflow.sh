#!/bin/bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# DNA: #龍芯⚡️丙午·乙未·乙丑·萃-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
##龍芯⚡️2026-06-21-TOOL-TEST-WORKFLOW-v1.0
# 君子协议: 本文件受龍魂DNA追溯保护

#!/bin/bash
BASE="http://127.0.0.1:9622"
echo "🐉 测试5条工作流"
echo "=================="

for wf in brand-kit art-to-brand doc-publish comms-theme mcp-skill; do
  echo ""
  echo "▶ 工作流: $wf"
  curl -s -X POST "$BASE/api/workflows/$wf/run" \
    -H "Content-Type: application/json" \
    -d '{}' | python3 -m json.tool 2>/dev/null || echo "  ❌ 失败"
done

echo ""
echo "=================="
echo "测试完成"
