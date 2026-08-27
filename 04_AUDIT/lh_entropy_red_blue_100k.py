#!/usr/bin/env python3
"""
龙魂红蓝对抗 · AI熵增引擎 10万次防御验证 v1.0
DNA: #龍芯⚡️2026-08-27-丙午·丙申·戊子·癸亥-LHAE-REDBLUE-100K-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0（核心思想层）
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

红队（P77黑天使军团）:
  红天使: 攻击向量池注入（NaN/inf/负值/极端/零/单热/微值/混合/长度/类型）
  暗天使: 极端参数穿透（gamma/floor 攻击组合）
  夜天使: 10万次主战场（真实标定参数·随机扰动对抗）
蓝队（龍魂引擎防御层）:
  崩溃防护 + 有限性校验 + 合理域校验 + 串行/向量化交叉自检
判定:
  🟢 拦截/有限合理 = 防御成功
  🔴 NaN/inf泄漏 = 红队击穿（蓝队护栏缺口）
"""
import datetime
import json
import os
import sys
import time

import numpy as np

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.join(ROOT, "engines"))
from lh_ai_entropy_engine import (  # noqa: E402
    run_monte_carlo_vectorized,
    run_monte_carlo,
)

DNA = "#龍芯⚡️2026-08-27-丙午·丙申·戊子·癸亥-LHAE-REDBLUE-100K-v1.0-UID9622"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"

# ── 红队攻击向量池 ──
ATTACK_VECTORS = [
    ("nan", (float("nan"),) * 4),
    ("inf+", (float("inf"),) * 4),
    ("inf-", (float("-inf"),) * 4),
    ("negative", (-1.0, -2.0, -3.0, -4.0)),
    ("huge-1e6", (1e6,) * 4),
    ("zero", (0.0, 0.0, 0.0, 0.0)),
    ("single-hot", (0.0, 0.0, 0.0, 5.0)),
    ("equal-1", (1.0, 1.0, 1.0, 1.0)),
    ("tiny-1e-6", (1e-6, 1e-6, 1e-6, 1e-6)),
    ("mixed-edge", (3.0, 0.0, 0.0, 3.0)),
    ("default-random", None),
    ("bad-len", (1.0, 2.0, 3.0)),
    ("bad-type", ("a", "b", "c", "d")),
]

PARAM_ATTACKS = [
    ("gamma-zero", {"gamma": 0.0}),
    ("gamma-neg", {"gamma": -0.2}),
    ("gamma-nan", {"gamma": float("nan")}),
    ("gamma-huge", {"gamma": 1e6}),
    ("floor-neg", {"floor_guard": -1.0}),
    ("floor-nan", {"floor_guard": float("nan")}),
    ("floor-huge", {"floor_guard": 1e6}),
    ("floor-tiny", {"floor_guard": 1e-9}),
]

REAL_INIT = (1.9, 0.6, 1.1, 2.2)  # 真实标定 v2.0
MAIN_SIMS = 100_000
ATTACK_SIMS = 10_000
PARAM_SIMS = 5_000
CROSS_SIMS = 2_000


def is_finite_array(a):
    return bool(np.all(np.isfinite(a))) if a is not None else False


def classify_result(res):
    """蓝队判定: 🟢有限合理 / 🔴NaN泄漏 / 越界"""
    if res is None:
        return "🔴 no-result", None
    s = res.summary()
    hp = s.get("fixed_point_H_star", {})
    mean = hp.get("mean")
    conv = s.get("convergence_rate")
    neg = s.get("mean_negentropy")
    vals = [v for v in (mean, conv, neg) if v is not None]
    if not vals or not is_finite_array(np.array(vals, dtype=float)):
        return "🔴 NaN/inf泄漏", s
    if mean is not None and not (0.0 <= mean <= 8.0):
        return "🔴 越界", s
    return "🟢 有限合理", s


def vector_attack(name, init_h, n_sims=ATTACK_SIMS):
    """红队向量注入 → 蓝队防御"""
    try:
        res = run_monte_carlo_vectorized(
            n_sims=n_sims, n_steps=200, seed=9622, verbose=False,
            floor_guard=1.0, gamma=0.20, init_h=init_h, tag=f"red-{name}")
        status, s = classify_result(res)
    except (ValueError, TypeError) as e:
        return "🟢 拦截(拒绝非法输入)", {"error": str(e)[:80]}
    except Exception as e:  # noqa: BLE001
        return "🔴 崩溃", {"error": repr(e)[:120]}
    return status, s


def param_attack(name, kw, init_h=REAL_INIT, n_sims=PARAM_SIMS):
    try:
        res = run_monte_carlo_vectorized(
            n_sims=n_sims, n_steps=200, seed=9622, verbose=False,
            init_h=init_h, tag=f"red-param-{name}", **kw)
        status, s = classify_result(res)
    except (ValueError, TypeError) as e:
        return "🟢 拦截(拒绝非法输入)", {"error": str(e)[:80]}
    except Exception as e:  # noqa: BLE001
        return "🔴 崩溃", {"error": repr(e)[:120]}
    return status, s


def main():
    print("⚔️ 龙魂红蓝对抗 · AI熵增引擎 10万次防御验证 v1.0")
    print(f"DNA: {DNA}")
    print(f"确认码: {CONFIRM}")
    print("=" * 64)
    report = {"dna": DNA, "timestamp": datetime.datetime.now().isoformat(),
              "confirm": CONFIRM, "attack_vectors": [], "param_attacks": [],
              "main_battle": {}, "cross_check": {}, "status": "🔴 未完成"}

    # 阶段一: 红天使向量注入
    print("\n[红天使] 阶段一 · 攻击向量池注入")
    for name, vec in ATTACK_VECTORS:
        status, s = vector_attack(name, vec)
        detail = ""
        hp = s.get("fixed_point_H_star", {}) if s else {}
        if "mean" in hp:
            detail = f" H*={hp['mean']} conv={s.get('convergence_rate')}"
        print(f"  {name:<16} {status}{detail}")
        report["attack_vectors"].append({"name": name, "status": status,
                                         "summary": s})

    # 阶段二: 暗天使参数穿透
    print("\n[暗天使] 阶段二 · 极端参数穿透")
    for name, kw in PARAM_ATTACKS:
        status, s = param_attack(name, kw)
        detail = ""
        hp = s.get("fixed_point_H_star", {}) if s else {}
        if "mean" in hp:
            detail = f" H*={hp['mean']}"
        print(f"  {name:<16} {status}{detail}")
        report["param_attacks"].append({"name": name, "status": status,
                                        "summary": s})

    # 阶段三: 蓝队交叉自检（串行 vs 向量化）
    print(f"\n[蓝队] 阶段三 · 串行 vs 向量化交叉自检 (n={CROSS_SIMS})")
    rv = run_monte_carlo_vectorized(
        n_sims=CROSS_SIMS, n_steps=200, seed=9622, verbose=False,
        floor_guard=1.0, gamma=0.20, init_h=REAL_INIT, tag="cross-vec")
    # 串行版不支持 init_h/gamma/floor → 用默认随机，只比"双引擎都能跑+输出有限"
    rs = run_monte_carlo(n_sims=CROSS_SIMS, n_steps=200, seed=9622, verbose=False)
    sv = rv.summary()
    ss = rs.summary()
    vec_ok = is_finite_array(np.array([sv["fixed_point_H_star"].get("mean", 0.0),
                                       sv["convergence_rate"],
                                       sv["mean_negentropy"]]))
    ser_ok = is_finite_array(np.array([ss["fixed_point_H_star"].get("mean", 0.0),
                                       ss["convergence_rate"],
                                       ss["mean_negentropy"]]))
    cross = {
        "vectorized": {"mean": sv["fixed_point_H_star"].get("mean"),
                       "conv": sv["convergence_rate"], "finite": bool(vec_ok)},
        "serial": {"mean": ss["fixed_point_H_star"].get("mean"),
                   "conv": ss["convergence_rate"], "finite": bool(ser_ok)},
    }
    cross["ok"] = bool(vec_ok and ser_ok)
    print(f"  向量化: H*={cross['vectorized']['mean']} "
          f"conv={cross['vectorized']['conv']}")
    print(f"  串行:   H*={cross['serial']['mean']} "
          f"conv={cross['serial']['conv']}")
    print(f"  交叉自检: {'🟢 双引擎均有限' if cross['ok'] else '🔴 引擎输出非有限'}")
    report["cross_check"] = cross

    # 阶段四: 夜天使10万次主战场
    print(f"\n[夜天使] 阶段四 · 10万次主战场 "
          f"(γ=0.20 floor=1.0 init_h={REAL_INIT})")
    t0 = time.time()
    rmain = run_monte_carlo_vectorized(
        n_sims=MAIN_SIMS, n_steps=200, seed=9622, verbose=False,
        floor_guard=1.0, gamma=0.20, init_h=REAL_INIT, tag="red-blue-main-100k")
    dt = time.time() - t0
    sm = rmain.summary()
    hp = sm["fixed_point_H_star"]
    mean_h = hp.get("mean")
    finite = is_finite_array(np.array(
        [mean_h if mean_h is not None else np.nan,
         sm["convergence_rate"], sm["mean_negentropy"]]))
    # 物理相对判据: H* 有限、非负、低于初值总熵、且收敛率≥70%
    init_total = float(sum(REAL_INIT))
    h_upper = min(init_total, 2.5)
    in_range = bool(finite and 0.0 <= mean_h <= h_upper
                    and sm["convergence_rate"] >= 0.7)
    main = {
        "n_sims": MAIN_SIMS, "n_steps": 200, "elapsed_s": round(dt, 2),
        "H_star_mean": mean_h, "H_star_stats": hp,
        "conv_rate": sm["convergence_rate"], "converged": sm["converged"],
        "diverged": sm["diverged"], "oscillating": sm["oscillating"],
        "colors": sm["final_colors"], "mean_negentropy": sm["mean_negentropy"],
        "finite": bool(finite), "in_target_range": in_range,
    }
    print(f"  ⏱ {dt:.1f}s · H*={mean_h}bits · conv={sm['convergence_rate']:.2%}")
    print(f"  三色: {sm['final_colors']} · 负熵={sm['mean_negentropy']:.2f}bits")
    verdict = (f"🟢 H*∈[0,{h_upper}]且有限·收敛≥70%" if in_range
               else "🔴 越界/非有限/收敛不足")
    print(f"  判定: {verdict}")
    report["main_battle"] = main

    # 汇总
    red_breach = [v for v in report["attack_vectors"] if "🔴" in v["status"]]
    param_breach = [v for v in report["param_attacks"] if "🔴" in v["status"]]
    report["red_breaches"] = [v["name"] for v in red_breach + param_breach]
    report["status"] = (
        "🔴 红队击穿" if (red_breach or param_breach or not main["in_target_range"])
        else "🟢 全防御成功")
    print("\n" + "=" * 64)
    print(f"最终判定: {report['status']}")
    print(f"红队击穿点: {report['red_breaches'] or '无'}")
    print(f"10万次主战场: {'🟢 通过' if main['in_target_range'] else '🔴 未达标'}")

    # 落盘
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "lh_entropy_red_blue_100k_report.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"\n✅ 报告已落盘: {out}")


if __name__ == "__main__":
    main()
