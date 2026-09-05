#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丁酉·壬午·子时·䷛大过-HALLUCINATION-METRICS-v2.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 修订注记: 2026-09-05 落地审计修正（外部「融合稿」→ 系统引擎）· 修复项见模块 docstring「落地审计裁决」
"""
龍魂·大模型幻觉量化评估引擎 v2.0（融合版·落地修正）
DNA: #龍芯⚡️丙午·丁酉·壬午·子时·䷛大过-HALLUCINATION-METRICS-v2.0-UID9622

融合自：简洁架构 + Notion数学验证器 + ECE校准 + 五维度显式支持

设计原则：
1. 纯Python·零外部依赖·每步公式可审计
2. 简洁架构（易读易维护）+ 数学验证器（防算错）
3. 三色审计 + DNA追溯 + 确认码焊死
4. _公式字段可直接粘贴复算
5. 内置验收测试，开箱即验

落地审计裁决（2026-09-05 · 判据④实机原则）：
| # | 外部稿问题 | 落地裁决 |
|:---|:---|:---|
| 1 | 文件头伪签（DNA日期式无归属名） | 四行规范头 · v∞干支DNA · 归属名实名焊死 |
| 2 | MathValidator 伪独立（把已合并faithfulness传两次） | 真独立：从 extraction/reasoning 原值复算 faithfulness 再推 H |
| 3 | h_index.components 缺原始分项 | 补 extract_f1/reason_em · 公式链端到端可复算 |
| 4 | acceptance_test 冗余切片 [:51]/[:52]（恰为全量） | 去除 · 精确长度注释 |
| 5 | 文件名含「融合版」中文 | 系统惯例 lh_ 英文蛇形：lh_hallucination_metrics.py |
| 6 | export_jsonl 默认写当前目录（污染工作区） | 默认路径收敛 _work/ · 不入 git |
| 7 | 语义方向未言明 | 明示：H=无幻觉度(质量分)，越高越好；🟢≥0.80 / 🟡≥0.50 / 🔴<0.50 |

指标语义（防误读）：
- factual_f1 / extract TokenF1 / reason EM / 各维度 F1 越高=幻觉越少
- H = clip(h_base + (μ_dim-0.5)×0.2, 0, 1) → 🟢PASS / 🟡REVIEW / 🔴REJECT
- ECE：置信度校准，0=完美，越大越差（与 H 方向相反，单独汇报）
"""

import json
import hashlib
import random
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# ============================================================
# 一、常量区（焊死·不可篡改）
# ============================================================

GREEN_THRESHOLD = 0.80   # H ≥ 0.80 → 🟢
YELLOW_THRESHOLD = 0.50  # 0.50 ≤ H < 0.80 → 🟡
# H < 0.50 → 🔴

WEIGHTS = {
    "factual": 0.50,
    "faithfulness": 0.50,
}

DIMENSIONS = ["人文科学", "社会科学", "自然科学", "应用科学", "形式科学"]

DNA_PREFIX = "#龍芯⚡️"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
ENGINE_DNA = "#龍芯⚡️丙午·丁酉·壬午·子时·䷛大过-HALLUCINATION-METRICS-v2.0-UID9622"

# ============================================================
# 二、数学核心函数（每个函数附验证公式）
# ============================================================

def calc_confusion_matrix(pred: List[int], gold: List[int]) -> Dict:
    """
    计算混淆矩阵：TP/FP/FN/TN → 精确率P/召回率R/F1/准确率Acc

    公式：
        P = TP / (TP + FP)
        R = TP / (TP + FN)
        F1 = 2 * P * R / (P + R)
        Acc = (TP + TN) / N
    """
    assert len(pred) == len(gold), f"长度不一致: pred={len(pred)}, gold={len(gold)}"
    assert all(v in (0, 1) for v in pred), "预测值必须为0或1"
    assert all(v in (0, 1) for v in gold), "标签值必须为0或1"

    TP = sum(p == 1 and g == 1 for p, g in zip(pred, gold))
    FP = sum(p == 1 and g == 0 for p, g in zip(pred, gold))
    FN = sum(p == 0 and g == 1 for p, g in zip(pred, gold))
    TN = sum(p == 0 and g == 0 for p, g in zip(pred, gold))
    N = len(pred)

    P = TP / (TP + FP) if TP + FP > 0 else 0.0
    R = TP / (TP + FN) if TP + FN > 0 else 0.0
    F1 = 2 * P * R / (P + R) if P + R > 0 else 0.0
    Acc = (TP + TN) / N

    return {
        "TP": TP, "FP": FP, "FN": FN, "TN": TN, "N": N,
        "precision": round(P, 6),
        "recall": round(R, 6),
        "f1": round(F1, 6),
        "accuracy": round(Acc, 6),
        "_formula": f"P={TP}/({TP}+{FP})={P:.6f}  R={TP}/({TP}+{FN})={R:.6f}  F1=2×P×R/(P+R)={F1:.6f}",
    }


def calc_token_f1(pred_list: List[str], gold_list: List[str]) -> Dict:
    """
    计算Token级F1（信息抽取题专用 · 字符级集合 Dice）

    公式：
        TokenF1 = 2 * |pred ∩ gold| / (|pred| + |gold|)
        约定: 双方均为空 → 1.0（视为相等）；交集为空 → 0.0
        AvgTokenF1 = sum(TokenF1) / N
    """
    assert len(pred_list) == len(gold_list), "列表长度不一致"

    def tokenize(s: str) -> List[str]:
        return [c for c in s if c.strip()]

    scores = []
    for pred, gold in zip(pred_list, gold_list):
        p_set = set(tokenize(pred))
        g_set = set(tokenize(gold))
        inter = len(p_set & g_set)
        denom = len(p_set) + len(g_set)
        f1 = 1.0 if denom == 0 else (2 * inter / denom if inter > 0 else 0.0)
        scores.append(round(f1, 6))

    avg = sum(scores) / len(scores)
    return {
        "avg_token_f1": round(avg, 6),
        "scores": scores,
        "n": len(scores),
        "_formula": "TokenF1=2×|pred∩gold|/(|pred|+|gold|)",
    }


def calc_em(pred_list: List[str], gold_list: List[str]) -> Dict:
    """
    计算精确匹配率（知识推理题专用）

    公式：
        EM = 精确匹配数 / N
        PM = 部分包含数 / N
    """
    assert len(pred_list) == len(gold_list), "列表长度不一致"
    N = len(pred_list)
    em_count = sum(p.strip() == g.strip() for p, g in zip(pred_list, gold_list))
    pm_count = sum(g.strip() in p for p, g in zip(pred_list, gold_list))
    return {
        "em": round(em_count / N, 6),
        "pm": round(pm_count / N, 6),
        "em_count": em_count,
        "pm_count": pm_count,
        "n": N,
        "_formula": f"EM={em_count}/{N}，PM={pm_count}/{N}",
    }


def calc_ece(confidence: List[float], correctness: List[float], bins: int = 10) -> Dict:
    """
    计算期望校准误差 ECE

    公式：
        ECE = Σ_m (|B_m| / n) × |acc(B_m) - conf(B_m)|
        0 = 完美校准，越大越差
    """
    n = len(confidence)
    assert n == len(correctness) > 0, "列表长度不一致或为空"
    assert all(0 <= c <= 1 for c in confidence), "置信度须在[0,1]"

    bin_list = [[] for _ in range(bins)]
    for c, a in zip(confidence, correctness):
        idx = min(int(c * bins), bins - 1)
        bin_list[idx].append((c, a))

    ece = 0.0
    details = []
    for i, b in enumerate(bin_list):
        if not b:
            continue
        avg_c = sum(x[0] for x in b) / len(b)
        avg_a = sum(x[1] for x in b) / len(b)
        contrib = (len(b) / n) * abs(avg_a - avg_c)
        ece += contrib
        details.append({
            "bin": f"[{i/bins:.1f},{(i+1)/bins:.1f})",
            "n": len(b),
            "avg_conf": round(avg_c, 4),
            "avg_acc": round(avg_a, 4),
            "gap": round(abs(avg_a - avg_c), 4),
            "contrib": round(contrib, 6),
        })

    return {
        "ece": round(ece, 6),
        "details": details,
        "_formula": "ECE=Σ(|Bm|/n)×|acc(Bm)-conf(Bm)|",
    }


def calc_h_index(
    factual_f1: float,
    extract_f1: float,
    reason_em: float,
    dim_scores: Dict[str, float],
) -> Dict:
    """
    计算幻觉综合指数 H（主裁判公式）

    公式：
        faithfulness = (extract_f1 + reason_em) / 2
        h_base = 0.5 × factual_f1 + 0.5 × faithfulness
        mu_dim = mean(dim_scores)
        delta = (mu_dim - 0.5) × 0.2
        H = clip(h_base + delta, 0, 1)

    三色（H=无幻觉度，越高越好）：
        H ≥ 0.80 → 🟢 PASS
        0.50 ≤ H < 0.80 → 🟡 REVIEW
        H < 0.50 → 🔴 REJECT
    """
    assert 0 <= factual_f1 <= 1, "factual_f1超范围"
    assert 0 <= extract_f1 <= 1, "extract_f1超范围"
    assert 0 <= reason_em <= 1, "reason_em超范围"

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
        "h_index": round(h, 6),
        "color": color,
        "action": action,
        "components": {
            "factual_f1": round(factual_f1, 6),
            "extract_f1": round(extract_f1, 6),   # 落地修正：保留原始分项供独立复算
            "reason_em": round(reason_em, 6),     # 落地修正：保留原始分项供独立复算
            "faithfulness": round(faithfulness, 6),
            "mu_dim": round(mu_dim, 6),
            "delta": round(delta, 6),
            "h_base": round(h_base, 6),
        },
        "_formula": (
            f"H=clip(0.5×{factual_f1:.4f}+0.5×({extract_f1:.4f}+{reason_em:.4f})/2"
            f"+{delta:.4f},0,1)={h:.6f}"
        ),
    }


# ============================================================
# 三、数学验证器（独立复算·防篡改）
# ============================================================

class MathValidator:
    """独立于主引擎的数学验证器，所有函数可单独跑"""

    @staticmethod
    def verify_f1(TP: int, FP: int, FN: int) -> float:
        P = TP / (TP + FP) if TP + FP > 0 else 0.0
        R = TP / (TP + FN) if TP + FN > 0 else 0.0
        return round(2 * P * R / (P + R) if P + R > 0 else 0.0, 6)

    @staticmethod
    def verify_h(factual_f1: float, extract_f1: float, reason_em: float, mu_dim: float) -> float:
        faithfulness = (extract_f1 + reason_em) / 2
        h_base = 0.5 * factual_f1 + 0.5 * faithfulness
        delta = (mu_dim - 0.5) * 0.2
        return round(max(0.0, min(1.0, h_base + delta)), 6)

    @staticmethod
    def validate_report(report: Dict) -> bool:
        """
        真独立复算（落地修正）：从报告的原始分项 extraction/reasoning 重推 H，
        与主引擎结果比对。不再把「已合并的 faithfulness」当两个参数传入。
        """
        factual_f1 = report["factual"]["f1"]
        extract_f1 = report["extraction"]["avg_token_f1"]
        reason_em = report["reasoning"]["em"]
        mu_dim = report["h_index"]["components"]["mu_dim"]

        expected = MathValidator.verify_h(factual_f1, extract_f1, reason_em, mu_dim)
        actual = report["h_index"]["h_index"]
        diff = abs(expected - actual)
        ok = diff < 1e-5
        print(f"  核验: 期望H={expected:.6f}  实际H={actual:.6f}  diff={diff:.2e}  {'✅ 通过' if ok else '❌ 不通过'}")
        return ok


# ============================================================
# 四、主引擎（融合版）
# ============================================================

class HallucinationMetrics:
    """
    龙魂·大模型幻觉量化评估引擎 v2.0（融合版）

    用法：
        engine = HallucinationMetrics()
        report = engine.run(
            factual_pred=[...], factual_gold=[...],
            extract_pred=[...], extract_gold=[...],
            reason_pred=[...], reason_gold=[...],
            dim_data={"人文科学": (pred, gold), ...}
        )
        print(engine.summary(report))
        engine.export_jsonl(report, "幻觉检测记录.jsonl")

    语义提醒：H = 无幻觉度（质量分），越高越好。
    """

    def __init__(self):
        self.dna = ENGINE_DNA
        self._records = []

    def run(
        self,
        factual_pred: List[int],
        factual_gold: List[int],
        extract_pred: List[str],
        extract_gold: List[str],
        reason_pred: List[str],
        reason_gold: List[str],
        dim_data: Optional[Dict[str, Tuple[List[int], List[int]]]] = None,
        confidence: Optional[List[float]] = None,
        correctness: Optional[List[float]] = None,
    ) -> Dict:
        """
        完整幻觉评估流程

        参数：
            factual_pred/gold: 事实判别题（0=正常，1=幻觉）
            extract_pred/gold: 信息抽取题（文本）
            reason_pred/gold: 知识推理题（文本）
            dim_data: 五维度分层数据 {"人文科学": (pred, gold), ...}
            confidence: 模型置信度 [0,1]
            correctness: 正确性 [0,1]
        """
        ts = datetime.now().isoformat()

        # Step 1: 事实性幻觉
        factual_result = calc_confusion_matrix(factual_pred, factual_gold)

        # Step 2: 忠实性·信息抽取
        extract_result = calc_token_f1(extract_pred, extract_gold)

        # Step 3: 忠实性·知识推理
        reason_result = calc_em(reason_pred, reason_gold)

        # Step 4: 五维度得分
        dim_scores = {}
        if dim_data:
            for dim, (pred, gold) in dim_data.items():
                dim_scores[dim] = calc_confusion_matrix(pred, gold)["f1"]
        else:
            # 默认：用事实性F1填充所有维度
            for dim in DIMENSIONS:
                dim_scores[dim] = factual_result["f1"]

        # Step 5: 幻觉综合指数 H
        h_result = calc_h_index(
            factual_result["f1"],
            extract_result["avg_token_f1"],
            reason_result["em"],
            dim_scores,
        )

        # Step 6: ECE校准（可选）
        ece_result = None
        if confidence and correctness:
            ece_result = calc_ece(confidence, correctness)

        # Step 7: 生成运行DNA
        digest = hashlib.sha256(
            json.dumps({
                "h": h_result["h_index"],
                "n_factual": len(factual_gold),
                "ts": ts,
            }, ensure_ascii=False).encode()
        ).hexdigest()[:8].upper()
        run_dna = f"{DNA_PREFIX}{datetime.now().strftime('%Y-%m-%d')}-HALLUCINATION-RUN-{digest}-UID9622"

        report = {
            "engine": "HallucinationMetrics v2.0 (融合版·落地修正)",
            "engine_dna": ENGINE_DNA,
            "run_dna": run_dna,
            "timestamp": ts,
            "confirm": CONFIRM,
            "factual": factual_result,
            "extraction": extract_result,
            "reasoning": reason_result,
            "dimensions": dim_scores,
            "ece": ece_result,
            "h_index": h_result,
            "color": h_result["color"],
            "action": h_result["action"],
        }

        self._records.append(report)
        return report

    def summary(self, report: Optional[Dict] = None) -> str:
        """生成人类可读的摘要"""
        r = report or (self._records[-1] if self._records else None)
        if not r:
            return "⚠️ 无记录，请先运行 run()"

        h = r["h_index"]
        lines = [
            "\n" + "=" * 70,
            f"🐉 龍魂·幻觉评估报告 v2.0",
            "=" * 70,
            f"DNA: {r['run_dna']}",
            f"引擎: {r['engine']}",
            f"时间: {r['timestamp']}",
            "=" * 70,
            f"\n📊 幻觉综合指数 H = {h['h_index']:.4f}  {h['color']}",
            f"   Action: {h['action']}",
            f"\n📋 分项指标:",
            f"   事实性 F1:        {r['factual']['f1']:.4f}",
            f"   信息抽取 TokenF1:  {r['extraction']['avg_token_f1']:.4f}",
            f"   知识推理 EM:      {r['reasoning']['em']:.4f}",
            f"   五维度均值:       {h['components']['mu_dim']:.4f}",
            f"\n🧭 各维度 F1:",
        ]
        for dim, score in r["dimensions"].items():
            bar = "█" * int(score * 10)
            lines.append(f"   {dim:10} {score:.4f} {bar}")

        if r.get("ece"):
            lines.append(f"\n📐 置信度校准 ECE: {r['ece']['ece']:.4f}")
            lines.append(f"   解释: 0=完美校准，越小越好（与H方向相反·单独汇报）")

        lines.append(f"\n🔐 确认码: {r['confirm']}")
        lines.append("=" * 70 + "\n")
        return "\n".join(lines)

    def export_jsonl(self, path: Optional[str] = None):
        """导出JSONL格式，便于流式审计。默认收敛至 _work/ 不入 git。"""
        if path is None:
            path = "_work/hallucination_records.jsonl"
        with open(path, "w", encoding="utf-8") as f:
            for r in self._records:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        print(f"✅ 已导出 {len(self._records)} 条记录 → {path}")


# ============================================================
# 五、验收测试（黄金标准·开箱即验）
# ============================================================

def acceptance_test(export_path: Optional[str] = None):
    """内置验收测试，运行即验证整套系统"""
    print("=" * 70)
    print("🐉 龍魂·幻觉检测引擎 v2.0（融合版·落地修正）验收测试")
    print("=" * 70)

    random.seed(9622)  # 固定种子 → 全程可复现

    # 事实判别：100条，模拟78%准确率（演示配置：0=正常，1=幻觉）
    factual_gold = [random.randint(0, 1) for _ in range(100)]
    factual_pred = [g if random.random() < 0.78 else 1 - g for g in factual_gold]

    # 信息抽取：51条（17×3），80%逐字保留，20%截半
    extract_gold = ["北京是中国首都", "量子纠缠是物理现象", "五行包含金木水火土"] * 17
    extract_pred = [s if random.random() < 0.80 else s[:len(s)//2] for s in extract_gold]

    # 知识推理：52条（13×4），72%精确命中
    reason_gold = ["正确答案A", "是的", "不正确", "符合题意"] * 13
    reason_pred = [s if random.random() < 0.72 else "其他" for s in reason_gold]

    # 五维度：每维20条，75%准确率
    dim_data = {}
    for dim in DIMENSIONS:
        n = 20
        gold = [random.randint(0, 1) for _ in range(n)]
        pred = [g if random.random() < 0.75 else 1 - g for g in gold]
        dim_data[dim] = (pred, gold)

    # 置信度校准：100条（演示配置·与正确性独立生成，仅作功能展示）
    confidence = [0.5 + random.random() * 0.5 for _ in range(100)]
    correctness = [1 if random.random() < 0.78 else 0 for _ in range(100)]

    # 运行引擎
    engine = HallucinationMetrics()
    report = engine.run(
        factual_pred, factual_gold,
        extract_pred, extract_gold,
        reason_pred, reason_gold,
        dim_data,
        confidence, correctness,
    )

    # 输出摘要
    print(engine.summary(report))

    # 独立数学验证
    print("🔍 独立数学验证:")
    MathValidator.validate_report(report)

    print(f"\n🧬 引擎DNA: {engine.dna}")
    print(f"🔐 {CONFIRM}")
    print("=" * 70)

    # 导出JSONL（默认 _work/，不入 git）
    engine.export_jsonl(export_path)

    return report


# ============================================================
# 六、命令行入口
# ============================================================

if __name__ == "__main__":
    acceptance_test()
