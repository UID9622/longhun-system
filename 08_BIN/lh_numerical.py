# DNA: #龍芯⚡️丙午·丙申·甲子·癸酉·䷪夬-CODE-补DNA-e861073e
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""
🐉 龍魂 · 数值方法引擎 v1.0（Numerical Methods）

ML核心优化算法——沿损失梯度反方向走一小步。龍魂视角：
梯度下降是「千里之行，始于足下」——每一步都往更好的方向走。
η大小决定步长——太大可能越过最优，太小走得太慢。

核心公式:
  牛顿迭代:  x_{n+1} = x_n - f(x_n)/f'(x_n)
  误差界:    |e_{n+1}| ≤ C|e_n|^p (牛顿二次收敛 p=2)

知识卡: 数值方法 · Numerical Methods（ID=108 · dr=9·火·离宫 · 🔴底座）
常见误区: 跳过数值方法直接用框架——遇到NaN/梯度爆炸就不知道根因在哪。
落地映射: 自动微分 · 梯度下降 · 训练管线 · 数值稳定性

DNA: #龍芯⚡️丙午·甲申·甲子·庚午·䷙大畜-NUMERICAL-METHODS-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0（核心思想层）· 工程层 MulanPSL v2
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
三色: 🟢 通过
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)

用法:
  python3 bin/lh_numerical.py --newton          # 牛顿迭代求 sqrt(2)
  python3 bin/lh_numerical.py --gd --lr 0.1     # 梯度下降最小化 x²-4x+4
  python3 bin/lh_numerical.py --stability-check 1e-300 1e300  # NaN/溢出检测
  python3 bin/lh_numerical.py --self-test
"""

import argparse
import math
import os
import sys


def _stamp() -> str:
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from lh_time_engine import get_output_stamp
        return get_output_stamp()
    except Exception:
        return "🐉[时间引擎不可用]"


def newton(f, df, x0, eps=1e-10, max_iter=100):
    """牛顿迭代求根: x_{n+1} = x_n - f(x_n)/f'(x_n)"""
    x = x0
    hist = []
    for i in range(max_iter):
        fx = f(x)
        dfx = df(x)
        if dfx == 0:
            raise ZeroDivisionError(f"迭代第{i}步导数接近0, x={x}")
        x_new = x - fx / dfx
        hist.append((i + 1, x_new, abs(f(x_new))))
        if abs(f(x_new)) < eps:
            return x_new, hist
        x = x_new
    raise RuntimeError(f"{max_iter}步未收敛, x={x}, f(x)={f(x)}")


def gradient_descent(df, x0, lr=0.1, n_iter=100, tol=1e-6):
    """梯度下降: x ← x - lr·∇f(x)（ML优化视角·千里之行始于足下）"""
    x = x0
    hist = []
    for i in range(n_iter):
        g = df(x)
        x_new = x - lr * g
        hist.append((i + 1, x_new, abs(g)))
        if abs(g) < tol:
            return x_new, hist
        x = x_new
    return x, hist


def error_order(errs):
    """误差收敛阶估计 p ≈ log(|e_{n+2}/e_{n+1}|) / log(|e_{n+1}/e_n|)"""
    if len(errs) < 4 or any(e == 0 for e in errs[:4]):
        return None
    p = []
    for i in range(len(errs) - 2):
        r1, r2 = errs[i + 1] / errs[i], errs[i + 2] / errs[i + 1]
        if r1 > 0 and r2 > 0 and r1 != 1:
            p.append(math.log(r2) / math.log(r1))
    return sum(p) / len(p) if p else None


def stability_check(values):
    """数值稳定性检测: NaN/Inf/接近零分母/溢出"""
    issues = []
    for i, v in enumerate(values):
        if isinstance(v, float) and (math.isnan(v) or math.isinf(v)):
            issues.append(f"位置{i}: {v} (NaN/Inf)")
        elif isinstance(v, complex) and (math.isnan(v.real) or math.isinf(v.real)):
            issues.append(f"位置{i}: 复数虚部异常")
    return issues


def self_test():
    ok = True
    # 1) 知识卡示例: 牛顿法求 sqrt(2)
    root, hist = newton(lambda x: x * x - 2, lambda x: 2 * x, 1.0)
    err = abs(root - math.sqrt(2))
    ok &= err < 1e-9
    print(f"[1] 牛顿迭代 sqrt(2) = {root:.10f} (误差 {err:.2e}) "
          f"{'✅' if err < 1e-9 else '❌'} · {len(hist)}步")
    # 2) 二次收敛验证: 误差每步平方级缩小
    errs = [abs(h[1] - math.sqrt(2)) for h in hist]
    p = error_order(errs)
    ok &= p is not None and p > 1.5
    print(f"[2] 收敛阶估计 p ≈ {p:.2f} (牛顿理论 p=2) "
          f"{'✅' if p is not None and p > 1.5 else '❌'}")
    # 3) 梯度下降收敛: f(x)=x²-4x+4 最小值 x=2
    x, ghist = gradient_descent(lambda x: 2 * x - 4, 0.0, lr=0.1, n_iter=100)
    ok &= abs(x - 2.0) < 1e-4
    print(f"[3] 梯度下降 x²-4x+4 → x={x:.6f} (理论2.0) "
          f"{'✅' if abs(x-2.0) < 1e-4 else '❌'} · {len(ghist)}步")
    # 4) 学习率过大 → 越过最优不收敛
    x2, _ = gradient_descent(lambda x: 2 * x - 4, 0.0, lr=2.5, n_iter=50)
    ok &= abs(x2 - 2.0) > 1e-3
    print(f"[4] lr=2.5 过大振荡 x={x2:.4f} (验证步长过大的危害) "
          f"{'✅' if abs(x2-2.0) > 1e-3 else '❌'}")
    # 5) 数值稳定性
    issues = stability_check([1e-300, float("nan"), 1e300 * 1e300])
    ok &= len(issues) >= 2
    print(f"[5] 稳定性检测发现 {len(issues)} 处异常: {issues[:2]} "
          f"{'✅' if len(issues) >= 2 else '❌'}")
    print(f"\n🐉 数值方法自检: {'全绿 ✅' if ok else '有失败 ❌'}")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description="龍魂·数值方法引擎 v1.0")
    ap.add_argument("--newton", action="store_true", help="牛顿迭代求 sqrt(2)")
    ap.add_argument("--gd", action="store_true", help="梯度下降演示")
    ap.add_argument("--lr", type=float, default=0.1, help="学习率(默认0.1)")
    ap.add_argument("--n-iter", type=int, default=100, help="迭代次数")
    ap.add_argument("--stability-check", nargs="*", type=float, help="数值稳定性检测")
    ap.add_argument("--self-test", action="store_true", help="自我验证")
    args = ap.parse_args()

    if args.self_test:
        sys.exit(self_test())

    if args.newton:
        root, hist = newton(lambda x: x * x - 2, lambda x: 2 * x, 1.0)
        print(f"牛顿迭代求 sqrt(2):")
        for step, x, fx in hist:
            print(f"  step {step:>2}: x = {x:.10f} · |f(x)| = {fx:.2e}")
        print(f"结果: sqrt(2) ≈ {root:.10f} (math.sqrt(2) = {math.sqrt(2):.10f})")
    elif args.gd:
        x, hist = gradient_descent(lambda x: 2 * x - 4, 0.0, lr=args.lr, n_iter=args.n_iter)
        print(f"梯度下降 f(x)=x²-4x+4 (最小值 x=2) · lr={args.lr} · {len(hist)}步")
        for step, xv, g in hist[:: max(1, len(hist) // 5)] + [hist[-1]]:
            print(f"  step {step:>3}: x = {xv:.6f} · |∇f| = {g:.2e}")
        print(f"收敛于 x ≈ {x:.4f} {'✅' if abs(x-2.0)<1e-3 else '⚠️ 未收敛'}")
    elif args.stability_check:
        issues = stability_check(args.stability_check)
        if issues:
            print("⚠️ 数值异常:")
            for i in issues:
                print(f"  {i}")
        else:
            print("✅ 数值稳定: 无 NaN/Inf/溢出")
    else:
        ap.print_help()
        return 1
    print(f"\n{_stamp()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
