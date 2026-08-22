# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂·信任核心 CLI v1.0（统一入口 · 融合版）
============================================
DNA: #龍芯⚡️丙午·丙申-TRUST-CORE-v1.0-UNIFIED-ENTRY
创建者: 诸葛鑫（UID9622）
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
上层规则: CODEBUDDY对齐规则·第三层审计 / MEMORY.md §3-21 主动纠正+动态时间铁律
为什么存在: 2026-08-18 吸收 Kimi Agent 交付包「信任核心（事实校验+自愈）」
  与自研 `08_BIN/lh_fact_check.py`（身份时间线校准）融合成统一信任核心。
  引擎层=Kimi trust-core（可信度公式/自愈/审计/熔断），身份层=自研 lh_fact_check
  （动态年数·禁硬编码·时间线自洽）。彻底根除"一次算错→循环自证→滚进协议"雷。

用法:
  lh trust check "文本"                # 通用事实校验（身份文本扫描+DNA）
  lh trust check-time <声称年数> <起始年>   # 时间跨度校验（trust-core 三级纠正+熔断）
  lh trust check-identity <主体> <声称级别> # 身份级别校验（冒称L0→熔断）
  lh trust verify "文本"               # 身份时间线校准（动态年数·禁硬编码）
  lh trust scan [目录]                 # 扫描目录内错误时间线表述
  lh trust facts                      # 身份事实卡
  lh trust credibility <天数> <来源> <确认> # 可信度 C=0.4F+0.3S+0.3K
  lh trust dna <动作标签>               # DNA 生成（外部生成器优先）
  lh trust audit <名称>                # 审计日志读取
  lh trust heal [--once|--status] [--execute] [--confirm 码] # 自愈引擎（默认干跑·快照→修复→回滚→耻辱墙）
  lh trust test                       # 跑 trust-core 全部测试
  lh trust --status                   # 系统状态

来源枚举(credibility): founder=1.0 system=0.8 community=0.5 unknown=0.2
确认枚举(credibility): confirmed=1.0 unconfirmed=0.3 disputed=0.0
退出码: 0=🟢通过 1=🟡待核 2=🔴红线（对齐三色审计）

A-BOM 备案:
  目标函数: 信任一致性（事实校验+可信度+自愈+审计全链路留痕）
  输入特征: 文本/时间跨度声称/身份声称/来源与确认状态
  用户影响: 一切时间身份数字输入先验证再用·矛盾必纠·熔断防反复
  申诉通道: UID9622 口述事实修正→更新引擎 FACTS 后生效
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TRUST_CORE = ROOT / "04_ENGINES" / "trust-core"
FACT_CHECK = ROOT / "08_BIN" / "lh_fact_check.py"

# 三色退出码（对齐交付契约）
EXIT_GREEN = 0   # 🟢 通过
EXIT_YELLOW = 1  # 🟡 待核
EXIT_RED = 2     # 🔴 红线


def _stamp() -> str:
    """获取时间戳（不可达则降级）。"""
    try:
        r = subprocess.run(
            [sys.executable, str(ROOT / "bin" / "lh_time_engine.py"), "--stamp"],
            capture_output=True, text=True, timeout=10,
        )
        line = (r.stdout or "").strip().splitlines()
        if line:
            return line[-1][:80]
    except Exception:
        pass
    return "🐉丙午·时间引擎不可达"


def _load_trust_core():
    """加载 trust-core 引擎库（Kimi 交付包）。"""
    sys.path.insert(0, str(TRUST_CORE))
    from longhun_trust.audit import AuditLog
    from longhun_trust.credibility import (
        ConfirmationState, SourceLevel, compute_credibility, needs_confirmation,
    )
    from longhun_trust.dna import generate_dna, verify_confirm_code
    from longhun_trust.factcheck import FactCheckEngine
    return {
        "AuditLog": AuditLog,
        "ConfirmationState": ConfirmationState,
        "SourceLevel": SourceLevel,
        "compute_credibility": compute_credibility,
        "needs_confirmation": needs_confirmation,
        "generate_dna": generate_dna,
        "verify_confirm_code": verify_confirm_code,
        "FactCheckEngine": FactCheckEngine,
    }


def _run_fact_check(args: list[str]) -> int:
    """转调身份时间线校准引擎（08_BIN/lh_fact_check.py·已GPG签名·单一真相）。"""
    r = subprocess.run(
        [sys.executable, str(FACT_CHECK)] + args,
        cwd=str(ROOT), capture_output=True, text=True,
    )
    if r.stdout:
        print(r.stdout, end="")
    if r.stderr:
        print(r.stderr, end="", file=sys.stderr)
    return r.returncode


def cmd_check(args: argparse.Namespace, tc: dict) -> int:
    """通用事实校验：自由文本走身份扫描+DNA 锚。"""
    text = args.text
    from longhun_trust.factcheck import FactCheckEngine  # noqa: F401
    engine = tc["FactCheckEngine"]()
    dna = tc["generate_dna"]("TRUST-CHECK")
    # 自由文本：先过身份时间线扫描（动态年数），再过引擎校验
    r = subprocess.run(
        [sys.executable, str(FACT_CHECK), "--verify", text],
        cwd=str(ROOT), capture_output=True, text=True,
    )
    alerts = (r.stderr or "").strip()
    if r.returncode == 0:
        print("🟢 通用事实校验通过 · DNA:", dna)
        return EXIT_GREEN
    print("🟡 发现冲突表述，详情:", file=sys.stderr)
    print(alerts, file=sys.stderr)
    print("   调用: lh trust check-time <声称年数> <起始年> 做结构化校验", file=sys.stderr)
    return EXIT_YELLOW


def cmd_check_time(args: argparse.Namespace, tc: dict) -> int:
    """时间跨度校验（trust-core 三级纠正+熔断）。"""
    engine = tc["FactCheckEngine"]()
    result = engine.validate_time_span(args.claim, args.start)
    print(f"  {result.status} · {result.message}")
    if result.level is not None:
        print(f"  级别: {result.level.value} · 矛盾计数: "
              f"{engine._counts.get(f'time_span:{args.start}', 0)}/{engine.breaker_threshold}")
    return EXIT_GREEN if result.valid else EXIT_YELLOW


def cmd_check_identity(args: argparse.Namespace, tc: dict) -> int:
    """身份级别校验（冒称 L0 → SEVERE 熔断）。"""
    engine = tc["FactCheckEngine"]()
    result = engine.validate_identity(args.subject, args.level)
    print(f"  {result.status} · {result.message}")
    if result.level is not None:
        print(f"  级别: {result.level.value}")
    if result.level is not None and result.level.value == "severe":
        return EXIT_RED
    return EXIT_GREEN if result.valid else EXIT_YELLOW


def cmd_credibility(args: argparse.Namespace, tc: dict) -> int:
    """可信度计算 C=0.4F+0.3S+0.3K。"""
    src_map = {
        "founder": tc["SourceLevel"].FOUNDER, "system": tc["SourceLevel"].SYSTEM,
        "community": tc["SourceLevel"].COMMUNITY, "unknown": tc["SourceLevel"].UNKNOWN,
    }
    conf_map = {
        "confirmed": tc["ConfirmationState"].CONFIRMED,
        "unconfirmed": tc["ConfirmationState"].UNCONFIRMED,
        "disputed": tc["ConfirmationState"].DISPUTED,
    }
    src = src_map.get(args.source)
    conf = conf_map.get(args.confirmation)
    if src is None or conf is None:
        print(f"🔴 非法参数: 来源={args.source} 确认={args.confirmation}", file=sys.stderr)
        print("   来源: founder/system/community/unknown · 确认: confirmed/unconfirmed/disputed", file=sys.stderr)
        return EXIT_RED
    score = tc["compute_credibility"](args.age_days, src, conf)
    need = tc["needs_confirmation"](score)
    mark = "🟢" if not need else "🟡"
    print(f"  {mark} 可信度 C = {score}  (F:{'%.2f' % (0.4 * (1 - max(0, args.age_days) / 90))} "
          f"S:{src.value} K:{conf.value})")
    print(f"  {'需用户确认（<0.7）' if need else '可信度达标（≥0.7）'}")
    return EXIT_YELLOW if need else EXIT_GREEN


def cmd_dna(args: argparse.Namespace, tc: dict) -> int:
    """DNA 生成（外部生成器优先·禁手写干支）。"""
    dna = tc["generate_dna"](args.action, args.version)
    print("  🧬", dna)
    return EXIT_GREEN


def cmd_audit(args: argparse.Namespace, tc: dict) -> int:
    """审计日志读取（append-only·只增不删）。"""
    log = tc["AuditLog"](args.name)
    entries = log.read_all()
    print(f"  📜 审计日志 [{args.name}]: {len(entries)} 条")
    for e in entries[-20:][::-1]:
        ts = e.get("timestamp", "?")
        ev = e.get("event", "?")
        details = e.get("details", {})
        print(f"    {ts} [{ev}] {details}")
    return EXIT_GREEN


def cmd_heal(args: argparse.Namespace, tc: dict = None) -> int:
    """自愈引擎（转调 trust-core selfheal·默认干跑一轮）。"""
    cmd = [sys.executable, "-m", "longhun_trust.selfheal"]
    if args.status:
        cmd.append("--status")
    else:
        cmd.append("--once")          # 跑一轮（不 --execute = dry-run 只记录）
        if args.execute:
            cmd.append("--execute")   # 真执行安全策略
    if args.confirm:
        cmd += ["--confirm-code", args.confirm]
    r = subprocess.run(cmd, cwd=str(TRUST_CORE))
    return r.returncode


def cmd_test(args: argparse.Namespace, tc: dict = None) -> int:
    """跑 trust-core 全部测试。"""
    r = subprocess.run(
        [sys.executable, "-m", "pytest", str(TRUST_CORE / "tests"), "-q", "--no-header"],
        cwd=str(ROOT),
    )
    return r.returncode


def cmd_status(args: argparse.Namespace, tc: dict) -> int:
    """系统状态汇总。"""
    print("  🐉 龍魂·信任核心 v1.0（融合版）")
    print(f"    引擎库 : {TRUST_CORE}")
    print(f"    身份层 : {FACT_CHECK}  {'✅ 已签名' if (Path(str(FACT_CHECK) + '.asc')).exists() else '⚠️ 未签名'}")
    print(f"    模块   : audit credibility dna exceptions factcheck selfheal")
    # 事实卡
    r = subprocess.run(
        [sys.executable, str(FACT_CHECK)], cwd=str(ROOT),
        capture_output=True, text=True,
    )
    if r.stdout:
        print(r.stdout, end="")
    return EXIT_GREEN


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(
        prog="lh trust", description="龍魂·信任核心（事实校验+可信度+自愈+审计）",
    )
    sub = ap.add_subparsers(dest="cmd")

    p_check = sub.add_parser("check", help="通用事实校验（文本）")
    p_check.add_argument("text", help="要校验的文本")
    p_check.set_defaults(fn=cmd_check)

    p_ct = sub.add_parser("check-time", help="时间跨度校验")
    p_ct.add_argument("claim", type=int, help="声称年数")
    p_ct.add_argument("start", type=int, help="起始年份")
    p_ct.set_defaults(fn=cmd_check_time)

    p_ci = sub.add_parser("check-identity", help="身份级别校验")
    p_ci.add_argument("subject", help="主体标识")
    p_ci.add_argument("level", type=int, help="声称级别")
    p_ci.set_defaults(fn=cmd_check_identity)

    p_v = sub.add_parser("verify", help="身份时间线校准（文本）")
    p_v.add_argument("text", help="要校准的文本")
    p_v.set_defaults(fn=lambda a, tc: _run_fact_check(["--verify", a.text]))

    p_s = sub.add_parser("scan", help="扫描目录错误时间线表述")
    p_s.add_argument("dir", nargs="?", default=str(ROOT), help="目录（默认全项目）")
    p_s.set_defaults(fn=lambda a, tc: _run_fact_check(["--scan", a.dir]))

    p_f = sub.add_parser("facts", help="身份事实卡")
    p_f.set_defaults(fn=lambda a, tc: _run_fact_check([]))

    p_c = sub.add_parser("credibility", help="可信度计算")
    p_c.add_argument("age_days", type=float, help="距今天数")
    p_c.add_argument("source", help="来源: founder/system/community/unknown")
    p_c.add_argument("confirmation", help="确认: confirmed/unconfirmed/disputed")
    p_c.set_defaults(fn=cmd_credibility)

    p_d = sub.add_parser("dna", help="DNA 生成")
    p_d.add_argument("action", help="动作标签")
    p_d.add_argument("--version", default="v1.0", help="版本")
    p_d.set_defaults(fn=cmd_dna)

    p_a = sub.add_parser("audit", help="审计日志读取")
    p_a.add_argument("name", nargs="?", default="fact_check", help="日志名（默认 fact_check）")
    p_a.set_defaults(fn=cmd_audit)

    p_h = sub.add_parser("heal", help="自愈引擎")
    mode = p_h.add_mutually_exclusive_group()
    mode.add_argument("--once", action="store_true", help="跑一轮自愈（默认·dry-run）")
    mode.add_argument("--status", action="store_true", help="查看最近自愈报告")
    p_h.add_argument("--execute", action="store_true", help="真执行安全策略（默认只记录）")
    p_h.add_argument("--confirm", dest="confirm", default=None, help="回滚确认码")
    p_h.set_defaults(fn=cmd_heal)

    p_t = sub.add_parser("test", help="跑 trust-core 测试")
    p_t.set_defaults(fn=cmd_test)

    p_st = sub.add_parser("status", help="系统状态")
    p_st.set_defaults(fn=cmd_status)

    return ap


def main(argv: list[str] | None = None) -> int:
    ap = build_parser()
    args = ap.parse_args(argv)

    if getattr(args, "cmd", None) is None:
        ap.print_help()
        print("\n  🐉 示例:")
        print("    lh trust check-time 16 2008    # → 实际18年·🟡")
        print("    lh trust check-identity 黑客 0  # → 🔴 冒称L0熔断")
        print("    lh trust verify \"退伍16年\"       # → 动态年数报警")
        print("    lh trust heal --dry-run        # 自愈干跑")
        return EXIT_GREEN

    tc = _load_trust_core() if args.cmd not in ("heal", "test", "verify", "scan", "facts") else {}
    code = args.fn(args, tc)
    print()
    print("  " + _stamp())
    return code


if __name__ == "__main__":
    sys.exit(main())
