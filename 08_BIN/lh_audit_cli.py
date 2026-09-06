#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丁酉·癸未·未时·䷛大过-LH-AUDIT-CLI-v1.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 修订注记: 2026-09-06 v1.0 优化补全落盘（防空壳：先勘察既有 lh_hallucination_metrics.py v2.0 再合并增强·避免重复造轮子）
"""
龍魂·三色审计命令行工具 v1.0（社区便携版）
DNA: #龍芯⚡️丙午·丁酉·癸未·未时·䷛大过-LH-AUDIT-CLI-v1.0-UID9622

配套 DeepSeek-V3 Issue #1591（UID9622 龍魂审计数据集基准帖）的独立可运行 CLI。
别人拿过去就能用：一份模型响应 JSON 日志 → 三色审计报告 → 耻辱墙标记（可选）。

公式同秤声明（防空壳注记·判据④）：
- 数学公式与 08_BIN/lh_hallucination_metrics.py v2.0（lh halluc 引擎）严格同秤：
  factual 混淆 F1 + extract TokenF1 + reason EM + 五维度 μ + ECE + H 公式 + 🟢≥0.80/🟡≥0.50/🔴<0.50
- H = 无幻觉度（质量分），越高越好；ECE 0=完美校准，越大越差（单独汇报）
- 本地双跑同数据须同结果；差异 = 某侧被改，先查不盲信
- 默认 TokenF1 用字符集合 Dice（与 v2.0 同秤）；--mode multiset 提供计数版精确算法（可选）

用法:
    python3 lh_audit_cli.py audit --input sample.json [--output report.json] [--wall]
    python3 lh_audit_cli.py batch --dir ./audit_logs/ [--wall]
    python3 lh_audit_cli.py verify --report report.json
    python3 lh_audit_cli.py selftest
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

# ============================================================
# 常量区（与三色审计框架严格对齐·焊死）
# ============================================================
GREEN_THRESHOLD = 0.80   # H ≥ 0.80 → 🟢 PASS
YELLOW_THRESHOLD = 0.50  # 0.50 ≤ H < 0.80 → 🟡 REVIEW
# H < 0.50 → 🔴 REJECT

WEIGHTS = {"factual": 0.50, "faithfulness": 0.50}
DIMENSIONS = ["人文科学", "社会科学", "自然科学", "应用科学", "形式科学"]
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
ENGINE_DNA = "#龍芯⚡️丙午·丁酉·癸未·未时·䷛大过-LH-AUDIT-CLI-v1.0-UID9622"
SHAME_WALL_DIR = Path.home() / ".longhun" / "shame_wall"


# ============================================================
# 数学核心（与 lh_hallucination_metrics.py v2.0 同秤·每步可复算）
# ============================================================

def calc_confusion_matrix(pred: list, gold: list) -> dict:
    """混淆矩阵 → F1。断言长度一致 + 0/1 合法。"""
    assert len(pred) == len(gold), f"factual 长度不一致: pred={len(pred)} gold={len(gold)}"
    assert all(v in (0, 1) for v in pred), "factual_pred 必须为 0/1"
    assert all(v in (0, 1) for v in gold), "factual_gold 必须为 0/1"
    tp = sum(p == 1 and g == 1 for p, g in zip(pred, gold))
    fp = sum(p == 1 and g == 0 for p, g in zip(pred, gold))
    fn = sum(p == 0 and g == 1 for p, g in zip(pred, gold))
    tn = sum(p == 0 and g == 0 for p, g in zip(pred, gold))
    p = tp / (tp + fp) if tp + fp > 0 else 0.0
    r = tp / (tp + fn) if tp + fn > 0 else 0.0
    f1 = 2 * p * r / (p + r) if p + r > 0 else 0.0
    return {
        "TP": tp, "FP": fp, "FN": fn, "TN": tn, "N": len(pred),
        "precision": round(p, 6), "recall": round(r, 6),
        "f1": round(f1, 6),
        "_formula": f"P={tp}/{tp + fp}=...  R=...  F1=2PR/(P+R)={f1:.6f}",
    }


def _tokenize_set(s: str) -> list:
    return [c for c in s if c.strip()]


def calc_token_f1(pred_list: list, gold_list: list, mode: str = "set") -> dict:
    """
    TokenF1（信息抽取·字符级）。
    mode=set      → 字符集合 Dice（与 v2.0 同秤·默认）
    mode=multiset → Counter 计数版（精确，重复字符不塌缩）
    约定: 双方均为空 → 1.0；交集为空 → 0.0
    """
    assert len(pred_list) == len(gold_list), "extract 列表长度不一致"
    scores = []
    for pred, gold in zip(pred_list, gold_list):
        if mode == "multiset":
            p, g = Counter(_tokenize_set(pred)), Counter(_tokenize_set(gold))
            inter = sum((p & g).values())
            denom = sum(p.values()) + sum(g.values())
        else:
            p_set, g_set = set(_tokenize_set(pred)), set(_tokenize_set(gold))
            inter, denom = len(p_set & g_set), len(p_set) + len(g_set)
        f1 = 1.0 if denom == 0 else (2 * inter / denom if inter > 0 else 0.0)
        scores.append(round(f1, 6))
    avg = sum(scores) / len(scores) if scores else 0.0
    return {"avg_token_f1": round(avg, 6), "scores": scores, "n": len(scores),
            "_formula": f"TokenF1=2×|pred∩gold|/(|pred|+|gold|) mode={mode}"}


def calc_em(pred_list: list, gold_list: list) -> dict:
    """EM 精确匹配率（知识推理）。附 PM 部分包含。"""
    assert len(pred_list) == len(gold_list), "reason 列表长度不一致"
    n = len(pred_list)
    em_count = sum(p.strip() == g.strip() for p, g in zip(pred_list, gold_list))
    pm_count = sum(bool(g.strip()) and g.strip() in p for p, g in zip(pred_list, gold_list))
    return {"em": round(em_count / n, 6) if n else 0.0,
            "pm": round(pm_count / n, 6) if n else 0.0,
            "em_count": em_count, "pm_count": pm_count, "n": n,
            "_formula": f"EM={em_count}/{n}，PM={pm_count}/{n}"}


def calc_ece(confidence: list, correctness: list, bins: int = 10) -> dict:
    """ECE 期望校准误差。0=完美，越大越差。"""
    n = len(confidence)
    assert n == len(correctness) > 0, "confidence/correctness 长度不一致或为空"
    assert all(0 <= c <= 1 for c in confidence), "置信度须在 [0,1]"
    bin_list: list = [[] for _ in range(bins)]
    for c, a in zip(confidence, correctness):
        idx = min(int(c * bins), bins - 1)
        bin_list[idx].append((c, a))
    ece, details = 0.0, []
    for i, b in enumerate(bin_list):
        if not b:
            continue
        avg_c = sum(x[0] for x in b) / len(b)
        avg_a = sum(x[1] for x in b) / len(b)
        contrib = (len(b) / n) * abs(avg_a - avg_c)
        ece += contrib
        details.append({"bin": f"[{i / bins:.1f},{(i + 1) / bins:.1f})", "n": len(b),
                        "avg_conf": round(avg_c, 4), "avg_acc": round(avg_a, 4),
                        "gap": round(abs(avg_a - avg_c), 4), "contrib": round(contrib, 6)})
    return {"ece": round(ece, 6), "details": details,
            "_formula": "ECE=Σ(|Bm|/n)×|acc(Bm)-conf(Bm)|"}


def calc_h_index(factual_f1: float, extract_f1: float, reason_em: float,
                 dim_scores: dict) -> dict:
    """
    H 主裁判公式（与 v2.0 同秤）:
        faithfulness = (extract_f1 + reason_em) / 2
        h_base = 0.5×factual_f1 + 0.5×faithfulness
        mu_dim = mean(dim_scores);  delta = (mu_dim − 0.5) × 0.2
        H = clip(h_base + delta, 0, 1)
    """
    assert all(0 <= x <= 1 for x in (factual_f1, extract_f1, reason_em)), "分项超范围"
    faithfulness = (extract_f1 + reason_em) / 2
    h_base = WEIGHTS["factual"] * factual_f1 + WEIGHTS["faithfulness"] * faithfulness
    mu_dim = sum(dim_scores.values()) / len(dim_scores) if dim_scores else 0.5
    delta = (mu_dim - 0.5) * 0.2
    h = max(0.0, min(1.0, h_base + delta))
    if h >= GREEN_THRESHOLD:
        color, action = "🟢", "PASS"
    elif h >= YELLOW_THRESHOLD:
        color, action = "🟡", "REVIEW"
    else:
        color, action = "🔴", "REJECT"
    return {
        "h_index": round(h, 6), "color": color, "action": action,
        "components": {"factual_f1": round(factual_f1, 6),
                       "extract_f1": round(extract_f1, 6),
                       "reason_em": round(reason_em, 6),
                       "faithfulness": round(faithfulness, 6),
                       "mu_dim": round(mu_dim, 6), "delta": round(delta, 6),
                       "h_base": round(h_base, 6)},
        "_formula": (f"H=clip(0.5×{factual_f1:.4f}+0.5×({extract_f1:.4f}"
                     f"+{reason_em:.4f})/2+{delta:.4f},0,1)={h:.6f}"),
    }


class MathValidator:
    """独立复算器（防主函数算错·防空壳）"""

    @staticmethod
    def verify_h(factual_f1: float, extract_f1: float, reason_em: float, mu_dim: float) -> float:
        faithfulness = (extract_f1 + reason_em) / 2
        h_base = 0.5 * factual_f1 + 0.5 * faithfulness
        delta = (mu_dim - 0.5) * 0.2
        return round(max(0.0, min(1.0, h_base + delta)), 6)

    @staticmethod
    def validate_report(report: dict) -> bool:
        """从原始分项独立复算 H 与 report.h_index 比对。"""
        factual_f1 = report["factual"]["f1"]
        extract_f1 = report["extraction"]["avg_token_f1"]
        reason_em = report["reasoning"]["em"]
        mu_dim = report["h_index"]["components"]["mu_dim"]
        expected = MathValidator.verify_h(factual_f1, extract_f1, reason_em, mu_dim)
        actual = report["h_index"]["h_index"]
        ok = abs(expected - actual) < 1e-5
        print(f"  复算核验: 期望H={expected:.6f} 实际H={actual:.6f} "
              f"diff={abs(expected - actual):.2e}  {'✅ 通过' if ok else '❌ 不通过'}")
        return ok

    @staticmethod
    def rehash_report(report: dict) -> str:
        """对结果字段重算报告哈希（剔除时间戳/DNA/confirm/hash 自身 → 同一输入可复现）。"""
        payload = {
            "factual": report["factual"],
            "extraction": report["extraction"],
            "reasoning": report["reasoning"],
            "dimensions": report["dimensions"],
            "ece": report.get("ece"),
            "h_index": report["h_index"],
        }
        digest = hashlib.sha256(json.dumps(payload, sort_keys=True,
                                           ensure_ascii=False).encode()).hexdigest()
        return digest[:16].upper()


# ============================================================
# 完整审计
# ============================================================

def run_full_audit(data: dict, token_mode: str = "set") -> dict:
    """执行完整三色审计（对齐 v2.0 run() 字段命名·同秤）
    防空壳: factual_pred/gold 必填（H 依赖事实性分量·缺则拒算防误导）；
    extract/reason/dim/conf 可选（按输入能力降级但必在报告中注明）。"""
    missing = [k for k in ("factual_pred", "factual_gold") if k not in data]
    if missing:
        raise ValueError(f"缺必填字段: {missing}（须为输入数据格式·非审计报告格式）")
    factual = calc_confusion_matrix(data.get("factual_pred", []), data.get("factual_gold", []))
    extraction = calc_token_f1(data.get("extract_pred", []), data.get("extract_gold", []),
                               mode=token_mode)
    reasoning = calc_em(data.get("reason_pred", []), data.get("reason_gold", []))
    dims_raw = data.get("dim_data", {})
    dim_scores = {}
    if isinstance(dims_raw, dict) and dims_raw:
        for dim, pair in dims_raw.items():
            if isinstance(pair, (list, tuple)) and len(pair) == 2:
                dim_scores[str(dim)] = calc_confusion_matrix(pair[0], pair[1])["f1"]
            else:
                raise ValueError(f"dim_data[{dim}] 须为 [pred_list, gold_list] 二元组")
    else:
        for dim in DIMENSIONS:  # 默认用事实性 F1 填充（与 v2.0 一致）
            dim_scores[dim] = factual["f1"]

    ece_result = None
    if data.get("confidence") and data.get("correctness"):
        ece_result = calc_ece(data["confidence"], data["correctness"])

    h_result = calc_h_index(factual["f1"], extraction["avg_token_f1"], reasoning["em"],
                            dim_scores)

    ts = datetime.now().isoformat()
    digest = hashlib.sha256(json.dumps({"h": h_result["h_index"], "n": len(data.get("factual_gold", []))},
                                       sort_keys=True).encode()).hexdigest()[:8].upper()
    run_dna = f"#龍芯⚡️丙午·丁酉·癸未·未时·䷛大过-LH-AUDIT-RUN-{digest}-UID9622"

    report = {
        "engine": "lh-audit-cli v1.0（社区便携版·同秤 lh halluc v2.0）",
        "engine_dna": ENGINE_DNA,
        "run_dna": run_dna,
        "timestamp": ts,
        "confirm": CONFIRM,
        "token_mode": token_mode,
        "factual": factual,
        "extraction": extraction,
        "reasoning": reasoning,
        "dimensions": dim_scores,
        "ece": ece_result,
        "h_index": h_result,
        "color": h_result["color"],
        "action": h_result["action"],
        "report_hash": MathValidator.rehash_report({
            "factual": factual, "extraction": extraction, "reasoning": reasoning,
            "dimensions": dim_scores, "ece": ece_result, "h_index": h_result,
        }),
    }
    report["summary"] = f"{report['color']}  {report['action']}  H={h_result['h_index']:.4f}"
    return report


# ============================================================
# 耻辱墙标记（可选·--wall·仅 🔴 记录·append-only JSONL）
# ============================================================

def mark_shame_wall(report: dict, source: str = "") -> None:
    """🔴 REJECT 时可选记录审计耻辱墙（append-only JSONL）。
    注: 正式剽窃公示走 lh judge（shame_wall.db）；本处为幻觉审计拒签记录，分区存放不混库。"""
    try:
        SHAME_WALL_DIR.mkdir(parents=True, exist_ok=True)
        path = SHAME_WALL_DIR / "audit_rejects.jsonl"
        entry = {
            "ts": report["timestamp"], "source": source,
            "run_dna": report["run_dna"], "h": report["h_index"]["h_index"],
            "color": report["color"], "action": report["action"],
            "summary": report["summary"], "engine_dna": report["engine_dna"],
        }
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        print(f"🔴 已标记审计耻辱墙: {path}")
    except OSError as e:
        print(f"⚠️ 耻辱墙写入失败（不影响报告）: {e}")


# ============================================================
# 报告打印
# ============================================================

def print_report(report: dict) -> None:
    h = report["h_index"]
    print("\n" + "=" * 62)
    print("🐉 龍魂·三色审计报告  (lh-audit-cli v1.0)")
    print("=" * 62)
    print(f"DNA: {report['run_dna']}")
    print(f"引擎: {report['engine']}")
    print(f"时间: {report['timestamp']}")
    print(f"确认码: {report['confirm']}")
    print(f"报告哈希: {report['report_hash']}（可 verify 复算比对）")
    print("-" * 62)
    print(f"幻觉综合指数 H = {h['h_index']:.4f}  {h['color']}  {h['action']}")
    print(f"   事实性 F1:        {report['factual']['f1']:.4f}")
    print(f"   信息抽取 TokenF1: {report['extraction']['avg_token_f1']:.4f}"
          f"  [{report['token_mode']}]")
    print(f"   知识推理 EM:      {report['reasoning']['em']:.4f}")
    if report.get("ece"):
        print(f"   置信度校准 ECE:   {report['ece']['ece']:.4f}"
              f"  (0=完美·越大越差·与H方向相反)")
    if report["dimensions"]:
        print("   五维度 F1:")
        for d, s in report["dimensions"].items():
            print(f"     {d}: {s:.4f}")
    print("=" * 62 + "\n")


# ============================================================
# 自测（seed=9622 端点断言·防空壳：跑过才算数）
# ============================================================

def selftest() -> int:
    print("🐉 lh-audit-cli 自测（seed=9622·端点断言）")
    ok = True

    # 端点1: 全对 → H 必 = 1.0 🟢（防空壳: 公式退化检查）
    perf = run_full_audit({
        "factual_pred": [0, 1, 0, 1], "factual_gold": [0, 1, 0, 1],
        "extract_pred": ["北京是首都", "量子纠缠是物理现象"],
        "extract_gold": ["北京是首都", "量子纠缠是物理现象"],
        "reason_pred": ["正确答案A", "是的"], "reason_gold": ["正确答案A", "是的"],
        "dim_data": {"人文科学": [[0, 1], [0, 1]], "自然科学": [[1, 0], [1, 0]]},
    })
    ok &= abs(perf["h_index"]["h_index"] - 1.0) < 1e-6
    print(f"  全对端点: H={perf['h_index']['h_index']:.4f} {perf['color']}"
          f"  {'✅' if abs(perf['h_index']['h_index'] - 1.0) < 1e-6 else '❌'}")

    # 端点2: 全错 → H 必 = 0.0 🔴
    fail = run_full_audit({
        "factual_pred": [1, 0, 1, 0], "factual_gold": [0, 1, 0, 1],
        "extract_pred": ["不存在甲"], "extract_gold": ["完全不同的乙丙丁"],
        "reason_pred": ["错误答案"], "reason_gold": ["正确答案"],
        "dim_data": {"人文科学": [[1], [0]], "自然科学": [[0], [1]]},
    })
    ok &= abs(fail["h_index"]["h_index"] - 0.0) < 1e-6
    print(f"  全错端点: H={fail['h_index']['h_index']:.4f} {fail['color']}"
          f"  {'✅' if abs(fail['h_index']['h_index'] - 0.0) < 1e-6 else '❌'}")

    # 复算器一致性（混合构造）
    mixed = run_full_audit({
        "factual_pred": [0, 1, 0, 1], "factual_gold": [0, 1, 0, 0],
        "extract_pred": ["北京是首都", "量子纠缠"], "extract_gold": ["北京是首都", "量子纠缠是物理现象"],
        "reason_pred": ["正确答案A", "是的"], "reason_gold": ["正确答案A", "是的"],
        "dim_data": {"人文科学": [[0, 1, 0, 1], [0, 1, 0, 1]], "自然科学": [[1, 0, 1, 0], [1, 0, 1, 0]]},
        "confidence": [0.9, 0.7, 0.5, 0.8], "correctness": [1.0, 0.0, 1.0, 1.0],
    })
    ok &= MathValidator.validate_report(mixed)
    # verify 抓篡改（独立判据）
    forged = json.loads(json.dumps(mixed))
    forged["h_index"]["h_index"] = round(mixed["h_index"]["h_index"] + 0.05, 6)
    tamper_ok = MathValidator.rehash_report(forged) != forged["report_hash"]
    print(f"  篡改检测: hash 变化 {'✅ 抓出' if tamper_ok else '❌ 漏检'}")
    ok &= tamper_ok
    print(f"\n  结果: {'✅ 全部通过' if ok else '❌ 有失败'}")
    return 0 if ok else 1


# ============================================================
# CLI
# ============================================================

def _load_json(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert isinstance(data, dict), "JSON 顶层须为对象"
    return data


def cmd_audit(args) -> int:
    data = _load_json(args.input)
    report = run_full_audit(data, token_mode=args.mode)
    print_report(report)
    if args.wall and report["color"] == "🔴":
        mark_shame_wall(report, source=args.input)
    if args.output:
        Path(args.output).write_text(json.dumps(report, ensure_ascii=False, indent=2),
                                     encoding="utf-8")
        print(f"✅ 报告已保存: {args.output}")
    return 0 if report["color"] != "🔴" else 1


def cmd_batch(args) -> int:
    path = Path(args.dir)
    if not path.is_dir():
        print(f"❌ 目录不存在: {args.dir}")
        return 2
    files = [f for f in sorted(path.glob("*.json")) if not f.name.startswith("_")]
    if not files:
        print("📭 目录下无输入 .json 文件（跳过 _ 前缀自身产物）")
        return 0
    results, errors, color_count = [], [], {"🟢": 0, "🟡": 0, "🔴": 0}
    for fp in files:
        try:
            data = _load_json(str(fp))
            report = run_full_audit(data, token_mode=args.mode)
            results.append(report)
            color_count[report["color"]] += 1
            print(f"✅ {fp.name}: {report['summary']}")
            if args.wall and report["color"] == "🔴":
                mark_shame_wall(report, source=str(fp))
        except Exception as e:  # noqa: BLE001
            errors.append({"file": fp.name, "error": str(e)})
            print(f"❌ {fp.name}: {e}")
    summary_file = path / "_batch_summary.json"
    summary_file.write_text(
        json.dumps({"n": len(results), "color_count": color_count, "errors": errors,
                    "reports": results}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n📊 批量审计: 成功 {len(results)} · 失败 {len(errors)} · "
          f"🟢{color_count['🟢']} 🟡{color_count['🟡']} 🔴{color_count['🔴']}")
    print(f"   摘要已保存: {summary_file}")
    return 1 if errors else 0


def cmd_verify(args) -> int:
    """真验证（防空壳优化）: ①重算报告哈希比对 ②独立复算 H"""
    report = _load_json(args.report)
    h = report.get("h_index", {})
    print(f"🔍 报告验证: {args.report}")
    print(f"   DNA: {report.get('run_dna', 'N/A')}")
    print(f"   H = {h.get('h_index', 'N/A')}  {report.get('color', 'N/A')}")
    ok = True

    stored_hash = report.get("report_hash")
    if not stored_hash:
        print("   ❌ 缺 report_hash 字段（报告不完整或被截断）")
        ok = False
    else:
        recomputed = MathValidator.rehash_report(report)
        match = recomputed == stored_hash.upper()
        ok &= match
        print(f"   哈希复算: 存={stored_hash.upper()} 算={recomputed}"
              f"  {'✅ 一致·未被篡改' if match else '❌ 不一致·报告被改过'}")

    math_ok = MathValidator.validate_report(report)
    ok &= math_ok
    print(f"\n   结果: {'✅ 验证通过' if ok else '❌ 验证失败'}")
    return 0 if ok else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="龍魂·三色审计命令行工具 v1.0")
    parser.add_argument("--mode", choices=["set", "multiset"], default="set",
                        help="TokenF1 算法: set=与 lh halluc v2.0 同秤(默认) / multiset=计数精确版")
    sub = parser.add_subparsers(dest="command", required=True)

    p_audit = sub.add_parser("audit", help="单次审计")
    p_audit.add_argument("--input", required=True, help="输入 JSON 文件路径")
    p_audit.add_argument("--output", help="输出报告 JSON 路径（可选）")
    p_audit.add_argument("--wall", action="store_true", help="🔴 拒签时标记审计耻辱墙（可选）")
    p_audit.set_defaults(func=cmd_audit)

    p_batch = sub.add_parser("batch", help="批量审计目录下所有 JSON")
    p_batch.add_argument("--dir", required=True, help="审计日志目录")
    p_batch.add_argument("--wall", action="store_true", help="🔴 拒签时标记审计耻辱墙（可选）")
    p_batch.set_defaults(func=cmd_batch)

    p_verify = sub.add_parser("verify", help="验证报告哈希 + H 复算")
    p_verify.add_argument("--report", required=True, help="报告 JSON 路径")
    p_verify.set_defaults(func=cmd_verify)

    p_self = sub.add_parser("selftest", help="端点断言自测（seed=9622）")
    p_self.set_defaults(func=lambda a: selftest())

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
