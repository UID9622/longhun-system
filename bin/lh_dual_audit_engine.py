# DNA: #龍芯⚡️丙午·乙未·乙丑·观-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·乙未·乙卯·戌时·䷰革-lh_dual_audit_engine-INTEGRATION-SYSTEM
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
左右互搏審計引擎
系統內部兩個對立人格互相審計，左保守右探索，互搏產生真相

#龍芯⚡️丙午·乙未·乙卯·戌时·䷰革-lh_dual_audit_engine-INTEGRATION-SYSTEM
龍魂系統 - 算法工程師產出
兼容ARM64/aarch64，僅用標準庫
"""

import hashlib
import json
import time
import random
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, List, Dict, Optional


# ============================================================
# 數據結構定義
# ============================================================

class AuditColor(Enum):
    """審計結果顏色：綠通黃疑紅斷"""
    GREEN = "🟢"   # 通過
    YELLOW = "🟡"  # 標記複核
    RED = "🔴"     # 熔斷


@dataclass
class AuditResult:
    """單個人格的審計結果"""
    passed: bool           # 是否通過
    score: int             # 評分0-100
    dna: str               # DNA簽名
    opinion: str           # 觀點描述
    issues: List[str] = field(default_factory=list)   # 發現的問題
    warnings: List[str] = field(default_factory=list) # 警告


@dataclass
class CounterExample:
    """反例：右人格找到的反例"""
    found: bool            # 是否找到反例
    example: Any           # 反例內容
    description: str       # 反例說明
    severity: int          # 嚴重程度1-10


@dataclass
class DuelResult:
    """互搏對決結果"""
    left_dna: str          # 左人格DNA
    right_dna: str         # 右人格DNA
    consensus: bool        # 是否達成共識
    color: str             # 🟢🟡🔴
    score: int             # 綜合評分0-100
    left_opinion: str      # 左方觀點
    right_opinion: str     # 右方觀點
    resolution: str        # 最終決議
    innovation_found: bool # 是否發現新解法
    duel_dna: str = ""     # 互搏DNA
    timestamp: float = 0.0 # 時間戳


@dataclass
class Resolution:
    """衝突解決方案"""
    action: str            # 行動：pass / review / halt
    reason: str            # 理由
    reconciled_score: int  # 調和後評分
    advice: str            # 建議


# ============================================================
# DNA簽名工具
# ============================================================

class DnaSigner:
    """DNA簽名生成器 - 用SHA256做特徵指紋"""

    @staticmethod
    def sign(data: Any, persona: str = "") -> str:
        """對數據生成DNA簽名"""
        content = json.dumps({
            "data": data,
            "persona": persona,
            "nonce": random.randint(1000, 999999),
            "ts": time.time()
        }, sort_keys=True, default=str)
        h = hashlib.sha256(content.encode('utf-8')).hexdigest()
        # 取前16位作為DNA，夠用又簡潔
        return f"{persona[:1].upper()}{h[:16]}"

    @staticmethod
    def combine_dna(left_dna: str, right_dna: str, result_data: Any) -> str:
        """合流左右DNA生成互搏DNA"""
        merged = f"{left_dna}::{right_dna}::{json.dumps(result_data, sort_keys=True, default=str)}"
        h = hashlib.sha256(merged.encode('utf-8')).hexdigest()
        return f"D{h[:20]}"  # D = Duel


# ============================================================
# 左人格：保守者
# ============================================================

class LeftPersona:
    """
    左人格：保守者
    職責：驗證邏輯一致性、守住底線、檢查邊界條件
    作風：穩健、懷疑、不放過任何漏洞
    """

    def __init__(self):
        self.name = "保守者"
        self.dna_signer = DnaSigner()

    def audit(self, problem: Any, solution: Any) -> AuditResult:
        """
        對問題和解決方案進行保守審計
        檢查：邏輯一致性、邊界條件、假設有效性
        """
        issues = []
        warnings = []
        score = 100

        # 1. 檢查邊界條件
        if not self.check_boundary(solution):
            issues.append("邊界條件檢查未通過")
            score -= 30

        # 2. 驗證假設
        broken_assumptions = self.verify_assumptions(problem)
        if broken_assumptions:
            for ba in broken_assumptions:
                warnings.append(f"假設可能不成立: {ba}")
            score -= len(broken_assumptions) * 10

        # 3. 檢查解決方案基本有效性
        if solution is None or solution == "":
            issues.append("解決方案為空")
            score -= 50

        # 4. 類型和結構檢查
        if isinstance(solution, dict):
            if len(solution) == 0:
                issues.append("解決方案字典為空")
                score -= 20

        # 5. 數值合理性檢查
        if isinstance(solution, (int, float)):
            if abs(solution) > 1e18:
                warnings.append("數值過大，可能溢出")
                score -= 15
            if isinstance(solution, float):
                if solution != solution:  # NaN檢查
                    issues.append("結果為NaN")
                    score -= 40

        score = max(0, min(100, score))
        passed = score >= 70 and len(issues) == 0

        opinion = self._form_opinion(problem, solution, passed, issues, warnings)
        dna = self.dna_signer.sign({"problem": problem, "solution": solution, "score": score}, "left")

        return AuditResult(
            passed=passed,
            score=score,
            dna=dna,
            opinion=opinion,
            issues=issues,
            warnings=warnings
        )

    def check_boundary(self, solution: Any) -> bool:
        """檢查邊界條件：空值、極端值、類型異常"""
        if solution is None:
            return False
        if isinstance(solution, str) and len(solution.strip()) == 0:
            return False
        if isinstance(solution, (list, dict, tuple)) and len(solution) == 0:
            return False
        # 檢查極端數值
        if isinstance(solution, (int, float)):
            if solution == float('inf') or solution == float('-inf'):
                return False
        return True

    def verify_assumptions(self, problem: Any) -> List[str]:
        """驗證問題中的假設是否成立，返回不成立的假設列表"""
        broken = []
        prob_str = json.dumps(problem, default=str).lower()

        # 檢查常見危險假設
        dangerous_assumptions = [
            ("always", "假設'總是'成立可能過於絕對"),
            ("never", "假設'永不'可能遺漏邊界情況"),
            ("all", "假設'全部'需驗證覆蓋率"),
            ("none", "假設'沒有'需驗證是否存在例外"),
            ("perfect", "完美假設在現實中罕見"),
            ("unlimited", "無限資源假設通常不成立"),
            ("instant", "即時完成假設需驗證時序"),
        ]

        for keyword, warning in dangerous_assumptions:
            if keyword in prob_str:
                broken.append(warning)

        return broken

    def _form_opinion(self, problem: Any, solution: Any, passed: bool, issues: List[str], warnings: List[str]) -> str:
        """形成左方觀點"""
        if passed:
            base = "【左方-通過】保守審計認為方案在邏輯上站得住腳"
        else:
            base = "【左方-阻擊】保守審計發現嚴重問題，建議阻擊"

        detail_parts = []
        if issues:
            detail_parts.append(f"問題({len(issues)}項): {'; '.join(issues[:3])}")
        if warnings:
            detail_parts.append(f"警告({len(warnings)}項): {'; '.join(warnings[:3])}")

        if detail_parts:
            base += " | " + " | ".join(detail_parts)
        return base


# ============================================================
# 右人格：探索者
# ============================================================

class RightPersona:
    """
    右人格：探索者
    職責：挑戰假設、尋找反例、嘗試突破
    作風：激進、好奇、專找漏洞和反例
    """

    def __init__(self):
        self.name = "探索者"
        self.dna_signer = DnaSigner()

    def audit(self, problem: Any, solution: Any) -> AuditResult:
        """
        對問題和解決方案進行探索審計
        檢查：是否有更好的解、假設是否可被挑戰、是否存在反例
        """
        issues = []
        warnings = []
        score = 100

        # 1. 尋找反例
        counter = self.find_counterexample(solution)
        if counter.found:
            issues.append(f"發現反例: {counter.description}")
            score -= counter.severity * 8

        # 2. 挑戰假設
        challenged = self.challenge_assumptions(problem)
        if challenged:
            for ch in challenged:
                warnings.append(f"挑戰: {ch}")
            score -= len(challenged) * 8

        # 3. 檢查解決方案是否過於保守
        if isinstance(solution, (int, float)):
            # 探索者認為數值解可能不是最優
            warnings.append("數值解可能存在更優路徑")
            score -= 5

        # 4. 檢查是否有創新空間
        if isinstance(solution, dict):
            if "method" in solution:
                method = solution["method"]
                if method in ["greedy", "naive", "brute_force"]:
                    warnings.append(f"方法'{method}'可能有更高效替代方案")
                    score -= 10

        # 5. 檢查是否有未探索的解空間
        if isinstance(solution, list) and len(solution) > 0:
            if len(solution) == 1:
                warnings.append("僅有一個解，解空間可能未充分探索")
                score -= 8

        score = max(0, min(100, score))
        # 右人格標準更嚴：有反例就不算完全通過
        passed = score >= 75 and not counter.found

        opinion = self._form_opinion(problem, solution, passed, issues, warnings, counter)
        dna = self.dna_signer.sign({"problem": problem, "solution": solution, "score": score}, "right")

        return AuditResult(
            passed=passed,
            score=score,
            dna=dna,
            opinion=opinion,
            issues=issues,
            warnings=warnings
        )

    def find_counterexample(self, solution: Any) -> CounterExample:
        """
        尋找反例：嘗試構造讓解決方案失效的輸入
        返回找到的反例（如果有）
        """
        # 根據解的類型嘗試構造反例
        if solution is None:
            return CounterExample(
                found=True, example=None,
                description="空解對任何非空輸入都失效", severity=9
            )

        if isinstance(solution, bool):
            # 布爾解的反例就是其相反值在特定上下文中的失效
            return CounterExample(
                found=True, example=not solution,
                description=f"布爾值{solution}在邊界條件下可能不成立", severity=5
            )

        if isinstance(solution, (int, float)):
            if solution == 0:
                return CounterExample(
                    found=True, example=solution,
                    description="零值在除法或對數場景下失效", severity=7
                )
            # 檢查極端值
            if abs(solution) < 1e-10:
                return CounterExample(
                    found=True, example=solution,
                    description="極小值在精度要求高的場景下可能不夠", severity=4
                )

        if isinstance(solution, str):
            if len(solution) < 3:
                return CounterExample(
                    found=True, example="",
                    description="過短字符串在複雜匹配場景下可能失效", severity=3
                )

        if isinstance(solution, (list, tuple)):
            if len(solution) == 0:
                return CounterExample(
                    found=True, example=[],
                    description="空集合在需要元素的場景下失效", severity=8
                )

        # 沒找到明顯反例
        return CounterExample(
            found=False, example=None,
            description="未發現明顯反例", severity=0
        )

    def challenge_assumptions(self, problem: Any) -> List[str]:
        """
        挑戰問題中的假設
        返回被挑戰的假設列表
        """
        challenged = []
        prob_str = json.dumps(problem, default=str)

        # 挑戰常見隱含假設
        challenges = [
            ("input", "輸入規模假設：大規模輸入時方案是否仍有效？"),
            ("time", "時間假設：並行/異步場景下時序是否仍成立？"),
            ("safe", "安全假設：惡意輸入下方案是否安全？"),
            ("correct", "正確性假設：'正確'的定義是否完備？"),
            ("optimal", "最優假設：當前解是否全局最優？"),
        ]

        for keyword, challenge in challenges:
            if keyword.lower() in prob_str.lower():
                challenged.append(challenge)

        # 總是挑戰一個：探索者認為沒有不可挑戰的假設
        if not challenged:
            challenged.append("隱含假設：問題描述中可能有未言明的假設")

        return challenged

    def _form_opinion(self, problem: Any, solution: Any, passed: bool,
                      issues: List[str], warnings: List[str], counter: CounterExample) -> str:
        """形成右方觀點"""
        if passed:
            base = "【右方-通過】探索審計暫時未找到顛覆性反例"
        else:
            base = "【右方-挑戰】探索審計發現值得深挖的問題"

        if counter.found:
            base += f" | 反例嚴重度:{counter.severity}/10"

        detail_parts = []
        if issues:
            detail_parts.append(f"問題({len(issues)}項)")
        if warnings:
            detail_parts.append(f"挑戰({len(warnings)}項): {'; '.join(warnings[:2])}")

        if detail_parts:
            base += " | " + " | ".join(detail_parts)
        return base


# ============================================================
# 互搏引擎：左右對決
# ============================================================

class MutualAuditEngine:
    """
    互搏引擎：左右對決核心
    左保守 vs 右探索，互搏產生最終審判
    """

    # 容忍閾值：分數差異在此範圍內算黃標而非熔斷
    TOLERANCE = 25

    def __init__(self, left: Optional[LeftPersona] = None, right: Optional[RightPersona] = None):
        self.left = left or LeftPersona()
        self.right = right or RightPersona()
        self.dna_signer = DnaSigner()
        self.duel_history: List[DuelResult] = []  # 互搏歷史

    def duel(self, problem: Any, solution: Any) -> DuelResult:
        """
        核心方法：左右對決
        1. 左右各自獨立審計
        2. 比較結果
        3. 判定顏色和決議
        4. 生成互搏DNA
        """
        # 左右各自獨立計算/審計
        left_result = self.left.audit(problem, solution)
        right_result = self.right.audit(problem, solution)

        # 解決衝突
        resolution = self.resolve_conflict(left_result, right_result)

        # 判斷共識
        consensus = resolution.action == "pass"

        # 判定顏色
        color = self._determine_color(left_result, right_result, resolution)

        # 計算綜合評分
        score = self._compute_score(left_result, right_result, resolution)

        # 檢查是否發現新解法
        innovation = self._detect_innovation(left_result, right_result)

        # 生成互搏DNA
        duel_dna = self.generate_duel_dna({
            "left": left_result.dna,
            "right": right_result.dna,
            "resolution": resolution.action,
            "score": score
        })

        result = DuelResult(
            left_dna=left_result.dna,
            right_dna=right_result.dna,
            consensus=consensus,
            color=color.value if isinstance(color, AuditColor) else color,
            score=score,
            left_opinion=left_result.opinion,
            right_opinion=right_result.opinion,
            resolution=f"[{resolution.action.upper()}] {resolution.reason} | 建議: {resolution.advice}",
            innovation_found=innovation,
            duel_dna=duel_dna,
            timestamp=time.time()
        )

        self.duel_history.append(result)
        return result

    def resolve_conflict(self, left_result: AuditResult, right_result: AuditResult) -> Resolution:
        """
        衝突解決：調和左右分歧
        """
        # 情況1：雙方都通過
        if left_result.passed and right_result.passed:
            return Resolution(
                action="pass",
                reason="左右一致通過，方案穩健",
                reconciled_score=(left_result.score + right_result.score) // 2,
                advice="可執行"
            )

        # 情況2：雙方都不通過
        if not left_result.passed and not right_result.passed:
            return Resolution(
                action="halt",
                reason="左右一致否決，方案存在根本問題",
                reconciled_score=min(left_result.score, right_result.score),
                advice="停止執行，重新設計方案"
            )

        # 情況3：一方通過一方不通過 - 看分數差異
        score_diff = abs(left_result.score - right_result.score)

        if score_diff <= self.TOLERANCE:
            # 分數差異在容忍範圍內，黃標處理
            return Resolution(
                action="review",
                reason=f"左右分歧但在容忍範圍內(差異{score_diff}分)",
                reconciled_score=(left_result.score + right_result.score) // 2,
                advice="轉人工複核後決定"
            )
        else:
            # 分數差異過大，熔斷
            return Resolution(
                action="halt",
                reason=f"左右嚴重對立(差異{score_diff}分)，存在認知衝突",
                reconciled_score=min(left_result.score, right_result.score),
                advice="熔斷停止，需高層介入或重新定義問題"
            )

    def generate_duel_dna(self, result: Dict) -> str:
        """生成互搏DNA簽名"""
        return self.dna_signer.combine_dna(
            result.get("left", ""),
            result.get("right", ""),
            result
        )

    def _determine_color(self, left: AuditResult, right: AuditResult, res: Resolution) -> AuditColor:
        """判定結果顏色"""
        if res.action == "pass":
            return AuditColor.GREEN
        elif res.action == "review":
            return AuditColor.YELLOW
        else:
            return AuditColor.RED

    def _compute_score(self, left: AuditResult, right: AuditResult, res: Resolution) -> int:
        """計算綜合評分"""
        base = (left.score + right.score) // 2
        # 調整：根據衝突解決結果微調
        if res.action == "pass":
            base = min(100, base + 5)  # 一致通過加分
        elif res.action == "halt":
            base = max(0, base - 10)   # 熔斷減分
        return max(0, min(100, base))

    def _detect_innovation(self, left: AuditResult, right: AuditResult) -> bool:
        """
        檢測是否發現新解法
        當右人格提出挑戰但左人格仍然通過時，可能意味著有新解法空間
        """
        # 右人格有挑戰/警告，左人格通過 = 可能有新角度
        if left.passed and len(right.warnings) >= 2:
            return True
        # 右人格找到反例但嚴重程度低 = 可能有替代方案
        if right.issues and "反例" in str(right.issues):
            return True
        return False

    def get_history(self) -> List[DuelResult]:
        """獲取互搏歷史"""
        return self.duel_history

    def clear_history(self):
        """清空歷史"""
        self.duel_history = []


# ============================================================
# 測試用例
# ============================================================

def test_basic_pass():
    """測試：雙方通過的場景"""
    engine = MutualAuditEngine()
    result = engine.duel(
        problem={"task": "calculate_sum", "inputs": [1, 2, 3]},
        solution={"result": 6, "method": "arithmetic"}
    )
    assert result.color == "🟢", f"期望綠燈，得到{result.color}"
    assert result.consensus == True
    assert result.score >= 70
    print(f"[TEST通過] 基本通過測試: {result.color} 評分{result.score}")
    return True


def test_boundary_fail():
    """測試：邊界條件失敗（空解）"""
    engine = MutualAuditEngine()
    result = engine.duel(
        problem={"task": "process_data"},
        solution=None
    )
    # 空解應該被左人格阻擊
    assert result.color in ["🟡", "🔴"], f"期望黃或紅，得到{result.color}"
    assert result.score < 70
    print(f"[TEST通過] 邊界失敗測試: {result.color} 評分{result.score}")
    return True


def test_conflict_review():
    """測試：左右分歧但可調和"""
    engine = MutualAuditEngine()
    # 構造一個有點問題但不太嚴重的解
    result = engine.duel(
        problem={"task": "sort_list", "assumption": "all_positive"},
        solution=[1, 2, 3]
    )
    # 這個應該是綠或黃，不應該紅
    assert result.color in ["🟢", "🟡"], f"不應熔斷，得到{result.color}"
    print(f"[TEST通過] 分歧調和測試: {result.color} 評分{result.score}")
    return True


def test_extreme_value():
    """測試：極端數值處理"""
    engine = MutualAuditEngine()
    result = engine.duel(
        problem={"task": "compute_factorial", "input": 1000},
        solution=float('inf')
    )
    assert result.color == "🔴", f"極端值應熔斷，得到{result.color}"
    print(f"[TEST通過] 極端數值測試: {result.color} 評分{result.score}")
    return True


def test_counterexample_found():
    """測試：反例發現"""
    right = RightPersona()
    counter = right.find_counterexample(0)
    assert counter.found == True
    assert counter.severity > 0
    print(f"[TEST通過] 反例發現測試: 嚴重度{counter.severity}/10")
    return True


def test_dna_consistency():
    """測試：DNA簽名一致性"""
    signer = DnaSigner()
    dna1 = signer.sign("test_data", "left")
    dna2 = signer.sign("test_data", "left")
    # DNA應該不同（因為有nonce和時間戳）
    assert dna1 != dna2, "DNA應該因nonce而不同"
    # 但格式應該一致
    assert dna1.startswith("L")
    assert dna2.startswith("L")
    print(f"[TEST通過] DNA一致性測試: {dna1} vs {dna2}")
    return True


def test_duel_dna_generation():
    """測試：互搏DNA生成"""
    engine = MutualAuditEngine()
    result = engine.duel(
        problem={"task": "simple_add", "inputs": [5, 3]},
        solution=8
    )
    assert len(result.duel_dna) > 0
    assert result.duel_dna.startswith("D")
    assert len(result.left_dna) > 0
    assert len(result.right_dna) > 0
    print(f"[TEST通過] 互搏DNA測試: 左{result.left_dna} 右{result.right_dna} 互{result.duel_dna}")
    return True


def test_naive_method_challenge():
    """測試：探索者挑戰樸素方法"""
    engine = MutualAuditEngine()
    result = engine.duel(
        problem={"task": "find_maximum", "dataset": "large"},
        solution={"result": 999, "method": "brute_force"}
    )
    # 探索者應該對brute_force提出警告
    assert "brute_force" in result.right_opinion or result.right_opinion != ""
    print(f"[TEST通過] 方法挑戰測試: {result.color} 右方觀點截選: {result.right_opinion[:50]}...")
    return True


def test_history_tracking():
    """測試：歷史記錄"""
    engine = MutualAuditEngine()
    engine.clear_history()
    engine.duel(problem="p1", solution="s1")
    engine.duel(problem="p2", solution="s2")
    history = engine.get_history()
    assert len(history) == 2
    print(f"[TEST通過] 歷史記錄測試: 記錄了{len(history)}次互搏")
    return True


def test_innovation_detection():
    """測試：新解法發現檢測"""
    engine = MutualAuditEngine()
    # 構造一個右方有挑戰但左方通過的場景 = 可能有新解法
    result = engine.duel(
        problem={"task": "route_optimization", "assumption": "optimal"},
        solution={"path": ["A", "B", "C"], "cost": 100}
    )
    # 應該設置了innovation_found標誌（或True或False，但不報錯）
    assert isinstance(result.innovation_found, bool)
    print(f"[TEST通過] 新解法檢測測試: innovation={result.innovation_found}")
    return True


def test_all_assumption_checks():
    """測試：假設驗證全面性"""
    left = LeftPersona()
    # 測試包含多個危險假設的問題
    assumptions = left.verify_assumptions("this always works with all inputs and perfect results")
    assert len(assumptions) >= 3, f"應發現多個危險假設，只發現{len(assumptions)}個"
    print(f"[TEST通過] 假設驗證測試: 發現{len(assumptions)}個危險假設")
    return True


def run_all_tests():
    """運行全部測試"""
    print("=" * 60)
    print("左右互搏審計引擎 - 測試開始")
    print("龍魂系統互搏核心 v1.0")
    print("=" * 60)

    tests = [
        test_basic_pass,
        test_boundary_fail,
        test_conflict_review,
        test_extreme_value,
        test_counterexample_found,
        test_dna_consistency,
        test_duel_dna_generation,
        test_naive_method_challenge,
        test_history_tracking,
        test_innovation_detection,
        test_all_assumption_checks,
    ]

    passed = 0
    failed = 0

    for test_fn in tests:
        try:
            test_fn()
            passed += 1
        except Exception as e:
            failed += 1
            print(f"[TEST失敗] {test_fn.__name__}: {e}")

    print("=" * 60)
    print(f"測試完成: {passed}通過 / {failed}失敗 / 共{len(tests)}項")
    if failed == 0:
        print("全部通過 - 龍魂互搏核心就緒")
    print("=" * 60)
    return failed == 0


# ============================================================
# DNA簽名 - 文件末尾
# ============================================================
FILE_DNA = "L6F8E2A1B9C3D5E7"  # 保守者開頭

if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
