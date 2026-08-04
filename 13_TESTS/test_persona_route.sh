#!/usr/bin/env bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂人格路由 API 测试脚本
# DNA: #龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-TEST-PERSONA-ROUTE-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

set -e

API_HOST="${API_HOST:-127.0.0.1}"
API_PORT="${API_PORT:-8779}"
BASE="http://${API_HOST}:${API_PORT}"

echo "=== 龍魂人格路由 API 测试 ==="
echo "目标: $BASE"

# 启动 API（如果未运行）
if ! curl -s "$BASE/health" >/dev/null 2>&1; then
    echo "启动 API..."
    python3 bin/lh_persona_api.py --host "$API_HOST" --port "$API_PORT" >/tmp/persona_api_test.log 2>&1 &
    sleep 3
fi

echo "1. 健康检查"
curl -s "$BASE/health" | python3 -m json.tool

echo ""
echo "2. 人格列表"
curl -s "$BASE/persona/list" | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'总人格: {d[\"total\"]}, 在线: {d[\"online\"]}')"

echo ""
echo "3. 安全任务路由 → 应命中 P77"
curl -s -X POST "$BASE/persona/route" -H "Content-Type: application/json" -d '{"task":"检查这段代码有没有SQL注入漏洞"}' | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'主人格: {d[\"route\"][\"primary\"]}, 执行: {d[\"execution\"][\"executed_persona\"]}, 降级: {d[\"execution\"][\"fallback_used\"]}')"

echo ""
echo "4. 工程任务路由 → 应命中 P04"
curl -s -X POST "$BASE/persona/route" -H "Content-Type: application/json" -d '{"task":"帮我生成一个登录页面的HTML代码"}' | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'主人格: {d[\"route\"][\"primary\"]}, 执行: {d[\"execution\"][\"executed_persona\"]}, 降级: {d[\"execution\"][\"fallback_used\"]}')"

echo ""
echo "5. 直接执行 P01 战略人格"
curl -s -X POST "$BASE/persona/execute" -H "Content-Type: application/json" -d '{"persona_id":"P01","task":"分析当前项目最大的三个风险"}' | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'请求人格: {d[\"requested_persona\"]}, 执行: {d[\"execution\"][\"executed_persona\"]}, 成功: {d[\"execution\"][\"success\"]}')"

echo ""
echo "=== 全部测试完成 ==="
