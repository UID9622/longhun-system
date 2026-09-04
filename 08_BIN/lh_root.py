#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DNA: #龍芯⚡️丙午·丙申·戊午·庚申·䷠遁-ALIGNMENT-RULES-V2.4-LH-ROOT-CLI-v1.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0（核心思想层）
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

龍魂·369数字根CLI v1.0 — 洛书369数字根 + 五行 + 生克 + 洛书宫位 + 权重
统一命令: lh root 369 | lh root --wuxing 2025 | lh root --luoshu 369
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "core"))

from longhun_core.digital_root import DigitalRoot  # noqa: E402


def _fmt(d):
    return json.dumps(d, ensure_ascii=False, indent=2)


def cmd_compute(engine, n):
    print("🐉 洛书369 · 数字根推演: %s" % n)
    print("=" * 46)
    print("  数字:      %s" % n)
    print("  数字根:    %s" % engine.compute(n))
    print("  根路径:    %s" % " → ".join(map(str, engine.root_trace(n))))
    print("  369不动点: %s" % ("✅ 是" if engine.is_369(n) else "—"))
    fp = engine.verify_fixed_point()
    print("  不动点验:  %s" % fp.get("verification", ""))
    wx = engine.wuxing(n)
    print("  五行:      %s · 方位 %s · 色 %s" % (wx["element"], wx["direction"], wx["color"]))
    ls = engine.luo_shu_position(n)
    print("  洛书宫位:  %s %s" % (ls.get("position", ""), ls.get("description", "")))
    print("=" * 46)


def cmd_wuxing(engine, n):
    wx = engine.wuxing(n)
    print("🐉 %s → 数字根 %s → 五行: %s · 方位 %s · 色 %s" % (n, engine.compute(n), wx["element"], wx["direction"], wx["color"]))


def cmd_shengke(engine, a, b):
    sk = engine.sheng_ke(a, b)
    print("🐉 生克判定: %s(%s) vs %s(%s)" % (a, engine.wuxing(a)["element"], b, engine.wuxing(b)["element"]))
    print(_fmt(sk))


def cmd_luoshu(engine, n):
    ls = engine.luo_shu_position(n)
    print("🐉 洛书宫位: %s → %s" % (n, ls.get("position", "")))
    print(_fmt(ls))


def cmd_weight(engine, pairs):
    data = {}
    for p in pairs:
        if "=" in p:
            k, v = p.split("=", 1)
            try:
                data[k] = float(v)
            except ValueError:
                print("⚠️ 跳过非法权重: %s" % p)
    if not data:
        print("用法: lh root --weight 速度=30 安全=50 成本=20")
        return
    w = engine.weight_score(data)
    print("🐉 权重得分: %s (数字根=%s)" % (w["score"], w["root"]))
    print(_fmt(w))


def main():
    p = argparse.ArgumentParser(prog="lh root", description="洛书369数字根引擎")
    p.add_argument("number", nargs="?", type=int, help="要推演的数字 (如 369)")
    p.add_argument("--wuxing", type=int, metavar="N", help="数字五行属性")
    p.add_argument("--luoshu", type=int, metavar="N", help="洛书宫位")
    p.add_argument("--shengke", nargs=2, type=int, metavar=("A", "B"), help="五行生克判定")
    p.add_argument("--weight", nargs="+", metavar="K=V", help="权重计算 如 速度=30 安全=50")
    p.add_argument("--check", type=int, metavar="N", help="自检: 验证引擎")
    args = p.parse_args()

    engine = DigitalRoot()

    if args.check is not None:
        fp = engine.verify_fixed_point()
        assert fp["is_369"], "369不动点验证失败"
        print("🟢 Digital Root v1.0 自检通过 | 369根=%s 洛书和=%s" % (fp["digital_root"], engine.constants["LUO_SHU_SUM"]))
        return

    if args.wuxing is not None:
        cmd_wuxing(engine, args.wuxing)
    elif args.luoshu is not None:
        cmd_luoshu(engine, args.luoshu)
    elif args.shengke is not None:
        cmd_shengke(engine, args.shengke[0], args.shengke[1])
    elif args.weight:
        cmd_weight(engine, args.weight)
    elif args.number is not None:
        cmd_compute(engine, args.number)
    else:
        p.print_help()
        print("\n示例:")
        print("  lh root 369              → 数字根+五行+洛书完整推演")
        print("  lh root --wuxing 2025    → 数字五行属性")
        print("  lh root --luoshu 369     → 洛书宫位")
        print("  lh root --shengke 3 9    → 五行生克")
        print("  lh root --weight 速度=30 安全=50 成本=20 → 权重")
        print("  lh root --check          → 引擎自检")
        sys.exit(0)


if __name__ == "__main__":
    main()
