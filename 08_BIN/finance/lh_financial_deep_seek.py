# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂·金融深度求索引擎 v2.0 (Longhun Financial Deep Seek)
DNA: #龍芯⚡️丙午·丙申·癸亥·巳时·䷒临-FINANCIAL-DEEP-SEEK-v2.0-E7E9A326
创建者: 诸葛鑫（UID9622）
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)

设计目标（对齐 DeepSeek-V3 issue #1466 评论 5309136671 的病根）:
  #1466 的核心矛盾: report.json 的 detection_rate=61.0 与 CSV 明细直算 80.7% 对不上,
  评论者反推撞上巧合后撤回, 遗留真问题: "数字口径不自声明 + 不可复现 + 无一致性对拍".
  v2.0 以此三病为需求, 对应落地:
    ① 内容寻址 DNA  : 同输入 + 同公式版本 => 同 DNA => 可复现可对拍 (不再用 time.time())
    ② 口径锁         : 每个维度/指标带 formula + version + inputs_hash, 数字永远自报口径
    ③ 明细-聚合对拍  : declared_scores 与本引擎重算逐维比对, 偏差>容差 => 🟡 MISMATCH
    ④ 黄金回归       : 固定锚点数据 + 期望值, --self-test 验证数字永不漂移
    ⑤ 真·数字根      : 369 底座 dr(n) = 1 + ((n-1) mod 9)  (龍魂 mod9 引擎标准)
    ⑥ 权重 A-BOM 备案: 权重来源与理由显式声明, 可 --weights 覆盖

零黑箱原则: 每个输出可追溯到输入 + 公式 + 版本。不编造, 缺字段显式标 ⚠️。
"""

import hashlib
import json
import sys
import unittest
from datetime import datetime
from typing import Any, Dict, List, Optional

# ═══════════════════════════════════════════════════════════════
# §0 常量与 A-BOM 备案
# ═══════════════════════════════════════════════════════════════

FORMULA_VERSION = "v2.0"  # 口径版本: 公式变更必须升版本, 旧版本输出仍可复现

# A-BOM 备案注释块 (算法审计协议 v1.0 · 零黑箱):
# 目标函数  : 综合健康分 = Σ(权重_k × 维度分_k), 维度分 ∈ [0,1]
# 输入特征  : current_assets/current_liabilities/total_debt/total_assets/
#             revenue/net_income/volatility/consistency (+ declared_scores 对拍用)
# 用户影响  : 输出仅作财务体检参考, 不构成投资建议
# 申诉通道  : --weights 覆盖权重重算, --explain 全公式可核
DEFAULT_WEIGHTS: Dict[str, float] = {
    # 权重来源: 龍魂五维财务体检标准 v1.0 (启发式初值, 理由见下)
    "liquidity": 0.25,     # 短期偿债安全垫 —— 现金为王, 权重最高
    "debt": 0.20,          # 杠杆健康度 —— 负债率越低越稳
    "efficiency": 0.20,    # 资产周转 —— 钱有没有转起来
    "profitability": 0.20, # 盈利质量 —— ROA
    "stability": 0.15,     # 波动与一致性 —— 保命项
}

THRESHOLDS: Dict[str, float] = {
    "excellent": 0.85,  # 🟢
    "good": 0.70,       # 🟢
    "fair": 0.50,       # 🟡
    "poor": 0.30,       # 🔴
    "critical": 0.15,   # 🔴
}

RECONCILE_TOLERANCE = 0.02  # 对拍容差: 偏差 > 0.02 即标 🟡 MISMATCH

REQUIRED_FIELDS = [
    "current_assets", "current_liabilities", "total_debt",
    "total_assets", "revenue", "net_income",
]
OPTIONAL_FIELDS = ["volatility", "consistency"]

# ═══════════════════════════════════════════════════════════════
# §1 工具函数
# ═══════════════════════════════════════════════════════════════


def clamp01(x: float) -> float:
    """夹取到 [0,1]"""
    return max(0.0, min(1.0, x))


def digital_root(n: int) -> int:
    """369 底座数字根: dr(n) = 1 + ((n-1) mod 9) —— 对齐 bin/lh_mod9_runtime_engine.py"""
    if n <= 0:
        return 1
    return 1 + ((n - 1) % 9)


def content_dna(data: Dict, formula_version: str = FORMULA_VERSION) -> str:
    """内容寻址 DNA: 由规范化输入 + 公式版本 哈希生成。

    为什么用内容而不是时间戳:
      issue #1466 的病根是"同一输入两个数字对不上"。
      内容寻址 => 同输入 => 同 DNA => 输出可复现、可对拍、可审计。
    """
    canonical = json.dumps(data, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    h = hashlib.sha256(f"{canonical}|{formula_version}".encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️FIN-DEEP-SEEK-{formula_version}-{h}"


def inputs_hash(data: Dict) -> str:
    """输入指纹(口径锁用): 仅输入内容的 SHA256 前 12 位"""
    canonical = json.dumps(data, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(canonical.encode()).hexdigest()[:12]


# ═══════════════════════════════════════════════════════════════
# §2 核心引擎
# ═══════════════════════════════════════════════════════════════


class FinancialDeepSeek:
    """多因子财务健康评估引擎 v2.0 —— 可复现 · 口径锁 · 对拍校验"""

    def __init__(self, weights: Optional[Dict[str, float]] = None, tolerance: float = RECONCILE_TOLERANCE):
        self.weights: Dict[str, float] = dict(DEFAULT_WEIGHTS)
        if weights:
            # 权重覆盖: 只认五维合法键, 非法键拒绝(防拼写错误静默产生假分数)
            for k in weights:
                if k not in DEFAULT_WEIGHTS:
                    raise ValueError(f"unknown dimension '{k}', valid: {list(DEFAULT_WEIGHTS)}")
            self.weights.update(weights)
        self.tolerance = tolerance
        self.dna = content_dna({"__engine__": True}, FORMULA_VERSION)

    # ── 五个维度评分 (每个都返回 score + formula + inputs, 口径锁落地) ──

    def _score_liquidity(self, d: Dict) -> Dict[str, Any]:
        ca = d.get("current_assets", 0.0)
        cl = d.get("current_liabilities", 0.0)
        ratio = (ca / cl) if cl > 0 else 0.0  # 流动比率, 分母为 0 => 0(无安全垫可谈)
        score = clamp01(ratio / 3.0)          # 比率≥3 => 1.0 (3 倍速动红线)
        return {
            "score": round(score, 4),
            "formula": "clamp01(current_assets / (current_liabilities × 3))",
            "inputs": {"current_assets": ca, "current_liabilities": cl},
        }

    def _score_debt(self, d: Dict) -> Dict[str, Any]:
        debt = d.get("total_debt", 0.0)
        assets = d.get("total_assets", 0.0)
        ratio = (debt / assets) if assets > 0 else 1.0  # 无资产 => 视为全负债
        score = clamp01(1.0 - ratio)
        return {
            "score": round(score, 4),
            "formula": "clamp01(1 - total_debt / total_assets)",
            "inputs": {"total_debt": debt, "total_assets": assets},
        }

    def _score_efficiency(self, d: Dict) -> Dict[str, Any]:
        revenue = d.get("revenue", 0.0)
        assets = d.get("total_assets", 0.0)
        ratio = (revenue / assets) if assets > 0 else 0.0
        score = clamp01(ratio / 2.0)  # 总资产周转率≥2 => 1.0
        return {
            "score": round(score, 4),
            "formula": "clamp01(revenue / (total_assets × 2))",
            "inputs": {"revenue": revenue, "total_assets": assets},
        }

    def _score_profitability(self, d: Dict) -> Dict[str, Any]:
        ni = d.get("net_income", 0.0)
        assets = d.get("total_assets", 0.0)
        roa = (ni / assets) if assets > 0 else 0.0
        score = clamp01(roa / 0.15)  # ROA≥15% => 1.0
        return {
            "score": round(score, 4),
            "formula": "clamp01(net_income / (total_assets × 0.15))",
            "inputs": {"net_income": ni, "total_assets": assets},
        }

    def _score_stability(self, d: Dict) -> Dict[str, Any]:
        volatility = d.get("volatility", 0.5)
        consistency = d.get("consistency", 0.5)
        raw = 1.0 - ((volatility + (1.0 - consistency)) / 2.0)
        score = clamp01(raw)
        return {
            "score": round(score, 4),
            "formula": "clamp01(1 - (volatility + (1 - consistency)) / 2)",
            "inputs": {"volatility": volatility, "consistency": consistency},
        }

    # ── 对拍校验 (issue #1466 核心场景: 外部数字 vs 真实计算) ──

    def _reconcile(self, data: Dict, dims: Dict[str, Dict]) -> Dict[str, Any]:
        declared = data.get("declared_scores")
        if not declared:
            return {"status": "SKIPPED", "note": "no declared_scores provided"}
        diffs: Dict[str, float] = {}
        mismatch_dims: List[str] = []
        for k in self.weights:
            if k in declared:
                diff = abs(float(declared[k]) - float(dims[k]["score"]))
                diffs[k] = round(diff, 4)
                if diff > self.tolerance:
                    mismatch_dims.append(k)
        return {
            "status": "RECONCILED" if not mismatch_dims else "MISMATCH",
            "tolerance": self.tolerance,
            "diffs": diffs,
            "mismatch_dims": mismatch_dims,
        }

    # ── 输入完整性与异常 ──

    @staticmethod
    def _completeness(data: Dict) -> Dict[str, Any]:
        all_fields = REQUIRED_FIELDS + OPTIONAL_FIELDS
        missing = [f for f in all_fields if f not in data]
        pct = round((len(all_fields) - len(missing)) / len(all_fields), 4)
        negatives = [f for f in ["current_assets", "total_debt", "total_assets"] if data.get(f, 0.0) < 0]
        return {
            "completeness": pct,
            "missing_fields": missing,
            "negative_anomalies": negatives,
        }

    # ── 主评估 ──

    def assess(self, data: Dict) -> Dict[str, Any]:
        # 输入规范化: 数值字段统一转 float, 防字符串混入
        clean: Dict[str, float] = {}
        for f in REQUIRED_FIELDS + OPTIONAL_FIELDS:
            if f in data:
                try:
                    clean[f] = float(data[f])
                except (TypeError, ValueError):
                    clean[f] = 0.0
        declared = data.get("declared_scores")

        # 1. 五维评分 (带口径)
        dims = {
            "liquidity": self._score_liquidity(clean),
            "debt": self._score_debt(clean),
            "efficiency": self._score_efficiency(clean),
            "profitability": self._score_profitability(clean),
            "stability": self._score_stability(clean),
        }

        # 2. 加权综合分 (用未舍入的分数累加, 最后统一 round)
        composite = sum(dims[k]["score"] * self.weights[k] for k in self.weights)
        composite = round(composite, 4)

        # 3. 真·数字根 (369 底座): 综合分百分位 => dr ∈ [1,9]
        root = digital_root(round(composite * 100))

        # 4. 风险等级 (三色)
        level, tricolor = self._risk_level(composite)

        # 5. 对拍 + 完整性 + 审计链
        recon = self._reconcile(data, dims)
        completeness = self._completeness(data)

        # 6. 口径锁: 本输出由什么输入 + 什么公式版本 + 什么 DNA 得出
        contract = {
            "engine": "longhun_financial_deep_seek",
            "formula_version": FORMULA_VERSION,
            "inputs_hash": inputs_hash(clean),
        }

        return {
            "dna": content_dna(clean, FORMULA_VERSION),
            "metric_contract": contract,
            "composite_score": composite,
            "digital_root": root,
            "risk_level": level,
            "tricolor": tricolor,
            "dimensions": {k: dims[k] for k in self.weights},
            "weights": dict(self.weights),
            "reconciliation": recon,
            "completeness": completeness["completeness"],
            "missing_fields": completeness["missing_fields"],
            "negative_anomalies": completeness["negative_anomalies"],
            # 时间戳仅作展示, 不参与 DNA —— 保证同输入同输出可复现
            "timestamp": datetime.now().isoformat(),
        }

    @staticmethod
    def _risk_level(score: float):
        if score >= THRESHOLDS["excellent"]:
            return "Excellent", "🟢"
        if score >= THRESHOLDS["good"]:
            return "Good", "🟢"
        if score >= THRESHOLDS["fair"]:
            return "Fair", "🟡"
        if score >= THRESHOLDS["poor"]:
            return "Poor", "🔴"
        return "Critical", "🔴"

    # ── 报告 ──

    def report(self, data: Dict, lang: str = "en") -> str:
        r = self.assess(data)
        if lang == "zh":
            return self._report_zh(r)
        return self._report_en(r)

    @staticmethod
    def _report_en(r: Dict) -> str:
        lines = [
            "🐉 Longhun Financial Deep Seek Report",
            "=" * 54,
            f"DNA: {r['dna']}",
            f"Metric Contract: engine={r['metric_contract']['engine']} version={r['metric_contract']['formula_version']} inputs={r['metric_contract']['inputs_hash']}",
            f"Composite Score: {r['composite_score']:.4f}",
            f"Digital Root: {r['digital_root']}",
            f"Risk Level: {r['tricolor']} {r['risk_level']}",
            f"Reconciliation: {r['reconciliation']['status']}",
            "-" * 30,
            "Dimension Scores (formula-versioned):",
        ]
        for k, v in r["dimensions"].items():
            lines.append(f"  {k:14s}: {v['score']:.4f}  | {v['formula']}")
        lines.append("-" * 30)
        if r["missing_fields"]:
            lines.append(f"⚠️ Missing fields: {', '.join(r['missing_fields'])} (completeness={r['completeness']})")
        else:
            lines.append(f"✅ Input completeness: {r['completeness']}")
        if r["reconciliation"]["status"] == "MISMATCH":
            lines.append(f"🟡 MISMATCH dims: {r['reconciliation']['mismatch_dims']} diffs={r['reconciliation']['diffs']}")
        lines.append("=" * 54)
        return "\n".join(lines)

    @staticmethod
    def _report_zh(r: Dict) -> str:
        level_map = {"Excellent": "优秀", "Good": "良好", "Fair": "一般", "Poor": "较差", "Critical": "危急"}
        lines = [
            "🐉 龍魂·金融深度求索报告",
            "=" * 54,
            f"DNA: {r['dna']}",
            f"口径锁: 引擎={r['metric_contract']['engine']} 版本={r['metric_contract']['formula_version']} 输入指纹={r['metric_contract']['inputs_hash']}",
            f"综合分: {r['composite_score']:.4f}",
            f"数字根: {r['digital_root']}",
            f"风险等级: {r['tricolor']} {level_map.get(r['risk_level'], r['risk_level'])}",
            f"对拍校验: {r['reconciliation']['status']}",
            "-" * 30,
            "五维得分 (带口径):",
        ]
        for k, v in r["dimensions"].items():
            lines.append(f"  {k:14s}: {v['score']:.4f}  | {v['formula']}")
        lines.append("-" * 30)
        if r["missing_fields"]:
            lines.append(f"⚠️ 缺字段: {', '.join(r['missing_fields'])} (完整度={r['completeness']})")
        else:
            lines.append(f"✅ 输入完整度: {r['completeness']}")
        if r["reconciliation"]["status"] == "MISMATCH":
            lines.append(f"🟡 对拍不一致维度: {r['reconciliation']['mismatch_dims']} 偏差={r['reconciliation']['diffs']}")
        lines.append("=" * 54)
        return "\n".join(lines)

    def explain(self, data: Dict) -> str:
        """零黑箱逐维解释: 公式 + 输入 + 中间计算"""
        r = self.assess(data)
        lines = [
            "🐉 逐维解释 (零黑箱 · 每步可核)",
            "=" * 54,
            f"综合分 = Σ(权重 × 维度分)  版本: {r['metric_contract']['formula_version']}",
            f"输入指纹: {r['metric_contract']['inputs_hash']}",
        ]
        for k, v in r["dimensions"].items():
            ins = ", ".join(f"{ik}={iv}" for ik, iv in v["inputs"].items())
            lines.append(f"\n[{k}] 权重 {r['weights'][k]}")
            lines.append(f"  公式: {v['formula']}")
            lines.append(f"  输入: {ins}")
            lines.append(f"  得分: {v['score']:.4f}")
        lines.append(f"\n加权综合: {r['composite_score']:.4f}  数字根(369): {r['digital_root']}  等级: {r['tricolor']} {r['risk_level']}")
        lines.append("=" * 54)
        return "\n".join(lines)

    # ── 黄金回归 (锚点固定, 数字永不漂移) ──

    GOLDEN_CASES: List[Dict[str, Any]] = [
        {
            "name": "healthy_sme",
            "data": {
                "current_assets": 900000, "current_liabilities": 100000,
                "total_debt": 100000, "total_assets": 1000000,
                "revenue": 1500000, "net_income": 200000,
                "volatility": 0.2, "consistency": 0.85,
            },
            "expect": {"composite_score": 0.9038, "digital_root": 9, "risk_level": "Excellent"},
        },
        {
            "name": "mid_sme",
            "data": {
                "current_assets": 500000, "current_liabilities": 200000,
                "total_debt": 300000, "total_assets": 1000000,
                "revenue": 800000, "net_income": 120000,
                "volatility": 0.35, "consistency": 0.70,
            },
            "expect": {"composite_score": 0.6896, "digital_root": 6, "risk_level": "Fair"},
        },
        {
            "name": "distressed_sme",
            "data": {
                "current_assets": 50000, "current_liabilities": 500000,
                "total_debt": 900000, "total_assets": 1000000,
                "revenue": 100000, "net_income": -50000,
                "volatility": 0.8, "consistency": 0.2,
            },
            "expect": {"composite_score": 0.0683, "digital_root": 7, "risk_level": "Critical"},
        },
    ]

    def self_test(self) -> bool:
        """黄金回归: 固定锚点数据必须产出固定期望值, 偏差>0.0001 即失败"""
        ok = True
        for case in self.GOLDEN_CASES:
            r = self.assess(case["data"])
            exp = case["expect"]
            dc = abs(r["composite_score"] - exp["composite_score"])
            dr_ok = r["digital_root"] == exp["digital_root"]
            lv_ok = r["risk_level"] == exp["risk_level"]
            pass_ = dc <= 0.0001 and dr_ok and lv_ok
            ok = ok and pass_
            mark = "🟢" if pass_ else "🔴"
            print(f"{mark} golden[{case['name']}] composite={r['composite_score']} "
                  f"(exp {exp['composite_score']}) dr={r['digital_root']} "
                  f"level={r['risk_level']}")
        return ok


# ═══════════════════════════════════════════════════════════════
# §3 CLI
# ═══════════════════════════════════════════════════════════════

DEMO_DATA = {
    "current_assets": 500000, "current_liabilities": 200000,
    "total_debt": 300000, "total_assets": 1000000,
    "revenue": 800000, "net_income": 120000,
    "volatility": 0.35, "consistency": 0.70,
}


def main(argv: Optional[List[str]] = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    weights = None
    lang = "en"
    for i, a in enumerate(args):
        if a == "--weights" and i + 1 < len(args):
            try:
                weights = json.loads(args[i + 1])
            except json.JSONDecodeError:
                print(json.dumps({"error": "invalid --weights JSON"}, ensure_ascii=False))
                return 1
        if a == "--lang" and i + 1 < len(args):
            lang = args[i + 1]

    if "--self-test" in args:
        engine = FinancialDeepSeek(weights=weights)
        ok = engine.self_test()
        return 0 if ok else 1

    if "--explain" in args:
        data = _parse_input(args)
        engine = FinancialDeepSeek(weights=weights)
        print(engine.explain(data))
        return 0

    data = _parse_input(args)
    engine = FinancialDeepSeek(weights=weights)
    if "--json" in args or data.get("__json__"):
        print(json.dumps(engine.assess(data), indent=2, ensure_ascii=False))
    else:
        print(engine.report(data, lang=lang))
    return 0


def _parse_input(args: List[str]) -> Dict:
    """从 argv 提取 JSON 数据: 优先最后一个类 JSON 参数, 否则用 DEMO_DATA"""
    for a in reversed(args):
        if a.startswith("{"):
            try:
                return json.loads(a)
            except json.JSONDecodeError:
                continue
    return dict(DEMO_DATA)


# ═══════════════════════════════════════════════════════════════
# §4 锚点测试 (12 项 · 全真跑)
# ═══════════════════════════════════════════════════════════════


class TestFinancialDeepSeek(unittest.TestCase):

    def setUp(self):
        self.engine = FinancialDeepSeek()
        self.demo = dict(DEMO_DATA)

    def test_01_dimension_scores_in_range(self):
        r = self.engine.assess(self.demo)
        for k, v in r["dimensions"].items():
            self.assertTrue(0.0 <= v["score"] <= 1.0, f"{k} out of range")

    def test_02_composite_in_range(self):
        r = self.engine.assess(self.demo)
        self.assertTrue(0.0 <= r["composite_score"] <= 1.0)

    def test_03_content_addressed_dna_reproducible(self):
        """同一输入 => 同一 DNA (可复现, issue #1466 病根的直接解药)"""
        r1 = self.engine.assess(self.demo)
        r2 = self.engine.assess(self.demo)
        self.assertEqual(r1["dna"], r2["dna"])
        self.assertEqual(r1["composite_score"], r2["composite_score"])
        # 不同输入 => 不同 DNA
        other = dict(self.demo, net_income=200000)
        r3 = self.engine.assess(other)
        self.assertNotEqual(r1["dna"], r3["dna"])

    def test_04_digital_root_in_1_9(self):
        r = self.engine.assess(self.demo)
        self.assertTrue(1 <= r["digital_root"] <= 9)

    def test_05_risk_level_mapping(self):
        self.assertEqual(self.engine._risk_level(0.90)[0], "Excellent")
        self.assertEqual(self.engine._risk_level(0.75)[0], "Good")
        self.assertEqual(self.engine._risk_level(0.60)[0], "Fair")
        self.assertEqual(self.engine._risk_level(0.40)[0], "Poor")
        self.assertEqual(self.engine._risk_level(0.10)[0], "Critical")

    def test_06_missing_fields_explicit(self):
        partial = {"current_assets": 100, "current_liabilities": 50}
        r = self.engine.assess(partial)
        self.assertIn("total_assets", r["missing_fields"])
        self.assertLess(r["completeness"], 1.0)

    def test_07_reconciliation_mismatch_detected(self):
        """对拍: 外部声明分数与本引擎重算偏差 > 容差 => 🟡 MISMATCH"""
        data = dict(self.demo, declared_scores={
            "liquidity": 0.9, "debt": 0.7, "efficiency": 0.4,
            "profitability": 0.8, "stability": 0.675,
        })
        r = self.engine.assess(data)
        self.assertEqual(r["reconciliation"]["status"], "MISMATCH")
        self.assertIn("liquidity", r["reconciliation"]["mismatch_dims"])

    def test_08_reconciliation_reconciled(self):
        data = dict(self.demo, declared_scores={
            "liquidity": 0.8333, "debt": 0.7, "efficiency": 0.4,
            "profitability": 0.8, "stability": 0.675,
        })
        r = self.engine.assess(data)
        self.assertEqual(r["reconciliation"]["status"], "RECONCILED")

    def test_09_zero_denominator_no_crash(self):
        """除零边界: 负债/资产为 0 不得崩"""
        edge = {
            "current_assets": 0, "current_liabilities": 0,
            "total_debt": 0, "total_assets": 0,
            "revenue": 0, "net_income": 0, "volatility": 0.5, "consistency": 0.5,
        }
        r = self.engine.assess(edge)
        self.assertTrue(0.0 <= r["composite_score"] <= 1.0)

    def test_10_weights_override_and_validation(self):
        w = {"liquidity": 0.5, "debt": 0.2, "efficiency": 0.1, "profitability": 0.1, "stability": 0.1}
        e = FinancialDeepSeek(weights=w)
        r = e.assess(self.demo)
        self.assertEqual(r["weights"]["liquidity"], 0.5)
        with self.assertRaises(ValueError):
            FinancialDeepSeek(weights={"liq": 1.0})  # 非法维度键

    def test_11_explain_contains_formulas(self):
        txt = self.engine.explain(self.demo)
        self.assertIn("current_assets", txt)
        self.assertIn("公式", txt)

    def test_12_golden_regression_stable(self):
        self.assertTrue(self.engine.self_test())


def run_anchors() -> int:
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestFinancialDeepSeek)
    res = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if res.wasSuccessful() else 1


if __name__ == "__main__":
    if "--anchors" in sys.argv or "--test" in sys.argv:
        sys.exit(run_anchors())
    sys.exit(main())
