#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
龍魂系统·路由模块 (Router Module)

【核心功能】
- ExecutionRouter: 本地执行路由器 (任务调度+权限管理+DNA追踪)
- PersonaRouter: 人格路由系统 (虚伪词汇阻挡+加权人格决策)

【龍魂系统坐标】
DNA:#龍芯⚡️2026-06-03-ROUTER-MODULE-FILE1-v1.0
层级: L1·季节性路由

【责任声明】
UID9622·不免责·永久有效
献礼: 曾仕强老师 · Steve Jobs · Open Source · UID9622
"""

from .execution_router import (
    ExecutionRouter,
    TaskStatus,
    ExecutionContext,
    TaskDefinition,
    ExecutionRecord,
    ExecutionPriority
)

try:
    from ..people_skill_scope import (
        SkillScopeGuard,
        get_skill_scope_guard,
    )
except ImportError:
    try:
        import sys, os
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from people_skill_scope import (
            SkillScopeGuard,
            get_skill_scope_guard,
        )
    except ImportError:
        pass

from .persona_router import (
    PersonaRouter,
    PersonaRoutingDecision,
    VetoWordMatch,
    VetoWordCategory,
    PersonaId,
    DEFAULT_PERSONA_WEIGHTS,
    get_persona_router
)

__all__ = [
    # ExecutionRouter
    "ExecutionRouter",
    "TaskStatus",
    "ExecutionContext",
    "TaskDefinition",
    "ExecutionRecord",
    "ExecutionPriority",

    # SkillScopeGuard
    "SkillScopeGuard",
    "get_skill_scope_guard",

    # PersonaRouter
    "PersonaRouter",
    "PersonaRoutingDecision",
    "VetoWordMatch",
    "VetoWordCategory",
    "PersonaId",
    "DEFAULT_PERSONA_WEIGHTS",
    "get_persona_router",
]

# ═══════════════════════════════════════════════════════════════
# 【模块初始化检查】
# ═══════════════════════════════════════════════════════════════

def check_router_module():
    """
    检查路由模块的完整性

    Returns:
        (all_pass, errors)
    """
    errors = []

    try:
        persona_router = get_persona_router()
        ok, errs = persona_router.selftest()
        if not ok:
            errors.extend([f"PersonaRouter: {e}" for e in errs])
    except Exception as e:
        errors.append(f"PersonaRouter初始化失败: {str(e)}")

    return len(errors) == 0, errors


if __name__ == "__main__":
    print("🔍 路由模块完整性检查...\n")
    all_pass, errors = check_router_module()

    if all_pass:
        print("✅ 路由模块完整可用")
    else:
        print("❌ 路由模块检查失败:")
        for error in errors:
            print(f"  - {error}")
        exit(1)
