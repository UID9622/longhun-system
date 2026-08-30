#!/bin/bash
# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
##龍芯⚡️丙午·甲午·丙寅·甲午·䷕贲-TOOL-TEST_PERSONA_API-v1.0
# 君子協議: 本文件受龍魂DNA追溯保護

#!/bin/bash

# 龍魂人格 API 测试脚本
# DNA: #龍芯⚇️2026-06-09-PERSONA-API-TEST-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

set +e
# 注: 不启用 set -e —— ((PASS++))/((FAIL++)) 从 0 递增时退出码为 1 会中断整脚本(仅第1项可跑)

API_URL="http://localhost:9001"
PASS=0
FAIL=0

echo "╔════════════════════════════════════════════════════════════╗"
echo "║         龍魂人格 API 测试套件 / Persona API Tests          ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# 测试 1: 列表所有人格
echo "[1/5] 列出所有人格 (GET /personas/list)"
echo "─────────────────────────────────────────────────────────────"
if response=$(curl -s "$API_URL/personas/list"); then
    if echo "$response" | python3 -c "import sys, json; data = json.load(sys.stdin); personas = data.get('personas', []); print(f'✅ 成功: {len(personas)} 个人格'); [print(f'   • {p.get(\"code\")}: {p.get(\"name\")} ({p.get(\"layer\")})') for p in personas[:5]]" 2>/dev/null; then
        ((PASS++))
    else
        echo "❌ 失败: 无法解析响应"
        ((FAIL++))
    fi
else
    echo "❌ 失败: 连接错误"
    ((FAIL++))
fi
echo ""

# 测试 2: 查询单个人格 (P01)
echo "[2/5] 查询人格 P01 (GET /personas/P01)"
echo "─────────────────────────────────────────────────────────────"
if response=$(curl -s "$API_URL/personas/P01"); then
    if echo "$response" | python3 -c "import sys, json; data = json.load(sys.stdin); print(f'✅ 成功: {data.get(\"name\")} (角色: {data.get(\"role\")})')" 2>/dev/null; then
        ((PASS++))
    else
        echo "❌ 失败: 无法解析响应"
        ((FAIL++))
    fi
else
    echo "❌ 失败: 连接错误"
    ((FAIL++))
fi
echo ""

# 测试 3: 查询本地人格 (K04)
echo "[3/5] 查询本地人格 K04 (GET /personas/K04)"
echo "─────────────────────────────────────────────────────────────"
if response=$(curl -s "$API_URL/personas/K04"); then
    if echo "$response" | python3 -c "import sys, json; data = json.load(sys.stdin); print(f'✅ 成功: {data.get(\"name\")} (层级: {data.get(\"layer\")})')" 2>/dev/null; then
        ((PASS++))
    else
        echo "❌ 失败: 无法解析响应"
        ((FAIL++))
    fi
else
    echo "❌ 失败: 连接错误"
    ((FAIL++))
fi
echo ""

# 测试 4: 任务路由 (任务分配 - L1)
echo "[4/5] 任务路由测试 (POST /personas/route)"
echo "─────────────────────────────────────────────────────────────"
if response=$(curl -s -X POST "$API_URL/personas/route?task=strategy_planning&layer=L1"); then
    if echo "$response" | python3 -c "import sys, json; data = json.load(sys.stdin); assigned = data.get('assigned_personas', []); print(f'✅ 成功: 分配给 {len(assigned)} 个人格'); [print(f'   • {p}') for p in assigned[:3]]" 2>/dev/null; then
        ((PASS++))
    else
        echo "❌ 失败: 无法解析响应"
        ((FAIL++))
    fi
else
    echo "❌ 失败: 连接错误"
    ((FAIL++))
fi
echo ""

# 测试 5: 错误处理 (无效人格 ID)
echo "[5/5] 错误处理测试 (GET /personas/INVALID)"
echo "─────────────────────────────────────────────────────────────"
if response=$(curl -s -w "\n%{http_code}" "$API_URL/personas/INVALID"); then
    http_code=$(echo "$response" | tail -n1)
    if [ "$http_code" = "404" ]; then
        echo "✅ 成功: 正确返回 404"
        ((PASS++))
    else
        echo "❌ 失败: 期望 404，得到 $http_code"
        ((FAIL++))
    fi
else
    echo "❌ 失败: 连接错误"
    ((FAIL++))
fi
echo ""

echo "╔════════════════════════════════════════════════════════════╗"
echo "║                      测试结果汇总                           ║"
echo "╠════════════════════════════════════════════════════════════╣"
echo "║ ✅ 通过: $PASS/5"
echo "║ ❌ 失败: $FAIL/5"
if [ $FAIL -eq 0 ]; then
    echo "║ 🟢 状态: 所有测试通过"
    echo "╚════════════════════════════════════════════════════════════╝"
    exit 0
else
    echo "║ 🔴 状态: 有测试失败"
    echo "╚════════════════════════════════════════════════════════════╝"
    exit 1
fi
