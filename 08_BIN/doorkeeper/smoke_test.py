# DNA: #龍芯⚡️丙午·壬辰·乙亥·壬午·䷚颐-SYNC-COMPLIANCE-20260827-7A2C9F3D
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
"""doorkeeper 冒烟测试（M77 对齐修正版验收）"""
import sys
import traceback
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

try:
    print("== 1. 模块导入 ==")
    from door_protocol import 五行, 八门, 三色, 判定门机, 获取五行
    from dna_tracer import DNATracer, dna
    from tricolor_audit import audit_engine
    from service_manager import ServiceManager, service_mgr
    print("✅ 全部模块导入成功")

    print("\n== 2. 门机判定逻辑 ==")
    assert 判定门机('running', False) == 八门.生门
    assert 判定门机('crashed', True) == 八门.死门
    assert 判定门机('', False, 是否攻击=True) == 八门.伤门
    assert 判定门机('', False, 是否入侵=True) == 八门.惊门
    assert 判定门机('sleeping', False) == 八门.休门
    assert 判定门机('stopped', True) == 八门.杜门
    print("✅ 门机判定 6/6")
    print("   死门五行(动态读取):", 获取五行(八门.死门).value)
    print("   惊门五行(动态读取):", 获取五行(八门.惊门).value)

    print("\n== 3. 真实服务端口检测 ==")
    alive = 0
    for name, svc in service_mgr.服务列表.items():
        ok = service_mgr.check_health(svc)
        if ok:
            alive += 1
        print(f"   {'✅' if ok else '❌'} {name} :{svc.端口} {svc.健康路径}")
    print(f"   存活 {alive}/{len(service_mgr.服务列表)}")

    print("\n== 4. 三色审计快速判定 ==")
    from tricolor_audit import 三色 as TC
    assert audit_engine.quick_audit("x", True, 0) == TC.绿
    assert audit_engine.quick_audit("x", True, 3) == TC.黄
    assert audit_engine.quick_audit("x", False, 0) == TC.红
    print("✅ 三色快速审计 3/3（绿/黄/红）")

    print("\n🎉 冒烟测试全绿")
except AssertionError as e:
    print("🔴 断言失败:", e)
    traceback.print_exc()
    sys.exit(1)
except Exception as e:
    print("🔴 异常:", e)
    traceback.print_exc()
    sys.exit(1)
