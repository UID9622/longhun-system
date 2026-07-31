# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂人民技能边界联动测试

DNA:#龍芯⚡️2026-06-21-SKILL-SCOPE-INTEGRATION-TEST-v1.0
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from people_skill_scope import get_skill_scope_guard
from router.execution_router import (
    ExecutionRouter,
    TaskDefinition,
    ExecutionContext,
    ExecutionPriority,
)


def main():
    print("╔═══════════════════════════════════════════════════╗")
    print("║  龍魂人民技能边界联动测试                         ║")
    print("║  赋能不是取代 · 专精一项 · 越界审计               ║")
    print("╚═══════════════════════════════════════════════════╝")

    guard = get_skill_scope_guard()
    print(f"\n技能领域数: {guard.stats()['domains']}")

    # 1. 农民用农业生产 — 应该允许
    verdict = guard.personalized_verdict(
        uid="USER-FARMER-001",
        domain_name="农业生产",
        stated_intent="看天气、记农事",
        profession="农民",
    )
    print(f"\n农民用农业生产: {verdict['result']}")
    print(f"  说明: {verdict['reason']}")
    assert verdict["result"] == "🟢 允许", "农民农业生产应该被允许"

    # 2. 普通人用医疗建议 — 应该拒绝
    verdict = guard.personalized_verdict(
        uid="USER-NORMAL-001",
        domain_name="医疗建议",
        stated_intent="帮我诊断病情",
        profession="自由职业",
    )
    print(f"\n普通人用医疗建议: {verdict['result']}")
    print(f"  说明: {verdict['reason']}")
    assert verdict["result"] == "🔴 拒绝", "普通人医疗建议应该被拒绝"

    # 3. 程序员取代意图 — 应该需确认
    verdict = guard.personalized_verdict(
        uid="USER-DEV-001",
        domain_name="编程",
        stated_intent="我要写一个全自动工具，把团队里其他人的活都取代",
        profession="程序员",
    )
    print(f"\n程序员取代意图: {verdict['result']}")
    print(f"  说明: {verdict['reason']}")
    assert verdict["result"] == "🟡 需确认", "取代意图应该需要确认"

    # 4. ExecutionRouter 技能边界审查
    print("\n【ExecutionRouter 联动】")
    router = ExecutionRouter(
        manifest_path=os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "manifest.json"
        )
    )
    # 不依赖 manifest 也能测试 authorize_task
    router.system_ready = True

    ctx = ExecutionContext(
        executor_uid="USER-DEV-001",
        current_si=0.9,
        current_f1f7_confidence=0.9,
        timestamp="2026-06-21T00:00:00",
        shichen="子时",
        digital_root=1,
        persona_routing={},
    )

    # 越界任务
    bad_task = TaskDefinition(
        task_id="T1",
        task_name="越界医疗诊断",
        module_name="medical",
        function_name="diagnose",
        parameters={},
        required_si=0.3,
        required_f1f7=0.5,
        description="普通人请求医疗诊断",
        skill_domain="医疗建议",
        stated_intent="帮我诊断病情",
        profession="自由职业",
    )
    ok, priority, reason = router.authorize_task(bad_task, ctx)
    print(f"越界任务授权: {ok} | {priority.value} | {reason}")
    assert not ok, "越界任务应该被拒绝"

    # 取代意图任务
    replace_task = TaskDefinition(
        task_id="T2",
        task_name="取代同事工具",
        module_name="dev",
        function_name="auto_tool",
        parameters={},
        required_si=0.3,
        required_f1f7=0.5,
        description="自动取代团队工作",
        skill_domain="编程",
        stated_intent="我要写一个全自动工具，把团队里其他人的活都取代",
        profession="程序员",
    )
    ok, priority, reason = router.authorize_task(replace_task, ctx)
    print(f"取代意图任务授权: {ok} | {priority.value} | {reason}")
    assert not ok, "取代意图任务应该被拒绝"

    # 正常赋能任务
    good_task = TaskDefinition(
        task_id="T3",
        task_name="提高工作效率",
        module_name="dev",
        function_name="helper_tool",
        parameters={},
        required_si=0.3,
        required_f1f7=0.5,
        description="帮自己写个小工具",
        skill_domain="编程",
        stated_intent="帮我写一个小工具提高我的工作效率",
        profession="程序员",
    )
    ok, priority, reason = router.authorize_task(good_task, ctx)
    print(f"赋能任务授权: {ok} | {priority.value} | {reason}")
    assert ok, "正常赋能任务应该被允许"

    print("\n✅ 技能边界联动测试全部通过")


if __name__ == "__main__":
    main()
