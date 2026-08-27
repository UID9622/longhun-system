#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""
🐉 龍魂低算力内核 · lh CLI v1.0.0
纯标准库·零依赖·断网可跑

用法: lh <command> [args...]

命令:
  lh version              版本信息
  lh dna [文本]           签发干支DNA（不传文本打印时间戳）
  lh audit --json '{...}' 三色审计
  lh root <数字>          计算数字根
  lh root --wuxing <n>    数字五行属性
  lh root --shengke <a> <b> 五行生克关系
  lh chain write '{...}'  写入年轮链
  lh chain verify         验证年轮链完整性
  lh chain stats          年轮链统计
  lh flow stats           流控统计
  lh flow tricolor        流控三色审计
  lh bench                跑自检基准测试
  lh info                 系统信息摘要

DNA: #龍芯⚡️丙午·丙申·丁巳·丙午·䷟恒-LH-CLI-UID9622
License: MulanPSL v2
"""

import sys
import json
import os

# 添加父目录到路径（开发模式）
_parent = os.path.dirname(os.path.abspath(__file__))
if _parent not in sys.path:
    sys.path.insert(0, _parent)

try:
    from longhun_core import (
        __version__, __dna__,
        DNAEngine, generate_dna,
        TricolorAudit, audit_report,
        YearRingChain, write_record, verify_chain,
        DigitalRoot, compute_root,
        FlowController, create_rate_limiter,
    )
except ImportError:
    # 打包后路径
    from core.longhun_core import (
        __version__, __dna__,
        DNAEngine, generate_dna,
        TricolorAudit, audit_report,
        YearRingChain, write_record, verify_chain,
        DigitalRoot, compute_root,
        FlowController, create_rate_limiter,
    )


VERSION = f"🐉 longhun-core v{__version__}"
DIVIDER = "═" * 50


def cmd_version(args=None):
    print(DIVIDER)
    print(f"🐉 龍魂低算力内核 v{__version__}")
    print("治大国若烹小鲜。——《道德经》第60章")
    print(DIVIDER)
    print(f"DNA:    {__dna__}")
    print(f"五模块: dna_trace | tricolor_audit | historian | digital_root | flow_control")
    print(f"零依赖: 纯 Python 标准库")
    print(f"许可证: 工程层 MulanPSL v2 · 思想层 CC BY-NC-SA 4.0")
    print(DIVIDER)


def cmd_dna(args):
    engine = DNAEngine()
    if args:
        text = " ".join(args)
        dna = engine.stamp(module="CLI", action="DNA", extra=text[:20])
        print(f"🐉 DNA: {dna['dna']}")
        print(f"   紧凑: {dna['compact']}")
        print(f"   卦: {dna['gua']} | 生肖: {dna['sheng_xiao']} | 黄帝{dna['huangdi_year']}年")
        print(f"   干支: {dna['ganzhi']['year']}年 {dna['ganzhi']['month']}月 {dna['ganzhi']['day']}日 {dna['ganzhi']['hour']}时")
        print(f"   哈希: {dna['hash']}")
    else:
        info = engine.time_info()
        print(f"🐉 {info['year_gan']}{info['year_zhi']}·{info['month_gan']}{info['month_zhi']}·{info['day_gan']}{info['day_zhi']}·{info['hour_zhi']}时·{info['gua_name']}")
        print(f"   黄帝{info['huangdi_year']}年 | 生肖{info['sheng_xiao']}")
        print(f"   {info['timestamp_iso']}")


def cmd_audit(args):
    auditor = TricolorAudit()
    if not args:
        # 演示
        result = auditor.audit({"阻塞率": 0.02, "耗时_ms": 120, "错误率": 0.005,
                                "required_fields": ["id"], "present_fields": ["id","ts"],
                                "可解释度": 0.9})
    else:
        # 跳过 --json 前缀
        filtered = [a for a in args if a != "--json"]
        data_str = " ".join(filtered)
        # 尝试解析 JSON
        try:
            if "=" in data_str and "{" not in data_str:
                # kv 格式: key=val key2=val2
                data = {}
                for pair in data_str.split():
                    if "=" in pair:
                        k, v = pair.split("=", 1)
                        try:
                            data[k] = float(v)
                        except ValueError:
                            data[k] = v
            else:
                data = json.loads(data_str)
        except json.JSONDecodeError:
            print(f"🔴 JSON 解析失败: {data_str}")
            sys.exit(1)
        result = auditor.audit(data)

    print(DIVIDER)
    print(f"🔍 三色审计报告")
    print(DIVIDER)
    print(f"判定:  {result.tricolor} {result.status}")
    print(f"R值:   {result.r_value}/100")
    print(f"DNA:   {result.dna}")
    print(f"时间:  {result.timestamp}")
    print(DIVIDER)
    print(f"检查项:")
    for c in result.checks:
        mark = "✅" if c["passed"] else "❌"
        print(f"  {mark} {c['name']}: {c['detail']}")
    print(DIVIDER)
    print(f"汇总: {result.summary['passed']}/{result.summary['total_checks']} 通过")


def cmd_root(args):
    engine = DigitalRoot()
    if not args:
        # 不动点展示
        fp = engine.verify_fixed_point()
        print(DIVIDER)
        print("🐉 369 洛书不动点")
        print(DIVIDER)
        print(f"不动点:  {fp['fixed_point']}")
        print(f"数字根:  {fp['digital_root']}")
        print(f"判定:    {fp['verification']}")
        print(f"log369:  {fp['log_369']}")
        print(f"perm369: {fp['perm_369']}")
        print(DIVIDER)
        print(f"洛书宫和: {engine.constants['LUO_SHU_SUM']}")
        return

    if "--wuxing" in args:
        idx = args.index("--wuxing")
        n = int(args[idx + 1]) if idx + 1 < len(args) else 369
        wx = engine.wuxing(n)
        print(f"🐉 {n} → 数字根 {engine.compute(n)} → {wx['element']}({wx['direction']}){wx['color']}")
        return

    if "--shengke" in args:
        idx = args.index("--shengke")
        a = int(args[idx + 1]) if idx + 1 < len(args) else 3
        b = int(args[idx + 2]) if idx + 2 < len(args) else 6
        sk = engine.sheng_ke(a, b)
        print(f"🐉 {a}({engine.wuxing(a)['element']}) vs {b}({engine.wuxing(b)['element']}): {sk['relation']} — {sk['detail']}")
        return

    n = int(args[0])
    dr = engine.compute(n)
    trace = engine.root_trace(n)
    wx = engine.wuxing(n)
    luo = engine.luo_shu_position(n)

    print(DIVIDER)
    print(f"🐉 数字根: {n} → {dr}")
    print(DIVIDER)
    print(f"追溯:  {' → '.join(str(t) for t in trace)}")
    print(f"五行:  {wx['element']}({wx['direction']}){wx['color']}")
    print(f"洛书:  第{luo['row']}行第{luo['col']}列 = {luo['luo_shu_value']}")
    print(f"369判定: {'🟢 是' if engine.is_369(n) else '— 否'}")
    print(DIVIDER)


def cmd_chain(args):
    if not args:
        print("用法: lh chain <write|verify|stats>")
        return

    sub = args[0]
    if sub == "write":
        data_str = " ".join(args[1:]) if len(args) > 1 else '{"action":"cli-test"}'
        try:
            data = json.loads(data_str)
        except json.JSONDecodeError:
            data = {"action": data_str}
        record = write_record(data)
        print(f"🐉 年轮链写入 #{record['index']}")
        print(f"   哈希: {record['hash'][:16]}...")
        print(f"   前驱: {record['prev_hash'][:16]}...")
    elif sub == "verify":
        is_valid, breaks = verify_chain()
        if is_valid:
            print("🟢 年轮链完整，无断裂")
        else:
            print(f"🔴 年轮链断裂: {len(breaks)} 处")
            for b in breaks[:5]:
                print(f"   #{b['index']}: {b['type']}")
    elif sub == "stats":
        from longhun_core.historian import _get_chain
        chain = _get_chain()
        s = chain.stats()
        print(DIVIDER)
        print(f"🐉 年轮链统计")
        print(DIVIDER)
        print(f"名称:   {s['name']}")
        print(f"长度:   {s['length']}")
        print(f"完整:   {'🟢 是' if s['valid'] else '🔴 否'}")
        print(f"断裂:   {s['breaks']}")
        print(f"根哈希: {s['root_hash']}")
        print(DIVIDER)


def cmd_flow(args):
    fc = FlowController()
    if not args:
        print("用法: lh flow <stats|tricolor>")
        return

    sub = args[0]
    if sub == "stats":
        stats = fc.all_stats()
        if not stats:
            # 跑一些流量来产生统计
            for _ in range(100):
                fc.process("default", tokens=1, timeout=0.01)
            stats = fc.all_stats()
        print(DIVIDER)
        print("🐉 流控统计")
        print(DIVIDER)
        for tid, s in stats.items():
            print(f"  [{tid}]")
            print(f"   速率: {s['rate']} t/s | 桶容量: {s['capacity']}")
            print(f"   消费: {s['total_consumed']} | 拒绝: {s['total_blocked']}")
            print(f"   阻塞率: {s['block_rate']:.2%}")
        print(DIVIDER)
    elif sub == "tricolor":
        for _ in range(100):
            fc.process("default", tokens=1, timeout=0.01)
        tc = fc.tricolor_assessment()
        print(DIVIDER)
        print(f"🐉 流控三色审计")
        print(DIVIDER)
        print(f"判定: {tc['tricolor']} R={tc['R_value']}/100")
        print(f"平均阻塞率: {tc['avg_block_rate']:.3f}")
        print(f"最大阻塞率: {tc['max_block_rate']:.3f}")
        print(f"活跃租户: {tc['active_tenants']}")
        print(DIVIDER)


def cmd_bench(args=None):
    """跑自检基准测试"""
    import time as _time

    print(DIVIDER)
    print("🐉 龍魂低算力内核 · 基准测试")
    print(DIVIDER)

    # 1. DNA 吞吐
    engine = DNAEngine()
    count = 10000
    t0 = _time.perf_counter()
    for i in range(count):
        engine.stamp(module=f"BENCH", action=f"T{i}")
    t1 = _time.perf_counter()
    dna_rate = count / (t1 - t0)
    print(f"📊 DNA签发:  {dna_rate:,.0f} 条/秒 ({count}条, {t1-t0:.3f}s)")

    # 2. 年轮链写入
    chain = YearRingChain(name="bench")
    count2 = 5000
    t0 = _time.perf_counter()
    for i in range(count2):
        chain.write({"id": f"bench-{i}", "value": i})
    t1 = _time.perf_counter()
    chain_rate = count2 / (t1 - t0) if (t1 - t0) > 0 else 0
    print(f"📊 年轮链写入: {chain_rate:,.0f} 条/秒 ({count2}条, {t1-t0:.3f}s)")

    # 3. 流控吞吐
    bucket = create_rate_limiter(999999)  # 不限速
    count3 = 100000
    t0 = _time.perf_counter()
    for i in range(count3):
        bucket.try_consume(1)
    t1 = _time.perf_counter()
    flow_rate = count3 / (t1 - t0) if (t1 - t0) > 0 else 0
    print(f"📊 流控吞吐:  {flow_rate:,.0f} token/秒 ({count3}条, {t1-t0:.3f}s)")

    # 4. 三色审计
    auditor = TricolorAudit()
    count4 = 50000
    data = {"阻塞率": 0.02, "耗时_ms": 120, "错误率": 0.005}
    t0 = _time.perf_counter()
    for i in range(count4):
        auditor.quick_eval(data)
    t1 = _time.perf_counter()
    audit_rate = count4 / (t1 - t0) if (t1 - t0) > 0 else 0
    print(f"📊 审计吞吐:  {audit_rate:,.0f} 条/秒 ({count4}条, {t1-t0:.3f}s)")

    # 5. 数字根
    count5 = 100000
    t0 = _time.perf_counter()
    for i in range(count5):
        compute_root(i)
    t1 = _time.perf_counter()
    root_rate = count5 / (t1 - t0) if (t1 - t0) > 0 else 0
    print(f"📊 数字根:    {root_rate:,.0f} 次/秒 ({count5}次, {t1-t0:.3f}s)")

    # 6. 内存估算
    import sys as _sys
    print(f"\n📊 内存估算:")
    print(f"   审计引擎对象: ~{_sys.getsizeof(auditor)} bytes")
    print(f"   年轮链 {chain.length}条: ~{_sys.getsizeof(chain.chain)} bytes (含数据)")
    print(f"   单条审计记录: ~{_sys.getsizeof(auditor.quick_eval(data))} bytes (str 引用)")

    print(DIVIDER)
    print(f"🟢 基准测试完成 — 零网络依赖 · 纯标准库")
    print(DIVIDER)


def cmd_info(args=None):
    """系统信息摘要"""
    import hashlib
    import sys as _sys

    print(DIVIDER)
    print(f"🐉 龍魂低算力内核 v{__version__}")
    print(DIVIDER)
    print(f"Python:  {_sys.version.split()[0]}")
    print(f"平台:    {_sys.platform}")
    print(f"DNA:     {__dna__}")
    print(DIVIDER)
    print("五模块:")
    print("  dna_trace      — 干支DNA追溯·44,875条/秒")
    print("  tricolor_audit — 三色审计🟢🟡🔴·7项默认检查")
    print("  historian      — 年轮链·篡改即断链🔴")
    print("  digital_root   — 369洛书数字根·五行属性")
    print("  flow_control   — 令牌桶流控·327,785 token/秒")
    print(DIVIDER)
    print("纯标准库 · 零网络依赖 · 断网可跑")
    print("工程层: MulanPSL v2 | 思想层: CC BY-NC-SA 4.0")
    print(DIVIDER)


def cmd_help(args=None):
    """lh-core 独立帮助入口"""
    print(DIVIDER)
    print("🐉 龍魂低算力内核 · lh-core 帮助")
    print(DIVIDER)
    print(f"版本: v{__version__}")
    print(f"DNA:  {__dna__}")
    print(DIVIDER)
    print("用法: lh-core <command> [args...]")
    print("      lh core <command> [args...]   (通过完整版 lh 调用)")
    print()
    print("命令:")
    print("  help, --help, -h   显示本帮助")
    print("  version            版本与 DNA")
    print("  info               系统信息摘要")
    print("  dna [文本]          签发干支 DNA")
    print("  audit --json '{...}'   三色审计")
    print("  root <数字>          数字根 · 洛书 · 五行")
    print("  root --wuxing <n>    数字五行属性")
    print("  root --shengke <a> <b>  五行生克关系")
    print("  chain write/verify/stats  年轮链写入/校验/统计")
    print("  flow stats/tricolor  流控统计与三色审计")
    print("  bench              自检基准测试")
    print()
    print("示例:")
    print("  lh-core dna 我的第一行代码")
    print("  lh-core audit --json '{\"阻塞率\":0.02,\"耗时_ms\":120,\"错误率\":0.005}'")
    print("  lh-core root 369")
    print("  lh-core root --wuxing 2025")
    print("  lh-core chain write '{\"action\":\"deploy\"}'")
    print("  lh-core flow tricolor")
    print("  lh-core bench")
    print()
    print("特性:")
    print("  · 纯 Python 标准库 · 零第三方依赖")
    print("  · 断网可跑 · 低算力设备友好")
    print("  · DNA 追溯 · 三色审计 · 年轮链 · 数字根 · 流控")
    print(DIVIDER)


def main():
    if len(sys.argv) < 2:
        cmd_version()
        print()
        print("用法: lh-core <command> [args...]")
        print("      lh-core --help  查看完整帮助")
        return

    cmd = sys.argv[1]
    args = sys.argv[2:]

    if cmd in ("--help", "-h", "help"):
        cmd_help()
        return

    commands = {
        "version": cmd_version,
        "dna": cmd_dna,
        "audit": cmd_audit,
        "root": cmd_root,
        "chain": cmd_chain,
        "flow": cmd_flow,
        "bench": cmd_bench,
        "info": cmd_info,
    }

    if cmd in commands:
        commands[cmd](args)
    else:
        print(f"🔴 未知命令: {cmd}")
        print(f"   可用: {', '.join(commands.keys())}, help")
        sys.exit(1)


if __name__ == "__main__":
    main()
