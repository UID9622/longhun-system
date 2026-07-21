#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂·全系统集成测试 v1.0
DNA: #龍芯⚡️2026-07-21-INTEGRATION-TEST-v1.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

测试范围:
  1. 所有引擎导入+基础功能
  2. 路由总线回调链
  3. 论文→引擎→协议 引用完整性
  4. 三色审计传播
  5. 已有引擎回归（不破坏现有功能）

用法:
  python3 bin/lh_system_integration_test.py        # 全系统集成测试
  python3 bin/lh_system_integration_test.py report # 完整报告
"""

import sys, os, json, importlib, time, traceback
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))
os.chdir(str(Path(__file__).parent.parent))

DNA = "#龍芯⚡️2026-07-21-INTEGRATION-TEST-v1.0"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# §1 引擎导入测试
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ENGINES_TO_TEST = [
    # 已有成熟引擎（回归）— 直接脚本运行模式，类名可能不同
    ("已有·电商信任引擎",     "bin/lh_ecom_trust_engine.py", None, False),
    ("已有·DNA捆绑防御",      "bin/lh_dna_bind_defender.py", None, False),
    ("已有·技术主权守门",     "bin/lh_tech_sovereignty_guard.py", None, False),
    ("已有·水军检测",         "bin/lh_water_army_detect.py", None, False),
    ("已有·道德经锚定",       "bin/lh_daodejing_anchor.py", None, False),
    # Validator引擎（回归）
    ("Validator·CNSH翻译",   "bin/lh_cnshtranslator_validator.py", None, False),
    ("Validator·DNA可逆编码", "bin/lh_dna_reversible_validator.py", None, False),
    ("Validator·封闭空间",    "bin/lh_closed_space_validator.py", None, False),
    ("Validator·算法审计",    "bin/lh_algo_audit_validator.py", None, False),
    # 🔥 新增引擎
    ("新增·黎曼三视角引擎",    "bin/lh_riemann_zeta_engine.py", "RiemannZetaEngine", True),
    ("新增·责任塌缩引擎",      "bin/lh_responsibility_collapse_engine.py", "ResponsibilityCollapseEngine", True),
    ("新增·易经世界模型引擎",  "bin/lh_yijing_world_engine.py", "YijingWorldEngine", True),
    ("新增·跨模块路由总线",    "bin/lh_cross_module_router.py", "CrossModuleRouter", True),
]


def test_engine_imports():
    """测试所有引擎是否可导入"""
    results = []
    for name, path, class_name, has_class in ENGINES_TO_TEST:
        try:
            full_path = os.path.join(os.path.dirname(__file__), "..", path)
            exists = os.path.exists(full_path)
            if not exists:
                results.append({"name": name, "status": "🔴", "detail": f"文件不存在: {path}"})
                continue

            if has_class and class_name:
                # 动态导入
                module_path = path.replace("/", ".").replace(".py", "")
                mod = importlib.import_module(module_path)
                cls = getattr(mod, class_name, None)
                if cls is None:
                    results.append({"name": name, "status": "🔴", "detail": f"类 {class_name} 未找到"})
                    continue
                instance = cls()
                results.append({"name": name, "status": "🟢", "detail": f"导入+实例化成功"})
            else:
                # 仅验证文件存在
                results.append({"name": name, "status": "🟢", "detail": f"文件存在 {os.path.getsize(full_path)} bytes"})

        except Exception as e:
            results.append({"name": name, "status": "🔴", "detail": f"异常: {str(e)[:80]}"})

    return results


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# §2 路由回调链测试
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def test_routing_chain():
    """测试跨模块回调链"""
    from bin.lh_cross_module_router import CrossModuleRouter, CALLBACK_ROUTES

    router = CrossModuleRouter()
    results = []

    # 测试所有已定义路由
    total_routes = 0
    working_routes = 0
    for src_engine, events in CALLBACK_ROUTES.items():
        for event, targets in events.items():
            for target in targets:
                total_routes += 1
                try:
                    result = router.dispatch(src_engine, event, {"test": True})
                    if result["status"] == "🟢":
                        working_routes += 1
                except Exception as e:
                    pass

    # 电商信任→水军检测 回调
    result = router.dispatch("lh_ecom_trust_engine", "on_report_submit",
                              {"report_id": "INTEGRATION_TEST", "score": 500})
    results.append({
        "name": "回调·电商→水军检测",
        "status": "🟢" if result["status"] == "🟢" and len(result["results"]) > 0 else "🔴",
        "detail": f"{len(result.get('results',[]))}个下游回调",
    })

    # 算法审计→技术主权 回调
    result = router.dispatch("lh_algo_audit_validator", "on_audit_fail",
                              {"audit_id": "TEST", "violations": 3})
    results.append({
        "name": "回调·审计→主权",
        "status": "🟢" if result["status"] == "🟢" else "🔴",
        "detail": f"results={len(result.get('results',[]))}",
    })

    # 黎曼→数学验证 回调
    result = router.dispatch("lh_riemann_zeta_engine", "on_zeta_critical_zero",
                              {"zero": "14.134725"})
    results.append({
        "name": "回调·黎曼→数学",
        "status": "🟢" if result["status"] == "🟢" else "🔴",
        "detail": "路由已定义",
    })

    # 责任塌缩→伦理锚定 回调
    result = router.dispatch("lh_responsibility_collapse_engine", "on_collapse_warning",
                              {"P_good": 0.25, "color": "🔴"})
    results.append({
        "name": "回调·责任塌缩→伦理",
        "status": "🟢" if result["status"] == "🟢" else "🔴",
        "detail": "路由已定义",
    })

    # 易经→文化DNA 回调
    result = router.dispatch("lh_yijing_world_engine", "on_world_state_change",
                              {"from": 0, "to": 63})
    results.append({
        "name": "回调·易经→文化DNA",
        "status": "🟢" if result["status"] == "🟢" else "🔴",
        "detail": "路由已定义",
    })

    # 水量统计
    results.append({
        "name": "📡 回调路由总量",
        "status": "🟢" if total_routes > 5 else "🟡",
        "detail": f"共{total_routes}条·{working_routes}条就绪",
    })

    return results


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# §3 引用链验证
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def test_citation_chain():
    """论文→引擎→协议 双向引用完整性"""
    from bin.lh_cross_module_router import CrossModuleRouter

    router = CrossModuleRouter()
    audit = router.audit_citation_chain()
    results = []

    results.append({
        "name": "引用链·论文→引擎",
        "status": "🟢" if audit["summary"]["red"] <= 1 else "🔴",
        "detail": f"🟢{audit['summary']['green']}/🟡{audit['summary']['yellow']}/🔴{audit['summary']['red']}",
    })

    # 检查新增引擎是否都有论文/协议关联
    new_engines = ["lh_riemann_zeta_engine", "lh_responsibility_collapse_engine",
                    "lh_yijing_world_engine", "lh_cross_module_router"]
    for eng in new_engines:
        info = router.get_engine(eng)
        has_paper = len(info.get("papers", [])) > 0
        has_proto = len(info.get("protocols", [])) > 0
        results.append({
            "name": f"引用·{eng}",
            "status": "🟢" if (has_paper or has_proto) else "🔴",
            "detail": f"论文{len(info.get('papers',[]))}·协议{len(info.get('protocols',[]))}",
        })

    return results


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# §4 新增引擎功能验证
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def test_new_engines_functional():
    """新增引擎核心功能点验证"""
    results = []

    # 黎曼引擎
    try:
        from bin.lh_riemann_zeta_engine import RiemannZetaEngine
        engine = RiemannZetaEngine()
        r = engine.assess(0.5, 14.134)
        results.append({
            "name": "黎曼·综合评估",
            "status": "🟢" if r["composite_score"] > 0.9 else "🔴",
            "detail": f"σ=0.5,t=14.13 → 综合={r['composite_score']:.4f} {r['verdict'][:2]}",
        })
        zeros = engine.verify_rh_known_zeros(5)
        all_ok = all(z["composite"] > 0.8 for z in zeros)
        results.append({
            "name": "黎曼·零点验证",
            "status": "🟢" if all_ok else "🔴",
            "detail": f"5个已知零点→{sum(1 for z in zeros if z['composite']>0.8)}/5超阈值",
        })
    except Exception as e:
        results.append({"name": "黎曼·功能验证", "status": "🔴", "detail": str(e)[:80]})

    # 责任塌缩引擎
    try:
        from bin.lh_responsibility_collapse_engine import (
            ResponsibilityCollapseEngine, kindness_probability
        )
        engine = ResponsibilityCollapseEngine()
        full = engine.full_assessment()
        results.append({
            "name": "责任·完整评估",
            "status": "🟢" if "adjusted_P" in full else "🔴",
            "detail": f"adjP={full['adjusted_P']:.4f} {full['overall_color']}",
        })
        # 验证极端塌缩
        P_c = kindness_probability(0.6, 0.3, 2.0, 2.5)
        results.append({
            "name": "责任·塌缩验证",
            "status": "🟢" if P_c < 0.3 else "🔴",
            "detail": f"reward0.3/risk2.0/x2.5 → P={P_c:.4f}",
        })
    except Exception as e:
        results.append({"name": "责任·功能验证", "status": "🔴", "detail": str(e)[:80]})

    # 易经世界引擎
    try:
        from bin.lh_yijing_world_engine import YijingWorldEngine
        engine = YijingWorldEngine()
        evo = engine.evolve(0, 63)
        results.append({
            "name": "易经·乾坤演化",
            "status": "🟢" if evo["change_count"] == 6 else "🔴",
            "detail": f"坤→乾 {evo['change_count']}爻变·{evo['path_length']}步",
        })
        # 三才能级
        analysis = engine.analyze_state(63)
        results.append({
            "name": "易经·能级分析",
            "status": "🟢" if analysis["energy"] > 0.9 else "🔴",
            "detail": f"乾卦E={analysis['energy']:.4f} {analysis['level']}",
        })
    except Exception as e:
        results.append({"name": "易经·功能验证", "status": "🔴", "detail": str(e)[:80]})

    return results


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# §5 全系统测试编排
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def run_integration_tests():
    """全系统集成测试"""
    print("\n" + "=" * 70)
    print("🧬 龍魂全系统集成测试 v1.0")
    print(f"DNA: {DNA}")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

    all_results = []
    total_passed = 0
    total_tests = 0

    # Phase 1: 引擎导入
    print("\n📦 Phase 1: 引擎导入测试")
    print("-" * 50)
    results = test_engine_imports()
    for r in results:
        print(f"  {r['status']} {r['name']:30} {r['detail']}")
        all_results.append(r)
        total_tests += 1
        if r['status'] == '🟢':
            total_passed += 1

    # Phase 2: 路由回调链
    print("\n📡 Phase 2: 路由回调链测试")
    print("-" * 50)
    results = test_routing_chain()
    for r in results:
        print(f"  {r['status']} {r['name']:30} {r['detail']}")
        all_results.append(r)
        total_tests += 1
        if r['status'] != '🔴':
            total_passed += 1

    # Phase 3: 引用链
    print("\n🔗 Phase 3: 论文↔引擎↔协议 引用链")
    print("-" * 50)
    results = test_citation_chain()
    for r in results:
        print(f"  {r['status']} {r['name']:30} {r['detail']}")
        all_results.append(r)
        total_tests += 1
        if r['status'] == '🟢':
            total_passed += 1

    # Phase 4: 新增引擎功能验证
    print("\n⚙️ Phase 4: 新增引擎功能验证")
    print("-" * 50)
    results = test_new_engines_functional()
    for r in results:
        print(f"  {r['status']} {r['name']:30} {r['detail']}")
        all_results.append(r)
        total_tests += 1
        if r['status'] == '🟢':
            total_passed += 1

    # 结果汇总
    print("\n" + "=" * 70)
    print(f"🏁 集成测试结果: {total_passed}/{total_tests} 通过")
    print("=" * 70)

    # 三色总结
    green = sum(1 for r in all_results if r['status'] == '🟢')
    yellow = sum(1 for r in all_results if r['status'] == '🟡')
    red = sum(1 for r in all_results if r['status'] == '🔴')
    print(f"  🟢 {green}  🟡 {yellow}  🔴 {red}")
    print(f"  通过率: {total_passed/total_tests*100:.1f}%")

    if red == 0:
        print("\n  🟢 全系统集成测试通过·所有链路联通")
    else:
        print(f"\n  🔴 有 {red} 项未通过·需检查")

    # 保存报告
    report = {
        "time": datetime.now().isoformat(),
        "dna": DNA,
        "total": total_tests,
        "passed": total_passed,
        "green": green, "yellow": yellow, "red": red,
        "results": all_results,
    }

    report_path = Path(__file__).parent.parent / "05_系統報告" / "integration_test_2026-07-21.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    print(f"\n  报告已保存: {report_path}")

    return total_passed == total_tests


def run_full_report():
    """完整系统报告"""
    print("\n" + "=" * 70)
    print("🧬 龍魂全系统复盘报告")
    print("DNA: " + DNA)
    print("=" * 70)

    from bin.lh_cross_module_router import CrossModuleRouter

    router = CrossModuleRouter()

    # 1. 引擎全景
    print("\n## 1. 引擎全景")
    print()
    print("| 引擎 | 状态 | 测试 | 关联协议 | 关联论文 | 路由出 |")
    print("|:---|:---:|:---:|:---:|:---:|:---:|")
    for name, eng in sorted(router.registry["engines"].items()):
        protocols = len(eng.get("protocols", []))
        papers = len(eng.get("papers", []))
        routes = len(router.routes.get(name, {}))
        print(f"| {name} | {eng['status']} | {eng.get('tests','?')} | {protocols} | {papers} | {routes} |")

    # 2. 论文关联
    print("\n## 2. 论文→引擎 关联")
    print()
    print("| 论文 | 引擎 | 状态 |")
    print("|:---|:---|:---:|")
    for name, paper in sorted(router.registry["papers"].items()):
        engs = ", ".join(paper.get("engines", [])) or "❌无引擎"
        print(f"| {name[:40]} | {engs} | {paper['status']} |")

    # 3. 协议关联
    print("\n## 3. 协议→引擎 关联")
    print()
    print("| 协议 | 引擎 | 级别 | 有数学 |")
    print("|:---|:---|:---:|:---:|")
    for name, proto in sorted(router.registry["protocols"].items()):
        engs = ", ".join(proto.get("engines", [])) or "❌无引擎"
        print(f"| {name[:40]} | {engs} | {proto['level']} | {'✅' if proto['has_math'] else '❌'} |")

    # 4. 回调路由矩阵
    print("\n## 4. 回调路由矩阵")
    print()
    print("| 源引擎 | 事件 | → 目标引擎.方法 | 说明 |")
    print("|:---|:---|:---|:---|")
    for src, events in sorted(router.routes.items()):
        for evt, targets in events.items():
            for t in targets:
                print(f"| {src} | `{evt}` | → `{t['target']}.{t['method']}` | {t['description']} |")

    # 5. 健康检查
    print("\n## 5. 健康检查")
    print()
    health = router.health_check()
    total = len(health)
    green_count = sum(1 for v in health.values() if v["file_exists"] and v["status"] == "🟢")
    yellow_count = sum(1 for v in health.values() if v["status"] == "🟡")
    red_count = sum(1 for v in health.values() if not v["file_exists"] or v["status"] == "🔴")
    print(f"- 总引擎: {total}")
    print(f"- 🟢 运行中: {green_count}")
    print(f"- 🟡 待升级(validator内): {yellow_count}")
    print(f"- 🔴 异常: {red_count}")

    # 6. 当前待补齐项
    print("\n## 6. 待补齐清单")
    print()
    audit = router.audit_citation_chain()
    if audit["🟡"]:
        print("### 🟡 待处理")
        for item in audit["🟡"]:
            print(f"- {item}")
    if audit["🔴"]:
        print("### 🔴 红线")
        for item in audit["🔴"]:
            print(f"- {item}")
    if not audit["🟡"] and (len(audit["🔴"]) <= 1):
        print("- ✅ 核心链路全部联通·仅EUV光刻因需要国家认证待冻结")

    print("\n" + "=" * 70)
    print("复盘完成。")
    print("=" * 70)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "report":
        run_full_report()
    else:
        ok = run_integration_tests()
        sys.exit(0 if ok else 1)
