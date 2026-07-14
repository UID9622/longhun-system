"""人格路由示例 — 不同输入自动匹配不同人格

v2.1: 内联路由表，全部可运行。
"""

from longhun import PersonaRouter

inputs = [
    "检查一下系统有没有漏洞",
    "这段代码修一下，别报错了",
    "同步一下 Notion 和本地数据",
    "帮我部署到服务器上",
    "这个数字的五行属性是什么",
    "这个功能还值得留吗，还是该删了",
    "铁律和宪法不能改",
]

router = PersonaRouter()

for text in inputs:
    result = router.route(text)
    print(f"「{text}」")
    print(f"  → {result.persona} {result.persona_name}: {result.action} (置信: {result.confidence:.0%})")
    print(f"  DNA: {result.dna}")
    print()

# 指定人格
print("=" * 50)
result = router.route("任意内容", persona="P00")
print(f"指定人格: {result.persona} {result.persona_name}: {result.action}")
