#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
龍魂 · 八卦阵参数回归框架 v1.0
目标：从实测数据回归地利 G(x)、人和 H(p)、水军检测的权重与阈值。
DNA: #龍芯⚡️2026-07-19-BAGUA-PARAM-REGRESSION-v1.0
"""

import json
import math
import random
from pathlib import Path
from collections import defaultdict

PROJECT = Path(__file__).resolve().parent.parent
OUT = PROJECT / "models" / "longhun-v1.0" / "bagua_regression"
OUT.mkdir(parents=True, exist_ok=True)


# ========== 5.2 地利 G(x) ==========
def G_score(x, weights=None):
    """
    地利得分 G(x) = Σ w_i * g_i(x)
    x = {"drain":坡度得分, "aspect":朝向得分, "watershed":汇水比, "barrier":屏障系数, "access":通达数}
    """
    if weights is None:
        weights = {"drain": 0.25, "aspect": 0.20, "watershed": 0.25, "barrier": 0.20, "access": 0.10}
    return sum(weights[k] * x.get(k, 0.0) for k in weights)


def grid_search_G(samples, n_trials=2000):
    """
    对 G(x) 权重做随机搜索，最大化与人工标记得分的 Pearson 相关。
    samples: [{"features": {...}, "label": 0..1}, ...]
    """
    keys = ["drain", "aspect", "watershed", "barrier", "access"]
    best = None
    best_corr = -1
    labels = [s["label"] for s in samples]
    for _ in range(n_trials):
        w = {k: random.random() for k in keys}
        s = sum(w.values())
        w = {k: v / s for k, v in w.items()}
        preds = [G_score(smp["features"], w) for smp in samples]
        corr = pearson(preds, labels)
        if corr > best_corr:
            best_corr = corr
            best = w
    return best, best_corr


def pearson(a, b):
    n = len(a)
    if n < 2:
        return 0.0
    ma, mb = sum(a) / n, sum(b) / n
    num = sum((a[i] - ma) * (b[i] - mb) for i in range(n))
    den = math.sqrt(sum((x - ma) ** 2 for x in a) * sum((y - mb) ** 2 for y in b))
    return num / den if den > 1e-9 else 0.0


# ========== 5.4 阵势指数 Z ==========
def Z_score(T, G, H, alpha=0.25, beta=0.35, gamma=0.40):
    if min(T, G, H) <= 0:
        return 0.0
    return T ** alpha * G ** beta * H ** gamma


def grid_search_Z(samples, n_grid=21):
    """
    回归 Z 的指数权重 α,β,γ，约束 α+β+γ=1。
    samples: [{"T":..., "G":..., "H":..., "label":...}, ...]
    """
    best = None
    best_corr = -1
    for i in range(n_grid):
        for j in range(n_grid - i):
            alpha = i / n_grid
            beta = j / n_grid
            gamma = 1 - alpha - beta
            preds = [Z_score(s["T"], s["G"], s["H"], alpha, beta, gamma) for s in samples]
            corr = pearson(preds, [s["label"] for s in samples])
            if corr > best_corr:
                best_corr = corr
                best = (alpha, beta, gamma)
    return {"alpha": best[0], "beta": best[1], "gamma": best[2]}, best_corr


# ========== 7.3 水军检测阈值 ==========
def shuijun_classify(f, thresholds=None):
    """
    f = {"rho": 机器节律, "entropy": 偏好熵, "factor_score": 七因子异常数}
    thresholds: {"rho":0.6, "entropy":2.5, "factor":2}
    返回八门标签：开门/休门/伤门/杜门/景门/死门/惊门/生门
    """
    if thresholds is None:
        thresholds = {"rho": 0.6, "entropy": 2.5, "factor": 2}
    rho = f.get("rho", 0)
    ent = f.get("entropy", 0)
    fac = f.get("factor_score", 0)
    # 简单规则（示例，待真实数据回归）
    if fac >= 5:
        return "惊门"
    if rho >= thresholds["rho"] and ent >= thresholds["entropy"]:
        return "死门"
    if rho >= thresholds["rho"] or ent >= thresholds["entropy"]:
        return "杜门"
    if fac >= thresholds["factor"]:
        return "伤门"
    if fac >= 1:
        return "休门"
    return "开门"


def search_shuijun_thresholds(samples):
    """
    网格搜索水军分类阈值，最大化 F1（假设标签已人工标注）。
    samples: [{"features":{rho,entropy,factor_score}, "label":"死门"/...}, ...]
    """
    best_f1 = 0
    best_thr = None
    # 简化为二分类：死门 vs 非死门
    for rho_thr in [0.5, 0.6, 0.7, 0.8]:
        for ent_thr in [2.0, 2.5, 3.0, 3.5]:
            for fac_thr in [1, 2, 3, 4]:
                tp = fp = fn = 0
                for s in samples:
                    pred = shuijun_classify(s["features"], {"rho": rho_thr, "entropy": ent_thr, "factor": fac_thr})
                    true = s["label"] == "死门"
                    pred_dead = pred == "死门"
                    if true and pred_dead:
                        tp += 1
                    elif not true and pred_dead:
                        fp += 1
                    elif true and not pred_dead:
                        fn += 1
                precision = tp / (tp + fp) if (tp + fp) else 0
                recall = tp / (tp + fn) if (tp + fn) else 0
                f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0
                if f1 > best_f1:
                    best_f1 = f1
                    best_thr = {"rho": rho_thr, "entropy": ent_thr, "factor": fac_thr, "precision": precision, "recall": recall, "f1": f1}
    return best_thr, best_f1


# ========== 合成示例数据 ==========
def make_synthetic_G(n=200):
    samples = []
    for _ in range(n):
        # 模拟：排水、朝向、汇水、屏障、通达
        x = {
            "drain": random.uniform(0.3, 1.0),
            "aspect": random.uniform(0.4, 1.0),
            "watershed": random.uniform(0.2, 1.0),
            "barrier": random.uniform(0.5, 1.0),
            "access": random.uniform(0.3, 1.0),
        }
        # 假设真实权重：drain=0.3, watershed=0.3, barrier=0.2, aspect=0.1, access=0.1
        label = 0.3 * x["drain"] + 0.3 * x["watershed"] + 0.2 * x["barrier"] + 0.1 * x["aspect"] + 0.1 * x["access"]
        label = min(1.0, max(0.0, label + random.uniform(-0.05, 0.05)))
        samples.append({"features": x, "label": label})
    return samples


def make_synthetic_Z(n=200):
    samples = []
    for _ in range(n):
        T = random.uniform(0.4, 1.0)
        G = random.uniform(0.4, 1.0)
        H = random.uniform(0.4, 1.0)
        # 假设真实权重 alpha=0.25,beta=0.35,gamma=0.40
        label = (T ** 0.25) * (G ** 0.35) * (H ** 0.40)
        label = min(1.0, max(0.0, label + random.uniform(-0.03, 0.03)))
        samples.append({"T": T, "G": G, "H": H, "label": label})
    return samples


def make_synthetic_shuijun(n=200):
    samples = []
    for _ in range(n):
        is_bot = random.random() < 0.3
        if is_bot:
            f = {
                "rho": random.uniform(0.65, 0.95),
                "entropy": random.uniform(2.6, 4.0),
                "factor_score": random.randint(2, 6),
            }
            label = "死门" if f["factor_score"] >= 4 else "杜门"
        else:
            f = {
                "rho": random.uniform(0.0, 0.55),
                "entropy": random.uniform(1.0, 2.4),
                "factor_score": random.randint(0, 2),
            }
            label = "开门"
        samples.append({"features": f, "label": label})
    return samples


def main():
    print("=" * 60)
    print("🐉 八卦阵参数回归框架 v1.0")
    print("=" * 60)

    # G(x) 权重回归
    print("\n📐 地利 G(x) 权重回归（合成数据示例）")
    g_samples = make_synthetic_G()
    g_w, g_corr = grid_search_G(g_samples, n_trials=2000)
    print(f"   最佳权重: {g_w}")
    print(f"   Pearson 相关: {g_corr:.4f}")

    # Z 指数权重回归
    print("\n🌐 阵势指数 Z 权重回归（合成数据示例）")
    z_samples = make_synthetic_Z()
    z_w, z_corr = grid_search_Z(z_samples, n_grid=41)
    print(f"   最佳 αβγ: {z_w}")
    print(f"   Pearson 相关: {z_corr:.4f}")

    # 水军阈值回归
    print("\n🛡️ 水军检测阈值回归（合成数据示例）")
    s_samples = make_synthetic_shuijun()
    thr, f1 = search_shuijun_thresholds(s_samples)
    print(f"   最佳阈值: {thr}")
    print(f"   F1: {f1:.4f}")

    # 保存结果
    result = {
        "DNA": "#龍芯⚡️2026-07-19-BAGUA-PARAM-REGRESSION-v1.0",
        "note": "合成数据演示，真实数据替换后可得 deployable 参数",
        "G_weights": g_w,
        "G_correlation": g_corr,
        "Z_weights": z_w,
        "Z_correlation": z_corr,
        "shuijun_thresholds": thr,
        "shuijun_f1": f1,
    }
    out_path = OUT / "regression_result_v1.0.json"
    out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n💾 结果保存: {out_path}")


if __name__ == "__main__":
    main()
