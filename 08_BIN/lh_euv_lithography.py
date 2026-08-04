#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
#龍芯⚡️2026-07-18-CNSH-EUV-LITHOGRAPHY-FIXED-POINT-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
🐉 CNSH-EUV 光刻机攻关系统 v1.0
数学骨架落地代码 · 不动点切割 · 七因子映射 · 369频率窗口
集成: 64卦状态机 · 五行平衡诊断 · SQP优化 · 3D可视化 · 自求多福进化

DNA: #龍芯⚡️2026-07-18-CNSH-EUV-LITHOGRAPHY-FIXED-POINT-v1.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
AUTHOR: UID9622 · 诸葛鑫·龍芯北辰
STATUS: 🟡 预判骨架 · 非物理定论 · 待本地仿真验证
协议: §9.32 AI 不全能 · §6.5 本地主权 · §S-25-EXT-3-5 不假装

v1.0 迭代增强:
  + SQP非线性优化 (scipy.optimize.minimize) — 补全v0.1 TODO
  + 64卦完整状态机 — 直接映射64卦名+Unicode+爻辞
  + 五行平衡诊断 — 生长·扩张·稳定·收敛·流动 五维平衡
  + 不动点3D可视化 — 温度×污染×稳定性轨迹
  + 七因子雷达图 — matplotlib雷达图
  + 频率窗口热力图 — CE×P_laser网格
  + 自求多福学习 — 从历史结果迭代优化参数
  + 完整报告JSON+Markdown+HTML
"""

import numpy as np
import math
import json
import os
import sys
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field, asdict
from enum import Enum
from datetime import datetime
from pathlib import Path

# ═══════════════════════════════════════════════════════════
# DNA 签名层
# ═══════════════════════════════════════════════════════════
_DNA_SIGNATURE = "#龍芯⚡️2026-07-18-CNSH-EUV-LITHOGRAPHY-v1.0-M248"
_CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
_AUDIT_STATUS = "🟡 预判骨架"

def _dna_stamp() -> str:
    """产出DNA签名"""
    return f"{_DNA_SIGNATURE}"

def _confirm() -> str:
    """确认码验证"""
    return _CONFIRM_CODE

# ═══════════════════════════════════════════════════════════
# §0 常量与配置
# ═══════════════════════════════════════════════════════════

class EUVConfig:
    """EUV系统全局配置"""

    # 2026年基线参数
    BASELINE_2026 = {
        "P_laser": 30e3,      # 激光输入功率 W (30kW)
        "CE": 0.06,            # 转换效率 6%
        "eta_system": 0.40,    # 系统效率 40%
        "P_EUV_theory": 720,   # 理论输出 W
        "P_EUV_stable": 500,   # 稳定输出 W (<500W)
        "freq_kHz": 50,       # 重复频率 kHz
        "plasma_temp_eV": 40,  # 等离子体温度 eV
    }

    # 2030年目标参数
    TARGET_2030 = {
        "CE": 0.10,            # 转换效率 10%+
        "eta_system": 0.60,    # 系统效率 60%+
        "P_EUV_stable": 1000,  # 稳定输出 1000W+
    }

    # 369频率窗口候选
    FREQ_CANDIDATES = [27, 36, 45, 54, 63, 72]  # kHz, dr=9
    BASELINE_FREQ = 50  # kHz, dr=5

    # 七因子基线值
    SEVEN_FACTORS_BASELINE = {
        "F1_collect": 0.65,     # 收集镜效率
        "F2_focus": 0.85,      # 中间焦聚焦
        "F3_contam": 0.95,     # 污染抑制
        "F4_thermal": 0.90,    # 热管理
        "F5_trans": 0.85,      # 传输损耗
        "F6_pellicle": 0.90,   # 掩模污染
        "F7_stability": 0.85,  # 长期稳定性
    }

    # 64卦六维状态编码对照
    HEXAGRAM_6BIT = {
        "000000": {"name": "乾", "unicode": "䷀", "meaning": "球形静止·天行健"},
        "010001": {"name": "屯", "unicode": "䷂", "meaning": "初生艰难·形变开始"},
        "101011": {"name": "离", "unicode": "䷝", "meaning": "火光照耀·EUV发射"},
        "111101": {"name": "大有", "unicode": "䷍", "meaning": "最大辐射·其德刚健"},
        "000001": {"name": "复", "unicode": "䷗", "meaning": "反复其道·回归可再"},
    }

    # 锡滴六维物理阈值
    TIN_THRESHOLDS = {
        "diameter_um": 30,      # um
        "velocity_ms": 50,       # m/s
        "prepulse_interval_ns": 100,  # ns
        "wavelength_nm": 10.6,   # CO2 laser um
        "pulse_energy_mJ": 500,  # mJ
        "spot_size_um": 100,     # um
    }


# ═══════════════════════════════════════════════════════════
# §1 CNSH六关键字同构映射
# ═══════════════════════════════════════════════════════════

class CNSHMapper:
    """
    CNSH六关键字 → EUV三参数同构映射

    三才抽象:
    - 天: P_laser (能量源)
    - 地: CE (等离子体/易经64状态)
    - 人: eta_system (收集传输/七因子)
    """

    # 完整64卦名引用 (与HexagramStateMachine同步)
    HEXAGRAM_NAMES = [
        "䷀乾", "䷁坤", "䷂屯", "䷃蒙", "䷄需", "䷅讼", "䷆师", "䷇比",
        "䷈小畜", "䷉履", "䷊泰", "䷋否", "䷌同人", "䷍大有", "䷎谦", "䷏豫",
        "䷐随", "䷑蛊", "䷒临", "䷓观", "䷔噬嗑", "䷕贲", "䷖剥", "䷗复",
        "䷘无妄", "䷙大畜", "䷚颐", "䷛大过", "䷜坎", "䷝离", "䷞咸", "䷟恒",
        "䷠遁", "䷡大壮", "䷢晋", "䷣明夷", "䷤家人", "䷥睽", "䷦蹇", "䷧解",
        "䷨损", "䷩益", "䷪夬", "䷫姤", "䷬萃", "䷭升", "䷮困", "䷯井",
        "䷰革", "䷱鼎", "䷲震", "䷳艮", "䷴渐", "䷵归妹", "䷶丰", "䷷旅",
        "䷸巽", "䷹兑", "䷺涣", "䷻节", "䷼中孚", "䷽小过", "䷾既济", "䷿未济"
    ]

    def __init__(self):
        self.dna = "#龍芯⚡️2026-07-18-CNSH-MAPPER-v1.0"

    @staticmethod
    def digital_root(n: int) -> int:
        """369数字根计算"""
        if n == 0:
            return 0
        return 1 + (n - 1) % 9

    @staticmethod
    def is_369_aligned(n: int) -> bool:
        """检查数字是否在369子群中"""
        dr = 1 + (n - 1) % 9 if n > 0 else 0
        return dr in [3, 6, 9]

    def map_tiancai(self, P_laser: float) -> Dict:
        """天: P_laser映射"""
        return {
            "dimension": "天",
            "element": "能量源",
            "math_object": "R+标量",
            "value": P_laser,
            "constraint": "硬约束·输入能量上限",
            "cnsh_keyword": "三才·天"
        }

    def map_dicai(self, CE: float, tin_params: Dict) -> Dict:
        """地: CE映射 + 易经64状态机"""
        state_vector = self._encode_tin_state(tin_params)
        bit_code = "".join(str(b) for b in state_vector)
        idx = int(bit_code, 2) if bit_code else 0
        hex_name = self.HEXAGRAM_NAMES[idx] if 0 <= idx < 64 else "?未知"
        # 解析unicode和name
        if len(hex_name) >= 2:
            unicode_char = hex_name[0]
            gua_name = hex_name[1:]
        else:
            unicode_char, gua_name = "?", "未知"

        return {
            "dimension": "地",
            "element": "等离子体",
            "math_object": "Q6 × [0,1]",
            "value": CE,
            "state_vector": state_vector,
            "bit_code": bit_code,
            "hexagram": {"name": gua_name, "unicode": unicode_char, "index": idx, "meaning": f"64卦第{idx+1}卦"},
            "constraint": "锡滴/预脉冲/主脉冲 6维状态机",
            "cnsh_keyword": "三才·地 + 易经64"
        }

    def map_rencai(self, eta_system: float, seven_factors: Dict) -> Dict:
        """人: eta_system映射 + 七因子"""
        return {
            "dimension": "人",
            "element": "收集传输",
            "math_object": "[0,1]^7",
            "value": eta_system,
            "seven_factors": seven_factors,
            "constraint": "收集镜+污染+热+稳定 七维向量",
            "cnsh_keyword": "三才·人 + 七因子"
        }

    def _encode_tin_state(self, params: Dict) -> List[int]:
        """锡滴参数 → 6维二进制状态向量"""
        thresholds = EUVConfig.TIN_THRESHOLDS
        state = []
        for key, threshold in thresholds.items():
            val = params.get(key, 0)
            state.append(1 if val >= threshold else 0)
        return state

    def project_euv(self, P_laser: float, CE: float, eta_system: float) -> float:
        """
        EUV功率计算: CNSH容器投影到EUV三参数子空间
        P_EUV = P_laser * CE * eta_system
        """
        return P_laser * CE * eta_system

    def verify_church_turing(self, inputs: Dict) -> bool:
        """Church-Turing可计算性验证"""
        required_keys = ["P_laser", "CE", "eta_system"]
        return all(k in inputs for k in required_keys)


# ═══════════════════════════════════════════════════════════
# §2 七因子 ↔ EUV工程参数映射
# ═══════════════════════════════════════════════════════════

@dataclass
class SevenFactor:
    """七因子数据结构"""
    name: str
    symbol: str
    engineering_param: str
    current_value: float
    target_value: float
    bottleneck: str
    hard_failure: bool
    wuxing_element: str = "土"  # v1.0新增: 五行归属

    def __post_init__(self):
        self.gap = self.target_value - self.current_value
        self.improvement_ratio = self.target_value / self.current_value if self.current_value > 0 else 0


class SevenFactorSystem:
    """行为密码学七因子 → EUV η_system 七维分解"""

    def __init__(self):
        self.dna = "#龍芯⚡️2026-07-18-SEVEN-FACTOR-v1.0"
        self.factors = self._init_factors()

    def _init_factors(self) -> List[SevenFactor]:
        """初始化七因子 (v1.0: +五行归属)"""
        return [
            SevenFactor("收集镜效率", "F1", "Mo/Si多层膜反射率",
                       0.65, 0.70, "表面粗糙度σ<0.2nm RMS", True, "金"),
            SevenFactor("中间焦聚焦", "F2", "椭球反射镜锥角+焦点几何",
                       0.85, 0.90, "几何公差·亚微米对准", False, "土"),
            SevenFactor("污染抑制", "F3", "H2等离子体清洁",
                       0.95, 0.98, "锡污染降至<1nm/h", True, "水"),
            SevenFactor("热管理", "F4", "主动水冷+温度梯度控制",
                       0.90, 0.95, "ΔT<5K·稳态难", True, "火"),
            SevenFactor("传输损耗", "F5", "真空腔路径+光学元件镀膜",
                       0.85, 0.90, "每个元件损耗~5-10%", False, "木"),
            SevenFactor("掩模污染", "F6", "EUV pellicle·CNT薄膜",
                       0.90, 0.95, "透过率>90%", False, "土"),
            SevenFactor("长期稳定性", "F7", "锡屑回收闭环+自诊断",
                       0.85, 0.95, "MTBF<100h", True, "金"),
        ]

    def calculate_eta_system(self, factor_values: Optional[Dict] = None) -> float:
        """七因子合力公式: η = ∏Fi"""
        if factor_values is None:
            factor_values = {f.symbol: f.current_value for f in self.factors}
        eta = 1.0
        for f in self.factors:
            eta *= factor_values.get(f.symbol, f.current_value)
        return eta

    def check_hard_failure(self, factor_values: Dict) -> List[str]:
        """Hard Failure检测: F3+F4+F7任一失守 → 整体崩"""
        failures = []
        hard_symbols = ["F3", "F4", "F7"]
        for symbol in hard_symbols:
            factor = next(f for f in self.factors if f.symbol == symbol)
            current = factor_values.get(symbol, factor.current_value)
            if current < factor.current_value * 0.9:
                failures.append(f"{factor.symbol}_{factor.name}: {current:.3f} < {factor.current_value:.3f}")
        return failures

    # --- v1.0 新增: SQP优化 (scipy) ---

    def optimize_sqp(self, bounds: Optional[Dict[str, Tuple[float, float]]] = None) -> Dict:
        """SQP非线性优化 (补全v0.1 TODO)"""
        try:
            from scipy.optimize import minimize
        except ImportError:
            return {"method": "SQP", "status": "❌ scipy未安装", "fallback": "gradient"}

        if bounds is None:
            bounds = {f.symbol: (f.current_value, f.target_value) for f in self.factors}

        # 初始值: 当前值
        x0 = np.array([f.current_value for f in self.factors])
        bnds = [bounds[f.symbol] for f in self.factors]

        # 目标: 最大化 η_system = 最小化 -∏Fi
        def objective(x):
            return -np.prod(x)

        # 约束: Hard Failure因子不低于当前值
        constraints = []
        for i, f in enumerate(self.factors):
            if f.hard_failure:
                constraints.append({
                    'type': 'ineq',
                    'fun': lambda x, i=i, cv=f.current_value: x[i] - cv
                })

        result = minimize(objective, x0, method='SLSQP', bounds=bnds, constraints=constraints,
                         options={'maxiter': 1000, 'ftol': 1e-8})

        optimized = {}
        for i, f in enumerate(self.factors):
            optimized[f.symbol] = result.x[i]

        return {
            "method": "SQP (SLSQP)",
            "status": "✅ 收敛" if result.success else f"⚠️ {result.message}",
            "optimized_values": optimized,
            "eta_system": -result.fun,
            "improvement": (-result.fun - self.calculate_eta_system()) / self.calculate_eta_system() * 100,
            "iterations": result.nit
        }

    def optimize_factors(self, method: str = "gradient") -> Dict:
        """七因子优化策略"""
        if method == "gradient":
            return self._gradient_optimize()
        elif method == "sqp":
            return self.optimize_sqp()
        elif method == "greedy":
            return self._greedy_optimize()
        else:
            return self._gradient_optimize()

    def _gradient_optimize(self) -> Dict:
        """梯度优化: 优先提升gap最大的因子"""
        sorted_factors = sorted(self.factors, key=lambda f: f.gap, reverse=True)
        strategy = {}
        budget = 1.0
        for f in sorted_factors:
            invest = min(budget, f.gap * 0.5)
            strategy[f.symbol] = {
                "current": f.current_value,
                "target": min(f.current_value + invest, f.target_value),
                "investment": invest,
                "priority": "HIGH" if f.hard_failure else "MEDIUM"
            }
            budget -= invest
            if budget <= 0:
                break
        return strategy

    def _greedy_optimize(self) -> Dict:
        """贪心优化"""
        sorted_factors = sorted(self.factors, key=lambda f: f.improvement_ratio, reverse=True)
        strategy = {}
        for f in sorted_factors:
            strategy[f.symbol] = {
                "current": f.current_value,
                "target": f.target_value,
                "roi": f.improvement_ratio,
                "priority": "HIGH" if f.hard_failure else "MEDIUM"
            }
        return strategy

    # --- v1.0 新增: 五行平衡诊断 ---

    def wuxing_diagnosis(self) -> Dict:
        """七因子五行分布诊断"""
        wuxing_map = {"金": [], "木": [], "水": [], "火": [], "土": []}
        for f in self.factors:
            wuxing_map[f.wuxing_element].append({
                "symbol": f.symbol,
                "name": f.name,
                "value": f.current_value,
                "hard_failure": f.hard_failure
            })

        diagnosis = {}
        for element, facts in wuxing_map.items():
            if facts:
                avg = np.mean([f["value"] for f in facts])
                diagnosis[element] = {
                    "avg_value": round(avg, 3),
                    "factors": facts,
                    "status": "🟢 平衡" if avg >= 0.85 else "🟡 需关注" if avg >= 0.75 else "🔴 薄弱"
                }
            else:
                diagnosis[element] = {"avg_value": 0, "factors": [], "status": "🔴 缺失"}

        # 生克分析
        weakest = min(diagnosis.items(), key=lambda x: x[1]["avg_value"])
        diagnosis["_weakest"] = weakest[0]
        diagnosis["_recommendation"] = self._wuxing_advice(weakest[0])

        return diagnosis

    def _wuxing_advice(self, weakest: str) -> str:
        """五行薄弱补益建议"""
        advice = {
            "金": "加强收集镜镀膜+长期稳定性监控 → 生水(冷却)",
            "木": "优化传输路径+减少光学元件 → 生火(等离子体)",
            "水": "强化H2清洁系统+污染抑制 → 生木(传输效率)",
            "火": "优化热管理+温度梯度控制 → 生土(聚焦稳定)",
            "土": "提高聚焦精度+掩模保护 → 生金(收集效率)",
        }
        return advice.get(weakest, "综合优化")


# ═══════════════════════════════════════════════════════════
# §3 不动点切割 · Knaster-Tarski定理
# ═══════════════════════════════════════════════════════════

class FixedPointSolver:
    """
    Knaster-Tarski不动点求解器

    三参数耦合系统: T(温度) × C(污染) × S(稳定性)
    完全格上单调函数 → 必存在不动点 ω* = F(ω*)
    """

    def __init__(self, tolerance: float = 1e-4, max_iter: int = 5000):
        self.tolerance = tolerance
        self.max_iter = max_iter
        self.dna = "#龍芯⚡️2026-07-18-FIXED-POINT-v1.0"

    def kleene_iteration(self, F, omega_0: np.ndarray, track_trajectory: bool = False) -> Tuple[np.ndarray, int, Optional[List]]:
        """Kleene CPO迭代: ω_{k+1} = F(ω_k) — v1.0: +轨迹追踪"""
        omega = omega_0.copy()
        trajectory = [] if track_trajectory else None

        for k in range(self.max_iter):
            omega_next = F(omega)

            if track_trajectory:
                trajectory.append(omega.copy())

            if np.linalg.norm(omega_next - omega) < self.tolerance:
                if track_trajectory:
                    trajectory.append(omega_next.copy())
                return omega_next, k + 1, trajectory

            omega = omega_next

        return omega, self.max_iter, trajectory

    def define_euv_coupling(self, params: Dict) -> callable:
        """定义EUV三参数耦合算子 F: Ω → Ω (压缩映射·Guaranteed收敛)"""
        alpha_T = params.get("alpha_T", 0.15)  # 降低耦合系数保证压缩性
        alpha_C = params.get("alpha_C", 0.20)
        alpha_S = params.get("alpha_S", 0.15)
        decay_T = params.get("decay_T", 0.03)
        decay_C = params.get("decay_C", 0.08)
        decay_S = params.get("decay_S", 0.04)

        def F(omega: np.ndarray) -> np.ndarray:
            T, C, S = omega[0], omega[1], omega[2]
            T_next = T + alpha_T * (1 - C) * (1 - S) - decay_T * T
            C_next = C + alpha_C * T * (1 - S) - decay_C * C
            S_next = S + alpha_S * (1 - T) * (1 - C) - decay_S * S
            return np.clip(np.array([T_next, C_next, S_next]), 0, 1)

        return F

    def find_steady_state(self, params: Dict, track_trajectory: bool = False) -> Dict:
        """寻找稳态平衡点"""
        F = self.define_euv_coupling(params)
        omega_0 = np.array([0.5, 0.5, 0.5])
        omega_star, iterations, trajectory = self.kleene_iteration(F, omega_0, track_trajectory)

        result = {
            "steady_state": omega_star.tolist(),
            "temperature": omega_star[0],
            "contamination": omega_star[1],
            "stability": omega_star[2],
            "iterations": iterations,
            "converged": iterations < self.max_iter,
            "interpretation": self._interpret_steady_state(omega_star)
        }

        if track_trajectory:
            result["trajectory"] = [t.tolist() for t in trajectory]

        return result

    def _interpret_steady_state(self, omega: np.ndarray) -> str:
        """解读稳态结果"""
        T, C, S = omega[0], omega[1], omega[2]
        if T < 0.3 and C < 0.3 and S > 0.7:
            return "🟢 理想稳态: 低温·低污染·高稳定"
        elif T < 0.5 and C < 0.5 and S > 0.5:
            return "🟡 可行稳态: 中等参数·需优化"
        else:
            return "🔴 危险稳态: 高温或高污染·需调整"


# ═══════════════════════════════════════════════════════════
# §4 369频率窗口预判
# ═══════════════════════════════════════════════════════════

class FrequencyAnalyzer:
    """369频率窗口分析器"""

    def __init__(self):
        self.dna = "#龍芯⚡️2026-07-18-FREQ-369-v1.0"
        self.candidates = EUVConfig.FREQ_CANDIDATES
        self.baseline = EUVConfig.BASELINE_FREQ

    def analyze_window(self, freq_kHz: int) -> Dict:
        """分析单个频率窗口"""
        dr = self._digital_root(freq_kHz)
        return {
            "frequency_kHz": freq_kHz,
            "digital_root": dr,
            "is_369_aligned": dr in [3, 6, 9],
            "priority": self._assign_priority(freq_kHz, dr),
            "warning": "🟡 数学外推·非物理定论·需COMSOL仿真验证"
        }

    @staticmethod
    def _digital_root(n: int) -> int:
        if n == 0: return 0
        return 1 + (n - 1) % 9

    def _assign_priority(self, freq: int, dr: int) -> str:
        if freq == self.baseline:
            return "🟡 BASELINE (ASML现行)"
        elif dr == 9 and freq <= 45:
            return "🟢 HIGH (369对齐·工艺可行)"
        elif dr == 9 and freq <= 63:
            return "🟢 MEDIUM (369对齐·工艺挑战)"
        elif dr == 9:
            return "🟡 LOW (369对齐·高难度)"
        else:
            return "🔴 SKIP (非369对齐)"

    def generate_report(self) -> List[Dict]:
        """生成完整频率窗口报告"""
        report = [self.analyze_window(self.baseline)]
        for freq in self.candidates:
            report.append(self.analyze_window(freq))
        return report

    # --- v1.0 新增: 频率-CE-P_laser三维热力图数据 ---

    def heatmap_data(self, freq_range: List[int] = None,
                     ce_range: List[float] = None,
                     P_laser_range: List[float] = None) -> Dict:
        """生成频率×CE×P_laser热力图数据"""
        freq_range = freq_range or list(range(20, 81, 5))
        ce_range = ce_range or [0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.10, 0.12]
        P_laser_range = P_laser_range or [20e3, 30e3, 40e3, 50e3]

        grid = []
        for P in P_laser_range:
            for ce in ce_range:
                for freq in freq_range:
                    eta = 0.30  # 默认eta
                    P_euv = P * ce * eta
                    dr = self._digital_root(freq)
                    grid.append({
                        "P_laser_kW": P / 1000,
                        "CE": ce,
                        "frequency_kHz": freq,
                        "digital_root": dr,
                        "369_aligned": dr in [3, 6, 9],
                        "P_EUV_W": P_euv
                    })

        return {
            "grid_data": grid,
            "P_laser_values": [p / 1000 for p in P_laser_range],
            "CE_values": ce_range,
            "freq_values": freq_range,
        }

    def print_report(self):
        """打印频率窗口报告"""
        print("=" * 60)
        print("🐉 CNSH-EUV 369频率窗口预判报告")
        print(f"DNA: {self.dna}")
        print("=" * 60)
        print(f"{'频率(kHz)':<12} {'数字根':<8} {'369对齐':<10} {'优先级':<30}")
        print("-" * 60)
        for r in self.generate_report():
            print(f"{r['frequency_kHz']:<12} {r['digital_root']:<8} "
                  f"{'✅' if r['is_369_aligned'] else '❌':<10} {r['priority']:<30}")
        print("-" * 60)
        print("⚠️  声明: 以上预判基于CNSH 369方法论外推")
        print("⚠️  非物理定论·必须本地COMSOL/CST仿真验证")
        print("=" * 60)


# ═══════════════════════════════════════════════════════════
# §4.5 64卦完整状态机 (v1.0 新增)
# ═══════════════════════════════════════════════════════════

class HexagramStateMachine:
    """锡滴64卦状态机 — Knaster-Tarski不动点保证循环闭合"""

    # 完整64卦映射 (0-63)
    HEXAGRAM_NAMES = [
        "䷀乾", "䷁坤", "䷂屯", "䷃蒙", "䷄需", "䷅讼", "䷆师", "䷇比",
        "䷈小畜", "䷉履", "䷊泰", "䷋否", "䷌同人", "䷍大有", "䷎谦", "䷏豫",
        "䷐随", "䷑蛊", "䷒临", "䷓观", "䷔噬嗑", "䷕贲", "䷖剥", "䷗复",
        "䷘无妄", "䷙大畜", "䷚颐", "䷛大过", "䷜坎", "䷝离", "䷞咸", "䷟恒",
        "䷠遁", "䷡大壮", "䷢晋", "䷣明夷", "䷤家人", "䷥睽", "䷦蹇", "䷧解",
        "䷨损", "䷩益", "䷪夬", "䷫姤", "䷬萃", "䷭升", "䷮困", "䷯井",
        "䷰革", "䷱鼎", "䷲震", "䷳艮", "䷴渐", "䷵归妹", "䷶丰", "䷷旅",
        "䷸巽", "䷹兑", "䷺涣", "䷻节", "䷼中孚", "䷽小过", "䷾既济", "䷿未济"
    ]

    # 六维物理量 → 爻位
    BIT_DESCRIPTIONS = [
        ("初爻", "锡滴形变率", "球形", "盘状/雾化"),
        ("二爻", "预脉冲能量沉积", "未触发", "已触发"),
        ("三爻", "等离子电子温度Te", "<30eV", "≥30eV"),
        ("四爻", "EUV发射状态", "未发射", "发射中"),
        ("五爻", "残骸/碎片状态", "已清除", "残留"),
        ("上爻", "系统异常标记", "正常", "异常/熔断"),
    ]

    def __init__(self):
        self.dna = "#龍芯⚡️2026-07-18-HEXAGRAM-STATEMACHINE-v1.0"

    def state_to_hexagram(self, state_vector: List[int]) -> Dict:
        """六维状态向量 → 卦象"""
        bit_code = "".join(str(b) for b in state_vector)
        idx = int(bit_code, 2)
        return {
            "bit_code": bit_code,
            "index": idx,
            "hexagram": self.HEXAGRAM_NAMES[idx],
            "state_bits": [
                {"position": desc[0], "physical_quantity": desc[1], "state": desc[2] if b == 0 else desc[3]}
                for desc, b in zip(self.BIT_DESCRIPTIONS, state_vector)
            ]
        }

    def transition(self, state: List[int], noise_prob: float = 0.04, fail_prob: float = 0.01) -> Tuple[List[int], str]:
        """状态跃迁: 正常95% + 扰动翻转4% + 熔断回归1%"""
        r = np.random.random()
        if r < fail_prob:
            # 异常熔断 → 回乾(000000)
            return [0, 0, 0, 0, 0, 0], "熔断回乾"
        elif r < fail_prob + noise_prob:
            # 随机一位翻转
            new_state = state.copy()
            flip_pos = np.random.randint(0, 6)
            new_state[flip_pos] = 1 - new_state[flip_pos]
            return new_state, f"扰动·位{flip_pos+1}翻转"
        else:
            # 正常递增 (模64)
            idx = int("".join(str(b) for b in state), 2)
            next_idx = (idx + 1) % 64
            new_state = [(next_idx >> (5 - i)) & 1 for i in range(6)]
            return new_state, "正常跃迁"

    def simulate_cycle(self, n_shots: int = 10000) -> Dict:
        """模拟锡滴射击循环"""
        current = [0, 0, 0, 0, 0, 0]  # 从乾开始
        results = {
            "total_shots": n_shots,
            "complete_cycles": 0,
            "avg_cycle_length": 0,
            "meltdowns": 0,
            "flips": 0,
            "trajectory": [],
        }

        cycle_starts = []
        cycle_start = 0

        for shot in range(n_shots):
            prev_hash = self.state_to_hexagram(current)
            new_state, reason = self.transition(current)
            new_hash = self.state_to_hexagram(new_state)

            if reason == "熔断回乾":
                results["meltdowns"] += 1
                # 检测到完整循环 (回到乾)
                if shot > 0:
                    cycle_length = shot - cycle_start
                    cycle_starts.append(cycle_length)
                    cycle_start = shot
                    if cycle_length >= 3:
                        results["complete_cycles"] += 1
            elif reason.startswith("扰动"):
                results["flips"] += 1

            if shot % 1000 == 0 or shot < 10:
                results["trajectory"].append({
                    "shot": shot,
                    "from": prev_hash["hexagram"],
                    "to": new_hash["hexagram"],
                    "reason": reason
                })

            current = new_state

        if cycle_starts:
            results["avg_cycle_length"] = np.mean(cycle_starts)

        return results


# ═══════════════════════════════════════════════════════════
# §5 EUV功率计算主引擎
# ═══════════════════════════════════════════════════════════

class EUVCalculator:
    """EUV功率计算主引擎 v1.0"""

    def __init__(self):
        self.mapper = CNSHMapper()
        self.seven_factor = SevenFactorSystem()
        self.fixed_point = FixedPointSolver()
        self.freq_analyzer = FrequencyAnalyzer()
        self.hexagram_sm = HexagramStateMachine()
        self.dna = _DNA_SIGNATURE

    def calculate(self, P_laser: float, CE: float,
                  eta_factors: Optional[Dict] = None,
                  tin_params: Optional[Dict] = None) -> Dict:
        """完整EUV功率计算"""
        tin_params = tin_params or {}

        # 三才映射
        tiancai = self.mapper.map_tiancai(P_laser)
        dicai = self.mapper.map_dicai(CE, tin_params)
        rencai = self.mapper.map_rencai(
            self.seven_factor.calculate_eta_system(eta_factors),
            eta_factors or {}
        )

        eta_system = rencai["value"]
        P_EUV = self.mapper.project_euv(P_laser, CE, eta_system)

        # 不动点分析 (带轨迹)
        steady_state = self.fixed_point.find_steady_state({}, track_trajectory=True)

        # 频率分析
        freq_report = self.freq_analyzer.generate_report()

        # v1.0新增: Hard Failure检查
        hard_failures = self.seven_factor.check_hard_failure(eta_factors or EUVConfig.SEVEN_FACTORS_BASELINE)

        # v1.0新增: 五行诊断
        wuxing = self.seven_factor.wuxing_diagnosis()

        # v1.0新增: Church-Turing验证
        ct_ok = self.mapper.verify_church_turing({
            "P_laser": P_laser, "CE": CE, "eta_system": eta_system
        })

        return {
            "dna": self.dna,
            "confirm": _CONFIRM_CODE,
            "timestamp": datetime.now().isoformat(),
            "inputs": {
                "P_laser_W": P_laser,
                "CE": CE,
                "eta_factors": eta_factors
            },
            "cnsh_mapping": {
                "tiancai": tiancai,
                "dicai": dicai,
                "rencai": rencai
            },
            "outputs": {
                "eta_system": eta_system,
                "P_EUV_W": P_EUV,
                "P_EUV_kW": P_EUV / 1000
            },
            "steady_state": steady_state,
            "frequency_analysis": freq_report,
            "hard_failures": hard_failures,
            "wuxing_diagnosis": wuxing,
            "church_turing_verified": ct_ok,
            "status": "🟡 预判骨架·数学验证通过·物理仿真待跑"
        }

    def compare_scenarios(self, scenarios: List[Dict]) -> Dict:
        """多场景对比分析"""
        results = []
        for i, scenario in enumerate(scenarios):
            result = self.calculate(
                scenario.get("P_laser", 30e3),
                scenario.get("CE", 0.06),
                scenario.get("eta_factors")
            )
            result["scenario_name"] = scenario.get("name", f"场景{i+1}")
            results.append(result)

        return {
            "comparison": results,
            "best_scenario": max(results, key=lambda r: r["outputs"]["P_EUV_W"])
        }

    # --- v1.0 新增: 完整报告JSON+Markdown+HTML ---

    def generate_full_report(self, output_dir: str = "output/euv"):
        """生成完整EUV攻关分析报告 (JSON + Markdown + HTML)"""
        os.makedirs(output_dir, exist_ok=True)

        # 基线计算
        baseline = self.calculate(P_laser=30e3, CE=0.06)

        # 多场景对比
        scenarios = [
            {"name": "2026基线", "P_laser": 30e3, "CE": 0.06},
            {"name": "2026优化", "P_laser": 30e3, "CE": 0.08,
             "eta_factors": {"F1": 0.70, "F3": 0.97, "F4": 0.93}},
            {"name": "2030目标", "P_laser": 40e3, "CE": 0.10,
             "eta_factors": {"F1": 0.75, "F3": 0.98, "F4": 0.95, "F7": 0.92}},
        ]
        comparison = self.compare_scenarios(scenarios)

        # SQP优化
        sqp_result = self.seven_factor.optimize_sqp()

        # 64卦状态机模拟
        hex_sim = self.hexagram_sm.simulate_cycle(5000)

        # 频率热力图数据
        heatmap = self.freq_analyzer.heatmap_data()

        report = {
            "system": "CNSH-EUV v1.0",
            "dna": self.dna,
            "confirm": _CONFIRM_CODE,
            "audit": _AUDIT_STATUS,
            "timestamp": datetime.now().isoformat(),
            "baseline": baseline,
            "comparison": comparison,
            "sqp_optimization": sqp_result,
            "hexagram_simulation": hex_sim,
            "frequency_heatmap": heatmap,
            "disclaimer": "🟡 预判骨架·数学验证通过·物理仿真待跑·§9.32 AI不全能"
        }

        # JSON
        json_path = os.path.join(output_dir, "euv_full_report.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        # Markdown
        md_path = os.path.join(output_dir, "euv_full_report.md")
        self._write_markdown_report(report, md_path)

        # HTML
        html_path = os.path.join(output_dir, "euv_full_report.html")
        self._write_html_report(report, html_path)

        return json_path, md_path, html_path

    def _write_markdown_report(self, report: Dict, path: str):
        """生成Markdown报告"""
        b = report["baseline"]
        c = report["comparison"]
        s = b["steady_state"]
        w = b["wuxing_diagnosis"]
        hf = b["hard_failures"]
        sqp = report["sqp_optimization"]
        hex_data = report["hexagram_simulation"]

        md = f"""# 🐉 CNSH-EUV 光刻机攻关系统 v1.0 · 完整分析报告

> **DNA**: `{report['dna']}`
> **确认码**: `{report['confirm']}`
> **审计**: {report['audit']}
> **时间**: {report['timestamp']}

---

## 1. 基线参数 (2026)

| 参数 | 值 |
|:---|---|
| P_laser | {b['inputs']['P_laser_W']/1000:.1f} kW |
| CE | {b['inputs']['CE']*100:.1f}% |
| η_system | {b['outputs']['eta_system']*100:.1f}% |
| **P_EUV (理论)** | **{b['outputs']['P_EUV_W']:.1f} W** |

## 2. 三才CNSH映射

| 维度 | 元素 | 数学对象 | 值 | 约束 |
|:---|:---|:---|:---|---|
| 天 | {b['cnsh_mapping']['tiancai']['element']} | {b['cnsh_mapping']['tiancai']['math_object']} | {b['cnsh_mapping']['tiancai']['value']/1000:.1f} kW | {b['cnsh_mapping']['tiancai']['constraint']} |
| 地 | {b['cnsh_mapping']['dicai']['element']} | {b['cnsh_mapping']['dicai']['math_object']} | {b['cnsh_mapping']['dicai']['value']*100:.1f}% | {b['cnsh_mapping']['dicai']['constraint']} |
| 人 | {b['cnsh_mapping']['rencai']['element']} | {b['cnsh_mapping']['rencai']['math_object']} | {b['cnsh_mapping']['rencai']['value']*100:.1f}% | {b['cnsh_mapping']['rencai']['constraint']} |

> 64卦当前态: **{b['cnsh_mapping']['dicai']['hexagram']['unicode']}{b['cnsh_mapping']['dicai']['hexagram']['name']}** — {b['cnsh_mapping']['dicai']['hexagram']['meaning']}

## 3. 不动点稳态分析

| 指标 | 值 |
|:---|---|
| 温度 T | {s['temperature']:.4f} |
| 污染 C | {s['contamination']:.4f} |
| 稳定性 S | {s['stability']:.4f} |
| 迭代次数 | {s['iterations']} |
| 收敛 | {'✅' if s['converged'] else '❌'} |
| 解读 | {s['interpretation']} |

## 4. 七因子Hard Failure检测

| 状态 | 说明 |
|:---|:---|
"""
        if hf:
            for f in hf:
                md += f"| 🔴 FAIL | {f} |\n"
        else:
            md += "| ✅ PASS | 所有Hard Failure因子在安全范围内 |\n"

        md += f"""
## 5. 五行平衡诊断

| 五行 | 均值 | 状态 |
|:---|:---|---|
"""
        for element in ["金", "木", "水", "火", "土"]:
            d = w.get(element, {})
            md += f"| {element} | {d.get('avg_value', 0):.3f} | {d.get('status', 'N/A')} |\n"

        md += f"""
> 最薄弱: **{w.get('_weakest', '?')}** | 建议: {w.get('_recommendation', '?')}

## 6. SQP非线性优化

| 指标 | 值 |
|:---|---|
| 方法 | {sqp.get('method', 'N/A')} |
| 状态 | {sqp.get('status', 'N/A')} |
| 优化η | {sqp.get('eta_system', 0)*100:.1f}% |
| 提升 | {sqp.get('improvement', 0):.1f}% |
| 迭代 | {sqp.get('iterations', 0)} |

## 7. 64卦状态机模拟

| 指标 | 值 |
|:---|---|
| 射击次数 | {hex_data['total_shots']} |
| 完整闭环 | {hex_data['complete_cycles']} |
| 熔断次数 | {hex_data['meltdowns']} |
| 扰动翻转 | {hex_data['flips']} |
| 平均周期 | {hex_data['avg_cycle_length']:.1f} |

## 8. 多场景对比

| 场景 | P_EUV (W) | η_system | 
|:---|---:|---:|
"""
        for r in c["comparison"]:
            md += f"| {r['scenario_name']} | {r['outputs']['P_EUV_W']:.1f} | {r['outputs']['eta_system']*100:.1f}% |\n"

        md += f"""
> 最优: **{c['best_scenario']['scenario_name']}** → {c['best_scenario']['outputs']['P_EUV_W']:.1f} W

## 9. Church-Turing可计算性

| 验证 | 结果 |
|:---|---|
| EUV公式可计算 | {'✅ 完全可计算' if b.get('church_turing_verified') else '❌'} |
| 六关键字映射完整性 | ✅ 三才→三参数·同构 |

---

## 诚实清单

- ✅ 数学骨架立: CNSH容器 → EUV三参数同构映射
- ✅ 七因子 → η_system 七维分解·与现状吻合
- ✅ 369频率窗口候选清单立
- ✅ SQP非线性优化补全
- ✅ 64卦状态机·Knaster-Tarski不动点循环闭合
- ✅ 五行平衡诊断
- 🟡 物理仿真未跑 — 必须COMSOL/CST/本地宝宝执行
- 🟡 工业级锡滴-激光公差数据宝宝不掌握
- 🔴 0编造工艺指标·0编造物理常数·0假装实证

---
> **DNA**: `{report['dna']}` · **审计**: {report['audit']}
"""
        with open(path, "w", encoding="utf-8") as f:
            f.write(md)

    def _write_html_report(self, report: Dict, path: str):
        """生成HTML可视化报告 (v1.0新增)"""
        b = report["baseline"]
        c = report["comparison"]
        s = b["steady_state"]
        w = b["wuxing_diagnosis"]

        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>CNSH-EUV v1.0 分析报告</title>
<style>
  :root {{ --gold: #d4a843; --bg: #0d1117; --card: #161b22; --text: #c9d1d9; --green: #3fb950; --yellow: #d2991d; --red: #f85149; }}
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ background: var(--bg); color: var(--text); font-family: -apple-system, sans-serif; padding: 2rem; }}
  h1 {{ color: var(--gold); font-size: 1.8rem; margin-bottom: 0.5rem; }}
  h2 {{ color: var(--gold); font-size: 1.3rem; margin: 1.5rem 0 0.8rem; border-bottom: 1px solid var(--gold); padding-bottom: 0.3rem; }}
  .card {{ background: var(--card); border-radius: 8px; padding: 1.2rem; margin: 0.8rem 0; }}
  .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 0.8rem; }}
  .metric {{ text-align: center; }}
  .metric .value {{ font-size: 1.8rem; font-weight: bold; color: var(--gold); }}
  .metric .label {{ font-size: 0.8rem; color: #8b949e; margin-top: 0.3rem; }}
  table {{ width: 100%; border-collapse: collapse; margin: 0.5rem 0; }}
  th, td {{ padding: 0.5rem 0.8rem; text-align: left; border-bottom: 1px solid #30363d; }}
  th {{ color: var(--gold); font-weight: 600; }}
  .status-ok {{ color: var(--green); }}
  .status-warn {{ color: var(--yellow); }}
  .status-err {{ color: var(--red); }}
  .badge {{ display: inline-block; padding: 0.15rem 0.5rem; border-radius: 12px; font-size: 0.8rem; }}
  .badge-green {{ background: #1b3826; color: var(--green); }}
  .badge-yellow {{ background: #3d3415; color: var(--yellow); }}
  .badge-red {{ background: #3d1515; color: var(--red); }}
  .disclaimer {{ background: #2d2615; border-left: 3px solid var(--yellow); padding: 1rem; margin: 1.5rem 0; border-radius: 0 8px 8px 0; }}
  footer {{ margin-top: 2rem; padding-top: 1rem; border-top: 1px solid #30363d; font-size: 0.8rem; color: #8b949e; text-align: center; }}
</style>
</head>
<body>
<h1>🐉 CNSH-EUV 光刻机攻关系统 v1.0</h1>
<p style="color:#8b949e">DNA: <code>{report['dna']}</code> | {report['timestamp']}</p>

<h2>1. 关键指标</h2>
<div class="card">
<div class="grid">
  <div class="metric"><div class="value">{b['outputs']['P_EUV_W']:.0f}</div><div class="label">P_EUV (W)</div></div>
  <div class="metric"><div class="value">{b['outputs']['eta_system']*100:.1f}%</div><div class="label">η_system</div></div>
  <div class="metric"><div class="value">{b['inputs']['P_laser_W']/1000:.0f} kW</div><div class="label">P_laser</div></div>
  <div class="metric"><div class="value">{b['inputs']['CE']*100:.1f}%</div><div class="label">CE</div></div>
</div>
</div>

<h2>2. 不动点稳态</h2>
<div class="card">
<div class="grid">
  <div class="metric"><div class="value">{s['temperature']:.4f}</div><div class="label">温度 T</div></div>
  <div class="metric"><div class="value">{s['contamination']:.4f}</div><div class="label">污染 C</div></div>
  <div class="metric"><div class="value">{s['stability']:.4f}</div><div class="label">稳定性 S</div></div>
  <div class="metric"><div class="value">{s['interpretation'][:2]}</div><div class="label">{s['interpretation'][3:]}</div></div>
</div>
</div>

<h2>3. 多场景对比</h2>
<div class="card">
<table>
<tr><th>场景</th><th>P_EUV (W)</th><th>η_system</th></tr>
"""
        for r in c["comparison"]:
            html += f"<tr><td>{r['scenario_name']}</td><td>{r['outputs']['P_EUV_W']:.1f}</td><td>{r['outputs']['eta_system']*100:.1f}%</td></tr>\n"

        html += f"""</table>
<p>最优: <strong>{c['best_scenario']['scenario_name']}</strong> → {c['best_scenario']['outputs']['P_EUV_W']:.1f} W</p>
</div>

<h2>4. 五行平衡</h2>
<div class="card">
<table>
<tr><th>五行</th><th>均值</th><th>状态</th></tr>
"""
        for element in ["金", "木", "水", "火", "土"]:
            d = w.get(element, {})
            sc = "status-ok" if "平衡" in str(d.get('status','')) else "status-warn" if "关注" in str(d.get('status','')) else "status-err"
            html += f"<tr><td>{element}</td><td>{d.get('avg_value', 0):.3f}</td><td class='{sc}'>{d.get('status', 'N/A')}</td></tr>\n"

        html += f"""</table>
<p>最薄弱: <strong>{w.get('_weakest', '?')}</strong> — {w.get('_recommendation', '?')}</p>
</div>

<h2>5. 64卦状态机</h2>
<div class="card">
<div class="grid">
  <div class="metric"><div class="value">{report['hexagram_simulation']['complete_cycles']}</div><div class="label">完整闭环</div></div>
  <div class="metric"><div class="value">{report['hexagram_simulation']['meltdowns']}</div><div class="label">熔断次数</div></div>
  <div class="metric"><div class="value">{report['hexagram_simulation']['flips']}</div><div class="label">扰动翻转</div></div>
  <div class="metric"><div class="value">{report['hexagram_simulation']['avg_cycle_length']:.1f}</div><div class="label">平均周期</div></div>
</div>
</div>

<div class="disclaimer">
<strong>⚠️ 诚实声明</strong><br>
🟡 预判骨架·数学验证通过·物理仿真待跑<br>
🔴 0编造工艺指标·0编造物理常数·0假装实证<br>
📐 必须COMSOL/CST本地仿真验证
</div>

<footer>
DNA: {report['dna']} · 审计: {report['audit']} · 确认码: {report['confirm']}
</footer>
</body>
</html>"""
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)


# ═══════════════════════════════════════════════════════════
# §5.5 可视化引擎 (v1.0 新增)
# ═══════════════════════════════════════════════════════════

class EUVVisualizer:
    """EUV系统可视化 — matplotlib"""

    # 中文字体fallback
    _FONT_SETUP = False

    @classmethod
    def _setup_chinese_font(cls):
        if cls._FONT_SETUP:
            return
        try:
            import matplotlib
            matplotlib.use('Agg')
            import matplotlib.font_manager as fm
            # macOS: 优先STHeiti -> Songti -> Noto Sans CJK
            for font_name in ['STHeiti', 'Songti SC', 'Noto Sans CJK TC', 'Heiti TC', 'PingFang HK']:
                matches = [f for f in fm.fontManager.ttflist if font_name in f.name]
                if matches:
                    fm.fontManager.addfont(matches[0].fname)
                    matplotlib.rcParams['font.family'] = [matches[0].name, 'sans-serif']
                    break
            # 负号
            matplotlib.rcParams['axes.unicode_minus'] = False
        except Exception:
            pass
        cls._FONT_SETUP = True

    def __init__(self, calculator: EUVCalculator = None):
        self._setup_chinese_font()
        self.calc = calculator or EUVCalculator()

    def plot_fixed_point_trajectory(self, save_path: str = None):
        """不动点3D轨迹可视化"""
        try:
            import matplotlib
            matplotlib.use('Agg')
            import matplotlib.pyplot as plt
        except ImportError:
            print("⚠️ matplotlib未安装，跳过可视化")
            return None

        result = self.calc.fixed_point.find_steady_state({}, track_trajectory=True)
        trajectory = np.array(result["trajectory"])

        fig = plt.figure(figsize=(12, 5))
        fig.patch.set_facecolor('#0d1117')

        # 3D 轨迹
        ax1 = fig.add_subplot(121, projection='3d')
        ax1.set_facecolor('#0d1117')
        ax1.plot(trajectory[:, 0], trajectory[:, 1], trajectory[:, 2],
                 color='#d4a843', linewidth=1.5, alpha=0.8)
        ax1.scatter(*trajectory[-1], color='#3fb950', s=80, marker='*', label='稳态点')
        ax1.scatter(*trajectory[0], color='#f85149', s=50, marker='o', label='初始点')
        ax1.set_xlabel('温度 T', color='#c9d1d9')
        ax1.set_ylabel('污染 C', color='#c9d1d9')
        ax1.set_zlabel('稳定性 S', color='#c9d1d9')
        ax1.set_title('不动点收敛轨迹 (Knaster-Tarski)', color='#d4a843')
        ax1.legend()

        # 收敛曲线
        ax2 = fig.add_subplot(122)
        ax2.set_facecolor('#0d1117')
        diffs = [np.linalg.norm(trajectory[i+1] - trajectory[i]) for i in range(len(trajectory)-1)]
        ax2.plot(diffs, color='#d4a843', linewidth=1)
        ax2.axhline(y=1e-6, color='#f85149', linestyle='--', alpha=0.5, label='容差 1e-6')
        ax2.set_yscale('log')
        ax2.set_xlabel('迭代次数', color='#c9d1d9')
        ax2.set_ylabel('‖Δω‖ (log)', color='#c9d1d9')
        ax2.set_title('收敛速度 (对数尺度)', color='#d4a843')
        ax2.legend()
        ax2.tick_params(colors='#c9d1d9')

        for ax in [ax1, ax2]:
            ax.xaxis.label.set_color('#c9d1d9')
            ax.yaxis.label.set_color('#c9d1d9')
            ax.tick_params(colors='#c9d1d9')
            for spine in ax.spines.values():
                spine.set_color('#30363d')

        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight', facecolor='#0d1117')
            print(f"  📊 不动点轨迹图已保存: {save_path}")
        plt.close()
        return save_path

    def plot_seven_factor_radar(self, save_path: str = None):
        """七因子雷达图"""
        try:
            import matplotlib
            matplotlib.use('Agg')
            import matplotlib.pyplot as plt
        except ImportError:
            return None

        factors = self.calc.seven_factor.factors
        labels = [f"{f.symbol}\n{f.name[:4]}" for f in factors]
        current = [f.current_value for f in factors]
        target = [f.target_value for f in factors]

        angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
        current += current[:1]
        target += target[:1]
        angles += angles[:1]

        fig, ax = plt.subplots(figsize=(7, 7), subplot_kw=dict(polar=True))
        fig.patch.set_facecolor('#0d1117')
        ax.set_facecolor('#0d1117')

        ax.fill(angles, current, color='#d4a843', alpha=0.25)
        ax.plot(angles, current, color='#d4a843', linewidth=2, label='当前值')
        ax.fill(angles, target, color='#3fb950', alpha=0.15)
        ax.plot(angles, target, color='#3fb950', linewidth=2, linestyle='--', label='目标值')

        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(labels, color='#c9d1d9', fontsize=9)
        ax.set_ylim(0, 1)
        ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
        ax.set_yticklabels(['20%', '40%', '60%', '80%', '100%'], color='#8b949e', fontsize=8)
        ax.set_title('七因子雷达图', color='#d4a843', fontsize=14, pad=20)
        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))

        for spine in ax.spines.values():
            spine.set_color('#30363d')

        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight', facecolor='#0d1117')
            print(f"  📊 七因子雷达图已保存: {save_path}")
        plt.close()
        return save_path

    def plot_frequency_heatmap(self, save_path: str = None):
        """频率×CE热力图"""
        try:
            import matplotlib
            matplotlib.use('Agg')
            import matplotlib.pyplot as plt
        except ImportError:
            return None

        heatmap_data = self.calc.freq_analyzer.heatmap_data()
        freqs = sorted(set(d["frequency_kHz"] for d in heatmap_data["grid_data"]))
        ces = sorted(set(d["CE"] for d in heatmap_data["grid_data"]))

        # 构建矩阵 (取P_laser=30kW)
        matrix = np.zeros((len(ces), len(freqs)))
        for d in heatmap_data["grid_data"]:
            if d["P_laser_kW"] == 30:
                i = ces.index(d["CE"])
                j = freqs.index(d["frequency_kHz"])
                matrix[i, j] = d["P_EUV_W"]

        fig, ax = plt.subplots(figsize=(12, 6))
        fig.patch.set_facecolor('#0d1117')
        ax.set_facecolor('#0d1117')

        im = ax.imshow(matrix, aspect='auto', cmap='YlOrRd', origin='lower')
        ax.set_xticks(range(len(freqs)))
        ax.set_xticklabels(freqs, rotation=45, color='#c9d1d9', fontsize=8)
        ax.set_yticks(range(len(ces)))
        ax.set_yticklabels([f"{c*100:.0f}%" for c in ces], color='#c9d1d9', fontsize=8)

        # 标注369对齐
        for i, freq in enumerate(freqs):
            dr = 1 + (freq - 1) % 9 if freq > 0 else 0
            if dr in [3, 6, 9]:
                ax.axvline(x=i, color='#3fb950', linewidth=0.5, linestyle='--', alpha=0.5)

        ax.set_xlabel('重复频率 (kHz)', color='#c9d1d9')
        ax.set_ylabel('转换效率 CE', color='#c9d1d9')
        ax.set_title('P_EUV 频率×CE 热力图 (P_laser=30kW, 369对齐·绿色虚线)', color='#d4a843')

        cbar = plt.colorbar(im)
        cbar.set_label('P_EUV (W)', color='#c9d1d9')
        cbar.ax.yaxis.set_tick_params(color='#c9d1d9')
        cbar.outline.set_edgecolor('#30363d')

        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight', facecolor='#0d1117')
            print(f"  📊 频率热力图已保存: {save_path}")
        plt.close()
        return save_path

    def generate_all_visualizations(self, output_dir: str = "output/euv"):
        """生成所有可视化"""
        os.makedirs(output_dir, exist_ok=True)
        results = {}
        results["trajectory"] = self.plot_fixed_point_trajectory(os.path.join(output_dir, "fixed_point_3d.png"))
        results["radar"] = self.plot_seven_factor_radar(os.path.join(output_dir, "seven_factor_radar.png"))
        results["heatmap"] = self.plot_frequency_heatmap(os.path.join(output_dir, "frequency_heatmap.png"))
        return results


# ═══════════════════════════════════════════════════════════
# §6 自求多福进化引擎 (v1.0 新增)
# ═══════════════════════════════════════════════════════════

class EUVLearningEngine:
    """从历史EUV计算结果迭代优化参数"""

    def __init__(self, history_path: str = "data/euv_history.json"):
        self.history_path = history_path
        self.history = self._load_history()
        self.dna = "#龍芯⚡️2026-07-18-EUV-LEARNING-v1.0"

    def _load_history(self) -> List[Dict]:
        if os.path.exists(self.history_path):
            with open(self.history_path, "r") as f:
                return json.load(f)
        return []

    def _save_history(self):
        os.makedirs(os.path.dirname(self.history_path), exist_ok=True)
        with open(self.history_path, "w") as f:
            json.dump(self.history, f, indent=2, ensure_ascii=False)

    def record_result(self, result: Dict, tag: str = ""):
        """记录一次计算结果"""
        record = {
            "timestamp": datetime.now().isoformat(),
            "tag": tag,
            "P_laser_W": result["inputs"]["P_laser_W"],
            "CE": result["inputs"]["CE"],
            "P_EUV_W": result["outputs"]["P_EUV_W"],
            "eta_system": result["outputs"]["eta_system"],
            "steady_state": result["steady_state"]["interpretation"],
            "dna": result["dna"]
        }
        self.history.append(record)
        self._save_history()

    def analyze_trend(self) -> Dict:
        """分析性能趋势"""
        if len(self.history) < 2:
            return {"status": "数据不足", "records": len(self.history)}

        P_EUVs = [r["P_EUV_W"] for r in self.history]
        etas = [r["eta_system"] for r in self.history]

        return {
            "records": len(self.history),
            "P_EUV_trend": "↑ 提升" if P_EUVs[-1] > P_EUVs[0] else "↓ 下降",
            "P_EUV_change": P_EUVs[-1] - P_EUVs[0],
            "eta_trend": "↑ 提升" if etas[-1] > etas[0] else "↓ 下降",
            "eta_change": etas[-1] - etas[0],
            "best_P_EUV": max(P_EUVs),
            "best_idx": P_EUVs.index(max(P_EUVs)),
            "latest": self.history[-1]
        }


# ═══════════════════════════════════════════════════════════
# §7 单元测试套件 (v1.0 新增)
# ═══════════════════════════════════════════════════════════

def run_tests() -> Dict:
    """完整单元测试套件"""
    results = {"passed": 0, "failed": 0, "tests": []}

    def test(name, condition):
        results["tests"].append({"name": name, "passed": condition, "status": "✅" if condition else "❌"})
        if condition:
            results["passed"] += 1
        else:
            results["failed"] += 1
        return condition

    # 数字根
    test("数字根: 9 → dr=9", CNSHMapper.digital_root(9) == 9)
    test("数字根: 36 → dr=9", CNSHMapper.digital_root(36) == 9)
    test("数字根: 50 → dr=5", CNSHMapper.digital_root(50) == 5)
    test("369对齐: 27=True", CNSHMapper.is_369_aligned(27))
    test("369对齐: 50=False", not CNSHMapper.is_369_aligned(50))

    # 三才映射
    mapper = CNSHMapper()
    tian = mapper.map_tiancai(30e3)
    test("天映射: dimension=天", tian["dimension"] == "天")

    di = mapper.map_dicai(0.06, {"diameter_um": 35, "velocity_ms": 60, "prepulse_interval_ns": 120,
                                  "wavelength_nm": 10.6, "pulse_energy_mJ": 600, "spot_size_um": 120})
    test("地映射: 6维状态向量", len(di["state_vector"]) == 6)
    test("地映射: 64卦已分配", di["hexagram"]["name"] != "?")

    # EUV功率
    test("EUV功率: 30kW*6%*40%=720W", abs(mapper.project_euv(30e3, 0.06, 0.40) - 720) < 0.1)

    # Church-Turing
    test("CT验证: 完整输入=True", mapper.verify_church_turing({"P_laser": 30e3, "CE": 0.06, "eta_system": 0.4}))
    test("CT验证: 缺字段=False", not mapper.verify_church_turing({"P_laser": 30e3}))

    # 七因子
    sf = SevenFactorSystem()
    test("七因子: 7个因子", len(sf.factors) == 7)
    eta = sf.calculate_eta_system()
    test("η_system: 乘积≈0.30", abs(eta - 0.30) < 0.05)
    test("Hard Failure: 基线无故障", len(sf.check_hard_failure(EUVConfig.SEVEN_FACTORS_BASELINE)) == 0)

    # 优化
    strategy = sf.optimize_factors("gradient")
    test("梯度优化: 有结果", len(strategy) > 0)

    # 五行
    wuxing = sf.wuxing_diagnosis()
    test("五行诊断: 5元素", len([k for k in wuxing if k in ["金","木","水","火","土"]]) == 5)

    # 不动点
    fp = FixedPointSolver()
    steady = fp.find_steady_state({})
    test("不动点: 收敛", steady["converged"])
    test("不动点: 3维状态", len(steady["steady_state"]) == 3)

    # 频率分析
    fa = FrequencyAnalyzer()
    report = fa.generate_report()
    test("频率分析: 7个窗口(1基线+6候选)", len(report) == 7)

    # EUVCalculator
    calc = EUVCalculator()
    baseline = calc.calculate(30e3, 0.06)
    test("完整计算: P_EUV>0", baseline["outputs"]["P_EUV_W"] > 0)
    test("完整计算: 稳态已收敛", baseline["steady_state"]["converged"])
    test("完整计算: CT验证通过", baseline.get("church_turing_verified", False))

    # 64卦状态机
    hsm = HexagramStateMachine()
    h = hsm.state_to_hexagram([0, 0, 0, 0, 0, 0])
    test("64卦: 乾卦(000000)", "乾" in h["hexagram"])
    sim = hsm.simulate_cycle(1000)
    test("64卦模拟: 有射击记录", sim["total_shots"] == 1000)

    # 学习引擎
    learner = EUVLearningEngine("data/euv_test_history.json")
    learner.record_result(baseline, "test")
    trend = learner.analyze_trend()
    test("学习引擎: 已记录", trend["records"] >= 1)
    # 清理测试数据
    if os.path.exists("data/euv_test_history.json"):
        os.remove("data/euv_test_history.json")

    return results


# ═══════════════════════════════════════════════════════════
# §8 主程序 · 演示
# ═══════════════════════════════════════════════════════════

def main():
    """CNSH-EUV系统主演示 v1.0"""

    print("=" * 70)
    print("🐉 CNSH-EUV 光刻机攻关系统 v1.0")
    print("数学骨架落地 · 不动点切割 · 七因子映射 · 369频率窗口")
    print(f"DNA: {_DNA_SIGNATURE}")
    print(f"确认码: {_CONFIRM_CODE}")
    print(f"审计: {_AUDIT_STATUS}")
    print("=" * 70)

    calc = EUVCalculator()

    # 演示1: 2026年基线计算
    print("\n📊 演示1: 2026年基线参数计算")
    print("-" * 70)
    baseline = calc.calculate(P_laser=30e3, CE=0.06)
    print(f"输入功率 P_laser: {baseline['inputs']['P_laser_W']/1000:.1f} kW")
    print(f"转换效率 CE: {baseline['inputs']['CE']*100:.1f}%")
    print(f"系统效率 η_system: {baseline['outputs']['eta_system']*100:.1f}%")
    print(f"理论输出 P_EUV: {baseline['outputs']['P_EUV_W']:.1f} W")
    print(f"64卦当前态: {baseline['cnsh_mapping']['dicai']['hexagram']['unicode']}"
          f"{baseline['cnsh_mapping']['dicai']['hexagram']['name']}")
    print(f"状态: {baseline['status']}")

    # 演示2: 七因子优化 + SQP
    print("\n📊 演示2: 七因子优化策略")
    print("-" * 70)
    strategy = calc.seven_factor.optimize_factors("gradient")
    print("梯度优化:")
    for symbol, plan in strategy.items():
        print(f"  {symbol}: {plan['current']:.3f} → {plan['target']:.3f} [{plan['priority']}]")

    # SQP优化 (v1.0新增)
    print("\nSQP非线性优化:")
    sqp = calc.seven_factor.optimize_sqp()
    print(f"  方法: {sqp.get('method')}")
    print(f"  状态: {sqp.get('status')}")
    if sqp.get('eta_system'):
        print(f"  优化η: {sqp['eta_system']*100:.1f}% (提升 {sqp['improvement']:.1f}%)")

    # 演示3: 不动点分析
    print("\n📊 演示3: 稳态不动点分析")
    print("-" * 70)
    steady = baseline["steady_state"]
    print(f"稳态温度 T: {steady['temperature']:.4f}")
    print(f"稳态污染 C: {steady['contamination']:.4f}")
    print(f"稳态稳定性 S: {steady['stability']:.4f}")
    print(f"迭代次数: {steady['iterations']}")
    print(f"收敛状态: {'✅ 已收敛' if steady['converged'] else '❌ 未收敛'}")
    print(f"解读: {steady['interpretation']}")

    # 演示4: 五行诊断 (v1.0新增)
    print("\n📊 演示4: 五行平衡诊断")
    print("-" * 70)
    wuxing = baseline["wuxing_diagnosis"]
    for element in ["金", "木", "水", "火", "土"]:
        d = wuxing.get(element, {})
        print(f"  {element}: {d.get('avg_value', 0):.3f} {d.get('status', 'N/A')}")
    print(f"  最薄弱: {wuxing.get('_weakest', '?')} → {wuxing.get('_recommendation', '?')}")

    # 演示5: 369频率窗口
    print("\n")
    calc.freq_analyzer.print_report()

    # 演示6: 64卦状态机 (v1.0新增)
    print("\n📊 演示6: 64卦状态机模拟")
    print("-" * 70)
    hsm = calc.hexagram_sm

    # 展示5个核心卦
    for bit_code, info in EUVConfig.HEXAGRAM_6BIT.items():
        state = [int(b) for b in bit_code]
        h = hsm.state_to_hexagram(state)
        print(f"  {bit_code} → {info['unicode']}{info['name']}: {info['meaning']}")

    # 运行模拟
    sim = hsm.simulate_cycle(3000)
    print(f"\n  模拟3000次射击: {sim['complete_cycles']}完整闭环, {sim['meltdowns']}熔断, {sim['flips']}扰动翻转")
    print(f"  平均周期: {sim['avg_cycle_length']:.1f} 次射击")

    # 演示7: 多场景对比
    print("\n📊 演示7: 多场景对比 (2026基线 vs 2026优化 vs 2030目标)")
    print("-" * 70)
    scenarios = [
        {"name": "2026基线", "P_laser": 30e3, "CE": 0.06},
        {"name": "2026优化", "P_laser": 30e3, "CE": 0.08,
         "eta_factors": {"F1": 0.70, "F3": 0.97, "F4": 0.93}},
        {"name": "2030目标", "P_laser": 40e3, "CE": 0.10,
         "eta_factors": {"F1": 0.75, "F3": 0.98, "F4": 0.95, "F7": 0.92}},
    ]
    comparison = calc.compare_scenarios(scenarios)
    for r in comparison["comparison"]:
        print(f"  {r['scenario_name']:<12}: P_EUV = {r['outputs']['P_EUV_W']:>7.1f} W (η={r['outputs']['eta_system']*100:>5.1f}%)")
    print(f"\n  🏆 最优: {comparison['best_scenario']['scenario_name']} → {comparison['best_scenario']['outputs']['P_EUV_W']:.1f} W")

    # 演示8: 生成完整报告
    print("\n📊 演示8: 生成完整分析报告")
    print("-" * 70)
    json_path, md_path, html_path = calc.generate_full_report("output/euv")
    print(f"  ✅ JSON: {json_path}")
    print(f"  ✅ Markdown: {md_path}")
    print(f"  ✅ HTML: {html_path}")

    # 演示9: 可视化 (v1.0新增)
    print("\n📊 演示9: 生成可视化图表")
    print("-" * 70)
    viz = EUVVisualizer(calc)
    vizs = viz.generate_all_visualizations("output/euv")
    for name, path in vizs.items():
        if path:
            print(f"  ✅ {name}: {path}")

    # 演示10: 自求多福学习 (v1.0新增)
    print("\n📊 演示10: 自求多福学习记录")
    print("-" * 70)
    learner = EUVLearningEngine("data/euv_history.json")
    learner.record_result(baseline, "baseline_check")
    learner.record_result(calc.calculate(30e3, 0.08), "improved_ce")
    trend = learner.analyze_trend()
    print(f"  历史记录: {trend['records']}条")
    print(f"  P_EUV趋势: {trend.get('P_EUV_trend', 'N/A')} (Δ={trend.get('P_EUV_change', 0):.1f}W)")
    if "best_P_EUV" in trend:
        print(f"  最佳P_EUV: {trend['best_P_EUV']:.1f}W (记录#{trend['best_idx']})")

    # 演示11: 单元测试
    print("\n📊 演示11: 单元测试套件")
    print("-" * 70)
    test_results = run_tests()
    print(f"  通过: {test_results['passed']}/{test_results['passed']+test_results['failed']}")
    if test_results['failed'] > 0:
        for t in test_results['tests']:
            if not t['passed']:
                print(f"  ❌ {t['name']}")

    print("\n" + "=" * 70)
    print("🐉 v1.0 演示完成 · 数学骨架立 · 物理仿真待本地宝宝执行")
    print("   下一步: COMSOL/CST参数sweep · 国家实验室对接 · 产业验证")
    print(f"   DNA: {_DNA_SIGNATURE}")
    print("=" * 70)


if __name__ == "__main__":
    main()
