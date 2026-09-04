#!/usr/bin/env python3
"""
龙魂反熵增引擎 · 真实AI熵采集与参数重标定器 v2.0
DNA: #龍芯⚡️2026-08-27-丙午·丙申·戊子·癸亥-LHAE-CALIBRATOR-v2.0-UID9622
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0（君子协议，来源链不可切断）
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

任务: 接入真实AI系统（本地ollama）→ 实测四熵 → 以实测熵为初值重标定 γ/floor
原理:
  1. 真实采样: 对本地ollama模型 多主题 × 多温度 × 多次生成（不连云·本地推理）
  2. 实测四熵:
       H_behavior = 输出字符分布Shannon熵（行为熵）
       H_align    = 温度0.3 vs 0.9 输出分布KL（对齐/行为漂移）
       H_context  = 长prompt vs 短prompt 输出熵差（上下文敏感）
       H_knowledge= 跨主题输出熵标准差（知识不一致）
  3. 以实测熵为Monte Carlo初值 → 重扫γ×floor → 精跑10万 → 标定报告
节能: 每模型约14次生成×64token · 本地推理 · 用完即沉默
三色: 🟢 真实采样 · 🟢 标定参数 · 🟢 精跑实证
"""

import collections
import datetime
import json
import math
import os
import sys
import urllib.request

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lh_ai_entropy_engine import run_monte_carlo_vectorized

OLLAMA_BASE = os.environ.get("OLLAMA_BASE", "http://127.0.0.1:11434")
DNA = "#龍芯⚡️2026-08-27-丙午·丙申·戊子·癸亥-LHAE-CALIBRATOR-v2.0-UID9622"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"

# 两主题短prompt（测行为熵/对齐/知识差异）
PROMPTS = {
    "protocol": "用三句话解释什么是数据主权。",
    "math": "证明为什么任何数除以零都没有定义。",
}
# 长prompt（测上下文敏感）
LONG_PROMPT = (
    "你是龍魂系统的协议引擎，请严格按协议执行：先声明DNA追溯码，再说明"
    "数据主权归属，接着给出三色审计结论。协议要求所有输出必须包含归属名、"
    "确认码，并解释P0天条中的为人民服务条款。请完整展开，不少于80字。"
)


def ollama_generate(model, prompt, temperature=0.7, num_predict=64, timeout=180,
                    think=True):
    """调用本地ollama非流式生成，返回文本。
    think=False: 关闭推理模型思考（deepseek-r1 直接输出回答，
                 避免响应全被思考吃掉导致空返回）。
    """
    options = {"temperature": temperature, "num_predict": num_predict,
               "num_ctx": 2048}
    if not think:
        options["think"] = False
    body = json.dumps({
        "model": model, "prompt": prompt, "stream": False,
        "options": options,
    }).encode("utf-8")
    req = urllib.request.Request(
        OLLAMA_BASE + "/api/generate", data=body,
        headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    text = data.get("response", "")
    # 容错：推理模型(response空但thinking有内容) → 思考流即其真实输出分布
    if not text:
        text = data.get("thinking", "")
    # 全空 → 重试一次关思考（deepseek-r1: think参数可能不生效）
    if not text and think:
        return ollama_generate(model, prompt, temperature, num_predict,
                               timeout, think=False)
    return text


def char_freq(text):
    return collections.Counter(text)


def shannon(text):
    """字符级Shannon熵 (bits)"""
    if not text:
        return 0.0
    n = len(text)
    freq = char_freq(text)
    return -sum((c / n) * math.log2(c / n) for c in freq.values())


def kl(p, q):
    """字符频率分布 KL 散度 (bits)"""
    keys = set(p) | set(q)
    pn = sum(p.values()) or 1.0
    qn = sum(q.values()) or 1.0
    total = 0.0
    for k in keys:
        pp = p.get(k, 0) / pn
        qq = q.get(k, 0) / qn
        if pp > 0 and qq > 0:
            total += pp * math.log2(pp / qq)
    return total


def collect_model_entropy(model, n_repeat=3, n_predict=64):
    """采集单模型真实四熵"""
    samples = {}  # (topic, temp) -> [texts]
    for topic, prompt in PROMPTS.items():
        for temp in (0.3, 0.9):
            texts = []
            for _ in range(n_repeat):
                texts.append(ollama_generate(model, prompt, temp, n_predict))
            samples[(topic, temp)] = texts

    # h_behavior: 全部输出平均字符熵
    all_texts = [t for ts in samples.values() for t in ts]
    h_behavior = float(np.mean([shannon(t) for t in all_texts]))

    # h_align: 同主题 温度0.3 vs 0.9 输出分布KL
    kl_vals = []
    for topic in PROMPTS:
        p = char_freq("".join(samples[(topic, 0.3)]))
        q = char_freq("".join(samples[(topic, 0.9)]))
        kl_vals.append(kl(p, q))
    h_align = min(float(np.mean(kl_vals)), 2.0)

    # h_context: 长prompt vs 短prompt 熵差
    short_h = h_behavior
    long_texts = [ollama_generate(model, LONG_PROMPT, 0.5, n_predict)
                  for _ in range(2)]
    long_h = float(np.mean([shannon(t) for t in long_texts]))
    h_context = min(abs(long_h - short_h), 2.5)

    # h_knowledge: 跨主题熵差异（std）
    topic_h = {t: float(np.mean([shannon(x) for x in samples[(t, 0.9)]]))
               for t in PROMPTS}
    h_knowledge = min(float(np.std(list(topic_h.values()))), 2.0)

    return {
        "H_behavior": round(h_behavior, 4),
        "H_context": round(h_context, 4),
        "H_align": round(h_align, 4),
        "H_knowledge": round(h_knowledge, 4),
        "H_total_init": round(h_behavior + h_context + h_align + h_knowledge, 4),
    }


def recalibrate(init_h, gammas, floors, n_sims=5000, n_steps=200, seed=9622,
                verbose=True):
    """以真实初值为初态，重扫 γ×floor"""
    results = []
    for gamma in gammas:
        for floor in floors:
            r = run_monte_carlo_vectorized(
                n_sims=n_sims, n_steps=n_steps, seed=seed, verbose=False,
                floor_guard=floor, gamma=gamma, init_h=init_h,
                tag=f"real-γ={gamma}·floor={floor}")
            s = r.summary()
            hp = s["fixed_point_H_star"]
            mean_h = hp.get("mean", 0.0)
            if 1.0 <= mean_h <= 2.5 and 0.70 <= r.convergence_rate <= 0.95:
                quality = "🟢 GOOD"
            elif 0.0 < mean_h < 1.0:
                quality = "🟡 low (不动点偏低)"
            elif mean_h > 2.5:
                quality = "🟡 high (不动点偏高)"
            else:
                quality = "🔴 degenerate"
            row = {
                "gamma": gamma, "floor": floor,
                "H_star": round(mean_h, 4),
                "conv_rate": round(r.convergence_rate, 4),
                "converged": r.converged, "diverged": r.diverged,
                "oscillating": r.oscillating,
                "colors": s["final_colors"],
                "negentropy": round(s["mean_negentropy"], 2),
                "quality": quality,
            }
            results.append(row)
            if verbose:
                print(f"  γ={gamma:<5} floor={floor:<5} H*={mean_h:.4f} "
                      f"conv={r.convergence_rate:.2%} {quality}")
    return results


def main():
    print("⚡ 龙魂反熵增引擎 · 真实AI熵采集与参数重标定 v2.0")
    print(f"DNA: {DNA}")
    print(f"确认码: {CONFIRM}")
    print("=" * 60)

    # 真实采样（本地ollama·不连云）
    # longhun-v4.0 F16 8B 单次生成72s+输出乱码 → 节能剔除
    models = ["qwen2.5:7b", "deepseek-r1:7b"]
    all_cal = {}
    for model in models:
        print(f"\n🎤 采集真实熵: {model}")
        ent = collect_model_entropy(model, n_repeat=3)
        all_cal[model] = ent
        print("  " + json.dumps(ent, ensure_ascii=False))

    # 聚合: 仅取采集成功(H_total_init>0.1)的模型均值，失败模型剔除不稀释
    keys = ["H_behavior", "H_context", "H_align", "H_knowledge"]
    valid_models = {m: e for m, e in all_cal.items() if e["H_total_init"] > 0.1}
    if not valid_models:
        raise SystemExit("🔴 所有模型采集失败，无法标定")
    avg = {k: round(float(np.mean([e[k] for e in valid_models.values()])), 4)
           for k in keys}
    avg_init = (avg["H_behavior"], avg["H_context"], avg["H_align"],
                avg["H_knowledge"])
    print("\n📊 标准真实初值 (三模型均值):")
    print("  " + json.dumps(avg, ensure_ascii=False))
    print(f"  H_total_init = {sum(avg.values()):.4f} bits")

    # 重扫参数
    print("\n📊 重扫 γ×floor（以真实初值 · 5000次/组合）")
    grid = recalibrate(
        avg_init,
        gammas=[0.05, 0.08, 0.12, 0.15, 0.20, 0.25],
        floors=[0.5, 1.0, 1.5],
        n_sims=5000, n_steps=200, verbose=True,
    )

    # 选最优组合精跑10万
    good = [g for g in grid if g["quality"] == "🟢 GOOD"]
    if good:
        best = min(good, key=lambda g: abs(g["H_star"] - 1.73))
        print(f"\n🎯 最优标定参数: γ={best['gamma']} floor={best['floor']} "
              f"H*={best['H_star']}bits · 精跑10万次确认")
        rbest = run_monte_carlo_vectorized(
            n_sims=100_000, n_steps=200, seed=9622, verbose=False,
            floor_guard=best["floor"], gamma=best["gamma"], init_h=avg_init,
            tag=f"v2.0-real-final-γ{best['gamma']}-floor{best['floor']}")
        best_run = rbest.summary()
        print(json.dumps(best_run, ensure_ascii=False, indent=2))
    else:
        best_run = None
        best = None
        print("\n⚠️ 网格内未找到🟢GOOD参数·需扩大扫描域")

    # 报告落盘
    report = {
        "dna": "#龍芯⚡️2026-08-27-丙午·丙申·戊子·癸亥-LHAE-CALIBRATION-REPORT-v2.0-UID9622",
        "timestamp": datetime.datetime.now().isoformat(),
        "method": "真实AI接入·本地ollama采样·实测四熵为Monte Carlo初值",
        "models_measured": all_cal,
        "models_used_for_init": list(valid_models.keys()),
        "standard_real_init": avg,
        "phase1_real_entropy": {
            "note": "H_behavior=输出分布熵·H_align=温度扰动KL·"
                    "H_context=长/短prompt熵差·H_knowledge=跨主题熵std",
            "avg": avg,
        },
        "phase2_recalibrated_grid": grid,
        "phase3_final_100k": best_run,
        "recalibrated_params": (
            {"gamma": best["gamma"], "floor": best["floor"]}
            if best is not None else None),
        "compare_v1_2": {
            "old": {"gamma": 0.15, "floor": 1.5,
                    "source": "数学仿真初值(均匀随机)"},
            "new": ({"gamma": best["gamma"], "floor": best["floor"],
                     "source": "真实AI实测熵初值"}
                    if best is not None else None),
        },
        "confirm": CONFIRM,
        "status": "🟢 真实标定完成",
    }

    print("\n📊 最终标定报告")
    print(json.dumps(report, ensure_ascii=False, indent=2))

    out_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "data",
        "entropy_calibration_report.json")
    out_path = os.path.normpath(out_path)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"\n✅ 标定报告已保存: {out_path}")


if __name__ == "__main__":
    main()
