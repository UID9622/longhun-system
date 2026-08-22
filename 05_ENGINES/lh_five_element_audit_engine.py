#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
# 龍芯⚡️丙午·乙巳·癸酉·亥时·☰乾-FIVE-ELEMENT-AUDIT-v1.0
# CREATOR: 诸葛鑫（UID9622）
# PROTOCOL: CC BY-NC-SA 4.0
"""
龍魂 · 五行审计决策引擎 v1.0

核心能力：
  1. 数字根计算 dr(n) = 1 + (n-1) % 9
  2. 三六九不动点判定：dr(n) ∈ {3,6,9} 为宇宙稳态
  3. 五行映射：1-9 → 木火土金水
  4. 五行审计：输入按 木·火·土·金·水 五维评分，检测平衡与相生相克
  5. 输出三色决策 + DNA 追溯

用法：
  from engines.lh_five_element_audit_engine import FiveElementAuditEngine
  engine = FiveElementAuditEngine()
  report = engine.audit_text("龍魂系统采用DNA追溯码，输出经GPG签名，数据留存在本地。")
"""

import sys
import hashlib
import math
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional

# 兼容直接运行与项目内导入
_PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))
if str(_PROJECT_ROOT / "engines") not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT / "engines"))

try:
    from lh_math_formula_core import digital_root, element_of, ELEMENT_RELATIONS, AuditColor
except Exception:
    # 兜底：引擎目录单独运行时
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from lh_math_formula_core import digital_root, element_of, ELEMENT_RELATIONS, AuditColor


# ═══════════════════════════════════════════════════════════════════════════════
# 配置
# ═══════════════════════════════════════════════════════════════════════════════

CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"

FIVE_DIMENSIONS = {
    "木": {
        "name": "生发·来源",
        "terms": [
            "dna", "追溯", "签章", "标识", "来源", "出处", "版本", "协议",
            "声明", "license", "演进", "扩展", "生长", "迭代", "开源",
        ],
    },
    "火": {
        "name": "明达·输出",
        "terms": [
            "输出", "产物", "去向", "可见", "透明", "公开", "目标", "清晰",
            "明确", "无歧义", "影响", "范围", "风险", "披露", "告知",
        ],
    },
    "土": {
        "name": "稳定·归档",
        "terms": [
            "归档", "存档", "留痕", "固化", "不可篡改", "本地", "存储",
            "主权", "回滚", "恢复", "撤销", "可逆", "备份", "副本", "稳定",
        ],
    },
    "金": {
        "name": "坚固·规则",
        "terms": [
            "签名", "签章", "gpg", "身份", "uid", "实名", "认证", "规则",
            "铁律", "规范", "安全", "加密", "防护", "熔断", "breaker", "p0",
        ],
    },
    "水": {
        "name": "流动·链路",
        "terms": [
            "日志", "记录", "完整", "哈希链", "链上", "链路", "追踪", "trace",
            "审计", "audit", "审查", "流动", "数据流", "可追溯", "连续性",
        ],
    },
}


# ═══════════════════════════════════════════════════════════════════════════════
# 数据模型
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class FixedPointInfo:
    digital_root: int
    is_369: bool          # 三六九不动点
    is_global_fixed: bool # dr == 9，全局不动点
    is_cycle: bool        # 3↔6 二周期轨道
    element: str


@dataclass
class FiveElementAuditReport:
    dna: str
    input_digest: str
    fixed_point: FixedPointInfo
    dimension_scores: Dict[str, float]
    balance: float
    shengke: Dict[str, Any]
    overall_score: float
    color: str
    decision: str
    audited_at: str
    confirm: str = CONFIRM


# ═══════════════════════════════════════════════════════════════════════════════
# 引擎
# ═══════════════════════════════════════════════════════════════════════════════

class FiveElementAuditEngine:
    """五行审计决策引擎：数字根 + 三六九不动点 + 五行五维评分"""

    def __init__(self):
        self.elements_order = ["木", "火", "土", "金", "水"]

    @staticmethod
    def _now_iso() -> str:
        return datetime.now().isoformat()

    @staticmethod
    def _generate_dna(tag: str) -> str:
        now = datetime.now().isoformat()
        h = hashlib.sha256(f"{tag}-{time.time()}-{now}".encode()).hexdigest()[:8]
        return f"#龍芯⚡️{now[:10].replace('-','')}·{tag}-v1.0-{h}"

    @staticmethod
    def _text_to_seed(text: str) -> int:
        """将任意文本映射为整数种子，用于数字根计算"""
        if text.isdigit():
            return int(text)
        return int(hashlib.sha256(text.encode("utf-8")).hexdigest(), 16)

    def analyze_fixed_point(self, value: Any) -> FixedPointInfo:
        """分析数字根与不动点性质"""
        if isinstance(value, str):
            n = self._text_to_seed(value)
        else:
            n = int(value)
        dr = digital_root(n)
        return FixedPointInfo(
            digital_root=dr,
            is_369=dr in {3, 6, 9},
            is_global_fixed=dr == 9,
            is_cycle=dr in {3, 6},
            element=element_of(n),
        )

    def _score_dimension(self, element: str, text: str) -> Tuple[float, List[str]]:
        """对单一五行维度按关键词命中数评分：命中越多分越高，命中3个即满分"""
        text_lower = text.lower()
        terms = FIVE_DIMENSIONS[element]["terms"]
        hits = [term for term in terms if term in text_lower]
        # 命中 2 个视为该维度充分表达
        score = min(1.0, len(hits) / 2.0)
        return round(score, 4), hits

    def audit_text(self, text: str) -> FiveElementAuditReport:
        """对文本进行五行审计决策"""
        fixed = self.analyze_fixed_point(text)

        # 五维评分
        dimension_scores = {}
        dimension_details = {}
        for element in self.elements_order:
            s, d = self._score_dimension(element, text)
            dimension_scores[element] = s
            dimension_details[element] = d

        # 五行平衡指数
        balance = self._balance_score(dimension_scores)

        # 相生相克分析
        shengke = self._shengke_analysis(dimension_scores)

        # 综合评分
        overall, color, decision = self._overall_decision(fixed, dimension_scores, balance, shengke)

        digest = hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]
        return FiveElementAuditReport(
            dna=self._generate_dna("FIVE-ELEMENT-AUDIT"),
            input_digest=digest,
            fixed_point=fixed,
            dimension_scores=dimension_scores,
            balance=balance,
            shengke=shengke,
            overall_score=overall,
            color=color,
            decision=decision,
            audited_at=self._now_iso(),
        )

    def audit_scores(self, scores: Dict[str, float], seed: int = 0) -> FiveElementAuditReport:
        """外部直接传入五维评分（0~1）进行审计"""
        fixed = self.analyze_fixed_point(seed)
        dimension_scores = {e: max(0.0, min(1.0, scores.get(e, 0.0))) for e in self.elements_order}
        balance = self._balance_score(dimension_scores)
        shengke = self._shengke_analysis(dimension_scores)
        overall, color, decision = self._overall_decision(fixed, dimension_scores, balance, shengke)

        return FiveElementAuditReport(
            dna=self._generate_dna("FIVE-ELEMENT-SCORE"),
            input_digest=f"seed-{seed}",
            fixed_point=fixed,
            dimension_scores=dimension_scores,
            balance=balance,
            shengke=shengke,
            overall_score=overall,
            color=color,
            decision=decision,
            audited_at=self._now_iso(),
        )

    def _balance_score(self, scores: Dict[str, float]) -> float:
        """五行平衡指数 = 100 * (1 - std/mean)，越平衡越接近100"""
        vals = list(scores.values())
        if not vals:
            return 0.0
        mean = sum(vals) / len(vals)
        if mean == 0:
            return 0.0
        variance = sum((v - mean) ** 2 for v in vals) / len(vals)
        std = math.sqrt(variance)
        cv = std / mean
        return max(0, round(100 * (1 - min(cv, 1)), 2))

    def _shengke_analysis(self, scores: Dict[str, float]) -> Dict[str, Any]:
        """分析五行相生相克关系"""
        relations = []
        penalty = 0.0
        bonus = 0.0

        for a, b in zip(self.elements_order, self.elements_order[1:] + [self.elements_order[0]]):
            # a 生 b
            if scores[b] > scores[a] + 0.2:
                bonus += 0.05
                relations.append(f"{a}生{b}·顺畅")
            elif scores[b] < scores[a] - 0.4:
                # a 克 b 过强（被克方太弱）
                penalty += 0.05
                relations.append(f"{a}克{b}·失衡")

        # 检查相克对：木↔土、火↔金、土↔水
        ke_pairs = [("木", "土"), ("火", "金"), ("土", "水"), ("金", "木"), ("水", "火")]
        for a, b in ke_pairs:
            if scores[a] > 0.7 and scores[b] < 0.3:
                penalty += 0.03
                relations.append(f"{a}强{b}弱·相克明显")

        return {
            "relations": relations,
            "bonus": round(bonus, 4),
            "penalty": round(penalty, 4),
        }

    def _overall_decision(
        self,
        fixed: FixedPointInfo,
        scores: Dict[str, float],
        balance: float,
        shengke: Dict[str, Any],
    ) -> Tuple[float, str, str]:
        """综合决策：分数 + 三色 + 决议文案"""
        # 基础分：五维平均分
        base = sum(scores.values()) / len(scores)
        # 平衡加成
        balance_bonus = balance / 100 * 0.1
        # 相生相克调整
        adjusted = base + balance_bonus + shengke["bonus"] - shengke["penalty"]
        adjusted = max(0.0, min(1.0, adjusted))

        # 数字根稳态加成：369不动点小幅加分，9不动点最大
        if fixed.is_global_fixed:
            adjusted = min(1.0, adjusted + 0.05)
        elif fixed.is_369:
            adjusted = min(1.0, adjusted + 0.02)

        overall = round(adjusted * 100, 2)

        if overall >= 80:
            color = "🟢"
            decision = "五行相生、数字根稳态，决策通过"
        elif overall >= 60:
            color = "🟡"
            decision = "五行局部失衡，需复核后决策"
        else:
            color = "🔴"
            decision = "五行严重失衡或规则缺失，禁止执行"

        return overall, color, decision

    def demo(self):
        """演示五行审计决策"""
        print("=" * 64)
        print("🐉 龍魂 · 五行审计决策引擎 v1.0")
        print("=" * 64)

        cases = [
            ("理想系统", "龍魂系统采用DNA追溯码，GPG签名，数据本地存储，来源可查去向可追责任可究，日志完整，具备P0熔断。"),
            ("来源缺失", "系统输出结果，但没有DNA标识和版本记录，无法追溯来源。"),
            ("高危漏洞", "代码使用eval执行用户输入，无签名无日志，数据可出境，缺少熔断机制。"),
            ("数字根测试", "123456789"),
        ]

        for label, text in cases:
            r = self.audit_text(text)
            print(f"\n[{label}]")
            print(f"  输入摘要: {text[:40]}...")
            print(f"  数字根: {r.fixed_point.digital_root} ({r.fixed_point.element})")
            print(f"  三六九不动点: {'是' if r.fixed_point.is_369 else '否'} | 全局不动点(9): {'是' if r.fixed_point.is_global_fixed else '否'}")
            print(f"  五维评分: " + " · ".join(f"{k}={v:.2f}" for k, v in r.dimension_scores.items()))
            print(f"  五行平衡: {r.balance}")
            print(f"  综合评分: {r.color} {r.overall_score}")
            print(f"  决议: {r.decision}")
            print(f"  DNA: {r.dna}")


if __name__ == "__main__":
    FiveElementAuditEngine().demo()
