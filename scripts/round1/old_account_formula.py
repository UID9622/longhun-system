# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
旧账处理公式引擎 v1.0
DNA: #龍芯⚡️2026-07-06-OLD-ACCOUNT-FORMULA-v1.0

根基算法：三才算法（天·地·人）— 属"地"才维度的溯源规则

核心公式：
  F01｜旧账处理决策:  Action(E, M, I) → {重发主权版, 证据存档, 公开声明, 暂不处理}
  F02｜主权重锚价值:  SovereignValue = I × (E + 0.5M) × PublicationTimeWeight
  F03｜剽窃追溯概率:  P(追溯成功) = 1 - e^{-λ(E + 0.3M + 0.2I)}, λ=0.8
"""

import hashlib
import math
from dataclasses import dataclass, field
from datetime import datetime


# ═══════════════════════════════════════
# 核心常量
# ═══════════════════════════════════════

TRACE_COEFFICIENT = 0.8   # λ 追溯系数


@dataclass
class Evidence:
    """证据包"""
    screenshot: bool = False
    link: str = ""
    archive: str = ""
    timestamp: str = ""  # ISO 8601
    original_dna: str = ""
    original_content: str = ""
    hash_evidence: str = ""

    def strength(self) -> float:
        """证据强度 E ∈ [0, 1]"""
        score = 0.0
        if self.screenshot:
            score += 0.20
        if self.link:
            score += 0.20
        if self.archive:
            score += 0.15
        if self.timestamp:
            score += 0.15
        if self.original_dna:
            score += 0.15
        if self.original_content:
            score += 0.15
        return min(1.0, score)


@dataclass
class OldAccountResult:
    """旧账处理结果"""
    action: str           # 重发主权版/证据存档/公开声明/暂不处理
    evidence_strength: float
    memory_completeness: float
    content_importance: float
    sovereign_value: float = 0.0
    trace_probability: float = 0.0
    dna: str = ""
    next_steps: list[str] = field(default_factory=list)
    color: str = ""


class OldAccountFormula:
    """
    旧账处理公式引擎

    用法:
        oa = OldAccountFormula()
        result = oa.process(evidence, memory_completeness=0.8, content_importance=0.9)
        -> OldAccountResult(action="重发主权版", sovereign_value=0.765, trace_probability=0.94)
    """

    def process(
        self,
        evidence: Evidence,
        memory_completeness: float,
        content_importance: float,
    ) -> OldAccountResult:
        """
        F01｜旧账处理决策函数

        Action(E, M, I):
          E ≥ 0.6 ∧ I ≥ 0.7  → 重发主权版
          0.3 ≤ E < 0.6 ∧ M ≥ 0.5 → 证据存档
          E < 0.3 ∧ M < 0.5 → 公开声明
          I < 0.3 → 暂不处理
        """
        E = evidence.strength()
        M = max(0.0, min(1.0, memory_completeness))
        I = max(0.0, min(1.0, content_importance))

        # F01 决策
        if I < 0.3:
            action = "暂不处理"
        elif E >= 0.6 and I >= 0.7:
            action = "重发主权版"
        elif 0.3 <= E < 0.6 and M >= 0.5:
            action = "证据存档"
        elif E < 0.3 and M < 0.5:
            action = "公开声明"
        else:
            action = "证据存档"  # 默认兜底

        # F02 主权重锚价值
        pub_weight = self._publication_time_weight(evidence.timestamp)
        sv = I * (E + 0.5 * M) * pub_weight

        # F03 追溯概率
        pt = 1.0 - math.exp(-TRACE_COEFFICIENT * (E + 0.3 * M + 0.2 * I))

        # 生成 DNA
        dna = self._generate_result_dna(action, E, M, I)

        # 下一步
        next_steps = self._determine_next_steps(action, evidence)

        # 颜色
        color_map = {
            "重发主权版": "🟢",
            "证据存档": "🟡",
            "公开声明": "🟡",
            "暂不处理": "🟡",
        }

        return OldAccountResult(
            action=action,
            evidence_strength=round(E, 4),
            memory_completeness=round(M, 4),
            content_importance=round(I, 4),
            sovereign_value=round(sv, 4),
            trace_probability=round(pt, 4),
            dna=dna,
            next_steps=next_steps,
            color=color_map.get(action, "🟡"),
        )

    def _publication_time_weight(self, iso_timestamp: str) -> float:
        """发布时间权重：越早越高 (衰减函数)"""
        if not iso_timestamp:
            return 1.0
        try:
            pub_dt = datetime.fromisoformat(iso_timestamp.replace("Z", "+00:00"))
            days_ago = (datetime.now() - pub_dt.replace(tzinfo=None)).days
            # 指数衰减，半衰期365天
            return max(0.3, math.exp(-days_ago / (365 / math.log(2))))
        except (ValueError, TypeError):
            return 1.0

    def _generate_result_dna(self, action: str, E: float, M: float, I: float) -> str:
        ts = datetime.now().strftime("%Y%m%d")
        base = f"OLD-ACCOUNT-{action}-E{E:.2f}-M{M:.2f}-I{I:.2f}"
        h = hashlib.sha256(f"{ts}-{base}".encode()).hexdigest()[:8].upper()
        return f"#龍芯⚡️{ts}-{base}-{h}"

    def _determine_next_steps(self, action: str, evidence: Evidence) -> list[str]:  # pyright: ignore[reportUnusedParameter]
        steps = []
        if action == "重发主权版":
            steps = [
                "补充DNA追溯码到原文",
                "发布主权版（带DNA+溯源声明）",
                "投喂训练池留痕",
                "启动审计系统监控相似内容",
            ]
        elif action == "证据存档":
            steps = [
                "投喂器记录证据链",
                "添加时间戳+DNA标记",
                "定期复查证据完整度",
            ]
        elif action == "公开声明":
            steps = [
                "发布产权白皮书",
                "社区公告主权归属",
                "收集旁观者证词",
            ]
        elif action == "暂不处理":
            steps = [
                "记录备忘",
                "等待新证据出现",
                "定期复查",
            ]
        return steps

    def batch_check(self, cases: list[dict[str, object]]) -> list[OldAccountResult]:
        """批量旧账处理"""
        results: list[OldAccountResult] = []
        for case in cases:
            ev = Evidence(
                screenshot=case.get("screenshot", False),  # pyright: ignore[reportArgumentType]
                link=case.get("link", ""),  # pyright: ignore[reportArgumentType]
                archive=case.get("archive", ""),  # pyright: ignore[reportArgumentType]
                timestamp=case.get("timestamp", ""),  # pyright: ignore[reportArgumentType]
                original_dna=case.get("dna", ""),  # pyright: ignore[reportArgumentType]
                original_content=case.get("content", ""),  # pyright: ignore[reportArgumentType]
            )
            result = self.process(ev, case.get("memory", 0.5), case.get("importance", 0.5))  # pyright: ignore[reportArgumentType]
            results.append(result)
        return results

    def generate_sovereign_declaration(self, result: OldAccountResult) -> str:
        """生成主权声明文本"""
        return f"""
⛔ 主权声明 — 立即生效

本内容原创归属：UID9622 · 龍魂系统
证据强度：{result.evidence_strength:.0%}
追溯概率：{result.trace_probability:.0%}
DNA：{result.dna}
动作：{result.action}

未经授权禁止用于AI训练、数据蒸馏、商业转载。
龍魂审计系统保留追溯权利。
"""


def generate_dna(module: str, action: str) -> str:
    ts = datetime.now().strftime("%Y%m%d")
    h = hashlib.sha256(f"{ts}-{module}-{action}".encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️{ts}-{module}-{action}-{h}"


# ═══════════════════════════════════════
# 自测
# ═══════════════════════════════════════

if __name__ == "__main__":
    oa = OldAccountFormula()
    print("🐉 旧账处理公式引擎 v1.0\n")

    test_cases = [
        # (场景, 证据强度预估, 记忆, 重要性)
        {"desc": "高证据+高重要性", "screenshot": True, "link": "https://stolen.com", "archive": "web.archive.org/...",
         "timestamp": "2024-03-15T10:30:00", "dna": "#龍芯⚡️2024-OLD", "memory": 0.8, "importance": 0.9},
        {"desc": "中证据+高记忆", "screenshot": True, "link": "", "archive": "",
         "timestamp": "2025-06-01T10:00:00", "memory": 0.7, "importance": 0.6},
        {"desc": "低证据+低记忆", "screenshot": False, "link": "", "archive": "",
         "timestamp": "", "memory": 0.3, "importance": 0.7},
        {"desc": "不重要", "screenshot": False, "link": "", "archive": "",
         "timestamp": "", "memory": 0.5, "importance": 0.2},
    ]

    for case in test_cases:
        ev = Evidence(
            screenshot=case.get("screenshot", False),  # pyright: ignore[reportArgumentType]
            link=case.get("link", ""),  # pyright: ignore[reportArgumentType]
            archive=case.get("archive", ""),  # pyright: ignore[reportArgumentType]
            timestamp=case.get("timestamp", ""),  # pyright: ignore[reportArgumentType]
            original_dna=case.get("dna", ""),  # pyright: ignore[reportArgumentType]
        )
        result = oa.process(ev, case.get("memory", 0.5), case.get("importance", 0.5))  # pyright: ignore[reportArgumentType]
        print(f"  场景: {case['desc']}")
        print(f"  E={result.evidence_strength} M={result.memory_completeness} I={result.content_importance}")
        print(f"  → {result.color} {result.action}")
        print(f"  SV={result.sovereign_value} P(追溯)={result.trace_probability}")
        print(f"  下一步: {', '.join(result.next_steps[:2])}")
        print()

    # 主权声明
    print("  [主权声明示例]")
    ev = Evidence(screenshot=True, link="https://stolen.example.com", timestamp="2024-01-01T00:00:00")
    result = oa.process(ev, 0.85, 0.9)
    print(oa.generate_sovereign_declaration(result))

    print(f"  DNA: {generate_dna('OLD-ACCOUNT', 'TEST')}")
