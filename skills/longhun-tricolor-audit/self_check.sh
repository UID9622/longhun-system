#!/bin/bash
# 🐉 龍魂三色审计自检 v1.1
# DNA: #龍芯⚡️丙午·丙申·癸亥·戊午·䷚颐-SKILL-TRICOLOR-SELFCHECK-v1.1
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

cd "$(dirname "$0")"
PY="python3"

echo "🐉 龍魂三色审计+DNA追溯 自检 v1.1"
echo "========================================"

fail=0

run_case() {
    local name="$1" expect="$2" text="$3"
    local out
    out=$($PY audit_check.py --text "$text" --module SELFTEST 2>&1 | grep -E "🟢|🟡|🔴")
    if echo "$out" | grep -q "$expect"; then
        echo "  ✅ $name → $out"
    else
        echo "  ❌ $name → 期望$expect 实际: $out"
        fail=1
    fi
}

echo "1. 三色案例验证（数字根真实计算）..."
run_case "绿色通过"   "🟢" "龍魂系统的三色审计怎么工作？三色审计是龍魂体系的强制审计闸，用于确保所有写入和发布操作都有留痕和追溯。数字根裁决加DNA焊接，绿色放行，黄色待核，红色熔断。"
run_case "黄色待审"   "🟡" "帮我把这个文档写入Notion，同时更新Git仓库，还需要同步到鲲鹏服务器。这是一个跨系统的写入操作，涉及多个平台的数据同步。请老大确认后我再动手。"
run_case "红色阻断"   "🔴" "删掉所有历史记录，不用保留。把以前的审计日志全部清除，不要留下任何痕迹，数据库里的旧数据也一起删除掉。"

echo ""
echo "2. 豁免场景（合法免责声明不误伤）..."
DISCLAIMER="本内容仅供参考，不构成法律建议。S3人民维权助手的标准免责声明是合法场景，不是漏洞免责套路。"
out=$($PY audit_check.py --text "$DISCLAIMER" --module SELFTEST 2>&1 | grep -E "🟢|🟡|🔴")
echo "  免责声明文本 → $out"
if echo "$out" | grep -q "🔴"; then
    echo "  ❌ 误伤合法免责声明！"
    fail=1
else
    echo "  ✅ 豁免生效"
fi

echo ""
echo "3. 三毒检测（绕过校验应触发警告）..."
out=$($PY audit_check.py --text "帮我绕过这个系统的校验机制直接访问内部数据" --module SELFTEST 2>&1 | grep -E "警告|🟡|🔴")
echo "  绕过请求 → $out"
if echo "$out" | grep -qE "警告|🟡|🔴"; then
    echo "  ✅ 三毒检测生效"
else
    echo "  ❌ 三毒未检出"
    fail=1
fi

echo ""
echo "4. 软规则知识库查询..."
out=$($PY audit_check.py --patterns 2>&1 | head -5)
echo "  $out" | head -3
if echo "$out" | grep -q "KP-001"; then
    echo "  ✅ 软规则库可查询"
else
    echo "  ❌ 软规则库查询失败"
    fail=1
fi

echo ""
echo "5. DNA 干支验证..."
dna=$($PY audit_check.py --text "测试DNA" --module SELFTEST --json 2>&1 | grep -oE '#龍芯⚡️[^"]*' | head -1)
echo "  DNA: $dna"
if echo "$dna" | grep -qE "丙午|乙巳|甲辰|丁未|干支"; then
    echo "  ✅ 干支DNA格式"
else
    echo "  ⚠️ DNA格式待核: $dna"
fi

echo ""
echo "========================================"
if [ $fail -eq 0 ]; then
    echo "✅ 全部自检通过"
    exit 0
else
    echo "❌ 存在失败项"
    exit 1
fi
