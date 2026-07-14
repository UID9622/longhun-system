"""Hello 龍魂 — 最简单的调用示例

v2.1: 内联引擎已对接，全部可运行。
"""

from longhun import PersonaRouter, CNSHParser, DNA, Auditor


def main():
    # 1. 人格路由（内联路由表·可用）
    router = PersonaRouter()
    result = router.route("检查一下系统安全")
    print(f"人格: {result.persona} ({result.persona_name})")
    print(f"动作: {result.action}")
    print(f"置信: {result.confidence:.0%}")
    print(f"DNA: {result.dna}")

    # 2. 语义解析（内联语义域·可用）
    parser = CNSHParser()
    intent = parser.parse("帮我看下token还有多少")
    print(f"\n意图: {intent.domain} → {intent.action}")
    print(f"关键词: {intent.keywords}")
    print(f"置信: {intent.confidence:.0%}")

    # 3. DNA 追溯（可用）
    dna = DNA.generate(module="DEMO", action="HELLO")
    print(f"\nDNA: {dna}")
    print(f"验证: {'✅' if DNA.verify(dna) else '❌'}")

    # 4. 安全审计（内联引擎·可用）
    auditor = Auditor()
    report = auditor.scan("这是一段需要审计的内容")
    print(f"\n审计: {report.level} (score={report.score:.2f})")
    print(f"红色: {report.red_count} 黄色: {report.yellow_count}")
    print(f"DNA: {report.dna}")

    # 5. 测试红色警报词
    report2 = auditor.scan("技术无国界，应该灵活处理")
    print(f"\n红线测试: {report2.level} (score={report2.score:.2f})")
    if report2.fuse_appeal:
        print(f"熔断: {report2.fuse_appeal}")


if __name__ == "__main__":
    main()
