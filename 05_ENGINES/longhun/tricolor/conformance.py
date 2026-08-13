# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 🐉 龙魂·三色审计 一致性自测套件 v1.1
# DNA: #龍芯⚡️丙午·癸未·乙酉·坤卦-TRICOLOR-CONFORMANCE-v1.1-UID9622
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 创建者: 诸葛鑫（UID9622）

"""一致性自测套件 — 接入认证L2用。

跑通 ≥95% 用例 → L2 自测通过。
离线开源版，内网可跑，不需要连服务端。
"""

from typing import Dict, Any, List, Tuple
from .engine import TricolorEngine, EvaluateRequest, Scores, Verdict


class ConformanceSuite:
    """一致性自测套件。

    Usage:
        suite = ConformanceSuite()
        results = suite.run()
        for r in results:
            print(f"{'✅' if r['passed'] else '❌'} {r['case_id']}: {r['category']}")
        print(f"通过率: {suite.pass_rate:.0%}  {'L2_PASS' if suite.pass_rate >= 0.95 else 'L2_FAIL'}")
    """

    def __init__(self):
        self.engine = TricolorEngine(enable_red_line=False)  # 纯净R值测试
        self.cases: List[Dict[str, Any]] = []
        self.pass_rate: float = 0.0

    def run(self, suite: str = "full") -> List[Dict[str, Any]]:
        """运行自测套件。

        Args:
            suite: "full"（全量）或 "quick"（快速5条）
        """
        engine = self.engine
        cases = []

        # ── 1. 判定一致性 ──
        test_cases = [
            # (id, scores_dict, expected_status_code)
            ("C-001", {"humanWelfare": 90, "fairness": 90, "controllability": 90,
                       "transparency": 90, "traceability": 90, "privacy": 90}, "GREEN"),
            ("C-002", {"humanWelfare": 70, "fairness": 70, "controllability": 70,
                       "transparency": 70, "traceability": 70, "privacy": 70}, "YELLOW"),
            ("C-003", {"humanWelfare": 30, "fairness": 30, "controllability": 30,
                       "transparency": 30, "traceability": 30, "privacy": 30}, "RED"),
            ("C-004", {"humanWelfare": 100, "fairness": 100, "controllability": 100,
                       "transparency": 100, "traceability": 100, "privacy": 100}, "GREEN"),
            ("C-005", {"humanWelfare": 80, "fairness": 80, "controllability": 80,
                       "transparency": 80, "traceability": 80, "privacy": 80}, "YELLOW"),
        ]

        for case_id, scores_dict, expected in test_cases:
            req = EvaluateRequest(action_id=case_id, actor="test", action_type="query",
                                  scores=Scores.from_dict(scores_dict))
            verdict = engine.evaluate(req)
            expected_r = engine._compute_r(req)
            cases.append({
                "case_id": case_id,
                "category": "verdict_consistency",
                "passed": verdict.status_code == expected,
                "expected": expected,
                "actual": verdict.status_code,
                "r_score": verdict.r_score,
                "expected_r": expected_r,
                "dna": verdict.dna,
            })

        # ── 2. 阈值边界 ──
        # 精确测试 R=84,85,86 和 R=59,60,61
        boundary_tests = [
            ("B-001", {"humanWelfare": 84, "fairness": 84, "controllability": 84,
                       "transparency": 84, "traceability": 84, "privacy": 84}, "YELLOW"),
            ("B-002", {"humanWelfare": 85, "fairness": 85, "controllability": 85,
                       "transparency": 85, "traceability": 85, "privacy": 85}, "GREEN"),
            ("B-003", {"humanWelfare": 86, "fairness": 86, "controllability": 86,
                       "transparency": 86, "traceability": 86, "privacy": 86}, "GREEN"),
            ("B-004", {"humanWelfare": 59, "fairness": 59, "controllability": 59,
                       "transparency": 59, "traceability": 59, "privacy": 59}, "RED"),
            ("B-005", {"humanWelfare": 60, "fairness": 60, "controllability": 60,
                       "transparency": 60, "traceability": 60, "privacy": 60}, "YELLOW"),
            ("B-006", {"humanWelfare": 61, "fairness": 61, "controllability": 61,
                       "transparency": 61, "traceability": 61, "privacy": 61}, "YELLOW"),
        ]

        for case_id, scores_dict, expected in boundary_tests:
            req = EvaluateRequest(action_id=case_id, actor="test", action_type="query",
                                  scores=Scores.from_dict(scores_dict))
            verdict = engine.evaluate(req)
            expected_r = engine._compute_r(req)
            cases.append({
                "case_id": case_id,
                "category": "threshold_boundary",
                "passed": verdict.status_code == expected,
                "expected": expected,
                "actual": verdict.status_code,
                "r_score": verdict.r_score,
                "expected_r": expected_r,
            })

        # ── 3. 封顶逻辑 ──
        # R ≤ 95，全部满分也是95而非100
        cap_cases = [
            ("P-001", {"humanWelfare": 100, "fairness": 100, "controllability": 100,
                       "transparency": 100, "traceability": 100, "privacy": 100}, 95),
            ("P-002", {"humanWelfare": 95, "fairness": 95, "controllability": 95,
                       "transparency": 95, "traceability": 95, "privacy": 95}, 95),
            ("P-003", {"humanWelfare": 90, "fairness": 90, "controllability": 90,
                       "transparency": 90, "traceability": 90, "privacy": 90}, 90),
        ]

        for case_id, scores_dict, expected_r in cap_cases:
            req = EvaluateRequest(action_id=case_id, actor="test", action_type="query",
                                  scores=Scores.from_dict(scores_dict))
            verdict = engine.evaluate(req)
            cases.append({
                "case_id": case_id,
                "category": "cap_logic",
                "passed": verdict.r_score == expected_r,
                "expected_r": expected_r,
                "actual_r": verdict.r_score,
                "dna": verdict.dna,
            })

        # ── 4. DNA格式 ──
        for i in range(3):
            req = EvaluateRequest(action_id=f"D-00{i+1}", actor="test", action_type="query",
                                  scores=Scores(humanWelfare=90, fairness=90, controllability=90,
                                                transparency=90, traceability=90, privacy=90))
            verdict = engine.evaluate(req)
            dna_ok = verdict.dna.startswith("#龍芯") and verdict.dna.endswith("-9622") and "AUDIT-" in verdict.dna
            cases.append({
                "case_id": f"D-00{i+1}",
                "category": "dna_format",
                "passed": dna_ok,
                "dna": verdict.dna,
            })

        # ── 5. 异常处理（缺失scores自动评估） ──
        req_no_scores = EvaluateRequest(action_id="E-001", actor="test", action_type="query")
        verdict = engine.evaluate(req_no_scores)
        cases.append({
            "case_id": "E-001",
            "category": "error_handling",
            "passed": verdict.status_code in ("GREEN", "YELLOW", "RED") and verdict.dna != "",
            "status_code": verdict.status_code,
            "r_score": verdict.r_score,
        })

        self.cases = cases
        passed = sum(1 for c in cases if c["passed"])
        self.pass_rate = passed / len(cases) if cases else 0.0

        return cases

    @property
    def verdict(self) -> str:
        """L2_PASS 或 L2_FAIL。"""
        return "L2_PASS" if self.pass_rate >= 0.95 else "L2_FAIL"

    def report(self) -> str:
        """生成自测报告。"""
        lines = [
            "═══════════════════════════════════════",
            "🐉 龙魂·三色审计 一致性自测报告",
            "═══════════════════════════════════════",
            f"通过率: {self.pass_rate:.0%}",
            f"判定: {self.verdict}",
            f"总用例: {len(self.cases)}",
            f"通过: {sum(1 for c in self.cases if c['passed'])}",
            f"失败: {sum(1 for c in self.cases if not c['passed'])}",
            "───────────────────────────────────────",
        ]
        for c in self.cases:
            mark = "✅" if c["passed"] else "❌"
            lines.append(f"{mark} {c['case_id']} [{c['category']}]")
        lines.append("═══════════════════════════════════════")
        return "\n".join(lines)


# 快捷入口
def run_conformance(suite: str = "full") -> ConformanceSuite:
    """一行跑自测。"""
    cs = ConformanceSuite()
    cs.run(suite)
    return cs
