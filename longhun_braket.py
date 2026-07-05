#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║  DNA追溯头（不可删除 · 删除即断链）                                       ║
# ║  DNA Trace Header (DO NOT DELETE · deletion breaks the chain)            ║
# ╚═══════════════════════════════════════════════════════════════════════════╝
# 龍芯⚡️2026-07-05-LONGHUN-BRAKET-v1.0
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 创始人: UID9622 · 龍芯北辰 · 诸葛鑫
# 理论来源: 【龍魂系统】曾老师智慧算法：用量子力学重构AI人格协作（Bra-Ket完整版）
# Notion: https://www.notion.so/uid9622/AI-Bra-Ket-3664bb869a0841478008c6c111b9289d

"""
龍魂 Bra-Ket 人格协作量子引擎 v1.0

用量子力学的狄拉克符号描述龍魂人格内阁的叠加态、测量坍缩与酉演化，
实现任务驱动的多人格自动协作权重分配。

用法:
    python3 longhun_braket.py --task "帮我做财务分析"
    python3 longhun_braket.py --task "设计一个高并发系统" --evolve 2.0
    python3 longhun_braket.py --list-personas
    python3 longhun_braket.py --demo
"""

import json
import math
import argparse
import hashlib
from pathlib import Path
from datetime import datetime
from types import SimpleNamespace
from typing import Dict, List, Optional, Tuple, Any

try:
    import numpy as np
    from scipy.linalg import expm
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False


class 人格态:
    """人格态 |P⟩，对应 Bra-Ket 中的右矢（列向量）"""

    def __init__(self, code: str, name: str, dimension: int = 8):
        self.code = code
        self.name = name
        self.dim = dimension
        self.ket = self._zero_ket()

    def _zero_ket(self):
        if HAS_NUMPY:
            return np.zeros(self.dim, dtype=complex)
        return [0.0 + 0.0j] * self.dim

    def __repr__(self):
        return f"|{self.code}:{self.name}⟩"

    def bra(self):
        """⟨self| = |self⟩†"""
        if HAS_NUMPY:
            return np.conj(self.ket)
        return [x.conjugate() for x in self.ket]

    def 内积(self, other: "人格态") -> complex:
        """⟨self|other⟩"""
        if HAS_NUMPY:
            return np.dot(self.bra(), other.ket)
        return sum(a * b for a, b in zip(self.bra(), other.ket))

    def 外积(self, other: "人格态"):
        """|self⟩⟨other|"""
        if HAS_NUMPY:
            return np.outer(self.ket, other.bra())
        return [[self.ket[i] * other.bra()[j] for j in range(self.dim)] for i in range(self.dim)]

    def 归一化(self) -> "人格态":
        """归一化 |ψ⟩ / ||ψ||"""
        if HAS_NUMPY:
            norm = np.sqrt(np.dot(self.bra(), self.ket).real)
            if norm > 1e-10:
                self.ket = self.ket / norm
        else:
            norm_sq = sum((x * x.conjugate()).real for x in self.ket)
            norm = math.sqrt(norm_sq)
            if norm > 1e-10:
                self.ket = [x / norm for x in self.ket]
        return self


class 测量结果:
    """任务场景测量后的坍缩结果，支持链式调用。"""

    def __init__(self, engine: "龍魂BraKet引擎", state: 人格态, scenario: str, weights: List[float]):
        self.engine = engine
        self.state = state
        self.场景 = scenario
        self.weights = weights

    def 酉演化(self, 时间: float = 1.0) -> "演化态":
        return self.engine._演化态(self.state, time=时间)

    def 协作概率(self) -> List[SimpleNamespace]:
        return [self.engine._概率对象(p) for p in self.engine.协作概率(self.state)]

    def 三色审计(self) -> SimpleNamespace:
        probs = self.engine.协作概率(self.state)
        audit = self.engine.三色审计(probs)
        return self.engine._审计对象(audit)


class 演化态:
    """经过酉演化后的状态，可读取协作概率与三色审计。"""

    def __init__(self, engine: "龍魂BraKet引擎", state: 人格态):
        self.engine = engine
        self.state = state

    def 协作概率(self) -> List[SimpleNamespace]:
        return [self.engine._概率对象(p) for p in self.engine.协作概率(self.state)]

    def 三色审计(self) -> SimpleNamespace:
        probs = self.engine.协作概率(self.state)
        audit = self.engine.三色审计(probs)
        return self.engine._审计对象(audit)


class 龍魂BraKet引擎:
    """龍芯量子人格协作系统"""

    DNA = "#龍芯⚡️2026-07-05-LONGHUN-BRAKET-v1.0"
    CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"

    # Bra-Ket 页面定义的 8 个基态人格（P00-P07）
    DEFAULT_PERSONAS = [
        ("P00", "文心", "战略核心态，元认知统筹"),
        ("P01", "诸葛亮", "推演态，战略推演"),
        ("P02", "宝宝", "执行态，情感协调+任务分配"),
        ("P03", "雯雯", "优化态，结构化整理"),
        ("P04", "鲁班", "技术态，技术执行"),
        ("P05", "上帝之眼", "监管态，三色审计+独立熔断权"),
        ("P06", "数学大师", "计算态，权重归一化计算"),
        ("P07", "管仲", "财务态，财务核算"),
    ]

    # 默认日常协作态权重（概率幅平方）
    DEFAULT_WEIGHTS = [0.10, 0.15, 0.30, 0.15, 0.10, 0.05, 0.05, 0.10]

    # 场景关键词 → 权重分布
    SCENARIO_WEIGHTS = {
        "财务": [0.05, 0.10, 0.15, 0.10, 0.05, 0.05, 0.10, 0.40],
        "战略": [0.30, 0.40, 0.10, 0.10, 0.05, 0.05, 0.00, 0.00],
        "规划": [0.30, 0.40, 0.10, 0.10, 0.05, 0.05, 0.00, 0.00],
        "技术": [0.10, 0.15, 0.15, 0.15, 0.40, 0.05, 0.00, 0.00],
        "代码": [0.10, 0.15, 0.15, 0.15, 0.40, 0.05, 0.00, 0.00],
        "审计": [0.05, 0.10, 0.10, 0.15, 0.05, 0.45, 0.10, 0.10],
        "计算": [0.05, 0.10, 0.10, 0.10, 0.05, 0.05, 0.50, 0.05],
        "数学": [0.05, 0.10, 0.10, 0.10, 0.05, 0.05, 0.50, 0.05],
    }

    COUPLING_STRENGTH = 0.1

    def __init__(
        self,
        base_dir: Optional[str] = None,
        use_registry: bool = True,
        personas: Optional[List[Dict[str, Any]]] = None,
        weights: Optional[List[float]] = None,
    ):
        self.base_dir = Path(base_dir) if base_dir else Path(__file__).parent
        self.timestamp = datetime.now().isoformat()
        self.personas: Dict[str, 人格态] = {}
        self.weights = list(self.DEFAULT_WEIGHTS)
        self.scenarios = dict(self.SCENARIO_WEIGHTS)
        self.dna = self._生成DNA()

        # 优先使用显式传入的人格定义
        if personas is not None:
            self._初始化自定义人格(personas, weights)
        elif use_registry:
            self._加载注册表()
        else:
            self._初始化默认人格()

    def _初始化默认人格(self):
        for idx, (code, name, desc) in enumerate(self.DEFAULT_PERSONAS):
            p = 人格态(code, name)
            p.ket = self._basis_vector(idx, len(self.DEFAULT_PERSONAS))
            p.desc = desc
            p.weight = self.DEFAULT_WEIGHTS[idx] if idx < len(self.DEFAULT_WEIGHTS) else 0.5
            self.personas[code] = p
        self.dim = len(self.DEFAULT_PERSONAS)

    def _初始化自定义人格(self, personas: List[Dict[str, Any]], weights: Optional[List[float]] = None):
        self.dim = len(personas)
        for idx, info in enumerate(personas):
            code = info.get("code", f"P{idx:02d}")
            name = info.get("name", code)
            p = 人格态(code, name, self.dim)
            p.ket = self._basis_vector(idx, self.dim)
            p.desc = info.get("role", info.get("duty", info.get("desc", "")))
            p.triggers = info.get("triggers", [])
            p.weight = float(info.get("weight", 0.5))
            self.personas[code] = p
        if weights is not None:
            self.weights = list(weights)[:self.dim]
            while len(self.weights) < self.dim:
                self.weights.append(0.0)
        else:
            total = sum(p.weight for p in self.personas.values())
            self.weights = [p.weight / total if total > 0 else 1.0 / self.dim for p in self.personas.values()]

    def _basis_vector(self, index: int, dim: int):
        if HAS_NUMPY:
            v = np.zeros(dim, dtype=complex)
            v[index] = 1.0
            return v
        v = [0.0 + 0.0j] * dim
        v[index] = 1.0
        return v

    def _加载注册表(self):
        registry_path = self.base_dir / "persona" / "persona_registry.json"
        if registry_path.exists():
            try:
                with open(registry_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                reg_personas = data.get("personas", {})
                if reg_personas:
                    items = sorted(reg_personas.items(), key=lambda x: x[0])
                    self.dim = len(items)
                    for idx, (code, info) in enumerate(items):
                        p = 人格态(code, info.get("name", code), self.dim)
                        p.ket = self._basis_vector(idx, self.dim)
                        p.desc = info.get("role", "")
                        p.triggers = info.get("triggers", [])
                        p.weight = info.get("weight", 0.5)
                        self.personas[code] = p
                    # 根据注册表权重生成默认概率分布
                    total = sum(p.weight for p in self.personas.values())
                    self.weights = [p.weight / total for p in self.personas.values()]
                    return
            except Exception as e:
                print(f"[WARN] 人格注册表加载失败: {e}，使用默认 Bra-Ket 8 人格")
        self._初始化默认人格()

    def _生成DNA(self) -> str:
        ts = datetime.now().strftime("%Y%m%d-%H%M%S")
        h = hashlib.sha256(f"{self.DNA}-{ts}-{self.CONFIRM}".encode()).hexdigest()[:8].upper()
        return f"{self.DNA}-{ts}-{h}"

    def 创建叠加态(self, weights: List[float], name: str = "龍芯叠加态") -> 人格态:
        """由概率权重构建归一化叠加态 |ψ⟩ = Σ α_i |P_i⟩"""
        dim = len(self.personas)
        weights = [float(w) for w in weights]
        # 把概率权重转为概率幅
        s = sum(weights)
        if s < 1e-10:
            weights = [1.0 / dim] * dim
        else:
            weights = [w / s for w in weights]
        amplitudes = [math.sqrt(w) for w in weights]

        state = 人格态("SUPER", name, dim)
        if HAS_NUMPY:
            state.ket = np.zeros(dim, dtype=complex)
        else:
            state.ket = [0.0 + 0.0j] * dim

        for i, (code, p) in enumerate(self.personas.items()):
            amp = amplitudes[i] if i < len(amplitudes) else 0.0
            if HAS_NUMPY:
                state.ket += amp * p.ket
            else:
                state.ket = [state.ket[j] + amp * p.ket[j] for j in range(dim)]
        return state.归一化()

    def _基于注册表生成权重(self, task: str) -> List[float]:
        """根据任务关键词匹配每个注册人格的 triggers，生成权重分布"""
        weights = []
        for code, p in self.personas.items():
            triggers = getattr(p, "triggers", [])
            role = getattr(p, "desc", "")
            score = 0.0
            for trigger in triggers:
                if trigger.lower() in task:
                    score += 1.0
            # role 字段也参与匹配
            if role and role.lower() in task:
                score += 2.0
            # 基础权重兜底
            base = getattr(p, "weight", 0.5)
            weights.append(base * 0.3 + score * 0.7)
        return weights

    def 场景测量(self, task: str) -> Tuple[人格态, str, List[float]]:
        """根据任务关键词进行场景识别（测量），返回坍缩后的初始态"""
        task = task.lower()
        matched_scenario = None
        for keyword in self.scenarios.keys():
            if keyword in task:
                matched_scenario = keyword
                break

        if matched_scenario is None:
            matched_scenario = "日常"

        # 如果使用注册表且人格数不等于默认8人格，动态生成权重
        if self.dim != len(self.DEFAULT_PERSONAS):
            weights = self._基于注册表生成权重(task)
        else:
            weights = self.scenarios.get(matched_scenario, self.weights)
            weights = list(weights)
            while len(weights) < self.dim:
                weights.append(0.0)
            weights = weights[:self.dim]

        state = self.创建叠加态(weights, name=f"{matched_scenario}场景态")
        return state, matched_scenario, weights

    def 构建哈密顿量(self) -> Any:
        """Ĥ = diag(固有能量) + 协作耦合（非对角）"""
        dim = self.dim
        if HAS_NUMPY:
            H = np.diag(self.weights[:dim])
            for i in range(dim):
                for j in range(i + 1, dim):
                    H[i, j] = self.COUPLING_STRENGTH
                    H[j, i] = self.COUPLING_STRENGTH
            return H
        else:
            H = [[0.0 + 0.0j] * dim for _ in range(dim)]
            for i in range(dim):
                H[i][i] = self.weights[i] if i < len(self.weights) else 0.0
            for i in range(dim):
                for j in range(i + 1, dim):
                    H[i][j] = self.COUPLING_STRENGTH
                    H[j][i] = self.COUPLING_STRENGTH
            return H

    def 酉演化(self, state: 人格态, time: float = 1.0) -> 人格态:
        """|ψ(t)⟩ = e^{-iĤt} |ψ(0)⟩"""
        H = self.构建哈密顿量()
        if HAS_NUMPY:
            U = expm(-1j * H * time)
            evolved = 人格态("EVOL", "演化态", self.dim)
            evolved.ket = U @ state.ket
        else:
            # 无 numpy 时退化为相位旋转
            evolved = 人格态("EVOL", "演化态", self.dim)
            evolved.ket = [state.ket[i] * complex(math.cos(H[i][i] * time), -math.sin(H[i][i] * time))
                           for i in range(self.dim)]
        return evolved.归一化()

    def 协作概率(self, state: 人格态) -> List[Dict[str, Any]]:
        """测量各人格基态的概率 |⟨P_i|ψ⟩|²"""
        probs = []
        for code, p in self.personas.items():
            amp = p.内积(state)
            prob = abs(amp) ** 2
            probs.append({
                "code": code,
                "name": p.name,
                "desc": getattr(p, "desc", ""),
                "amplitude": complex(amp),
                "probability": float(prob),
                "percentage": f"{prob * 100:.2f}%",
            })
        probs.sort(key=lambda x: x["probability"], reverse=True)
        return probs

    def 三色审计(self, probs: List[Dict[str, Any]], top_n: int = 3) -> Dict[str, Any]:
        """基于概率分布生成三色审计"""
        if not probs:
            return {"status": "🔴 失败", "reason": "无人格概率"}
        total_top3 = sum(p["probability"] for p in probs[:top_n])
        if total_top3 >= 0.8:
            status = "🟢 通过"
            reason = f"前 {top_n} 人格集中度 {total_top3 * 100:.1f}%，协作目标清晰"
        elif total_top3 >= 0.5:
            status = "🟡 提醒"
            reason = f"前 {top_n} 人格集中度 {total_top3 * 100:.1f}%，建议进一步聚焦"
        else:
            status = "🔴 熔断"
            reason = f"前 {top_n} 人格集中度 {total_top3 * 100:.1f}%，人格发散，需人工裁决"
        return {"status": status, "reason": reason, "top3_concentration": total_top3}

    @staticmethod
    def _概率对象(p: Dict[str, Any]) -> SimpleNamespace:
        """将概率字典包装为支持属性访问的对象（CNSH 友好）。"""
        return SimpleNamespace(
            代码=p.get("code", ""),
            名字=p.get("name", ""),
            描述=p.get("desc", ""),
            概率=p.get("probability", 0.0),
            百分比=p.get("percentage", "0.00%"),
            amplitude=p.get("amplitude", 0.0),
        )

    @staticmethod
    def _审计对象(audit: Dict[str, Any]) -> SimpleNamespace:
        """将审计字典包装为支持属性访问的对象（CNSH 友好）。"""
        return SimpleNamespace(
            状态=audit.get("status", ""),
            原因=audit.get("reason", ""),
            top3_concentration=audit.get("top3_concentration", 0.0),
        )

    def _演化态(self, state: 人格态, time: float = 1.0) -> 演化态:
        """返回支持链式调用的演化态对象。"""
        return 演化态(self, self.酉演化(state, time=time))

    def 测量(self, task: str) -> 测量结果:
        """CNSH 友好接口：场景测量 → 返回可链式调用的测量结果。"""
        state, scenario, weights = self.场景测量(task)
        return 测量结果(self, state, scenario, weights)

    def 执行任务(self, task: str, evolve_time: float = 1.0) -> Dict[str, Any]:
        """完整流程：场景测量 → 酉演化 → 概率分布 → 三色审计"""
        initial_state, scenario, weights = self.场景测量(task)
        evolved_state = self.酉演化(initial_state, time=evolve_time)
        probs = self.协作概率(evolved_state)
        audit = self.三色审计(probs)
        return {
            "dna": self.dna,
            "timestamp": self.timestamp,
            "task": task,
            "scenario": scenario,
            "dimension": self.dim,
            "persona_count": len(self.personas),
            "initial_state": str(initial_state),
            "evolved_state": str(evolved_state),
            "probabilities": probs,
            "audit": audit,
            "top_persona": probs[0]["name"] if probs else None,
        }

    def 人格列表(self) -> List[Dict[str, Any]]:
        return [{"code": p.code, "name": p.name, "desc": getattr(p, "desc", "")}
                for p in self.personas.values()]


def main():
    parser = argparse.ArgumentParser(description="龍魂 Bra-Ket 人格协作量子引擎")
    parser.add_argument("--task", "-t", type=str, help="任务描述，例如：帮我做财务分析")
    parser.add_argument("--evolve", "-e", type=float, default=1.0, help="演化时间（默认 1.0）")
    parser.add_argument("--json", "-j", action="store_true", help="输出 JSON 格式")
    parser.add_argument("--list-personas", action="store_true", help="列出人格基态")
    parser.add_argument("--demo", action="store_true", help="运行内置示例")
    parser.add_argument("--use-registry", action="store_true", default=True, help="加载 persona_registry.json")
    parser.add_argument("--no-registry", action="store_true", help="不使用人格注册表，使用默认8人格")
    args = parser.parse_args()

    if not HAS_NUMPY:
        print("[WARN] 未安装 numpy/scipy，将使用纯 Python 退化模式（无酉演化矩阵指数）")

    use_registry = not args.no_registry
    engine = 龍魂BraKet引擎(use_registry=use_registry)

    if args.list_personas:
        print(json.dumps(engine.人格列表(), ensure_ascii=False, indent=2))
        return

    if args.demo:
        tasks = [
            "帮我做财务分析",
            "设计一个高并发系统架构",
            "审计这段代码有没有安全漏洞",
            "计算这个模型的权重分布",
        ]
        results = []
        for task in tasks:
            result = engine.执行任务(task, evolve_time=args.evolve)
            results.append(result)
        print(json.dumps(results, ensure_ascii=False, indent=2, default=str))
        return

    if not args.task:
        parser.print_help()
        return

    result = engine.执行任务(args.task, evolve_time=args.evolve)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    else:
        print(f"\n🌌 龍魂 Bra-Ket 人格协作结果")
        print(f"DNA: {result['dna']}")
        print(f"任务: {result['task']}")
        print(f"识别场景: {result['scenario']}")
        print(f"人格维度: {result['dimension']}")
        print(f"\n协作概率分布:")
        for p in result['probabilities']:
            bar = "█" * int(p['probability'] * 30)
            print(f"  {p['name']:8s} {p['percentage']:>7s} {bar}")
        print(f"\n主执行人格: {result['top_persona']}")
        print(f"三色审计: {result['audit']['status']} · {result['audit']['reason']}")


if __name__ == "__main__":
    main()
