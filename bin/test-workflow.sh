##龍芯⚡️2026-06-21-TOOL-TEST-WORKFLOW-v1.0
# 君子協議: 本文件受龍魂DNA追溯保護

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
