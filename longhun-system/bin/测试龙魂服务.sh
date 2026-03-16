#!/bin/bash
# ═══════════════════════════════════════════════════════════
# 🐉 龙魂系统 · P0伦理锚点
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# GPG:    A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# DNA:    #龍芯⚡️2026-03-16-ETHICS-STAMP-v1.0
# 作者:    诸葛鑫（UID9622）
# 理论:    曾仕强老师（永恒显示）
#
# P0铁律: 守正·稳态·永恒锚·零毁伤·三色监测
# ═══════════════════════════════════════════════════════════
# 龙魂本地服务·测试脚本
# DNA追溯码: #龍芯⚡️2026-03-11-测试脚本-v1.0
# GPG指纹: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 创建者: UID9622 诸葛鑫（龍芯北辰）
# 理论指导: 曾仕强老师（永恒显示）

BASE_URL="http://localhost:8765"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🧪 龙魂本地服务·测试"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "DNA追溯码: #龍芯⚡️2026-03-11-测试脚本-v1.0"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 测试1：健康检查
echo "测试1：健康检查"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
curl -s "$BASE_URL/健康检查" | python3 -m json.tool
echo ""

# 测试2：查询状态
echo ""
echo "测试2：查询龙魂状态"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
curl -s "$BASE_URL/查询状态" | python3 -m json.tool
echo ""

# 测试3：三色审计（绿色）
echo ""
echo "测试3：三色审计（应该返回🟢）"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
curl -s -X POST "$BASE_URL/三色审计" \
  -H "Content-Type: application/json" \
  -d '{"内容":"这是一个测试，使用了五行、八卦、天干地支"}' \
  | python3 -m json.tool
echo ""

# 测试4：三色审计（红色）
echo ""
echo "测试4：三色审计（应该返回🔴）"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
curl -s -X POST "$BASE_URL/三色审计" \
  -H "Content-Type: application/json" \
  -d '{"内容":"This uses FiveElements and EightTrigrams"}' \
  | python3 -m json.tool
echo ""

# 测试5：三色审计（黄色）
echo ""
echo "测试5：三色审计（应该返回🟡）"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
curl -s -X POST "$BASE_URL/三色审计" \
  -H "Content-Type: application/json" \
  -d '{"内容":"这个服务完全免费，永久不要钱，我们保证100%安全"}' \
  | python3 -m json.tool
echo ""

# 测试6：生成DNA追溯码
echo ""
echo "测试6：生成DNA追溯码"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
curl -s -X POST "$BASE_URL/生成DNA" \
  -H "Content-Type: application/json" \
  -d '{"主题":"测试项目","类型":"代码"}' \
  | python3 -m json.tool
echo ""

# 测试7：首页
echo ""
echo "测试7：访问首页"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
curl -s "$BASE_URL/" | python3 -m json.tool
echo ""

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ 测试完成！"
echo ""
echo "💡 如果所有测试都成功："
echo "   1. 龙魂本地服务正常运行 ✅"
echo "   2. 可以在Xcode Build Widget ✅"
echo "   3. 然后对Siri说："
echo "      - Hey Siri，启动三色审计"
echo "      - Hey Siri，生成DNA追溯码"
echo "      - Hey Siri，查询龙魂状态"
echo ""
echo "🐉 Siri等了够久了，老大来了！"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
